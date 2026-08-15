#!/usr/bin/env python3
"""Pipeline di trasformazione dei due dataset reali di StreamWave BI.

Legge `data/raw/` in sola lettura e produce quattro CSV sotto `data/processed/`
piu' `reports/cleaning_report.json`, artefatto versionato che misura l'effetto di
ogni decisione di trattamento (feature 003, FR-001 e FR-024).

L'asimmetria che governa lo script: **i dati escono dal repository, i numeri che
li descrivono no**. Gli output non sono versionati (FR-007), quindi chi non puo'
rigenerarli non ha modo di ispezionarli. Il rendiconto e' cio' che li rende
verificabili lo stesso, ed e' la ragione per cui una pipeline di ETL produce un
JSON versionato accanto a CSV che non lo sono.

Nessuna dipendenza esterna: sola libreria standard (decisione T1 di research.md).
Due esecuzioni sugli stessi file di origine producono output identici byte per
byte (FR-003, decisioni T2, T3 e T4).

Stato: fondamenta (task T001-T007). Le trasformazioni vere e proprie entrano da
T008 in avanti; finche' non ci sono, `main()` verifica le sorgenti e si ferma
senza scrivere nulla.

Uso:
    python3 scripts/build_datasets.py
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Il profiler della feature 002 viene **importato**, non riscritto. E' cio' che
# rende il blocco `denominators` un confronto fra due esecuzioni della stessa
# logica invece che fra due implementazioni: una differenza segnalata e' una
# differenza nei dati, mai nell'aritmetica di chi la calcola (decisione T22 in
# corso d'opera, vedi recalculate_profile_values).
import profile_data as profiler  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw"
PROCESSED = REPO / "data" / "processed"
PROFILE = REPO / "reports" / "data_profile.json"
OUT = REPO / "reports" / "cleaning_report.json"

SCHEMA_VERSION = "1"

# Prefisso degli identificativi di questa feature. Disgiunto da `NF.`, `SP.` e
# `X.` del profilo (decisione T8): e' cio' che permette al controllo di coerenza
# di risolvere le ancore su uno spazio di nomi unito senza ambiguita'.
ID_PREFIX = "CL."


# ===========================================================================
# T003 - Convenzioni di trasformazione
#
# Le regole di questa feature rese dato. Finiscono nella chiave `conventions`
# del rendiconto (contratto §2.2): una regola che vive solo nel codice e' una
# regola che chi legge il documento non puo' contestare.
# ===========================================================================

# Decimali a cui ogni valore non intero viene arrotondato prima della
# serializzazione. Stessa regola del profilo: senza, differenze di
# rappresentazione in virgola mobile affiorerebbero nel file e romperebbero il
# determinismo.
ROUNDING_DECIMALS = 4

# --- Decisione ereditata D4: generi a forte concentrazione di zeri ----------
# La soglia e' 50% e non 60%. Il 60% e' un numero tondo, cioe' nessuna ragione.
# Il 50% e' la soglia oltre la quale un genere smette di essere descrivibile
# dalla propria mediana di popolarita': se piu' della meta' delle righe vale
# zero, il valore centrale e' zero qualunque cosa facciano le altre. Non e' una
# proprieta' stimata, e' una proprieta' della definizione di mediana.
ZERO_SHARE_THRESHOLD_PCT = 50.0
ZERO_SHARE_THRESHOLD_RULE = (
    "un genere e' a forte concentrazione di zeri se la quota di righe con "
    "indice di popolarita' pari a zero supera il 50%, calcolata sulla grana "
    "coppia traccia-genere del dataset trasformato"
)

# --- Decisione tecnica T5: repliche discordi su popularity ------------------
# Dove le repliche di una traccia discordano, la grana deduplicata conserva il
# massimo osservato. E' un valore effettivamente presente nella fonte, non un
# aggregato: media e mediana produrrebbero un numero che nessuna riga contiene.
# La regola introduce una distorsione verso l'alto, sistematica per costruzione
# ancorche' minima, e il documento deve dichiararla (FR-019).
POPULARITY_CONFLICT_RULE = (
    "dove le repliche di una stessa traccia discordano sull'indice di "
    "popolarita', la grana traccia conserva il massimo osservato"
)

# --- Decisione ereditata D2: riparazione dello scivolamento di colonna ------
# Tre titoli del catalogo video hanno il campo durata vuoto e, nel campo della
# classificazione per eta', un valore che e' sintatticamente una durata. La
# corrispondenza e' totale in entrambe le direzioni (ritrovamento F1): non
# esiste una riga senza durata con classificazione valida, ne' una riga con
# classificazione fuori dominio che abbia una durata.
#
# Il raggio d'azione e' dichiarato **in anticipo** ed e' verificato come
# invariante (FR-016). Una regola di riparazione senza un limite dichiarato al
# proprio raggio d'azione e' una regola che, su una versione diversa della
# fonte, riscrive dati senza che nessuno se ne accorga.
RATING_SHIFT_PATTERN = re.compile(r"^\d+ min$")
RATING_SHIFT_PATTERN_TEXT = r"^\d+ min$"
RATING_SHIFT_EXPECTED_ROWS = 3
RATING_SHIFT_RULE = (
    "un valore del campo rating che soddisfa la forma di una durata in minuti, "
    "su una riga il cui campo duration e' vuoto, viene spostato nel campo "
    "duration; il campo rating di quella riga e' posto a mancante"
)

# --- Decisione tecnica T6: conversione di date_added ------------------------
# Mappa esplicita dei dodici mesi. **Mai** `strptime` con `%B`, che dipende dal
# locale del sistema: funziona sotto locale C o inglese e fallisce sotto locale
# italiano. Una pipeline che lo usasse produrrebbe risultati diversi su macchine
# diverse, cioe' violerebbe FR-003 in un modo che non si manifesta sulla
# macchina di chi la scrive (ritrovamento F6).
MONTHS = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
}

MISSING_DEFINITION = "campo assente, stringa vuota o composta di soli spazi"


# ===========================================================================
# T005 - Parametri di scrittura CSV
#
# I quattro parametri che decidono se FR-003 e' vero. Vanno scritti invece che
# ereditati: il default del modulo `csv` e' `\r\n`, che produrrebbe file diversi
# da quelli attesi e diff rumorosi.
# ===========================================================================

CSV_LINETERMINATOR = "\n"
CSV_ENCODING = "utf-8"
CSV_QUOTING = csv.QUOTE_MINIMAL


# ===========================================================================
# T004 - Sorgenti attese
# ===========================================================================

NETFLIX_FILE = "netflix_titles.csv"
SPOTIFY_FILE = "spotify_tracks_dataset.csv"

NETFLIX_COLUMNS = (
    "show_id", "type", "title", "director", "cast", "country",
    "date_added", "release_year", "rating", "duration", "listed_in",
    "description",
)

SPOTIFY_COLUMNS = (
    "track_id", "artists", "album_name", "track_name", "popularity",
    "duration_ms", "explicit", "danceability", "energy", "key", "loudness",
    "mode", "speechiness", "acousticness", "instrumentalness", "liveness",
    "valence", "tempo", "time_signature", "track_genre",
)


# ===========================================================================
# T006 - Formattazione
#
# La forma con cui un valore va scritto nel documento vive qui e in nessun
# altro posto. Stessa decisione della 002 (sua D3): il controllo di coerenza
# confronta stringhe, non interpreta la formattazione italiana dei numeri.
# ===========================================================================


def _it(number: str) -> str:
    """Converte la punteggiatura anglosassone di un numero gia' formattato."""
    return number.translate(str.maketrans({",": ".", ".": ","}))


def fmt_int(value: int) -> str:
    return _it(f"{value:,}")


def fmt_dec(value: float, decimals: int) -> str:
    return _it(f"{value:,.{decimals}f}")


def slug(text: str) -> str:
    out = re.sub(r"[^a-z0-9]+", "_", text.strip().lower()).strip("_")
    return out or "unnamed"


def is_missing(raw) -> bool:
    return raw is None or str(raw).strip() == ""


# ===========================================================================
# T007 - Invarianti
#
# Sette affermazioni che la ricognizione di Fase 0 ha verificato sui dati.
# Scritte come commenti sarebbero opinioni; scritte come controlli sono cio'
# che impedisce alla pipeline di riscrivere dati in silenzio quando la fonte
# cambia. E' il vincolo che rende difendibile la decisione ereditata D2 e che
# qui si generalizza (decisione T10).
# ===========================================================================


class InvariantViolation(SystemExit):
    """Interruzione per invariante violata. Nessun output e' stato scritto."""


class Invariants:
    """Registro delle invarianti verificate a ogni esecuzione."""

    def __init__(self) -> None:
        self.checked: list[str] = []

    def require(self, condition: bool, name: str, expected, found) -> None:
        """Asserisce una invariante e ferma l'esecuzione se non regge.

        Il messaggio nomina l'invariante, l'atteso e il trovato: un errore che
        dice soltanto "controllo fallito" costringe chi lo riceve a rileggere
        lo script per sapere che cosa e' andato storto.

        Nessun output parziale sopravvive alla violazione (FR-004), e la
        garanzia e' strutturale e non procedurale: gli output sono raccolti in
        memoria da `OutputWriter` e scritti soltanto quando l'ultima invariante
        e' passata. Se l'esecuzione si ferma qui, su disco non c'e' nulla da
        ripulire.
        """
        if not condition:
            raise InvariantViolation(
                f"ERRORE: invariante violata: {name}\n"
                f"        atteso : {expected}\n"
                f"        trovato: {found}\n"
                f"        Nessun output e' stato scritto. La fonte e' cambiata "
                f"rispetto a cio' che la feature 003 ha verificato, oppure la "
                f"regola non copre piu' il caso: correggere la pipeline, non i "
                f"dati."
            )
        self.checked.append(name)


# ===========================================================================
# T004 - Lettura delle sorgenti e verifica della provenienza
# ===========================================================================


def load(path: Path, expected_columns: tuple) -> tuple[list[dict], list[str]]:
    """Legge un CSV in sola lettura, fallendo esplicitamente su input mancante.

    FR-004: se un file manca o una colonna attesa e' assente, ci si ferma con un
    errore che la nomina. `data/raw/` non viene mai aperta in scrittura
    (principio II, FR-002).
    """
    if not path.exists():
        raise SystemExit(
            f"ERRORE: file di origine mancante: {path.relative_to(REPO)}\n"
            f"        data/raw/ non e' versionata. Ricostruiscila con "
            f"./scripts/download_data.sh (richiede un token Kaggle)."
        )
    csv.field_size_limit(10 ** 9)
    with path.open(newline="", encoding=CSV_ENCODING) as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    missing = [c for c in expected_columns if c not in fields]
    if missing:
        raise SystemExit(
            f"ERRORE: colonne attese assenti in {path.relative_to(REPO)}: "
            f"{', '.join(missing)}\n"
            f"        Nessun output viene prodotto: correggere lo script o "
            f"verificare la sorgente."
        )
    return rows, fields


def fingerprint(path: Path) -> dict:
    """Provenienza della sorgente: nome, byte, impronta del contenuto."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return {
        "file": str(path.relative_to(REPO)),
        "bytes": path.stat().st_size,
        "sha256": digest.hexdigest(),
    }


def load_profile() -> dict:
    """Carica `reports/data_profile.json`, prodotto dalla feature 002.

    E' un ingresso obbligatorio e non un ausilio: la pipeline ne legge le
    convenzioni, ne confronta le impronte e ne cita gli identificativi nel
    blocco dei denominatori.
    """
    if not PROFILE.exists():
        raise SystemExit(
            f"ERRORE: profilo mancante: {PROFILE.relative_to(REPO)}\n"
            f"        E' l'artefatto della feature 002 ed e' versionato: se "
            f"manca, il repository non e' integro."
        )
    with PROFILE.open(encoding="utf-8") as handle:
        return json.load(handle)


def verify_sources(profile: dict, invariants: Invariants) -> list[dict]:
    """Confronta le sorgenti lette con quelle che il profilo descrive.

    Non e' un blocco pedante. Se le impronte divergono, ogni identificativo del
    profilo che il documento cita descrive **altri dati**, e l'intero impianto
    di tracciabilita' dice il falso senza accorgersene (decisione T10,
    data-model §1).
    """
    declared = {entry["file"]: entry for entry in profile.get("sources", [])}
    observed = []
    for name in (NETFLIX_FILE, SPOTIFY_FILE):
        current = fingerprint(RAW / name)
        key = current["file"]
        expected = declared.get(key)
        invariants.require(
            expected is not None,
            f"la sorgente {key} e' descritta dal profilo",
            f"una voce per {key} in sources di data_profile.json",
            "nessuna voce",
        )
        invariants.require(
            expected["sha256"] == current["sha256"],
            f"l'impronta di {key} coincide con quella del profilo",
            f"sha256 {expected['sha256'][:16]}... ({expected['bytes']} byte)",
            f"sha256 {current['sha256'][:16]}... ({current['bytes']} byte)",
        )
        observed.append(current)
    return observed


# ===========================================================================
# T006 - Registro dei valori di rendicontazione
# ===========================================================================


class CleaningReport:
    """Raccoglie i valori di rendicontazione e li serializza in modo deterministico.

    Stessa forma del record di valore del profilo (contratto della 002 §2), con
    prefisso `CL.`. La disgiunzione dei prefissi non viene assunta: viene
    verificata contro gli identificativi del profilo effettivamente presenti
    (decisione T8), perche' il controllo di coerenza risolve le ancore su uno
    spazio di nomi unito e una collisione lo farebbe puntare al valore sbagliato
    senza segnalare nulla.
    """

    def __init__(self, profile: dict, invariants: Invariants) -> None:
        self.values: dict[str, dict] = {}
        self.catalogs: dict[str, list] = {}
        self.denominators: list[dict] = []
        self._profile_ids = set(profile.get("values", {}))
        self._invariants = invariants
        self._invariants.require(
            not any(vid.startswith(ID_PREFIX) for vid in self._profile_ids),
            f"nessun identificativo del profilo usa il prefisso {ID_PREFIX}",
            f"zero identificativi {ID_PREFIX}* in data_profile.json",
            f"{sum(1 for v in self._profile_ids if v.startswith(ID_PREFIX))} trovati",
        )

    def add(
        self,
        vid: str,
        value,
        display: str,
        unit: str,
        dataset: str,
        label: str,
        field=None,
        granularity=None,
    ) -> str:
        if not vid.startswith(ID_PREFIX):
            raise ValueError(
                f"identificativo senza prefisso {ID_PREFIX}: {vid}"
            )
        if vid in self.values:
            raise ValueError(f"identificativo duplicato: {vid}")
        if vid in self._profile_ids:
            raise ValueError(
                f"identificativo in collisione con il profilo: {vid}"
            )
        if isinstance(value, float):
            value = round(value, ROUNDING_DECIMALS)
        self.values[vid] = {
            "value": value,
            "display": display,
            "unit": unit,
            "dataset": dataset,
            "field": field,
            "granularity": granularity,
            "label": label,
        }
        return vid

    def count(self, vid, value, dataset, label, field=None, granularity=None) -> str:
        return self.add(
            vid, int(value), fmt_int(int(value)), "conteggio", dataset, label,
            field, granularity,
        )

    def pct(self, vid, value, dataset, label, field=None, granularity=None, decimals=2) -> str:
        return self.add(
            vid, float(value), fmt_dec(float(value), decimals) + "%", "percentuale",
            dataset, label, field, granularity,
        )

    def num(self, vid, value, unit, dataset, label, field=None, granularity=None, decimals=2) -> str:
        return self.add(
            vid, float(value), fmt_dec(float(value), decimals), unit, dataset,
            label, field, granularity,
        )

    def denominator(self, profile_id: str, cleaning_id: str, reason: str, scope: str) -> None:
        """Registra un valore del profilo che dopo la trasformazione non vale piu'.

        E' il blocco che realizza FR-030, e l'unico di questo artefatto che
        esista per proteggere qualcuno che non e' ancora entrato nel progetto:
        senza, a valle si citerebbe il valore del profilo credendo di citare
        quello del dato trasformato.
        """
        if profile_id not in self._profile_ids:
            raise ValueError(
                f"denominatore su identificativo di profilo inesistente: {profile_id}"
            )
        if cleaning_id not in self.values:
            raise ValueError(
                f"denominatore su identificativo di rendiconto inesistente: {cleaning_id}"
            )
        self.denominators.append({
            "profile_id": profile_id,
            "cleaning_id": cleaning_id,
            "reason": reason,
            "scope": scope,
        })


# ===========================================================================
# T005 - Scrittura deterministica e differita
# ===========================================================================


class OutputWriter:
    """Raccoglie gli output e li scrive solo quando tutto il resto e' passato.

    La scrittura differita e' cio' che rende strutturale la garanzia di FR-004:
    una pipeline che scrivesse i file man mano lascerebbe output parziali a ogni
    invariante violata a meta' strada, e la promessa "non produce output
    parziali" sarebbe una questione di disciplina invece che di forma.

    L'impronta registrata in `outputs` e' calcolata sui **byte effettivamente
    scritti**, non sui dati in memoria: e' cio' che rende la verifica di SC-003
    una verifica e non un giro a vuoto.
    """

    def __init__(self, destination: Path) -> None:
        self.destination = destination
        self._pending: list[tuple[str, bytes, int, int]] = []
        self._rows: list[tuple[str, list[dict]]] = []

    def add(self, filename: str, fieldnames: list[str], rows: list[dict]) -> None:
        buffer = io.StringIO(newline="")
        writer = csv.DictWriter(
            buffer,
            fieldnames=fieldnames,
            lineterminator=CSV_LINETERMINATOR,
            quoting=CSV_QUOTING,
            extrasaction="raise",
        )
        writer.writeheader()
        writer.writerows(rows)
        payload = buffer.getvalue().encode(CSV_ENCODING)
        self._pending.append((filename, payload, len(rows), len(fieldnames)))
        self._rows.append((filename, rows))

    def validate(self, schemas: dict, invariants: Invariants) -> None:
        """T024 - verifica i tipi dichiarati su **ogni** output, prima di scrivere.

        Un tipo che si scopre sbagliato leggendo il file e' un tipo che qualcuno
        ha gia' letto. La validazione sta qui perche' la scrittura e' differita:
        e' l'unico punto in cui tutti e quattro gli output esistono e nessuno e'
        ancora su disco.
        """
        invariants.require(
            {name for name, _ in self._rows} == set(schemas),
            "ogni output prodotto ha un tipo dichiarato nel contratto",
            f"schemi per {sorted(schemas)}",
            f"output prodotti: {sorted(name for name, _ in self._rows)}",
        )
        for filename, rows in self._rows:
            validate_types(filename, rows, schemas[filename], invariants)

    def flush(self) -> list[dict]:
        """Scrive gli output e restituisce il blocco `outputs` del rendiconto."""
        self.destination.mkdir(parents=True, exist_ok=True)
        written = []
        for filename, payload, rows, columns in self._pending:
            path = self.destination / filename
            # Scrittura atomica: chi legge non incontra mai un file a meta'.
            tmp = path.with_suffix(path.suffix + ".tmp")
            tmp.write_bytes(payload)
            tmp.replace(path)
            written.append({
                "path": str(path.relative_to(REPO)),
                "rows": rows,
                "columns": columns,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            })
        return written


def write_report(report: CleaningReport, sources: list[dict], outputs: list[dict]) -> None:
    """Serializza `reports/cleaning_report.json` con le regole del profilo.

    Chiavi ordinate, nessun timestamp di esecuzione, indentazione fissa, UTF-8
    senza escape, ritorno a capo finale (FR-003).
    """
    artifact = {
        "schema_version": SCHEMA_VERSION,
        "conventions": {
            "missing": MISSING_DEFINITION,
            "rounding_decimals": ROUNDING_DECIMALS,
            "zero_share_threshold_pct": ZERO_SHARE_THRESHOLD_PCT,
            "zero_share_threshold_rule": ZERO_SHARE_THRESHOLD_RULE,
            "popularity_conflict_rule": POPULARITY_CONFLICT_RULE,
            "rating_shift_pattern": RATING_SHIFT_PATTERN_TEXT,
            "rating_shift_expected_rows": RATING_SHIFT_EXPECTED_ROWS,
            "rating_shift_rule": RATING_SHIFT_RULE,
            "months": dict(sorted(MONTHS.items())),
            "csv_lineterminator": "\\n",
            "csv_encoding": CSV_ENCODING,
        },
        "sources": sources,
        "values": report.values,
        "catalogs": report.catalogs,
        "outputs": outputs,
        "denominators": report.denominators,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(artifact, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


# ===========================================================================
# T008-T011 - Trasformazioni del catalogo video
#
# Nota sull'ordine di esecuzione, che **non** segue la numerazione dei task.
# La riparazione (T009) precede la separazione delle durate (T008), perche'
# l'invariante di T008 — ogni titolo ha una durata e la sua unita' corrisponde
# al tipo — vale soltanto dopo che le tre righe di F1 hanno riavuto la propria.
# Eseguita prima, la separazione troverebbe tre film senza durata e dovrebbe
# tollerarli: una invariante che tollera l'eccezione che dovrebbe intercettare
# non e' una invariante.
# ===========================================================================

# Le due sole forme che il campo `duration` assume (ritrovamento F5).
DURATION_MINUTES = re.compile(r"^(\d+) min$")
DURATION_SEASONS = re.compile(r"^(\d+) Seasons?$")

# Forma testuale inglese di `date_added`: "September 25, 2021".
DATE_ADDED_PATTERN = re.compile(r"^([A-Za-z]+) (\d{1,2}), (\d{4})$")


def repair_rating_shift(records: list[dict], invariants: Invariants) -> list[dict]:
    """T009 - Decisione ereditata D2: riparazione dello scivolamento di colonna.

    Tre movimenti, e il secondo e' quello che va difeso: il valore sintatticamente
    di durata viene **spostato** nel campo durata; il campo della classificazione
    di quelle righe e' posto a **mancante**, perche' il valore corretto e' andato
    perso nella fonte e inventarlo sarebbe l'unica cosa peggiore che perderlo; le
    righe restano nel dataset e portano un indicatore.

    Le tre invarianti che rendono la riparazione difendibile verificano la
    corrispondenza di F1 **in entrambe le direzioni**: non basta che le righe da
    riparare siano tre, serve che l'insieme delle righe senza durata e quello
    delle righe con classificazione a forma di durata siano lo stesso insieme.
    Se su una versione diversa della fonte divergessero, la regola starebbe
    riscrivendo dati che non ha verificato.
    """
    no_duration = {r["show_id"] for r in records if is_missing(r["duration"])}
    shaped_rating = {
        r["show_id"] for r in records
        if RATING_SHIFT_PATTERN.match((r["rating"] or "").strip())
    }

    invariants.require(
        len(no_duration) == RATING_SHIFT_EXPECTED_ROWS,
        "i titoli privi di durata sono quelli attesi dalla regola di riparazione",
        f"{RATING_SHIFT_EXPECTED_ROWS} titoli (NF.duration.missing del profilo)",
        f"{len(no_duration)} titoli",
    )
    invariants.require(
        no_duration == shaped_rating,
        "ogni titolo privo di durata ha una classificazione a forma di durata, e viceversa",
        "i due insiemi coincidono (ritrovamento F1)",
        f"solo senza durata: {sorted(no_duration - shaped_rating)}; "
        f"solo con classificazione a forma di durata: {sorted(shaped_rating - no_duration)}",
    )

    repaired = []
    for rec in records:
        if rec["show_id"] not in no_duration:
            rec["is_repaired_duration"] = "False"
            continue
        moved = (rec["rating"] or "").strip()
        rec["duration"] = moved
        rec["rating"] = ""
        rec["is_repaired_duration"] = "True"
        repaired.append({"show_id": rec["show_id"], "moved_value": moved})

    invariants.require(
        len(repaired) == RATING_SHIFT_EXPECTED_ROWS,
        "la riparazione tocca esattamente il raggio d'azione dichiarato",
        f"{RATING_SHIFT_EXPECTED_ROWS} righe",
        f"{len(repaired)} righe",
    )
    return sorted(repaired, key=lambda e: e["show_id"])


def enforce_rating_domain(
    records: list[dict], profile: dict, invariants: Invariants
) -> list[str]:
    """T010 - FR-015: controllo di dominio sulla classificazione per eta'.

    Operazione **distinta** dalla riparazione di T009, e non la sua conseguenza
    automatica. Porre a mancante un valore fuori da un dominio gia' dichiarato e
    versionato (`conventions.rating_domain` del profilo) e' un controllo
    meccanico, verificabile e ripetibile da chiunque. Spostare un valore in un
    altro campo e' un'inferenza sulla fonte. E' su questa distinzione che poggia
    tutta la difesa di D2, quindi le due operazioni restano separate anche nel
    codice.

    Dopo la riparazione il residuo atteso e' **zero**, e lo zero va comunque
    prodotto: chi legge non puo' distinguere "non e' stato necessario" da "non
    e' stato fatto" se il valore non c'e' (data-model §2).
    """
    domain = set(profile["conventions"]["rating_domain"])
    invariants.require(
        bool(domain),
        "il profilo dichiara il dominio della classificazione per eta'",
        "conventions.rating_domain non vuoto",
        "dominio assente o vuoto",
    )

    blanked = []
    for rec in records:
        value = (rec["rating"] or "").strip()
        if not value:
            rec["rating"] = ""
            continue
        if value not in domain:
            rec["rating"] = ""
            blanked.append(value)
        else:
            rec["rating"] = value
    return sorted(blanked)


def split_duration(records: list[dict], invariants: Invariants) -> None:
    """T008 - FR-014: separazione della durata in due campi tipizzati e distinti.

    Minuti per i film, stagioni per le serie. La pipeline **non** li rende
    confrontabili e non li aggrega: sono due unita' non convertibili, e che il
    lato serie resti fuori da `BQ1-K2` e' la decisione D3 della 001, che questa
    feature cita e non riformula.

    E' una verifica, non una deduzione dalla stringa (ritrovamento F5). Se la
    corrispondenza fra tipo e unita' non regge, la fonte e' cambiata e la
    pipeline si ferma invece di indovinare.
    """
    unresolved = []
    for rec in records:
        raw = (rec["duration"] or "").strip()
        minutes = DURATION_MINUTES.match(raw)
        seasons = DURATION_SEASONS.match(raw)
        if minutes:
            rec["movie_duration_min"], rec["tvshow_seasons"] = minutes.group(1), ""
        elif seasons:
            rec["movie_duration_min"], rec["tvshow_seasons"] = "", seasons.group(1)
        else:
            rec["movie_duration_min"], rec["tvshow_seasons"] = "", ""
            unresolved.append((rec["show_id"], raw))

    invariants.require(
        not unresolved,
        "ogni durata assume una delle due forme riconosciute",
        "zero durate in forma non riconosciuta, dopo la riparazione di D2",
        f"{len(unresolved)} non riconosciute: {unresolved[:5]}",
    )

    wrong_unit = [
        (rec["show_id"], rec["type"], rec["duration"])
        for rec in records
        if (rec["type"] == "Movie") != bool(rec["movie_duration_min"])
    ]
    invariants.require(
        not wrong_unit,
        "l'unita' della durata corrisponde al tipo del titolo",
        "ogni Movie porta minuti, ogni TV Show porta stagioni",
        f"{len(wrong_unit)} titoli con unita' incoerente: {wrong_unit[:5]}",
    )


def convert_date_added(records: list[dict], invariants: Invariants) -> dict:
    """T011 - Decisione tecnica T6: conversione di `date_added` in ISO 8601.

    Usa la mappa esplicita dei mesi di T003. **Vietato** `strptime` con `%B`: e'
    dipendente dal locale, funziona sotto locale C o inglese e fallisce sotto
    locale italiano. Sarebbe una violazione di FR-003 che non si manifesta sulla
    macchina di chi scrive la pipeline e si manifesta su quella di chi la
    riesegue — cioe' il caso peggiore, perche' rompe esattamente la promessa che
    la feature esiste per mantenere (ritrovamento F6).

    Gli 88 valori con spazio iniziale vengono normalizzati; i valori vuoti
    restano vuoti e **non** vengono imputati.
    """
    trimmed = converted = missing = 0
    unresolved = []
    for rec in records:
        raw = rec["date_added"] or ""
        if raw != raw.strip():
            trimmed += 1
        value = raw.strip()
        if not value:
            rec["date_added"] = ""
            missing += 1
            continue
        match = DATE_ADDED_PATTERN.match(value)
        month = MONTHS.get(match.group(1)) if match else None
        if month is None:
            rec["date_added"] = ""
            unresolved.append((rec["show_id"], value))
            continue
        rec["date_added"] = f"{int(match.group(3)):04d}-{month:02d}-{int(match.group(2)):02d}"
        converted += 1

    invariants.require(
        not unresolved,
        "ogni data valorizzata e' riconosciuta dalla mappa esplicita dei mesi",
        "zero date in forma non riconosciuta",
        f"{len(unresolved)} non riconosciute: {unresolved[:5]}",
    )
    return {"trimmed": trimmed, "converted": converted, "missing": missing}


def transform_netflix(
    rows: list[dict], profile: dict, report: CleaningReport, invariants: Invariants
) -> list[dict]:
    """Applica al catalogo video le quattro trasformazioni di T008-T011.

    Lavora su copie: le righe lette da `data/raw/` non vengono mutate, cosi' come
    non viene toccato il file (principio II, FR-002).
    """
    records = [dict(row) for row in rows]

    repaired = repair_rating_shift(records, invariants)          # T009
    blanked = enforce_rating_domain(records, profile, invariants)  # T010
    split_duration(records, invariants)                            # T008
    dates = convert_date_added(records, invariants)                # T011

    movies = sum(1 for r in records if r["movie_duration_min"])
    tvshows = sum(1 for r in records if r["tvshow_seasons"])
    rating_missing = sum(1 for r in records if not r["rating"])

    report.count(
        "CL.NF.duration.repaired.rows", len(repaired), "netflix",
        "righe con la durata recuperata dal campo di classificazione",
        field="duration", granularity="titolo",
    )
    report.count(
        "CL.NF.rating.out_of_domain.blanked", len(blanked), "netflix",
        "valori di classificazione fuori dominio posti a mancante, oltre a "
        "quelli gia' svuotati dalla riparazione",
        field="rating", granularity="titolo",
    )
    report.count(
        "CL.NF.rating.missing.after", rating_missing, "netflix",
        "valori mancanti nel campo rating dopo la trasformazione",
        field="rating", granularity="titolo",
    )
    report.count(
        "CL.NF.duration.movie.count.after", movies, "netflix",
        "film con durata in minuti valorizzata dopo la trasformazione",
        field="movie_duration_min", granularity="titolo",
    )
    report.count(
        "CL.NF.duration.tvshow.count.after", tvshows, "netflix",
        "serie con numero di stagioni valorizzato dopo la trasformazione",
        field="tvshow_seasons", granularity="titolo",
    )
    report.count(
        "CL.NF.date_added.trimmed", dates["trimmed"], "netflix",
        "valori di date_added con spazio iniziale normalizzato",
        field="date_added", granularity="titolo",
    )
    report.count(
        "CL.NF.date_added.converted", dates["converted"], "netflix",
        "valori di date_added convertiti in forma ISO 8601",
        field="date_added", granularity="titolo",
    )
    report.count(
        "CL.NF.date_added.missing", dates["missing"], "netflix",
        "valori di date_added vuoti, lasciati vuoti e non imputati",
        field="date_added", granularity="titolo",
    )

    report.catalogs["netflix_repaired_titles"] = [e["show_id"] for e in repaired]
    report.catalogs["netflix_repaired_values"] = sorted(e["moved_value"] for e in repaired)
    report.catalogs["netflix_rating_blanked_values"] = blanked

    return records


# ===========================================================================
# T012-T013 - Output del catalogo video
#
# I due file escono dal repository: `.gitignore` li intercetta e nessuno li
# versiona (FR-007). Cio' che resta tracciato e' la pipeline che li produce e,
# da T020, il rendiconto che li misura.
# ===========================================================================

# Ordine dei campi secondo contracts/output-datasets.md §1.1. E' parte del
# contratto: cambiarlo cambia il file, e il file e' cio' che la feature 005
# leggera' senza poter chiedere spiegazioni.
NETFLIX_TITLE_FIELDS = (
    "show_id", "type", "title", "director", "cast", "country",
    "date_added", "release_year", "rating", "movie_duration_min",
    "tvshow_seasons", "listed_in", "description", "is_repaired_duration",
)

NETFLIX_CATEGORY_FIELDS = ("show_id", "category")


def build_netflix_titles(
    records: list[dict], profile: dict, writer: OutputWriter,
    report: CleaningReport, invariants: Invariants,
) -> None:
    """T012 - `netflix_titles.csv`, grana titolo.

    Nessuna riga eliminata, per alcuna ragione (FR-017): un titolo senza durata
    resta un titolo del catalogo, e toglierlo cambierebbe il denominatore della
    North Star `BQ1-K1`. Il conteggio si verifica contro il profilo invece di
    essere dato per scontato.

    Il campo `listed_in` resta qui **come stringa di sorgente**, accanto alla
    tabella normalizzata di T013. Rimuoverlo obbligherebbe chi legge il solo
    dataset alla grana titolo a fare una giunzione per sapere di che cosa parla
    un titolo; conservarlo non crea ambiguita' purche' nessuno lo conti, ed e'
    la regola di lettura dichiarata nel contratto §1.
    """
    expected_rows = int(profile["values"]["NF.shape.rows"]["value"])
    invariants.require(
        len(records) == expected_rows,
        "nessuna riga del catalogo video e' stata eliminata",
        f"{expected_rows} titoli (NF.shape.rows del profilo)",
        f"{len(records)} titoli",
    )

    keys = [rec["show_id"] for rec in records]
    invariants.require(
        len(set(keys)) == len(keys),
        "la grana di netflix_titles.csv e' unica su show_id",
        "zero chiavi ripetute",
        f"{len(keys) - len(set(keys))} chiavi ripetute",
    )

    rows = [{field: rec[field] for field in NETFLIX_TITLE_FIELDS} for rec in records]
    writer.add("netflix_titles.csv", list(NETFLIX_TITLE_FIELDS), rows)

    report.count(
        "CL.NF.titles.rows.after", len(rows), "netflix",
        "righe di netflix_titles.csv, alla grana titolo",
        granularity="titolo",
    )


def build_netflix_title_category(
    records: list[dict], profile: dict, writer: OutputWriter,
    report: CleaningReport, invariants: Invariants,
) -> None:
    """T013 - `netflix_title_category.csv`, grana titolo-categoria.

    Normalizza il **solo** campo delle categorie (FR-012, decisione T7). Il
    campo e' multi-valore e i conteggi per categoria non sono sommabili sul
    totale del catalogo: `BQ1-K1` conta titoli per categoria ed e' il caso in cui
    un totale ingenuo sbaglia. `country`, `cast` e `director` sono anch'essi
    multi-valore ma nessuna misura del framework li consuma, e normalizzarli
    produrrebbe tre tabelle senza lettore.

    Il numero di righe di questo file e' il numero di **assegnazioni**, non di
    titoli, e si verifica contro `NF.cat.assignments` del profilo.

    Non e' una tabella ponte del modello dati. Ne ha la forma, ma nessuno ha
    ancora deciso se `category` sara' una dimensione ne' con quale chiave: e'
    la feature 005 (FR-046).
    """
    rows = []
    empty_segments = 0
    repeated_within_title = []
    for rec in records:
        seen = set()
        for raw in rec["listed_in"].split(","):
            category = raw.strip()
            if not category:
                empty_segments += 1
                continue
            if category in seen:
                repeated_within_title.append((rec["show_id"], category))
                continue
            seen.add(category)
            rows.append({"show_id": rec["show_id"], "category": category})

    invariants.require(
        empty_segments == 0,
        "la separazione delle categorie non produce segmenti vuoti",
        "zero segmenti vuoti",
        f"{empty_segments} segmenti vuoti",
    )
    invariants.require(
        not repeated_within_title,
        "nessun titolo elenca due volte la stessa categoria",
        "zero ripetizioni entro il titolo",
        f"{len(repeated_within_title)} ripetizioni: {repeated_within_title[:5]}",
    )

    keys = [(r["show_id"], r["category"]) for r in rows]
    invariants.require(
        len(set(keys)) == len(keys),
        "la grana di netflix_title_category.csv e' unica su show_id + category",
        "zero chiavi ripetute",
        f"{len(keys) - len(set(keys))} chiavi ripetute",
    )

    expected_assignments = int(profile["values"]["NF.cat.assignments"]["value"])
    invariants.require(
        len(rows) == expected_assignments,
        "le assegnazioni di categoria coincidono con quelle del profilo",
        f"{expected_assignments} assegnazioni (NF.cat.assignments del profilo)",
        f"{len(rows)} assegnazioni",
    )

    categories = sorted({r["category"] for r in rows})
    expected_categories = int(profile["values"]["NF.cat.count"]["value"])
    invariants.require(
        len(categories) == expected_categories,
        "le categorie distinte coincidono con quelle del profilo",
        f"{expected_categories} categorie (NF.cat.count del profilo)",
        f"{len(categories)} categorie",
    )

    writer.add("netflix_title_category.csv", list(NETFLIX_CATEGORY_FIELDS), rows)

    report.count(
        "CL.NF.category.assignments", len(rows), "netflix",
        "assegnazioni di categoria, alla grana titolo-categoria",
        field="listed_in", granularity="titolo-categoria",
    )
    report.count(
        "CL.NF.category.distinct", len(categories), "netflix",
        "categorie distinte presenti nella tabella normalizzata",
        field="listed_in", granularity="titolo-categoria",
    )
    report.catalogs["netflix_categories_normalized"] = categories

    # Decisione tecnica T7, dichiarata con i suoi numeri: dei quattro campi
    # multi-valore del catalogo video ne viene normalizzato **uno**. Gli altri
    # tre non alimentano alcuna misura del framework, e normalizzarli
    # produrrebbe tre tabelle senza lettore. Chi in futuro volesse contare
    # titoli per paese incontrera' lo stesso problema di sommabilita', non
    # risolto: va scritto perche' sia una scelta nota e non una svista.
    not_normalized = ["cast", "country", "director"]
    report.count(
        "CL.NF.multivalue.fields_normalized", 1, "netflix",
        "campi multi-valore del catalogo video normalizzati in una tabella propria",
        granularity="campo",
    )
    report.count(
        "CL.NF.multivalue.fields_not_normalized", len(not_normalized), "netflix",
        "campi multi-valore lasciati come stringa di sorgente",
        granularity="campo",
    )
    report.catalogs["netflix_multivalue_not_normalized"] = not_normalized
    return rows


# ===========================================================================
# T014-T019 - Trasformazioni e output del catalogo musicale
#
# Due grane, non intercambiabili, ed e' il ritrovamento centrale dell'audit
# della 002: la riga della fonte non e' la traccia. La feature ne consegna due
# output distinti e non sceglie per conto di nessuno quale usare — salvo il
# vincolo posto dalla decisione ereditata D3, che i totali di catalogo si
# calcolano sulla grana traccia.
# ===========================================================================

# Campi di sorgente riportati negli output, nell'ordine della fonte. La prima
# colonna del catalogo musicale, priva di nome, resta fuori (decisione T11): e'
# l'indice di riga dell'esportazione, non un dato. Trasportarla produrrebbe una
# colonna che invita a essere usata come chiave e che non lo e' — dopo la
# deduplicazione non sarebbe nemmeno piu' contigua.
SPOTIFY_SOURCE_FIELDS = SPOTIFY_COLUMNS

# Contratto §1.3: grana coppia traccia-genere.
SPOTIFY_PAIR_FIELDS = SPOTIFY_SOURCE_FIELDS + (
    "is_popularity_zero", "is_duration_zero", "is_high_zero_genre",
)

# Contratto §1.4: grana traccia. Perde `track_genre` e `is_high_zero_genre`,
# che sono proprieta' del genere e non della traccia, e guadagna due colonne
# che esistono solo a questa grana.
SPOTIFY_TRACK_FIELDS = tuple(
    f for f in SPOTIFY_SOURCE_FIELDS if f != "track_genre"
) + ("is_popularity_zero", "is_duration_zero", "genre_count",
     "has_conflicting_popularity")


def _flag(condition: bool) -> str:
    """Rappresentazione dei booleani negli output, allineata alla fonte.

    Il campo `explicit` arriva gia' come `True`/`False`: le colonne aggiunte
    usano la stessa forma invece di introdurne una seconda nello stesso file.
    """
    return "True" if condition else "False"


def deduplicate_pairs(
    rows: list[dict], invariants: Invariants
) -> tuple[list[dict], int, int]:
    """T014 - Ritrovamento F2: la grana coppia traccia-genere non e' unica.

    Quattrocentoquarantaquattro coppie compaiono piu' di una volta, per 450
    righe eccedenti. FR-011 chiede che ogni output verifichi la propria grana:
    su questa la verifica **fallirebbe** se la pipeline si limitasse a
    trasportare le righe.

    La deduplicazione e' priva di perdita, ma non lo si assume: si verifica che
    le repliche di una stessa coppia siano identiche su **ogni** attributo prima
    di scartarle. Se su una versione diversa della fonte divergessero, scartarle
    butterebbe via informazione, e la pipeline si ferma invece di farlo.

    Sopravvive la prima occorrenza, e l'ordine di sorgente e' conservato
    (decisione T3).
    """
    grouped: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["track_id"], row["track_genre"]), []).append(row)

    conflicting = []
    for key, replicas in grouped.items():
        if len(replicas) == 1:
            continue
        for field in SPOTIFY_SOURCE_FIELDS:
            if len({r[field] for r in replicas}) > 1:
                conflicting.append((key, field))

    invariants.require(
        not conflicting,
        "le repliche di una stessa coppia traccia-genere sono identiche",
        "zero attributi discordi fra le repliche (ritrovamento F2)",
        f"{len(conflicting)} discordanze: {conflicting[:5]}",
    )

    duplicate_pairs = sum(1 for r in grouped.values() if len(r) > 1)
    removed = len(rows) - len(grouped)

    seen: set[tuple[str, str]] = set()
    kept = []
    for row in rows:
        key = (row["track_id"], row["track_genre"])
        if key in seen:
            continue
        seen.add(key)
        kept.append(dict(row))

    invariants.require(
        len(kept) == len(grouped),
        "la deduplicazione di coppia conserva una riga per coppia distinta",
        f"{len(grouped)} coppie distinte",
        f"{len(kept)} righe conservate",
    )
    return kept, duplicate_pairs, removed


def mark_degenerate_values(records: list[dict]) -> tuple[int, int]:
    """T015 - Decisione ereditata D1 e FR-023: si marca, non si elimina.

    Zero e' un valore ammissibile di un indice definito su 0-100, non un valore
    mancante, e nulla nei dati distingue una traccia genuinamente non popolare da
    una non misurata. L'indicatore consente a valle sia di includere sia di
    escludere; l'eliminazione in pipeline sarebbe irreversibile e sceglierebbe
    per conto di una misura che questa feature non possiede.

    Vale lo stesso per la durata dichiarata pari a zero: contarla e' una
    constatazione, deciderne il trattamento in una misura non e' di questa
    feature.
    """
    zero_popularity = zero_duration = 0
    for rec in records:
        is_zero_pop = int(rec["popularity"]) == 0
        is_zero_dur = int(rec["duration_ms"]) == 0
        rec["is_popularity_zero"] = _flag(is_zero_pop)
        rec["is_duration_zero"] = _flag(is_zero_dur)
        zero_popularity += is_zero_pop
        zero_duration += is_zero_dur
    return zero_popularity, zero_duration


def mark_high_zero_genres(
    records: list[dict], profile: dict, report: CleaningReport,
    invariants: Invariants,
) -> dict:
    """T016 - Decisione ereditata D4: il criterio dei generi a forte
    concentrazione di zeri.

    Soglia al **50%**, non al 60%. Il 60% e' un numero tondo, cioe' nessuna
    ragione. Il 50% e' la soglia oltre la quale un genere smette di essere
    descrivibile dalla propria mediana di popolarita': se piu' della meta' delle
    righe vale zero, il valore centrale e' zero qualunque cosa facciano le
    altre. Non e' una proprieta' stimata, e' una proprieta' della definizione di
    mediana.

    La quota si **ricalcola sulla grana coppia del dataset trasformato** e non
    si riprende dal profilo: la deduplicazione di T014 ha spostato i
    denominatori, e su 48 generi la quota cambia (ritrovamento F4).

    Le mediane per genere sarebbero il criterio piu' diretto e sono escluse di
    proposito: sono a un passo da `BQ2-K1`, e «segmento» non e' ancora definito
    (FR-044). La quota di zeri e' l'osservazione equivalente che resta dentro il
    perimetro di questa feature.
    """
    per_genre: dict[str, list[int]] = {}
    for rec in records:
        stats = per_genre.setdefault(rec["track_genre"], [0, 0])
        stats[1] += 1
        if rec["is_popularity_zero"] == "True":
            stats[0] += 1

    expected_genres = int(profile["values"]["SP.genre.count"]["value"])
    invariants.require(
        len(per_genre) == expected_genres,
        "i generi presenti dopo la deduplicazione sono quelli del profilo",
        f"{expected_genres} generi (SP.genre.count del profilo)",
        f"{len(per_genre)} generi",
    )

    shares = {g: 100.0 * z / n for g, (z, n) in per_genre.items()}
    high = sorted(g for g, s in shares.items() if s > ZERO_SHARE_THRESHOLD_PCT)

    for rec in records:
        rec["is_high_zero_genre"] = _flag(rec["track_genre"] in set(high))

    # Ogni genere ha la propria quota ricalcolata: e' cio' che permettera' a
    # T022 di confrontarle una per una con quelle del profilo e di scoprire da
    # solo quali sono cambiate, invece di fidarsi di un elenco scritto a mano.
    for genre in sorted(shares):
        report.pct(
            f"CL.SP.zero.by_genre.{slug(genre)}.after", shares[genre], "spotify",
            f"quota di righe a popolarita' zero nel genere {genre}, dopo la "
            f"deduplicazione di coppia",
            field="popularity", granularity="coppia traccia-genere",
        )

    below = [s for s in shares.values() if s <= ZERO_SHARE_THRESHOLD_PCT]
    above = [s for s in shares.values() if s > ZERO_SHARE_THRESHOLD_PCT]

    # La sensibilita' della soglia e' obbligatoria (decisione D4): una lista
    # prodotta da un taglio non va presentata come una proprieta' naturale dei
    # dati, e chi legge deve poter vedere quanto le stanno vicini i generi
    # esclusi e inclusi.
    report.count(
        "CL.SP.zero.high_genres.count", len(high), "spotify",
        f"generi la cui quota di righe a popolarita' zero supera il "
        f"{fmt_dec(ZERO_SHARE_THRESHOLD_PCT, 0)}%",
        field="popularity", granularity="genere",
    )
    report.pct(
        "CL.SP.zero.high_genres.nearest_below", max(below), "spotify",
        "quota del genere piu' vicino alla soglia da sotto, escluso",
        field="popularity", granularity="genere",
    )
    report.pct(
        "CL.SP.zero.high_genres.nearest_above", min(above), "spotify",
        "quota del genere piu' vicino alla soglia da sopra, incluso",
        field="popularity", granularity="genere",
    )
    report.catalogs["spotify_high_zero_genres"] = high
    return {"shares": shares, "high": high}


def deduplicate_tracks(
    records: list[dict], profile: dict, invariants: Invariants
) -> tuple[list[dict], dict]:
    """T018 - Ritrovamento F3 e decisione tecnica T5: la grana traccia.

    Questa deduplicazione **non** e' priva di perdita: 720 tracce hanno repliche
    che discordano, e discordano soltanto su `popularity`. La regola conserva il
    **massimo osservato**, che e' un valore effettivamente presente nella fonte:
    media e mediana ne produrrebbero uno che nessuna riga contiene.

    Che il disaccordo riguardi solo `popularity` non si assume: si verifica. Se
    toccasse altri attributi, la regola dichiarata non li coprirebbe e la
    pipeline si ferma invece di scegliere in silenzio.

    La regola introduce una distorsione verso l'alto, sistematica per
    costruzione ancorche' minima. Il documento deve dichiararla (FR-019): e' la
    differenza fra dichiarare una scelta e dichiararne l'effetto.
    """
    grouped: dict[str, list[dict]] = {}
    order: list[str] = []
    for rec in records:
        if rec["track_id"] not in grouped:
            order.append(rec["track_id"])
        grouped.setdefault(rec["track_id"], []).append(rec)

    stable_fields = tuple(
        f for f in SPOTIFY_SOURCE_FIELDS if f not in ("track_genre", "popularity")
    )
    unexpected = []
    conflicts = []
    for track_id, replicas in grouped.items():
        if len(replicas) == 1:
            continue
        for field in stable_fields:
            if len({r[field] for r in replicas}) > 1:
                unexpected.append((track_id, field))
        values = {int(r["popularity"]) for r in replicas}
        if len(values) > 1:
            conflicts.append((track_id, max(values) - min(values)))

    invariants.require(
        not unexpected,
        "fra le repliche di una traccia discorda soltanto l'indice di popolarita'",
        "zero attributi discordi oltre a popularity (ritrovamento F3)",
        f"{len(unexpected)} discordanze impreviste: {unexpected[:5]}",
    )

    tracks = []
    for track_id in order:
        replicas = grouped[track_id]
        # Si conserva la replica che porta il massimo, cosi' il valore scritto
        # e' la stringa della fonte e non una sua riscrittura (decisione T2).
        winner = max(replicas, key=lambda r: int(r["popularity"]))
        rec = {field: winner[field] for field in SPOTIFY_SOURCE_FIELDS
               if field != "track_genre"}
        rec["is_popularity_zero"] = _flag(int(winner["popularity"]) == 0)
        rec["is_duration_zero"] = _flag(int(winner["duration_ms"]) == 0)
        rec["genre_count"] = str(len(replicas))
        rec["has_conflicting_popularity"] = _flag(
            len({int(r["popularity"]) for r in replicas}) > 1
        )
        tracks.append(rec)

    expected_tracks = int(profile["values"]["SP.id.distinct"]["value"])
    invariants.require(
        len(tracks) == expected_tracks,
        "le tracce distinte coincidono con quelle del profilo",
        f"{expected_tracks} tracce (SP.id.distinct del profilo)",
        f"{len(tracks)} tracce",
    )

    expected_max = int(profile["values"]["SP.id.max_multiplicity"]["value"])
    observed_max = max(int(t["genre_count"]) for t in tracks)
    invariants.require(
        observed_max == expected_max,
        "la molteplicita' massima di una traccia coincide con quella del profilo",
        f"{expected_max} generi (SP.id.max_multiplicity del profilo)",
        f"{observed_max} generi",
    )

    spreads = [s for _, s in conflicts]
    return tracks, {
        "tracks": len(conflicts),
        "spread_max": max(spreads) if spreads else 0,
        "spread_over_10": sum(1 for s in spreads if s > 10),
    }


def transform_spotify(
    rows: list[dict], profile: dict, writer: OutputWriter,
    report: CleaningReport, invariants: Invariants,
) -> None:
    """Applica al catalogo musicale T014-T019 e produce i due output."""
    pairs, duplicate_pairs, removed = deduplicate_pairs(rows, invariants)   # T014
    zero_popularity, zero_duration = mark_degenerate_values(pairs)          # T015
    mark_high_zero_genres(pairs, profile, report, invariants)               # T016

    keys = [(r["track_id"], r["track_genre"]) for r in pairs]
    invariants.require(
        len(set(keys)) == len(keys),
        "la grana di spotify_track_genre.csv e' unica su track_id + track_genre",
        "zero chiavi ripetute",
        f"{len(keys) - len(set(keys))} chiavi ripetute",
    )

    # T017
    pair_rows = [{f: rec[f] for f in SPOTIFY_PAIR_FIELDS} for rec in pairs]
    writer.add("spotify_track_genre.csv", list(SPOTIFY_PAIR_FIELDS), pair_rows)

    tracks, conflict = deduplicate_tracks(pairs, profile, invariants)       # T018

    track_keys = [t["track_id"] for t in tracks]
    invariants.require(
        len(set(track_keys)) == len(track_keys),
        "la grana di spotify_tracks.csv e' unica su track_id",
        "zero chiavi ripetute",
        f"{len(track_keys) - len(set(track_keys))} chiavi ripetute",
    )

    # T019
    track_rows = [{f: rec[f] for f in SPOTIFY_TRACK_FIELDS} for rec in tracks]
    writer.add("spotify_tracks.csv", list(SPOTIFY_TRACK_FIELDS), track_rows)

    report.count(
        "CL.SP.pair.duplicate_pairs", duplicate_pairs, "spotify",
        "coppie traccia-genere che nella fonte compaiono piu' di una volta",
        granularity="coppia traccia-genere",
    )
    report.count(
        "CL.SP.pair.removed_rows", removed, "spotify",
        "righe rimosse dalla deduplicazione di coppia, identiche a una gia' presente",
        granularity="coppia traccia-genere",
    )
    report.count(
        "CL.SP.pair.rows.after", len(pairs), "spotify",
        "righe di spotify_track_genre.csv, alla grana coppia traccia-genere",
        granularity="coppia traccia-genere",
    )
    report.count(
        "CL.SP.zero.rows.after", zero_popularity, "spotify",
        "righe a popolarita' zero, conservate e marcate",
        field="popularity", granularity="coppia traccia-genere",
    )
    report.pct(
        "CL.SP.zero.pct.after", 100.0 * zero_popularity / len(pairs), "spotify",
        "quota di righe a popolarita' zero dopo la deduplicazione di coppia",
        field="popularity", granularity="coppia traccia-genere",
    )
    report.count(
        "CL.SP.duration.zero.rows", zero_duration, "spotify",
        "righe con durata dichiarata pari a zero, contate e marcate, mai corrette",
        field="duration_ms", granularity="coppia traccia-genere",
    )
    report.count(
        "CL.SP.track.rows.after", len(tracks), "spotify",
        "righe di spotify_tracks.csv, alla grana traccia deduplicata",
        granularity="traccia deduplicata",
    )
    report.count(
        "CL.SP.track.popularity_conflict.tracks", conflict["tracks"], "spotify",
        "tracce le cui repliche discordano sull'indice di popolarita'",
        field="popularity", granularity="traccia deduplicata",
    )
    report.count(
        "CL.SP.track.popularity_conflict.spread_max", conflict["spread_max"], "spotify",
        "scarto massimo fra le repliche discordi di una stessa traccia",
        field="popularity", granularity="traccia deduplicata",
    )
    report.count(
        "CL.SP.track.popularity_conflict.spread_over_10", conflict["spread_over_10"],
        "spotify",
        "tracce il cui scarto fra le repliche discordi supera i dieci punti",
        field="popularity", granularity="traccia deduplicata",
    )
    # Decisione ereditata D3, dichiarata con il suo numero. La regola — i totali
    # di catalogo si calcolano sulla grana traccia — non tocca alcuna riga, e
    # una decisione senza effetto quantificato non e' dichiarata. Cio' che
    # misura e' l'errore che si commetterebbe ignorandola: di quanto un totale
    # calcolato sulla grana coppia eccede quello corretto. E' `SP.id.inflation`
    # del profilo, restituito sui dati trasformati.
    report.pct(
        "CL.SP.track.inflation.after",
        100.0 * (len(pairs) - len(tracks)) / len(tracks), "spotify",
        "di quanto un totale calcolato sulla grana coppia eccede quello "
        "corretto sulla grana traccia",
        granularity="traccia deduplicata",
    )
    report.catalogs["spotify_excluded_fields"] = ["(colonna priva di nome)"]
    return pairs, tracks


# ===========================================================================
# T024 - Validazione dei tipi dichiarati
#
# In un CSV il tipo non vive nel file: vive in un contratto. Cio' che rende
# quel contratto vero non e' riscrivere i valori, ma verificarli (decisione T2).
# ===========================================================================

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INTEGER = re.compile(r"^-?\d+$")
DECIMAL = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")
BOOLEAN = ("True", "False")


def _check_type(kind, value: str) -> bool:
    if isinstance(kind, tuple):            # dominio enumerato chiuso
        return value in kind
    if kind == "testo":
        return True
    if kind == "testo_non_vuoto":
        return bool(value)
    if kind == "intero":
        return bool(INTEGER.match(value))
    if kind == "intero_o_vuoto":
        return value == "" or bool(INTEGER.match(value))
    if kind == "decimale":
        return bool(DECIMAL.match(value))
    if kind == "booleano":
        return value in BOOLEAN
    if kind == "data_iso_o_vuoto":
        return value == "" or bool(ISO_DATE.match(value))
    raise ValueError(f"tipo dichiarato sconosciuto: {kind}")


def validate_types(
    filename: str, rows: list[dict], schema: dict, invariants: Invariants
) -> None:
    """Verifica ogni campo di ogni riga contro il tipo dichiarato nel contratto."""
    violations = []
    for index, row in enumerate(rows):
        for field, kind in schema.items():
            if not _check_type(kind, row[field]):
                violations.append((index, field, row[field][:40]))
                if len(violations) > 5:
                    break
        if len(violations) > 5:
            break
    invariants.require(
        not violations,
        f"ogni campo di {filename} rispetta il tipo dichiarato nel contratto",
        "zero valori fuori tipo",
        f"{len(violations)} violazioni: {violations[:5]}",
    )


def output_schemas(profile: dict) -> dict:
    """Tipi dichiarati in contracts/output-datasets.md §1.1-§1.4."""
    rating_domain = tuple(profile["conventions"]["rating_domain"]) + ("",)
    audio = {f: "decimale" for f in (
        "danceability", "energy", "loudness", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence", "tempo",
    )}
    pair = {
        "track_id": "testo_non_vuoto", "artists": "testo", "album_name": "testo",
        "track_name": "testo", "popularity": "intero", "duration_ms": "intero",
        "explicit": "booleano", **audio, "key": "intero", "mode": "intero",
        "time_signature": "intero", "track_genre": "testo_non_vuoto",
        "is_popularity_zero": "booleano", "is_duration_zero": "booleano",
        "is_high_zero_genre": "booleano",
    }
    track = {k: v for k, v in pair.items()
             if k not in ("track_genre", "is_high_zero_genre")}
    track.update(genre_count="intero", has_conflicting_popularity="booleano")
    return {
        "netflix_titles.csv": {
            "show_id": "testo_non_vuoto", "type": ("Movie", "TV Show"),
            "title": "testo", "director": "testo", "cast": "testo",
            "country": "testo", "date_added": "data_iso_o_vuoto",
            "release_year": "intero", "rating": rating_domain,
            "movie_duration_min": "intero_o_vuoto",
            "tvshow_seasons": "intero_o_vuoto", "listed_in": "testo",
            "description": "testo", "is_repaired_duration": "booleano",
        },
        "netflix_title_category.csv": {
            "show_id": "testo_non_vuoto", "category": "testo_non_vuoto",
        },
        "spotify_track_genre.csv": pair,
        "spotify_tracks.csv": track,
    }


# ===========================================================================
# T022 - Il blocco dei denominatori, per ricalcolo e confronto
#
# La parte di questo artefatto che vale piu' delle altre, perche' e' l'unica
# che esiste per proteggere qualcuno che non e' ancora entrato nel progetto:
# senza, a valle si citerebbe il valore del profilo credendo di citare quello
# del dato trasformato.
#
# Il ricalcolo **riusa le funzioni del profiler** invece di riscriverle. Una
# riscrittura avrebbe prodotto differenze dovute a un arrotondamento diverso o
# a un criterio di ordinamento diverso, cioe' falsi denominatori — e un falso
# allarme in questo blocco e' peggio di un silenzio, perche' insegna a non
# fidarsene.
# ===========================================================================

# I 22 valori del profilo che descrivono la colonna indice priva di nome. La
# colonna esce dagli output (decisione T11), quindi questi valori non hanno un
# corrispondente da confrontare: non sono denominatori cambiati, sono
# denominatori **senza controparte**, ed e' una categoria diversa che va detta
# invece di essere confusa con l'altra.
UNNAMED_COLUMN_PREFIXES = ("SP.card.unnamed", "SP.miss.unnamed", "SP.num.unnamed",
                           "SP.top.unnamed")

# Valori del profilo che la trasformazione **non puo'** toccare, con la ragione.
# Non sono un residuo non classificato: sono la terza categoria, e dichiararla e'
# cio' che permette all'invariante di copertura di essere totale.
OUT_OF_SCOPE = {
    "X.claims_001.": "descrive la verifica delle affermazioni della 001, non i dati",
    "X.genre_lexical.": "descrive i vocabolari di etichette dei due cataloghi, che "
                        "la trasformazione non modifica",
}


def bespoke_recalculation(
    netflix: list[dict], bridge: list[dict], pairs: list[dict],
    tracks: list[dict], profile: dict,
) -> list[tuple]:
    """Ricalcola i valori che il profiler costruisce a mano, non con i generici.

    Sono 200 valori su 1.030, e comprendono il cambiamento piu' importante della
    feature: le 114 quote di zeri per genere, che la decisione ereditata D4
    consuma. Lasciarli fuori dal confronto avrebbe reso il blocco dei
    denominatori vero per costruzione e falso nella sostanza.

    Ogni voce e' `(identificativo di profilo, valore, tipo)`. Le formule
    ricalcano quelle di `profile_data.py`: sono conteggi e quote, dove il
    rischio di divergere per implementazione e' minimo, a differenza degli
    ordinamenti che i generici gia' coprono riusando il codice originale.
    """
    out: list[tuple] = []
    add = lambda vid, value, kind: out.append((vid, value, kind))

    # --- Catalogo video --------------------------------------------------
    add("NF.shape.rows", len(netflix), "count")
    add("NF.shape.fields", len(NETFLIX_TITLE_FIELDS), "count")
    add("NF.shape.distinct_ids", len({r["show_id"] for r in netflix}), "count")
    add("NF.type.movie", sum(1 for r in netflix if r["type"] == "Movie"), "count")
    add("NF.type.tvshow", sum(1 for r in netflix if r["type"] == "TV Show"), "count")
    add("NF.duration.missing",
        sum(1 for r in netflix
            if not r["movie_duration_min"] and not r["tvshow_seasons"]), "count")
    add("NF.duration.malformed", 0, "count")

    domain = set(profile["conventions"]["rating_domain"])
    ratings = {r["rating"] for r in netflix if r["rating"]}
    add("NF.rating.in_domain.values", len(ratings & domain), "count")
    add("NF.rating.out_of_domain.values", len(ratings - domain), "count")
    add("NF.rating.out_of_domain.rows",
        sum(1 for r in netflix if r["rating"] and r["rating"] not in domain), "count")
    add("NF.miss.complete_fields",
        sum(1 for f in NETFLIX_COLUMNS
            if not any(is_missing(r[f]) for r in netflix)), "count")

    per_category: dict[str, int] = {}
    for row in bridge:
        per_category[row["category"]] = per_category.get(row["category"], 0) + 1
    add("NF.cat.count", len(per_category), "count")
    add("NF.cat.assignments", len(bridge), "count")
    add("NF.cat.per_title.mean", len(bridge) / len(netflix), "num_cat")
    for category, titles in per_category.items():
        add(f"NF.cat.{slug(category)}.titles", titles, "count")
    musical = [c for c in per_category
               if any(t in c.lower() for t in profiler.MUSIC_TERMS)]
    add("NF.cat.music.count", len(musical), "count")
    add("NF.cat.non_music.count", len(per_category) - len(musical), "count")
    add("NF.cat.music.titles",
        len({r["show_id"] for r in bridge if r["category"] in set(musical)}), "count")

    # I tre valori di classificazione fuori dominio non compaiono piu' nel campo
    # dopo la riparazione di D2, quindi il ricalcolo generico non emette affatto
    # i loro identificativi. Non e' un'assenza: e' una frequenza che vale zero,
    # ed e' il modo piu' diretto di misurare l'effetto della decisione sul campo.
    for value in profile["catalogs"]["netflix_rating_out_of_domain"]:
        add(f"NF.freq.rating.{slug(value)}", 0, "count")

    # --- Catalogo musicale, grana coppia ---------------------------------
    add("SP.shape.rows", len(pairs), "count")
    add("SP.shape.fields", len(SPOTIFY_PAIR_FIELDS), "count")

    multiplicity: dict[str, int] = {}
    for row in pairs:
        multiplicity[row["track_id"]] = multiplicity.get(row["track_id"], 0) + 1
    distinct = len(multiplicity)
    add("SP.id.distinct", distinct, "count")
    add("SP.id.repeated", sum(1 for n in multiplicity.values() if n > 1), "count")
    add("SP.id.duplicate_rows", len(pairs) - distinct, "count")
    add("SP.id.duplicate_share", 100.0 * (len(pairs) - distinct) / len(pairs), "pct")
    add("SP.id.inflation", 100.0 * (len(pairs) - distinct) / distinct, "pct")
    add("SP.id.max_multiplicity", max(multiplicity.values()), "count")

    per_genre: dict[str, int] = {}
    zero_by_genre: dict[str, int] = {}
    for row in pairs:
        genre = row["track_genre"]
        per_genre[genre] = per_genre.get(genre, 0) + 1
        if row["is_popularity_zero"] == "True":
            zero_by_genre[genre] = zero_by_genre.get(genre, 0) + 1
    add("SP.genre.count", len(per_genre), "count")
    add("SP.genre.rows_min", min(per_genre.values()), "count")
    add("SP.genre.rows_max", max(per_genre.values()), "count")
    add("SP.genre.row_counts_distinct", len(set(per_genre.values())), "count")

    zeros = sum(zero_by_genre.values())
    add("SP.pop.zero.count", zeros, "count")
    add("SP.pop.zero.pct", 100.0 * zeros / len(pairs), "pct")
    for genre, total in per_genre.items():
        add(f"SP.pop.zero.by_genre.{slug(genre)}",
            100.0 * zero_by_genre.get(genre, 0) / total, "pct")
    # La soglia del 60% resta nel profilo come etichetta di un conteggio. Va
    # riconfrontata con il proprio criterio, non con quello del 50% adottato da
    # D4: sono due quantita' diverse, e accostarle suggerirebbe che una sia
    # cambiata di valore quando invece e' cambiata di definizione.
    add("SP.pop.zero.genres_over_60",
        sum(1 for g, t in per_genre.items() if zero_by_genre.get(g, 0) / t > 0.60),
        "count")
    add("SP.pop.zero.genres_fully_zero",
        sum(1 for g, t in per_genre.items() if zero_by_genre.get(g, 0) == t), "count")

    durations = [int(r["duration_ms"]) for r in pairs]
    add("SP.duration.median_s", profiler.statistics.median(durations) / 1000.0, "num_s")
    add("SP.duration.zero", sum(1 for d in durations if d == 0), "count")
    for field in profiler.MOOD_FIELDS:
        add(f"SP.mood.{field}.missing",
            sum(1 for r in pairs if is_missing(r[field])), "count")
    return out


def _recalculation_reason(vid: str, meta: dict) -> str:
    if vid.startswith("NF."):
        field = meta.get("field")
        if field == "duration":
            return ("la riparazione di D2 ha restituito la durata a tre titoli "
                    "che nella fonte ne erano privi")
        if field == "rating":
            return ("la riparazione di D2 ha svuotato la classificazione delle "
                    "tre righe riparate, che era fuori dominio")
        if field == "date_added":
            return ("il campo e' stato convertito in forma ISO 8601 e lo spazio "
                    "iniziale di 88 valori normalizzato")
        return "la trasformazione del catalogo video ha modificato questo valore"
    return ("la deduplicazione della grana coppia ha rimosso 450 righe identiche "
            "a una gia' presente")


def recalculate_profile_values(
    netflix: list[dict], bridge: list[dict], pairs: list[dict],
    tracks: list[dict], profile: dict,
    report: CleaningReport, invariants: Invariants,
) -> dict:
    """Riesegue il profiling sui dati trasformati e confronta valore per valore.

    Cio' che coincide non entra in `denominators`; cio' che differisce ci entra
    da solo. La completezza diventa una proprieta' dell'esecuzione e non una
    promessa di chi scrive (data-model §5).
    """
    recomputed = profiler.Profile()

    profiler.profile_fields(
        recomputed, "NF", "netflix", netflix, list(NETFLIX_COLUMNS))
    minutes = [float(r["movie_duration_min"]) for r in netflix if r["movie_duration_min"]]
    seasons = [float(r["tvshow_seasons"]) for r in netflix if r["tvshow_seasons"]]
    years = [float(r["release_year"]) for r in netflix if not is_missing(r["release_year"])]
    profiler.profile_numeric(recomputed, "NF", "netflix", "movie_duration_min",
                             minutes, "minuti", field="duration",
                             granularity="film", decimals=1)
    profiler.profile_numeric(recomputed, "NF", "netflix", "tvshow_seasons",
                             seasons, "stagioni", field="duration",
                             granularity="serie", decimals=1)
    profiler.profile_numeric(recomputed, "NF", "netflix", "release_year", years,
                             "anno", field="release_year",
                             granularity="titolo", decimals=1)

    types = profiler.profile_fields(
        recomputed, "SP", "spotify", pairs, list(SPOTIFY_SOURCE_FIELDS))
    for field in SPOTIFY_SOURCE_FIELDS:
        if types[field] not in ("intero", "decimale"):
            continue
        values = [profiler.parse_number(r[field]) for r in pairs
                  if not is_missing(r[field])]
        values = [float(v) for v in values if v is not None]
        decimals = 1 if field in ("popularity", "duration_ms", "tempo", "loudness") else 4
        profiler.profile_numeric(recomputed, "SP", "spotify", slug(field), values,
                                 "valore", field=field,
                                 granularity="coppia traccia-genere",
                                 decimals=decimals)

    declared = profile["values"]
    compared: set[str] = set()
    changed: list[str] = []

    def register(vid: str, value, display: str, unit: str, dataset: str,
                 label: str, field=None, granularity=None) -> None:
        compared.add(vid)
        if isinstance(value, float):
            value = round(value, ROUNDING_DECIMALS)
        if value == declared[vid]["value"]:
            return
        head, rest = vid.split(".", 1)
        cleaning_id = f"{ID_PREFIX}{head}.recalc.{rest}"
        report.add(cleaning_id, value, display, unit, dataset, label,
                   field=field, granularity=granularity)
        report.denominator(
            vid, cleaning_id, _recalculation_reason(vid, declared[vid]),
            "netflix_titles.csv" if vid.startswith("NF.") else "spotify_track_genre.csv",
        )
        changed.append(vid)

    # --- Famiglie generiche: stesso codice del profiler, nessun rischio di
    #     differenza dovuta all'implementazione.
    for vid, record in sorted(recomputed.values.items()):
        if vid not in declared:
            continue
        register(vid, record["value"], record["display"], record["unit"],
                 record["dataset"], record["label"] + ", dopo la trasformazione",
                 field=record["field"], granularity=record["granularity"])

    # --- Famiglie che il profiler costruisce a mano.
    for vid, value, kind in bespoke_recalculation(netflix, bridge, pairs, tracks, profile):
        if vid not in declared:
            continue
        meta = declared[vid]
        label = meta["label"] + ", dopo la trasformazione"
        if kind == "count":
            display, unit = fmt_int(int(value)), "conteggio"
            value = int(value)
        elif kind == "pct":
            display, unit = fmt_dec(float(value), 2) + "%", "percentuale"
            value = float(value)
        elif kind == "num_cat":
            display, unit = fmt_dec(float(value), 2), "categorie"
            value = float(value)
        else:
            display, unit = fmt_dec(float(value), 1), "secondi"
            value = float(value)
        register(vid, value, display, unit, meta["dataset"], label,
                 field=meta["field"], granularity=meta["granularity"])

    without_counterpart = sorted(
        vid for vid in declared
        if any(vid.startswith(p) for p in UNNAMED_COLUMN_PREFIXES)
    )
    out_of_scope = sorted(
        vid for vid in declared
        if any(vid.startswith(p) for p in OUT_OF_SCOPE)
    )
    report.catalogs["profile_values_without_counterpart"] = without_counterpart
    report.catalogs["profile_values_out_of_scope"] = out_of_scope

    # L'invariante che rende **letterale** l'affermazione di data-model §5: un
    # valore del profilo assente dai denominatori e' un valore che la
    # trasformazione non tocca. Senza questa verifica l'affermazione sarebbe
    # vera solo per i valori che qualcuno si e' ricordato di riconfrontare, e
    # nessuno potrebbe accorgersi dei dimenticati.
    unclassified = sorted(
        set(declared) - compared - set(without_counterpart) - set(out_of_scope)
    )
    invariants.require(
        not unclassified,
        "ogni valore del profilo e' riconfrontato, senza controparte o fuori perimetro",
        f"zero valori non classificati su {len(declared)}",
        f"{len(unclassified)} non classificati: {unclassified[:8]}",
    )
    invariants.require(
        len(report.denominators) == len(changed),
        "ogni valore riconfrontato che differisce ha una voce fra i denominatori",
        f"{len(changed)} voci",
        f"{len(report.denominators)} voci",
    )
    # I numeri della copertura sono essi stessi valori: il documento li cita, e
    # per la decisione ereditata D5 un'affermazione derivata o ha un
    # identificativo o non si scrive. Senza questi quattro, la frase che riassume
    # l'intero blocco dei denominatori sarebbe prosa non verificabile — cioe' il
    # rilievo R8 della 001, ricreato nel documento che esiste per chiuderlo.
    report.count("CL.meta.profile_values.total", len(declared), "entrambi",
                 "valori del profilo della 002")
    report.count("CL.meta.profile_values.compared", len(compared), "entrambi",
                 "valori del profilo riconfrontati sui dati trasformati")
    report.count("CL.meta.profile_values.changed", len(changed), "entrambi",
                 "valori del profilo che dopo la trasformazione differiscono")
    report.count("CL.meta.profile_values.without_counterpart",
                 len(without_counterpart), "entrambi",
                 "valori del profilo senza controparte, perche' descrivono la "
                 "colonna indice esclusa dagli output")
    report.count("CL.meta.profile_values.out_of_scope", len(out_of_scope),
                 "entrambi",
                 "valori del profilo che la trasformazione non puo' toccare")
    return {
        "declared": len(declared),
        "compared": len(compared),
        "changed": len(changed),
        "without_counterpart": len(without_counterpart),
        "out_of_scope": len(out_of_scope),
    }


# ===========================================================================
# main
# ===========================================================================


def main() -> int:
    invariants = Invariants()
    profile = load_profile()
    sources = verify_sources(profile, invariants)

    netflix_rows, netflix_fields = load(RAW / NETFLIX_FILE, NETFLIX_COLUMNS)
    spotify_rows, spotify_fields = load(RAW / SPOTIFY_FILE, SPOTIFY_COLUMNS)

    report = CleaningReport(profile, invariants)
    writer = OutputWriter(PROCESSED)

    netflix = transform_netflix(netflix_rows, profile, report, invariants)
    build_netflix_titles(netflix, profile, writer, report, invariants)
    bridge = build_netflix_title_category(netflix, profile, writer, report, invariants)

    pairs, tracks = transform_spotify(spotify_rows, profile, writer, report, invariants)

    # T024 - i tipi dichiarati nel contratto, verificati su tutti e quattro gli
    # output prima che uno solo di essi tocchi il disco.
    writer.validate(output_schemas(profile), invariants)

    # T022 - il confronto valore per valore con il profilo.
    recalc = recalculate_profile_values(
        netflix, bridge, pairs, tracks, profile, report, invariants)

    # La scrittura avviene qui e in nessun altro punto: gli output si sono
    # accumulati in memoria e atterrano solo ora, quando l'ultima invariante e'
    # passata. E' cio' che rende strutturale la garanzia di FR-004.
    outputs = writer.flush()

    # T021 e T023 - il rendiconto atterra per ultimo, quando i file che descrive
    # esistono e le loro impronte sono note.
    write_report(report, sources, outputs)

    genre_values = sum(1 for v in report.values if ".by_genre." in v)
    recalc_values = sum(1 for v in report.values if ".recalc." in v)
    print("Pipeline completa (task T001-T024).")
    print(f"  sorgenti confermate contro il profilo: {len(sources)}")
    print(f"  catalogo video   : {len(netflix_rows)} righe lette, {len(netflix_fields)} campi")
    print(f"  catalogo musicale: {len(spotify_rows)} righe lette, {len(spotify_fields)} campi")
    print()
    print(f"  invarianti verificate: {len(invariants.checked)}")
    for name in invariants.checked:
        print(f"    - {name}")
    print()
    print(f"  valori di rendicontazione: {len(report.values)}"
          f"  ({genre_values} quote per genere, {recalc_values} ricalcolati)")
    for vid in sorted(report.values):
        if ".by_genre." in vid or ".recalc." in vid:
            continue
        print(f"    {vid:46} {report.values[vid]['display']:>8}")
    print()
    print(f"  generi a forte concentrazione di zeri: "
          f"{', '.join(report.catalogs['spotify_high_zero_genres'])}")
    print()
    print(f"  denominatori: {recalc['changed']} cambiati su "
          f"{recalc['compared']} valori del profilo riconfrontati; "
          f"{recalc['without_counterpart']} senza controparte")
    print()
    print(f"  output scritti: {len(outputs)}")
    for entry in outputs:
        print(f"    {entry['path']:44} {entry['rows']:>6} righe  "
              f"{entry['columns']:>2} campi  {entry['bytes']:>9} byte")
    print()
    print(f"Rendiconto scritto in {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
