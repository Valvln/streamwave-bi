#!/usr/bin/env python3
"""Verifica che il documento di audit e il profilo non siano divergenti.

Confronta ogni valore marcato in `docs/data_audit.md` con il valore
corrispondente di `reports/data_profile.json` (feature 002, FR-033).

Legge **solo** i due artefatti versionati: non richiede `data/raw/` e non
riesegue il profiling (FR-036). Chi clona il repository senza token Kaggle puo'
quindi verificare la coerenza di ogni numero del documento.

Esce con stato 1 su qualunque errore: un controllo che segnala senza fallire e'
un controllo che verra' ignorato (FR-034).

Copre tre forme di ancoraggio:

    8.807<!--@NF.shape.rows-->          cifre, confrontate con `display`
    dodici<!--@X.claims_001.coincide--> numerale in lettere, confrontato con `value`
    `Music & Musicals`<!--@catalogs.netflix_categories_musical-->
                                        letterale, verificato come membro di una lista

La seconda e la terza forma esistono perche' la prima da sola lasciava scoperta
la zona in cui gli errori passano davvero: le affermazioni derivate scritte a
mano. Un controllo che copre solo le cifre certifica le ancore, non il documento.

Uso:
    python3 scripts/check_audit_coherence.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOC = REPO / "docs" / "data_audit.md"
PROFILE = REPO / "reports" / "data_profile.json"

# Grammatica della marcatura (contracts/profile-artifact.md §4): il marcatore
# segue il valore senza spazio interposto. Si cattura o un letterale fra apici
# inversi, o il testo che precede immediatamente il marcatore fino al primo
# spazio. E' cio' che evita l'estrazione euristica di "tutti i numeri" vietata
# da FR-025: nulla di non marcato viene mai confrontato.
MARKER = re.compile(
    r"(?P<display>`[^`]*`|\S*?)(?P<comment><!--@(?P<vid>[A-Za-z0-9._\[\]]+)-->)"
)

# Numerali italiani ammessi come forma ancorabile. Deliberatamente corto: copre
# i numeri piccoli che in prosa si scrivono in lettere. Oltre il venti, e per
# qualunque misura, si scrive in cifre.
NUMBER_WORDS = {
    "zero": 0, "uno": 1, "una": 1, "due": 2, "tre": 3, "quattro": 4,
    "cinque": 5, "sei": 6, "sette": 7, "otto": 8, "nove": 9, "dieci": 10,
    "undici": 11, "dodici": 12, "tredici": 13, "quattordici": 14,
    "quindici": 15, "sedici": 16, "diciassette": 17, "diciotto": 18,
    "diciannove": 19, "venti": 20,
}
# Numerali che in italiano sono anche articoli o pronomi: segnalarli come
# "cifre non marcate" produrrebbe un elenco inservibile.
AMBIGUOUS_WORDS = {"uno", "una"}

# Sigle strutturali del progetto, escluse dall'avviso. Sono riferimenti, non
# quantita'. L'elenco e' dichiarato qui perche' una esclusione non scritta e'
# una esclusione che nessuno puo' contestare.
STRUCTURAL = re.compile(
    r"""\b(?:
          BQ\d(?:-K\d)?      # sigle KPI del framework 001
        | (?:FR|SC|US|T)-?\d+ # requisiti, criteri, storie, task
        | [RDFVA]\d+          # rilievi, decisioni, ritrovamenti, inventario, assunzioni
        | 0\d\d               # numeri di feature (001-010)
        | \d{4}-\d{2}-\d{2}   # date
        | v?\d+\.\d+\.\d+     # versioni
    )\b""",
    re.VERBOSE,
)
SECTION_REF = re.compile(r"§\s*\d+(?:\.\d+)*")
# Ancore dei link interni: `[testo](file.md#52-nota-...)` contiene cifre che
# appartengono alla struttura del documento, non al suo contenuto.
LINK_TARGET = re.compile(r"\]\([^)]*\)")
# Il codice in linea fra apici inversi contiene identificativi — `sha256`,
# `duration_ms`, `TV-Y7` — le cui cifre non sono quantita'. I letterali che
# *sono* dati vengono ancorati, e l'ancora li sottrae a questa scansione prima.
INLINE_CODE = re.compile(r"`[^`]*`")
DIGITS = re.compile(r"\d[\d.,]*")
WORDS = re.compile(
    r"\b(" + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)


def load() -> tuple[str, dict]:
    for path in (DOC, PROFILE):
        if not path.exists():
            raise SystemExit(
                f"ERRORE: artefatto mancante: {path.relative_to(REPO)}\n"
                f"        Il controllo confronta documento e profilo: servono "
                f"entrambi, e sono entrambi versionati."
            )
    return DOC.read_text(encoding="utf-8"), json.loads(
        PROFILE.read_text(encoding="utf-8")
    )


def line_of(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def resolve(artifact: dict, vid: str):
    """Risolve un identificativo nei tre spazi dei nomi dell'artefatto."""
    for prefix in ("catalogs", "conventions"):
        if vid.startswith(prefix + "."):
            container = artifact.get(prefix, {})
            key = vid[len(prefix) + 1:]
            if key not in container:
                return None
            return (prefix, container[key])
    if vid in artifact["values"]:
        return ("values", artifact["values"][vid])
    return None


def check_markers(text: str, artifact: dict) -> tuple[list[str], dict]:
    errors: list[str] = []
    tally = {"cifre": 0, "lettere": 0, "letterali": 0}

    # Un commento che vive *dentro* un frammento di codice in linea e' la
    # sintassi mostrata come esempio, non un'ancora: il documento ha il diritto
    # di documentare il proprio meccanismo senza attivarlo. In un'ancora vera su
    # un letterale il commento sta invece fuori dagli apici.
    code_spans = [m.span() for m in INLINE_CODE.finditer(text)]

    for match in MARKER.finditer(text):
        comment_at = match.start("comment")
        if any(start <= comment_at < end for start, end in code_spans):
            continue

        vid = match.group("vid")
        found = match.group("display")
        line = line_of(text, match.start())
        target = resolve(artifact, vid)

        if target is None:
            errors.append(
                f"  riga {line}: riferimento non risolvibile @{vid} — "
                f"l'identificativo non esiste nel profilo"
            )
            continue

        space, payload = target

        # --- Letterale fra apici inversi: appartenenza a un elenco ---
        if found.startswith("`") and found.endswith("`"):
            literal = found.strip("`")
            tally["letterali"] += 1
            members = payload if isinstance(payload, list) else [payload]
            members = [str(m) for m in members]
            if literal not in members:
                shown = ", ".join(members[:6]) + ("…" if len(members) > 6 else "")
                errors.append(
                    f"  riga {line}: @{vid} — «{literal}» non compare "
                    f"nell'elenco ({shown})"
                )
            continue

        if space != "values":
            errors.append(
                f"  riga {line}: @{vid} — un riferimento a {space} va usato su "
                f"un letterale fra apici inversi, non su «{found}»"
            )
            continue

        # --- Numerale in lettere: confronto sul valore numerico ---
        word = found.lower().strip(".,;:")
        if word in NUMBER_WORDS:
            tally["lettere"] += 1
            if NUMBER_WORDS[word] != payload["value"]:
                errors.append(
                    f"  riga {line}: @{vid} — atteso {payload['value']}, "
                    f"trovato «{found}» ({NUMBER_WORDS[word]})"
                )
            continue

        # --- Cifre: confronto carattere per carattere con la forma dichiarata ---
        tally["cifre"] += 1
        if found != payload["display"]:
            errors.append(
                f"  riga {line}: @{vid} — atteso «{payload['display']}», "
                f"trovato «{found}»"
            )
    return errors, tally


def check_inventory(artifact: dict) -> list[str]:
    """Ogni sigla dell'inventario della 001 deve risolversi (SC-003)."""
    errors = []
    values = artifact["values"]
    for claim_id, ids in sorted(artifact.get("inventory_001", {}).items()):
        for vid in ids:
            if vid not in values:
                errors.append(
                    f"  inventario {claim_id}: rimanda a @{vid}, assente dal profilo"
                )
    return errors


def unmarked_quantities(text: str) -> list[str]:
    """Avviso non bloccante su cifre e numerali non adiacenti a un marcatore.

    Decisione D8: riconoscere che un numero *sarebbe dovuto* essere marcato
    richiederebbe di distinguere in prosa italiana un valore di profilo da una
    data o da un riferimento a una sezione. E' l'euristica che FR-025 vieta, e
    trasformarla in un gate produrrebbe fallimenti falsi. L'elenco serve alla
    revisione, non decide al posto suo.
    """
    blank = lambda m: " " * len(m.group(0))
    stripped = MARKER.sub(blank, text)
    stripped = LINK_TARGET.sub(blank, stripped)
    stripped = INLINE_CODE.sub(blank, stripped)
    stripped = STRUCTURAL.sub(blank, stripped)
    stripped = SECTION_REF.sub(blank, stripped)

    warnings = []
    in_code = False
    for number, line in enumerate(stripped.split("\n"), start=1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        # Le intestazioni sono struttura: la loro numerazione non e' un dato.
        if in_code or line.lstrip().startswith("#"):
            continue
        for match in DIGITS.finditer(line):
            token = match.group(0).rstrip(".,")
            if token:
                warnings.append(f"  riga {number}: «{token}» (cifre)")
        for match in WORDS.finditer(line):
            token = match.group(0)
            if token.lower() not in AMBIGUOUS_WORDS:
                warnings.append(f"  riga {number}: «{token}» (numerale)")
    return warnings


def main() -> int:
    text, artifact = load()

    errors, tally = check_markers(text, artifact)
    errors += check_inventory(artifact)
    warnings = unmarked_quantities(text)

    print(f"Documento : {DOC.relative_to(REPO)}")
    print(f"Profilo   : {PROFILE.relative_to(REPO)} ({len(artifact['values'])} valori)")
    print(
        f"Marcatori : {sum(tally.values())} "
        f"({tally['cifre']} in cifre, {tally['lettere']} in lettere, "
        f"{tally['letterali']} letterali)"
    )

    if warnings:
        print(f"\nAVVISI ({len(warnings)}) — quantita' non marcate, da vagliare:")
        for warning in warnings:
            print(warning)

    if errors:
        print(f"\nERRORI ({len(errors)}):")
        for error in errors:
            print(error)
        print("\nESITO: divergenza fra documento e profilo.")
        return 1

    print("\nESITO: documento e profilo coerenti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
