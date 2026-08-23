# Data Model: Misure DAX e documento dei KPI

**Feature**: 007b-kpi-measures | **Data**: 2026-08-22

## Perché questo file descrive due cose, non una

Ogni `data-model.md` precedente descrive o le righe e colonne di un artefatto sotto `data/` (`005`, `006`) o la forma di un documento di prosa (`007a`). Questa feature produce entrambi: un artefatto JSON che uno script scrive (`reports/kpi_measures.json`) e un documento che una persona legge (`docs/kpi_measures.md`), e i due non hanno la stessa forma — il primo è dati, il secondo è la loro esposizione con provenienza e limiti. Le due sezioni seguenti li descrivono separatamente; la terza dichiara come si corrispondono.

## Entità 1 — `reports/kpi_measures.json`

Stesso schema a quattro blocchi di `reports/bq3_scenarios.json`: `values`, `catalogs`, `conventions`, `sources`, più `schema_version`.

### 1.1 Blocco `values`

Una voce per ciascun valore pubblicato, identificata da una chiave che segue la stessa disciplina di prefisso degli altri artefatti (`KPI.misura[.segmento].campo`). Non sono otto voci: i tre KPI per segmento contribuiscono 114 voci ciascuno, e gli operatori di supporto (invarianza, quota film, doppia mediana) ne aggiungono altre.

| Chiave (esempio) | Contenuto |
|---|---|
| `KPI.BQ1K1.share` | `music_adjacent_catalog_share` — quota, 4 cifre |
| `KPI.BQ1K1.c1.category_count.music_musicals` | conteggio titoli in `Music & Musicals` sul ponte trasformato (E7) |
| `KPI.BQ1K1.c1.median_of_42` | mediana dei 42 conteggi per categoria (E2/D10) |
| `KPI.BQ1K1.c1.above_median` | booleano — `Music & Musicals` supera la mediana (condizione stretta) |
| `KPI.BQ1K1.north_star_invariance.transformed_count` | conteggio diretto su `netflix_title_category.csv` (E7) |
| `KPI.BQ1K1.north_star_invariance.origin_count` | `375`, ripubblicato da `NF.cat.music_musicals.titles` per confronto fianco a fianco |
| `KPI.BQ1K1.north_star_invariance.matches` | booleano — esito del confronto di E7 |
| `KPI.BQ1K2.gap_minutes` | `format_duration_gap`, con segno, 2 cifre |
| `KPI.BQ1K2.median_music_all_rows` | mediana durata musicale, tutte le tracce (E3, variante 1) |
| `KPI.BQ1K2.median_music_excluding_zero` | mediana durata musicale, esclusa la riga `is_duration_zero` (E3, variante 2) |
| `KPI.BQ1K2.median_variant_delta` | differenza fra le due varianti di E3 |
| `KPI.BQ1K2.movie_share_of_video_catalog` | quota film sul catalogo video (E4), 4 cifre |
| `KPI.BQ1K3.overlap_share` | `mood_profile_overlap`, quota, 4 cifre |
| `KPI.BQ2K1.<segmento>.demand_index` | mediana di popolarità del segmento, 1 cifra — 114 voci |
| `KPI.BQ2K1.<segmento>.zero_share` | quota di righe a popolarità zero del segmento, 4 cifre — 114 voci |
| `KPI.BQ2K2.<segmento>.affinity` | `segment_catalog_affinity`, 4 cifre — 114 voci |
| `KPI.BQ2K3.<segmento>.score` | punteggio pesato, 4 cifre — 114 voci |
| `KPI.BQ2K3.<segmento>.quadrant_high_high` | booleano — appartenenza al quadrante alta-domanda/alta-affinità — 114 voci |
| `KPI.BQ2K3.<segmento>.rank` | posizione in graduatoria, punteggio decrescente — 114 voci |

**`BQ3-K1`/`BQ3-K2` non compaiono in questo blocco**: FR-011 li cita direttamente da `reports/bq3_scenarios.json`, senza ricalcolo — introdurre una copia qui duplicherebbe una fonte già ancorata (lo stesso argomento per cui `dim_category_mood.json` non viene mai ricopiato altrove).

**Ogni voce porta**, oltre al valore: `display` (stringa formattata secondo E5), `value` (stringa `Decimal`, mai un numero JSON nativo — la stessa disciplina di `build_bq3_scenarios.py`, "i numeri escono come stringhe, come entrano"), `label` (prosa breve), `unit`.

### 1.2 Blocco `catalogs`

| Chiave | Contenuto |
|---|---|
| `catalogs.mood_categories` | le 42 categorie distinte di `dim_category_mood`, stesso elenco già usato da `check_audit_coherence.py` (`TAXONOMY_GUARD`) |
| `catalogs.segments` | i 114 segmenti distinti di `dim_segment` |
| `catalogs.high_zero_segments` | i 7 segmenti con `is_high_zero_genre` vero — sottoinsieme di `catalogs.segments`, usato per decidere dove F R-008 richiede l'avvertimento testuale |

### 1.3 Blocco `conventions`

| Chiave | Contenuto |
|---|---|
| `conventions.median_rule` | testo di E2/D10 — ordinamento, media dei due centrali su conteggio pari, nessuna eccezione per i pari merito |
| `conventions.duration_zero_inclusion` | testo di E3 — inclusione, con riferimento alle due varianti pubblicate |
| `conventions.rounding` | la tabella di E5, cifre per unità di misura, stessa forma di `bq3_rounding` in `build_bq3_scenarios.py` |
| `conventions.mood_table_version` | ripubblica `MOOD.table.version` per comodità di lettura di chi apre solo questo artefatto — non è un valore nuovo, è una citazione |

### 1.4 Blocco `sources`

Impronta (`sha256`, dimensione in byte) di ciascuno dei file letti: `netflix_titles.csv`, `netflix_title_category.csv`, `spotify_tracks.csv`, `spotify_track_genre.csv`, `dim_category_mood.json`, più `bq3_scenarios.json` se citato per FR-011. Stessa funzione `fingerprint()` di `build_bq3_scenarios.py`, applicata a più file.

### 1.5 Guardia (FR-004)

Prima di scrivere il file, lo script verifica che: (a) l'insieme dei 42 nomi di categoria letti dal ponte titolo-categoria coincida con `catalogs.mood_categories`; (b) l'insieme dei 114 nomi di segmento letti da `spotify_track_genre.csv` coincida con `catalogs.segments`; (c) nessuna aggregazione per categoria o per segmento operi su un insieme vuoto. Una qualunque disuguaglianza ferma lo script con un errore esplicito, senza scrivere alcun file — stesso principio del `guard_rate` di `build_bq3_scenarios.py`.

## Entità 1bis — `reports/kpi_engine_check.json`

**Aggiunta dalla revisione di regia sul piano — rilievo bloccante.** `reports/kpi_measures.json` è generato dallo script ed è deterministico per FR-003: non può contenere una lettura umana senza smettere di esserlo. Le otto letture del motore prodotte da E9, e il confronto che ne segue, hanno quindi bisogno di un artefatto proprio — **curato a mano, mai scritto né riscritto da alcuno script**, sul precedente di `data/benchmarks/bq3_tier_upgrade.json` — perché senza di esso il numero letto dal motore non avrebbe alcuna ancora, e sotto severità stretta il controllo di coerenza fermerebbe proprio il ramo in cui E9 trova una divergenza: l'unico caso in cui questa feature avrebbe qualcosa di nuovo da dire.

| Chiave (esempio) | Contenuto |
|---|---|
| `ENGINE.check.date` | data in cui Valerio ha eseguito il confronto |
| `ENGINE.check.pbix_state` | riferimento allo stato del `.pbix` da cui provengono le letture (es. commit o versione della materializzazione citata in `docs/roadmap.md`) |
| `ENGINE.check.<misura>.reading` | il valore letto dal motore per ciascuna delle otto misure |
| `ENGINE.check.<misura>.matches` | booleano — coincide con `reports/kpi_measures.json` |
| `ENGINE.check.<misura>.delta` | la differenza, dove `matches` è falso — anch'essa un valore misurato per costruzione (confronto fra due valori misurati, regola D5), non un numero scritto a mano nella prosa |

**Perché è curato a mano e non generato.** Il passaggio che lo alimenta — Valerio che legge un numero a schermo in Power BI Desktop — non è uno script e non può esserlo (principio V): è un'osservazione umana, irripetibile allo stesso modo di una ricognizione di benchmark. Congelarla in un artefatto versionato, invece di scriverla solo nella prosa di `docs/kpi_measures.md`, è ciò che le dà un'ancora — esattamente la stessa ragione per cui `data/benchmarks/bq3_tier_upgrade.json` esiste.

**Sesto membro di `ARTIFACTS`.** Entra dopo `reports/kpi_measures.json` (quinto), con verifica di assenza di collisioni di prefisso di chiave (`ENGINE.` non è usato da alcun altro artefatto) contro gli altri cinque.

## Entità 2 — `docs/kpi_measures.md`

Otto blocchi, uno per KPI, ciascuno con la forma seguente (da FR-020):

| Campo | Obbligatorio | Contenuto |
|---|---|---|
| `domanda_di_business` | sì | quale delle tre domande (BQ1/BQ2/BQ3) e come questo KPI vi contribuisce |
| `formula_prosa` | sì | la formula in prosa, ereditata da `kpi_operators.md` |
| `formula_dax` | sì, tranne `BQ3-K1`/`BQ3-K2` | il testo DAX trascritto, da incollare nel modello per E9 |
| `provenienza_modello_dati` | sì | tabelle/colonne da cui la misura legge, `data_model.md` |
| `valore_pubblicato` | sì | il valore, con ancora verso `reports/kpi_measures.json` o `reports/bq3_scenarios.json` |
| `confidenza` | sì | ereditata, mai alterata |
| `stato_di_verifica_e9` | sì | «verificato contro il motore reale» o «calcolato da script, verifica in corso» o nota in loco con divergenza (FR-030) |
| `limiti_specifici` | dove applicabile | i limiti propri del KPI, non quelli generali della sezione "Limiti Dichiarati" |

**Le tre voci per-segmento** (`BQ2-K1`, `BQ2-K2`, `BQ2-K3`) non ripetono questa forma 114 volte in prosa: pubblicano la tabella completa (o un rimando esplicito all'artefatto se la lunghezza lo richiede, `kpi_operators.md` §7.3) più i campi sopra una sola volta per la formula e la provenienza, che sono comuni a tutte le righe.

## Come le due entità si corrispondono

Ogni `valore_pubblicato` di un blocco-KPI in `docs/kpi_measures.md` porta un'ancora che risolve a una chiave di `values` in `reports/kpi_measures.json` (o a `reports/bq3_scenarios.json` per `BQ3-K1`/`BQ3-K2`) — è la proprietà che `scripts/check_audit_coherence.py` verifica meccanicamente dopo l'estensione del blocco C del piano. Nessuna chiave di `values` resta senza un punto del documento che la cita, e nessun valore del documento è scritto a mano: è la stessa relazione biunivoca che l'entità 3 della `007a` aveva dichiarato per i numerali citati come esempio, letta qui al contrario — lì il numero era un input già ancorato da un'altra feature, qui è un risultato che questa feature stessa ancora per la prima volta.

**Il caso che rompe questa corrispondenza**, dichiarato esplicitamente perché non venga scoperto in fase di controllo: le affermazioni derivate (E3's `median_variant_delta`, l'esito booleano di E7, la posizione in graduatoria di `BQ2-K3`) sono ciascuna una chiave propria di `values`, non un numero calcolato a mente nella prosa del documento — regola D5, la stessa che la `002` aveva violato tre volte sotto un esito verde.

**Lo stesso vale per E9, verso l'artefatto diverso.** Lo `stato_di_verifica_e9` di ciascun blocco-KPI non ancora a `reports/kpi_measures.json` — che non contiene alcuna lettura del motore — ma a `reports/kpi_engine_check.json` (Entità 1bis): la lettura, l'esito booleano del confronto e, dove diverge, la differenza sono ciascuno una chiave di quell'artefatto, mai un numero scritto a mano nella prosa di `docs/kpi_measures.md`.
