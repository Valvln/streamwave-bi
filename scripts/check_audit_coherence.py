#!/usr/bin/env python3
"""Verifica che i documenti di lettura e gli artefatti di numeri non divergano.

Confronta ogni valore marcato in `docs/data_audit.md` (feature 002), in
`docs/data_cleaning.md` (feature 003) e in `docs/bq3_scenarios.md` (feature 004)
con il valore corrispondente di `reports/data_profile.json`,
`reports/cleaning_report.json` e `reports/bq3_scenarios.json`.

Legge **solo** artefatti versionati: non richiede `data/raw/`, non riesegue il
profiling e non riesegue la pipeline (FR-036 della 002, FR-041 della 003). Chi
clona il repository senza token Kaggle puo' quindi verificare la coerenza di
ogni numero dei due documenti.

Esce con stato 1 su qualunque errore: un controllo che segnala senza fallire e'
un controllo che verra' ignorato (FR-034 della 002, FR-039 della 003).

Copre quattro forme di ancoraggio:

    8.807<!--@NF.shape.rows-->          cifre, confrontate con `display`
    dodici<!--@X.claims_001.coincide--> numerale in lettere, confrontato con `value`
    `Music & Musicals`<!--@catalogs.netflix_categories_musical-->
                                        letterale, verificato come membro di una lista
    due<!--#-->                         numerale dichiarato **non misurato**

Le prime tre esistono perche' la sola marcatura delle cifre lasciava scoperta la
zona in cui gli errori passano davvero: le affermazioni derivate scritte a mano.
La quarta e' la decisione ereditata D5 della 003, corollario (c): sul documento
della 003 una quantita' priva di entrambi i marcatori e' un **errore**, non un
avviso, e distinguere un fatto misurato da un numerale retorico non e' compito
di un'euristica sulla prosa italiana — e' compito di chi scrive, che lo sa in un
istante. Il marcatore di non-misurato e' il modo di dirlo.

La severita' e' quindi **per documento** (contratto della 003 §3.2): sul
documento della 002 le quantita' non marcate restano avvisi, perche' applicarvi
la regola nuova significherebbe rimarcare un artefatto gia' mergiato.

Uso:
    python3 scripts/check_audit_coherence.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROFILE = REPO / "reports" / "data_profile.json"
CLEANING = REPO / "reports" / "cleaning_report.json"
SCENARIOS = REPO / "reports" / "bq3_scenarios.json"

# Gli artefatti da unire, dichiarati **una volta sola**: erano elencati sia qui
# sia nell'intestazione stampata, e un quarto artefatto aggiunto in un solo
# punto avrebbe prodotto un controllo che verifica tre cose e ne dichiara due.
ARTIFACTS = (PROFILE, CLEANING, SCENARIOS)

# I documenti verificati, con la propria severita'. `strict` decide se una
# quantita' priva di marcatore sia un errore o un avviso.
DOCUMENTS = (
    (REPO / "docs" / "data_audit.md", False, "feature 002"),
    (REPO / "docs" / "data_cleaning.md", True, "feature 003"),
    (REPO / "docs" / "bq3_scenarios.md", True, "feature 004"),
    (REPO / "docs" / "data_model.md", True, "feature 005"),
)

# Grammatica della marcatura (docs/convenzioni-marcatura.md): il marcatore
# segue il valore senza spazio interposto. Si cattura o un letterale fra apici
# inversi, o il testo che precede immediatamente il marcatore fino al primo
# spazio. E' cio' che evita l'estrazione euristica di "tutti i numeri" vietata
# da FR-025: nulla di non marcato viene mai confrontato.
MARKER = re.compile(
    r"(?P<display>`[^`]*`|\S*?)"
    r"(?P<comment><!--(?:@(?P<vid>[A-Za-z0-9._\[\]]+)|(?P<unmeasured>#))-->)"
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
        | [Dd]ivergenz[ae]\s+\d+(?:\s+e\s+\d+)*   # divergenze dei verbali di revisione
        | ISO\s+\d+           # nomi di standard
    )\b""",
    re.VERBOSE,
)
# Numerazione di un elenco ordinato Markdown a inizio riga: e' sintassi, come le
# intestazioni. L'esclusione e' scritta qui perche' una esclusione non dichiarata
# e' una esclusione che nessuno puo' contestare.
ORDERED_LIST = re.compile(r"^\s{0,3}\d+\.\s", re.MULTILINE)
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


def load_artifacts() -> tuple[dict, list[str]]:
    """Unisce i tre artefatti in un solo spazio dei nomi, verificando le collisioni.

    La disgiunzione dei prefissi (decisione T8 della 003) e' cio' che rende
    l'unione sicura, ma non viene **assunta**: una collisione farebbe risolvere
    un'ancora sul valore sbagliato senza che nulla lo segnali, ed e' esattamente
    il tipo di errore silenzioso contro cui questo controllo esiste.
    """
    artifacts = []
    for path in ARTIFACTS:
        if not path.exists():
            raise SystemExit(
                f"ERRORE: artefatto mancante: {path.relative_to(REPO)}\n"
                f"        Il controllo confronta i documenti con gli artefatti "
                f"di numeri: sono tutti versionati e devono esserci."
            )
        artifacts.append(json.loads(path.read_text(encoding="utf-8")))

    merged: dict = {"values": {}, "catalogs": {}, "conventions": {}, "inventory_001": {}}
    collisions = []
    for artifact in artifacts:
        for space in ("values", "catalogs", "conventions"):
            for key, payload in artifact.get(space, {}).items():
                if key in merged[space] and merged[space][key] != payload:
                    collisions.append(f"{space}.{key}")
                merged[space][key] = payload
        merged["inventory_001"].update(artifact.get("inventory_001", {}))
    return merged, sorted(set(collisions))


def read_document(path: Path) -> str:
    if not path.exists():
        raise SystemExit(
            f"ERRORE: documento mancante: {path.relative_to(REPO)}\n"
            f"        Il controllo verifica i documenti dichiarati in DOCUMENTS."
        )
    return path.read_text(encoding="utf-8")


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
    tally = {"cifre": 0, "lettere": 0, "letterali": 0, "non misurati": 0}

    # Un commento che vive *dentro* un frammento di codice in linea e' la
    # sintassi mostrata come esempio, non un'ancora: il documento ha il diritto
    # di documentare il proprio meccanismo senza attivarlo. In un'ancora vera su
    # un letterale il commento sta invece fuori dagli apici.
    code_spans = [m.span() for m in INLINE_CODE.finditer(text)]

    for match in MARKER.finditer(text):
        comment_at = match.start("comment")
        if any(start <= comment_at < end for start, end in code_spans):
            continue

        found = match.group("display")
        line = line_of(text, match.start())

        # --- Marcatore malformato ---
        # Se il testo catturato come valore contiene a sua volta un'apertura di
        # commento, l'ancora e' rotta: qualcosa e' stato inserito **dentro**
        # l'identificativo. La grammatica non ammette `<` in un identificativo,
        # quindi il motore ripiega sull'alternativa e riconosce il marcatore
        # interno — declassando in silenzio un valore ancorato a "non
        # misurato". E' successo davvero, su cinque ancore, e il controllo
        # passava: senza questa guardia la garanzia di §2 e' falsa proprio nel
        # caso in cui servirebbe.
        if "<!--" in found:
            errors.append(
                f"  riga {line}: marcatore malformato — il valore catturato "
                f"«{found}» contiene un'apertura di commento. L'ancora e' "
                f"rotta e il documento reso mostrera' testo spezzato"
            )
            continue

        # --- Non misurato: si registra che la decisione e' stata presa ---
        # Il marcatore non asserisce nulla sul valore. Dichiara che chi scrive
        # ha **considerato** quel numerale e afferma che non e' un fatto sui
        # dati. Cio' che elimina e' la categoria dell'omissione distratta, che
        # e' quella in cui la 002 ha perso tre affermazioni; non elimina la
        # categoria della dichiarazione falsa, contro cui esiste la revisione
        # in contesto pulito.
        if match.group("unmeasured"):
            tally["non misurati"] += 1
            continue

        vid = match.group("vid")
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


def residual_comment_ends(text: str) -> list[str]:
    """Chiusure di commento rimaste nel testo dopo l'estrazione dei marcatori.

    Seconda guardia contro l'ancora rotta. Un commento HTML termina al **primo**
    `-->`: se dentro un marcatore ne e' finito un altro, la coda dell'ancora
    resta visibile nel documento reso — il lettore vede `.rows.after-->` dove si
    aspetta un numero. Cercarla dopo aver rimosso i marcatori ben formati la
    trova sempre, anche in casi che la prima guardia non prevede.
    """
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    stripped = MARKER.sub(blank, text)
    stripped = re.sub(r"<!--.*?-->", blank, stripped, flags=re.DOTALL)
    errors = []
    for number, line in enumerate(stripped.split("\n"), start=1):
        if "-->" in line:
            errors.append(
                f"  riga {number}: chiusura di commento «-->» rimasta nel testo "
                f"— un'ancora e' rotta e sara' visibile nel documento reso"
            )
    return errors


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
    """Cifre e numerali non adiacenti ad alcun marcatore.

    Sul documento della 002 e' un **avviso**: la decisione D8 di quella feature
    osservava che riconoscere se un numero *sarebbe dovuto* essere marcato
    richiede di distinguere in prosa italiana un valore di profilo da una data o
    da un riferimento a una sezione, cioe' l'euristica che FR-025 vieta.

    Sul documento della 003 e' un **errore**, e non perche' l'euristica sia
    migliorata: perche' l'onere si e' spostato. Con il marcatore di non-misurato
    chi scrive dichiara l'intenzione, e al controllo non resta nulla da
    indovinare — una quantita' senza marcatore non e' piu' ambigua, e' omessa.
    """
    # La sostituzione preserva i ritorni a capo, non solo la lunghezza. Un
    # apice inverso spaiato fa estendere `INLINE_CODE` alla riga successiva, e
    # cancellarne il ritorno a capo sposterebbe di uno tutti i numeri di riga da
    # li' in avanti: un errore segnalato sulla riga sbagliata e' un errore che
    # chi lo riceve cerca dove non e'.
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    stripped = MARKER.sub(blank, text)
    stripped = LINK_TARGET.sub(blank, stripped)
    stripped = INLINE_CODE.sub(blank, stripped)
    stripped = STRUCTURAL.sub(blank, stripped)
    stripped = SECTION_REF.sub(blank, stripped)
    stripped = ORDERED_LIST.sub(blank, stripped)

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
    artifact, collisions = load_artifacts()

    listed = " + ".join(str(path.relative_to(REPO)) for path in ARTIFACTS)
    print(f"Artefatti : {listed}")
    print(f"            {len(artifact['values'])} valori in uno spazio dei nomi unito")

    failed = False
    if collisions:
        print(f"\nERRORI (1):")
        print(f"  i due artefatti collidono su {len(collisions)} chiavi con "
              f"contenuto diverso: {', '.join(collisions)}")
        failed = True

    inventory_errors = check_inventory(artifact)

    for path, strict, owner in DOCUMENTS:
        text = read_document(path)
        errors, tally = check_markers(text, artifact)
        errors += residual_comment_ends(text)
        unmarked = unmarked_quantities(text)
        if path is DOCUMENTS[0][0]:
            errors += inventory_errors

        severity = "errore" if strict else "avviso"
        print(f"\nDocumento : {path.relative_to(REPO)} ({owner})")
        print(
            f"Marcatori : {sum(tally.values())} "
            f"({tally['cifre']} in cifre, {tally['lettere']} in lettere, "
            f"{tally['letterali']} letterali, "
            f"{tally['non misurati']} non misurati)"
        )
        print(f"Severita' : quantita' non marcata = {severity}")

        if unmarked:
            if strict:
                errors += [
                    w + " — priva di ancora e di marcatore di non-misurato"
                    for w in unmarked
                ]
            else:
                print(f"\n  AVVISI ({len(unmarked)}) — quantita' non marcate, da vagliare:")
                for warning in unmarked:
                    print(warning)

        if errors:
            print(f"\n  ERRORI ({len(errors)}):")
            for error in errors:
                print(error)
            failed = True

    if failed:
        print("\nESITO: divergenza fra documenti e artefatti.")
        return 1

    print("\nESITO: documenti e artefatti coerenti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
