---

description: "Task list template for feature implementation"
---

# Tasks: Dashboard — modello, pagine, misure a schermo

**Input**: Documenti di progettazione da `/specs/008a-dashboard-model-pages/`

**Prerequisiti**: plan.md, spec.md, research.md, data-model.md, contracts/dashboard-contract.md, quickstart.md — tutti presenti. `contracts/page-contract.md` **non** esiste ancora: è il prodotto della Fase 2.

**Test**: nessun task di test in senso software. La correttezza si verifica con le dodici prove di [quickstart.md](./quickstart.md) — una eseguibile, undici manuali — incorporate come task lungo le fasi e riverificate in blocco da T037, più la revisione in contesto pulito (T039-T040).

**Una lista diversa da tutte le precedenti, e va detto prima di leggerla.** Ventuno task su quarantatré sono marcati **(manuale, Valerio)**: non sono istruzioni che questa sessione esegue, sono istruzioni che una persona esegue davanti a Power BI Desktop. È il principio V, e la constitution lo prescrive esplicitamente — «i task di build della dashboard DEVONO essere formulati come istruzioni eseguibili da una persona». La sessione li scrive, ne raccoglie l'esito e lo documenta; non li esegue e non può verificarli da sé.

**La marcatura `[P]` è quasi assente**, e non è una svista. La Fase 2 scrive per intero un solo file (`contracts/page-contract.md`); le Fasi 4-7 toccano tutte lo stesso `.pbix`, che è un file solo e non ammette lavoro parallelo. `[P]` compare solo dove due task toccano file davvero distinti.

## Path Conventions

Repository singolo. Contratto di pagina in `specs/008a-dashboard-model-pages/contracts/page-contract.md`; esito in `specs/008a-dashboard-model-pages/quickstart.md`, sezione «Esito della costruzione»; contratto di lettura in `specs/008a-dashboard-model-pages/contracts/dashboard-contract.md`; verbale in `specs/008a-dashboard-model-pages/review.md`. Il deliverable vive nel `.pbix`, **non versionato**, sulla macchina di Valerio. Fuori dalla cartella della feature si toccano solo `README.md` e — unicamente in caso di ritrovamento — `docs/kpi_measures.md`.

---

## Phase 1: Setup

**Purpose**: gli input del contratto di pagina, raccolti prima di scriverlo, perché il contratto non contenga scelte prese mentre lo si scrive.

- [X] T001 Scrivi l'intestazione e la mappa KPI → pagina → grana in `specs/008a-dashboard-model-pages/contracts/page-contract.md`: le quattro pagine (ingresso, `BQ1`, `BQ2`, `BQ3`), quale KPI vive su quale, e la grana pubblicata di ciascuno secondo [data-model.md](./data-model.md) §1.4
- [X] T002 Aggiungi in `specs/008a-dashboard-model-pages/contracts/page-contract.md` la sezione «La regola che governa ogni pagina»: la regola di invarianza a schermo (`F2`) enunciata una volta sola, con l'elenco delle tre grane ammesse, così che le sezioni per pagina la citino invece di ripeterla

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: il contratto di pagina completo, e la sua approvazione. È il terzo punto di fermata della feature.

**⚠️ CRITICAL**: nessun task della Fase 3 o successive inizia prima che T010 abbia ricevuto risposta. Aprire Power BI prima dell'approvazione annulla l'unico presidio che questa feature possiede.

- [X] T003 Scrivi in `specs/008a-dashboard-model-pages/contracts/page-contract.md` la sezione della **pagina di ingresso**: la North Star (`BQ1-K1`) con le sue etichette, la navigazione verso le tre pagine di domanda, e la dichiarazione esplicita che la pagina non porta prosa — lo spazio per essa è della `008b`
- [X] T004 Scrivi la sezione della **pagina `BQ1`**: `BQ1-K1` con `C1` accanto, `BQ1-K2` con il proprio segno e la quota di film che ne dichiara l'asimmetria, `BQ1-K3`; per ciascuno la visuale scelta e la ragione **contro la forma del dato** — tre valori unici sul catalogo intero, che è la ragione per cui la scheda regge qui e non regge su `BQ2` (`FR-002`)
- [X] T005 Scrivi la sezione della **pagina `BQ2`**: la dispersione domanda × affinità come visuale primaria con le due soglie come linee di riferimento, la graduatoria completa dei 114 segmenti come visuale di dettaglio sulla stessa pagina, la quota di zeri accanto a ogni indice di domanda (`D7`), l'avvertimento accanto ai sette segmenti `is_high_zero_genre`, `C3` accanto a `BQ2-K3`; e la ragione per cui una cima di graduatoria è stata scartata (`F3`)
- [X] T006 Scrivi la sezione della **pagina `BQ3`**: i due KPI come tre valori di scenario affiancati con le rispettive unità, il divieto di scheda singola e il divieto di qualunque moltiplicazione (`F4`), e la nota che il debito della `004` sulla verificabilità del benchmark resta aperto mentre quei numeri vanno a schermo
- [X] T007 Scrivi in `specs/008a-dashboard-model-pages/contracts/page-contract.md`, per ciascuna delle quattro pagine, la voce **«interazioni non offerte, e perché»** (`FR-004`): nessun filtro di categoria video dove vive `BQ1-K3` (issue `#18`), nessun filtro di anno, nessuna somma su più segmenti, nessun conteggio di righe per segmento, nessun verdetto composto sulle tre condizioni della North Star (`F6`)
- [X] T008 Scrivi la sezione **«Dove la `008b` scriverà»**: per ciascuna pagina, lo spazio lasciato libero per la narrazione e i limiti, dichiarato come riservato e non come vuoto — così che la feature successiva non debba ridisegnare le pagine per farvi entrare il proprio testo
- [X] T009 Rileggi `specs/008a-dashboard-model-pages/contracts/page-contract.md` contro `FR-003`: nessun valore di KPI trascritto, solo nomi di misura e rinvii alle sezioni di `docs/kpi_measures.md` che li pubblicano
- [X] T010 **PUNTO DI FERMATA 3** — proponi il commit del contratto di pagina e **fermati**: il contratto torna a Valerio per approvazione o correzione, prima che Power BI Desktop venga aperto (`FR-005`, `F1`). Riporta che cosa il contratto decide e su che cosa chiede una conferma

**Checkpoint**: contratto approvato e committato. Il repository è in uno stato coerente e nulla di ciò che esiste può ancora contraddirlo.

---

## Phase 3: User Story 4 - Il modello è caricato con i tipi giusti (Priority: P1) 🎯

**Goal**: che nessuna pagina venga costruita sopra colonne tipizzate male.

**Independent Test**: prova 2 di [quickstart.md](./quickstart.md).

**⚠️ Questa fase precede ogni altra costruzione.** È il costo di una lettura contro il costo di rifare le pagine — la lezione che `E9` ha già pagato per conto di questa feature.

- [X] T011 **(manuale, Valerio)** Apri il `.pbix` e ispeziona `energy`, `valence`, `danceability` di `dim_track`: i valori devono stare fra 0 e 1. Se sono nell'ordine delle centinaia, **fermati**, correggi la tipizzazione e annota l'accaduto come ricomparsa dell'issue `#11` (`FR-007`)
- [X] T012 **(manuale, Valerio)** Annota l'esito di T011 in forma grezza, per la trascrizione del blocco B: difetto assente, oppure presente e corretto

**Checkpoint**: le tre colonne di mood sono nel dominio giusto. Solo ora si costruisce.

---

## Phase 4: User Story 1 - Le tre domande a schermo, con i loro KPI (Priority: P1) 🎯

**Goal**: il deliverable — otto KPI su quattro pagine, con etichette e navigazione.

**Independent Test**: prove 3, 4, 5, 6, 7 e 10 di [quickstart.md](./quickstart.md).

- [X] T013 **(manuale, Valerio)** [US1] Verifica nel `.pbix` le sette tabelle e i loro conteggi di riga contro [data-model.md](./data-model.md) §1.1, inclusa la versione 2 di `dim_category_mood`; accerta inoltre in quale forma il modello porta oggi i sei valori di scenario di `BQ3` e, se sono digitati, portali a leggere `reports/bq3_scenarios.json` come tabella disconnessa (`CP-2`)
- [X] T014 **(manuale, Valerio)** [US1] Verifica nel `.pbix` le cinque relazioni e le loro direzioni contro [data-model.md](./data-model.md) §1.2: R1 bidirezionale, nessuna relazione fra gruppo video e gruppo musicale, R5 fra `dim_segment[segment]` e `fact_track_segment[track_genre]`
- [X] T015 **(manuale, Valerio)** [US1] Incolla nel `.pbix` le dieci misure con i nomi semantici di [data-model.md](./data-model.md) §1.3, organizzate in cartelle DAX per domanda di business; il testo DAX è quello pubblicato da `docs/kpi_measures.md`, non riscritto (`FR-008`, `FR-009`)
- [X] T016 **(manuale, Valerio)** [US1] Esponi come misure proprie le due soglie del quadrante — le stesse espressioni `MEDIANX ( ALL ( dim_segment ), … )` che vivono dentro `segment_entry_priority_quadrant` (`F7`, `FR-010`) — e scrivi le due misure companion di `CP-1`: la quota di titoli `Movie` sul catalogo video e `C3`, sul modello di `c1_music_above_median`
- [X] T017 **(manuale, Valerio)** [US1] Leggi le due misure di soglia contro i valori pubblicati in `docs/kpi_measures.md` §7.1 e le due companion di `CP-1` contro §3.4 e §7.1; annota per ciascuna coincidenza o divergenza (★3, prova 11)
- [X] T018 **(manuale, Valerio)** [US1] Costruisci la **pagina di ingresso** secondo il contratto approvato: North Star con le sue etichette, navigazione verso le tre pagine, nessuna prosa
- [X] T019 **(manuale, Valerio)** [US1] Costruisci la **pagina `BQ1`** secondo il contratto: `BQ1-K1` con `C1`, `BQ1-K2`, `BQ1-K3`, **senza alcun filtro di categoria video** (`FR-020`)
- [X] T020 **(manuale, Valerio)** [US1] Costruisci la **pagina `BQ3`** secondo il contratto: tre valori di scenario affiancati per ciascuno dei due KPI, con le unità; nessuna scheda singola, nessuna moltiplicazione (`FR-013`, `FR-014`)
- [X] T021 **(manuale, Valerio)** [US1] Aggiungi accanto a ciascuno degli otto KPI l'etichetta di **fonte** e quella di **confidenza**, nella forma di `business_case.md` §5.4 (`F5`, `FR-012`)
- [X] T022 **(manuale, Valerio)** [US1] Aggiungi gli elementi di navigazione su tutte e quattro le pagine: da ciascuna si raggiunge ogni altra senza usare il riquadro delle schede (`FR-021`)
- [X] T023 **(manuale, Valerio)** [US1] Confronta ciascuno degli otto valori letti a schermo con quello pubblicato da `docs/kpi_measures.md` alla stessa grana; annota ogni divergenza come **ritrovamento**, non come scostamento (prova 6, `F9`)

**Checkpoint**: otto KPI a schermo con etichette e navigazione. La pagina `BQ2` esiste ma non è ancora completa: la Fase 5 la chiude.

---

## Phase 5: User Story 2 - I 114 segmenti leggibili, senza troncare (Priority: P1)

**Goal**: che la domanda `BQ2` si legga a colpo d'occhio senza che il vincolo delle 114 voci produca una vista che mente per omissione.

**Independent Test**: prova 8 di [quickstart.md](./quickstart.md).

- [X] T024 **(manuale, Valerio)** [US2] Costruisci sulla pagina `BQ2` la **dispersione** domanda × affinità, con le due misure di soglia di T016 come linee di riferimento e i segmenti del quadrante distinguibili dagli altri
- [X] T025 **(manuale, Valerio)** [US2] Costruisci sulla stessa pagina la **graduatoria completa**: tutti i 114 segmenti, ordinati per punteggio decrescente, con la quota di zeri accanto a ogni indice di domanda e `C3` accanto a `BQ2-K3` (`FR-015`, `FR-016`, `FR-017`)
- [X] T026 **(manuale, Valerio)** [US2] Aggiungi l'avvertimento accanto al nome dei sette segmenti `is_high_zero_genre` — `country`, `iranian`, `jazz`, `latin`, `rock`, `romance`, `soul` (`D7`, `FR-015`)
- [X] T027 **(manuale, Valerio)** [US2] Verifica a schermo: 114 righe contate, nessun segmento escluso, e due segmenti a pari punteggio che portano la stessa posizione con la successiva che salta (`kpi_measures.md` §7.2)

**Checkpoint**: la pagina `BQ2` risponde alla domanda di business e non nasconde la coda.

---

## Phase 6: User Story 3 - Nessuna interazione produce un valore non pubblicato (Priority: P1)

**Goal**: che la regola `F2` sia vera del file costruito, non solo del contratto approvato.

**Independent Test**: prova 9 di [quickstart.md](./quickstart.md).

- [X] T028 **(manuale, Valerio)** [US3] Percorri le quattro pagine ed **elenca** ogni filtro, slicer e interazione incrociata attivi; per ciascuno dichiara quale grana produce, confrontandola con le tre di [data-model.md](./data-model.md) §1.4 (`FR-019`)
- [X] T029 **(manuale, Valerio)** [US3] Verifica che nessuna pagina che espone `BQ1-K3` offra un filtro di categoria video, e che nessuna offra un filtro di anno (issue `#18`, `FR-020`)
- [X] T030 **(manuale, Valerio)** [US3] Verifica che nessuna visuale offra un conteggio di righe per segmento, una somma su più segmenti o un asse temporale (`FR-018`)
- [X] T031 **(manuale, Valerio)** [US3] Verifica che nessuna pagina componga `C1` e `C3` in un verdetto né nomini la regola «tre su tre» (`F6`, prova 12)

**Checkpoint**: la regola di invarianza a schermo è verificata sul costruito, pagina per pagina.

---

## Phase 7: User Story 5 - Chi legge il repository sa che cosa esiste (Priority: P2)

**Goal**: che il deliverable sia ispezionabile da chi non può aprirlo.

**Independent Test**: leggere contratto ed esito in sequenza e ricostruire che cosa esiste, senza aprire il `.pbix`.

- [X] T032 [US5] Compila in `specs/008a-dashboard-model-pages/quickstart.md`, sezione «Esito della costruzione», l'elenco delle pagine che esistono: nome, KPI esposti, visuali, filtri presenti (`FR-022`)
- [X] T033 [US5] Compila l'elenco degli **scostamenti** dal contratto approvato, ciascuno con la propria ragione; zero scostamenti è ammesso solo se le pagine coincidono con il contratto in ogni voce (`FR-023`, `F9`)
- [X] T034 [US5] Compila l'esito di ★1 (T011-T012) e di ★3 (T017), e lo stato dichiarato delle issue `#11` e `#18` con l'evidenza che manca per chiuderle (`FR-025`)
- [X] T035 [US5] Se e solo se T023 o T017 hanno prodotto un ritrovamento, scrivi la **nota in loco** su `docs/kpi_measures.md`: data, feature, valore precedente, valore corretto, causa, fonte verificabile — senza riscrivere il valore originale (`FR-024`)
- [X] T035a [US5] **Indipendentemente dall'esito di T017 e T023**, scrivi la **nota in loco** su `docs/kpi_measures.md` §3.4 e §7.1 con il testo DAX delle due misure companion di `CP-1`, verificato da T017: non è una correzione ma un'aggiunta, ed è dovuta perché quelle due sezioni sono gli unici punti del documento che dichiarano un valore senza il proprio blocco DAX mentre nel modello quel DAX ora esiste. Senza la nota il documento canonico esce silenziosamente fuori sincrono con il modello. **Estensione decisa il 2026-08-24 dopo T017**: la nota copre anche §11.1, dove le due soglie del quadrante figurano fra gli esclusi dal confronto contro il motore perché non leggibili come valori a sé stanti — `F7` le ha rese leggibili e T017 le ha lette, quindi quell'esclusione non è più vera. È lo stesso difetto di sincronia e va chiuso con lo stesso strumento
- [X] T036 [US5] Allinea `specs/008a-dashboard-model-pages/contracts/dashboard-contract.md` all'esito reale: che cosa `008b` e `010` possono presupporre su ciò che **esiste**, non su ciò che era stato disegnato
- [X] T037 [US5] Esegui le dodici prove di [quickstart.md](./quickstart.md) in blocco, incluso `python3 scripts/check_audit_coherence.py`, e registra l'esito

**Checkpoint**: il deliverable è documentato. La feature è pronta per la revisione.

---

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T038 Prepara la copia isolata per la revisione in contesto pulito: `contracts/page-contract.md` e la sezione «Esito della costruzione» di `quickstart.md`, **senza** spec, piano, task né history — è l'unica configurazione in cui la revisione dice qualcosa (`CLAUDE.md`)
- [X] T039 Raccogli il verbale in `specs/008a-dashboard-model-pages/review.md` e **committalo prima di toccare l'artefatto revisionato**: dichiarazione di che cosa è stato letto e cosa no, ancoraggio alla versione revisionata (commit e impronta), rilievi (`FR-027`, i quattro obblighi di `CLAUDE.md`)
- [X] T040 Chiudi i soli rilievi **strettamente necessari** — il documento afferma il falso o pubblica un valore che non regge — e rinvia gli altri come issue GitHub con numero; aggiungi in coda al verbale il blocco di chiusura che distingue *risolto*, *indebolito* e *rinviato*
- [X] T041 [P] Allinea `README.md`: riga di stato della `008a` — al 2026-08-25 «costruita, in revisione», da portare a «revisionata» con il link al verbale **dopo T040**, perché il README non asserisca una revisione che non esiste, deliverable elencato (il `.pbix` non versionato, con il rinvio a contratto ed esito che lo rendono ispezionabile), `Setup` e `Struttura` allineati se qualcosa cambia nel modo di rigenerare o verificare il progetto (`FR-026`)
- [X] T042 Riesegui `python3 scripts/check_audit_coherence.py` dopo le correzioni di T040 e T041, e riporta: contratto approvato, esito con gli scostamenti, stato di `#11` e `#18`, rilievi chiusi e rinviati, esito del controllo

---

## Dependencies & Execution Order

```text
Fase 1 (T001-T002)
   └─> Fase 2 (T003-T009) ──> T010 ⏸ PUNTO DI FERMATA 3
                                   └─> Fase 3 (T011-T012) ★1 tipizzazione
                                          └─> Fase 4 (T013-T023) costruzione
                                                 └─> Fase 5 (T024-T027) pagina BQ2
                                                        └─> Fase 6 (T028-T031) verifica interazioni
                                                               └─> Fase 7 (T032-T037) esito
                                                                      └─> Fase 8 (T038-T042) revisione e chiusura
```

**L'ordine è quasi interamente sequenziale, e non è un difetto della scomposizione**: un solo file di contratto, un solo `.pbix`, un solo esito. Le uniche coppie davvero parallelizzabili sono T041 (README) rispetto a T040 (chiusura dei rilievi), che toccano file diversi.

**I tre vincoli d'ordine che non si negoziano**:

1. **T010 prima di T011.** Aprire Power BI prima dell'approvazione del contratto annulla il presidio;
2. **T011-T012 prima di T013.** Costruire sopra una tipizzazione sbagliata è il costo che la `007b` ha già evitato una volta;
3. **T039 prima di T040.** Il verbale si committa prima che l'artefatto revisionato venga toccato — è l'omissione della `004`, e l'obbligo esiste perché è già accaduta.

## Implementation Strategy

**MVP**: le Fasi 1-4. A quel punto esistono quattro pagine, otto KPI etichettati e la navigazione: il deliverable è leggibile, benché la pagina `BQ2` non sia ancora completa e le verifiche di invarianza non siano state fatte.

**Il confine di sosta migliore, se la giornata si spezza, è T010.** È il punto in cui il repository è coerente per costruzione: esistono spec, piano, task e contratto, e non esiste ancora nulla che possa contraddirli. Ogni altro confine cade in mezzo alla costruzione, dove metà delle pagine esistono e l'esito non è scrivibile.

**Che cosa fare se la costruzione si scosta dal contratto**: annotare lo scostamento **mentre accade**, dentro la Fase 4 o 5, non ricostruirlo a memoria nella Fase 7. È il secondo rischio dichiarato dal piano, e l'unico presidio contro di esso è l'abitudine di chi costruisce.

---

## Avanzamento

Tracciamento di comodo, non una fonte: la misura autorevole del tempo speso sono i timestamp dei commit, ed è su quelli che la regia misura lo scostamento dalle stime di [plan.md](./plan.md).

| Blocco | Task | Stato | Data |
|---|---|---|---|
| A — contratto di pagina | T001-T009 | chiuso | 2026-08-24 |
| ⏸ punto di fermata 3 | T010 | chiuso: contratto approvato, `CP-1`, `CP-2` e `CP-3` confermati | 2026-08-24 |
| ★1 — tipizzazione | T011-T012 | chiuso: difetto assente | 2026-08-24 |
| ★2 — costruzione, modello | T013-T017 | chiuso: un difetto di caricamento trovato e corretto | 2026-08-24 |
| ★2 — costruzione, pagine | T018-T031 | chiuso: quattro pagine costruite, interazioni verificate | 2026-08-24 / 2026-08-25 |
| B — esito | T032-T037 | chiuso | 2026-08-25 |
| C — note in loco | T035, T035a | chiuso: T035 non dovuto (zero ritrovamenti); T035a su §3.4, §7.1 e §11.1 | 2026-08-25 |
| D — contratto di lettura | T036 | chiuso: riallineato all'esito | 2026-08-25 |
| E — revisione | T038-T040 | chiuso: 25 rilievi, 8 risolti, 17 rinviati a #22-#25 | 2026-08-25 |
| F — chiusura | T041-T042 | chiuso | 2026-08-25 |

**Le voci di esito già compilate** stanno nella sezione «Esito della costruzione» di [quickstart.md](./quickstart.md), ciascuna con la propria data.
