# Le misure dei KPI, con i loro valori

Il valore di ciascuno degli otto<!--#--> KPI del [business case](business_case.md), la formula DAX con cui si scrive nel modello, la provenienza di ogni numero e i limiti che quel numero porta con sé.

**Data**: 2026-08-22 · **Feature**: `007b` · **Stato**: concluso, [revisionato in contesto pulito](../specs/007b-kpi-measures/review.md)

---

## 1. Che cosa è questo documento, e come si legge

[`kpi_operators.md`](kpi_operators.md) ha fissato **con quale regola** ciascun KPI andasse calcolato, e dichiara in apertura di non contenere alcun valore. Questo documento contiene i valori. È il primo del progetto in cui un numero pubblicato è un **risultato di questa feature** e non un input ereditato da una precedente: ogni cifra che segue nasce qui, e per questo ciascuna porta un'ancora verso l'artefatto che la produce.

**La grammatica delle ancore** è quella di [`convenzioni-marcatura.md`](convenzioni-marcatura.md), e questa pagina è verificata in **severità stretta**: una quantità priva di ancora o di marcatore di non-misurato è un errore, non un avviso.

### 1.1 Perché i valori li calcola uno script e non il motore di reporting

Il `.pbix` non è versionato, e le misure DAX si scrivono nella GUI di Power BI Desktop — fuori dall'automazione, per il principio V della constitution. Un valore letto a schermo e ricopiato a mano in questa pagina non sarebbe riproducibile da nessun altro: chi clona il repository senza una licenza Power BI non avrebbe modo di rigenerarlo, e il principio II cadrebbe.

I valori pubblicati sono quindi calcolati da [`scripts/build_kpi_measures.py`](../scripts/build_kpi_measures.py), che applica **le stesse regole** di [`data_model.md`](data_model.md) e `kpi_operators.md` sugli stessi dati e scrive [`reports/kpi_measures.json`](../reports/kpi_measures.json). La catena riproducibile è intera:

```bash
python3 scripts/build_datasets.py       # data/raw/ -> data/processed/
python3 scripts/build_kpi_measures.py   # data/processed/ -> reports/kpi_measures.json
```

Lo script è sullo schema di [`scripts/build_bq3_scenarios.py`](../scripts/build_bq3_scenarios.py): aritmetica interamente in `decimal.Decimal` e mai in virgola mobile, `ROUND_HALF_UP` dichiarato esplicitamente invece della modalità predefinita `ROUND_HALF_EVEN`, nessuna lettura dell'orologio, nessun generatore casuale. Due<!--#--> esecuzioni consecutive producono file identici byte per byte, e lo stesso vale rigenerando prima `data/processed/`.

**Che cosa questo non garantisce, ed è la ragione per cui la §11 esiste.** Che lo script e il motore DAX diano lo stesso numero non è assunto: è verificato incollando le formule di questa pagina nel modello e leggendo i valori restituiti. L'esito di quel confronto vive in [`reports/kpi_engine_check.json`](../reports/kpi_engine_check.json) e ciascuna sezione lo dichiara.

### 1.2 Arrotondamento e precisione

Una regola per **unità di misura**, non per KPI: un giudizio preso otto<!--#--> volte si discute otto<!--#--> volte.

| Unità | Cifre pubblicate | Dove si applica |
|---|---|---|
| quota o indice sul dominio `0-1` | 4<!--#--> decimali | `share`, `overlap`, `affinity`, `score`, `zero_share`, profili di mood |
| durata in minuti | 2<!--#--> decimali | `format_duration_gap` e le mediane che lo compongono |
| indice di popolarità sulla scala `0-100` | 1<!--#--> decimale | `segment_demand_index` e la soglia del quadrante |
| conteggi, posizioni in graduatoria, esiti booleani | nessun arrotondamento | esatti per costruzione |

L'arrotondamento è **di presentazione**. Ogni derivazione — mediana, differenza, media delle distanze, punteggio pesato, confronto di soglia, ordinamento — opera sui valori esatti e arrotonda soltanto al momento di scrivere: arrotondare prima sposterebbe una mediana o farebbe cadere un segmento dal lato sbagliato di una soglia.

**Due<!--#--> precisazioni che la regola per unità non copre da sola**, entrambe dichiarate nella convenzione `kpi_rounding` dell'artefatto:

- una **mediana di conteggi** può essere un mezzo intero, perché i conteggi per categoria sono 42<!--@CL.NF.category.distinct--> e il numero è pari: si pubblica a 2<!--#--> decimali e non come intero;
- una sola voce fa eccezione alla regola dei minuti, ed è dichiarata in §3.3.

---

## 2. `BQ1-K1` — `music_adjacent_catalog_share`

**Domanda di business**: BQ1 — Posizionamento. Quanto del catalogo video è già contenuto musicale, cioè quanto il terreno su cui StreamWave vorrebbe entrare sia già presidiato da ciò che possiede. · **Confidenza**: **alta**, invariata da `business_case.md` §5.4 · **Operatore**: `kpi_operators.md` §2.1 (`D9.1`, `D9.3`)

**Formula in prosa**: titoli distinti assegnati alla categoria `Music & Musicals`<!--@catalogs.netflix_categories_musical-->, diviso i titoli distinti del catalogo video.

### 2.1 Il valore

| | Valore | Ancora |
|---|---|---|
| `music_adjacent_catalog_share` | 0,0426<!--@KPI.BQ1K1.share--> | `KPI.BQ1K1.share` |
| numeratore — titoli in `Music & Musicals` | 375<!--@KPI.BQ1K1.numerator_titles--> | `KPI.BQ1K1.numerator_titles` |
| denominatore — titoli distinti del catalogo | 8807<!--@KPI.BQ1K1.denominator_titles--> | `KPI.BQ1K1.denominator_titles` |

**Il denominatore non è il conteggio delle assegnazioni.** Sono 8.807<!--@CL.NF.titles.rows.after--> titoli distinti contro 19.323<!--@CL.NF.category.assignments--> assegnazioni, e confonderli è la trappola dichiarata di questo KPI: userebbe un denominatore più che doppio e dimezzerebbe abbondantemente la quota.

**Provenienza nel modello dati**: `bridge_title_category` (numeratore), `dim_title` (denominatore), `dim_category` (l'etichetta) — `data_model.md` §8 e §10.2.

### 2.2 La formula DAX

```dax
music_adjacent_catalog_share =
DIVIDE (
    CALCULATE (
        DISTINCTCOUNT ( bridge_title_category[show_id] ),
        dim_category[category] = "Music & Musicals"
    ),
    DISTINCTCOUNT ( dim_title[show_id] )
)
```

`DIVIDE` invece dell'operatore `/` per la stessa ragione per cui lo script si ferma su un denominatore nullo: un catalogo vuoto deve dare un risultato assente, non un errore che si propaga a ogni visuale della pagina.

### 2.3 `C1` — la condizione della North Star, che non è la quota

`C1` chiede che «il contenuto musicale non sia residuale nel catalogo attuale: la sua categoria si colloca nella metà superiore delle categorie per numero di titoli» (`business_case.md` §3). Non è calcolabile dalla quota, che è una proporzione sull'intero catalogo: `C1` chiede una posizione rispetto alla mediana delle categorie (`D9.2`).

| | Valore | Ancora |
|---|---|---|
| titoli di `Music & Musicals` | 375<!--@KPI.BQ1K1.c1.category_count.music_musicals--> | `KPI.BQ1K1.c1.category_count.music_musicals` |
| mediana dei 42<!--@CL.NF.category.distinct--> conteggi per categoria | 248,00<!--@KPI.BQ1K1.c1.median_of_42--> | `KPI.BQ1K1.c1.median_of_42` |
| **`C1` è soddisfatta** | sì<!--@KPI.BQ1K1.c1.above_median--> | `KPI.BQ1K1.c1.above_median` |

La soglia è **stretta**: una categoria esattamente sulla mediana non supera. Qui il margine non è marginale, ma la convenzione va dichiarata comunque, per coerenza con la soglia dei quadranti di §7.

```dax
c1_music_above_median =
VAR CountsByCategory =
    ADDCOLUMNS (
        VALUES ( dim_category[category] ),
        "@titles", CALCULATE ( DISTINCTCOUNT ( bridge_title_category[show_id] ) )
    )
VAR MedianOfCategories = MEDIANX ( CountsByCategory, [@titles] )
VAR MusicTitles =
    CALCULATE (
        DISTINCTCOUNT ( bridge_title_category[show_id] ),
        dim_category[category] = "Music & Musicals"
    )
RETURN
    IF ( MusicTitles > MedianOfCategories, TRUE (), FALSE () )
```

**Che cosa `C1` soddisfatta significa, e che cosa no.** Significa che la categoria musicale non è residuale per numero di titoli. Non significa che il catalogo sia musicale: la quota di §2.1 dice che è il 4<!--#--> per cento circa, e le due<!--#--> letture non si contraddicono — misurano cose diverse. Una categoria può stare sopra la mediana di 42<!--@CL.NF.category.distinct--> categorie e restare una frazione piccola del totale, ed è esattamente ciò che accade qui.

### 2.4 L'invarianza del numeratore, verificata invece che assunta

`kpi_operators.md` §2.1 dichiarava l'invarianza del numeratore fra dato di origine e dato trasformato come **un'assunzione dichiarata, non una conseguenza dedotta**, e indicava dove si sarebbe chiusa: eseguendo l'operatore di §2.2, «la verifica esce quasi gratis, ed è il momento in cui va fatta». Questa feature l'ha eseguita.

| | Valore | Ancora |
|---|---|---|
| conteggio sul dato **trasformato** (`netflix_title_category.csv`) | 375<!--@KPI.BQ1K1.north_star_invariance.transformed_count--> | `KPI.BQ1K1.north_star_invariance.transformed_count` |
| conteggio sul dato di **origine** (`NF.cat.music_musicals.titles`) | 375<!--@KPI.BQ1K1.north_star_invariance.origin_count--> | `KPI.BQ1K1.north_star_invariance.origin_count` |
| differenza | 0<!--@KPI.BQ1K1.north_star_invariance.delta--> | `KPI.BQ1K1.north_star_invariance.delta` |
| **i due<!--#--> conteggi coincidono** | sì<!--@KPI.BQ1K1.north_star_invariance.matches--> | `KPI.BQ1K1.north_star_invariance.matches` |

> **L'assunzione `D9.1` è chiusa: l'invarianza del numeratore della North Star non è più un'assunzione, è un fatto verificato.**

L'esito è dichiarato come valore con ancora propria — `matches` e `delta` — e non lasciato dedurre dall'accostamento di due<!--#--> numeri uguali: un confronto fra valori misurati è esso stesso un valore misurato, e questa è la forma in cui si pubblica.

**Che cosa la verifica dimostra, e che cosa continua a non dimostrare.** Dimostra che il conteggio dei titoli di `Music & Musicals`<!--@catalogs.netflix_categories_musical--> è identico prima e dopo la trasformazione. Non dimostra che la corrispondenza fra titoli e categorie sia rimasta identica riga per riga su **tutte** le 42<!--@CL.NF.category.distinct--> categorie: due<!--#--> totali che coincidono su una categoria restano compatibili, in linea di principio, con riassegnazioni che si compensano altrove. La verifica chiude l'assunzione **sul numeratore della North Star**, che è ciò che `D9.1` dichiarava aperto, e non un invariante generale del ponte.

**Stato di verifica contro il motore reale (E9)**: vedi §11 — lo stato è dichiarato in un punto solo perché discende da un unico confronto, congelato in un unico artefatto.

---

## 3. `BQ1-K2` — `format_duration_gap`

**Domanda di business**: BQ1 — Posizionamento. Quanto il formato musicale sia diverso, per durata, dal formato video già servito — cioè quanto la nuova offerta chieda al pubblico un'abitudine di consumo diversa. · **Confidenza**: **alta**, invariata da `business_case.md` §5.4 · **Operatore**: `kpi_operators.md` §3 (`D5`)

**Formula in prosa**: durata mediana di una traccia musicale, in minuti, **meno** durata mediana di un film del catalogo video, in minuti. Il risultato si pubblica **con il proprio segno**, non in valore assoluto.

### 3.1 Il valore

| | Valore | Ancora |
|---|---|---|
| `format_duration_gap` | -94,45<!--@KPI.BQ1K2.gap_minutes--> minuti | `KPI.BQ1K2.gap_minutes` |
| durata mediana di una traccia | 3,55<!--@KPI.BQ1K2.median_music_all_rows--> minuti | `KPI.BQ1K2.median_music_all_rows` |
| durata mediana di un film | 98,00<!--@KPI.BQ1K2.median_movie--> minuti | `KPI.BQ1K2.median_movie` |
| tracce deduplicate | 89741<!--@KPI.BQ1K2.music_tracks--> | `KPI.BQ1K2.music_tracks` |
| titoli di tipo `Movie` | 6131<!--@KPI.BQ1K2.movie_titles--> | `KPI.BQ1K2.movie_titles` |

**Il segno negativo non è un allarme.** `kpi_operators.md` §3 lo aveva dichiarato prima che il numero esistesse: un film dura tipicamente decine di minuti e una traccia pochi, quindi il valore sarebbe stato fortemente negativo. È la conseguenza aritmetica della differenza di formato che il KPI esiste per misurare. Il KPI **non ha direzione normativa** — non è un obiettivo da massimizzare — e il segno porta l'informazione su quale dei due<!--#--> formati sia più lungo, che il valore assoluto perderebbe.

**Grana**: traccia deduplicata sul lato musicale, film sul lato video. Le serie sono escluse: il catalogo video le misura in stagioni, e convertirle richiederebbe un'assunzione che i dati non contengono.

**Provenienza nel modello dati**: `dim_track[duration_min]` — che `data_model.md` §13 definisce come `duration_ms` diviso `60000`, senza alcun arrotondamento a livello di colonna — e `dim_title[movie_duration_min]` filtrata ai soli film.

### 3.2 La formula DAX

```dax
format_duration_gap =
VAR MedianTrackMinutes = MEDIANX ( dim_track, dim_track[duration_min] )
VAR MedianMovieMinutes =
    CALCULATE (
        MEDIANX ( dim_title, dim_title[movie_duration_min] ),
        dim_title[type] = "Movie"
    )
RETURN
    MedianTrackMinutes - MedianMovieMinutes
```

### 3.3 `D11` — le righe a durata degenere entrano nella mediana

Era il primo dei tre<!--#--> vincoli lasciati aperti da `kpi_operators.md` §12. La decisione è **l'inclusione**, per la stessa disciplina già applicata da `D7` agli zeri di popolarità: la trasformazione ha scelto di conservare e marcare, non di eliminare, e una misura che filtrasse sulla marcatura ritirerebbe quella scelta senza dichiararlo.

La decisione è resa **verificabile** invece che dichiarata a parole: entrambe le varianti sono calcolate e pubblicate.

| Variante | Valore | Ancora |
|---|---|---|
| tutte le righe, inclusa quella marcata `is_duration_zero` — **adottata** | 3,55<!--@KPI.BQ1K2.median_music_all_rows--> minuti | `KPI.BQ1K2.median_music_all_rows` |
| esclusa la riga marcata `is_duration_zero` | 3,55<!--@KPI.BQ1K2.median_music_excluding_zero--> minuti | `KPI.BQ1K2.median_music_excluding_zero` |
| **differenza fra le due<!--#--> varianti** | -0,000042<!--@KPI.BQ1K2.median_variant_delta--> minuti | `KPI.BQ1K2.median_variant_delta` |

**Perché questa voce sola porta sei<!--#--> decimali** invece dei 2<!--#--> che la regola dei minuti prescrive. La differenza vale meno di un centesimo di minuto, e a 2<!--#--> decimali uscirebbe come `-0,00`: un segno affermato su una grandezza nulla, e per di più proprio nel valore che esiste per rendere verificabile la decisione. L'eccezione vale per questa voce e per nessun'altra, ed è dichiarata nella convenzione `kpi_rounding` dell'artefatto.

**Che cosa la differenza dice.** Che la decisione, su questi dati, non sposta il valore pubblicato: la riga degenere è 1<!--@CL.SP.duration.zero.rows--> su 89.741<!--@CL.SP.track.rows.after-->, e una mediana su quella popolazione non si muove per una riga sola. La decisione resta necessaria — l'operatore la chiedeva, e l'esito non era noto prima di calcolarlo — ma il suo effetto sul numero è nullo alla precisione a cui il numero si pubblica.

### 3.4 L'asimmetria del confronto, dichiarata accanto al valore

Secondo vincolo aperto di §12. Il lato video contribuisce con i **soli film**, il lato musicale con l'intero catalogo: il confronto è asimmetrico per costruzione, e la sua leggibilità dipende dal sapere quanto del catalogo video i film siano.

| | Valore | Ancora |
|---|---|---|
| quota di titoli `Movie` sul catalogo video | 0,6962<!--@KPI.BQ1K2.movie_share_of_video_catalog--> | `KPI.BQ1K2.movie_share_of_video_catalog` |

Il numero è pubblicato senza un giudizio su quanto l'asimmetria sia grave: `kpi_operators.md` chiedeva di dichiararla, non di valutarla, e la valutazione richiederebbe un criterio che nessun documento del progetto ha fissato.

**Stato di verifica contro il motore reale (E9)**: vedi §11 — lo stato è dichiarato in un punto solo perché discende da un unico confronto, congelato in un unico artefatto.

---

## 4. `BQ1-K3` — `mood_profile_overlap`

**Domanda di business**: BQ1 — Posizionamento. Quanta parte del catalogo musicale sia, per profilo emotivo, già compatibile con ciò che il catalogo video occupa — cioè quanto la nuova offerta sia in continuità con il gusto già servito. · **Confidenza**: **media**, invariata da `business_case.md` §5.4 e **non elevabile**: dipende da `dim_category_mood`, costruita dall'analista e non osservata (`data_model.md` §15) · **Operatore**: `kpi_operators.md` §4 (`D1`)

**Formula in prosa**: quota di tracce il cui profilo cade dentro l'intervallo occupato dal catalogo video su **tutti e tre<!--#--> gli assi contemporaneamente** — energia, positività, ritmo — con intervalli **chiusi** e AND logico. Geometricamente, un parallelepipedo allineato agli assi.

### 4.1 Il valore

| | Valore | Ancora |
|---|---|---|
| `mood_profile_overlap` | 0,8450<!--@KPI.BQ1K3.overlap_share--> | `KPI.BQ1K3.overlap_share` |
| tracce dentro l'intervallo su tutti e tre<!--#--> gli assi | 75832<!--@KPI.BQ1K3.tracks_inside--> | `KPI.BQ1K3.tracks_inside` |

Gli intervalli, letti come minimo e massimo sulle 42<!--@CL.NF.category.distinct--> righe della tabella dei mood, senza ponderazione:

| Asse | Minimo | Massimo |
|---|---|---|
| energia (`mood_energy`) | 0,0500<!--@KPI.BQ1K3.bound.mood_energy.min--> | 0,9500<!--@KPI.BQ1K3.bound.mood_energy.max--> |
| positività (`mood_valence`) | 0,0500<!--@KPI.BQ1K3.bound.mood_valence.min--> | 0,9500<!--@KPI.BQ1K3.bound.mood_valence.max--> |
| ritmo (`mood_danceability`) | 0,0500<!--@KPI.BQ1K3.bound.mood_danceability.min--> | 0,9500<!--@KPI.BQ1K3.bound.mood_danceability.max--> |

**Versione della tabella dei mood su cui il valore è calcolato**: la 2<!--@MOOD.table.version-->. È il contratto di versione di [`content_taxonomy_bridge.md`](content_taxonomy_bridge.md) §5: una revisione della tabella **invalida** questo valore, non lo corregge automaticamente.

**Provenienza nel modello dati**: `dim_track` (colonne `energy`, `valence`, `danceability`, lette senza trasformazione), `dim_category_mood` — `data_model.md` §11.

### 4.2 La formula DAX

```dax
mood_profile_overlap =
VAR EnergyMin = MINX ( dim_category_mood, dim_category_mood[mood_energy] )
VAR EnergyMax = MAXX ( dim_category_mood, dim_category_mood[mood_energy] )
VAR ValenceMin = MINX ( dim_category_mood, dim_category_mood[mood_valence] )
VAR ValenceMax = MAXX ( dim_category_mood, dim_category_mood[mood_valence] )
VAR DanceMin = MINX ( dim_category_mood, dim_category_mood[mood_danceability] )
VAR DanceMax = MAXX ( dim_category_mood, dim_category_mood[mood_danceability] )
VAR TracksInside =
    COUNTROWS (
        FILTER (
            dim_track,
            dim_track[energy] >= EnergyMin
                && dim_track[energy] <= EnergyMax
                && dim_track[valence] >= ValenceMin
                && dim_track[valence] <= ValenceMax
                && dim_track[danceability] >= DanceMin
                && dim_track[danceability] <= DanceMax
        )
    )
RETURN
    DIVIDE ( TracksInside, COUNTROWS ( dim_track ) )
```

Gli operatori sono `>=` e `<=` perché gli intervalli sono **chiusi**: minimo e massimo sono valori assegnati a categorie reali, non limiti teorici, e un valore che li tocca sta dentro.

### 4.3 Il limite specifico, che il valore porta con sé

**Questa quota è una stima per eccesso.** Un parallelepipedo contiene sempre l'inviluppo convesso che vi si iscrive, e in genere lo eccede: include combinazioni dei tre<!--#--> assi che nessuna categoria video occupa realmente — un'energia pari a quella della categoria più energica insieme a una positività pari a quella della categoria più cupa, per esempio, anche se nessuna categoria è insieme l'una e l'altra. La sovrapposizione reale è quindi **minore o uguale** a 0,8450<!--@KPI.BQ1K3.overlap_share-->, e quanto minore questo progetto non lo misura.

Non è un difetto dell'implementazione: `data_model.md` §11 non costruisce alcuna struttura congiunta a tre<!--#--> dimensioni, e un inviluppo convesso richiederebbe una regola di aggregazione che nessun documento precedente ha fissato. Il limite è strutturale e dichiarato, non correggibile qui.

**Un secondo limite, più facile da perdere.** Gli estremi valgono 0,0500<!--@KPI.BQ1K3.bound.mood_energy.min--> e 0,9500<!--@KPI.BQ1K3.bound.mood_energy.max--> su **tutti e tre<!--#--> gli assi**: la tabella dei mood è costruita dall'analista su una scala a passi regolari, e i suoi estremi sono quindi una proprietà del criterio di assegnazione prima che del catalogo video. Un intervallo così ampio su ciascun asse rende la quota alta quasi per costruzione, ed è la ragione principale per cui la confidenza di questo KPI resta **media** e non sale.

**Stato di verifica contro il motore reale (E9)**: vedi §11 — lo stato è dichiarato in un punto solo perché discende da un unico confronto, congelato in un unico artefatto.

---

## 5. `BQ2-K1` — `segment_demand_index`

**Domanda di business**: BQ2 — Segmento di ingresso. Quale segmento musicale mostri la domanda più forte, per orientare da dove entrare. · **Confidenza**: **media**, invariata da `business_case.md` §5.4 · **Operatore**: `kpi_operators.md` §5 (`D7`)

**Formula in prosa**: mediana dell'indice di popolarità delle righe del segmento, sulla scala `0-100`. Accanto al valore, **obbligatoriamente**, la quota di righe a popolarità nulla del segmento.

**Grana**: coppia traccia-segmento. La popolarità si legge dalla **tabella di fatto**, mai dalla dimensione delle tracce: è la regola di lettura non negoziabile di `data_model.md` §12. Prendere il valore alla grana traccia porterebbe dentro un segmento un valore osservato su una riga di un altro segmento.

**Provenienza nel modello dati**: `fact_track_segment` (popolarità e `is_popularity_zero`), `dim_segment` (`is_high_zero_genre`) — `data_model.md` §12 e §14.

### 5.1 I valori

Un valore per ciascuno dei 114<!--@SP.genre.count--> segmenti. La tabella completa, insieme ad affinità e punteggio, è in **[§9, Appendice](#9-appendice--i-114-segmenti)**: qui stanno gli estremi e ciò che serve a leggerla.

| | Valore | Ancora |
|---|---|---|
| segmento più domandato — `pop` | 66,0<!--@KPI.BQ2K1.pop.demand_index--> | `KPI.BQ2K1.pop.demand_index` |
| segmenti a `is_high_zero_genre` vero | 7<!--@KPI.BQ2K1.high_zero_segments_count--> | `KPI.BQ2K1.high_zero_segments_count` |

### 5.2 La formula DAX

```dax
segment_demand_index =
MEDIANX ( fact_track_segment, fact_track_segment[popularity] )

segment_zero_share =
DIVIDE (
    CALCULATE (
        COUNTROWS ( fact_track_segment ),
        fact_track_segment[is_popularity_zero] = TRUE ()
    ),
    COUNTROWS ( fact_track_segment )
)
```

Le due<!--#--> misure sono **due<!--#--> misure e non una**, ed è deliberato: `D7` impone che la quota compaia accanto al valore, e una misura unica che le fondesse renderebbe possibile portarne una sola in una visuale.

### 5.3 Il ritrovamento: la quota di zeri non è un'avvertenza teorica

`D7` argomentava che una mediana calcolata su un segmento pieno di zeri è trascinata verso il basso da un difetto della fonte — una traccia priva di segnale di popolarità sulla piattaforma di origine, non priva di domanda reale. **Quanto** la trascinasse nessun documento poteva dirlo prima che le mediane esistessero. Su questi dati la risposta è netta.

| | Valore | Ancora |
|---|---|---|
| segmenti la cui mediana di popolarità è **esattamente nulla** | 7<!--@KPI.BQ2K1.zero_median_segments_count--> | `KPI.BQ2K1.zero_median_segments_count` |
| **l'insieme dei segmenti a mediana nulla coincide esattamente con quello dei segmenti marcati `is_high_zero_genre`** | sì<!--@KPI.BQ2K1.zero_median_matches_high_zero--> | `KPI.BQ2K1.zero_median_matches_high_zero` |
| migliore posizione in graduatoria raggiunta da uno dei 7<!--@KPI.BQ2K1.high_zero_segments_count--> segmenti | 96<!--@KPI.BQ2K3.high_zero_best_rank--> | `KPI.BQ2K3.high_zero_best_rank` |

I 7<!--@KPI.BQ2K1.high_zero_segments_count--> segmenti sono `country`, `iranian`, `jazz`, `latin`, `rock`, `romance`, `soul`. **Tutti e 7<!--@KPI.BQ2K1.zero_median_segments_count--> hanno mediana nulla, e nessuno risale oltre la posizione 96<!--@KPI.BQ2K3.high_zero_best_rank--> su 114<!--@SP.genre.count-->.**

> **Come questo va letto, e come non va letto.** Non dice che `rock` e `jazz` non abbiano domanda. Dice che su questi dati **il loro indice di domanda non è informativo**: più della metà delle righe di ciascuno porta popolarità nulla, la mediana cade dentro quella metà, e il valore che ne esce misura la copertura della fonte invece della domanda. Chi porterà questi segmenti in una dashboard deve presentarli come **non misurati dalla fonte**, non come «a domanda bassa».

Nessuna correzione statistica è stata applicata: ricalcolare la mediana escludendo gli zeri sarebbe una decisione diversa, già scartata dalla trasformazione, che ha scelto di includere le righe a popolarità nulla e di marcarle. Questo documento rende visibile, accanto al valore, il fatto che lo condiziona — che è precisamente ciò che `D7` chiedeva e nulla di più.

**L'avvertimento si pubblica anche dove la mediana fosse alta.** Su questi dati non accade — i 7<!--@KPI.BQ2K1.high_zero_segments_count--> hanno tutti mediana nulla — ma la regola resta quella di `D7` e non dipende dall'esito osservato.

### 5.4 Il limite ereditato sul campione

Il catalogo musicale non è più bilanciato dopo la trasformazione: il segmento meno numeroso porta 904<!--@KPI.BQ2K1.romance.rows--> righe contro le 1000<!--@KPI.BQ2K1.techno.rows--> del più numeroso. Il conteggio delle righe di un segmento misura il **campionamento**, non il mercato, e non va usato per dimensionare un segmento — è la ragione per cui questo KPI poggia sulla domanda e mai sull'offerta (`kpi_operators.md` §5.2).

**Stato di verifica contro il motore reale (E9)**: vedi §11 — lo stato è dichiarato in un punto solo perché discende da un unico confronto, congelato in un unico artefatto.

---

## 6. `BQ2-K2` — `segment_catalog_affinity`

**Domanda di business**: BQ2 — Segmento di ingresso. Quanto il profilo emotivo di un segmento musicale sia vicino a quello del catalogo video già servito — cioè quanto entrare in quel segmento sia una continuazione e non una rottura. · **Confidenza**: **media**, invariata da `business_case.md` §5.4 e **non elevabile** (`data_model.md` §15) · **Operatore**: `kpi_operators.md` §6 (`D2`)

**Formula in prosa**: `1 − d`, dove `d` è la media delle tre<!--#--> distanze assolute per asse fra il profilo mediano del segmento e il profilo mediano del catalogo video.

### 6.1 Il valore

Un valore per ciascuno dei 114<!--@SP.genre.count--> segmenti — tabella completa in **[§9](#9-appendice--i-114-segmenti)**. Il profilo del catalogo video, termine di paragone comune a tutti:

| Asse | Profilo mediano del catalogo video | Ancora |
|---|---|---|
| energia | 0,5000<!--@KPI.BQ2K2.video_profile.mood_energy--> | `KPI.BQ2K2.video_profile.mood_energy` |
| positività | 0,5000<!--@KPI.BQ2K2.video_profile.mood_valence--> | `KPI.BQ2K2.video_profile.mood_valence` |
| ritmo | 0,4000<!--@KPI.BQ2K2.video_profile.mood_danceability--> | `KPI.BQ2K2.video_profile.mood_danceability` |

| | Valore | Ancora |
|---|---|---|
| affinità più alta — `british` | 0,9277<!--@KPI.BQ2K2.british.affinity--> | `KPI.BQ2K2.british.affinity` |
| affinità più bassa — `sleep` | 0,6408<!--@KPI.BQ2K2.sleep.affinity--> | `KPI.BQ2K2.sleep.affinity` |

**Il profilo video è ponderato sulle assegnazioni, non sulle categorie**: mediana di ciascun asse sulle 19.323<!--@CL.NF.category.assignments--> righe del ponte, ciascuna portando il profilo della propria categoria. È la regola di `data_model.md` §11, e la sua ragione è la simmetria del confronto — sul lato musicale il profilo del segmento è una mediana sulle coppie, e l'assegnazione titolo-categoria è l'esatto omologo video della coppia.

**Versione della tabella dei mood**: la 2<!--@MOOD.table.version-->, con lo stesso contratto di versione di §4.1.

**Provenienza nel modello dati**: `fact_track_segment`, `dim_track`, `dim_segment` sul lato musicale; `bridge_title_category`, `dim_category`, `dim_category_mood` sul lato video — `data_model.md` §8 e §11.

### 6.2 La formula DAX

```dax
segment_catalog_affinity =
VAR VideoEnergy =
    MEDIANX ( bridge_title_category, RELATED ( dim_category_mood[mood_energy] ) )
VAR VideoValence =
    MEDIANX ( bridge_title_category, RELATED ( dim_category_mood[mood_valence] ) )
VAR VideoDance =
    MEDIANX ( bridge_title_category, RELATED ( dim_category_mood[mood_danceability] ) )
VAR SegmentEnergy = MEDIANX ( fact_track_segment, RELATED ( dim_track[energy] ) )
VAR SegmentValence = MEDIANX ( fact_track_segment, RELATED ( dim_track[valence] ) )
VAR SegmentDance = MEDIANX ( fact_track_segment, RELATED ( dim_track[danceability] ) )
VAR Distance =
    (
        ABS ( SegmentEnergy - VideoEnergy )
            + ABS ( SegmentValence - VideoValence )
            + ABS ( SegmentDance - VideoDance )
    ) / 3
RETURN
    1 - Distance
```

Le tre<!--#--> variabili del lato video **non** portano un `ALL` sul lato musicale, e l'omissione è deliberata: `data_model.md` §4 dichiara che i due<!--#--> lati del modello non si toccano: nessuna relazione propaga il filtro di segmento al ponte titolo-categoria, quindi il profilo video resta invariante per costruzione del modello e non per una precauzione scritta nella misura. Se una feature a valle collegasse i due<!--#--> lati, questa misura andrebbe rivista — ed è una ragione in più perché quel collegamento non venga introdotto senza dichiararlo.

### 6.3 Il limite specifico, che è severo

**La grandezza assoluta di questo numero non ha un'interpretazione indipendente dal criterio di mood.** Sottrarre un profilo *assegnato* (lato video, costruito dall'analista) da uno *osservato* (lato musicale, letto dalla fonte) presuppone che uno stesso numero indichi la stessa posizione sull'asse su entrambe le scale — e `content_taxonomy_bridge.md` §7 dichiara che questo è sostenuto **solo agli estremi**, mai al centro.

Ciò che il valore garantisce è di essere **confrontabile con sé stesso fra segmenti diversi**: che `british` sia più affine di `sleep` è un'affermazione difendibile. Che `british` sia affine al `93`<!--#--> per cento non lo è, e non va scritta.

**Un secondo limite, che la formula sceglie deliberatamente.** La media delle distanze assolute è un operatore **compensativo**: uno scostamento piccolo su un asse bilancia uno grande su un altro. `D2` lo dichiara e non lo nasconde dietro l'argomento — falso — che l'euclidea sarebbe compensativa e questa no. L'unica alternativa davvero non compensativa sarebbe il massimo degli scostamenti per asse, scartata perché produrrebbe un'affinità governata dal solo asse peggiore.

**Stato di verifica contro il motore reale (E9)**: vedi §11 — lo stato è dichiarato in un punto solo perché discende da un unico confronto, congelato in un unico artefatto.

---

## 7. `BQ2-K3` — `segment_entry_priority`

**Domanda di business**: BQ2 — Segmento di ingresso. Da quale segmento conviene entrare, componendo domanda e affinità in un'unica priorità. · **Confidenza**: **media**, ereditata dai due<!--#--> KPI che compone, entrambi a media · **Operatore**: `kpi_operators.md` §7 (`D3`, `D4`, `D8`)

**Questo KPI non legge alcuna tabella**: compone i due<!--#--> precedenti, e ne eredita per intero provenienza e limiti — incluso il vincolo di versione su `dim_category_mood`, la 2<!--@MOOD.table.version-->.

**Pubblica due<!--#--> valori distinti per segmento**, con ruoli non intercambiabili: l'appartenenza al quadrante (booleana) e il punteggio pesato con la sua posizione in graduatoria (continui).

### 7.1 Le soglie e il quadrante

| | Valore | Ancora |
|---|---|---|
| soglia di domanda — mediana dei 114<!--@SP.genre.count--> segmenti | 36,5<!--@KPI.BQ2K3.threshold.demand--> | `KPI.BQ2K3.threshold.demand` |
| soglia di affinità — mediana dei 114<!--@SP.genre.count--> segmenti | 0,8210<!--@KPI.BQ2K3.threshold.affinity--> | `KPI.BQ2K3.threshold.affinity` |
| **segmenti nel quadrante alta domanda / alta affinità** | 33<!--@KPI.BQ2K3.quadrant_members_count--> | `KPI.BQ2K3.quadrant_members_count` |
| **`C3` è soddisfatta** | sì<!--@KPI.BQ2K3.c3_satisfied--> | `KPI.BQ2K3.c3_satisfied` |

Entrambe le soglie sono **strette**: un segmento esattamente sulla mediana non entra nel quadrante. Entrambe sono calcolate sui valori **esatti**, non su quelli arrotondati per la pubblicazione — arrotondare prima farebbe cadere dal lato sbagliato i segmenti vicini alla soglia.

`C3` chiede che «esista almeno un segmento musicale che si colloca contemporaneamente nella metà superiore per domanda e nella metà superiore per affinità» (`business_case.md` §3). Il quadrante lo risponde per sì o per no, ed è soddisfatta.

### 7.2 La graduatoria

Ordinata per punteggio **decrescente**: la prima posizione è quella del punteggio più alto (`D8`). Tabella completa in **[§9](#9-appendice--i-114-segmenti)**; le prime cinque<!--#--> posizioni:

| # | Segmento | Domanda | Affinità | Punteggio | Quadrante |
|---|---|---|---|---|---|
| 1<!--@KPI.BQ2K3.pop.rank--> | `pop` | 66,0<!--@KPI.BQ2K1.pop.demand_index--> | 0,8793<!--@KPI.BQ2K2.pop.affinity--> | 0,7697<!--@KPI.BQ2K3.pop.score--> | sì<!--@KPI.BQ2K3.pop.quadrant_high_high--> |
| 2<!--@KPI.BQ2K3.pop_film.rank--> | `pop-film` | 60,0<!--@KPI.BQ2K1.pop_film.demand_index--> | 0,8820<!--@KPI.BQ2K2.pop_film.affinity--> | 0,7410<!--@KPI.BQ2K3.pop_film.score--> | sì<!--@KPI.BQ2K3.pop_film.quadrant_high_high--> |
| 3<!--@KPI.BQ2K3.british.rank--> | `british` | 52,0<!--@KPI.BQ2K1.british.demand_index--> | 0,9277<!--@KPI.BQ2K2.british.affinity--> | 0,7238<!--@KPI.BQ2K3.british.score--> | sì<!--@KPI.BQ2K3.british.quadrant_high_high--> |
| 4<!--@KPI.BQ2K3.psych_rock.rank--> | `psych-rock` | 51,0<!--@KPI.BQ2K1.psych_rock.demand_index--> | 0,9230<!--@KPI.BQ2K2.psych_rock.affinity--> | 0,7165<!--@KPI.BQ2K3.psych_rock.score--> | sì<!--@KPI.BQ2K3.psych_rock.quadrant_high_high--> |
| 5<!--@KPI.BQ2K3.k_pop.rank--> | `k-pop` | 60,0<!--@KPI.BQ2K1.k_pop.demand_index--> | 0,8243<!--@KPI.BQ2K2.k_pop.affinity--> | 0,7122<!--@KPI.BQ2K3.k_pop.score--> | sì<!--@KPI.BQ2K3.k_pop.quadrant_high_high--> |

**Perché quadrante e punteggio non si fondono, con l'esempio che questi dati forniscono.** `metal` occupa la posizione 9<!--@KPI.BQ2K3.metal.rank--> con punteggio 0,6915<!--@KPI.BQ2K3.metal.score-->, più alto di quello di 105<!--#--> altri segmenti, e **non** sta nel quadrante: la sua affinità vale 0,8130<!--@KPI.BQ2K2.metal.affinity-->, sotto la soglia di 0,8210<!--@KPI.BQ2K3.threshold.affinity-->. Leggere «punteggio alto» come sinonimo di «nel quadrante» lo classificherebbe male, ed è esattamente la distinzione che `D4` chiedeva di preservare — qui con un caso reale invece che ipotetico.

**Sui pari merito**: due<!--#--> segmenti con lo stesso punteggio ricevono la **stessa** posizione, e la successiva salta di altrettante unità. È la scelta che non introduce un criterio di spareggio che nessuna decisione della `007a` ha fissato: spareggiare per nome produrrebbe un ordine riproducibile ma arbitrario, presentato con l'autorevolezza di un risultato.

### 7.3 La formula DAX

```dax
segment_entry_priority_score =
0.5 * DIVIDE ( [segment_demand_index], 100 ) + 0.5 * [segment_catalog_affinity]

segment_entry_priority_quadrant =
VAR DemandThreshold = MEDIANX ( ALL ( dim_segment ), [segment_demand_index] )
VAR AffinityThreshold = MEDIANX ( ALL ( dim_segment ), [segment_catalog_affinity] )
RETURN
    IF (
        [segment_demand_index] > DemandThreshold
            && [segment_catalog_affinity] > AffinityThreshold,
        TRUE (),
        FALSE ()
    )

segment_entry_priority_rank =
RANKX ( ALL ( dim_segment ), [segment_entry_priority_score],, DESC, Skip )
```

La domanda si porta sul dominio `0-1` dividendo per il proprio **massimo teorico**, `100`, e non riscalandola sui valori osservati fra i segmenti (`D3`): è un indice delimitato per definizione, e riscalarlo sugli osservati renderebbe il punteggio di ogni segmento dipendente dal segmento più domandato del gruppo. `Skip` è il parametro che realizza la regola dei pari merito di §7.2.

### 7.4 Il limite che i 7<!--@KPI.BQ2K1.high_zero_segments_count--> segmenti introducono nella graduatoria

La domanda entra nel punteggio con peso 0,5<!--#-->, e per i 7<!--@KPI.BQ2K1.zero_median_segments_count--> segmenti a mediana nulla quel contributo è **nullo**. La loro posizione in graduatoria — nessuna sopra la 96<!--@KPI.BQ2K3.high_zero_best_rank--> — non misura quindi una priorità bassa: misura l'assenza di segnale della fonte su metà del punteggio. **Questi 7<!--@KPI.BQ2K1.high_zero_segments_count--> segmenti vanno esclusi da qualunque lettura della coda della graduatoria**, o la coda si legge come una classifica di preferenza quando è in parte una classifica di copertura del dato.

**Stato di verifica contro il motore reale (E9)**: vedi §11 — lo stato è dichiarato in un punto solo perché discende da un unico confronto, congelato in un unico artefatto.

---

## 8. `BQ3-K1` e `BQ3-K2` — citati, non ricalcolati

**Domanda di business**: BQ3 — Impatto stimato. Quanto ricavo aggiuntivo la mossa possa produrre, sotto assunzioni dichiarate. · **Confidenza**: **bassa**, invariata da `business_case.md` §5.4 e **non elevabile** · **Operatore**: nessuno nuovo — la derivazione è chiusa per intero in [`bq3_scenarios.md`](bq3_scenarios.md)

**Questa feature non calcola nulla per questi due<!--#--> KPI, e l'assenza è dichiarata invece che lasciata dedurre.** I valori esistono già, ancorati in [`reports/bq3_scenarios.json`](../reports/bq3_scenarios.json) dalla feature `004`. Ricalcolarli qui produrrebbe una seconda copia della stessa fonte, capace di divergere dall'originale senza che nulla lo segnali — la stessa ragione per cui `dim_category_mood.json` non viene mai ricopiato altrove. `reports/kpi_measures.json` non contiene alcuna voce `BQ3`; lo script si limita a verificare che le voci qui citate esistano davvero nell'artefatto della `004`.

**Nessuna formula DAX è trascritta** per questi due<!--#-->: non c'è una misura da scrivere nel modello, ci sono sei<!--#--> valori di scenario congelati in un artefatto.

| | Pessimista | Centrale | Ottimista |
|---|---|---|---|
| `premium_tier_adoption_rate` (`BQ3-K1`) | 15<!--@BQ3.adoption.worst--> | 30<!--@BQ3.adoption.base--> | 60<!--@BQ3.adoption.best--> |
| `arpu_uplift` (`BQ3-K2`) | 0,60<!--@BQ3.uplift.worst--> | 1,20<!--@BQ3.uplift.base--> | 2,40<!--@BQ3.uplift.best--> |

Unità: punti percentuali della base per `BQ3-K1`, euro per utente al mese per `BQ3-K2`. Ampiezza della banda: 45<!--@BQ3.band.spread_pp--> punti percentuali, con un rapporto di 4<!--@BQ3.band.ratio--> fra scenario ottimista e pessimista.

**Che cosa resta vincolante, e va ripetuto ogni volta che questi numeri compaiono:**

- **si presentano sempre come intervallo, mai come valore singolo.** La confidenza è bassa perché il valore dipende interamente dalle assunzioni di scenario;
- il tasso di `BQ3-K1` è **lordo**: le disdette sono fuori dal perimetro del progetto;
- l'uplift di `BQ3-K2` **non è scalabile**. Nessuna base utenti è quantificata in questo progetto, e moltiplicarlo per una dimensione di base produrrebbe un totale che nessuno ha misurato, presentato con l'autorevolezza di uno misurato;
- l'uplift è **a regime**, non cumulato sull'orizzonte.

**Stato di verifica contro il motore reale (E9)**: vedi §11 — lo stato è dichiarato in un punto solo perché discende da un unico confronto, congelato in un unico artefatto.

---

## 9. Appendice — i 114<!--@SP.genre.count--> segmenti

Le tre<!--#--> misure per segmento in una tabella sola, ordinata per posizione in graduatoria. `Domanda` è `BQ2-K1`, `Affinità` è `BQ2-K2`, `Punteggio` e `Quadrante` sono `BQ2-K3`; `Quota di zeri` accompagna obbligatoriamente la domanda per `D7`.

**Che le tre<!--#--> misure stiano in una tabella unica invece che in tre<!--#--> è una scelta di questo documento**, e va dichiarata: `BQ2-K3` compone le altre due<!--#-->, e vederle affiancate è ciò che rende leggibile perché un segmento occupi quella posizione. Non cambia nulla nell'artefatto, dove le tre<!--#--> misure restano voci distinte con chiavi distinte.

I 7<!--@KPI.BQ2K1.high_zero_segments_count--> segmenti marcati `is_high_zero_genre` portano l'avvertimento testuale esplicito accanto al proprio nome, come `D7` impone.

| # | Segmento | Domanda | Quota di zeri | Affinità | Punteggio | Quadrante |
|---|---|---|---|---|---|---|
| 1<!--@KPI.BQ2K3.pop.rank--> | `pop` | 66,0<!--@KPI.BQ2K1.pop.demand_index--> | 0,1793<!--@KPI.BQ2K1.pop.zero_share--> | 0,8793<!--@KPI.BQ2K2.pop.affinity--> | 0,7697<!--@KPI.BQ2K3.pop.score--> | sì<!--@KPI.BQ2K3.pop.quadrant_high_high--> |
| 2<!--@KPI.BQ2K3.pop_film.rank--> | `pop-film` | 60,0<!--@KPI.BQ2K1.pop_film.demand_index--> | 0,0020<!--@KPI.BQ2K1.pop_film.zero_share--> | 0,8820<!--@KPI.BQ2K2.pop_film.affinity--> | 0,7410<!--@KPI.BQ2K3.pop_film.score--> | sì<!--@KPI.BQ2K3.pop_film.quadrant_high_high--> |
| 3<!--@KPI.BQ2K3.british.rank--> | `british` | 52,0<!--@KPI.BQ2K1.british.demand_index--> | 0,1260<!--@KPI.BQ2K1.british.zero_share--> | 0,9277<!--@KPI.BQ2K2.british.affinity--> | 0,7238<!--@KPI.BQ2K3.british.score--> | sì<!--@KPI.BQ2K3.british.quadrant_high_high--> |
| 4<!--@KPI.BQ2K3.psych_rock.rank--> | `psych-rock` | 51,0<!--@KPI.BQ2K1.psych_rock.demand_index--> | 0,1205<!--@KPI.BQ2K1.psych_rock.zero_share--> | 0,9230<!--@KPI.BQ2K2.psych_rock.affinity--> | 0,7165<!--@KPI.BQ2K3.psych_rock.score--> | sì<!--@KPI.BQ2K3.psych_rock.quadrant_high_high--> |
| 5<!--@KPI.BQ2K3.k_pop.rank--> | `k-pop` | 60,0<!--@KPI.BQ2K1.k_pop.demand_index--> | 0,0390<!--@KPI.BQ2K1.k_pop.zero_share--> | 0,8243<!--@KPI.BQ2K2.k_pop.affinity--> | 0,7122<!--@KPI.BQ2K3.k_pop.score--> | sì<!--@KPI.BQ2K3.k_pop.quadrant_high_high--> |
| 6<!--@KPI.BQ2K3.chill.rank--> | `chill` | 57,0<!--@KPI.BQ2K1.chill.demand_index--> | 0,0390<!--@KPI.BQ2K1.chill.zero_share--> | 0,8373<!--@KPI.BQ2K2.chill.affinity--> | 0,7037<!--@KPI.BQ2K3.chill.score--> | sì<!--@KPI.BQ2K3.chill.quadrant_high_high--> |
| 7<!--@KPI.BQ2K3.sad.rank--> | `sad` | 54,0<!--@KPI.BQ2K1.sad.demand_index--> | 0,0140<!--@KPI.BQ2K1.sad.zero_share--> | 0,8570<!--@KPI.BQ2K2.sad.affinity--> | 0,6985<!--@KPI.BQ2K3.sad.score--> | sì<!--@KPI.BQ2K3.sad.quadrant_high_high--> |
| 8<!--@KPI.BQ2K3.indian.rank--> | `indian` | 49,0<!--@KPI.BQ2K1.indian.demand_index--> | 0,0120<!--@KPI.BQ2K1.indian.zero_share--> | 0,8933<!--@KPI.BQ2K2.indian.affinity--> | 0,6917<!--@KPI.BQ2K3.indian.score--> | sì<!--@KPI.BQ2K3.indian.quadrant_high_high--> |
| 9<!--@KPI.BQ2K3.metal.rank--> | `metal` | 57,0<!--@KPI.BQ2K1.metal.demand_index--> | 0,2054<!--@KPI.BQ2K1.metal.zero_share--> | 0,8130<!--@KPI.BQ2K2.metal.affinity--> | 0,6915<!--@KPI.BQ2K3.metal.score--> | no<!--@KPI.BQ2K3.metal.quadrant_high_high--> |
| 10<!--@KPI.BQ2K3.hip_hop.rank--> | `hip-hop` | 58,0<!--@KPI.BQ2K1.hip_hop.demand_index--> | 0,2856<!--@KPI.BQ2K1.hip_hop.zero_share--> | 0,8023<!--@KPI.BQ2K2.hip_hop.affinity--> | 0,6912<!--@KPI.BQ2K3.hip_hop.score--> | no<!--@KPI.BQ2K3.hip_hop.quadrant_high_high--> |
| 11<!--@KPI.BQ2K3.indie.rank--> | `indie` | 47,0<!--@KPI.BQ2K1.indie.demand_index--> | 0,2859<!--@KPI.BQ2K1.indie.zero_share--> | 0,9080<!--@KPI.BQ2K2.indie.affinity--> | 0,6890<!--@KPI.BQ2K3.indie.score--> | sì<!--@KPI.BQ2K3.indie.quadrant_high_high--> |
| 12<!--@KPI.BQ2K3.mandopop.rank--> | `mandopop` | 49,0<!--@KPI.BQ2K1.mandopop.demand_index--> | 0,0110<!--@KPI.BQ2K1.mandopop.zero_share--> | 0,8878<!--@KPI.BQ2K2.mandopop.affinity--> | 0,6889<!--@KPI.BQ2K3.mandopop.score--> | sì<!--@KPI.BQ2K3.mandopop.quadrant_high_high--> |
| 13<!--@KPI.BQ2K3.grunge.rank--> | `grunge` | 55,0<!--@KPI.BQ2K1.grunge.demand_index--> | 0,0380<!--@KPI.BQ2K1.grunge.zero_share--> | 0,8200<!--@KPI.BQ2K2.grunge.affinity--> | 0,6850<!--@KPI.BQ2K3.grunge.score--> | no<!--@KPI.BQ2K3.grunge.quadrant_high_high--> |
| 14<!--@KPI.BQ2K3.emo.rank--> | `emo` | 51,0<!--@KPI.BQ2K1.emo.demand_index--> | 0,0480<!--@KPI.BQ2K1.emo.zero_share--> | 0,8567<!--@KPI.BQ2K2.emo.affinity--> | 0,6833<!--@KPI.BQ2K3.emo.score--> | sì<!--@KPI.BQ2K3.emo.quadrant_high_high--> |
| 15<!--@KPI.BQ2K3.indie_pop.rank--> | `indie-pop` | 47,0<!--@KPI.BQ2K1.indie_pop.demand_index--> | 0,2590<!--@KPI.BQ2K1.indie_pop.zero_share--> | 0,8907<!--@KPI.BQ2K2.indie_pop.affinity--> | 0,6803<!--@KPI.BQ2K3.indie_pop.score--> | sì<!--@KPI.BQ2K3.indie_pop.quadrant_high_high--> |
| 16<!--@KPI.BQ2K3.electro.rank--> | `electro` | 50,5<!--@KPI.BQ2K1.electro.demand_index--> | 0,3768<!--@KPI.BQ2K1.electro.zero_share--> | 0,8400<!--@KPI.BQ2K2.electro.affinity--> | 0,6725<!--@KPI.BQ2K3.electro.score--> | sì<!--@KPI.BQ2K3.electro.quadrant_high_high--> |
| 17<!--@KPI.BQ2K3.anime.rank--> | `anime` | 50,0<!--@KPI.BQ2K1.anime.demand_index--> | 0,0080<!--@KPI.BQ2K1.anime.zero_share--> | 0,8413<!--@KPI.BQ2K2.anime.affinity--> | 0,6707<!--@KPI.BQ2K3.anime.score--> | sì<!--@KPI.BQ2K3.anime.quadrant_high_high--> |
| 18<!--@KPI.BQ2K3.acoustic.rank--> | `acoustic` | 47,0<!--@KPI.BQ2K1.acoustic.demand_index--> | 0,0560<!--@KPI.BQ2K1.acoustic.zero_share--> | 0,8700<!--@KPI.BQ2K2.acoustic.affinity--> | 0,6700<!--@KPI.BQ2K3.acoustic.score--> | sì<!--@KPI.BQ2K3.acoustic.quadrant_high_high--> |
| 19<!--@KPI.BQ2K3.brazil.rank--> | `brazil` | 45,0<!--@KPI.BQ2K1.brazil.demand_index--> | 0,0341<!--@KPI.BQ2K1.brazil.zero_share--> | 0,8818<!--@KPI.BQ2K2.brazil.affinity--> | 0,6659<!--@KPI.BQ2K3.brazil.score--> | sì<!--@KPI.BQ2K3.brazil.quadrant_high_high--> |
| 20<!--@KPI.BQ2K3.folk.rank--> | `folk` | 41,0<!--@KPI.BQ2K1.folk.demand_index--> | 0,2092<!--@KPI.BQ2K1.folk.zero_share--> | 0,9210<!--@KPI.BQ2K2.folk.affinity--> | 0,6655<!--@KPI.BQ2K3.folk.score--> | sì<!--@KPI.BQ2K3.folk.quadrant_high_high--> |
| 21<!--@KPI.BQ2K3.world_music.rank--> | `world-music` | 44,0<!--@KPI.BQ2K1.world_music.demand_index--> | 0,0120<!--@KPI.BQ2K1.world_music.zero_share--> | 0,8783<!--@KPI.BQ2K2.world_music.affinity--> | 0,6592<!--@KPI.BQ2K3.world_music.score--> | sì<!--@KPI.BQ2K3.world_music.quadrant_high_high--> |
| 22<!--@KPI.BQ2K3.singer_songwriter.rank--> | `singer-songwriter` | 43,0<!--@KPI.BQ2K1.singer_songwriter.demand_index--> | 0,2460<!--@KPI.BQ2K1.singer_songwriter.zero_share--> | 0,8843<!--@KPI.BQ2K2.singer_songwriter.affinity--> | 0,6572<!--@KPI.BQ2K3.singer_songwriter.score--> | sì<!--@KPI.BQ2K3.singer_songwriter.quadrant_high_high--> |
| 22<!--@KPI.BQ2K3.songwriter.rank--> | `songwriter` | 43,0<!--@KPI.BQ2K1.songwriter.demand_index--> | 0,2460<!--@KPI.BQ2K1.songwriter.zero_share--> | 0,8843<!--@KPI.BQ2K2.songwriter.affinity--> | 0,6572<!--@KPI.BQ2K3.songwriter.score--> | sì<!--@KPI.BQ2K3.songwriter.quadrant_high_high--> |
| 24<!--@KPI.BQ2K3.mpb.rank--> | `mpb` | 42,0<!--@KPI.BQ2K1.mpb.demand_index--> | 0,0400<!--@KPI.BQ2K1.mpb.zero_share--> | 0,8913<!--@KPI.BQ2K2.mpb.affinity--> | 0,6557<!--@KPI.BQ2K3.mpb.score--> | sì<!--@KPI.BQ2K3.mpb.quadrant_high_high--> |
| 25<!--@KPI.BQ2K3.piano.rank--> | `piano` | 50,0<!--@KPI.BQ2K1.piano.demand_index--> | 0,0982<!--@KPI.BQ2K1.piano.zero_share--> | 0,7985<!--@KPI.BQ2K2.piano.affinity--> | 0,6493<!--@KPI.BQ2K3.piano.score--> | no<!--@KPI.BQ2K3.piano.quadrant_high_high--> |
| 26<!--@KPI.BQ2K3.deep_house.rank--> | `deep-house` | 51,0<!--@KPI.BQ2K1.deep_house.demand_index--> | 0,0852<!--@KPI.BQ2K1.deep_house.zero_share--> | 0,7870<!--@KPI.BQ2K2.deep_house.affinity--> | 0,6485<!--@KPI.BQ2K3.deep_house.score--> | no<!--@KPI.BQ2K3.deep_house.quadrant_high_high--> |
| 27<!--@KPI.BQ2K3.alt_rock.rank--> | `alt-rock` | 45,0<!--@KPI.BQ2K1.alt_rock.demand_index--> | 0,3493<!--@KPI.BQ2K1.alt_rock.zero_share--> | 0,8440<!--@KPI.BQ2K2.alt_rock.affinity--> | 0,6470<!--@KPI.BQ2K3.alt_rock.score--> | sì<!--@KPI.BQ2K3.alt_rock.quadrant_high_high--> |
| 28<!--@KPI.BQ2K3.sertanejo.rank--> | `sertanejo` | 47,0<!--@KPI.BQ2K1.sertanejo.demand_index--> | 0,0010<!--@KPI.BQ2K1.sertanejo.zero_share--> | 0,8182<!--@KPI.BQ2K2.sertanejo.affinity--> | 0,6441<!--@KPI.BQ2K3.sertanejo.score--> | no<!--@KPI.BQ2K3.sertanejo.quadrant_high_high--> |
| 29<!--@KPI.BQ2K3.gospel.rank--> | `gospel` | 41,0<!--@KPI.BQ2K1.gospel.demand_index--> | 0,0070<!--@KPI.BQ2K1.gospel.zero_share--> | 0,8750<!--@KPI.BQ2K2.gospel.affinity--> | 0,6425<!--@KPI.BQ2K3.gospel.score--> | sì<!--@KPI.BQ2K3.gospel.quadrant_high_high--> |
| 30<!--@KPI.BQ2K3.progressive_house.rank--> | `progressive-house` | 52,0<!--@KPI.BQ2K1.progressive_house.demand_index--> | 0,1021<!--@KPI.BQ2K1.progressive_house.zero_share--> | 0,7627<!--@KPI.BQ2K2.progressive_house.affinity--> | 0,6413<!--@KPI.BQ2K3.progressive_house.score--> | no<!--@KPI.BQ2K3.progressive_house.quadrant_high_high--> |
| 31<!--@KPI.BQ2K3.edm.rank--> | `edm` | 47,0<!--@KPI.BQ2K1.edm.demand_index--> | 0,3615<!--@KPI.BQ2K1.edm.zero_share--> | 0,8113<!--@KPI.BQ2K2.edm.affinity--> | 0,6407<!--@KPI.BQ2K3.edm.score--> | no<!--@KPI.BQ2K3.edm.quadrant_high_high--> |
| 32<!--@KPI.BQ2K3.electronic.rank--> | `electronic` | 48,0<!--@KPI.BQ2K1.electronic.demand_index--> | 0,0580<!--@KPI.BQ2K1.electronic.zero_share--> | 0,7933<!--@KPI.BQ2K2.electronic.affinity--> | 0,6367<!--@KPI.BQ2K3.electronic.score--> | no<!--@KPI.BQ2K3.electronic.quadrant_high_high--> |
| 33<!--@KPI.BQ2K3.metalcore.rank--> | `metalcore` | 50,0<!--@KPI.BQ2K1.metalcore.demand_index--> | 0,0410<!--@KPI.BQ2K1.metalcore.zero_share--> | 0,7700<!--@KPI.BQ2K2.metalcore.affinity--> | 0,6350<!--@KPI.BQ2K3.metalcore.score--> | no<!--@KPI.BQ2K3.metalcore.quadrant_high_high--> |
| 34<!--@KPI.BQ2K3.j_pop.rank--> | `j-pop` | 41,0<!--@KPI.BQ2K1.j_pop.demand_index--> | 0,1413<!--@KPI.BQ2K1.j_pop.zero_share--> | 0,8578<!--@KPI.BQ2K2.j_pop.affinity--> | 0,6339<!--@KPI.BQ2K3.j_pop.score--> | sì<!--@KPI.BQ2K3.j_pop.quadrant_high_high--> |
| 35<!--@KPI.BQ2K3.hard_rock.rank--> | `hard-rock` | 41,0<!--@KPI.BQ2K1.hard_rock.demand_index--> | 0,1403<!--@KPI.BQ2K1.hard_rock.zero_share--> | 0,8555<!--@KPI.BQ2K2.hard_rock.affinity--> | 0,6328<!--@KPI.BQ2K3.hard_rock.score--> | sì<!--@KPI.BQ2K3.hard_rock.quadrant_high_high--> |
| 36<!--@KPI.BQ2K3.turkish.rank--> | `turkish` | 40,0<!--@KPI.BQ2K1.turkish.demand_index--> | 0,0220<!--@KPI.BQ2K1.turkish.zero_share--> | 0,8653<!--@KPI.BQ2K2.turkish.affinity--> | 0,6327<!--@KPI.BQ2K3.turkish.score--> | sì<!--@KPI.BQ2K3.turkish.quadrant_high_high--> |
| 37<!--@KPI.BQ2K3.trip_hop.rank--> | `trip-hop` | 39,0<!--@KPI.BQ2K1.trip_hop.demand_index--> | 0,0331<!--@KPI.BQ2K1.trip_hop.zero_share--> | 0,8673<!--@KPI.BQ2K2.trip_hop.affinity--> | 0,6287<!--@KPI.BQ2K3.trip_hop.score--> | sì<!--@KPI.BQ2K3.trip_hop.quadrant_high_high--> |
| 38<!--@KPI.BQ2K3.dub.rank--> | `dub` | 44,0<!--@KPI.BQ2K1.dub.demand_index--> | 0,0601<!--@KPI.BQ2K1.dub.zero_share--> | 0,8163<!--@KPI.BQ2K2.dub.affinity--> | 0,6282<!--@KPI.BQ2K3.dub.score--> | no<!--@KPI.BQ2K3.dub.quadrant_high_high--> |
| 39<!--@KPI.BQ2K3.ambient.rank--> | `ambient` | 50,0<!--@KPI.BQ2K1.ambient.demand_index--> | 0,0681<!--@KPI.BQ2K1.ambient.zero_share--> | 0,7557<!--@KPI.BQ2K2.ambient.affinity--> | 0,6278<!--@KPI.BQ2K3.ambient.score--> | no<!--@KPI.BQ2K3.ambient.quadrant_high_high--> |
| 40<!--@KPI.BQ2K3.swedish.rank--> | `swedish` | 38,0<!--@KPI.BQ2K1.swedish.demand_index--> | 0,1510<!--@KPI.BQ2K1.swedish.zero_share--> | 0,8703<!--@KPI.BQ2K2.swedish.affinity--> | 0,6252<!--@KPI.BQ2K3.swedish.score--> | sì<!--@KPI.BQ2K3.swedish.quadrant_high_high--> |
| 41<!--@KPI.BQ2K3.pagode.rank--> | `pagode` | 45,0<!--@KPI.BQ2K1.pagode.demand_index--> | 0,0250<!--@KPI.BQ2K1.pagode.zero_share--> | 0,7962<!--@KPI.BQ2K2.pagode.affinity--> | 0,6231<!--@KPI.BQ2K3.pagode.score--> | no<!--@KPI.BQ2K3.pagode.quadrant_high_high--> |
| 41<!--@KPI.BQ2K3.r_n_b.rank--> | `r-n-b` | 42,0<!--@KPI.BQ2K1.r_n_b.demand_index--> | 0,1920<!--@KPI.BQ2K1.r_n_b.zero_share--> | 0,8262<!--@KPI.BQ2K2.r_n_b.affinity--> | 0,6231<!--@KPI.BQ2K3.r_n_b.score--> | sì<!--@KPI.BQ2K3.r_n_b.quadrant_high_high--> |
| 43<!--@KPI.BQ2K3.funk.rank--> | `funk` | 43,0<!--@KPI.BQ2K1.funk.demand_index--> | 0,2940<!--@KPI.BQ2K1.funk.zero_share--> | 0,8152<!--@KPI.BQ2K2.funk.affinity--> | 0,6226<!--@KPI.BQ2K3.funk.score--> | no<!--@KPI.BQ2K3.funk.quadrant_high_high--> |
| 44<!--@KPI.BQ2K3.german.rank--> | `german` | 37,0<!--@KPI.BQ2K1.german.demand_index--> | 0,3333<!--@KPI.BQ2K1.german.zero_share--> | 0,8643<!--@KPI.BQ2K2.german.affinity--> | 0,6172<!--@KPI.BQ2K3.german.score--> | sì<!--@KPI.BQ2K3.german.quadrant_high_high--> |
| 44<!--@KPI.BQ2K3.house.rank--> | `house` | 42,0<!--@KPI.BQ2K1.house.demand_index--> | 0,4034<!--@KPI.BQ2K1.house.zero_share--> | 0,8143<!--@KPI.BQ2K2.house.affinity--> | 0,6172<!--@KPI.BQ2K3.house.score--> | no<!--@KPI.BQ2K3.house.quadrant_high_high--> |
| 46<!--@KPI.BQ2K3.cantopop.rank--> | `cantopop` | 35,0<!--@KPI.BQ2K1.cantopop.demand_index--> | 0,0150<!--@KPI.BQ2K1.cantopop.zero_share--> | 0,8827<!--@KPI.BQ2K2.cantopop.affinity--> | 0,6163<!--@KPI.BQ2K3.cantopop.score--> | no<!--@KPI.BQ2K3.cantopop.quadrant_high_high--> |
| 47<!--@KPI.BQ2K3.dubstep.rank--> | `dubstep` | 44,0<!--@KPI.BQ2K1.dubstep.demand_index--> | 0,0480<!--@KPI.BQ2K1.dubstep.zero_share--> | 0,7840<!--@KPI.BQ2K2.dubstep.affinity--> | 0,6120<!--@KPI.BQ2K3.dubstep.score--> | no<!--@KPI.BQ2K3.dubstep.quadrant_high_high--> |
| 48<!--@KPI.BQ2K3.punk.rank--> | `punk` | 40,0<!--@KPI.BQ2K1.punk.demand_index--> | 0,1471<!--@KPI.BQ2K1.punk.zero_share--> | 0,8230<!--@KPI.BQ2K2.punk.affinity--> | 0,6115<!--@KPI.BQ2K3.punk.score--> | sì<!--@KPI.BQ2K3.punk.quadrant_high_high--> |
| 49<!--@KPI.BQ2K3.garage.rank--> | `garage` | 35,0<!--@KPI.BQ2K1.garage.demand_index--> | 0,0410<!--@KPI.BQ2K1.garage.zero_share--> | 0,8632<!--@KPI.BQ2K2.garage.affinity--> | 0,6066<!--@KPI.BQ2K3.garage.score--> | no<!--@KPI.BQ2K3.garage.quadrant_high_high--> |
| 50<!--@KPI.BQ2K3.french.rank--> | `french` | 37,0<!--@KPI.BQ2K1.french.demand_index--> | 0,0801<!--@KPI.BQ2K1.french.zero_share--> | 0,8393<!--@KPI.BQ2K2.french.affinity--> | 0,6047<!--@KPI.BQ2K3.french.score--> | sì<!--@KPI.BQ2K3.french.quadrant_high_high--> |
| 51<!--@KPI.BQ2K3.j_rock.rank--> | `j-rock` | 37,0<!--@KPI.BQ2K1.j_rock.demand_index--> | 0,0290<!--@KPI.BQ2K1.j_rock.zero_share--> | 0,8385<!--@KPI.BQ2K2.j_rock.affinity--> | 0,6043<!--@KPI.BQ2K3.j_rock.score--> | sì<!--@KPI.BQ2K3.j_rock.quadrant_high_high--> |
| 52<!--@KPI.BQ2K3.blues.rank--> | `blues` | 34,0<!--@KPI.BQ2K1.blues.demand_index--> | 0,3457<!--@KPI.BQ2K1.blues.zero_share--> | 0,8658<!--@KPI.BQ2K2.blues.affinity--> | 0,6029<!--@KPI.BQ2K3.blues.score--> | no<!--@KPI.BQ2K3.blues.quadrant_high_high--> |
| 53<!--@KPI.BQ2K3.rock_n_roll.rank--> | `rock-n-roll` | 32,0<!--@KPI.BQ2K1.rock_n_roll.demand_index--> | 0,1080<!--@KPI.BQ2K1.rock_n_roll.zero_share--> | 0,8847<!--@KPI.BQ2K2.rock_n_roll.affinity--> | 0,6023<!--@KPI.BQ2K3.rock_n_roll.score--> | no<!--@KPI.BQ2K3.rock_n_roll.quadrant_high_high--> |
| 54<!--@KPI.BQ2K3.punk_rock.rank--> | `punk-rock` | 38,0<!--@KPI.BQ2K1.punk_rock.demand_index--> | 0,1020<!--@KPI.BQ2K1.punk_rock.zero_share--> | 0,8180<!--@KPI.BQ2K2.punk_rock.affinity--> | 0,5990<!--@KPI.BQ2K3.punk_rock.score--> | no<!--@KPI.BQ2K3.punk_rock.quadrant_high_high--> |
| 55<!--@KPI.BQ2K3.groove.rank--> | `groove` | 39,5<!--@KPI.BQ2K1.groove.demand_index--> | 0,0922<!--@KPI.BQ2K1.groove.zero_share--> | 0,7925<!--@KPI.BQ2K2.groove.affinity--> | 0,5938<!--@KPI.BQ2K3.groove.score--> | no<!--@KPI.BQ2K3.groove.quadrant_high_high--> |
| 56<!--@KPI.BQ2K3.samba.rank--> | `samba` | 39,0<!--@KPI.BQ2K1.samba.demand_index--> | 0,0190<!--@KPI.BQ2K1.samba.zero_share--> | 0,7972<!--@KPI.BQ2K2.samba.affinity--> | 0,5936<!--@KPI.BQ2K3.samba.score--> | no<!--@KPI.BQ2K3.samba.quadrant_high_high--> |
| 57<!--@KPI.BQ2K3.malay.rank--> | `malay` | 28,0<!--@KPI.BQ2K1.malay.demand_index--> | 0,0040<!--@KPI.BQ2K1.malay.zero_share--> | 0,8963<!--@KPI.BQ2K2.malay.affinity--> | 0,5882<!--@KPI.BQ2K3.malay.score--> | no<!--@KPI.BQ2K3.malay.quadrant_high_high--> |
| 58<!--@KPI.BQ2K3.techno.rank--> | `techno` | 43,0<!--@KPI.BQ2K1.techno.demand_index--> | 0,0720<!--@KPI.BQ2K1.techno.zero_share--> | 0,7282<!--@KPI.BQ2K2.techno.affinity--> | 0,5791<!--@KPI.BQ2K3.techno.score--> | no<!--@KPI.BQ2K3.techno.quadrant_high_high--> |
| 59<!--@KPI.BQ2K3.spanish.rank--> | `spanish` | 32,0<!--@KPI.BQ2K1.spanish.demand_index--> | 0,1070<!--@KPI.BQ2K1.spanish.zero_share--> | 0,8338<!--@KPI.BQ2K2.spanish.affinity--> | 0,5769<!--@KPI.BQ2K3.spanish.score--> | no<!--@KPI.BQ2K3.spanish.quadrant_high_high--> |
| 60<!--@KPI.BQ2K3.children.rank--> | `children` | 36,0<!--@KPI.BQ2K1.children.demand_index--> | 0,1092<!--@KPI.BQ2K1.children.zero_share--> | 0,7927<!--@KPI.BQ2K2.children.affinity--> | 0,5763<!--@KPI.BQ2K3.children.score--> | no<!--@KPI.BQ2K3.children.quadrant_high_high--> |
| 61<!--@KPI.BQ2K3.club.rank--> | `club` | 37,0<!--@KPI.BQ2K1.club.demand_index--> | 0,0010<!--@KPI.BQ2K1.club.zero_share--> | 0,7817<!--@KPI.BQ2K2.club.affinity--> | 0,5758<!--@KPI.BQ2K3.club.score--> | no<!--@KPI.BQ2K3.club.quadrant_high_high--> |
| 62<!--@KPI.BQ2K3.hardcore.rank--> | `hardcore` | 32,0<!--@KPI.BQ2K1.hardcore.demand_index--> | 0,1001<!--@KPI.BQ2K1.hardcore.zero_share--> | 0,8243<!--@KPI.BQ2K2.hardcore.affinity--> | 0,5722<!--@KPI.BQ2K3.hardcore.score--> | no<!--@KPI.BQ2K3.hardcore.quadrant_high_high--> |
| 63<!--@KPI.BQ2K3.synth_pop.rank--> | `synth-pop` | 34,0<!--@KPI.BQ2K1.synth_pop.demand_index--> | 0,0940<!--@KPI.BQ2K1.synth_pop.zero_share--> | 0,8042<!--@KPI.BQ2K2.synth_pop.affinity--> | 0,5721<!--@KPI.BQ2K3.synth_pop.score--> | no<!--@KPI.BQ2K3.synth_pop.quadrant_high_high--> |
| 64<!--@KPI.BQ2K3.show_tunes.rank--> | `show-tunes` | 25,0<!--@KPI.BQ2K1.show_tunes.demand_index--> | 0,0400<!--@KPI.BQ2K1.show_tunes.zero_share--> | 0,8870<!--@KPI.BQ2K2.show_tunes.affinity--> | 0,5685<!--@KPI.BQ2K3.show_tunes.score--> | no<!--@KPI.BQ2K3.show_tunes.quadrant_high_high--> |
| 65<!--@KPI.BQ2K3.minimal_techno.rank--> | `minimal-techno` | 39,0<!--@KPI.BQ2K1.minimal_techno.demand_index--> | 0,0541<!--@KPI.BQ2K1.minimal_techno.zero_share--> | 0,7335<!--@KPI.BQ2K2.minimal_techno.affinity--> | 0,5618<!--@KPI.BQ2K3.minimal_techno.score--> | no<!--@KPI.BQ2K3.minimal_techno.quadrant_high_high--> |
| 66<!--@KPI.BQ2K3.bluegrass.rank--> | `bluegrass` | 24,0<!--@KPI.BQ2K1.bluegrass.demand_index--> | 0,0100<!--@KPI.BQ2K1.bluegrass.zero_share--> | 0,8830<!--@KPI.BQ2K2.bluegrass.affinity--> | 0,5615<!--@KPI.BQ2K3.bluegrass.score--> | no<!--@KPI.BQ2K3.bluegrass.quadrant_high_high--> |
| 67<!--@KPI.BQ2K3.forro.rank--> | `forro` | 41,0<!--@KPI.BQ2K1.forro.demand_index--> | 0,0000<!--@KPI.BQ2K1.forro.zero_share--> | 0,7122<!--@KPI.BQ2K2.forro.affinity--> | 0,5611<!--@KPI.BQ2K3.forro.score--> | no<!--@KPI.BQ2K3.forro.quadrant_high_high--> |
| 68<!--@KPI.BQ2K3.trance.rank--> | `trance` | 40,0<!--@KPI.BQ2K1.trance.demand_index--> | 0,0691<!--@KPI.BQ2K1.trance.zero_share--> | 0,7193<!--@KPI.BQ2K2.trance.affinity--> | 0,5597<!--@KPI.BQ2K3.trance.score--> | no<!--@KPI.BQ2K3.trance.quadrant_high_high--> |
| 69<!--@KPI.BQ2K3.study.rank--> | `study` | 28,0<!--@KPI.BQ2K1.study.demand_index--> | 0,0130<!--@KPI.BQ2K1.study.zero_share--> | 0,8292<!--@KPI.BQ2K2.study.affinity--> | 0,5546<!--@KPI.BQ2K3.study.score--> | no<!--@KPI.BQ2K3.study.quadrant_high_high--> |
| 70<!--@KPI.BQ2K3.ska.rank--> | `ska` | 36,0<!--@KPI.BQ2K1.ska.demand_index--> | 0,0460<!--@KPI.BQ2K1.ska.zero_share--> | 0,7457<!--@KPI.BQ2K2.ska.affinity--> | 0,5528<!--@KPI.BQ2K3.ska.score--> | no<!--@KPI.BQ2K3.ska.quadrant_high_high--> |
| 71<!--@KPI.BQ2K3.guitar.rank--> | `guitar` | 26,0<!--@KPI.BQ2K1.guitar.demand_index--> | 0,0210<!--@KPI.BQ2K1.guitar.zero_share--> | 0,8343<!--@KPI.BQ2K2.guitar.affinity--> | 0,5472<!--@KPI.BQ2K3.guitar.score--> | no<!--@KPI.BQ2K3.guitar.quadrant_high_high--> |
| 72<!--@KPI.BQ2K3.goth.rank--> | `goth` | 24,0<!--@KPI.BQ2K1.goth.demand_index--> | 0,0170<!--@KPI.BQ2K1.goth.zero_share--> | 0,8493<!--@KPI.BQ2K2.goth.affinity--> | 0,5447<!--@KPI.BQ2K3.goth.score--> | no<!--@KPI.BQ2K3.goth.quadrant_high_high--> |
| 73<!--@KPI.BQ2K3.dancehall.rank--> | `dancehall` | 31,0<!--@KPI.BQ2K1.dancehall.demand_index--> | 0,1481<!--@KPI.BQ2K1.dancehall.zero_share--> | 0,7760<!--@KPI.BQ2K2.dancehall.affinity--> | 0,5430<!--@KPI.BQ2K3.dancehall.score--> | no<!--@KPI.BQ2K3.dancehall.quadrant_high_high--> |
| 74<!--@KPI.BQ2K3.comedy.rank--> | `comedy` | 23,0<!--@KPI.BQ2K1.comedy.demand_index--> | 0,0000<!--@KPI.BQ2K1.comedy.zero_share--> | 0,8558<!--@KPI.BQ2K2.comedy.affinity--> | 0,5429<!--@KPI.BQ2K3.comedy.score--> | no<!--@KPI.BQ2K3.comedy.quadrant_high_high--> |
| 75<!--@KPI.BQ2K3.tango.rank--> | `tango` | 19,0<!--@KPI.BQ2K1.tango.demand_index--> | 0,0140<!--@KPI.BQ2K1.tango.zero_share--> | 0,8797<!--@KPI.BQ2K2.tango.affinity--> | 0,5348<!--@KPI.BQ2K3.tango.score--> | no<!--@KPI.BQ2K3.tango.quadrant_high_high--> |
| 76<!--@KPI.BQ2K3.disney.rank--> | `disney` | 23,0<!--@KPI.BQ2K1.disney.demand_index--> | 0,0050<!--@KPI.BQ2K1.disney.zero_share--> | 0,8380<!--@KPI.BQ2K2.disney.affinity--> | 0,5340<!--@KPI.BQ2K3.disney.score--> | no<!--@KPI.BQ2K3.disney.quadrant_high_high--> |
| 77<!--@KPI.BQ2K3.rockabilly.rank--> | `rockabilly` | 28,0<!--@KPI.BQ2K1.rockabilly.demand_index--> | 0,1431<!--@KPI.BQ2K1.rockabilly.zero_share--> | 0,7750<!--@KPI.BQ2K2.rockabilly.affinity--> | 0,5275<!--@KPI.BQ2K3.rockabilly.score--> | no<!--@KPI.BQ2K3.rockabilly.quadrant_high_high--> |
| 78<!--@KPI.BQ2K3.disco.rank--> | `disco` | 32,0<!--@KPI.BQ2K1.disco.demand_index--> | 0,2260<!--@KPI.BQ2K1.disco.zero_share--> | 0,7305<!--@KPI.BQ2K2.disco.affinity--> | 0,5253<!--@KPI.BQ2K3.disco.score--> | no<!--@KPI.BQ2K3.disco.quadrant_high_high--> |
| 79<!--@KPI.BQ2K3.power_pop.rank--> | `power-pop` | 23,0<!--@KPI.BQ2K1.power_pop.demand_index--> | 0,0562<!--@KPI.BQ2K1.power_pop.zero_share--> | 0,8095<!--@KPI.BQ2K2.power_pop.affinity--> | 0,5198<!--@KPI.BQ2K3.power_pop.score--> | no<!--@KPI.BQ2K3.power_pop.quadrant_high_high--> |
| 80<!--@KPI.BQ2K3.heavy_metal.rank--> | `heavy-metal` | 23,0<!--@KPI.BQ2K1.heavy_metal.demand_index--> | 0,0020<!--@KPI.BQ2K1.heavy_metal.zero_share--> | 0,8022<!--@KPI.BQ2K2.heavy_metal.affinity--> | 0,5161<!--@KPI.BQ2K3.heavy_metal.score--> | no<!--@KPI.BQ2K3.heavy_metal.quadrant_high_high--> |
| 81<!--@KPI.BQ2K3.j_dance.rank--> | `j-dance` | 22,0<!--@KPI.BQ2K1.j_dance.demand_index--> | 0,0272<!--@KPI.BQ2K1.j_dance.zero_share--> | 0,8103<!--@KPI.BQ2K2.j_dance.affinity--> | 0,5152<!--@KPI.BQ2K3.j_dance.score--> | no<!--@KPI.BQ2K3.j_dance.quadrant_high_high--> |
| 82<!--@KPI.BQ2K3.industrial.rank--> | `industrial` | 24,0<!--@KPI.BQ2K1.industrial.demand_index--> | 0,0700<!--@KPI.BQ2K1.industrial.zero_share--> | 0,7853<!--@KPI.BQ2K2.industrial.affinity--> | 0,5127<!--@KPI.BQ2K3.industrial.score--> | no<!--@KPI.BQ2K3.industrial.quadrant_high_high--> |
| 83<!--@KPI.BQ2K3.j_idol.rank--> | `j-idol` | 22,0<!--@KPI.BQ2K1.j_idol.demand_index--> | 0,0020<!--@KPI.BQ2K1.j_idol.zero_share--> | 0,7820<!--@KPI.BQ2K2.j_idol.affinity--> | 0,5010<!--@KPI.BQ2K3.j_idol.score--> | no<!--@KPI.BQ2K3.j_idol.quadrant_high_high--> |
| 84<!--@KPI.BQ2K3.opera.rank--> | `opera` | 22,0<!--@KPI.BQ2K1.opera.demand_index--> | 0,1109<!--@KPI.BQ2K1.opera.zero_share--> | 0,7783<!--@KPI.BQ2K2.opera.affinity--> | 0,4992<!--@KPI.BQ2K3.opera.score--> | no<!--@KPI.BQ2K3.opera.quadrant_high_high--> |
| 85<!--@KPI.BQ2K3.death_metal.rank--> | `death-metal` | 25,0<!--@KPI.BQ2K1.death_metal.demand_index--> | 0,0240<!--@KPI.BQ2K1.death_metal.zero_share--> | 0,7427<!--@KPI.BQ2K2.death_metal.affinity--> | 0,4963<!--@KPI.BQ2K3.death_metal.score--> | no<!--@KPI.BQ2K3.death_metal.quadrant_high_high--> |
| 86<!--@KPI.BQ2K3.salsa.rank--> | `salsa` | 29,0<!--@KPI.BQ2K1.salsa.demand_index--> | 0,0962<!--@KPI.BQ2K1.salsa.zero_share--> | 0,7025<!--@KPI.BQ2K2.salsa.affinity--> | 0,4963<!--@KPI.BQ2K3.salsa.score--> | no<!--@KPI.BQ2K3.salsa.quadrant_high_high--> |
| 87<!--@KPI.BQ2K3.sleep.rank--> | `sleep` | 35,0<!--@KPI.BQ2K1.sleep.demand_index--> | 0,1860<!--@KPI.BQ2K1.sleep.zero_share--> | 0,6408<!--@KPI.BQ2K2.sleep.affinity--> | 0,4954<!--@KPI.BQ2K3.sleep.score--> | no<!--@KPI.BQ2K3.sleep.quadrant_high_high--> |
| 88<!--@KPI.BQ2K3.new_age.rank--> | `new-age` | 24,0<!--@KPI.BQ2K1.new_age.demand_index--> | 0,0332<!--@KPI.BQ2K1.new_age.zero_share--> | 0,7375<!--@KPI.BQ2K2.new_age.affinity--> | 0,4888<!--@KPI.BQ2K3.new_age.score--> | no<!--@KPI.BQ2K3.new_age.quadrant_high_high--> |
| 89<!--@KPI.BQ2K3.honky_tonk.rank--> | `honky-tonk` | 13,0<!--@KPI.BQ2K1.honky_tonk.demand_index--> | 0,0000<!--@KPI.BQ2K1.honky_tonk.zero_share--> | 0,8420<!--@KPI.BQ2K2.honky_tonk.affinity--> | 0,4860<!--@KPI.BQ2K3.honky_tonk.score--> | no<!--@KPI.BQ2K3.honky_tonk.quadrant_high_high--> |
| 90<!--@KPI.BQ2K3.hardstyle.rank--> | `hardstyle` | 23,0<!--@KPI.BQ2K1.hardstyle.demand_index--> | 0,0721<!--@KPI.BQ2K1.hardstyle.zero_share--> | 0,7363<!--@KPI.BQ2K2.hardstyle.affinity--> | 0,4832<!--@KPI.BQ2K3.hardstyle.score--> | no<!--@KPI.BQ2K3.hardstyle.quadrant_high_high--> |
| 91<!--@KPI.BQ2K3.afrobeat.rank--> | `afrobeat` | 21,0<!--@KPI.BQ2K1.afrobeat.demand_index--> | 0,0150<!--@KPI.BQ2K1.afrobeat.zero_share--> | 0,7507<!--@KPI.BQ2K2.afrobeat.affinity--> | 0,4803<!--@KPI.BQ2K3.afrobeat.score--> | no<!--@KPI.BQ2K3.afrobeat.quadrant_high_high--> |
| 92<!--@KPI.BQ2K3.party.rank--> | `party` | 25,0<!--@KPI.BQ2K1.party.demand_index--> | 0,2626<!--@KPI.BQ2K1.party.zero_share--> | 0,7053<!--@KPI.BQ2K2.party.affinity--> | 0,4777<!--@KPI.BQ2K3.party.score--> | no<!--@KPI.BQ2K3.party.quadrant_high_high--> |
| 93<!--@KPI.BQ2K3.idm.rank--> | `idm` | 12,0<!--@KPI.BQ2K1.idm.demand_index--> | 0,0140<!--@KPI.BQ2K1.idm.zero_share--> | 0,8330<!--@KPI.BQ2K2.idm.affinity--> | 0,4765<!--@KPI.BQ2K3.idm.score--> | no<!--@KPI.BQ2K3.idm.quadrant_high_high--> |
| 94<!--@KPI.BQ2K3.drum_and_bass.rank--> | `drum-and-bass` | 19,0<!--@KPI.BQ2K1.drum_and_bass.demand_index--> | 0,0030<!--@KPI.BQ2K1.drum_and_bass.zero_share--> | 0,7493<!--@KPI.BQ2K2.drum_and_bass.affinity--> | 0,4697<!--@KPI.BQ2K3.drum_and_bass.score--> | no<!--@KPI.BQ2K3.drum_and_bass.quadrant_high_high--> |
| 95<!--@KPI.BQ2K3.happy.rank--> | `happy` | 19,0<!--@KPI.BQ2K1.happy.demand_index--> | 0,0430<!--@KPI.BQ2K1.happy.zero_share--> | 0,7283<!--@KPI.BQ2K2.happy.affinity--> | 0,4592<!--@KPI.BQ2K3.happy.score--> | no<!--@KPI.BQ2K3.happy.quadrant_high_high--> |
| 96<!--@KPI.BQ2K3.soul.rank--> | `soul` — **alta concentrazione di zeri: la mediana è trascinata da un difetto della fonte, non da una domanda debole** | 0,0<!--@KPI.BQ2K1.soul.demand_index--> | 0,6106<!--@KPI.BQ2K1.soul.zero_share--> | 0,9180<!--@KPI.BQ2K2.soul.affinity--> | 0,4590<!--@KPI.BQ2K3.soul.score--> | no<!--@KPI.BQ2K3.soul.quadrant_high_high--> |
| 97<!--@KPI.BQ2K3.breakbeat.rank--> | `breakbeat` | 14,0<!--@KPI.BQ2K1.breakbeat.demand_index--> | 0,0030<!--@KPI.BQ2K1.breakbeat.zero_share--> | 0,7750<!--@KPI.BQ2K2.breakbeat.affinity--> | 0,4575<!--@KPI.BQ2K3.breakbeat.score--> | no<!--@KPI.BQ2K3.breakbeat.quadrant_high_high--> |
| 98<!--@KPI.BQ2K3.jazz.rank--> | `jazz` — **alta concentrazione di zeri: la mediana è trascinata da un difetto della fonte, non da una domanda debole** | 0,0<!--@KPI.BQ2K1.jazz.demand_index--> | 0,6817<!--@KPI.BQ2K1.jazz.zero_share--> | 0,9097<!--@KPI.BQ2K2.jazz.affinity--> | 0,4548<!--@KPI.BQ2K3.jazz.score--> | no<!--@KPI.BQ2K3.jazz.quadrant_high_high--> |
| 99<!--@KPI.BQ2K3.country.rank--> | `country` — **alta concentrazione di zeri: la mediana è trascinata da un difetto della fonte, non da una domanda debole** | 0,0<!--@KPI.BQ2K1.country.demand_index--> | 0,5870<!--@KPI.BQ2K1.country.zero_share--> | 0,9057<!--@KPI.BQ2K2.country.affinity--> | 0,4528<!--@KPI.BQ2K3.country.score--> | no<!--@KPI.BQ2K3.country.quadrant_high_high--> |
| 100<!--@KPI.BQ2K3.black_metal.rank--> | `black-metal` | 19,0<!--@KPI.BQ2K1.black_metal.demand_index--> | 0,0030<!--@KPI.BQ2K1.black_metal.zero_share--> | 0,6990<!--@KPI.BQ2K2.black_metal.affinity--> | 0,4445<!--@KPI.BQ2K3.black_metal.score--> | no<!--@KPI.BQ2K3.black_metal.quadrant_high_high--> |
| 101<!--@KPI.BQ2K3.detroit_techno.rank--> | `detroit-techno` | 8,0<!--@KPI.BQ2K1.detroit_techno.demand_index--> | 0,0010<!--@KPI.BQ2K1.detroit_techno.zero_share--> | 0,7952<!--@KPI.BQ2K2.detroit_techno.affinity--> | 0,4376<!--@KPI.BQ2K3.detroit_techno.score--> | no<!--@KPI.BQ2K3.detroit_techno.quadrant_high_high--> |
| 102<!--@KPI.BQ2K3.kids.rank--> | `kids` | 12,0<!--@KPI.BQ2K1.kids.demand_index--> | 0,0283<!--@KPI.BQ2K1.kids.zero_share--> | 0,7527<!--@KPI.BQ2K2.kids.affinity--> | 0,4363<!--@KPI.BQ2K3.kids.score--> | no<!--@KPI.BQ2K3.kids.quadrant_high_high--> |
| 103<!--@KPI.BQ2K3.romance.rank--> | `romance` — **alta concentrazione di zeri: la mediana è trascinata da un difetto della fonte, non da una domanda debole** | 0,0<!--@KPI.BQ2K1.romance.demand_index--> | 0,6139<!--@KPI.BQ2K1.romance.zero_share--> | 0,8702<!--@KPI.BQ2K2.romance.affinity--> | 0,4351<!--@KPI.BQ2K3.romance.score--> | no<!--@KPI.BQ2K3.romance.quadrant_high_high--> |
| 104<!--@KPI.BQ2K3.alternative.rank--> | `alternative` | 1,0<!--@KPI.BQ2K1.alternative.demand_index--> | 0,4845<!--@KPI.BQ2K1.alternative.zero_share--> | 0,8597<!--@KPI.BQ2K2.alternative.affinity--> | 0,4348<!--@KPI.BQ2K3.alternative.score--> | no<!--@KPI.BQ2K3.alternative.quadrant_high_high--> |
| 105<!--@KPI.BQ2K3.rock.rank--> | `rock` — **alta concentrazione di zeri: la mediana è trascinata da un difetto della fonte, non da una domanda debole** | 0,0<!--@KPI.BQ2K1.rock.demand_index--> | 0,5250<!--@KPI.BQ2K1.rock.zero_share--> | 0,8663<!--@KPI.BQ2K2.rock.affinity--> | 0,4332<!--@KPI.BQ2K3.rock.score--> | no<!--@KPI.BQ2K3.rock.quadrant_high_high--> |
| 106<!--@KPI.BQ2K3.chicago_house.rank--> | `chicago-house` | 10,0<!--@KPI.BQ2K1.chicago_house.demand_index--> | 0,0040<!--@KPI.BQ2K1.chicago_house.zero_share--> | 0,7567<!--@KPI.BQ2K2.chicago_house.affinity--> | 0,4283<!--@KPI.BQ2K3.chicago_house.score--> | no<!--@KPI.BQ2K3.chicago_house.quadrant_high_high--> |
| 107<!--@KPI.BQ2K3.classical.rank--> | `classical` | 3,0<!--@KPI.BQ2K1.classical.demand_index--> | 0,4094<!--@KPI.BQ2K1.classical.zero_share--> | 0,8220<!--@KPI.BQ2K2.classical.affinity--> | 0,4260<!--@KPI.BQ2K3.classical.score--> | no<!--@KPI.BQ2K3.classical.quadrant_high_high--> |
| 108<!--@KPI.BQ2K3.grindcore.rank--> | `grindcore` | 14,0<!--@KPI.BQ2K1.grindcore.demand_index--> | 0,0030<!--@KPI.BQ2K1.grindcore.zero_share--> | 0,6918<!--@KPI.BQ2K2.grindcore.affinity--> | 0,4159<!--@KPI.BQ2K3.grindcore.score--> | no<!--@KPI.BQ2K3.grindcore.quadrant_high_high--> |
| 109<!--@KPI.BQ2K3.dance.rank--> | `dance` | 1,0<!--@KPI.BQ2K1.dance.demand_index--> | 0,4798<!--@KPI.BQ2K1.dance.zero_share--> | 0,8073<!--@KPI.BQ2K2.dance.affinity--> | 0,4087<!--@KPI.BQ2K3.dance.score--> | no<!--@KPI.BQ2K3.dance.quadrant_high_high--> |
| 110<!--@KPI.BQ2K3.iranian.rank--> | `iranian` — **alta concentrazione di zeri: la mediana è trascinata da un difetto della fonte, non da una domanda debole** | 0,0<!--@KPI.BQ2K1.iranian.demand_index--> | 0,6559<!--@KPI.BQ2K1.iranian.zero_share--> | 0,8099<!--@KPI.BQ2K2.iranian.affinity--> | 0,4049<!--@KPI.BQ2K3.iranian.score--> | no<!--@KPI.BQ2K3.iranian.quadrant_high_high--> |
| 111<!--@KPI.BQ2K3.latino.rank--> | `latino` | 2,0<!--@KPI.BQ2K1.latino.demand_index--> | 0,3615<!--@KPI.BQ2K1.latino.zero_share--> | 0,7517<!--@KPI.BQ2K2.latino.affinity--> | 0,3858<!--@KPI.BQ2K3.latino.score--> | no<!--@KPI.BQ2K3.latino.quadrant_high_high--> |
| 112<!--@KPI.BQ2K3.reggae.rank--> | `reggae` | 2,0<!--@KPI.BQ2K1.reggae.demand_index--> | 0,3920<!--@KPI.BQ2K1.reggae.zero_share--> | 0,7430<!--@KPI.BQ2K2.reggae.affinity--> | 0,3815<!--@KPI.BQ2K3.reggae.score--> | no<!--@KPI.BQ2K3.reggae.quadrant_high_high--> |
| 113<!--@KPI.BQ2K3.reggaeton.rank--> | `reggaeton` | 2,0<!--@KPI.BQ2K1.reggaeton.demand_index--> | 0,3620<!--@KPI.BQ2K1.reggaeton.zero_share--> | 0,7417<!--@KPI.BQ2K2.reggaeton.affinity--> | 0,3808<!--@KPI.BQ2K3.reggaeton.score--> | no<!--@KPI.BQ2K3.reggaeton.quadrant_high_high--> |
| 114<!--@KPI.BQ2K3.latin.rank--> | `latin` — **alta concentrazione di zeri: la mediana è trascinata da un difetto della fonte, non da una domanda debole** | 0,0<!--@KPI.BQ2K1.latin.demand_index--> | 0,5909<!--@KPI.BQ2K1.latin.zero_share--> | 0,7525<!--@KPI.BQ2K2.latin.affinity--> | 0,3763<!--@KPI.BQ2K3.latin.score--> | no<!--@KPI.BQ2K3.latin.quadrant_high_high--> |

---

## 10. Limiti dichiarati

**Non risponde a**: se StreamWave debba entrare nel mercato musicale. I KPI misurano il posizionamento del catalogo, la domanda dei segmenti e un impatto stimato sotto assunzioni; la decisione è di chi legge.

**I cataloghi non sono di StreamWave.** Sono due<!--#--> cataloghi pubblici usati come proxy, e ogni valore di questa pagina descrive **loro**. È il limite più grande del progetto, ereditato dal business case, e nessuna cura nel calcolo lo riduce.

**Nessun dato comportamentale.** Non esiste in questo progetto alcuna osservazione di che cosa un utente guardi o ascolti: la «domanda» di `BQ2-K1` è un indice di popolarità pubblicato dalla fonte, di cui la fonte non dichiara il metodo di costruzione.

**Tre<!--#--> KPI su otto<!--#--> poggiano su una tabella costruita dall'analista.** `BQ1-K3`, `BQ2-K2` e, attraverso quest'ultimo, `BQ2-K3` leggono `dim_category_mood`, che è un'assegnazione e non un'osservazione. La confidenza **media** non è negoziabile (`data_model.md` §15) e non sale per nessuna cura nell'operatore: la cura riduce l'arbitrarietà della formula, non la natura del dato.

**I segmenti il cui indice di domanda non è informativo** sono 7<!--@KPI.BQ2K1.high_zero_segments_count-->, per la concentrazione di righe a popolarità nulla — §5.3 e §7.4. È il limite più concreto per chi userà `BQ2-K1` e `BQ2-K3` a schermo.

**La sovrapposizione di `BQ1-K3` è una stima per eccesso** — §4.3 — e la grandezza assoluta dell'affinità di `BQ2-K2` non ha interpretazione indipendente dal criterio di mood — §6.3.

**Ogni valore che dipende da `dim_category_mood` è calcolato sulla versione 2<!--@MOOD.table.version--> della tabella.** Una revisione della tabella **invalida** quei valori invece di correggerli automaticamente: è il contratto di versione di `content_taxonomy_bridge.md` §5.

**Nessuno di questi limiti è esposto a chi legge la dashboard**, da questa pagina. È un documento tecnico. Portarli a schermo in forma comprensibile è compito di chi costruirà la narrazione (`008b`), che li eredita da qui.

---

## 11. Stato di verifica contro il motore reale

Ogni valore di questa pagina è **calcolato da `scripts/build_kpi_measures.py`**. Che il motore DAX di Power BI Desktop, applicando le formule trascritte qui, restituisca lo stesso numero non è assunto: è verificato incollando le otto<!--#--> misure nel modello già materializzato e leggendo i valori restituiti.

L'esito di quel confronto è congelato in [`reports/kpi_engine_check.json`](../reports/kpi_engine_check.json) — **curato a mano e mai scritto da alcuno script**, perché è un'osservazione umana e non una derivazione: nessuno script di questo repository può aprire Power BI Desktop, incollare una formula o leggere il valore che restituisce, ed è esattamente il confine che il principio V traccia. È da quell'artefatto, e non da un numero scritto a mano in questa prosa, che ogni valore del confronto riceve la propria ancora.

**Stato al momento della stesura**: nessuna delle otto<!--#--> misure è ancora dichiarata «verificata contro il motore reale». Lo stato di default di ciascuna è **calcolato da `scripts/build_kpi_measures.py`, verifica contro il motore in corso**, e nessuna sezione lo anticipa: dichiarare «verificato» prima che il confronto sia avvenuto sarebbe una dichiarazione falsa su un fatto che nessun controllo automatico può presidiare.

---

## 12. Come si verifica

```bash
# rigenera l'artefatto dai dati, e verifica che due esecuzioni coincidano
python3 scripts/build_datasets.py
python3 scripts/build_kpi_measures.py

# ogni cifra ancorata di questa pagina contro gli artefatti versionati
python3 scripts/check_audit_coherence.py
```

Il controllo scandisce questa pagina in **severità stretta**: ogni quantità priva di ancora o di marcatore di non-misurato è un errore, non un avviso.

**Che cosa l'esito verde certifica, e che cosa no.** Certifica che ogni numero ancorato coincida con il valore dell'artefatto che lo produce, e che ogni ancora si risolva. Non può accorgersi di un'affermazione che *avrebbe dovuto* essere ancorata, né impedire che un fatto misurato venga dichiarato non-misurato. Soprattutto, non verifica che la formula sia quella giusta: un operatore sbagliato applicato coerentemente produce un artefatto verde e un numero falso. Contro questo esistono la revisione in contesto pulito e il confronto di §11, non il controllo.
