#!/usr/bin/env python3
"""Calcolo delle otto misure del framework KPI, sugli operatori della 007a.

Legge `data/processed/*.csv` e `data/curated/dim_category_mood.json` e produce
`reports/kpi_measures.json`, che contiene i valori dei sei KPI calcolabili piu'
gli operatori di supporto che le decisioni della 007b hanno reso obbligatori.

Che cosa questo script **non** e': una scrittura di misure DAX. Il `.pbix` non
e' versionato e le misure si scrivono nella GUI di Power BI Desktop, fuori
dall'automazione (principio V). Il testo DAX di ciascuna misura vive in
`docs/kpi_measures.md` come formula da incollare nel modello; questo script
applica **le stesse regole** di `docs/data_model.md` e `docs/kpi_operators.md`
sugli stessi dati, perche' chi clona il repository senza una licenza Power BI
possa comunque rigenerare ogni numero pubblicato. Che le due strade coincidano
non e' assunto: e' il confronto E9, il cui esito vive in
`reports/kpi_engine_check.json` — curato a mano, mai scritto da qui.

Derivazione deterministica per costruzione (FR-001, FR-002, FR-003): nessun
generatore casuale, nessuna lettura dell'orologio, nessun contatto con
l'esterno. Due esecuzioni consecutive producono file identici byte per byte.

L'aritmetica sta tutta in `decimal.Decimal` e mai in virgola mobile, con
precisione di contesto fissata esplicitamente: e' la stessa disciplina di
`scripts/build_bq3_scenarios.py`, e per la stessa ragione — in virgola mobile un
confine di arrotondamento si vede dal lato sbagliato, e una cifra sbagliata
finisce dentro un artefatto verde.

I numeri escono come **stringhe**, come entrano.

Uso:
    python3 scripts/build_kpi_measures.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from decimal import Decimal, ROUND_HALF_UP, getcontext
from pathlib import Path

# La precisione di contesto e' dichiarata qui e non lasciata al default
# implicito: due delle derivazioni (la media di tre distanze, la
# normalizzazione della domanda) non sono esatte in base dieci, e la cifra a cui
# vengono troncate non deve dipendere da come l'interprete e' stato avviato.
getcontext().prec = 28

REPO = Path(__file__).resolve().parent.parent
PROCESSED = REPO / "data" / "processed"
NF_TITLES = PROCESSED / "netflix_titles.csv"
NF_BRIDGE = PROCESSED / "netflix_title_category.csv"
SP_TRACKS = PROCESSED / "spotify_tracks.csv"
SP_PAIRS = PROCESSED / "spotify_track_genre.csv"
MOOD = REPO / "data" / "curated" / "dim_category_mood.json"
SCENARIOS = REPO / "reports" / "bq3_scenarios.json"
OUT = REPO / "reports" / "kpi_measures.json"

SCHEMA_VERSION = 1

MUSICAL_CATEGORY = "Music & Musicals"

# Le cardinalita' attese, dichiarate come costanti perche' la guardia di FR-004
# le confronti invece di scoprirle dai dati che dovrebbe verificare.
EXPECTED_CATEGORIES = 42
EXPECTED_SEGMENTS = 114
NORTH_STAR_ORIGIN_COUNT = 375  # NF.cat.music_musicals.titles, reports/data_profile.json

# --- D12: la soglia di C2 ---
# Maggioranza semplice, cioe' piu' della meta' del catalogo musicale. E' una
# **stipulazione**, non un'osservazione: la si dichiara come costante perche' il
# documento la possa ancorare invece di digitarla a mano, sullo stesso statuto
# delle soglie del quadrante di BQ2-K3. Vedi DECISION_RULE e la nota in loco in
# coda a docs/kpi_operators.md §12.
C2_THRESHOLD = Decimal("0.50")

# Le condizioni della regola di decisione sono tre perche' business_case.md §3 ne
# fissa tre: e' una costante di struttura della regola, non una misura.
DECISION_CONDITIONS = 3

# --- E5: arrotondamento e precisione di presentazione, per unita' di misura ---
# Una regola per unita' si discute una volta sola; un giudizio per singolo
# valore si discuterebbe otto volte. Le cifre sono di **presentazione**: ogni
# derivazione lavora sui valori esatti e arrotonda solo al momento di scrivere.
DIGITS_SHARE = Decimal("0.0001")      # quote e indici su 0-1: 4 cifre
DIGITS_MINUTES = Decimal("0.01")      # minuti: 2 cifre
DIGITS_POPULARITY = Decimal("0.1")    # indice di popolarita' 0-100: 1 cifra
# Eccezione dichiarata, e valida per una sola voce: la differenza fra le due
# varianti della mediana musicale di E3. A 2 cifre uscirebbe come «-0,00», cioe'
# un segno affermato su uno zero — una forma che asserisce il falso proprio nel
# valore che esiste per rendere verificabile la decisione E3. Vedi ROUNDING_RULE.
DIGITS_VARIANT_DELTA = Decimal("0.000001")

UNIT_SHARE = "quota, 0-1"
UNIT_MINUTES = "minuti"
UNIT_POPULARITY = "indice di popolarita', 0-100"
UNIT_COUNT = "conteggio"
UNIT_BOOL = "esito booleano"
UNIT_RANK = "posizione in graduatoria"

ROUNDING_RULE = (
    "ROUND_HALF_UP, dichiarato esplicitamente e non la modalita' predefinita di "
    "decimal.Decimal, che e' ROUND_HALF_EVEN. Le cifre pubblicate dipendono "
    "dall'unita' di misura e non dal singolo KPI: quote e indici sul dominio 0-1 "
    "(share, overlap, affinity, score, zero_share) a 4 cifre decimali; durate in "
    "minuti a 2; l'indice di popolarita' sulla scala 0-100 a 1; conteggi, "
    "posizioni in graduatoria ed esiti booleani senza arrotondamento perche' "
    "esatti per costruzione. L'arrotondamento e' di **presentazione**: ogni "
    "derivazione — mediana, differenza, media delle distanze, punteggio pesato, "
    "soglia del quadrante, ordinamento della graduatoria — opera sui valori "
    "esatti, e arrotonda solo al momento di scrivere il valore pubblicato. "
    "Arrotondare prima sposterebbe una mediana o un confronto di soglia. Tutta "
    "l'aritmetica in decimal.Decimal, mai in virgola mobile. "
    "Due precisazioni che la regola per unita' non copre da sola. La prima: una "
    "mediana di conteggi puo' essere un mezzo intero — i conteggi per categoria "
    "sono 42, numero pari — e si pubblica percio' a 2 cifre decimali, non come "
    "intero. La seconda e' un'eccezione a una voce sola, "
    "KPI.BQ1K2.median_variant_delta: la differenza fra le due varianti della "
    "mediana musicale di E3 vale meno di un centesimo di minuto, e a 2 cifre "
    "uscirebbe come «-0,00» — un segno affermato su uno zero, proprio nel valore "
    "che esiste per rendere verificabile la decisione E3. Si pubblica a 6 cifre. "
    "Fuori da questa voce nessun valore in minuti porta piu' di 2 cifre."
)

MEDIAN_RULE = (
    "Ordinamento crescente dei valori; su conteggio dispari il valore centrale, "
    "su conteggio pari la media aritmetica dei due valori centrali. Nessun "
    "trattamento speciale dei valori ripetuti: i pari merito entrano "
    "nell'ordinamento come qualunque altro valore. E' la definizione da manuale, "
    "adottata identica dai quattro operatori che usano una mediana — BQ1-K1/C1 "
    "sui 42 conteggi per categoria, BQ2-K1 sulla popolarita' per segmento, "
    "BQ2-K2 sui tre assi di mood, BQ2-K3 sulle soglie del quadrante. Decisione "
    "D10 di docs/kpi_operators.md, che chiude l'issue #7."
)

DURATION_ZERO_RULE = (
    "Le righe marcate is_duration_zero **entrano** nella mediana della durata "
    "musicale di BQ1-K2. E' la stessa disciplina gia' applicata a "
    "is_popularity_zero da D7: la trasformazione ha scelto di conservare e "
    "marcare, non di eliminare, e una misura che filtrasse sulla marcatura "
    "ritirerebbe quella scelta senza dichiararlo. La variante esclusa viene "
    "comunque calcolata e pubblicata — KPI.BQ1K2.median_music_excluding_zero — "
    "insieme alla differenza fra le due, perche' la decisione sia verificabile "
    "invece che dichiarata a parole. Decisione D11 di docs/kpi_operators.md."
)

RANK_RULE = (
    "La graduatoria di BQ2-K3 ordina i segmenti per punteggio decrescente e la "
    "prima posizione e' quella del punteggio piu' alto (D8). I pari merito "
    "ricevono la **stessa** posizione, e la posizione successiva salta di "
    "altrettante unita': due segmenti primi a pari merito sono entrambi in "
    "posizione 1 e il successivo e' in posizione 3. E' la scelta che non "
    "introduce un criterio di spareggio che nessuna decisione della 007a ha "
    "fissato: spareggiare per nome di segmento produrrebbe un ordine "
    "riproducibile ma arbitrario, presentato con l'autorevolezza di un "
    "risultato. L'ordinamento interno dell'elenco resta alfabetico per "
    "riproducibilita' del file, e non e' la graduatoria."
)

QUADRANT_RULE = (
    "L'appartenenza al quadrante alta-domanda/alta-affinita' di BQ2-K3 e' "
    "valutata con soglia **stretta** su entrambi gli assi (D4): un segmento vi "
    "appartiene se la sua domanda supera la mediana delle domande dei 114 "
    "segmenti **e** la sua affinita' supera la mediana delle affinita' degli "
    "stessi. Un segmento esattamente sulla mediana non entra. Entrambe le "
    "soglie sono calcolate sui valori esatti, non su quelli arrotondati per la "
    "pubblicazione."
)

SCALE_RULE = (
    "La domanda si porta sul dominio 0-1 per divisione per il proprio massimo "
    "teorico, 100, e non per riscalamento sui valori osservati fra i segmenti "
    "(D3): e' un indice delimitato per definizione, e riscalarlo sugli "
    "osservati renderebbe il punteggio di ogni segmento dipendente dal segmento "
    "piu' domandato del gruppo. I pesi della combinazione sono 0,5 e 0,5, per "
    "assenza di un criterio esterno che differenzi domanda e affinita'."
)


DECISION_RULE = (
    "La regola di decisione della North Star e' fissata da docs/business_case.md "
    "§3 e pubblicata **prima** che i valori esistessero: l'argomento di coerenza "
    "e' sostenuto se tutte e tre le condizioni C1, C2, C3 sono soddisfatte. "
    "C1 e' l'operatore D9.2 (il conteggio dei titoli di Music & Musicals supera "
    "la mediana dei 42 conteggi per categoria); C2 e' l'operatore D12, fissato "
    "dalla feature 009: mood_profile_overlap **supera** la soglia di maggioranza "
    "semplice 0,50, con confronto **stretto** per coerenza con D9.2 e D4. "
    "Su questi dati la scelta fra confronto stretto e largo non cambia l'esito, "
    "perche' il valore non cade sulla soglia; il **margine** invece dalla soglia "
    "dipende, e si restringe se la soglia e' piu' severa. C3 e' l'appartenenza "
    "al quadrante alta-domanda/alta-affinita' di almeno un segmento musicale "
    "(D4). "
    "La **confidenza del verdetto e' media**, ereditata dal termine piu' debole e "
    "non calcolata come media delle tre: una congiunzione non e' piu' affidabile "
    "del suo termine meno affidabile, e trattarla come una media lascerebbe che "
    "la confidenza alta di C1 coprisse quella media di C2. Il termine piu' "
    "debole e' C2, che poggia su una stima **per eccesso** (limite dichiarato di "
    "D1: il prodotto cartesiano dei tre intervalli scalari sovrastima la "
    "sovrapposizione reale, che e' quindi minore o uguale al valore pubblicato). "
    "Il verdetto **eredita la dipendenza dalla versione della tabella dei mood** "
    "attraverso C2: vedi kpi_mood_table_version. Per il contratto di versione di "
    "docs/content_taxonomy_bridge.md §5 una revisione della tabella **invalida** "
    "i valori che ne dipendono invece di correggerli, e con essi C2 e il verdetto."
)


# ===========================================================================
# Lettura
# ===========================================================================

def halt(message: str) -> "NoReturn":
    """Ferma la derivazione senza scrivere alcun file.

    Meglio nessun artefatto che un artefatto parziale: un file scritto a meta'
    e' indistinguibile, per chi lo legge dopo, da uno completo.
    """
    raise SystemExit(f"ERRORE: {message}\n        Nessun file e' stato scritto.")


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        halt(
            f"file di ingresso mancante: {path.relative_to(REPO)}\n"
            f"        `data/processed/` non e' versionato: si rigenera con "
            f"`python3 scripts/build_datasets.py`, che a sua volta richiede "
            f"`data/raw/`."
        )
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    if not path.exists():
        halt(f"artefatto mancante: {path.relative_to(REPO)}")
    return json.loads(path.read_text(encoding="utf-8"))


def flag(raw: str) -> bool:
    """Le marcature booleane della pipeline si scrivono `True`/`False`."""
    return raw == "True"


# ===========================================================================
# Aritmetica
# ===========================================================================

def median(values: list[Decimal], what: str) -> Decimal:
    """Mediana secondo E2/D10. Vedi MEDIAN_RULE."""
    if not values:
        halt(f"mediana richiesta su un insieme vuoto: {what} (FR-004)")
    ordered = sorted(values)
    size = len(ordered)
    middle = size // 2
    if size % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / Decimal(2)


def share(numerator: int, denominator: int, what: str) -> Decimal:
    if denominator == 0:
        halt(f"quota richiesta con denominatore nullo: {what} (FR-004)")
    return Decimal(numerator) / Decimal(denominator)


def share_decimal(numerator: Decimal, denominator: Decimal, what: str) -> Decimal:
    """Come `share`, ma fra due grandezze gia' decimali.

    Esiste separata perche' `share` dichiara nella firma che i suoi due termini
    sono conteggi, ed e' un'informazione che vale la pena non perdere: un
    rapporto fra conteggi e un rapporto fra quote sono cose diverse, e la firma
    e' il posto in cui la differenza resta visibile.
    """
    if denominator == 0:
        halt(f"quota richiesta con denominatore nullo: {what} (FR-004)")
    return numerator / denominator


def quantize(value: Decimal, digits: Decimal) -> Decimal:
    return value.quantize(digits, rounding=ROUND_HALF_UP)


def display_of(value: Decimal) -> str:
    """Formattazione esplicita con la virgola decimale italiana.

    Mai una funzione dipendente dal locale: sulla macchina di chi sviluppa
    darebbe il risultato giusto per caso (vincolo ereditato da F6 della 003).
    """
    return format(value, "f").replace(".", ",")


def slug(name: str) -> str:
    """Porta un nome di segmento o categoria nella forma ammessa da un
    identificativo di ancora.

    La grammatica di `docs/convenzioni-marcatura.md` ammette lettere, cifre,
    punto e parentesi quadre: un nome come `black-metal` romperebbe l'ancora
    silenziosamente, perche' il trattino chiuderebbe l'identificativo prima
    della fine. E' la stessa forma gia' usata da `dim_category_mood.json` per le
    categorie (`Action & Adventure` -> `action_adventure`).
    """
    out = []
    for char in name.lower():
        out.append(char if char.isalnum() else "_")
    collapsed = "_".join(part for part in "".join(out).split("_") if part)
    return collapsed


# ===========================================================================
# Le voci dell'artefatto
# ===========================================================================

def entry(value: Decimal, digits: Decimal, label: str, unit: str) -> dict:
    rounded = quantize(value, digits)
    # Uno zero non porta segno. `Decimal` conserva il segno dell'operando anche
    # quando l'arrotondamento azzera il valore, e «-0,0000» affermerebbe una
    # direzione su una grandezza nulla.
    if rounded == 0:
        rounded = abs(rounded)
    return {
        "display": display_of(rounded),
        "value": str(rounded),
        "label": label,
        "unit": unit,
    }


def count_entry(value: int, label: str) -> dict:
    return {
        "display": str(value),
        "value": str(value),
        "label": label,
        "unit": UNIT_COUNT,
    }


def bool_entry(value: bool, label: str) -> dict:
    """Un esito booleano e' un valore misurato quanto un numero.

    Un confronto fra due valori misurati e' esso stesso un valore misurato: o ha
    un identificativo proprio, o non si scrive (regola D5 del metodo di
    progetto). `display` porta la forma con cui il documento lo cita.
    """
    return {
        "display": "sì" if value else "no",
        "value": "true" if value else "false",
        "label": label,
        "unit": UNIT_BOOL,
    }


def rank_entry(value: int, label: str) -> dict:
    return {
        "display": str(value),
        "value": str(value),
        "label": label,
        "unit": UNIT_RANK,
    }


# ===========================================================================
# La guardia (FR-004)
# ===========================================================================

def guard_cardinalities(categories: set[str], segments: set[str], mood: dict) -> None:
    """Verifica le due cardinalita' su cui ogni aggregazione poggia.

    Non e' una formalita': un ponte che perdesse una categoria, o un insieme di
    coppie che perdesse un segmento, produrrebbe mediane e quote perfettamente
    plausibili calcolate su una popolazione diversa da quella dichiarata — e
    nessun controllo a valle se ne accorgerebbe, perche' i numeri resterebbero
    coerenti fra loro.
    """
    mood_categories = set(mood["catalogs"]["mood_categories"])
    if len(categories) != EXPECTED_CATEGORIES:
        halt(
            f"il ponte titolo-categoria porta {len(categories)} categorie "
            f"distinte, attese {EXPECTED_CATEGORIES} (FR-004)"
        )
    if categories != mood_categories:
        only_bridge = sorted(categories - mood_categories)
        only_mood = sorted(mood_categories - categories)
        halt(
            f"le categorie del ponte e quelle di dim_category_mood non "
            f"coincidono (FR-004)\n"
            f"        solo nel ponte: {only_bridge or '—'}\n"
            f"        solo nella tabella dei mood: {only_mood or '—'}"
        )
    if len(segments) != EXPECTED_SEGMENTS:
        halt(
            f"le coppie traccia-segmento portano {len(segments)} segmenti "
            f"distinti, attesi {EXPECTED_SEGMENTS} (FR-004)"
        )
    slugs = {slug(name) for name in segments}
    if len(slugs) != len(segments):
        halt(
            "due segmenti diversi producono lo stesso identificativo di ancora: "
            "le chiavi di BQ2-K1/K2/K3 collidono (FR-004)"
        )


# ===========================================================================
# BQ1-K1 — music_adjacent_catalog_share, C1, invarianza della North Star
# ===========================================================================

def build_bq1k1(titles: list[dict], bridge: list[dict], values: dict) -> None:
    distinct_titles = {row["show_id"] for row in titles}
    per_category: dict[str, set[str]] = {}
    for row in bridge:
        per_category.setdefault(row["category"], set()).add(row["show_id"])

    musical = per_category.get(MUSICAL_CATEGORY)
    if not musical:
        halt(
            f"la categoria «{MUSICAL_CATEGORY}» non compare nel ponte "
            f"titolo-categoria: il numeratore di BQ1-K1 non esiste (FR-004)"
        )

    exact_share = share(len(musical), len(distinct_titles), "BQ1-K1")
    values["KPI.BQ1K1.share"] = entry(
        exact_share, DIGITS_SHARE,
        "music_adjacent_catalog_share — titoli in Music & Musicals sul totale "
        "dei titoli distinti del catalogo video",
        UNIT_SHARE,
    )
    values["KPI.BQ1K1.numerator_titles"] = count_entry(
        len(musical),
        "titoli distinti assegnati a Music & Musicals sul ponte trasformato",
    )
    values["KPI.BQ1K1.denominator_titles"] = count_entry(
        len(distinct_titles),
        "titoli distinti del catalogo video, denominatore di BQ1-K1",
    )

    # --- C1 (D9.2): la posizione della categoria, che non e' la quota ---
    counts = {name: len(ids) for name, ids in per_category.items()}
    median_42 = median([Decimal(n) for n in counts.values()], "C1, conteggi per categoria")
    musical_count = Decimal(len(musical))
    values["KPI.BQ1K1.c1.category_count.music_musicals"] = count_entry(
        len(musical),
        "conteggio dei titoli di Music & Musicals, ingresso di C1",
    )
    values["KPI.BQ1K1.c1.median_of_42"] = entry(
        median_42, DIGITS_MINUTES,
        "mediana dei 42 conteggi di titoli per categoria (E2/D10)",
        UNIT_COUNT,
    )
    values["KPI.BQ1K1.c1.above_median"] = bool_entry(
        musical_count > median_42,
        "C1 — Music & Musicals supera la mediana dei 42 conteggi, soglia stretta",
    )

    # --- E7: l'invarianza del numeratore, verificata invece che assunta ---
    # Il conteggio sul trasformato e' lo stesso numeratore appena calcolato: e'
    # la ragione per cui D9.1 diceva che la verifica sarebbe uscita «quasi
    # gratis» eseguendo l'operatore di §2.2. Viene comunque ripubblicato con
    # chiave propria, perche' un confronto che vive solo nella prosa non e'
    # ancorabile.
    transformed = len(musical)
    values["KPI.BQ1K1.north_star_invariance.transformed_count"] = count_entry(
        transformed,
        "titoli distinti in Music & Musicals contati su netflix_title_category.csv",
    )
    values["KPI.BQ1K1.north_star_invariance.origin_count"] = count_entry(
        NORTH_STAR_ORIGIN_COUNT,
        "titoli distinti in Music & Musicals sul dato di origine, ripubblicato "
        "da NF.cat.music_musicals.titles per il confronto fianco a fianco",
    )
    values["KPI.BQ1K1.north_star_invariance.matches"] = bool_entry(
        transformed == NORTH_STAR_ORIGIN_COUNT,
        "E7 — il conteggio sul trasformato coincide con quello di origine, "
        "esito del confronto che chiude l'assunzione D9.1",
    )
    values["KPI.BQ1K1.north_star_invariance.delta"] = count_entry(
        transformed - NORTH_STAR_ORIGIN_COUNT,
        "differenza fra il conteggio sul trasformato e quello di origine",
    )


# ===========================================================================
# BQ1-K2 — format_duration_gap
# ===========================================================================

def build_bq1k2(titles: list[dict], tracks: list[dict], values: dict) -> None:
    all_music = []
    excluding_zero = []
    for row in tracks:
        minutes = Decimal(row["duration_ms"]) / Decimal(60000)
        all_music.append(minutes)
        if not flag(row["is_duration_zero"]):
            excluding_zero.append(minutes)

    movies = [row for row in titles if row["type"] == "Movie"]
    movie_minutes = [
        Decimal(row["movie_duration_min"]) for row in movies if row["movie_duration_min"]
    ]
    if len(movie_minutes) != len(movies):
        halt(
            f"{len(movies) - len(movie_minutes)} titoli di tipo Movie non "
            f"portano una durata: la mediana del lato video sarebbe calcolata "
            f"su una popolazione diversa da quella dichiarata (FR-004)"
        )

    median_all = median(all_music, "BQ1-K2, durata musicale, tutte le righe")
    median_excluding = median(excluding_zero, "BQ1-K2, durata musicale, esclusa la riga degenere")
    median_movie = median(movie_minutes, "BQ1-K2, durata dei film")

    # E3: la variante che entra nel gap e' quella **con** la riga degenere.
    exact_gap = median_all - median_movie

    values["KPI.BQ1K2.gap_minutes"] = entry(
        exact_gap, DIGITS_MINUTES,
        "format_duration_gap — durata mediana di una traccia meno durata "
        "mediana di un film, con il proprio segno (D5)",
        UNIT_MINUTES,
    )
    values["KPI.BQ1K2.median_music_all_rows"] = entry(
        median_all, DIGITS_MINUTES,
        "durata mediana di una traccia musicale, tutte le righe incluse quella "
        "marcata is_duration_zero (E3/D11, variante adottata)",
        UNIT_MINUTES,
    )
    values["KPI.BQ1K2.median_music_excluding_zero"] = entry(
        median_excluding, DIGITS_MINUTES,
        "durata mediana di una traccia musicale, esclusa la riga marcata "
        "is_duration_zero (E3/D11, variante di controllo)",
        UNIT_MINUTES,
    )
    values["KPI.BQ1K2.median_variant_delta"] = entry(
        median_all - median_excluding, DIGITS_VARIANT_DELTA,
        "differenza fra le due varianti della mediana musicale — quanto la "
        "decisione E3 sposta il valore pubblicato; pubblicata a 6 cifre per "
        "l'eccezione dichiarata in kpi_rounding",
        UNIT_MINUTES,
    )
    values["KPI.BQ1K2.median_movie"] = entry(
        median_movie, DIGITS_MINUTES,
        "durata mediana di un film del catalogo video",
        UNIT_MINUTES,
    )
    values["KPI.BQ1K2.movie_share_of_video_catalog"] = entry(
        share(len(movies), len(titles), "E4, quota di film"), DIGITS_SHARE,
        "quota di titoli Movie sul catalogo video — dichiara l'asimmetria del "
        "confronto, che oppone i soli film all'intero catalogo musicale (E4)",
        UNIT_SHARE,
    )
    values["KPI.BQ1K2.movie_titles"] = count_entry(
        len(movies), "titoli di tipo Movie nel catalogo video"
    )
    values["KPI.BQ1K2.music_tracks"] = count_entry(
        len(all_music), "tracce deduplicate del catalogo musicale"
    )


# ===========================================================================
# BQ1-K3 — mood_profile_overlap
# ===========================================================================

AXES = (
    ("mood_energy", "energy", "energia"),
    ("mood_valence", "valence", "positività"),
    ("mood_danceability", "danceability", "ritmo"),
)


def mood_table(mood: dict) -> dict[str, dict[str, Decimal]]:
    """Il passaggio da forma lunga a larga dichiarato da data_model.md §13.

    Le voci senza campo `category` — MOOD.coverage.rows, MOOD.table.version,
    MOOD.review.changes_count — si escludono nominandole, come quel documento
    prescrive.
    """
    table: dict[str, dict[str, Decimal]] = {}
    for payload in mood["values"].values():
        category = payload.get("category")
        if category is None:
            continue
        table.setdefault(category, {})[payload["axis"]] = Decimal(payload["value"])
    for category, profile in table.items():
        missing = {axis for axis, _, _ in AXES} - set(profile)
        if missing:
            halt(
                f"la categoria «{category}» non porta i tre assi di mood: "
                f"manca {sorted(missing)} (FR-004)"
            )
    return table


def build_bq1k3(tracks: list[dict], table: dict, values: dict) -> Decimal:
    """Calcola BQ1-K3 e **restituisce la quota esatta**, non arrotondata.

    La restituisce perche' `build_decision_rule` ne ha bisogno per il confronto
    di soglia di `C2`, e rileggerla dalla voce gia' scritta significherebbe
    confrontare un valore arrotondato per la pubblicazione: e' esattamente cio'
    che `kpi_rounding` vieta, e qui il confronto **e'** la misura. Lo schema e'
    quello gia' usato da `build_segment_measures`, che restituisce ai chiamanti
    cio' che serve a valle invece di farlo rileggere dall'artefatto.
    """
    bounds = {}
    for axis, _, italian in AXES:
        column = [profile[axis] for profile in table.values()]
        bounds[axis] = (min(column), max(column))
        values[f"KPI.BQ1K3.bound.{axis}.min"] = entry(
            bounds[axis][0], DIGITS_SHARE,
            f"estremo inferiore dell'asse {italian} sul catalogo video, "
            f"minimo sulle 42 righe di dim_category_mood",
            UNIT_SHARE,
        )
        values[f"KPI.BQ1K3.bound.{axis}.max"] = entry(
            bounds[axis][1], DIGITS_SHARE,
            f"estremo superiore dell'asse {italian} sul catalogo video, "
            f"massimo sulle 42 righe di dim_category_mood",
            UNIT_SHARE,
        )

    inside = 0
    for row in tracks:
        # Intervalli chiusi e AND logico sui tre assi: e' il parallelepipedo
        # allineato agli assi di D1, non l'inviluppo convesso — la stima e' per
        # eccesso, ed e' il limite dichiarato dall'operatore.
        if all(
            bounds[axis][0] <= Decimal(row[column]) <= bounds[axis][1]
            for axis, column, _ in AXES
        ):
            inside += 1

    overlap = share(inside, len(tracks), "BQ1-K3")
    values["KPI.BQ1K3.overlap_share"] = entry(
        overlap, DIGITS_SHARE,
        "mood_profile_overlap — quota di tracce il cui profilo cade dentro "
        "l'intervallo occupato dal catalogo video su tutti e tre gli assi (D1)",
        UNIT_SHARE,
    )
    values["KPI.BQ1K3.tracks_inside"] = count_entry(
        inside, "tracce il cui profilo cade dentro l'intervallo su tutti e tre gli assi"
    )
    return overlap


# ===========================================================================
# BQ2-K1, BQ2-K2, BQ2-K3 — le tre misure per segmento
# ===========================================================================

def build_segment_measures(
    pairs: list[dict], bridge: list[dict], table: dict, values: dict
) -> tuple[list[str], list[str]]:
    by_segment: dict[str, list[dict]] = {}
    for row in pairs:
        by_segment.setdefault(row["track_genre"], []).append(row)

    # --- Il profilo mediano del catalogo video (data_model.md §11) ---
    # Ponderato sulle assegnazioni titolo-categoria, non sulle 42 righe della
    # tabella: e' cio' che rende simmetrico il confronto con il lato musicale,
    # dove il profilo del segmento e' una mediana sulle coppie.
    video_profile = {}
    for axis, _, italian in AXES:
        column = [table[row["category"]][axis] for row in bridge]
        video_profile[axis] = median(column, f"profilo video, asse {italian}")
        values[f"KPI.BQ2K2.video_profile.{axis}"] = entry(
            video_profile[axis], DIGITS_SHARE,
            f"profilo mediano del catalogo video, asse {italian}, sulle 19.323 "
            f"assegnazioni titolo-categoria",
            UNIT_SHARE,
        )

    demand: dict[str, Decimal] = {}
    affinity: dict[str, Decimal] = {}
    high_zero: list[str] = []

    for name in sorted(by_segment):
        rows = by_segment[name]
        key = slug(name)

        # --- BQ2-K1 ---
        popularity = [Decimal(row["popularity"]) for row in rows]
        demand[name] = median(popularity, f"BQ2-K1, segmento {name}")
        zeros = sum(1 for row in rows if flag(row["is_popularity_zero"]))
        flags = {flag(row["is_high_zero_genre"]) for row in rows}
        if len(flags) != 1:
            halt(
                f"il segmento «{name}» porta valori diversi di "
                f"is_high_zero_genre sulle proprie righe: la marcatura non e' "
                f"costante entro il segmento e la dimensione non e' "
                f"costruibile (data_model.md §13)"
            )
        if flags.pop():
            high_zero.append(name)

        values[f"KPI.BQ2K1.{key}.demand_index"] = entry(
            demand[name], DIGITS_POPULARITY,
            f"segment_demand_index — mediana della popolarita' delle coppie "
            f"traccia-segmento del segmento «{name}»",
            UNIT_POPULARITY,
        )
        values[f"KPI.BQ2K1.{key}.zero_share"] = entry(
            share(zeros, len(rows), f"quota di zeri, segmento {name}"), DIGITS_SHARE,
            f"quota di righe a popolarita' nulla del segmento «{name}» — "
            f"obbligatoria accanto al valore per D7",
            UNIT_SHARE,
        )
        values[f"KPI.BQ2K1.{key}.rows"] = count_entry(
            len(rows), f"coppie traccia-segmento del segmento «{name}»"
        )

        # --- BQ2-K2 ---
        distances = []
        for axis, column, _ in AXES:
            segment_axis = median(
                [Decimal(row[column]) for row in rows], f"BQ2-K2, {name}, {axis}"
            )
            distances.append(abs(segment_axis - video_profile[axis]))
        distance = sum(distances, Decimal(0)) / Decimal(3)
        affinity[name] = Decimal(1) - distance

        values[f"KPI.BQ2K2.{key}.affinity"] = entry(
            affinity[name], DIGITS_SHARE,
            f"segment_catalog_affinity — 1 meno la media delle tre distanze "
            f"assolute per asse fra il profilo del segmento «{name}» e quello "
            f"del catalogo video (D2)",
            UNIT_SHARE,
        )
        values[f"KPI.BQ2K2.{key}.distance"] = entry(
            distance, DIGITS_SHARE,
            f"media delle tre distanze assolute per asse, segmento «{name}»",
            UNIT_SHARE,
        )

    # --- BQ2-K3: composizione, quadrante, graduatoria ---
    demand_threshold = median(list(demand.values()), "BQ2-K3, soglia di domanda")
    affinity_threshold = median(list(affinity.values()), "BQ2-K3, soglia di affinita'")
    values["KPI.BQ2K3.threshold.demand"] = entry(
        demand_threshold, DIGITS_POPULARITY,
        "mediana delle domande dei 114 segmenti, soglia stretta del quadrante (D4)",
        UNIT_POPULARITY,
    )
    values["KPI.BQ2K3.threshold.affinity"] = entry(
        affinity_threshold, DIGITS_SHARE,
        "mediana delle affinita' dei 114 segmenti, soglia stretta del quadrante (D4)",
        UNIT_SHARE,
    )

    score = {
        name: (
            Decimal("0.5") * (demand[name] / Decimal(100))
            + Decimal("0.5") * affinity[name]
        )
        for name in demand
    }

    # Pari merito: stessa posizione, e la successiva salta. Nessuno spareggio
    # per nome — sarebbe un ordine riproducibile ma arbitrario (RANK_RULE).
    ordered = sorted(score.values(), reverse=True)
    rank_of: dict[Decimal, int] = {}
    for position, value in enumerate(ordered, start=1):
        rank_of.setdefault(value, position)

    quadrant_members = []
    for name in sorted(demand):
        key = slug(name)
        in_quadrant = (
            demand[name] > demand_threshold and affinity[name] > affinity_threshold
        )
        if in_quadrant:
            quadrant_members.append(name)
        values[f"KPI.BQ2K3.{key}.score"] = entry(
            score[name], DIGITS_SHARE,
            f"segment_entry_priority_score — 0,5 per la domanda normalizzata "
            f"piu' 0,5 per l'affinita', segmento «{name}» (D3)",
            UNIT_SHARE,
        )
        values[f"KPI.BQ2K3.{key}.quadrant_high_high"] = bool_entry(
            in_quadrant,
            f"il segmento «{name}» sta nel quadrante alta domanda / alta "
            f"affinita', soglia mediana stretta su entrambi gli assi (D4)",
        )
        values[f"KPI.BQ2K3.{key}.rank"] = rank_entry(
            rank_of[score[name]],
            f"posizione del segmento «{name}» in graduatoria, punteggio "
            f"decrescente (D8)",
        )

    values["KPI.BQ2K3.quadrant_members_count"] = count_entry(
        len(quadrant_members),
        "segmenti nel quadrante alta domanda / alta affinita' — e' la risposta "
        "verificabile alla condizione C3 della regola di decisione della North Star",
    )
    values["KPI.BQ2K3.c3_satisfied"] = bool_entry(
        len(quadrant_members) > 0,
        "C3 — esiste almeno un segmento musicale nella meta' superiore per "
        "domanda e nella meta' superiore per affinita'",
    )
    values["KPI.BQ2K1.high_zero_segments_count"] = count_entry(
        len(high_zero),
        "segmenti con is_high_zero_genre vero, che portano l'avvertimento "
        "testuale esplicito accanto al proprio valore (D7)",
    )

    # --- Il ritrovamento che D7 prevedeva senza poterlo quantificare ---
    # Che la concentrazione di zeri trascini la mediana verso il basso era
    # l'argomento di D7; **quanto** la trascini nessun documento poteva dirlo
    # prima che le mediane esistessero. Le tre voci qui sotto lo dicono, e sono
    # affermazioni derivate: hanno un identificativo proprio perche' altrimenti
    # sarebbero un conto fatto a mente nella prosa del documento (regola D5).
    zero_median = sorted(name for name in demand if demand[name] == 0)
    values["KPI.BQ2K1.zero_median_segments_count"] = count_entry(
        len(zero_median),
        "segmenti la cui mediana di popolarita' vale esattamente zero",
    )
    values["KPI.BQ2K1.zero_median_matches_high_zero"] = bool_entry(
        zero_median == sorted(high_zero),
        "l'insieme dei segmenti a mediana nulla coincide esattamente con quello "
        "dei segmenti marcati is_high_zero_genre — ne' piu' ampio ne' piu' "
        "stretto",
    )
    values["KPI.BQ2K3.high_zero_best_rank"] = rank_entry(
        min(rank_of[score[name]] for name in high_zero) if high_zero else 0,
        "la migliore posizione in graduatoria raggiunta da uno dei segmenti "
        "marcati is_high_zero_genre",
    )
    return sorted(high_zero), quadrant_members


# ===========================================================================
# BQ3-K1 / BQ3-K2 — citazione, non ricalcolo
# ===========================================================================

def check_scenarios(scenarios: dict) -> None:
    """FR-011: i due KPI di BQ3 si citano, non si ricalcolano.

    Nessuna chiave viene copiata dentro `reports/kpi_measures.json`: copiarla
    duplicherebbe una fonte gia' ancorata, e la copia potrebbe divergere
    dall'originale senza che nulla lo segnali. Qui si verifica soltanto che le
    voci citate da `docs/kpi_measures.md` esistano davvero nell'artefatto della
    004 — se non esistessero, il documento porterebbe ancore non risolvibili e
    il difetto si scoprirebbe solo al controllo di coerenza.
    """
    required = [
        f"BQ3.{family}.{scenario}"
        for family in ("adoption", "uplift")
        for scenario in ("worst", "base", "best")
    ]
    missing = [vid for vid in required if vid not in scenarios.get("values", {})]
    if missing:
        halt(
            f"reports/bq3_scenarios.json non porta le voci che BQ3-K1/BQ3-K2 "
            f"citano: {missing} (FR-011)"
        )


# ===========================================================================
# C2 e il verdetto — la regola di decisione di business_case.md §3
# ===========================================================================

def build_decision_rule(overlap: Decimal, values: dict) -> None:
    """Chiude la regola di decisione: l'operatore di C2 e il verdetto congiunto.

    Non ricalcola nulla. Riceve la quota di sovrapposizione **esatta** da
    `build_bq1k3` e legge dalle voci gia' scritte i due booleani di C1 e C3:
    ricalcolarli produrrebbe una seconda copia capace di divergere dalla prima
    senza che nulla lo segnali.

    Perche' queste sei voci esistono invece di essere ricavate a mente da chi
    legge: un confronto, un conteggio e una congiunzione costruiti su valori
    misurati sono essi stessi valori misurati. O esistono con un identificativo
    proprio e vengono ancorati, o non si scrivono (regola D5 del metodo di
    progetto). E' la zona in cui gli errori si concentrano, perche' e' l'unica in
    cui chi scrive calcola a mente.
    """
    required = ("KPI.BQ1K1.c1.above_median", "KPI.BQ2K3.c3_satisfied")
    missing = [vid for vid in required if vid not in values]
    if missing:
        halt(
            f"il verdetto si calcolerebbe senza tutte e "
            f"{DECISION_CONDITIONS} le condizioni: mancano {missing}\n"
            f"        e' un errore di ordine delle chiamate in main(). Un "
            f"verdetto costruito su due condizioni sarebbe indistinguibile, per "
            f"chi lo legge, da uno costruito su tre."
        )

    # --- C2, decisione D12: confronto **stretto** contro la soglia ---
    # Il confronto opera sul valore esatto, mai su quello arrotondato per la
    # pubblicazione: arrotondare prima di un confronto di soglia e' cio' che
    # `kpi_rounding` vieta, e qui il confronto *e'* la misura.
    c2 = overlap > C2_THRESHOLD
    margin = overlap - C2_THRESHOLD

    values["KPI.BQ1K3.c2.threshold"] = entry(
        C2_THRESHOLD, DIGITS_SHARE,
        "soglia della condizione C2 — maggioranza semplice del catalogo "
        "musicale, stipulazione di D12 e non una misura sui dati",
        UNIT_SHARE,
    )
    values["KPI.BQ1K3.c2.satisfied"] = bool_entry(
        c2,
        "C2 — la sovrapposizione dei profili di mood supera la soglia di "
        "maggioranza semplice, con confronto stretto (D12)",
    )
    values["KPI.BQ1K3.c2.margin"] = entry(
        margin, DIGITS_SHARE,
        "margine di C2 — di quanto la sovrapposizione misurata supera la "
        "soglia. Dipende dalla soglia: una soglia piu' severa lo restringe",
        UNIT_SHARE,
    )
    # Quanto la stima dovrebbe essere gonfiata perche' la conclusione cambi,
    # come quota del valore stesso. E' la forma che risponde al limite di D1 —
    # la stima e' per eccesso, e di quanto il progetto non lo misura — mentre il
    # margine assoluto risponde alla domanda piu' semplice di quanto il valore
    # superi la soglia. Nessuna delle due e' una stima dell'errore: sono
    # entrambe **condizioni sull'errore**.
    values["KPI.BQ1K3.c2.margin_share_of_value"] = entry(
        share_decimal(margin, overlap, "margine di C2 come quota del valore"),
        DIGITS_SHARE,
        "margine di C2 come quota del valore — di quanto la stima per eccesso "
        "dovrebbe sovrastimare la sovrapposizione reale perche' C2 cada",
        UNIT_SHARE,
    )

    # --- Il verdetto congiunto ---
    conditions = (
        values["KPI.BQ1K1.c1.above_median"]["value"] == "true",
        c2,
        values["KPI.BQ2K3.c3_satisfied"]["value"] == "true",
    )
    satisfied = sum(1 for condition in conditions if condition)
    verdict = all(conditions)

    # Una tautologia nel codice corretto, ed e' per questo che vale la pena
    # verificarla: e' la sola forma di incoerenza che nessun lettore noterebbe
    # leggendo l'artefatto, perche' le due voci si leggono in punti diversi.
    if verdict != (satisfied == DECISION_CONDITIONS):
        halt(
            f"il conteggio delle condizioni soddisfatte ({satisfied}) e la loro "
            f"congiunzione ({verdict}) sono incoerenti fra loro"
        )

    values["KPI.verdict.conditions_satisfied"] = count_entry(
        satisfied,
        f"condizioni soddisfatte della regola di decisione, su "
        f"{DECISION_CONDITIONS} — seleziona quale delle tre letture di "
        f"business_case.md §3 si applica",
    )
    values["KPI.verdict.all_satisfied"] = bool_entry(
        verdict,
        "verdetto — l'argomento di coerenza dell'espansione e' sostenuto: tutte "
        "e tre le condizioni della regola di decisione sono soddisfatte",
    )


# ===========================================================================
# Scrittura
# ===========================================================================

def fingerprint(path: Path) -> dict:
    payload = path.read_bytes()
    return {
        "file": str(path.relative_to(REPO)),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
    }


def build_artifact(values: dict, catalogs: dict, mood: dict) -> dict:
    return {
        "catalogs": catalogs,
        "conventions": {
            "kpi_median_rule": MEDIAN_RULE,
            "kpi_duration_zero_inclusion": DURATION_ZERO_RULE,
            "kpi_rounding": ROUNDING_RULE,
            "kpi_rank_rule": RANK_RULE,
            "kpi_quadrant_rule": QUADRANT_RULE,
            "kpi_scale_rule": SCALE_RULE,
            "kpi_decision_rule": DECISION_RULE,
            # Citazione, non valore nuovo: chi apre solo questo artefatto deve
            # poter leggere su quale versione della tabella dei mood i tre KPI
            # che ne dipendono sono stati calcolati, senza aprirne un secondo
            # (contratto di versione, content_taxonomy_bridge.md §5).
            "kpi_mood_table_version": str(mood["values"]["MOOD.table.version"]["value"]),
        },
        "schema_version": SCHEMA_VERSION,
        "sources": [
            fingerprint(path)
            for path in (NF_TITLES, NF_BRIDGE, SP_TRACKS, SP_PAIRS, MOOD, SCENARIOS)
        ],
        "values": values,
    }


def write_artifact(artifact: dict) -> None:
    # Nessuna marca temporale di esecuzione: se serve datare, si data la fonte,
    # che e' un fatto, non l'esecuzione, che e' rumore (FR-002).
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(artifact, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> None:
    titles = read_csv(NF_TITLES)
    bridge = read_csv(NF_BRIDGE)
    tracks = read_csv(SP_TRACKS)
    pairs = read_csv(SP_PAIRS)
    mood = read_json(MOOD)
    scenarios = read_json(SCENARIOS)

    categories = {row["category"] for row in bridge}
    segments = {row["track_genre"] for row in pairs}
    guard_cardinalities(categories, segments, mood)
    check_scenarios(scenarios)

    table = mood_table(mood)
    values: dict = {}

    build_bq1k1(titles, bridge, values)
    build_bq1k2(titles, tracks, values)
    overlap = build_bq1k3(tracks, table, values)
    high_zero, quadrant = build_segment_measures(pairs, bridge, table, values)
    # Dopo tutte e quattro: la regola di decisione legge i tre booleani delle
    # condizioni, e non ne esiste nessuno prima che le misure che li determinano
    # siano state calcolate.
    build_decision_rule(overlap, values)

    catalogs = {
        "kpi_segments": sorted(segments),
        "kpi_high_zero_segments": high_zero,
        "kpi_quadrant_segments": sorted(quadrant),
    }

    write_artifact(build_artifact(values, catalogs, mood))
    print(f"Scritto {OUT.relative_to(REPO)}: {len(values)} valori.")
    for vid in sorted(values):
        if vid.startswith("KPI.BQ2K"):
            continue  # 114 segmenti per tre misure: l'elenco sta nell'artefatto
        entry_ = values[vid]
        print(f"  {vid:<52} {entry_['display']:>12}  {entry_['unit']}")
    print(f"  (piu' le voci per segmento di BQ2-K1, BQ2-K2, BQ2-K3)")


if __name__ == "__main__":
    main()
