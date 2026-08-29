---

description: "Task list template for feature implementation"
---

# Tasks: Il verdetto e la raccomandazione

**Input**: Documenti di progettazione da `/specs/009-verdetto-raccomandazione/`

**Prerequisiti**: plan.md, spec.md, research.md, data-model.md, contracts/document-contract.md, quickstart.md — tutti presenti.

**Test**: nessun task di test in senso software. La correttezza si verifica con le quattro prove di [quickstart.md](./quickstart.md) — incorporate come T007, T017 e T018 — più la revisione in contesto pulito (T021-T023), che è la sola capace di leggere l'argomentazione.

**Come questa lista è fatta, e perché non somiglia a quella della `007b`.** Là il peso stava nello script; qui sta nella prosa. La Fase Foundational è breve — una funzione, sei voci — e le Fasi 3-5 scrivono per intero `docs/raccomandazione.md`, una sezione per volta, ciascuna vincolata dal proprio obbligo del contratto. La marcatura `[P]` compare solo dove due task toccano file davvero distinti: i task che scrivono nel deliverable sono sequenziali per costruzione.

**Un vincolo di ordine che vale su tutta la lista**: nessuna sezione del documento si scrive prima che l'artefatto contenga i valori che quella sezione cita. Un'ancora che non risolve è un errore del controllo, e scrivere prosa attorno a un numero non ancora calcolato è il modo più efficiente di scoprirlo tardi.

## Path Conventions

Repository singolo. Script in `scripts/build_kpi_measures.py`; artefatto in `reports/kpi_measures.json`; deliverable in `docs/raccomandazione.md`; note in loco su `docs/kpi_operators.md` e `docs/kpi_measures.md`; modifiche di supporto in `scripts/check_audit_coherence.py`, `docs/convenzioni-marcatura.md`, `README.md`; verbale in `specs/009-verdetto-raccomandazione/review.md`.

---

## Phase 1: Setup

**Purpose**: fissare la decisione dell'operatore prima di calcolare qualunque cosa. È l'ordine che il progetto applica dalla `006` in poi — il criterio si scrive prima del valore — e qui è particolarmente semplice da rispettare, perché la decisione è già argomentata nella spec.

- [x] T001 Registra la decisione `D12` in `docs/kpi_operators.md`: riga nella tabella di §10 (che cosa fissa, da dove viene, dove è applicata) e **nota in loco** in coda a §12 che dichiara l'operatore di `C2` — soglia di maggioranza semplice `0,50`, confronto **stretto**, con la ragione della coerenza con `D9.2` e `D4` — senza riscrivere alcun testo preesistente (FR-001, FR-002, FR-003)
- [x] T002 Nella stessa nota di T001, dichiara che la scelta fra soglia stretta e larga **non cambia l'esito** di `C2` su questi dati, e — per il rilievo della regia — che il **margine** invece dalla soglia dipende: una soglia più severa lo restringerebbe (FR-004, decisione `V9` del piano)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: le sei voci nuove dell'artefatto. Nessuna sezione del deliverable si scrive prima che questa fase sia verde, perché ogni sezione cita un'ancora che deve già risolvere.

**⚠️ CRITICAL**: nessuna Fase 3+ inizia prima che T007 sia verde.

- [x] T003 In `scripts/build_kpi_measures.py`, modifica `build_bq1k3()` perché restituisca la quota di sovrapposizione come `Decimal` **esatto**, non arrotondato, e propaga il valore in `main()` — sullo schema di `build_segment_measures()`, che già restituisce due liste ai chiamanti (data-model.md §4)
- [x] T004 Implementa `build_decision_rule()` in `scripts/build_kpi_measures.py`: legge la quota esatta di T003 e i due booleani di `C1` e `C3` già in `values`, e scrive `KPI.BQ1K3.c2.threshold`, `.c2.satisfied`, `.c2.margin`, `.c2.margin_share_of_value` con etichette e unità secondo le convenzioni già in uso (FR-005)
- [x] T005 Nella stessa funzione, scrivi `KPI.verdict.conditions_satisfied` e `KPI.verdict.all_satisfied` — il conteggio delle condizioni soddisfatte e la congiunzione dei tre booleani, ciascuno con identificativo proprio perché sono affermazioni derivate (FR-006, `D5`)
- [x] T006 Aggiungi le due guardie di data-model.md §5: arresto esplicito con `halt()` se una delle tre condizioni manca da `values` quando il verdetto si calcola, e se `all_satisfied` e `conditions_satisfied` risultassero incoerenti fra loro; aggiungi la convenzione `kpi_decision_rule` all'artefatto, che dichiara soglia, strettezza, provenienza della regola, ereditarietà della confidenza e dipendenza dalla versione della tabella dei mood (FR-009)
- [x] T007 Esegui `python3 scripts/build_kpi_measures.py` due volte e verifica: le sei voci esistono, la convenzione esiste, le due impronte `sha256` coincidono, e `git diff reports/kpi_measures.json` mostra **solo righe aggiunte** — un valore preesistente che si muove è un ritrovamento da dichiarare, non un aggiornamento da accettare (FR-008, FR-010, quickstart §1 e §2)

---

## Phase 3: US1 + US2 — la risposta e il perché (Priority: P1)

**Story Goal**: un decisore che non ha letto nulla trova in apertura la risposta, e subito sotto le tre condizioni che la sostengono — tutte e tre, nella stessa forma, con la confidenza del verdetto argomentata.

**Independent Test**: si consegna il solo documento, fermo a queste due sezioni, e si verifica che un lettore sappia qual è la risposta, con quale cautela va presa, e su che cosa poggia.

- [x] T008 [US1] Crea `docs/raccomandazione.md` con l'intestazione e il blocco di apertura: che cosa è il documento, a chi si rivolge, dove vivono i documenti che lo sostengono — un rimando per **approfondire**, mai per completare (`V-7.5`, `V-D2`)
- [x] T009 [US1] Scrivi la sezione **«la risposta»** in `docs/raccomandazione.md`: la risposta come frase nella prima riga, l'esito ancorato al verdetto, la lettura corrispondente di `business_case.md` §3, e la cautela nella formulazione già pubblicata — non dice che l'espansione sarà redditizia, dice che sarebbe coerente (FR-011, FR-012, obblighi `V-1.1`-`V-1.4`)
- [x] T010 [US2] Scrivi la sezione **«perché»** in `docs/raccomandazione.md`: le tre condizioni, ciascuna in italiano comprensibile prima che nella forma tecnica, ciascuna con esito ancorato e confidenza; `C2` compare come le due sorelle e non come un buco (FR-013, obblighi `V-2.1`, `V-2.2`, chiude il rilievo `R2` della `008b`)
- [x] T011 [US2] Nella stessa sezione, dichiara la confidenza del verdetto — **media** — con l'argomento dell'ereditarietà dal termine più debole, e nomina `C2` come la più debole delle tre con la ragione (obblighi `V-2.3`, `V-2.4`, decisione `V5`)
- [x] T012 [US2] Nella stessa sezione, pubblica il **margine di robustezza** in entrambe le forme ancorate, con la frase che rende impossibili le due letture sbagliate: che sia una stima dell'errore, e che sia indipendente dalla soglia (obbligo `V-2.5`, decisioni `V3` e `V9`)

---

## Phase 4: US4 + US5 — con che cosa entrare, quanto vale, le assunzioni (Priority: P2)

**Story Goal**: le due sezioni operative del documento, ciascuna vincolata dai limiti che i suoi numeri portano con sé.

**Independent Test**: si verifica che nessuno scenario di `BQ3` compaia isolato, che l'orizzonte sia nella sezione dei valori, e che i segmenti non siano presentati come alternative disgiunte.

- [x] T013 [US4] Scrivi la sezione **«con che cosa entrare»** in `docs/raccomandazione.md`: la regione del catalogo caratterizzata dai segmenti del quadrante, con numerosità e posizione del candidato di punta **ancorate**; la dichiarazione che i segmenti si sovrappongono, non si sommano, e che contare le righe misura il campionamento e non il mercato (FR-014, FR-016, obblighi `V-3.1`-`V-3.3`)
- [x] T014 [US4] Nella stessa sezione, applica il vincolo sui 7 segmenti a domanda non misurata dalla fonte: nessuna lettura della coda della graduatoria senza l'esclusione dichiarata, e dove i 7 sono nominati si dice **non misurata dalla fonte**, mai «domanda bassa» (FR-015, obblighi `V-3.4`, `V-3.5`)
- [x] T015 [US4] Scrivi la sezione **«quanto vale»** in `docs/raccomandazione.md`: i due KPI di `BQ3` come terna pessimista/centrale/ottimista — mai un valore isolato, nemmeno in una frase di sintesi — l'orizzonte di 12 mesi scritto **qui** e non per rimando, il tasso dichiarato lordo, l'uplift dichiarato livello mensile a regime (FR-017, obblighi `V-4.1`-`V-4.4`)
- [x] T016 [US4] Nella stessa sezione, scrivi la **tabella di sensibilità**: per ciascuna base di riferimento tutti e tre gli scenari, le basi marcate con il marcatore di non-misurato e dichiarate in prosa come illustrazione parametrica di chi legge; usa la formulazione stretta di `bq3_scenarios.md` §8 e **non** «non è scalabile» (FR-018, obblighi `V-4.5`, `V-4.6`, decisione `V8`)
- [x] T017 [US4] Nella stessa sezione, dichiara **aperto** il debito della `004` sulla verificabilità del benchmark e nomina l'assunzione di trasferimento `A6` dove i numeri di `BQ3` compaiono (FR-019, obblighi `V-4.7`, `V-4.8`)
- [x] T018 [US5] Scrivi la sezione su **`A1` e `A6`** in `docs/raccomandazione.md`: le due assunzioni di trasferimento restano fuori dalla scala di confidenza per costruzione, in forma estesa e non in nota — è il punto in cui devono sopravvivere all'estrazione di una singola frase (FR-021, obbligo `V-6.2`)

---

## Phase 5: US1 — che cosa lo farebbe cambiare, che cosa non è (Priority: P1)

**Story Goal**: le due sezioni che distinguono una raccomandazione da un'opinione.

**⚠️ Nessuna di queste due sezioni si comprime.** Se il lavoro sfora, si riporta lo sforamento: la prima è la sola parte che distingue questo documento da un riassunto dei precedenti (spec, «Stima e scomposizione»).

- [x] T019 [US1] Scrivi la sezione **«che cosa lo farebbe cambiare»** in `docs/raccomandazione.md`, con almeno le quattro condizioni del contratto — revisione della tabella dei mood, sovrastima maggiore del margine, fallimento dell'assunzione di trasferimento, arrivo di dati che il progetto non ha — ciascuna che dichiara **che cosa succederebbe** e non solo che è un rischio (FR-020, obblighi `V-5.1`-`V-5.5`)
- [x] T020 [US1] Scrivi la sezione **«che cosa questa raccomandazione non è»** in `docs/raccomandazione.md`: non è un business case finanziario, non descrive StreamWave, non dice che il pubblico attuale vorrebbe la musica, non è una previsione, e i dati si fermano al 2021-2022 con il benchmark al 2018 (obblighi `V-6.1`, `V-6.3`-`V-6.5`)

---

## Phase 6: il repository resta coerente (US6, Priority: P2)

**Story Goal**: il controllo copre l'ottavo documento, la grammatica registra la riga, il README non presenta drift.

- [x] T021 Aggiungi `docs/raccomandazione.md` a `DOCUMENTS` in `scripts/check_audit_coherence.py` sotto severità stretta, come ottavo documento verificato e settimo sotto quel regime (FR-023)
- [x] T022 Esegui `python3 scripts/check_audit_coherence.py` e chiudi ogni segnalazione sul deliverable: ogni numerale in posizione di fatto misurato porta l'ancora o il marcatore, nessun numerale in lettere per un fatto misurato, nessun numero derivabile scritto a mano (FR-024, FR-026, obblighi `V-7.1`-`V-7.3`)
- [x] T023 [P] Aggiungi a `docs/convenzioni-marcatura.md` la riga di `docs/raccomandazione.md` nella tabella di severità di §5 e la riga di provenienza della feature `009` in coda alla tabella finale, con data e feature (FR-025)
- [x] T024 [P] Aggiungi a `docs/kpi_measures.md` una **nota di aggiunta** che dichiara dove `C2` vive ora e che la regola di decisione è leggibile per intero — chiude la parte residua della issue `#17`, che rilevava che `C2` non è mai nominata in quel documento
- [x] T025 [P] Aggiorna `README.md`: riga nella tabella di stato con link al verbale, deliverable elencato, prosa dei deliverable estesa al documento nuovo, `Setup` e `Struttura` allineati, conteggio dei documenti verificati aggiornato da sette a otto. Il passaggio «Il file è leggibile, non pubblicabile» e il capoverso che lo segue **non si toccano** (FR-027)
- [x] T026 Rileggi il deliverable finito contro `contracts/document-contract.md`, obbligo per obbligo, e verifica che nessuna sezione manchi invece di essere solo breve — è la verifica che il contratto esiste per rendere possibile

---

## Phase 7: revisione in contesto pulito e chiusura

**⚠️ L'ordine di questa fase è il presidio, e non è negoziabile**: il verbale si scrive e si committa **prima** di toccare il deliverable (obbligo 1 di `CLAUDE.md`).

- [ ] T027 Componi il perimetro della revisione secondo quickstart §4: il deliverable, più le copie autorevoli censite in research.md `R-3`, perché una revisione su estratti isolati non può per costruzione vedere che un'affermazione esiste in due copie divergenti (FR-029)
- [ ] T028 Esegui la revisione in contesto pulito su `docs/raccomandazione.md` e produci `specs/009-verdetto-raccomandazione/review.md`: dichiara in apertura che cosa è stato letto e che cosa no, incluse le uscite dal perimetro; ancora commit e impronta del contenuto letto (FR-028, obblighi 2 e 3 di `CLAUDE.md`)
- [ ] T029 **Proponi il commit del verbale prima di qualunque correzione** al deliverable (obbligo 1 di `CLAUDE.md`, FR-028)
- [ ] T030 Chiudi i **soli** rilievi strettamente necessari — quelli senza cui il deliverable afferma il falso o pubblica un valore che non regge — e apri una issue sul tracker per ciascuno degli altri (FR-030, regola del 2026-08-22)
- [ ] T031 Apri la issue del ritrovamento di research.md `R-3`: `kpi_operators.md` §9 usa la formulazione «non è scalabile» che `bq3_scenarios.md` §8 dichiara falsa — è un ritrovamento di questa feature, non un rilievo di revisione, e non si corregge qui
- [ ] T032 Scrivi il **blocco di chiusura** in coda a `specs/009-verdetto-raccomandazione/review.md`, distinguendo per ciascun rilievo **risolto**, **indebolito** e **rinviato**, e nominando l'issue per ogni rinvio. Il testo del revisore non si tocca, nemmeno dove sbaglia (obbligo 4 di `CLAUDE.md`)
- [ ] T033 Riesegui `python3 scripts/check_audit_coherence.py` dopo le correzioni della revisione e verifica che resti verde
- [ ] T034 Proponi i commit finali, raccolti per gruppo di documenti; verifica che nessuna issue fra `#11`, `#18`, `#20`, `#21`, `#26`, `#27`, `#29`, `#30` sia stata chiusa da questa feature, e dichiara nell'esito lo stato di ciascuna (FR-031, FR-032)

---

## Dipendenze

```
T001-T002  (la decisione, prima di tutto)
    ↓
T003 → T004 → T005 → T006 → T007   (l'artefatto; T007 è il gate)
    ↓
T008 → T009 → T010 → T011 → T012   (US1+US2: risposta e perché)
    ↓
T013 → T014 → T015 → T016 → T017 → T018   (US4+US5: entrare, quanto vale, assunzioni)
    ↓
T019 → T020                         (US1: cambiamento e limiti)
    ↓
T021 → T022                         (il controllo copre il documento)
    ↓
T023 [P] · T024 [P] · T025 [P]     (tre file distinti, in parallelo)
    ↓
T026                                (rilettura contro il contratto)
    ↓
T027 → T028 → T029 → T030 → T031 → T032 → T033 → T034
```

**Perché così poche `[P]`.** Dodici dei trentaquattro task scrivono nello stesso file, `docs/raccomandazione.md`, e sei nello stesso script. La regola del template — file diversi, nessuna dipendenza — le esclude. Le tre parallele di T023-T025 toccano tre file distinti e nessuna dipende dalle altre.

**Il gate reale della lista è T007.** Sopra di esso c'è aritmetica; sotto, prosa che cita ancore. Scrivere prosa attorno a un numero non ancora calcolato è il modo più efficiente di scoprire tardi che un'ancora non risolve.

---

## Strategia di consegna

**Il minimo che ha valore** è la Fase 3: la risposta e il perché. Un documento che si fermasse lì risponderebbe alla domanda per cui il progetto esiste, e sarebbe già più di quanto nove feature hanno prodotto. Non è però il deliverable: senza «che cosa lo farebbe cambiare» resterebbe un'opinione ben ancorata.

**L'ordine è per costruzione incrementale**: ogni fase lascia il documento in uno stato leggibile, e il repository in uno stato coerente — che è il vincolo del principio III alla fine di ogni sessione, non solo alla chiusura della feature.

**Dove il lavoro può sforare, e che cosa fare**: la Fase 4 è la più lunga, perché la sezione «quanto vale» porta sei vincoli ereditati e una tabella. Se sfora, si riporta. **La Fase 5 non si comprime**, ed è dichiarato in tre punti — spec, contratto, e qui — perché è la prima cosa che una sessione sotto pressione taglierebbe.
