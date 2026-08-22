---

description: "Task list template for feature implementation"
---

# Tasks: Misure DAX e documento dei KPI

**Input**: Documenti di progettazione da `/specs/007b-kpi-measures/`

**Prerequisiti**: plan.md, spec.md, research.md, data-model.md, contracts/kpi-measures-contract.md, quickstart.md — tutti presenti.

**Test**: nessun task di test in senso software separato dal deliverable. La correttezza si verifica con le dodici prove di [quickstart.md](./quickstart.md), incorporate come task T038, più la revisione in contesto pulito (T039-T040) e la riesecuzione del controllo di coerenza dopo le sue correzioni (T040a).

**Perché due soli file dominano questa lista**: la Fase Foundational scrive per intero `scripts/build_kpi_measures.py`; le Fasi 3-6 scrivono per intero `docs/kpi_measures.md`. La marcatura `[P]` segue la regola del template — file diversi, nessuna dipendenza — e per questo compare solo dove due task toccano file davvero distinti (l'estensione dello script di controllo, `convenzioni-marcatura.md`, `README.md`); i task che condividono uno dei due file principali sono sequenziali per costruzione.

## Path Conventions

Repository singolo. Script in `scripts/build_kpi_measures.py`; artefatto in `reports/kpi_measures.json`; documento pubblicato in `docs/kpi_measures.md`; modifiche a documenti già mergiati in `docs/kpi_operators.md` e `docs/business_case.md`; modifiche di supporto in `scripts/check_audit_coherence.py`, `docs/convenzioni-marcatura.md`, `README.md`; verbale in `specs/007b-kpi-measures/review.md`.

---

## Phase 1: Setup

**Purpose**: lo scheletro dello script su cui la Fase Foundational scrive la logica di calcolo.

- [X] T001 Crea `scripts/build_kpi_measures.py` con: percorsi di ingresso/uscita (`data/processed/*.csv`, `data/curated/dim_category_mood.json`, `reports/bq3_scenarios.json` → `reports/kpi_measures.json`), `SCHEMA_VERSION`, gli helper di arrotondamento per unità di misura (E5: quote a 4 cifre, minuti a 2, indice di popolarità a 1, `ROUND_HALF_UP` esplicito), `display_of()` senza dipendenza dal locale e `fingerprint()` — sullo schema di `scripts/build_bq3_scenarios.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: il nucleo di calcolo dello script. Nessuna sezione di `docs/kpi_measures.md` si scrive prima che l'artefatto esista con valori reali, perché ogni sezione del documento cita un'ancora che deve già risolvere a qualcosa.

**⚠️ CRITICAL**: nessuna Fase 3+ inizia prima che T013 sia verde.

- [X] T002 Implementa in `scripts/build_kpi_measures.py` la lettura dei cinque file di ingresso e la guardia di FR-004: l'insieme delle categorie lette dal ponte titolo-categoria coincide con le 42 attese, l'insieme dei segmenti letti da `spotify_track_genre.csv` coincide con i 114 attesi; arresto esplicito senza scrivere alcun file su qualunque disuguaglianza o insieme vuoto
- [X] T003 Implementa la funzione di mediana condivisa in `scripts/build_kpi_measures.py`: ordinamento, media aritmetica dei due valori centrali su conteggio pari, nessuna eccezione per i pari merito (E2/D10) — usata da tutte le misure che seguono
- [X] T004 Implementa `music_adjacent_catalog_share` (`BQ1-K1`, FR-005): titoli distinti in `Music & Musicals` sul ponte trasformato diviso titoli distinti di `dim_title`; conteggio dei titoli per ciascuna delle 42 categorie e posizione di `Music & Musicals` rispetto alla mediana dei 42 conteggi (operatore C1, D9.2)
- [X] T005 Implementa la verifica dell'invarianza del numeratore della North Star (E7, FR-012): conteggio diretto dei titoli distinti in `Music & Musicals` su `netflix_title_category.csv`, confronto con `375` (`NF.cat.music_musicals.titles`), esito booleano pubblicato come valore proprio
- [X] T006 Implementa `format_duration_gap` (`BQ1-K2`, FR-006): mediana della durata musicale meno mediana della durata dei film, con segno; entrambe le varianti della mediana musicale — con e senza la riga `is_duration_zero` (E3) — e la loro differenza; quota di titoli `Movie` sul catalogo video (E4)
- [X] T007 Implementa `mood_profile_overlap` (`BQ1-K3`, FR-007): quota di tracce il cui profilo cade, su tutti e tre gli assi contemporaneamente (AND logico), dentro gli intervalli chiusi `[min, max]` delle 42 righe di `dim_category_mood`
- [X] T008 Implementa `segment_demand_index` (`BQ2-K1`, FR-008) per ciascuno dei 114 segmenti: mediana di popolarità sulle coppie traccia-segmento, quota di righe a popolarità zero dello stesso segmento, propagazione del flag `is_high_zero_genre`
- [X] T009 Implementa `segment_catalog_affinity` (`BQ2-K2`, FR-009) per ciascuno dei 114 segmenti: `1 − d`, con `d` media delle tre distanze assolute per asse fra il profilo mediano del segmento e il profilo mediano ponderato del catalogo video sulle 19.323 assegnazioni titolo-categoria
- [X] T010 Implementa `segment_entry_priority` (`BQ2-K3`, FR-010) per ciascuno dei 114 segmenti: domanda normalizzata, punteggio pesato 0,5/0,5, appartenenza al quadrante alta-domanda/alta-affinità (soglia mediana stretta), graduatoria per punteggio decrescente
- [X] T011 Implementa la citazione di `premium_tier_adoption_rate` e `arpu_uplift` (`BQ3-K1`/`BQ3-K2`, FR-011): lettura diretta da `reports/bq3_scenarios.json`, nessun ricalcolo, valori repubblicati con chiave e ancora proprie che puntano alla fonte
- [X] T012 Assembla e scrivi `reports/kpi_measures.json` in `scripts/build_kpi_measures.py`: blocchi `values`/`catalogs`/`conventions`/`sources` (schema di `data-model.md`), impronta `sha256` di ciascun file di ingresso, nessuna marca temporale di esecuzione (FR-001, FR-002)
- [X] T013 Esegui `python3 scripts/build_kpi_measures.py` due volte di seguito; verifica che il file prodotto sia identico byte per byte (FR-003, SC-002)

**Checkpoint**: `reports/kpi_measures.json` esiste, è deterministico, e ogni misura ha un valore reale su cui `docs/kpi_measures.md` può ancorare.

---

## Phase 3: User Story 1 - La pipeline intera, non solo lo script, rigenera tutti gli 8 valori in modo riproducibile (Priority: P1) 🎯

**Goal**: chi clona il repository può rigenerare `reports/kpi_measures.json` partendo solo da `data/raw/` e codice versionato, senza affidarsi a un'esecuzione manuale non tracciata.

**Independent Test**: prova 1 di [quickstart.md](./quickstart.md).

### Implementation for User Story 1

- [X] T014 [US1] Rigenera `data/processed/` da `data/raw/` con `python3 scripts/build_datasets.py`, poi esegui `python3 scripts/build_kpi_measures.py`; verifica che l'artefatto prodotto coincida con quello di T013 e ripeti la catena una seconda volta per confermare la riproducibilità end-to-end (FR-003 esteso alla pipeline intera, non al solo script)
- [X] T015 [US1] Scrivi l'introduzione di `docs/kpi_measures.md`: paragrafo di metodologia che dichiara la catena `data/raw/` → `build_datasets.py` → `build_kpi_measures.py` (E1), la tabella di arrotondamento per unità di misura (E5), e il rimando a `scripts/build_bq3_scenarios.py` come schema di riferimento

**Checkpoint**: la riproducibilità è verificata sull'intera catena, non solo sul nuovo script; il documento ha un'intestazione.

---

## Phase 4: User Story 2 - L'invarianza del numeratore della North Star si legge come verificata o come ritrovamento (Priority: P1)

**Goal**: la sezione `BQ1-K1` dichiara l'esito reale del confronto fra il conteggio sul trasformato e il 375 di origine, mai come assunzione taciuta.

**Independent Test**: prova 3 di [quickstart.md](./quickstart.md).

### Implementation for User Story 2

- [X] T016 [US2] Scrivi la sezione `BQ1-K1` di `docs/kpi_measures.md`: i due operatori distinti (quota e C1), il testo DAX trascritto per ciascuno, provenienza dal modello dati, confidenza alta ereditata
- [X] T017 [US2] Aggiungi alla sezione `BQ1-K1` la sottosezione dell'invarianza (E7, FR-013): entrambi i conteggi ancorati, l'esito esplicito — «verificata» se coincidono con 375, ritrovamento con nota in loco su `docs/kpi_operators.md` §2.1 se divergono

**Checkpoint**: `BQ1-K1` è completa e l'esito dell'invarianza non è mai lasciato dedurre da due numeri accostati.

---

## Phase 5: User Story 3 - Ogni misura sulla popolarità porta accanto la propria quota di zeri, con avvertimento dove dovuto (Priority: P1)

**Goal**: la sezione `BQ2-K1` pubblica, per ciascuno dei 114 segmenti, la mediana di popolarità e la quota di zeri; i 7 segmenti `is_high_zero_genre` portano un avvertimento esplicito.

**Independent Test**: prova 4 di [quickstart.md](./quickstart.md).

### Implementation for User Story 3

- [X] T018 [US3] Scrivi la sezione `BQ2-K1` di `docs/kpi_measures.md`: la tabella dei 114 segmenti (mediana di popolarità, quota di zeri), il testo DAX trascritto, provenienza, confidenza media
- [X] T019 [US3] Aggiungi l'avvertimento testuale esplicito accanto al valore di ciascuno dei 7 segmenti con `is_high_zero_genre` vero (D7, FR-008); verifica che gli altri 107 portino comunque la quota senza l'avvertimento

**Checkpoint**: `BQ2-K1` è completa e l'obbligo non negoziabile di D7 è rispettato su tutti e 114 i segmenti.

---

## Phase 6: User Story 7 - Ogni valore pubblicato dichiara se è stato verificato contro il motore reale (Priority: P1)

**Goal**: tutte e otto le sezioni di `docs/kpi_measures.md` esistono (le sei ancora mancanti si scrivono qui, perché senza di esse la dichiarazione di questa user story — «ciascuna delle otto misure» — non avrebbe un documento completo su cui operare) e ciascuna dichiara l'esito reale del confronto E9, mai uno stato anticipato.

**Independent Test**: prove 5 e 12 di [quickstart.md](./quickstart.md).

### Implementation for User Story 7

- [X] T020 [US7] Scrivi la sezione `BQ1-K2` di `docs/kpi_measures.md`: il gap con segno, le due varianti della mediana musicale e la loro differenza (E3), la quota di film sul catalogo video (E4), il testo DAX trascritto
- [X] T021 [US7] Scrivi la sezione `BQ1-K3` di `docs/kpi_measures.md`: `mood_profile_overlap`, il testo DAX trascritto, il limite ereditato della stima per eccesso (D1)
- [X] T022 [US7] Scrivi la sezione `BQ2-K2` di `docs/kpi_measures.md`: la tabella dei 114 segmenti (affinità), il testo DAX trascritto, il limite ereditato di non comparabilità assoluta (D2)
- [X] T023 [US7] Scrivi la sezione `BQ2-K3` di `docs/kpi_measures.md`: la tabella dei 114 segmenti (punteggio, quadrante booleano, graduatoria), il testo DAX trascritto
- [X] T024 [US7] Scrivi le sezioni `BQ3-K1` e `BQ3-K2` di `docs/kpi_measures.md`: citazione diretta da `reports/bq3_scenarios.json`, dichiarazione esplicita che non c'è alcun ricalcolo, range best/base/worst, confidenza bassa
- [X] T025 [US7] Aggiungi a ciascuna delle otto sezioni lo stato di verifica di default: «calcolato da `scripts/build_kpi_measures.py`, verifica contro il motore in corso» (FR-030) — nessuna sezione dichiara «verificato» prima di questo punto
- [X] T026 [US7] Dispatch di E9: prepara per Valerio l'elenco degli otto testi DAX trascritti pronti da incollare nel `.pbix` già materializzato, con accanto il valore atteso da `reports/kpi_measures.json` per ciascuno — passo esterno a questa sessione, non scriptabile (principio V)
- [X] T026a [US7] Congela `reports/kpi_engine_check.json` dall'esito che Valerio riporta in T026: le otto letture del motore, la data della lettura, il riferimento allo stato del `.pbix`, l'esito booleano del confronto con `reports/kpi_measures.json` e la differenza dove diverge — curato a mano, mai scritto da uno script (FR-029a). **Rilievo bloccante della revisione di regia sul piano**: senza questo artefatto l'esito di E9 non ha ancora, e `reports/kpi_measures.json` non può contenerlo perché è deterministico per FR-003
- [X] T027 [US7] Incorpora l'esito di T026a in ciascuna delle otto sezioni di `docs/kpi_measures.md`, ancorato a `reports/kpi_engine_check.json`: «verificato contro il motore reale» dove i valori coincidono, nota in loco con entrambi i numeri e la causa (se identificabile) dove divergono (FR-030, FR-031)

**Checkpoint**: il documento è completo su tutte e otto le misure, e nessuna dichiara uno stato di verifica che non corrisponde a un confronto realmente avvenuto.

---

## Phase 7: User Story 5 - Il documento e gli artefatti sono verificabili meccanicamente (Priority: P2)

**Goal**: `docs/kpi_measures.md`, `reports/kpi_measures.json` e `reports/kpi_engine_check.json` entrano nel controllo di coerenza automatico.

**Independent Test**: prova 7 di [quickstart.md](./quickstart.md).

### Implementation for User Story 5

- [X] T028 [P] [US5] Aggiungi `docs/kpi_measures.md` alla tupla `DOCUMENTS` di `scripts/check_audit_coherence.py`, settima riga, severità stretta (`True`) — sesto documento sotto quel regime, dato che `docs/data_audit.md` resta ad avvisi (FR-021)
- [X] T028a [US5] Registra `docs/kpi_measures.md` nella tabella di severità §5 e nella tabella di Provenienza di `docs/convenzioni-marcatura.md` (data, feature `007b`); nella stessa riga di Provenienza registra `reports/kpi_measures.json` (quinto artefatto) e `reports/kpi_engine_check.json` (sesto artefatto, FR-029a) (FR-024)
- [X] T029 [P] [US5] Aggiungi `reports/kpi_measures.json` (quinto membro) e `reports/kpi_engine_check.json` (sesto membro, FR-029a) alla tupla `ARTIFACTS` di `scripts/check_audit_coherence.py`; verifica l'assenza di collisioni di prefisso di chiave con `PROFILE`, `CLEANING`, `SCENARIOS`, `MOOD` e fra i due nuovi membri (FR-022, FR-029a)
- [X] T030 [US5] Esegui `python3 scripts/check_audit_coherence.py` e correggi ogni numerale privo di ancora o di marcatore di non-misurato in `docs/kpi_measures.md`, finché l'esito è verde su sette documenti e sei artefatti (dipende da T028, T029)

**Checkpoint**: il controllo di coerenza passa in severità stretta sul settimo documento e sul sesto artefatto.

---

## Phase 8: User Story 4 - I tre vincoli di `kpi_operators.md` §12 e le issue `#7`/`#8` si chiudono con dichiarazione esplicita (Priority: P2)

**Goal**: `docs/kpi_operators.md` §12 non ha più vincoli aperti relativi alla mediana, alla durata degenere, all'asimmetria e all'arrotondamento; le issue `#7` e `#8` sono pronte per la chiusura.

**Independent Test**: prove 6 di [quickstart.md](./quickstart.md).

### Implementation for User Story 4

- [X] T031 [US4] Aggiungi **D10** a `docs/kpi_operators.md` §10 e §12: la convenzione di mediana (E2), con riferimento a T003; chiude l'issue `#7` (FR-015)
- [X] T032 [US4] Aggiungi **D11** a `docs/kpi_operators.md` §3 e §12: la decisione sulla durata degenere (E3), con riferimento al valore comparativo prodotto da T006 (FR-016)
- [X] T033 [US4] Aggiungi la nota in loco a `docs/kpi_operators.md` §11 che corregge l'attribuzione di `D6` a `BQ2-K1` (E6): data, feature `007b`, causa (contraddizione con §5.3), valore corretto, testo precedente non cancellato; chiude l'issue `#8` (FR-018)
- [X] T034 [US4] Registra in `docs/kpi_operators.md` §12 la chiusura dei vincoli residui: l'asimmetria di `BQ1-K2` con riferimento a `docs/kpi_measures.md` (E4), l'arrotondamento con riferimento alla tabella di E5 (FR-017)
- [X] T035 [US4] Prepara la proposta di chiusura delle issue GitHub `#7` e `#8` con riferimento al commit che introduce D10/D11 e la nota in loco di §11 — l'esecuzione della chiusura su GitHub resta a Valerio (FR-027)

**Checkpoint**: §12 non ha più vincoli aperti; le due issue sono pronte per la chiusura formale.

---

## Phase 9: User Story 6 - La nota in loco su `business_case.md` §3 rende vera la descrizione della North Star (Priority: P2)

**Goal**: `business_case.md` §3 dichiara, accanto al testo originale, che la misura legge la sola etichetta `Music & Musicals`.

**Independent Test**: prova 9 di [quickstart.md](./quickstart.md).

### Implementation for User Story 6

- [X] T036 [US6] Aggiungi la nota in loco a `business_case.md` §3: data, feature `007b`, causa (rilievo R11 della revisione `001`, assegnato dalla decisione di regia del 2026-08-21), valore corretto (`Music & Musicals`, una sola etichetta); testo originale non cancellato (FR-019)

**Checkpoint**: §3 non afferma più, senza qualifica, una descrizione che il KPI pubblicato smentirebbe.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: gli obblighi trasversali del progetto che nessun automatismo esegue, e la chiusura della feature.

- [X] T037 [P] Aggiorna `README.md`: riga nella tabella di stato con link a `specs/007b-kpi-measures/review.md`, deliverable elencato, la frase sui documenti che pubblicano misure estesa all'ottavo documento, `Setup` e `Struttura` allineati, conteggio dei documenti sotto controllo di coerenza aggiornato da sei a sette (FR-025)
- [X] T038 Esegui le dodici prove di [quickstart.md](./quickstart.md) per intero, in ordine; correggi ogni scostamento trovato prima di procedere alla revisione (le prove 1-11 sono eseguibili subito, la prova 12 solo dopo che T027 ha incorporato l'esito reale di E9)
- [ ] T039 **Dispatch della revisione in contesto pulito**: il revisore riceve **solo** `docs/kpi_measures.md` — una copia in una cartella isolata fuori dal repository, non lo script, non l'artefatto JSON, non `specs/`, non `git` — sul modello di `specs/007a-kpi-operators/review.md`. Il verbale produce `specs/007b-kpi-measures/review.md` secondo i quattro obblighi di `CLAUDE.md`: committato prima di correggere il documento, dichiara in apertura cosa è stato letto e cosa no, àncora commit e impronta del contenuto letto, non si corregge (FR-026)
- [ ] T040 Chiudi i rilievi del verbale con un blocco in coda che distingue, per ciascuno, risolto/indebolito/rinviato — solo i rilievi strettamente necessari si correggono in questa feature (il documento, senza quella correzione, afferma il falso o pubblica un valore che non regge); ogni rinvio nomina l'issue GitHub aperta per esso
- [ ] T040a Riesegui `python3 scripts/check_audit_coherence.py` dopo le correzioni di T040; le correzioni possono toccare numeri e ancore, e l'ultimo esito verde precedente è a T030, sei task prima — correggi ogni nuova ancora rotta prima di considerare la feature conclusa

**Checkpoint**: feature conclusa, repository coerente, `README.md` senza drift, controllo di coerenza verde riconfermato dopo le correzioni.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: nessuna dipendenza — T001 crea lo scheletro dello script.
- **Foundational (Phase 2)**: dipende da T001. T002-T013 sono strettamente sequenziali all'interno dello stesso file (`scripts/build_kpi_measures.py`) e bloccano ogni scrittura di `docs/kpi_measures.md`.
- **User Story 1 (Phase 3, P1)**: dipende da T013 (l'artefatto esiste ed è deterministico). T014 verifica la catena intera; T015 apre il documento.
- **User Story 2 (Phase 4, P1)**: dipende da T015 (documento aperto) e da T004/T005 (valori di `BQ1-K1` ed esito dell'invarianza già calcolati).
- **User Story 3 (Phase 5, P1)**: dipende da T015 e da T008. Nessuna dipendenza da Phase 4 — le due sezioni sono indipendenti nel contenuto, ma condividono il file e procedono in sequenza per evitare conflitti.
- **User Story 7 (Phase 6, P1, con le sei sezioni residue anticipate qui)**: dipende da T016-T019 (il documento deve avere già `BQ1-K1` e `BQ2-K1` prima che T025 possa dichiarare lo stato di default su «ciascuna delle otto» sezioni). T026 dipende dal documento completo (T020-T025); **T026a dipende dall'esito esterno di T026**, che questa sessione non può produrre da sola, ed è il task che congela `reports/kpi_engine_check.json` (rilievo bloccante della revisione di regia sul piano: senza di esso T027 scriverebbe un numero privo di ancora); T027 dipende da T026a, non direttamente da T026.
- **User Story 5 (Phase 7, P2)**: dipende dal documento completo (fine di Phase 6, T027 incluso — T029 aggiunge anche `reports/kpi_engine_check.json`, che T026a deve già aver scritto).
- **User Story 4 (Phase 8, P2)**: dipende da T003 (D10 cita la funzione di mediana) e T006 (D11 cita il valore comparativo). Nessuna dipendenza dal documento pubblicato.
- **User Story 6 (Phase 9, P2)**: nessuna dipendenza da alcun'altra fase — può procedere in qualunque momento dopo l'apertura della spec.
- **Polish (Phase 10)**: T037 dipende dal completamento delle Phase 3-9 (per sapere cosa il README deve riflettere). T038 dipende da tutte le fasi precedenti. T039-T040-T040a sono strettamente sequenziali e dipendono da T038 — T040a non è opzionale: le correzioni di T040 possono toccare numeri e ancore, e senza rieseguire il controllo l'ultimo esito verde resterebbe quello di T030, sei task prima.

### Perché questa feature non ha una vera indipendenza fra user story, come già la `007a`

Le user story P1 (1, 2, 3, 7) scrivono tutte nello stesso documento (`docs/kpi_measures.md`) e la Foundational scrive per intero lo stesso script: l'indipendenza dichiarata dagli Independent Test è **logica** (ciascuna sezione è verificabile da sola), non **di esecuzione**. L'unica vera anticipazione, sullo stesso modello della `007a` (che anticipò `BQ2-K1` nella Phase 5 per completare il documento prima della verifica di confidenza), è qui: **Phase 6 (User Story 7) scrive le sei sezioni che nessun'altra user story nomina** (`BQ1-K2`, `BQ1-K3`, `BQ2-K2`, `BQ2-K3`, `BQ3-K1`, `BQ3-K2`), perché senza di esse la dichiarazione di User Story 7 — "ciascuna delle otto misure" — non avrebbe un documento completo su cui operare.

### Parallel Opportunities

Le uniche parallelizzazioni reali, perché toccano file diversi senza dipendenza reciproca:

- T028 (`scripts/check_audit_coherence.py`, riga `DOCUMENTS`) e T029 (`scripts/check_audit_coherence.py`, riga `ARTIFACTS`) toccano lo stesso file ma blocchi indipendenti della stessa tupla-dichiarazione; marcati `[P]` perché non hanno dipendenza reciproca, pur condividendo il file.
- T037 (`README.md`) può procedere in parallelo a Phase 7 (US5) e Phase 8 (US4), perché nessuno dei tre dipende dagli altri due.

Nessun'altra coppia di task è marcata `[P]`: ogni altro task scrive in `scripts/build_kpi_measures.py` o in `docs/kpi_measures.md`, oppure dipende dal risultato del task precedente.

---

## Parallel Example: Phase 7 e README

```bash
# Una volta completata la Phase 6 (documento completo), questi task sono indipendenti:
Task: "Aggiungi docs/kpi_measures.md a DOCUMENTS in scripts/check_audit_coherence.py"
Task: "Aggiungi reports/kpi_measures.json a ARTIFACTS in scripts/check_audit_coherence.py"
Task: "Aggiorna README.md: tabella di stato, deliverable, frase sui documenti, Setup, Struttura"
```

---

## Implementation Strategy

### Perché non esiste un vero MVP

FR-020 richiede un valore per **ciascuno** degli otto KPI prima che il documento si possa considerare pubblicato, e SC-001 lo verifica sull'insieme completo. User Story 1 da sola (solo l'artefatto JSON, senza il documento) non è un incremento consegnabile nel senso in cui lo sarebbe per un'applicazione: è la base tecnica su cui ogni altra user story scrive. Le priorità P1/P2 ordinano **il rischio di ciò che si scrive per primo** — l'invarianza della North Star (US2) e la quota di zeri (US3) sono i due debiti più esposti ereditati dalla `007a` — non un confine di consegna parziale.

### Ordine di lavoro effettivo

1. T001: scheletro dello script.
2. T002-T013 (Foundational): il nucleo di calcolo, tutte e otto le misure, l'invarianza della North Star, l'artefatto scritto e verificato deterministico.
3. T014-T015 (US1): la catena intera verificata, il documento aperto.
4. T016-T017 (US2): `BQ1-K1` e l'esito dell'invarianza.
5. T018-T019 (US3): `BQ2-K1` e gli avvertimenti.
6. T020-T027, T026a incluso (US7): le sei sezioni residue, lo stato di default, il dispatch di E9, il congelamento del suo esito in `reports/kpi_engine_check.json`, l'incorporazione dell'esito reale nel documento.
7. T028-T030, T028a incluso (US5, P2): il documento e i due artefatti entrano nel controllo di coerenza automatico.
8. T031-T035 (US4, P2): D10, D11, la nota in loco di §11, la chiusura di §12, la proposta di chiusura delle issue.
9. T036 (US6, P2): la nota in loco su `business_case.md` §3.
10. T037-T040a (Polish): README, quickstart per intero, dispatch della revisione in contesto pulito, chiusura dei suoi rilievi, riesecuzione del controllo di coerenza dopo le correzioni.

**Il confine di sosta più sicuro, se la sessione si interrompe prima di ★ (E9), è la fine di Phase 8 o Phase 9** — a quel punto lo script esiste ed è deterministico, il documento è completo nella sua forma "calcolata", il controllo meccanico passa, e i debiti ereditati di `kpi_operators.md`/`business_case.md` sono chiusi. Ciò che resta — T026-T026a-T027 (E9 e il suo artefatto), T039-T040-T040a (revisione) — dipende da un'azione di Valerio fuori da questa sessione: non è lavoro da comprimere, è lavoro che aspetta un input esterno per definizione (coerente con "Ordine di lavoro e punti di sosta" di [plan.md](./plan.md)).

---

## Notes

- `[P]` compare solo su T028, T029, T037 — le uniche combinazioni di task che non hanno dipendenza reciproca stretta.
- `[Story]` mappa ogni task alla propria user story per tracciabilità verso spec.md; Setup, Foundational e Polish non portano l'etichetta, come da convenzione del template. T026a, T028a e T040a portano la lettera perché inseriti fra due task già numerati in risposta alla revisione di regia sul piano, sullo stesso schema dei suffissi letterali già in uso nel progetto per gli FR (`FR-011a`, `FR-013a`).
- Nessun task di test in senso software: la verifica è affidata interamente a T038 (le dodici prove di quickstart.md), alla revisione in contesto pulito (T039-T040) e alla sua riconferma meccanica (T040a).
- Propendere per commit dopo ogni fase (non dopo ogni task): la fase è l'unità di senso su ciascuno dei due file principali, il singolo task quasi mai lo è.
- `docs/roadmap.md` non compare in nessun task: appartiene alla regia (FR-028).
- T026, T026a e T027 sono i tre task di questa lista che una sessione esecutiva non può chiudere da sola senza un input esterno: T026 consegna a Valerio ciò che serve per E9, T026a congela il suo esito in `reports/kpi_engine_check.json` (senza il quale T027 scriverebbe un numero privo di ancora — rilievo bloccante della revisione di regia sul piano), T027 lo incorpora nel documento. Nessun task successivo a T025 dichiara «verificato contro il motore reale» prima che T027 sia stato eseguito per davvero (FR-030).
