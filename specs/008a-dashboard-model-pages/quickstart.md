# Quickstart: verifica delle pagine e del modello della `008a`

**Feature**: 008a-dashboard-model-pages | **Data**: 2026-08-24

Dodici prove, in ordine di esecuzione. **Una sola è eseguibile da chi ha clonato il repository**; le altre undici richiedono il `.pbix` aperto e non saranno mai automatizzabili — è il principio V, non una lacuna di questo documento. Il loro esito è un'osservazione umana, dichiarata come tale nella sezione finale, sulla stessa forma già usata da `E9` della `007b`.

## Prerequisiti

- `data/processed/` presente (rigenerato con `python3 scripts/build_datasets.py`, che richiede `data/raw/`).
- `data/curated/dim_category_mood.json` versionato, **versione 2**.
- Power BI Desktop, con il `.pbix` già materializzato.
- Il contratto di pagina [approvato](./contracts/page-contract.md).

---

## Le dodici prove

### 1 — Nulla di pubblicato è stato rotto *(eseguibile)*

```bash
python3 scripts/check_audit_coherence.py
```

Atteso: **esito verde**, invariato rispetto al merge della `007b` — sette documenti, sei artefatti. Questa feature non aggiunge documenti né artefatti.

**Che cosa questo verde certifica, e che cosa no.** Certifica che le note in loco eventualmente scritte nel blocco C non hanno rotto alcuna ancora. **Non dice nulla sul deliverable**: nessuno script di questo repository può aprire il `.pbix`, ed è la ragione per cui le undici prove seguenti esistono.

### 2 — Le tre colonne di mood stanno fra 0 e 1 *(manuale, ★1 — prima di ogni altra cosa)*

Aprire il modello e ispezionare `energy`, `valence`, `danceability` di `dim_track`.

Atteso: valori nel dominio `0-1`. Un valore nell'ordine delle centinaia è la ricomparsa del difetto dell'issue `#11`: **la costruzione si ferma**, la tipizzazione si corregge, e il fatto si dichiara nell'esito.

### 3 — Le sette tabelle e le cinque relazioni *(manuale)*

Confrontare il modello con [data-model.md](./data-model.md) §1.1 e §1.2.

Atteso: sette tabelle con i conteggi di riga attesi; cinque relazioni con le direzioni dichiarate; **nessuna relazione fra il gruppo video e quello musicale**; R5 che congiunge `dim_segment[segment]` con `fact_track_segment[track_genre]`.

### 4 — Le dieci misure, con i nomi semantici *(manuale)*

Atteso: le dieci misure di [data-model.md](./data-model.md) §1.3 esistono con i nomi dichiarati, organizzate in cartelle per domanda di business. Ogni nome diverso da quelli è uno scostamento e va elencato.

### 5 — Gli otto KPI sono a schermo *(manuale, SC-001)*

Percorrere le pagine e contare i KPI, confrontandoli con `docs/kpi_measures.md`.

Atteso: otto, nessuno mancante, nessuno in più. Ciascuno con l'etichetta di **fonte** e quella di **confidenza** accanto.

### 6 — I valori a schermo coincidono con quelli pubblicati *(manuale)*

Per ciascuno degli otto KPI, confrontare il valore letto a schermo con quello di `docs/kpi_measures.md` alla stessa grana.

Atteso: coincidenza. Una divergenza è un **ritrovamento**, non uno scostamento: si dichiara con nota in loco sul documento della `007b` (`F9`, `FR-024`), senza riscrivere il valore originale né correggere lo schermo in silenzio.

### 7 — La navigazione *(manuale, SC-002)*

Atteso: quattro pagine, e da ciascuna si raggiunge ogni altra tramite elementi di navigazione interni al report, senza usare il riquadro delle schede di Power BI.

### 8 — I 114 segmenti, senza troncamenti *(manuale, SC-003)*

Sulla pagina `BQ2`: scorrere la graduatoria fino in fondo.

Atteso: 114 righe. Ogni indice di domanda accompagnato dalla propria quota di zeri; i sette segmenti `is_high_zero_genre` — `country`, `iranian`, `jazz`, `latin`, `rock`, `romance`, `soul` — con l'avvertimento accanto al nome. Due segmenti a pari punteggio portano la stessa posizione e la successiva salta.

### 9 — Nessuna interazione produce una grana non pubblicata *(manuale, SC-004)*

Percorrere ogni pagina ed **elencare** ogni filtro, slicer e interazione incrociata attivi. Per ciascuno, verificare che la grana risultante sia una delle tre di [data-model.md](./data-model.md) §1.4.

Atteso in particolare: **nessun filtro di categoria video su alcuna pagina che espone `BQ1-K3`** (issue `#18`); nessun filtro di anno; nessuna visuale che sommi una quantità su più segmenti o che conti le righe di un segmento.

### 10 — `BQ3` come intervallo *(manuale)*

Atteso: tre valori di scenario affiancati per ciascuno dei due KPI, con le unità — punti percentuali della base per `BQ3-K1`, euro per utente al mese per `BQ3-K2`. Nessuna scheda singola; nessuna moltiplicazione per una base utenti o per una durata.

### 11 — Le due soglie del quadrante *(manuale, ★3)*

Leggere le due misure di soglia esposte per le linee di riferimento e confrontarle con `docs/kpi_measures.md` §7.1.

Atteso: coincidenza — che chiude l'esclusione dichiarata in §11.1, dove quelle due soglie erano registrate come **non lette dal motore come valori a sé stanti**. Una divergenza è un ritrovamento.

### 12 — La regola di decisione della North Star non compare *(manuale, F6)*

Atteso: `C1` compare accanto a `BQ1-K1` e `C3` accanto a `BQ2-K3`; **nessuna pagina** compone le condizioni in un verdetto né nomina la regola «tre su tre». È il presidio contro un esito che nessuno ha misurato, perché `C2` non esiste come valore pubblicato.

---

## Esito della costruzione

> **Da compilare nel blocco B**, dopo ★2 e ★3. Le voci si riempiono **mentre accadono** e non a memoria alla fine: è la regola di [tasks.md](./tasks.md), e la ragione per cui alcune sono già compilate mentre le pagine non esistono ancora. Una voce che porta ancora *(esito da dichiarare)* è una voce non ancora osservata; «Le pagine che esistono» vuota significa che la costruzione non è iniziata.

### Le pagine che esistono

*(una riga per pagina: nome, KPI esposti, visuali, filtri presenti)*

### Gli scostamenti dal contratto approvato

| Voce | Contratto | Costruito | Ragione |
|---|---|---|---|
| `BQ3`, tipo di visuale (T020, 2026-08-24) | «una tabella, due righe e tre colonne, più una colonna di unità» | una **matrice** | realizza la stessa disposizione — i due KPI in riga, i tre scenari in colonna — e regge gli stessi due divieti: nessuna scheda singola, nessuna moltiplicazione. La differenza è il nome della visuale in Power BI, non la forma con cui i sei valori si leggono |

### I ritrovamenti

**Nessuno finora.** Gli otto valori letti a schermo coincidono con quelli pubblicati da `docs/kpi_measures.md` alla stessa grana (T023, 2026-08-24); le due soglie e le due companion di `CP-1` coincidono con §7.1 e §3.4. La riga resta aperta fino a T027 e T031, che verificano la pagina `BQ2` e le interazioni.

*(I due difetti corretti in fase di caricamento non sono ritrovamenti: nessun valore pubblicato è risultato sbagliato. Stanno nella sezione dedicata più sotto.)*

### I difetti di caricamento trovati e corretti

Categoria distinta dalle due precedenti, e la distinzione non è formale: non è uno scostamento dal contratto — il contratto non parla di come i file si leggono — e non è un ritrovamento, perché nessun valore pubblicato è risultato sbagliato. È il caso che [data-model.md](./data-model.md) §1.1 prevede in una riga: «se il modello caricato ne mostrasse di diversi, è un difetto di caricamento e la costruzione si ferma».

**`dim_title` caricava 8809 righe invece delle 8807 attese** (T013, 2026-08-24).

- **Causa**: due record di `data/processed/netflix_titles.csv` contengono un ritorno a capo dentro un campo quotato — `s8202` nel campo `description`, `s8420` nel campo `title`. Il passaggio di origine leggeva il file con `QuoteStyle.None`, che ignora le virgolette e spezza quei due record in due righe ciascuno.
- **Correzione**: `QuoteStyle.Csv` sul passaggio di origine di `dim_title`. Dopo il ricaricamento il conteggio coincide con quello atteso.
- **Perimetro accertato**: è l'unico dei quattro file di `data/processed/` in cui record CSV e righe fisiche divergono. Le altre sei tabelle tornavano già prima della correzione, e la ragione è questa.
- **Che cosa il difetto avrebbe prodotto se non fosse stato visto**: le righe spurie portano i campi spostati di posizione, quindi `type` e `movie_duration_min` degeneri. Sarebbero entrate nella mediana dei film di `format_duration_gap` e nei conteggi per categoria della North Star, cambiando due valori pubblicati **senza che nulla lo segnalasse** — nessuno script di questo repository entra nel modello.
- **Il dato di origine non è stato toccato.** Il ritorno a capo dentro il titolo di `s8420` è il valore vero e resta tale: `data/processed/` è fuori dal perimetro di scrittura di questa feature, e il titolo si legge su due righe anche a schermo.
- **Nulla impedisce che ricompaia.** L'impostazione vive dentro il `.pbix`, che non è versionato: un reimport futuro può rimettere `QuoteStyle.None` senza che nessun controllo se ne accorga. È la stessa forma dell'issue `#11`, e alla chiusura va aperta una issue analoga.

**`bq3_scenarios` aveva perso la colonna `scenario`** (T020, 2026-08-24).

- **Causa**: la materializzazione della tabella disconnessa di `CP-2` non ha portato la colonna che nomina lo scenario.
- **Correzione**: colonna ripristinata prima di costruire la pagina.
- **Perché non è un dettaglio**: senza `scenario` i sei valori restano sei numeri senza l'etichetta che dice a quale ipotesi ciascuno appartiene. `F4` impone che `BQ3` compaia come intervallo a tre scenari, e un intervallo di cui non si sa quale estremo sia il pessimista non è un intervallo: è tre numeri affiancati. Il divieto di scheda singola sarebbe stato rispettato alla lettera e violato nella sostanza.
- **Stessa fragilità delle due precedenti**: vive nel `.pbix` non versionato, e rientra nella issue che alla chiusura va aperta.

### Le decisioni `CP` e come sono state eseguite

- **`CP-2` — i sei valori di `BQ3`**: creata la tabella `bq3_scenarios`, **disconnessa** dal resto del modello (T013, 2026-08-24). Le tabelle nel modello sono quindi otto invece delle sette di [data-model.md](./data-model.md) §1.1, e le relazioni restano cinque. L'assenza di relazioni è la proprietà che impedisce di filtrare gli scenari per segmento o per categoria.
- **`CP-1` — le due misure companion**: scritte ed esposte nel modello, e la loro lettura **coincide** con i valori pubblicati — la quota di titoli `Movie` con `kpi_measures.md` §3.4, `C3` con §7.1 (T016-T017, 2026-08-24). Nessun ritrovamento: la nota in loco di T035a resta dovuta come **aggiunta** del testo DAX, non come correzione di un valore.
- **`CP-3` — la North Star su due pagine**: eseguita come approvata (T018-T019, 2026-08-24). `music_adjacent_catalog_share` compare sulla pagina di ingresso con le sole etichette e sulla pagina `BQ1` con `C1` accanto. Stessa misura, stessa grana: non può divergere, e la ripetizione è voluta.

### L'esito delle prove 2 e 11

- **★1 — tipizzazione delle colonne di mood (issue `#11`)**: **difetto assente**. `energy`, `valence` e `danceability` di `dim_track` stanno nel dominio `0-1`; verificato in seconda lettura (T011-T012, 2026-08-24).
- **★3 — lettura delle due soglie (`F7`)**: **coincidenza**. Le due misure di soglia esposte per le linee di riferimento restituiscono i valori pubblicati in `kpi_measures.md` §7.1 (T016-T017, 2026-08-24).

  **Che cosa questa coincidenza chiude.** `kpi_measures.md` §11.1 dichiara le due soglie fra gli esclusi dal confronto contro il motore, perché vivevano come variabili interne a `segment_entry_priority_quadrant` e non erano leggibili come valori a sé stanti. Esposte come misure, sono state lette: l'esclusione non è più vera. È lo stesso caso di §3.4 e §7.1 — il documento canonico resta indietro rispetto al modello — e per la stessa ragione va registrato in loco. Vedi la nota su T035a in [tasks.md](./tasks.md).

### Lo stato delle due issue

- **`#11`**: *(chiusa / aperta, con l'evidenza che manca)*
- **`#18`**: *(chiusa / aperta, con l'evidenza che manca)*
