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

    # Il catalogo musicale entra da T014, la scrittura degli output da T012.
    # Finche' non ci sono, la pipeline verifica cio' che puo' verificare e si
    # ferma **senza scrivere nulla**: ne' CSV, ne' rendiconto. Un rendiconto
    # parziale sarebbe peggio di nessun rendiconto, perche' chi lo trova
    # versionato lo crede completo.
    print("Catalogo video trasformato in memoria (task T001-T011).")
    print(f"  sorgenti confermate contro il profilo: {len(sources)}")
    print(f"  catalogo video   : {len(netflix_rows)} righe lette, {len(netflix_fields)} campi")
    print(f"  catalogo musicale: {len(spotify_rows)} righe lette, {len(spotify_fields)} campi (non ancora trasformato)")
    print(f"  righe trasformate: {len(netflix)}")
    print()
    print(f"  invarianti verificate: {len(invariants.checked)}")
    for name in invariants.checked:
        print(f"    - {name}")
    print()
    print(f"  valori di rendicontazione: {len(report.values)}")
    for vid in sorted(report.values):
        print(f"    {vid:38} {report.values[vid]['display']:>7}")
    print()
    print("Catalogo musicale e scrittura degli output non ancora implementati (da T012).")
    print("Nessun output scritto: data/processed/ e reports/cleaning_report.json intatti.")

    # Nessun output e' in coda: e' cio' che rende letterale la riga qui sopra.
    assert not writer._pending
    return 0


if __name__ == "__main__":
    sys.exit(main())
