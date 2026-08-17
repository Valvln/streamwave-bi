# Research — Feature 005: Data Model Design

**Data**: 2026-08-17 | **Fase**: 0 (Outline & Research) | **Spec**: [spec.md](./spec.md)

Le decisioni di merito sul modello — che cosa è un segmento, quante grane esistono, dove vive la popolarità, come si realizzano i tre assi di mood, perché non c'è un calendario, perché il profilo di mood video sta per conto proprio — sono già prese e motivate in [spec.md](./spec.md), sezione «Decisioni», e approvate al primo punto di stop. **Non vengono ripetute qui.**

Questo file contiene le decisioni **tecniche e di artefatto** che la spec aveva lasciato al piano, numerate `T1`-`T11` secondo la convenzione della `003`.

---

## T1 — Quali artefatti la feature produce

**Decisione**: tre artefatti versionati, più due modifiche a documenti già mergiati.

| Artefatto | Natura | Perché |
|---|---|---|
| `docs/data_model.md` | **nuovo**, pubblicato | il deliverable. È l'obbligo del principio V: lo schema del modello dati e il mapping dei campi DEVONO esistere come artefatto testuale invece di vivere solo dentro un file binario |
| `specs/005-data-model-design/contracts/model-contract.md` | **nuovo**, di lavorazione | l'interfaccia fra questa feature e le tre che la consumano. Precedente diretto: il contratto della `003`, scritto «perché la `005` non dovesse riaprire il codice della pipeline» |
| `scripts/check_audit_coherence.py` | **modificato** | una riga in `DOCUMENTS` per registrare il documento nuovo sotto severità stretta |
| `docs/business_case.md` | **modificato** | due note in loco, §5.2 e §4 (BQ2) |
| `README.md` | **modificato** | chiusura del drift |

**Alternativa considerata e scartata**: produrre anche un `reports/data_model.json`, sul modello dei tre artefatti macchina già esistenti. Scartata per due ragioni, la seconda più forte della prima.

La prima è di natura. Gli altri tre artefatti sono **calcolati** dai dati: uno script li rigenera e chiunque può riottenerli. Un modello dati è una **decisione umana**; un JSON che la ricopia non è rigenerabile da nulla, e sarebbe il secondo artefatto versionato non riproducibile dopo `data/benchmarks/` — ma senza la giustificazione di quello, che congela un'osservazione esterna irripetibile.

La seconda è di valore probatorio, ed è dirimente: **un documento che ancora i propri numeri a un file scritto dalla stessa mano nella stessa ora non dimostra nulla.** L'ancora vale perché punta a un artefatto che *qualcun altro* ha prodotto da *altri dati*. Le quantità di `docs/data_model.md` sono cardinalità e conteggi che `reports/data_profile.json` e `reports/cleaning_report.json` già pubblicano: ancorarle lì è **più forte**, non più debole, che ancorarle a un file nuovo. Vedi `T2`.

## T2 — Il documento ancora agli artefatti esistenti, e le ancore esistono tutte

**Decisione**: `docs/data_model.md` entra in `DOCUMENTS` di `scripts/check_audit_coherence.py` con `strict = True`, come i due documenti nuovi che l'hanno preceduto, e risolve i propri identificativi sullo spazio dei nomi già unito dei tre artefatti.

Verifica di copertura eseguita in fase di piano: ogni cardinalità che il modello deve dichiarare ha già un identificativo.

| Grandezza che il modello dichiara | Identificativo | Valore |
|---|---|---|
| righe della dimensione dei titoli | `CL.NF.titles.rows.after` | 8.807 |
| righe del ponte titolo-categoria | `CL.NF.category.assignments` | 19.323 |
| righe della dimensione delle categorie | `CL.NF.category.distinct` | 42 |
| righe della dimensione delle tracce | `CL.SP.track.rows.after` | 89.741 |
| righe del fatto traccia-segmento | `CL.SP.pair.rows.after` | 113.550 |
| righe della dimensione dei segmenti | `SP.genre.count` | 114 |
| segmenti a forte concentrazione di zeri | `CL.SP.zero.high_genres.count` | 7 |
| tracce con popolarità discorde fra le due tabelle | `CL.SP.track.popularity_conflict.tracks` | 720 |
| scarto massimo fra le repliche discordi | `CL.SP.track.popularity_conflict.spread_max` | 44 |
| titoli con durata riparata | `CL.NF.duration.repaired.rows` | 3 |
| righe a durata degenere | `CL.SP.duration.zero.rows` | 1 |

**Sul conteggio dei segmenti**, che è l'unico caso in cui il modello cita un valore del **profilo** invece che del rendiconto: `SP.genre.count` non compare fra i `denominators` del rendiconto, né fra i valori senza controparte, né fra quelli fuori perimetro. Per l'invariante di classificazione totale dichiarata dal contratto della `003`, significa che è stato riconfrontato sul dato trasformato e **non è cambiato**: la deduplicazione di coppia rimuove righe ripetute, non può svuotare un genere. Citarlo per descrivere il dato trasformato è quindi corretto, e la ragione va scritta nel documento invece che lasciata dedurre.

**Nessun ritrovamento**: non esiste una grandezza che il modello debba dichiarare e che nessun artefatto pubblichi. Era il rischio che questa verifica esisteva per escludere, perché avrebbe obbligato o a toccare la pipeline della `003` — vietato dal perimetro — o a scrivere un numero senza fonte.

## T3 — Nessun `data-model.md` sotto `specs/`

**Decisione**: la Fase 1 di questa feature **non produce** `specs/005-data-model-design/data-model.md`, che il template prevede. La deviazione è dichiarata qui invece di essere taciuta.

**Perché**: per ogni altra feature del progetto quel file descrive le entità con cui la feature lavora, ed è cosa diversa dal suo deliverable. Per questa feature le due cose **coincidono**: il modello dati *è* il deliverable. Scriverlo due volte — una sotto `specs/` come artefatto di lavorazione, una sotto `docs/` come documento pubblicato — creerebbe due fonti destinate a divergere al primo rilievo di revisione, perché i rilievi si chiudono sul documento pubblicato e nessuno riapre la copia di lavorazione.

È lo stesso difetto che la `003` ha chiuso spostando la grammatica di marcatura da due contratti sotto `specs/` a `docs/convenzioni-marcatura.md`. Reintrodurlo qui, sull'artefatto che quella lezione riguardava più da vicino, sarebbe difficile da spiegare a chi legge il repository da fuori.

Il precedente della `003` conferma inoltre la lettura: il suo `data-model.md` si apre dichiarando «**non** è il modello dati del progetto: quello è della feature 005». Il file esisteva lì perché il soggetto era la trasformazione. Qui il soggetto è lo schema, e lo schema ha già la propria sede.

**Alternativa considerata**: scrivere `data-model.md` come descrizione meta delle entità che questa feature manipola — «tabella», «grana», «relazione», «mapping di colonna» — con gli invarianti che le legano. Scartata perché quegli invarianti sono requisiti (`FR-006`, `FR-007`, `FR-008`, `FR-018`) e vincoli di contratto (`T4` qui sotto): scriverli una terza volta in forma astratta aggiunge un file e nessuna informazione.

## T4 — La forma del modello: schema a stella con un ponte per lato

**Decisione**: schema a stella, due stelle che non si toccano — una per il catalogo video, una per il catalogo musicale — ciascuna con un ponte che risolve un'appartenenza multipla.

**Perché due stelle disgiunte e non un modello unico.** Non esiste alcuna chiave che leghi un titolo video a una traccia musicale, e non deve esistere: le due tassonomie sono disgiunte, ed è §5.3 del business case a dichiararlo («la sovrapposizione lessicale fra le due è trascurabile»). Il confronto fra i due cataloghi avviene **fra misure**, non fra righe: `BQ1-K2` confronta due mediane, `BQ1-K3` e `BQ2-K2` confrontano due profili aggregati. Tracciare una relazione fra i due lati produrrebbe una giunzione che nessuna misura del framework usa e che qualcuno userebbe per sbaglio.

Le due stelle si toccheranno in un solo punto, e non con una relazione: la tabella del profilo di mood delle categorie video, che la `006` riempirà, porta il lato video sugli stessi tre assi su cui il lato musicale è già misurato. È una **commensurazione**, non una giunzione.

**Alternativa considerata**: un unico modello con una tabella ponte fra generi musicali e categorie video. Scartata: sarebbe la tabella di corrispondenza della `006` promossa a relazione del modello, cioè un artefatto interpretativo travestito da struttura. Fondere una relazione osservata e una costruita è precisamente ciò che la decisione `D6` della spec vieta.

## T5 — Le sette tabelle e la convenzione di naming

**Decisione**: prefissi `dim_`, `fact_`, `bridge_`; nomi in inglese, `snake_case`; nomi di misura identici ai nomi semantici già pubblicati in §5.4 del business case.

| Tabella | Ruolo | Origine |
|---|---|---|
| `dim_title` | dimensione | `data/processed/netflix_titles.csv` |
| `dim_category` | dimensione | **derivata** — vedi `T7` |
| `bridge_title_category` | ponte | `data/processed/netflix_title_category.csv` |
| `dim_category_mood` | dimensione | **vuota** — la riempie la `006` |
| `dim_track` | dimensione | `data/processed/spotify_tracks.csv` |
| `dim_segment` | dimensione | **derivata** — vedi `T7` |
| `fact_track_segment` | fatto | `data/processed/spotify_track_genre.csv` |

**Sul nome `fact_track_segment` contro `fact_track_genre`.** Il file di origine si chiama `spotify_track_genre.csv` e la sua colonna `track_genre`. La tabella del modello porta invece il nome dell'unità di analisi che la decisione `D1` ha fissato: **segmento**. La colonna conserva il nome di origine, perché rinominarla romperebbe la tracciabilità verso il contratto della `003`. Il documento deve dichiarare l'equazione una volta sola e in modo visibile — *un segmento è un genere della fonte* — e non ripeterla a ogni riga.

**Alternativa considerata**: chiamare tutto `genre`, aderendo alla fonte. Scartata perché il business case, la constitution e i tre KPI di BQ2 parlano di *segmento*: un modello che non usa quella parola obbliga ogni lettore a fare la traduzione da sé, che è il modo in cui una definizione operativa faticosamente stabilita si perde.

## T6 — Direzione di filtro: singola ovunque, bidirezionale sui due ponti

**Decisione**: relazioni a filtro singolo dalla dimensione al fatto, con **due sole eccezioni bidirezionali**, entrambe sui ponti che risolvono un'appartenenza multipla.

| Relazione | Cardinalità | Direzione | Ragione |
|---|---|---|---|
| `dim_title` → `bridge_title_category` | uno a molti | **bidirezionale** | senza di essa non si può filtrare l'insieme dei titoli per categoria, che è ciò che `BQ1-K1` chiede |
| `dim_category` → `bridge_title_category` | uno a molti | singola | il ponte non deve filtrare l'elenco delle categorie |
| `dim_category` → `dim_category_mood` | uno a uno | singola | la tabella del profilo è un'estensione della dimensione, non un filtro su di essa |
| `dim_track` → `fact_track_segment` | uno a molti | singola | nessuna misura filtra le tracce a partire dal fatto |
| `dim_segment` → `fact_track_segment` | uno a molti | singola | idem |

**Il rischio della bidirezionalità, e perché qui è contenuto.** Un filtro bidirezionale su un ponte crea percorsi ambigui quando esistono più cammini fra due tabelle. Qui non esistono: la stella video ha un solo ponte e nessun ciclo, e le due stelle sono disgiunte per `T4`. La condizione che rende sicura la scelta è quindi **strutturale e verificabile**, non una speranza — ed è la ragione per cui `T4` va letta prima di questa.

**La trappola che la direzione lascia aperta, e che il modello chiude altrove.** Con il ponte bidirezionale, un conteggio calcolato *sul ponte* conta le assegnazioni e non i titoli: sono 19.323 contro 8.807. È esattamente l'errore che la scheda `BQ1-K1` mette in guardia di non commettere («il denominatore è il conteggio dei titoli distinti, non delle assegnazioni»). La direzione di filtro non lo può impedire; lo impedisce `FR-010`, che obbliga i due conteggi a portare nomi diversi e a vivere su tabelle diverse.

## T7 — Le due dimensioni derivate, e in che senso sono ammesse

**Decisione**: `dim_category` e `dim_segment` non sono fra i quattro dataset e sono **derivate dentro il modello**, come elenco dei valori distinti della rispettiva colonna. La derivazione è una **trasformazione interna al modello**, ammessa e da dichiarare, non una modifica alla pipeline della `003`.

Il confine che `FR-005` traccia regge: la pipeline produce dati normalizzati per forma; il modello decide che ruolo abbiano. Ricavare l'elenco dei valori distinti di una colonna che esiste già non aggiunge né toglie informazione, non interpreta e non seleziona — è la stessa operazione che il motore compie internamente per costruire un asse di raggruppamento.

**Attributi che le due dimensioni derivate portano oltre alla chiave**:

- `dim_segment` porta `is_high_zero_genre`. Il contratto della `003` §1.3 dichiara che il campo è **costante entro un genere** ed è replicato sulla riga «per comodità di lettura». Nel modello è una proprietà del segmento e sale sulla dimensione: lasciarlo sul fatto autorizzerebbe ad aggregarlo, cioè a contare 113.550 volte una proprietà che vale 114 volte.
- `dim_category` non porta attributi. Il profilo di mood, che sarebbe il candidato naturale, sta per conto proprio per la decisione `D6`.

**Il vincolo di riproducibilità è soddisfatto senza codice nuovo**: la derivazione è dichiarata come regola nel documento, e il principio II ammette Power Query M fra i linguaggi di trasformazione. Il **codice** M non viene però scritto da questa feature: sarebbe materializzazione, e la materializzazione è il ritrovamento `F2`. Il documento dichiara la regola; chi materializza la applica.

## T8 — Dove va ciascuna marcatura della `003`

**Decisione**: ogni marcatura sale alla grana di cui è proprietà, e il documento dichiara quale misura condiziona.

| Marcatura | Grana di cui è proprietà | Tabella | Misura che condiziona |
|---|---|---|---|
| `is_high_zero_genre` | segmento | `dim_segment` | `BQ2-K1`, per la divergenza 6 della revisione `001` |
| `is_popularity_zero` | coppia | `fact_track_segment` | `BQ2-K1`, ed è ciò che rende calcolabile la quota di zeri per segmento (`FR-023`) |
| `is_duration_zero` | traccia | `dim_track` | `BQ1-K2`, lato musicale |
| `has_conflicting_popularity` | traccia | `dim_track` | nessuna misura; è la traccia della perdita di `D3` e resta visibile |
| `is_repaired_duration` | titolo | `dim_title` | `BQ1-K2`, lato video |

**Su `is_duration_zero`, una precisazione che decide la riga della tabella.** Il contratto della `003` colloca il campo su **entrambi** i dataset musicali, e il rendiconto lo conta alla grana coppia: `CL.SP.duration.zero.rows` vale 1. Nel modello sale però sulla dimensione, perché la durata è una **proprietà della traccia** e non dell'appartenenza a un segmento — e soprattutto perché la misura che lo consuma, `BQ1-K2`, si calcola per dichiarazione della propria scheda sulle **tracce deduplicate**, cioè su `dim_track`. Lasciarlo sul fatto lo renderebbe invisibile proprio alla sola misura che lo riguarda.

Il valore della marcatura non sta comunque nel numero, che è una riga sola: sta nel fatto che la `007` debba **dichiarare** se quella traccia entra nella mediana, invece di non accorgersi che esiste.

## T9 — La conversione di unità di `BQ1-K2` avviene nel modello, non nella misura

**Decisione**: `dim_track` porta una colonna derivata di durata in minuti, ottenuta dal campo in millisecondi per divisione esatta. Nessun arrotondamento a livello di colonna.

**Perché nel modello e non nella misura**: `BQ1-K2` è una differenza fra due mediane espresse in minuti. Se la conversione vivesse dentro la misura, il lato video e il lato musicale arriverebbero al confronto passando per due strade diverse — uno letto, l'altro calcolato — e la simmetria del confronto dipenderebbe da come è scritta la misura. Convertire nel modello mette i due lati sulla stessa unità **prima** che qualcuno li confronti.

**Perché nessun arrotondamento**: arrotondare la colonna arrotonderebbe ogni traccia prima della mediana, che è una decisione statistica presa di nascosto. L'arrotondamento è di presentazione e appartiene alla `007` — `FR-021`.

## T10 — Stima: ~6,25 ore, dentro il limite, sopra le 5 previste

**Decisione**: la feature **non si scompone**. La stima rivista sta dentro le 6-7 ore del principio III, quindi la condizione che avrebbe attivato il taglio `005a`/`005b` non si verifica.

| Blocco | Ore |
|---|---|
| Fase 0 e Fase 1 — ricerca, contratto, quickstart | 1,25 |
| Task | 0,25 |
| `docs/data_model.md` | 2,00 |
| Registrazione nel controllo, marcatura delle quantità, esito verde | 0,75 |
| Note in loco su §5.2 e §4 del business case | 0,50 |
| Drift del README | 0,25 |
| Revisione in contesto pulito, verbale, chiusura dei rilievi | 1,25 |
| **Totale** | **~6,25** |

Lo scostamento dalla stima di roadmap è **di 1,25 ore su 5**, ed è materiale: va portato al secondo punto di stop e non scoperto a consuntivo. La roadmap dichiara che dal 17 agosto non esiste più margine e che «il primo scostamento va letto subito».

**Dove sta lo scarto rispetto alle 5 ore**: nella marcatura del documento e nel blocco di revisione. La roadmap includeva il costo di revisione nelle stime di `004`, `006`, `007` e `010`, ma la riga della `005` non lo dichiara; la marcatura sotto severità stretta è un costo che le stime precedenti hanno sempre sottovalutato, ed è il secondo caso — dopo la `003` — in cui compare a valle.

## T11 — Ritrovamento: dopo la `003` il campione non è più bilanciato

**Ritrovamento, non decisione.** Registrato per la regia secondo il precedente `FR-032` della `002`, e da dichiarare nel documento perché tocca una misura.

La nota di `BQ2-K1` in §5.5 del business case sostiene che «il catalogo di riferimento contiene **lo stesso numero di tracce per ogni segmento**, per come è stato campionato», e ne trae che contare le tracce per dimensionare un segmento misurerebbe il campionamento e non il mercato. L'affermazione descrive i **dati di origine** e lì resta vera.

Sul **dato trasformato** non lo è più: `CL.SP.recalc.genre.row_counts_distinct` vale 17 e `CL.SP.recalc.genre.rows_min` vale 904. La deduplicazione di coppia ha tolto righe in modo non uniforme fra i segmenti.

**Conseguenza, che va detta perché è controintuitiva**: la conclusione della nota non si indebolisce, si rafforza. Prima contare le righe era inutile perché il risultato era costante; ora è **peggio che inutile**, perché il risultato varia e la variazione è un residuo della deduplicazione, non un segnale di mercato. Un lettore che oggi costruisse un conteggio per segmento vedrebbe differenze e le prenderebbe per informazione.

**Non si apre una nota in loco sul business case**: l'affermazione originale è riferita alla fonte ed è corretta, quindi non c'è nulla da correggere. Il fatto nuovo riguarda `data/processed/` e appartiene al documento del modello, che è dove il lettore incontra quelle tabelle.
