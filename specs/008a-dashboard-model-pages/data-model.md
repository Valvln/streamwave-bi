# Data model: il modello nel `.pbix` e le entità di questa feature

**Feature**: 008a-dashboard-model-pages | **Data**: 2026-08-24

Due parti che non vanno confuse. La prima descrive **ciò che deve esistere dentro Power BI** — sette tabelle, cinque relazioni, dieci misure — e non è un modello nuovo: è la trascrizione operativa di [`docs/data_model.md`](../../docs/data_model.md), che resta la fonte autorevole. La seconda descrive le **entità documentali** che questa feature introduce, che vivono in `specs/` e non nel modello.

Nessuna delle due parti introduce una tabella, una colonna, una relazione o una misura che un documento precedente non abbia già fissato.

---

## Parte 1 — Il modello nel `.pbix`

### 1.1 Le sette tabelle

| Tabella | Gruppo | Chiave | Origine | Righe attese |
|---|---|---|---|---|
| `dim_title` | video | `show_id` | `data/processed/netflix_titles.csv` | 8.807 |
| `bridge_title_category` | video | `show_id` + `category` | `data/processed/netflix_title_category.csv` | 19.323 |
| `dim_category` | video | `category` | derivata dal ponte | 42 |
| `dim_category_mood` | video | `category` | `data/curated/dim_category_mood.json`, **versione 2** | 42 |
| `dim_track` | musicale | `track_id` | `data/processed/spotify_tracks.csv` | 89.741 |
| `dim_segment` | musicale | `segment` | derivata dal fatto | 114 |
| `fact_track_segment` | musicale | `track_id` + `track_genre` | `data/processed/spotify_track_genre.csv` | 113.550 |

I conteggi sono quelli pubblicati e ancorati da `docs/data_model.md` §3; qui sono **valori attesi di controllo**, non valori pubblicati da questa feature. Se il modello caricato ne mostrasse di diversi, è un difetto di caricamento e la costruzione si ferma.

**La versione della tabella dei mood non è un dettaglio**: ogni valore di `BQ1-K3`, `BQ2-K2` e `BQ2-K3` è calcolato sulla versione 2, e il contratto di versione di `content_taxonomy_bridge.md` §5 dice che una revisione della tabella **invalida** quei valori invece di correggerli. Se il modello caricasse una versione diversa, i valori a schermo divergerebbero da quelli pubblicati senza che nulla lo segnali.

### 1.2 Le cinque relazioni

| # | Da | A | Cardinalità | Direzione |
|---|---|---|---|---|
| R1 | `dim_title` | `bridge_title_category` | uno a molti | **bidirezionale** |
| R2 | `dim_category` | `bridge_title_category` | uno a molti | singola |
| R3 | `dim_category` | `dim_category_mood` | uno a uno | singola |
| R4 | `dim_track` | `fact_track_segment` | uno a molti | singola |
| R5 | `dim_segment` | `fact_track_segment` | uno a molti | singola |

**Nessuna relazione fra il gruppo video e quello musicale**, e non è un'omissione: `data_model.md` §4 la vieta, e `kpi_measures.md` §6.2 poggia su quel divieto per giustificare l'assenza di un `ALL` nella formula di `BQ2-K2`. Introdurre quel collegamento renderebbe sbagliata una misura pubblicata.

**R5 è l'unica relazione i cui due lati portano nomi di colonna diversi**: `dim_segment[segment]` con `fact_track_segment[track_genre]`. È dichiarato da `data_model.md` §6 e va saputo prima di tracciarla, perché sul lato video vale la simmetria opposta.

**R1 è bidirezionale e resta sicura solo finché fra `dim_title` e `dim_category` esiste un cammino solo.** Questa feature non aggiunge tabelle né relazioni, quindi la condizione regge per costruzione — ed è registrato qui perché l'obbligo di `data_model.md` §6 vincola *chiunque* modifichi il modello, non solo chi lo ha disegnato.

### 1.3 Le dieci misure

Otto principali più due companion, con i nomi semantici invariati (`F8`). Il testo DAX è quello pubblicato da `docs/kpi_measures.md`, incollato e non riscritto (`FR-009`).

| Misura | KPI | Grana del risultato | Sezione di `kpi_measures.md` | Cartella DAX |
|---|---|---|---|---|
| `music_adjacent_catalog_share` | `BQ1-K1` 🎯 | catalogo intero | §2.2 | `BQ1` |
| `c1_music_above_median` | `BQ1-K1`, companion | catalogo intero, booleano | §2.3 | `BQ1` |
| `format_duration_gap` | `BQ1-K2` | catalogo intero | §3.2 | `BQ1` |
| `mood_profile_overlap` | `BQ1-K3` | catalogo intero | §4.2 | `BQ1` |
| `segment_demand_index` | `BQ2-K1` | segmento | §5.2 | `BQ2` |
| `segment_zero_share` | `BQ2-K1`, companion (`D7`) | segmento | §5.2 | `BQ2` |
| `segment_catalog_affinity` | `BQ2-K2` | segmento | §6.2 | `BQ2` |
| `segment_entry_priority_score` | `BQ2-K3` | segmento | §7.3 | `BQ2` |
| `segment_entry_priority_quadrant` | `BQ2-K3` | segmento, booleano | §7.3 | `BQ2` |
| `segment_entry_priority_rank` | `BQ2-K3` | segmento, posizione | §7.3 | `BQ2` |

**`BQ3-K1` e `BQ3-K2` non compaiono in questa tabella e non è un'omissione**: non esiste una misura da scrivere. Sono sei valori di scenario congelati in `reports/bq3_scenarios.json` dalla feature `004`, portati nel modello come valori e verificati in modo esaustivo da `E9`. Come entrino nel modello è un vincolo che `data_model.md` §19 assegna «alle misure o alla dashboard»: la `007b` li ha portati senza scrivere una misura, e questa feature fa lo stesso.

**Due misure di soglia, aggiunte da `F7`**: le due espressioni `MEDIANX ( ALL ( dim_segment ), … )` che oggi vivono dentro `segment_entry_priority_quadrant` vengono esposte come misure proprie per servire le linee di riferimento della dispersione. Non sono formule nuove — sono le stesse variabili, estratte — e la loro lettura si confronta una volta con i valori pubblicati in §7.1 (★3).

### 1.4 Le tre grane pubblicate, che sono anche il perimetro di ciò che una pagina può mostrare

| Grana | KPI | Che cosa una selezione può legittimamente restringere |
|---|---|---|
| catalogo intero | `BQ1-K1`, `BQ1-K2`, `BQ1-K3` | **nulla**: il valore è unico e non ha varianti pubblicate |
| segmento | `BQ2-K1`, `BQ2-K2`, `BQ2-K3` | il segmento, per tutti e 114 |
| scenario | `BQ3-K1`, `BQ3-K2` | lo scenario, per tutti e tre — ma mai riducendo a uno solo (`F4`) |

È la forma tabellare della regola `F2`. Una quarta riga non esiste, e ogni interazione che ne produrrebbe una è vietata dal contratto di pagina.

### 1.5 Le colonne che vanno guardate prima di costruire

| Colonna | Tabella | Dominio atteso | Perché |
|---|---|---|---|
| `energy` | `dim_track` | `0-1` | issue `#11`: la tipizzazione a locale le ha già lette come centinaia una volta |
| `valence` | `dim_track` | `0-1` | come sopra |
| `danceability` | `dim_track` | `0-1` | come sopra |

`duration_min` di `dim_track` **non** è in questa lista, ed è la ragione per cui la lista è corta: `data_model.md` §13 la definisce come derivazione interna al modello da `duration_ms`, che è un intero. Non ha mai avuto un punto decimale da fraintendere, ed è il motivo per cui `format_duration_gap` era al riparo dal difetto mentre le tre colonne di mood non lo erano.

---

## Parte 2 — Le entità documentali di questa feature

| Entità | Dove vive | Che cosa è una istanza | Chi la produce |
|---|---|---|---|
| **Contratto di pagina** | `contracts/page-contract.md` | il disegno di una pagina: KPI esposti, visuale e ragione, filtri, interazioni escluse, navigazione | la sessione, blocco A |
| **Pagina** | nel `.pbix` | un'unità di navigazione: ingresso, `BQ1`, `BQ2`, `BQ3` | Valerio, blocco ★2 |
| **Scostamento** | sezione di esito in `quickstart.md` | una differenza fra contratto approvato e pagina costruita | Valerio lo osserva, la sessione lo registra |
| **Ritrovamento** | nota in loco su `docs/kpi_measures.md` | una differenza fra un valore letto a schermo e un valore pubblicato | Valerio lo osserva, la sessione lo dichiara |

**Le due ultime entità hanno regole di scrittura diverse, ed è la ragione per cui sono due entità** (`F9`). Uno scostamento si elenca con la propria ragione e non tocca alcun valore. Un ritrovamento obbliga a una nota in loco sull'artefatto che il valore pubblica, con data, feature, valore precedente, valore corretto, causa e fonte verificabile — e il valore originale resta.

**Validazione**: un contratto senza la voce «interazioni non offerte» è incompleto (`FR-004`); un contratto che trascrive un valore di KPI viola `FR-003`; un esito che elenca zero scostamenti è ammesso solo se le pagine costruite coincidono con il contratto in ogni voce, non come forma abbreviata di «non ho controllato».
