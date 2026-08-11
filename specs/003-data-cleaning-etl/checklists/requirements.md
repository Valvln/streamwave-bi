# Specification Quality Checklist: Data Cleaning & ETL

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-11
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Note di validazione

Tre annotazioni sul modo in cui alcuni criteri sono stati letti, perché una lettura rigida li darebbe per falliti.

**«No implementation details».** La spec nomina Python (FR-001) e `data/raw/`, `data/processed/`, `.gitignore`, `reports/data_profile.json`. Non sono scelte di implementazione lasciate scappare: Python per le trasformazioni è imposto dal principio II della constitution, e i percorsi sono vincoli di repository preesistenti che la feature eredita. Ogni scelta effettivamente libera — formato dei file di output, forma del meccanismo di ancoraggio, struttura interna della pipeline — è esplicitamente demandata a `/speckit.plan` nella sezione Assumptions.

**«Written for non-technical stakeholders».** Il lettore di riferimento di questo progetto è un board, non un utente finale generico. La spec presuppone la lettura di `docs/business_case.md` e `docs/data_audit.md`, come le due spec precedenti.

**«Success criteria are technology-agnostic».** SC-004 e SC-012 nominano git e l'assenza di `data/raw/`. Sono esiti verificabili, non dettagli tecnici: il fatto che gli output non siano versionati e che la verifica funzioni senza i dati di origine è una proprietà sostanziale della feature, non un modo di realizzarla.

## Decisioni che la revisione deve poter contestare

Non sono difetti della checklist: sono i punti in cui la spec ha deciso invece di rinviare, e sono il motivo per cui va in revisione prima di diventare un piano.

1. **D2 ripara invece di isolare.** La spec sposta tre valori da un campo all'altro sulla base di una regola sintattica. È l'unica trasformazione della feature che modifica un valore invece di marcarlo o di porlo a mancante. Il vincolo sul raggio d'azione (FR-016) è ciò che la rende difendibile; se la revisione non lo ritiene sufficiente, l'alternativa è isolare senza riparare, e le tre durate restano perse.
2. **D3 adotta 27,03% e non 21,28%.** La scelta rende scorretta l'espressione «circa un quinto» già pubblicata, e obbliga a una nota in loco su un artefatto mergiato (FR-035).
3. **D4 sposta la soglia dal 60% al 50%.** Riclassifica `country` e altri generi rispetto a quanto §3.5 di `docs/data_audit.md` presentava, e obbliga a una seconda nota in loco (FR-036).
4. **D4 evita deliberatamente la formulazione più diretta** — l'elenco dei generi la cui mediana di popolarità è zero — per non pubblicare una misura di posizione a un passo da `BQ2-K1`. La spec preferisce l'osservazione equivalente sulla quota di zeri. È una scelta di perimetro che costa chiarezza espositiva.
5. **D5 propone una regola che la regia porterà in `CLAUDE.md`.** La spec la applica ai propri artefatti, ma la regola vincolerà ogni documento successivo: è la decisione con il raggio più lungo fra le cinque, e la sola il cui costo ricadrà su feature che non l'hanno scelta.
6. **Un ritrovamento nuovo entra nella spec**: 720 tracce hanno repliche in disaccordo sulla popolarità, quindi la deduplicazione non è priva di perdita. Né la 001 né la 002 lo avevano registrato. La spec lo tratta come vincolo (FR-018, FR-019) senza pubblicarne le cifre, che spettano all'artefatto di rendicontazione.
