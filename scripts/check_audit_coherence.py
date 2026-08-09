#!/usr/bin/env python3
"""Verifica che il documento di audit e il profilo non siano divergenti.

Confronta ogni valore marcato in `docs/data_audit.md` con il valore
corrispondente di `reports/data_profile.json` (feature 002, FR-033).

Legge **solo** i due artefatti versionati: non richiede `data/raw/` e non
riesegue il profiling (FR-036). Chi clona il repository senza token Kaggle puo'
quindi verificare la coerenza di ogni numero del documento.

Esce con stato 1 su qualunque errore: un controllo che segnala senza fallire e'
un controllo che verra' ignorato (FR-034).

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
# segue il valore senza spazio interposto. Si cattura il testo che precede
# immediatamente il marcatore fino al primo spazio o inizio di riga: e' cio' che
# evita l'estrazione euristica di "tutti i numeri" vietata da FR-025.
MARKER = re.compile(r"(?P<display>\S*?)<!--@(?P<vid>[A-Za-z0-9._]+)-->")

# Sigle strutturali del progetto, escluse dall'avviso sui gruppi di cifre non
# marcati. Sono riferimenti, non quantita': segnalarle produrrebbe un elenco
# cosi' rumoroso da rendere l'avviso inservibile. L'elenco e' dichiarato qui
# perche' una esclusione non scritta e' una esclusione che nessuno puo'
# contestare.
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
DIGITS = re.compile(r"\d[\d.,]*")


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


def check_markers(text: str, values: dict) -> tuple[list[str], int]:
    """Confronto carattere per carattere fra testo marcato e campo display."""
    errors: list[str] = []
    cited = 0
    for match in MARKER.finditer(text):
        cited += 1
        vid = match.group("vid")
        found = match.group("display")
        line = line_of(text, match.start())
        if vid not in values:
            errors.append(
                f"  riga {line}: riferimento non risolvibile @{vid} — "
                f"l'identificativo non esiste nel profilo"
            )
            continue
        expected = values[vid]["display"]
        if found != expected:
            errors.append(
                f"  riga {line}: @{vid} — atteso «{expected}», trovato «{found}»"
            )
    return errors, cited


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


def unmarked_digits(text: str) -> list[str]:
    """Avviso non bloccante sui gruppi di cifre non adiacenti a un marcatore.

    Decisione D8: riconoscere che un numero *sarebbe dovuto* essere marcato
    richiederebbe di distinguere in prosa italiana un valore di profilo da una
    data o da un riferimento a una sezione. E' l'euristica che FR-025 vieta, e
    trasformarla in un gate produrrebbe fallimenti falsi. L'elenco serve alla
    revisione, non decide al posto suo.
    """
    blank = lambda m: " " * len(m.group(0))
    stripped = MARKER.sub(blank, text)
    stripped = LINK_TARGET.sub(blank, stripped)
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
                warnings.append(f"  riga {number}: «{token}»")
    return warnings


def main() -> int:
    text, artifact = load()
    values = artifact["values"]

    errors, cited = check_markers(text, values)
    errors += check_inventory(artifact)
    warnings = unmarked_digits(text)

    print(f"Documento : {DOC.relative_to(REPO)}")
    print(f"Profilo   : {PROFILE.relative_to(REPO)} ({len(values)} valori)")
    print(f"Marcatori : {cited}")

    if warnings:
        print(f"\nAVVISI ({len(warnings)}) — gruppi di cifre non marcati, da vagliare:")
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
