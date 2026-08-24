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

> **Da compilare nel blocco B**, dopo ★2 e ★3. Fino ad allora questa sezione è vuota, e la sua vuotezza è essa stessa un'informazione: le pagine non sono state costruite.

### Le pagine che esistono

*(una riga per pagina: nome, KPI esposti, visuali, filtri presenti)*

### Gli scostamenti dal contratto approvato

*(una riga per scostamento, con la ragione. Zero righe è ammesso solo se le pagine coincidono con il contratto in ogni voce — non come forma abbreviata di «non ho controllato».)*

### I ritrovamenti

*(una riga per ritrovamento, con il riferimento alla nota in loco che lo dichiara. L'esito atteso è zero.)*

### L'esito delle prove 2 e 11

- **★1 — tipizzazione delle colonne di mood (issue `#11`)**: *(esito da dichiarare)*
- **★3 — lettura delle due soglie (`F7`)**: *(esito da dichiarare)*

### Lo stato delle due issue

- **`#11`**: *(chiusa / aperta, con l'evidenza che manca)*
- **`#18`**: *(chiusa / aperta, con l'evidenza che manca)*
