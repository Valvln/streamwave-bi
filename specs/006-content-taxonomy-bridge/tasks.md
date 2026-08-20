---

description: "Task list — Feature 006: Content Taxonomy Bridge"
---

# Tasks: Content Taxonomy Bridge

**Input**: documenti di design da `/specs/006-content-taxonomy-bridge/`

**Prerequisiti**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/dim-category-mood-contract.md](./contracts/dim-category-mood-contract.md), [quickstart.md](./quickstart.md)

**Test**: nessun framework introdotto (T6 di research.md), come nella 002-004. I comportamenti verificabili si controllano da riga di comando o per lettura secondo [quickstart.md](./quickstart.md); i task di verifica stanno in coda a ciascuna fase.

**Organizzazione**: per user story, così ogni storia resta verificabile in autonomia. La corrispondenza con i cinque blocchi del piano è: Setup + Foundational = premesse di **A**, US1 = **A** (+ il terzo punto di fermata ★), US2 = **B**, US3 = **C**, US4 = coda di **C** e presidio di D6, US5 = **D** + la parte di **E** che è revisione del documento, Polish = il resto di **E**.

## Format: `[ID] [P?] [Story] Descrizione`

- **[P]**: eseguibile in parallelo (file diverso, nessuna dipendenza)
- **[Story]**: a quale user story appartiene (US1-US5)
- Ogni descrizione riporta il percorso del file

## Nota sul parallelismo

Come nella 002-004: l'autore è uno solo e le storie sono in dipendenza stretta per costruzione — D1 impone un ordine, non lo suggerisce. I `[P]` sono marcati solo dove file diverso **e** dipendenza effettivamente assente coincidono, che qui accade quasi solo in Setup e in Polish.

## Nota sulle sigle

`D1`-`D9` sono le decisioni della [spec](./spec.md). `F1`-`F5` e `T1`-`T9` sono ritrovamenti e decisioni tecniche di [research.md](./research.md). `FR-xxx` e `SC-xxx` rimandano a requisiti e criteri di successo della spec.

## ⚠️ I due vincoli che governano l'ordine

**Il primo è D1: il criterio precede ogni valore, e la precedenza deve essere nella history, non solo nella prosa.** US1 si chiude con un commit isolato (T010) che non contiene alcun valore, nemmeno di prova. Nessun task di US2 può cominciare prima di quel commit.

**Il secondo è il terzo punto di fermata della roadmap (`DA-1`, 2026-08-19): dopo il commit del criterio e prima che il modello proponga alcunché.** T010 non è solo un commit, è uno **stop**: il criterio torna in revisione prima che US2 inizi. È il punto di massima leva della feature — un criterio sbagliato produce tutti i 126 valori sbagliati, e nessuno lo riscrive più dopo che esistono.

Chi riprende questa lista a metà e non sa a che punto è: `git log --follow docs/mood_assignment_criteria.md` lo dice.

---

## Phase 1: Setup

**Scopo**: verificare le premesse trovate in Fase 0 **prima** di scrivere una riga. Tutte e tre si annullerebbero in silenzio se sbagliate.

- [X] T001 Verificare con `git check-ignore -v data/curated/test.json` che il percorso **non** sia intercettato da `.gitignore` (F1). Se lo fosse, fermarsi e cambiare collocazione prima di scrivere qualunque file
- [X] T002 [P] Verificare che il prefisso `MOOD.` per `values` sia disgiunto da `NF.`, `SP.`, `CL.`, `X.`, `BQ3.` nei quattro artefatti esistenti (T2 di research.md)
- [X] T003 [P] Verificare che le chiavi `mood_scale_anchor` e `mood_rounding` non collidano nello spazio piatto di `conventions` (F2, ripetuto qui perché nulla garantisce che due feature lo trovino nello stesso stato)
- [X] T004 [P] Rieseguire la normalizzazione a slug (minuscolo, non alfanumerico → `_`) sulle 42 categorie di `catalogs.netflix_categories_normalized` e confermare **zero collisioni** (F4). Se ne comparisse anche una sola, la forma degli identificativi `MOOD.category.<slug>.<asse>` va rivista prima di Fase 3

**Checkpoint**: le collocazioni reggono e i nomi non collidono. Si può scrivere.

---

## Phase 2: Foundational — gli ancoraggi di scala esistono già *(premessa di A)*

**Scopo**: verificare che F3 sia vero prima che il criterio ne dipenda. Blocca US1.

- [X] T005 Risolvere `SP.num.energy.min`, `SP.num.energy.max`, `SP.num.valence.min`, `SP.num.valence.max`, `SP.num.danceability.min`, `SP.num.danceability.max` in `reports/data_profile.json` e registrarne i valori esatti per l'uso nel criterio (F3). Se uno dei sei non risolvesse più — l'artefatto è cambiato dalla data della ricerca — il criterio deve ancorarsi a ciò che risolve davvero, non a ciò che questa fase presupponeva

**Checkpoint**: i sei identificativi esistono e sono noti. US1 può cominciare.

---

## Phase 3: User Story 1 — Il criterio esiste prima di ogni valore (Priority: P1) *(blocco A)*

**Goal**: `docs/mood_assignment_criteria.md` dichiara, per ciascuno dei tre assi, significato, base di attribuzione e ancoraggio agli estremi — ed è committato da solo.

**Independent Test**: il primo commit che introduce il file non tocca né la proposta né la tabella congelata, e li precede (quickstart, Prova 1).

- [X] T006 [US1] Scrivere in `docs/mood_assignment_criteria.md`, per ciascuno dei tre assi (`mood_energy`, `mood_valence`, `mood_danceability`), che cosa significa ogni valore per una categoria video e su quale base si assegna (FR-002)
- [X] T007 [US1] Scrivere per ciascun asse un esempio di ancoraggio all'estremo basso e uno all'estremo alto, **a livello di categoria o genere musicale come archetipo**, citando i sei identificativi di T005 come base osservabile (FR-004, D2, D7). Nessun titolo, trama o cast (FR-003) — se un esempio nomina un titolo specifico, va riscritto prima di procedere
- [X] T008 [US1] Aggiungere la nota di provenienza che dichiara che il criterio precede ogni valore della tabella, con rimando a questo piano e a D1
- [X] T009 [US1] Verificare che il file **non contenga** alcun valore numerico riconducibile a una cella della tabella, nemmeno di prova (FR-001) — solo gli identificativi di ancoraggio di T005
- [X] T010 [US1] **Punto di fermata obbligatorio (★, terzo stop della `DA-1`).** Proporre a Valerio il commit del solo criterio. È questo commit a costituire la prova di precedenza richiesta da D1 e dalla condizione 1 della quinta fonte della constitution — senza di esso resta un'affermazione. **Non proseguire alla Fase 4 prima che sia stato eseguito e il criterio confermato**
- [X] T011 [US1] **Verifica**: eseguire le Prove 1 e 2 di [quickstart.md](./quickstart.md) — precedenza in history, ancoraggio a osservazioni reali e non a titoli

**Checkpoint**: SC-001 verificabile. Il criterio esiste, è committato da solo, ed è il solo metro ammesso per ogni contestazione successiva.

---

## Phase 4: User Story 2 — La proposta è di un modello, invocato una volta, fuori dalla pipeline (Priority: P1) *(blocco B)*

**Goal**: `data/curated/dim_category_mood_proposal.json` contiene una prima stesura delle 42 righe, con prompt, modello e data versionati, e nessuno script del repository l'ha invocato.

**Independent Test**: il file esiste, i tre metadati sono presenti, e nessuna corrispondenza compare cercando una chiamata di rete verso un servizio LLM in uno script versionato (quickstart, Prova 3).

**⚠️ Nessuno script invoca il modello**: l'invocazione di questa fase è un passaggio **umano**, fuori da qualunque pipeline (FR-005).

- [X] T012 [US2] Invocare manualmente un LLM con il criterio di `docs/mood_assignment_criteria.md` come istruzione, ottenendo una prima stesura delle 42 righe (una per categoria di `catalogs.netflix_categories_normalized`, tre valori decimali ciascuna)
- [X] T013 [US2] Scrivere `data/curated/dim_category_mood_proposal.json` secondo [data-model.md](./data-model.md) §2: `schema_version`, `model`, `prompt` per intero, `invoked_at`, `rows` con le chiavi letterali delle 42 categorie, valori come **stringhe decimali** (T4 di research.md)
- [X] T014 [US2] Verificare con `grep -rniE "openai|anthropic|api[._-]?key|requests\.(get|post)|urllib\.request" scripts/` che nessuna corrispondenza esista (FR-005, FR-007): la proposta non è, e non deve poter sembrare, un passo di pipeline
- [X] T015 [US2] Proporre a Valerio il commit della proposta, **separato** dal commit del criterio (T010)
- [X] T016 [US2] **Verifica**: eseguire la Prova 3 di [quickstart.md](./quickstart.md)

**Checkpoint**: la proposta esiste, è distinta dal criterio nella history, e non è mai stata trattata come tabella finale (FR-007).

---

## Phase 5: User Story 3 — La proposta è verificata da chi non l'ha prodotta, e il conteggio degli spostamenti è pubblico (Priority: P1) *(blocco C)*

**Goal**: ogni riga della proposta è confrontata contro il criterio da chi non l'ha ottenuta; il numero di celle modificate è registrato nell'artefatto congelato, non solo dichiarato in prosa.

**Independent Test**: chi firma la verifica è dichiaratamente diverso da chi ha ottenuto la proposta; il campo del conteggio in `data/curated/dim_category_mood.json` non è vuoto (quickstart, Prova 4).

**⚠️ Non è la revisione in contesto pulito di D9.2** (FR-008): è un passo di lavorazione, che avviene prima del congelamento e con pieno accesso al resto del repository — l'indipendenza richiesta è quella di chi verifica, non l'assenza di contesto.

- [X] T017 [US3] **Dispatch esplicito della verifica a un attore distinto da chi ha condotto T012** — un subagent che non ha prodotto la proposta, oppure Valerio. Non serve l'isolamento stretto da subagent di T036: quell'attore legge il resto del repository, in particolare `reports/data_profile.json` per i sei ancoraggi di FR-004 (correzione B2 della revisione: la sola dichiarazione «chi verifica non è chi ha proposto», senza un meccanismo di dispatch, non la realizza — due task consecutivi nella stessa sessione sarebbero eseguiti dalla stessa sessione). L'attore verifica ciascuna delle 126 celle della proposta contro il criterio (T006-T008) come **unico metro di contestazione** — non un vincolo su che cosa possa leggere (FR-008)
- [X] T018 [US3] Per ogni cella contestata, registrare il punto specifico del criterio violato (FR-009). Una contestazione priva di questo riferimento non è ammessa come tale
- [X] T019 [US3] Contare le celle (categoria × asse) modificate rispetto alla proposta. **Se il conteggio è zero, scrivere la dichiarazione esplicita che è un ritrovamento** — la proposta seguiva già il criterio — **e non una conferma del processo** (FR-010, User Story 3 scenario 3)
- [X] T020 [US3] Scrivere `data/curated/dim_category_mood.json` secondo [data-model.md](./data-model.md) §3: `schema_version`, `version: 1`, `source` (percorso e impronta sha256 della proposta), `verification` (`verified_by` MUST nominare esplicitamente l'attore dispatchato in T017 — «subagent, non ha prodotto la proposta di T012» oppure «Valerio» — non una formula generica; `changes_count`; l'elenco delle celle modificate con il punto del criterio citato; la nota di ritrovamento se zero), `values` con le 126 celle `MOOD.category.<slug>.<asse>` più i tre identificativi aggregati, `catalogs.mood_categories`, `conventions` (`mood_scale_anchor` che cita i sei identificativi di T005, `mood_rounding`)
- [X] T021 [US3] Verificare che ogni valore in `values` sia una stringa decimale nell'intervallo `0-1` (FR-013, T4/T5 di research.md) — nessun `float`, nessun valore fuori scala
- [X] T022 [US3] Proporre a Valerio il commit della tabella congelata, separato dai due precedenti
- [X] T023 [US3] **Verifica**: eseguire la Prova 4 di [quickstart.md](./quickstart.md)

**Checkpoint**: SC-002 verificabile. `006a` è sostanzialmente chiuso — la tabella esiste, è congelata, e la verifica indipendente è dichiarata e quantificata.

---

## Phase 6: User Story 4 — La tabella congelata copre le 42 categorie sulla scala corretta, con versione dichiarata (Priority: P2) *(coda di C, chiusura di D6/R2)*

**Goal**: `scripts/check_audit_coherence.py` unisce `dim_category_mood.json` come quarto artefatto e **fallisce** — non avvisa — se le sue 42 categorie divergono da `catalogs.netflix_categories_normalized`.

**Independent Test**: alterare l'insieme delle categorie nella tabella fa fallire il controllo con uscita diversa da zero; ripristinato, il controllo torna verde (quickstart, Prova 7).

- [X] T024 [US4] Aggiungere `MOOD = REPO / "data" / "curated" / "dim_category_mood.json"` a `ARTIFACTS` in `scripts/check_audit_coherence.py`. `load_artifacts()` non cambia: il ciclo su `("values", "catalogs", "conventions")` è già generico (T8 di research.md)
- [X] T025 [US4] Scrivere una funzione di guardia nuova, chiamata da `main()` **prima** del ciclo sui documenti, che confronta `catalogs.mood_categories` dell'artefatto unito con `catalogs.netflix_categories_normalized` come insiemi e, se divergono, aggiunge l'esito a `failed` stampando la differenza simmetrica — quali categorie mancano da una parte, quali dall'altra (D6, FR-019). È il meccanismo che chiude la divergenza 5 della `002`: non un marcatore nella prosa, un controllo sui dati dell'artefatto
- [X] T026 [US4] Aggiornare l'intestazione e la docstring di `scripts/check_audit_coherence.py`, che oggi nominano tre artefatti e quattro documenti
- [X] T027 [US4] **Verifica**: eseguire le Prove 5, 6 e 7 di [quickstart.md](./quickstart.md) — copertura e scala, campo `version`, e il fallimento meccanico su tassonomia alterata, con ripristino dopo ciascuna alterazione
- [X] T028 [US4] Proporre a Valerio il commit dell'estensione dello script

**Checkpoint**: SC-004 verificato. Il presidio della divergenza 5 della `002` è un controllo che ferma, non un promemoria — è la chiusura diretta di R2.

---

## Phase 7: User Story 5 — Il documento pubblicato passa la revisione in contesto pulito standard prima di arrivare su `main` (Priority: P2) *(blocco D + parte di E)*

**Goal**: `docs/content_taxonomy_bridge.md` esiste, ogni sua cifra è ancorata, passa il controllo in severità stretta, ed è stato letto da un revisore che ha ricevuto **solo** quel file prima che venisse corretto.

**Independent Test**: `specs/006-content-taxonomy-bridge/review.md` dichiara in apertura di aver ricevuto solo il documento pubblicato, precede in history le correzioni al documento, e il suo blocco di chiusura dichiara come ogni rilievo è stato chiuso (quickstart, implicito in SC-003).

- [X] T029 [US5] Scrivere `docs/content_taxonomy_bridge.md` secondo [data-model.md](./data-model.md) §4 e FR-022: la natura interpretativa della tabella per prima; i quattro passi di D1 con i relativi artefatti, comprese le due revisioni distinte di D9; il conteggio degli spostamenti (`MOOD.review.changes_count`); il contratto di versione per la `007` (D5, FR-016); i limiti dichiarati
- [X] T030 [US5] Ancorare **ogni** numerale in posizione di fatto misurato secondo `docs/convenzioni-marcatura.md` — cifra, numerale in lettere, o letterale fra apici inversi per una categoria via `catalogs.mood_categories`. Nessun numerale in lettere per un fatto misurato (FR-024, corollario b della regola D5 della `003`)
- [X] T031 [US5] Aggiungere `docs/content_taxonomy_bridge.md` a `DOCUMENTS` in `scripts/check_audit_coherence.py` con `strict=True`, quinto documento (FR-023) — severità stretta fin dalla nascita, nessun periodo di avviso da onorare (T7 di research.md)
- [X] T032 [US5] Aggiornare `docs/convenzioni-marcatura.md` in tre punti (FR-023): §3 (da tre a **quattro** artefatti uniti), la tabella di severità di §5 (da quattro a **cinque** documenti), la tabella di provenienza in coda (data e feature `006`)
- [X] T033 [US5] Scrivere la **nota in loco** su `docs/data_model.md` §15, condizione 4 (D8, FR-021): data, la decisione presa (`DA-1`: un LLM propone, una persona decide, nessuno script chiama il modello a runtime), rimando a `docs/roadmap.md` sezione «Decisioni aperte», `DA-1`. Il testo originale della condizione 4 **non si riscrive**
- [X] T034 [US5] **Verifica**: eseguire le Prove 8, 9 e 10 di [quickstart.md](./quickstart.md) — severità stretta con le due alterazioni, assenza di attributi di record individuale, assenza di promozione di confidenza e di etichetta `Benchmark (esterno)`
- [X] T035 [US5] Proporre a Valerio il commit del documento, dell'estensione dello script, di `convenzioni-marcatura.md` e della nota in loco su `data_model.md` — o commit separati per gruppo, secondo la convenzione di `CLAUDE.md` sulle correzioni in loco vs. i documenti nuovi
- [X] T036 [US5] **Dispatch della revisione in contesto pulito**: il revisore riceve **solo** `docs/content_taxonomy_bridge.md` — non il criterio, non la proposta, non la tabella congelata, non alcun altro file del repository (D9.2, FR-011a). Sul modello di `specs/005-data-model-design/review.md`
- [X] T037 [US5] **Scrivere e proporre il commit di `specs/006-content-taxonomy-bridge/review.md` non appena la revisione torna, prima di correggere il documento** (primo obbligo di `CLAUDE.md`). Il verbale dichiara in apertura che cosa ha letto e che cosa no, e ancora la versione letta con commit e impronta (FR-011b)
- [X] T038 [US5] Chiudere i rilievi del verbale nel documento pubblicato (e, se un rilievo lo richiede, negli altri artefatti). Il verbale stesso **non si corregge**: il blocco di chiusura, aggiunto in coda, dichiara come ogni rilievo è stato chiuso — risolvendolo, indebolendo l'affermazione, respingendolo con la prova, o rinviandolo (quarto obbligo di `CLAUDE.md`)
- [X] T039 [US5] **Verifica**: confermare che il commit di `review.md` (T037) precede, in history git, ogni commit di correzione al documento prodotto da T038 (SC-003)

**Checkpoint**: SC-003 verificato. `006b` è chiuso: il documento esiste, è ancorato, è passato dalla revisione che `CLAUDE.md` impone a ogni feature, e la `006` non è la prima delle sei a saltarla.

---

## Phase 8: Polish e questioni trasversali *(resto di E)*

**Scopo**: chiudere ciò che riguarda il progetto e non la sola feature, e verificare la composizione di tutto ciò che le fasi precedenti hanno costruito una alla volta.

- [X] T040 Aggiornare `README.md` (FR-025): riga nella tabella di stato con link a `specs/006-content-taxonomy-bridge/review.md`, `docs/content_taxonomy_bridge.md` elencato come deliverable, la prosa dei deliverable estesa con un capoverso sul sesto documento, sezioni `Setup` (la riga del passo 5 dichiara ora cinque documenti e quattro artefatti) e `Struttura` allineate
- [X] T041 **Preparare, non scrivere**, i riferimenti puntuali per l'aggiornamento di `docs/roadmap.md` (FR-026): dove vive la chiusura di `DA-1` come eseguita (distinta dalla risoluzione di principio già registrata il 2026-08-19), della divergenza 10 della `001`, della divergenza 5 della `002`, della parte generale della divergenza 5 della `003`. **Non modificare `docs/roadmap.md` direttamente**: è artefatto di governance e appartiene alla regia (`CLAUDE.md`; stesso confine già osservato dalla `004`, plan.md "Project Structure"). Consegnare i riferimenti a Valerio perché la regia possa scrivere la sezione senza doverli ricostruire
- [X] T042 [P] Rileggere [contracts/dim-category-mood-contract.md](./contracts/dim-category-mood-contract.md) contro ciò che la feature ha effettivamente prodotto, e correggere il contratto se l'implementazione diverge — lezione della `003`: dove contratto e implementazione divergono, è il contratto a dover essere corretto, non chi legge a doverlo indovinare
- [X] T043 [P] Verificare che nessun artefatto della feature presenti `BQ1-K3`, `BQ2-K2` o `BQ2-K3` a confidenza `alta`, e che nessuno etichetti la fonte di `dim_category_mood` come `Benchmark (esterno)` (SC-005, FR-017, FR-018)
- [X] T044 Eseguire **l'intero** [quickstart.md](./quickstart.md) dalla Prova 1 alla Prova 10 su una copia pulita del repository, in sequenza. Le verifiche di fase hanno coperto le prove una alla volta; questa copre la loro composizione

---

## Dipendenze

```
Fase 1 (Setup)
   ↓
Fase 2 (Foundational — gli ancoraggi di F3 esistono)
   ↓
Fase 3 US1 (blocco A — il criterio)  ⚠️ ★ STOP OBBLIGATORIO PRIMA DI PROSEGUIRE (T010)
   ↓
Fase 4 US2 (blocco B — la proposta)
   ↓
Fase 5 US3 (blocco C — verifica indipendente + congelamento)  ← 006a sostanzialmente chiuso
   ↓
Fase 6 US4 (coda di C — presidio meccanico D6)
   ↓
Fase 7 US5 (blocco D + revisione D9.2)  ← 006b si chiude qui
   ↓
Fase 8 (Polish)
```

**Le cinque storie non sono indipendenti fra loro, ed è deliberato**: è la stessa forma di dipendenza verticale della `004`. US2 non ha un criterio da rispettare senza US1; US3 non ha una proposta da verificare senza US2; US4 verifica una tabella che US3 ha già scritto; US5 documenta un processo che deve essere già concluso per essere raccontato senza anticipazioni. L'indipendenza che il template chiede è **verticale**: ogni storia resta testabile con le proprie prove di quickstart, ma non è eseguibile fuori ordine.

## Opportunità di parallelismo

Poche, come nella 002-004: T002-T004 in Fase 1, T042-T043 in Fase 8. All'interno delle fasi i task scrivono quasi sempre sullo stesso file (il criterio, poi la proposta, poi la tabella) e vanno in sequenza per costruzione, non per scelta di processo.

## Strategia di consegna

**MVP**: Fasi 1-6. A quel punto `data/curated/dim_category_mood.json` esiste, copre le 42 categorie sulla scala corretta, porta versione e registro di verifica, e il controllo di coerenza lo protegge meccanicamente da un cambio di tassonomia — è tutto ciò che la `007` consuma (vedi [contracts/dim-category-mood-contract.md](./contracts/dim-category-mood-contract.md)). È **`006a`** della spec.

**Se il tempo stringe**, la linea di taglio è quella che la spec dichiara: fra Fase 6 e Fase 7, cioè fra `006a` e `006b`. Il documento pubblicato e la sua revisione in contesto pulito sono ciò che rende il lavoro leggibile e difendibile da fuori — indispensabile per un progetto da portfolio e per il contratto della `007`, ma non per l'esistenza della tabella.

**Se la scrittura del criterio (Fase 3) rivelasse che la scala non è ancorabile come F3 prevede** — i sei identificativi non esistono più, o non bastano — la feature si ferma a T005/T007 e il caso torna a Valerio: nessun task di questa lista prevede un ripiego automatico che sostituisca l'ancoraggio con un giudizio non verificabile.
