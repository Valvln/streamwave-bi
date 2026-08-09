#!/usr/bin/env python3
"""Profilo deterministico dei due dataset reali di StreamWave BI.

Legge `data/raw/` in sola lettura e produce `reports/data_profile.json`, artefatto
versionato di soli numeri che e' l'unica fonte di verita' di ogni valore prodotto
dal profiling (feature 002, FR-006).

Nessuna dipendenza esterna: sola libreria standard (decisione D1 di research.md).
Due esecuzioni sugli stessi file di origine producono un artefatto identico byte
per byte (FR-003, regole D5).

Uso:
    python3 scripts/profile_data.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw"
OUT = REPO / "reports" / "data_profile.json"

SCHEMA_VERSION = "1"

# ---------------------------------------------------------------------------
# Convenzioni di profilazione (decisione D9 di research.md).
# Sono dichiarate nell'artefatto: sono parte del dato, non del codice.
# ---------------------------------------------------------------------------

# Decimali a cui ogni valore non intero viene arrotondato prima della
# serializzazione. Regola 3 di D5: senza, differenze di rappresentazione in
# virgola mobile affiorerebbero nel file e romperebbero il determinismo.
ROUNDING_DECIMALS = 4

# Oltre questa soglia di valori distinti un campo categorico non viene
# enumerato: si riportano cardinalita' e valori piu' frequenti. La soglia e'
# superiore alla cardinalita' delle due tassonomie che la feature deve
# enumerare per intero (42 categorie video, 114 generi musicali) e inferiore a
# quella di ogni campo a testo libero.
HIGH_CARDINALITY_THRESHOLD = 120
TOP_N = 10

MISSING_DEFINITION = "campo assente, stringa vuota o composta di soli spazi"

# Criterio di riconoscimento del contenuto musicale dichiarato in una categoria
# del catalogo video (FR-021). E' esplicito perche' e' l'unico attributo del
# censimento che non sia lettura diretta: il documento di audit lo cita.
MUSIC_TERMS = ("music", "musical", "concert", "song", "sing", "opera", "sound")

# Regola di confronto per la corrispondenza lessicale fra nomi di genere
# musicale e nomi di categoria video (FR-022). Il conteggio non esiste senza la
# regola: una regola per token esatti darebbe un valore diverso.
LEXICAL_RULE = (
    "il nome del genere musicale, normalizzato in minuscolo, compare come "
    "sottostringa nel nome di almeno una categoria del catalogo video"
)

# Assi di mood usati dal framework KPI della 001 (nota metodologica §5.3).
MOOD_FIELDS = ("energy", "valence", "danceability")


# ---------------------------------------------------------------------------
# Formattazione (decisione D3): la forma con cui un valore va scritto nel
# documento di audit vive qui e in nessun altro posto. Il controllo di coerenza
# confronta stringhe, non interpreta la formattazione italiana dei numeri.
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Registro dei valori
# ---------------------------------------------------------------------------


class Profile:
    """Raccoglie i valori del profilo e li serializza in modo deterministico."""

    def __init__(self) -> None:
        self.values: dict[str, dict] = {}
        self.catalogs: dict[str, list] = {}

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
        if vid in self.values:
            raise ValueError(f"identificativo duplicato: {vid}")
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
        # Un anno non porta separatore di migliaia ne' decimali: "2017", non
        # "2.017,0". La forma di visualizzazione e' cio' che finisce nel
        # documento, quindi va corretta qui e non riscritta a mano la'.
        if unit == "anno":
            display = f"{float(value):.0f}"
        else:
            display = fmt_dec(float(value), decimals)
        return self.add(
            vid, float(value), display, unit, dataset, label, field, granularity,
        )

    def get(self, vid: str):
        return self.values[vid]["value"]


# ---------------------------------------------------------------------------
# Lettura delle sorgenti
# ---------------------------------------------------------------------------


def load(path: Path, expected_columns: tuple) -> tuple[list[dict], list[str]]:
    """Legge un CSV in sola lettura, fallendo esplicitamente su input mancante.

    FR-004: se un file manca o una colonna attesa e' assente, ci si ferma con un
    errore che la nomina. Un profilo silenziosamente incompleto e' peggio di
    nessun profilo.
    """
    if not path.exists():
        raise SystemExit(
            f"ERRORE: file di origine mancante: {path.relative_to(REPO)}\n"
            f"        data/raw/ non e' versionata. Ricostruiscila con "
            f"./scripts/download_data.sh (richiede un token Kaggle)."
        )
    csv.field_size_limit(10 ** 9)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    missing = [c for c in expected_columns if c not in fields]
    if missing:
        raise SystemExit(
            f"ERRORE: colonne attese assenti in {path.relative_to(REPO)}: "
            f"{', '.join(missing)}\n"
            f"        Il profilo non viene prodotto: correggere lo script o "
            f"verificare la sorgente."
        )
    return rows, fields


def fingerprint(path: Path) -> dict:
    """Provenienza della sorgente (FR-005): nome, byte, impronta del contenuto."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return {
        "file": str(path.relative_to(REPO)),
        "bytes": path.stat().st_size,
        "sha256": digest.hexdigest(),
    }


# ---------------------------------------------------------------------------
# Profilazione generica dei campi
# ---------------------------------------------------------------------------


def is_missing(raw) -> bool:
    return raw is None or str(raw).strip() == ""


def parse_number(raw: str):
    text = str(raw).strip()
    try:
        return int(text)
    except ValueError:
        pass
    try:
        value = float(text)
    except ValueError:
        return None
    return value


def observed_type(present: list[str]) -> str:
    if not present:
        return "vuoto"
    parsed = [parse_number(v) for v in present]
    if all(p is not None and isinstance(p, int) for p in parsed):
        return "intero"
    if all(p is not None for p in parsed):
        return "decimale"
    return "testo"


def profile_fields(profile: Profile, prefix: str, dataset: str, rows: list[dict], fields: list[str]) -> dict:
    """Forma, completezza, cardinalita' e frequenze di ogni campo (FR-012/13/14/19)."""
    total = len(rows)
    types: dict[str, str] = {}
    for field in fields:
        key = slug(field) if field.strip() else "unnamed"
        present = [r[field] for r in rows if not is_missing(r[field])]
        n_missing = total - len(present)
        label_field = field if field.strip() else "(colonna priva di nome)"

        profile.count(
            f"{prefix}.miss.{key}.count", n_missing, dataset,
            f"valori mancanti nel campo {label_field}", field=field,
            granularity="riga",
        )
        profile.pct(
            f"{prefix}.miss.{key}.pct", 100.0 * n_missing / total, dataset,
            f"quota di valori mancanti nel campo {label_field}", field=field,
            granularity="riga",
        )

        distinct = sorted(set(present))
        profile.count(
            f"{prefix}.card.{key}", len(distinct), dataset,
            f"valori distinti nel campo {label_field}", field=field,
            granularity="riga",
        )

        types[field] = observed_type(present)

        counter: dict[str, int] = {}
        for value in present:
            counter[value] = counter.get(value, 0) + 1
        if len(distinct) <= HIGH_CARDINALITY_THRESHOLD:
            for value in distinct:
                profile.count(
                    f"{prefix}.freq.{key}.{slug(value)}", counter[value], dataset,
                    f"righe con {label_field} = {value}", field=field,
                    granularity="riga",
                )
        else:
            ordered = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP_N]
            for rank, (value, freq) in enumerate(ordered, start=1):
                profile.count(
                    f"{prefix}.top.{key}.{rank:02d}", freq, dataset,
                    f"frequenza del {rank}o valore piu' comune di {label_field} "
                    f"({value})", field=field, granularity="riga",
                )
    return types


def profile_numeric(profile: Profile, prefix: str, dataset: str, name: str, values: list[float],
                    unit: str, field=None, granularity=None, decimals=2) -> None:
    """Posizione e dispersione di una variabile numerica (FR-017)."""
    if not values:
        return
    ordered = sorted(values)
    quartiles = statistics.quantiles(ordered, n=4, method="inclusive")
    stats = {
        "count": (len(ordered), "conteggio"),
        "min": (ordered[0], unit),
        "q1": (quartiles[0], unit),
        "median": (statistics.median(ordered), unit),
        "q3": (quartiles[2], unit),
        "max": (ordered[-1], unit),
        "mean": (statistics.fmean(ordered), unit),
        "iqr": (quartiles[2] - quartiles[0], unit),
        "stdev": (statistics.stdev(ordered) if len(ordered) > 1 else 0.0, unit),
    }
    descriptions = {
        "count": "valori validi", "min": "minimo", "q1": "primo quartile",
        "median": "mediana", "q3": "terzo quartile", "max": "massimo",
        "mean": "media", "iqr": "scarto interquartile",
        "stdev": "deviazione standard campionaria",
    }
    for stat, (value, stat_unit) in stats.items():
        vid = f"{prefix}.num.{name}.{stat}"
        if stat == "count":
            profile.count(vid, value, dataset, f"{descriptions[stat]} di {name}",
                          field=field, granularity=granularity)
        else:
            profile.num(vid, value, stat_unit, dataset,
                        f"{descriptions[stat]} di {name}", field=field,
                        granularity=granularity, decimals=decimals)


# ---------------------------------------------------------------------------
# Catalogo video
# ---------------------------------------------------------------------------

NETFLIX_COLUMNS = (
    "show_id", "type", "title", "director", "cast", "country", "date_added",
    "release_year", "rating", "duration", "listed_in", "description",
)

RATING_DOMAIN = (
    "G", "NC-17", "NR", "PG", "PG-13", "R", "TV-14", "TV-G", "TV-MA", "TV-PG",
    "TV-Y", "TV-Y7", "TV-Y7-FV", "UR",
)


def profile_netflix(profile: Profile) -> None:
    path = RAW / "netflix_titles.csv"
    rows, fields = load(path, NETFLIX_COLUMNS)
    total = len(rows)

    profile.count("NF.shape.rows", total, "netflix",
                  "titoli del catalogo video", granularity="titolo")
    profile.count("NF.shape.fields", len(fields), "netflix",
                  "campi del catalogo video")
    profile.count("NF.shape.distinct_ids", len({r["show_id"] for r in rows}),
                  "netflix", "identificativi di titolo distinti",
                  field="show_id", granularity="titolo")

    types = profile_fields(profile, "NF", "netflix", rows, fields)
    profile.catalogs["netflix_fields"] = [
        {"name": f if f.strip() else "", "observed_type": types[f]} for f in fields
    ]
    profile.catalogs["netflix_fields_excluded"] = []

    for kind, key, label in (("Movie", "movie", "film"), ("TV Show", "tvshow", "serie")):
        profile.count(f"NF.type.{key}", sum(1 for r in rows if r["type"] == kind),
                      "netflix", f"titoli di tipo {label}", field="type",
                      granularity="titolo")

    # --- Campo multi-valore: le categorie (FR-018) ---
    # Lo stesso campo produce conteggi diversi in due granularita', entrambe
    # legittime. Dichiararle e' cio' che impedisce di sommarle per sbaglio.
    assignments = 0
    titles_per_category: dict[str, int] = {}
    for row in rows:
        labels = {c.strip() for c in row["listed_in"].split(",") if c.strip()}
        assignments += len(labels)
        for label in labels:
            titles_per_category[label] = titles_per_category.get(label, 0) + 1

    categories = sorted(titles_per_category)
    profile.count("NF.cat.count", len(categories), "netflix",
                  "categorie distinte del catalogo video", field="listed_in",
                  granularity="categoria")
    profile.count("NF.cat.assignments", assignments, "netflix",
                  "assegnazioni titolo-categoria", field="listed_in",
                  granularity="coppia titolo-categoria")
    profile.num("NF.cat.per_title.mean", assignments / total, "categorie",
                "netflix", "categorie per titolo, in media", field="listed_in",
                granularity="titolo")

    # Censimento completo: tutte le categorie, nessuna selezione a monte (FR-021).
    for name in categories:
        profile.count(f"NF.cat.{slug(name)}.titles", titles_per_category[name],
                      "netflix", f"titoli distinti nella categoria {name}",
                      field="listed_in", granularity="titolo")

    musical = [c for c in categories if any(t in c.lower() for t in MUSIC_TERMS)]
    profile.count("NF.cat.music.count", len(musical), "netflix",
                  "categorie con contenuto musicale dichiarato secondo il "
                  "criterio registrato in conventions", field="listed_in",
                  granularity="categoria")
    profile.count("NF.cat.non_music.count", len(categories) - len(musical), "netflix",
                  "categorie senza contenuto musicale dichiarato",
                  field="listed_in", granularity="categoria")
    profile.count("NF.cat.music.titles", sum(titles_per_category[c] for c in musical),
                  "netflix", "titoli distinti nelle categorie a contenuto "
                  "musicale dichiarato", field="listed_in", granularity="titolo")
    # Nessun valore di quota qui: titoli musicali diviso titoli totali E' la
    # formula di BQ1-K1, la North Star. Il profilo espone numeratore e
    # denominatore, non il rapporto (FR-039). Il KPI e' della feature 007.
    profile.catalogs["netflix_categories"] = categories
    profile.catalogs["netflix_categories_musical"] = musical

    # --- Valori fuori dominio nella classificazione per eta' ---
    out_of_domain = sorted(
        {r["rating"].strip() for r in rows
         if not is_missing(r["rating"]) and r["rating"].strip() not in RATING_DOMAIN}
    )
    profile.count("NF.rating.out_of_domain.values", len(out_of_domain), "netflix",
                  "valori distinti della classificazione per eta' fuori dal "
                  "dominio dichiarato", field="rating", granularity="riga")
    profile.count("NF.rating.out_of_domain.rows",
                  sum(1 for r in rows if r["rating"].strip() in out_of_domain),
                  "netflix", "titoli con classificazione per eta' fuori dominio",
                  field="rating", granularity="titolo")
    profile.count("NF.rating.in_domain.values",
                  len({r["rating"].strip() for r in rows
                       if r["rating"].strip() in RATING_DOMAIN}),
                  "netflix", "valori distinti della classificazione per eta' "
                  "dentro il dominio dichiarato", field="rating",
                  granularity="riga")
    profile.catalogs["netflix_rating_out_of_domain"] = out_of_domain

    # --- Durate: formato misto, film in minuti e serie in stagioni ---
    minutes, seasons, malformed = [], [], 0
    for row in rows:
        text = row["duration"].strip()
        if not text:
            continue
        if text.endswith("min"):
            minutes.append(int(text.split()[0]))
        elif text.endswith(("Season", "Seasons")):
            seasons.append(int(text.split()[0]))
        else:
            malformed += 1
    profile.count("NF.duration.missing",
                  sum(1 for r in rows if is_missing(r["duration"])), "netflix",
                  "titoli privi di durata", field="duration", granularity="titolo")
    profile.count("NF.duration.malformed", malformed, "netflix",
                  "durate in un formato non riconosciuto", field="duration",
                  granularity="titolo")
    profile_numeric(profile, "NF", "netflix", "movie_duration_min", minutes,
                    "minuti", field="duration", granularity="film", decimals=1)
    profile_numeric(profile, "NF", "netflix", "tvshow_seasons", seasons,
                    "stagioni", field="duration", granularity="serie", decimals=1)

    years = [int(r["release_year"]) for r in rows if not is_missing(r["release_year"])]
    profile_numeric(profile, "NF", "netflix", "release_year", years, "anno",
                    field="release_year", granularity="titolo", decimals=1)


# ---------------------------------------------------------------------------
# Catalogo musicale
# ---------------------------------------------------------------------------

SPOTIFY_COLUMNS = (
    "track_id", "artists", "album_name", "track_name", "popularity",
    "duration_ms", "explicit", "danceability", "energy", "key", "loudness",
    "mode", "speechiness", "acousticness", "instrumentalness", "liveness",
    "valence", "tempo", "time_signature", "track_genre",
)


def profile_spotify(profile: Profile) -> None:
    path = RAW / "spotify_tracks_dataset.csv"
    rows, fields = load(path, SPOTIFY_COLUMNS)
    total = len(rows)

    profile.count("SP.shape.rows", total, "spotify",
                  "righe del catalogo musicale", granularity="coppia traccia-genere")
    profile.count("SP.shape.fields", len(fields), "spotify",
                  "campi del catalogo musicale")

    types = profile_fields(profile, "SP", "spotify", rows, fields)
    profile.catalogs["spotify_fields"] = [
        {"name": f if f.strip() else "", "observed_type": types[f]} for f in fields
    ]
    profile.catalogs["spotify_fields_excluded"] = []

    # --- Duplicazione degli identificativi (FR-015) ---
    # Entrambe le letture della sovrapposizione, con identificativi distinti:
    # l'affermazione "sovrastima di circa un quinto" della 001 non dichiara
    # quale delle due intendesse (ritrovamento F2).
    occurrences: dict[str, int] = {}
    for row in rows:
        occurrences[row["track_id"]] = occurrences.get(row["track_id"], 0) + 1
    distinct = len(occurrences)
    repeated = sum(1 for n in occurrences.values() if n > 1)

    profile.count("SP.id.distinct", distinct, "spotify",
                  "identificativi di traccia distinti", field="track_id",
                  granularity="traccia deduplicata")
    profile.count("SP.id.repeated", repeated, "spotify",
                  "identificativi che compaiono piu' di una volta",
                  field="track_id", granularity="traccia deduplicata")
    profile.count("SP.id.duplicate_rows", total - distinct, "spotify",
                  "righe eccedenti rispetto agli identificativi distinti",
                  field="track_id", granularity="riga")
    profile.count("SP.id.max_multiplicity", max(occurrences.values()), "spotify",
                  "molteplicita' massima di un identificativo", field="track_id",
                  granularity="traccia deduplicata")
    profile.pct("SP.id.duplicate_share", 100.0 * (total - distinct) / total,
                "spotify", "quota di righe che sono ripetizioni di una traccia "
                "gia' presente", field="track_id", granularity="riga")
    profile.pct("SP.id.inflation", 100.0 * (total - distinct) / distinct,
                "spotify", "di quanto un totale non deduplicato eccede il totale "
                "sulle tracce distinte", field="track_id",
                granularity="traccia deduplicata")

    # --- Struttura del campionamento (FR-016) ---
    per_genre: dict[str, int] = {}
    for row in rows:
        per_genre[row["track_genre"]] = per_genre.get(row["track_genre"], 0) + 1
    genres = sorted(per_genre)
    profile.count("SP.genre.count", len(genres), "spotify",
                  "generi musicali distinti", field="track_genre",
                  granularity="genere")
    profile.count("SP.genre.row_counts_distinct", len(set(per_genre.values())),
                  "spotify", "quanti conteggi di righe per genere diversi "
                  "esistono: 1 significa campione bilanciato per costruzione",
                  field="track_genre", granularity="genere")
    profile.count("SP.genre.rows_min", min(per_genre.values()), "spotify",
                  "righe del genere meno numeroso", field="track_genre",
                  granularity="genere")
    profile.count("SP.genre.rows_max", max(per_genre.values()), "spotify",
                  "righe del genere piu' numeroso", field="track_genre",
                  granularity="genere")
    profile.catalogs["spotify_genres"] = genres

    # --- Massa di zeri dell'indice di popolarita' ---
    popularity = [int(r["popularity"]) for r in rows]
    zeros = sum(1 for p in popularity if p == 0)
    profile.count("SP.pop.zero.count", zeros, "spotify",
                  "righe con indice di popolarita' pari a zero",
                  field="popularity", granularity="coppia traccia-genere")
    profile.pct("SP.pop.zero.pct", 100.0 * zeros / total, "spotify",
                "quota di righe con indice di popolarita' pari a zero",
                field="popularity", granularity="coppia traccia-genere")

    zero_by_genre = {
        g: sum(1 for r in rows if r["track_genre"] == g and int(r["popularity"]) == 0)
        for g in genres
    }
    for genre in genres:
        profile.pct(f"SP.pop.zero.by_genre.{slug(genre)}",
                    100.0 * zero_by_genre[genre] / per_genre[genre], "spotify",
                    f"quota a popolarita' zero nel genere {genre}",
                    field="popularity", granularity="coppia traccia-genere")
    profile.count("SP.pop.zero.genres_fully_zero",
                  sum(1 for g in genres if zero_by_genre[g] == per_genre[g]),
                  "spotify", "generi interamente a popolarita' zero",
                  field="popularity", granularity="genere")
    profile.count("SP.pop.zero.genres_over_60",
                  sum(1 for g in genres
                      if zero_by_genre[g] / per_genre[g] > 0.60),
                  "spotify", "generi con oltre il 60% di righe a popolarita' zero",
                  field="popularity", granularity="genere")

    # --- Distribuzioni numeriche di ogni campo numerico osservato ---
    for field in fields:
        if types[field] not in ("intero", "decimale"):
            continue
        name = slug(field) if field.strip() else "unnamed"
        values = [parse_number(r[field]) for r in rows if not is_missing(r[field])]
        values = [float(v) for v in values if v is not None]
        decimals = 1 if field in ("popularity", "duration_ms", "tempo", "loudness") else 4
        profile_numeric(profile, "SP", "spotify", name, values,
                        "valore", field=field, granularity="coppia traccia-genere",
                        decimals=decimals)

    durations = [int(r["duration_ms"]) for r in rows if not is_missing(r["duration_ms"])]
    profile.num("SP.duration.median_s", statistics.median(durations) / 1000.0,
                "secondi", "spotify", "durata mediana di una riga, in secondi",
                field="duration_ms", granularity="coppia traccia-genere", decimals=1)
    profile.count("SP.duration.zero", sum(1 for d in durations if d == 0), "spotify",
                  "righe con durata dichiarata pari a zero", field="duration_ms",
                  granularity="coppia traccia-genere")

    # --- Completezza degli assi di mood (§5.3 della 001) ---
    for field in MOOD_FIELDS:
        profile.count(f"SP.mood.{field}.missing",
                      sum(1 for r in rows if is_missing(r[field])), "spotify",
                      f"valori mancanti sull'asse di mood {field}", field=field,
                      granularity="coppia traccia-genere")


# ---------------------------------------------------------------------------
# Corrispondenza lessicale fra le due tassonomie
# ---------------------------------------------------------------------------


def profile_lexical(profile: Profile) -> None:
    """Quante etichette di genere musicale ricorrono nei nomi di categoria video.

    FR-022: il valore descrive i vocabolari di etichette, non la corrispondenza
    dei contenuti. La 001 (decisione D1) ha gia' escluso il matching lessicale
    come piano di confronto fra i due cataloghi; questo valore lo documenta, non
    lo riabilita.
    """
    categories = profile.catalogs["netflix_categories"]
    genres = profile.catalogs["spotify_genres"]
    lowered = [c.lower() for c in categories]
    matched = sorted(g for g in genres if any(g.lower() in c for c in lowered))
    profile.count("X.genre_lexical.count", len(matched), "entrambi",
                  "generi musicali il cui nome ricorre in almeno una categoria "
                  "video secondo la regola dichiarata in conventions",
                  granularity="etichetta")
    profile.pct("X.genre_lexical.share", 100.0 * len(matched) / len(genres),
                "entrambi", "quota di generi musicali con corrispondenza "
                "lessicale", granularity="etichetta")
    profile.catalogs["genre_lexical_matches"] = matched


# ---------------------------------------------------------------------------
# Inventario dei valori citati dalla 001 e registro delle divergenze
# ---------------------------------------------------------------------------

# Ogni voce: sigla, enunciato come la 001 lo scrive, collocazione, e i controlli
# nella forma (identificativo, valore affermato, decimali di confronto). Il
# confronto arrotonda il valore rigenerato ai decimali con cui la 001 lo
# dichiara: e' il solo modo di confrontare "29,9%" con un calcolo esatto.
CLAIMS_001 = [
    {
        "id": "V01",
        "text": "8.807 titoli: 6.131 film e 2.676 serie TV",
        "source": "specs/001-business-case-kpi/research.md — inventario Netflix",
        "checks": [("NF.shape.rows", 8807, 0), ("NF.type.movie", 6131, 0),
                   ("NF.type.tvshow", 2676, 0)],
    },
    {
        "id": "V02",
        "text": "completezza per campo: type 0%, duration 0,03%, listed_in 0%, "
                "rating 0,05%, release_year 0%, date_added 0,1%, country 9,4%, "
                "director 29,9%, description 0%",
        "source": "specs/001-business-case-kpi/research.md — tabella completezza",
        "checks": [("NF.miss.type.pct", 0.0, 2), ("NF.miss.duration.pct", 0.03, 2),
                   ("NF.miss.listed_in.pct", 0.0, 2), ("NF.miss.rating.pct", 0.05, 2),
                   ("NF.miss.release_year.pct", 0.0, 2),
                   ("NF.miss.date_added.pct", 0.1, 1),
                   ("NF.miss.country.pct", 9.4, 1),
                   ("NF.miss.director.pct", 29.9, 1),
                   ("NF.miss.description.pct", 0.0, 2)],
    },
    {
        "id": "V03",
        "text": "42 generi distinti, multi-valore per titolo",
        "source": "specs/001-business-case-kpi/research.md — inventario Netflix",
        "checks": [("NF.cat.count", 42, 0)],
    },
    {
        "id": "V04",
        "text": "18 valori (classificazione per eta')",
        "source": "specs/001-business-case-kpi/research.md — inventario Netflix",
        "checks": [("NF.card.rating", 18, 0)],
    },
    {
        "id": "V05",
        "text": "114.000 righe, 114 generi",
        "source": "specs/001-business-case-kpi/research.md — inventario Spotify",
        "checks": [("SP.shape.rows", 114000, 0), ("SP.genre.count", 114, 0)],
    },
    {
        "id": "V06",
        "text": "89.741 track_id distinti su 114.000 righe: 16.641 identificativi "
                "compaiono piu' volte; il 21% delle righe sono tracce ripetute",
        "source": "specs/001-business-case-kpi/research.md — ritrovamento R2",
        "checks": [("SP.id.distinct", 89741, 0), ("SP.id.repeated", 16641, 0),
                   ("SP.id.duplicate_share", 21.0, 0)],
    },
    {
        "id": "V07",
        "text": "ogni genere ha esattamente 1.000 tracce",
        "source": "specs/001-business-case-kpi/research.md — ritrovamento R1",
        "checks": [("SP.genre.rows_min", 1000, 0), ("SP.genre.rows_max", 1000, 0),
                   ("SP.genre.row_counts_distinct", 1, 0)],
    },
    {
        "id": "V08",
        "text": "duration_ms (mediana 213 s)",
        "source": "specs/001-business-case-kpi/research.md — inventario Spotify",
        "checks": [("SP.duration.median_s", 213.0, 0)],
    },
    {
        "id": "V09",
        "text": "film in minuti (6.128 titoli, mediana 98 min, range 3-312)",
        "source": "specs/001-business-case-kpi/research.md — ritrovamento R3",
        "checks": [("NF.num.movie_duration_min.count", 6128, 0),
                   ("NF.num.movie_duration_min.median", 98.0, 0),
                   ("NF.num.movie_duration_min.min", 3.0, 0),
                   ("NF.num.movie_duration_min.max", 312.0, 0)],
    },
    {
        "id": "V10",
        "text": "14,1% delle tracce ha popularity = 0",
        "source": "specs/001-business-case-kpi/research.md — ritrovamento R5",
        "checks": [("SP.pop.zero.pct", 14.1, 1)],
    },
    {
        "id": "V11",
        "text": "jazz 68%, iranian 66%, romance 64%, soul 61%, latin 59%; "
                "nessun genere e' interamente a zero",
        "source": "specs/001-business-case-kpi/research.md — ritrovamento R5",
        "checks": [("SP.pop.zero.by_genre.jazz", 68.0, 0),
                   ("SP.pop.zero.by_genre.iranian", 66.0, 0),
                   ("SP.pop.zero.by_genre.romance", 64.0, 0),
                   ("SP.pop.zero.by_genre.soul", 61.0, 0),
                   ("SP.pop.zero.by_genre.latin", 59.0, 0),
                   ("SP.pop.zero.genres_fully_zero", 0, 0)],
    },
    {
        "id": "V12",
        "text": "solo 6 generi Spotify su 114 hanno una corrispondenza lessicale "
                "con i 42 generi Netflix",
        "source": "specs/001-business-case-kpi/research.md — ritrovamento R4",
        "checks": [("X.genre_lexical.count", 6, 0)],
    },
    {
        "id": "V13",
        "text": "un totale calcolato senza deduplicare sovrastima di circa un quinto",
        "source": "docs/business_case.md §5.2",
        "checks": [],
        "forced_status": "ambiguo",
        "note": "L'enunciato ammette due letture aritmetiche e non dichiara quale "
                "adotti. Come quota di righe che sono ripetizioni vale "
                "SP.id.duplicate_share; come eccesso del totale non deduplicato "
                "sul totale corretto vale SP.id.inflation. La prima e' vicina a "
                "un quinto, la seconda no.",
        "related": ["SP.id.duplicate_share", "SP.id.inflation"],
    },
    {
        "id": "V14",
        "text": "audio feature reali e complete: valence, energy, danceability e "
                "le altre",
        "source": "specs/001-business-case-kpi/research.md — inventario Spotify",
        "checks": [("SP.mood.energy.missing", 0, 0),
                   ("SP.mood.valence.missing", 0, 0),
                   ("SP.mood.danceability.missing", 0, 0)],
    },
]


def build_inventory(profile: Profile) -> dict:
    inventory = {}
    for claim in CLAIMS_001:
        ids = [vid for vid, _, _ in claim["checks"]] + claim.get("related", [])
        missing = [vid for vid in ids if vid not in profile.values]
        if missing:
            raise SystemExit(
                f"ERRORE: la sigla {claim['id']} dell'inventario rimanda a "
                f"identificativi inesistenti: {', '.join(missing)}"
            )
        inventory[claim["id"]] = sorted(ids)
    return inventory


def build_divergences(profile: Profile) -> list:
    """Confronto automatico fra le affermazioni della 001 e i valori rigenerati.

    Decisione D6: una divergenza e' un ritrovamento, e affidarne il
    riconoscimento all'attenzione di chi scrive e' il modo tipico in cui sfugge.
    """
    registry = []
    for claim in CLAIMS_001:
        mismatches = []
        for vid, claimed, decimals in claim["checks"]:
            actual = profile.get(vid)
            if round(float(actual), decimals) != round(float(claimed), decimals):
                mismatches.append({
                    "value_id": vid,
                    "claimed": claimed,
                    "regenerated": actual,
                    "compared_at_decimals": decimals,
                })
        status = claim.get("forced_status") or ("diverge" if mismatches else "coincide")
        entry = {
            "claim_id": claim["id"],
            "claimed_text": claim["text"],
            "source": claim["source"],
            "status": status,
            "mismatches": mismatches,
        }
        if claim.get("note"):
            entry["note"] = claim["note"]
        registry.append(entry)
    return registry


# ---------------------------------------------------------------------------
# Uscita
# ---------------------------------------------------------------------------


def main() -> int:
    profile = Profile()
    profile_netflix(profile)
    profile_spotify(profile)
    profile_lexical(profile)

    artifact = {
        "schema_version": SCHEMA_VERSION,
        "conventions": {
            "missing": MISSING_DEFINITION,
            "high_cardinality_threshold": HIGH_CARDINALITY_THRESHOLD,
            "high_cardinality_top_n": TOP_N,
            "rounding_decimals": ROUNDING_DECIMALS,
            "music_terms": list(MUSIC_TERMS),
            "lexical_rule": LEXICAL_RULE,
            "rating_domain": list(RATING_DOMAIN),
            "dispersion": "scarto interquartile e deviazione standard campionaria",
        },
        "sources": [
            fingerprint(RAW / "netflix_titles.csv"),
            fingerprint(RAW / "spotify_tracks_dataset.csv"),
        ],
        "values": profile.values,
        "catalogs": profile.catalogs,
        "inventory_001": build_inventory(profile),
        "divergences": build_divergences(profile),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Regole di serializzazione deterministica (D5): chiavi ordinate, nessun
    # timestamp, indentazione fissa, UTF-8 senza escape, ritorno a capo finale.
    with OUT.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(artifact, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")

    diverging = [d for d in artifact["divergences"] if d["status"] != "coincide"]
    print(f"Profilo scritto in {OUT.relative_to(REPO)}")
    print(f"  valori: {len(profile.values)}")
    print(f"  sigle dell'inventario 001: {len(artifact['inventory_001'])}")
    print(f"  divergenze non coincidenti: {len(diverging)}")
    for entry in diverging:
        print(f"    {entry['claim_id']} [{entry['status']}] {entry['claimed_text'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
