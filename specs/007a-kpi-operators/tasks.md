---

description: "Task list template for feature implementation"
---

# Tasks: Operatori delle misure

**Input**: Documenti di progettazione da `/specs/007a-kpi-operators/`

**Prerequisiti**: plan.md, spec.md, research.md, data-model.md, contracts/kpi-operators-contract.md, quickstart.md — tutti presenti.

**Test**: nessun task di test in senso software. Il deliverable è un documento; la sua correttezza si verifica con le dieci prove di [quickstart.md](./quickstart.md), incorporate come task T017.

**Perché un solo file domina questa lista**: a differenza di una feature software, la maggior parte delle diciannove attività (T001, T003-T011, T015) scrive o corregge lo stesso file, `docs/kpi_operators.md`. La marcatura `[P]` segue comunque la regola del template — file diversi, nessuna dipendenza — e per questo motivo compare solo dove due task toccano file davvero distinti (script, `convenzioni-marcatura.md`, `README.md`); i task che condividono `docs/kpi_operators.md` sono sequenziali per costruzione, non per scelta.

## Path Conventions

Repository singolo. Deliverable in `docs/kpi_operators.md`; modifiche di supporto in `scripts/check_audit_coherence.py`, `docs/convenzioni-marcatura.md`, `README.md`; verbale in `specs/007a-kpi-operators/review.md`.

---

## Phase 1: Setup

**Purpose**: predisporre lo scheletro del documento su cui le fasi successive scrivono.

- [ ] T001 Crea `docs/kpi_operators.md` con intestazione (titolo, data, stato), il paragrafo introduttivo che dichiara il perimetro (nessun valore dei KPI, solo operatori) e le otto intestazioni di sezione vuote, una per KPI, nell'ordine `BQ1-K1`, `BQ1-K2`, `BQ1-K3`, `BQ2-K1`, `BQ2-K2`, `BQ2-K3`, `BQ3-K1`, `BQ3-K2`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: il terzo punto di stop del flusso, specifico di questa feature — dichiarato dal prompt di consegna come il punto di massima leva.

**⚠️ CRITICAL**: nessuna sezione del documento si scrive prima che questo task sia riportato.

- [ ] T002 Riporta in forma compatta le quattro decisioni più esposte (D1 intervallo occupato, D2 metrica di distanza, D3 pesi e commensurabilità, D4 quadranti contro combinazione pesata) con la propria ragione, verificando che nulla sia cambiato rispetto alla spec approvata dalla regia; il riporto è testuale, non un file — punto di stop ★ di [plan.md](./plan.md)

**Checkpoint**: dopo T002, la scrittura del documento può iniziare.

---

## Phase 3: User Story 1 - Le quattro decisioni più esposte sono argomentate prima che il documento esista (Priority: P1) 🎯

**Goal**: le sezioni `BQ1-K3`, `BQ2-K2`, `BQ2-K3` di `docs/kpi_operators.md` contengono gli operatori di D1-D4 per intero, ciascuno con opzione scartata e ragione.

**Independent Test**: prova 3 di [quickstart.md](./quickstart.md) — D1-D4 citano almeno un'opzione scartata con la ragione dello scarto.

### Implementation for User Story 1

- [ ] T003 [US1] Scrivi la sezione `BQ1-K3` in `docs/kpi_operators.md`: operatore D1 (prodotto cartesiano dei tre intervalli scalari indipendenti, FR-001), il limite dichiarato della stima per eccesso (FR-002), provenienza da `docs/data_model.md` §11 (FR-014)
- [ ] T004 [US1] Scrivi la sezione `BQ2-K2` in `docs/kpi_operators.md`: operatore D2 (distanza media assoluta per asse, complemento a 1, FR-003), citazione del vincolo di `docs/content_taxonomy_bridge.md` §7 senza ripeterlo per esteso (FR-004), provenienza da `docs/data_model.md` §11
- [ ] T005 [US1] Scrivi la sezione `BQ2-K3` in `docs/kpi_operators.md`: operatore D3 (normalizzazione per divisione, pesi 0,5/0,5, FR-005) e operatore D4 (appartenenza al quadrante booleana più punteggio pesato continuo, con ruolo distinto, FR-006), dichiarazione che il quadrante verifica direttamente C3 della North Star (FR-007)

**Checkpoint**: le tre sezioni più esposte esistono e sono verificabili con la prova 3.

---

## Phase 4: User Story 2 - L'operatore di `BQ1-K1` copre anche C1, non solo la quota (Priority: P1)

**Goal**: la sezione `BQ1-K1` distingue l'operatore della quota da quello di C1 e argomenta l'invariante sul dato trasformato.

**Independent Test**: prove 4 e 5 di [quickstart.md](./quickstart.md).

### Implementation for User Story 2

- [ ] T006 [US2] Scrivi la sezione `BQ1-K1` in `docs/kpi_operators.md`: D9.1 (invariante sul numeratore 375, argomentato citando `NF.shape.rows`, `CL.NF.titles.rows.after`, `CL.NF.duration.repaired.rows`, FR-013a), D9.2 (operatore di C1 — conteggio per categoria su `bridge_title_category` raggruppato, soglia mediana stretta, FR-013b), D9.3 (il rapporto 375/8.807 resta non pubblicato finché non è calcolato e ancorato, FR-013)

**Checkpoint**: `BQ1-K1` è completa e i tre identificativi dell'invariante sono citati esattamente.

---

## Phase 5: User Story 3 - Ogni operatore dichiara provenienza e non altera la confidenza già fissata (Priority: P1)

**Goal**: le restanti sezioni sono scritte — inclusa `BQ2-K1`, la sesta con operatore nuovo, anticipata qui da User Story 4 perché senza di essa il documento avrebbe solo sette KPI su otto e la verifica di confidenza non potrebbe coprirli tutti (correzione B2 della revisione della regia) — e l'intero documento è verificato contro la confidenza di `business_case.md` §5.4.

**Independent Test**: prova 6 di [quickstart.md](./quickstart.md).

### Implementation for User Story 3

- [ ] T007 [US3] Scrivi la sezione `BQ1-K2` in `docs/kpi_operators.md`: operatore D5 (`format_duration_gap` = musica meno video, segno pubblicato, FR-008), dichiarazione che il KPI non ha direzione normativa e il segno è solo aritmetico (FR-009), provenienza
- [ ] T008 [US3] Scrivi le sezioni `BQ3-K1` e `BQ3-K2` in `docs/kpi_operators.md` dichiarando esplicitamente che sono già derivate per intero dalla feature `004`, nessun operatore nuovo qui, solo richiamo della confidenza bassa già fissata
- [ ] T009 [US4] Scrivi la sezione `BQ2-K1` in `docs/kpi_operators.md`: operatore (mediana di popolarità), D6 citato come esempio di soglia limitata al confronto delle quote di zeri (FR-010), D7 (obbligo di pubblicare la quota di popolarità zero e l'avvertimento dove `is_high_zero_genre = vero`, FR-011), dichiarazione del campione sbilanciato (17 conteggi distinti, minimo 904, `docs/data_model.md` §18) come fatto ereditato senza valutazione (FR-017) — anticipata qui, prima di T010, perché è l'ottava sezione mancante
- [ ] T010 [US3] Confronta la confidenza dichiarata per gli otto KPI in `docs/kpi_operators.md` con `docs/business_case.md` §5.4, riga per riga (FR-015); correggi ogni scostamento prima di procedere

**Checkpoint**: tutte e otto le sezioni esistono; nessuna confidenza diverge dal business case.

---

## Phase 6: User Story 4 - I vincoli ereditati condizionano l'operatore senza diventare un giudizio (Priority: P2)

**Goal**: le sezioni di mood dichiarano i vincoli ereditati come fatto, non come valutazione. La prima metà di questa user story — il campione sbilanciato su `BQ2-K1` — è già chiusa da T009 in Phase 5; questa fase completa la seconda metà.

**Independent Test**: acceptance scenario di User Story 4 in spec.md — nessun aggettivo di entità non ancorato accanto al campione sbilanciato o all'ancoraggio solo agli estremi.

### Implementation for User Story 4

- [ ] T011 [US4] Rileggi le sezioni `BQ1-K3`, `BQ2-K2`, `BQ2-K3` scritte in T003-T005 e verifica che ciascuna dichiari che presuppone solo la stabilità degli assi e degli estremi ancorati di `dim_category_mood`, non dei valori delle celle, citando `CF-1` come motivo (FR-016); aggiungi la dichiarazione dove manca

**Checkpoint**: nessun operatore per segmento o per mood introduce un giudizio non ancorato.

---

## Phase 7: User Story 5 - Il documento è verificabile meccanicamente, non solo a lettura (Priority: P2)

**Goal**: `docs/kpi_operators.md` entra nel controllo di coerenza automatico sotto severità stretta.

**Independent Test**: prova 8 di [quickstart.md](./quickstart.md).

### Implementation for User Story 5

- [ ] T012 [P] [US5] Aggiungi `docs/kpi_operators.md` alla tupla `DOCUMENTS` di `scripts/check_audit_coherence.py`, sesta riga, severità stretta (`True`), sul modello della riga di `docs/data_model.md` (FR-020)
- [ ] T013 [P] [US5] Registra `docs/kpi_operators.md` nella tabella di Provenienza di `docs/convenzioni-marcatura.md`, con data e feature `007a` (FR-022)
- [ ] T014 [US5] Esegui `python3 scripts/check_audit_coherence.py` e correggi ogni numerale privo di ancora o di marcatore di non-misurato in `docs/kpi_operators.md`, finché l'esito è verde su tutti e sei i documenti (FR-021; dipende da T012)

**Checkpoint**: il controllo di coerenza passa in severità stretta.

---

## Phase 8: User Story 6 - La voce minore residua di `R13` è chiusa (Priority: P3)

**Goal**: la direzione della graduatoria di `BQ2-K3` è dichiarata esplicitamente.

**Independent Test**: acceptance scenario di User Story 6 in spec.md.

### Implementation for User Story 6

- [ ] T015 [US6] Verifica che la sezione `BQ2-K3` (T005) dichiari D8 — la posizione 1 è il segmento con il punteggio pesato più alto, ordinamento decrescente (FR-012); aggiungila se manca

**Checkpoint**: `R13` non ha più parti residue aperte su questo documento.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: gli obblighi trasversali del progetto che nessun automatismo esegue, e la chiusura della feature.

- [ ] T016 [P] Aggiorna `README.md`: riga nella tabella di stato con link a `specs/007a-kpi-operators/review.md`, deliverable elencato, la frase «i cinque documenti che pubblicano misure» estesa al sesto documento, commento del passo 5 di `Setup` allineato, sezione `Struttura` allineata (FR-023)
- [ ] T017 Esegui le dieci prove di [quickstart.md](./quickstart.md) per intero, in ordine, e correggi ogni scostamento trovato prima di procedere alla revisione
- [ ] T018 **Dispatch della revisione in contesto pulito**: il revisore riceve **solo** `docs/kpi_operators.md` — una copia in una cartella isolata fuori dal repository, non il resto di `docs/`, non `specs/`, non `git`, sul modello di `specs/005-data-model-design/review.md` — non chi ha scritto il documento nella stessa sessione. Il verbale che ne risulta produce `specs/007a-kpi-operators/review.md` secondo i quattro obblighi di `CLAUDE.md`: committato prima di correggere l'artefatto, dichiara in apertura cosa è stato letto e cosa no, àncora commit e impronta del contenuto letto, non si corregge (FR-024)
- [ ] T019 Chiudi i rilievi del verbale con un blocco in coda che dichiara per ciascuno l'esito — risolto, indebolito, respinto con prova, o rinviato — senza toccare il testo del revisore

**Checkpoint**: feature conclusa, repository coerente.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: nessuna dipendenza — T001 crea lo scheletro del documento.
- **Foundational (Phase 2)**: dipende da T001. T002 blocca ogni scrittura di contenuto (Phase 3 in poi) — è il punto di stop ★.
- **User Story 1-3 (Phase 3-5, tutte P1, con T009 di User Story 4 anticipato in Phase 5)**: dipendono da T002. Scrivono sezioni distinte dello stesso file, quindi procedono in sequenza (T003→T004→T005→T006→T007→T008→T009→T010), non in parallelo, per evitare conflitti sullo stesso documento.
- **User Story 4 (T009 in Phase 5, T011 in Phase 6, P2)**: T009 (scrittura di `BQ2-K1`) è anticipata in Phase 5, prima di T010, perché senza quella sezione il documento avrebbe solo sette KPI su otto e T010 non potrebbe verificarne la confidenza — è la correzione B2 della revisione della regia sulla versione precedente di questo file, che lasciava `BQ2-K1` in Phase 6, dopo la verifica di confidenza. T011 dipende da T003-T005.
- **User Story 5 (Phase 7, P2)**: dipende dal documento completo (dopo Phase 6), perché il controllo di coerenza scandisce l'intero file.
- **User Story 6 (Phase 8, P3)**: dipende da T005.
- **Polish (Phase 9)**: dipende dal completamento di tutte le fasi precedenti; T017-T019 sono strettamente sequenziali.

### Perché questa feature non ha una vera indipendenza fra user story

Il template presuppone che le user story tocchino componenti diverse e possano procedere in parallelo. Qui tutte tranne la 5 e parte della 9 scrivono nello stesso file: l'indipendenza è **logica** (ciascuna sezione è verificabile da sola, come dichiarano gli Independent Test) ma non **di esecuzione** — scriverle in parallelo produrrebbe conflitti di merge su un unico documento. L'ordine P1→P1→P1→P2→P2→P3 dato sopra è quasi sempre anche l'ordine di scrittura effettivo, con un'unica eccezione dichiarata: T009 (User Story 4, P2) anticipa in Phase 5 la scrittura di `BQ2-K1`, perché T010 (User Story 3, P1) non potrebbe verificare la confidenza degli otto KPI su un documento che ne contiene sette. La priorità ordina il rischio di ciò che si argomenta per primo, non necessariamente l'ordine fisico di scrittura quando la completezza del documento lo richiede prima.

### Parallel Opportunities

Le uniche parallelizzazioni reali della feature, perché toccano file diversi senza dipendenza reciproca:

- T012 (`scripts/check_audit_coherence.py`) e T013 (`docs/convenzioni-marcatura.md`) possono procedere insieme — entrambe dipendono solo dal documento completo (fine di Phase 6), non l'una dall'altra.
- T016 (`README.md`) può procedere in parallelo a T012/T013, per la stessa ragione.

Nessun'altra coppia di task è marcata `[P]`: ogni altro task scrive in `docs/kpi_operators.md` o dipende dal risultato del task precedente.

---

## Parallel Example: Phase 7 e README

```bash
# Una volta completata la Phase 6 (documento completo), questi tre task sono indipendenti:
Task: "Aggiungi docs/kpi_operators.md a DOCUMENTS in scripts/check_audit_coherence.py"
Task: "Registra docs/kpi_operators.md nella tabella di Provenienza di docs/convenzioni-marcatura.md"
Task: "Aggiorna README.md: tabella di stato, deliverable, frase sui documenti, Setup, Struttura"
```

---

## Implementation Strategy

### Perché non esiste un vero MVP

Il template propone tipicamente "User Story 1 come MVP". Qui non si applica: FR-019 richiede un operatore per **ciascuno** degli otto KPI prima che il documento si possa considerare pubblicato, e SC-001 lo verifica sull'insieme completo. Un documento con solo le sezioni di User Story 1 (D1-D4) non è un incremento consegnabile — è un documento incompleto che lascerebbe `BQ1-K1`, `BQ1-K2`, `BQ2-K1` senza operatore, violando esattamente il perimetro che questa feature esiste per chiudere. Le priorità P1/P2/P3 delle user story ordinano **il rischio di ciò che si scrive per primo** (le decisioni più esposte, argomentate quando l'attenzione è più fresca), non un confine di consegna parziale.

### Ordine di lavoro effettivo

1. T001-T002: scheletro del documento, punto di stop ★.
2. T003-T007: le cinque sezioni dei KPI di `BQ1`/`BQ2` con operatore nuovo argomentate per prime — `BQ1-K3`, `BQ2-K2`, `BQ2-K3` (US1), `BQ1-K1` (US2), `BQ1-K2` (US3) — nell'ordine di esposizione al rischio.
3. T008: le due sezioni già chiuse dalla `004` (`BQ3-K1`, `BQ3-K2`), senza operatore nuovo.
4. T009: la sesta sezione con operatore nuovo, `BQ2-K1` — anticipata da User Story 4 perché completa le otto sezioni prima della verifica di confidenza.
5. T010: verifica di confidenza sulle otto sezioni, ora complete (US3).
6. T011: vincoli ereditati sulle sezioni di mood, seconda metà di User Story 4.
7. T012-T014 (US5, P2): il documento entra nel controllo di coerenza automatico.
8. T015 (US6, P3): chiusura della voce minore residua.
9. T016-T019 (Polish): README, quickstart per intero, dispatch della revisione in contesto pulito, chiusura dei suoi rilievi.

Il confine di sosta più sicuro, se la sessione si interrompe, è la fine della Phase 5 (T010): a quel punto tutte e otto le sezioni esistono e la confidenza è verificata contro il business case — resta aperta solo la dichiarazione dei vincoli di mood su sezioni già scritte (T011, Phase 6), che è un completamento dichiarativo, non ulteriore analisi.

---

## Notes

- `[P]` compare solo su T012, T013, T016 — le uniche coppie di task che toccano file distinti senza dipendenza reciproca.
- `[Story]` mappa ogni task alla propria user story per tracciabilità verso spec.md; Setup, Foundational e Polish non portano l'etichetta, come da convenzione del template.
- Nessun task di test in senso software: la verifica è affidata interamente a T017 (le dieci prove di quickstart.md) e alla revisione in contesto pulito (T018-T019).
- Propendere per commit dopo ogni fase (non dopo ogni task): la fase è l'unità di senso su un documento unico, il singolo task quasi mai lo è.
- `docs/roadmap.md` non compare in nessun task: appartiene alla regia (FR-026).
