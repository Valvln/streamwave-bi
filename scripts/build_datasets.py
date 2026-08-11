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

    # Le trasformazioni entrano da T008. Finche' non ci sono, la pipeline
    # verifica cio' che puo' verificare e si ferma **senza scrivere nulla**:
    # ne' CSV, ne' rendiconto. Un rendiconto vuoto sarebbe peggio di nessun
    # rendiconto, perche' chi lo trova versionato lo crede completo.
    print("Fondamenta verificate (task T001-T007).")
    print(f"  sorgenti confermate contro il profilo: {len(sources)}")
    print(f"  invarianti verificate: {len(invariants.checked)}")
    for name in invariants.checked:
        print(f"    - {name}")
    print(f"  catalogo video   : {len(netflix_rows)} righe, {len(netflix_fields)} campi")
    print(f"  catalogo musicale: {len(spotify_rows)} righe, {len(spotify_fields)} campi")
    print()
    print("Trasformazioni non ancora implementate (da T008).")
    print("Nessun output scritto: data/processed/ e reports/cleaning_report.json intatti.")

    # Riferimenti volutamente non usati in questo stadio: esistono perche' i
    # task successivi vi scrivano dentro, e sono qui per rendere evidente che
    # nulla e' stato scritto.
    assert not report.values and not writer._pending
    return 0


if __name__ == "__main__":
    sys.exit(main())
