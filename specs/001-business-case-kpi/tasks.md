---

description: "Task list — Feature 001: Business Case e Framework KPI"
---

# Tasks: Business Case e Framework KPI

**Input**: documenti di design da `/specs/001-business-case-kpi/`

**Prerequisiti**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [quickstart.md](./quickstart.md)

**Test**: nessun task di test automatico. La spec non richiede TDD e la feature non produce codice: la verifica è quella descritta in [quickstart.md](./quickstart.md), controlli strutturali più sessione di revisione, ed è distribuita nei task di verifica di ciascuna fase.

**Organizzazione**: i task sono raggruppati per user story, così ogni storia resta implementabile e verificabile in autonomia.

## Format: `[ID] [P?] [Story] Descrizione`

- **[P]**: eseguibile in parallelo (file diverso, nessuna dipendenza)
- **[Story]**: a quale user story appartiene (US1, US2, US3)
- Ogni descrizione riporta il percorso del file

## Nota sul parallelismo

Quasi tutti i task scrivono **nello stesso file**, `docs/business_case.md`. Le opportunità di parallelizzazione sono quindi poche e reali solo dove il file di destinazione è diverso: sono marcate `[P]`, le altre no. Marcare `[P]` task che toccano sezioni diverse dello stesso file produrrebbe conflitti di scrittura.

---

## Phase 1: Setup

**Scopo**: predisporre il contenitore del deliverable.

- [ ] T001 Creare `docs/business_case.md` con la sola struttura di heading, nell'ordine delle otto sezioni definite in [data-model.md](./data-model.md#struttura-del-documento): inquadramento, assunzioni strutturali, North Star metric, le tre domande, framework KPI, scala di confidenza, impatto economico, out of scope

---

## Phase 2: Foundational (prerequisiti bloccanti)

**Scopo**: fissare le convenzioni che US2 e US3 useranno in ogni scheda KPI. **Bloccano US2 e US3, non US1** — l'inquadramento può procedere in parallelo a questa fase.

- [ ] T002 Scrivere in `docs/business_case.md` la nota metodologica sulle due granularità dei dati Spotify — coppia traccia-genere (114.000) e traccia deduplicata (89.741) — con la regola che ogni KPI dichiara in quale opera, per il vincolo 8 di [data-model.md](./data-model.md#vincoli-di-integrità)
- [ ] T003 Scrivere in `docs/business_case.md` la convenzione degli identificativi KPI: sigla `BQn-Km` più nome semantico inglese `snake_case`, con la regola di univocità del nome semantico sull'intero progetto (FR-005a)

---

## Phase 3: User Story 1 — Il board capisce cosa stiamo per misurare (P1) 🎯 MVP

**Obiettivo**: un lettore senza contesto capisce la decisione in gioco, la metrica di successo e il perimetro.

**Verifica indipendente**: consegnare il documento a un revisore senza contesto pregresso e chiedergli di riformulare decisione, North Star e due esclusioni. Superata se non pone domande di chiarimento.

- [ ] T004 [US1] Scrivere la sezione di inquadramento in `docs/business_case.md`: chi è StreamWave, quale decisione strategica è in valutazione, chi è il destinatario del documento (FR-002)
- [ ] T005 [US1] Scrivere la sezione delle assunzioni strutturali in `docs/business_case.md`: proxy Netflix→StreamWave e Spotify→mercato musicale (FR-013), copertura temporale dei dati reali con le conclusioni che impedisce (FR-015), base utenti e orizzonte a 12 mesi (FR-014). Ogni voce marcata visivamente come assunzione, mai come dato
- [ ] T006 [US1] Aggiungere alle assunzioni in `docs/business_case.md` il modello di ricavo a due tier con **valori di prezzo puntuali** per base e premium, la ragione della scelta e la dichiarazione che è uno scenario (FR-017); dichiarare che l'incertezza vive nel tasso di adozione e non nel prezzo (FR-017a)
- [ ] T007 [US1] Scrivere la sezione delle tre domande in `docs/business_case.md`: per ciascuna, formulazione originale e riformulazione misurabile con soggetto, unità di misura e criterio di confronto o soglia (FR-003)
- [ ] T008 [US1] Scrivere la sezione North Star in `docs/business_case.md`: una sola metrica, di natura coerenza strategica, con motivazione e almeno due alternative considerate e scartate con il perché (FR-008)
- [ ] T009 [US1] Scrivere la sezione "Out of scope" in `docs/business_case.md` con almeno cinque voci motivate (FR-012), incorporando i limiti emersi dalla ricerca: inutilizzabilità dei conteggi per dimensionare il mercato (R1), esclusione delle serie TV dal confronto di durata (R3), assenza del lato costi, assenza di dati comportamentali
- [ ] T010 [US1] Verificare `docs/business_case.md` eseguendo i controlli di [quickstart.md](./quickstart.md) su presenza delle sezioni e conteggio delle voci fuori scope; correggere finché l'esito è quello atteso

**Checkpoint**: a questo punto il documento è già consegnabile. Dichiara la decisione, il criterio di successo e il perimetro, senza ancora definire come si misura.

---

## Phase 4: User Story 2 — L'analista sa quali KPI costruire (P2)

**Obiettivo**: da 6 a 9 KPI definiti in modo non ambiguo, ciascuno agganciato a una sola domanda.

**Verifica indipendente**: fornire a un revisore la sola formula concettuale di ogni KPI e verificare che ne descriva calcolo e granularità come attesi, per almeno l'80% dei KPI.

**Dipende da**: Phase 2 (convenzioni) e Phase 3 (le domande riformulate esistono).

- [ ] T011 [US2] Scrivere in `docs/business_case.md` le schede dei 2-3 KPI di **BQ1** (posizionamento), costruite sul confronto di profilo di mood secondo la decisione D1 di [research.md](./research.md#d1--loverlap-si-costruisce-sul-profilo-di-mood-non-sui-generi): assi energia, positività e ritmo, con le audio feature sul lato musicale e la tabella di corrispondenza dichiarata sul lato video. Il KPI di durata confronta solo film e tracce (D3)
- [ ] T012 [US2] Scrivere in `docs/business_case.md` le schede dei 2-3 KPI di **BQ2** (segmento di ingresso), che usano `popularity` come proxy di domanda su tracce deduplicate e **non contano tracce** per dimensionare il segmento (D2)
- [ ] T013 [US2] Scrivere in `docs/business_case.md` le schede dei 2-3 KPI di **BQ3** (impatto stimato), derivati dal modello a due tier: adozione del tier premium ed effetto sul ricavo medio per utente. Nessun riferimento a ricavi pubblicitari o riduzione di churn, fuori dal modello assunto (FR-018)
- [ ] T014 [US2] Verificare che ogni scheda KPI in `docs/business_case.md` riporti tutti i campi obbligatori dell'entità KPI di [data-model.md](./data-model.md#kpi): sigla, nome semantico, nome, cosa misura, formula concettuale, unità, granularità, direzione di lettura, domanda di appartenenza
- [ ] T015 [US2] Scrivere in `docs/business_case.md` la tabella riepilogativa che indicizza le schede, con i soli campi brevi (sigla, nome semantico, domanda, fonte, confidenza, formato). La formula concettuale **non** deve comparire in tabella (FR-005b)
- [ ] T016 [US2] Scrivere in `docs/business_case.md` la sezione dell'impatto economico come titolo secondario a range best/base/worst, esplicitamente distinto dalla North Star e mai fuso con essa in un indice composito (FR-020)
- [ ] T017 [US2] Verificare `docs/business_case.md` eseguendo i controlli di cardinalità e univocità di [quickstart.md](./quickstart.md): totale KPI tra 6 e 9, da 2 a 3 per domanda, nessun nome semantico duplicato, nessuna sintassi DAX/SQL/Python nelle formule

**Checkpoint**: il documento contiene ora il framework completo, ma i numeri non sono ancora qualificati per affidabilità.

---

## Phase 5: User Story 3 — Chi legge un numero sa quanto fidarsi (P3)

**Obiettivo**: ogni KPI dichiara da dove viene e quanto è affidabile, con il formato di presentazione che ne discende.

**Verifica indipendente**: estrarre la tabella riepilogativa e verificare che ogni KPI compaia una volta sola con fonte e confidenza compilate, e che il formato sia coerente con il livello dichiarato.

**Dipende da**: Phase 4 (i KPI da qualificare devono esistere).

- [ ] T018 [US3] Scrivere in `docs/business_case.md` la sezione della scala di confidenza con i tre criteri operativi della decisione D5 di [research.md](./research.md#d5--criteri-operativi-della-scala-di-confidenza), formulati in modo applicabile da un terzo senza giudizio soggettivo (FR-009)
- [ ] T019 [US3] Assegnare a ogni KPI in `docs/business_case.md` fonte (`Netflix (reale)`, `Spotify (reale)`, `Sintetico`, `Derivato` con fonti a monte) e livello di confidenza, applicando i criteri di T018 (FR-010)
- [ ] T020 [US3] Assegnare a ogni KPI in `docs/business_case.md` il formato di presentazione, verificando il vincolo 4 di [data-model.md](./data-model.md#vincoli-di-integrità): confidenza bassa implica sempre range best/base/worst, mai valore puntuale (FR-011)
- [ ] T021 [US3] Aggiungere nelle schede dei KPI di BQ2 in `docs/business_case.md` la nota sulla fragilità di `popularity` — 14% di tracce a zero, concentrate in alcuni generi (R5) — che è la ragione per cui quei KPI non superano la confidenza media
- [ ] T022 [US3] Verificare che i KPI che compongono la North Star in `docs/business_case.md` siano tutti a confidenza alta (vincolo 6 di data-model.md); se non lo sono, la North Star va ridefinita, non la confidenza abbassata
- [ ] T023 [US3] Verificare `docs/business_case.md` eseguendo il controllo di coerenza confidenza-formato di [quickstart.md](./quickstart.md): ogni riga a confidenza bassa deve riportare `range`

---

## Phase 6: Polish e verifica finale

**Scopo**: chiudere la feature secondo la definizione di completo di quickstart.md.

- [ ] T024 Eseguire tutti i controlli strutturali di livello 1 di [quickstart.md](./quickstart.md) su `docs/business_case.md` e correggere gli scostamenti
- [ ] T025 Ispezionare ogni numero presente in `docs/business_case.md` e verificare che sia un input di scenario dichiarato come assunzione e mai un esito di calcolo (FR-016, SC-007); rimuovere quelli non riconducibili a un'assunzione
- [ ] T026 Condurre la sessione di revisione in contesto pulito su `docs/business_case.md` secondo il livello 2 di [quickstart.md](./quickstart.md), con le tre prove su comprensione, univocità delle formule e tenuta del perimetro
- [ ] T027 Scrivere il verbale in `specs/001-business-case-kpi/review.md` con l'esito di ciascuna prova e le divergenze rilevate (FR-019)
- [ ] T028 [P] Aggiornare la tabella di stato in `README.md`: fase Specification e Plan concluse, Implementation conclusa per la feature 001
- [ ] T029 [P] Aggiornare `specs/001-business-case-kpi/checklists/requirements.md` con l'esito della verifica finale

---

## Dipendenze e ordine di esecuzione

### Dipendenze tra fasi

```text
Phase 1 (Setup)
   ├─→ Phase 2 (Foundational) ──→ Phase 4 (US2) ──→ Phase 5 (US3) ──→ Phase 6
   └─→ Phase 3 (US1) ────────────────↑
```

Phase 2 e Phase 3 sono indipendenti tra loro: le convenzioni sugli identificativi non servono all'inquadramento, e l'inquadramento non serve alle convenzioni. Phase 4 richiede entrambe.

### Dipendenze tra user story

- **US1** non dipende da nulla oltre al setup. È il MVP.
- **US2** dipende da US1: un KPI senza la domanda riformulata non è verificabile.
- **US3** dipende da US2: qualifica KPI che devono già esistere.

Le tre storie sono **incrementali, non indipendenti**. È una conseguenza del deliverable: sono tre strati dello stesso documento, non tre funzionalità separate. Ogni strato però lascia il documento in uno stato consegnabile, che è ciò che il principio III richiede.

### Opportunità di parallelizzazione

Poche e circoscritte, perché il deliverable è un file solo:

- **T028 e T029** toccano file diversi da `docs/business_case.md` e sono eseguibili in parallelo tra loro
- **T002/T003** (Phase 2) e **T004-T009** (Phase 3) sono logicamente indipendenti, ma scrivono nello stesso file: vanno eseguiti in sequenza da un solo autore, oppure su sezioni separate con attenzione

```bash
# Esempio: gli unici due task realmente parallelizzabili
# T028 -> README.md
# T029 -> specs/001-business-case-kpi/checklists/requirements.md
```

---

## Strategia di implementazione

### MVP: solo User Story 1

Phase 1 → Phase 3 → verifica T010. Il risultato è un documento che inquadra la decisione, dichiara la North Star e il perimetro, senza il framework KPI. È già presentabile e già difendibile: la domanda è posta, il criterio di successo è dichiarato, i limiti sono espliciti.

### Consegna incrementale

1. **Phase 1 + 3** → documento di inquadramento (MVP)
2. **Phase 2 + 4** → framework KPI completo
3. **Phase 5** → qualificazione di fonte e confidenza
4. **Phase 6** → verifica e chiusura

Ogni stadio lascia il repository in uno stato coerente e presentabile, come richiede il principio III della constitution.

### Vincolo di tempo

29 task per una feature che deve stare in **una giornata lavorativa**. La maggior parte sono task di scrittura di poche righe su un documento unico; i più onerosi sono T011-T013 (le schede KPI) e T026 (la sessione di revisione). Se a metà giornata la Phase 4 non è conclusa, la scomposizione corretta è consegnare il MVP e aprire una feature 002 per il framework KPI, non allungare la giornata.

---

## Note

- Nessun task produce codice: la feature definisce, non calcola. Il principio II della constitution si applicherà alle feature successive
- Nessun task presuppone l'interazione con GUI di Power BI o Tableau (principio V)
- I riferimenti `R1`-`R5` e `D1`-`D6` rimandano ai ritrovamenti e alle decisioni di [research.md](./research.md)
- I riferimenti `FR-xxx` e `SC-xxx` rimandano ai requisiti e ai criteri di successo di [spec.md](./spec.md)
