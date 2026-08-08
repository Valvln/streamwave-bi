# Specification Quality Checklist: Business Case e Framework KPI

- **Purpose**: Validate specification completeness and quality before proceeding to planning
- **Created**: 2026-08-06
- **Feature**: [spec.md](../spec.md)

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

## Constitution Gate (principi I, III, IV, VI)

- [x] Sezione "Domanda di Business" compilata — la feature serve BQ1+BQ2+BQ3 come framework
- [x] Sezione "Limiti Dichiarati" compilata — 7 voci, incluse due inferenze da evitare
- [x] Sezione "Provenienza e Confidenza dei Dati" compilata — 7 famiglie di KPI classificate
- [x] Feature completabile in una giornata lavorativa (principio III) — è un solo documento, scomposto in tre strati incrementali (US1 inquadramento, US2 KPI, US3 provenienza)

## Notes

- **Iterazione 1 (2026-08-06)**: tutti gli item passano tranne un marker [NEEDS CLARIFICATION] su FR-017 (modello di ricavo), deliberato: nessun default difendibile, e la scelta determina quali KPI di revenue abbiano senso in BQ3.
- **Iterazione 2 (2026-08-06)**: marker risolto. Modello adottato: **due tier** (base solo video + premium con musica). FR-017 riscritto come requisito di dichiarazione dell'assunzione; aggiunto FR-018 che vincola i KPI di revenue a quel modello ed esclude esplicitamente ricavi pubblicitari ed effetti su churn. Assunzione e limite corrispondente propagati nelle sezioni Assumptions e Limiti Dichiarati. **Tutti gli item passano: spec pronta per `/speckit-plan`.**
- **Iterazione 3 (2026-08-06, dopo `/speckit.clarify`)**: 5 domande poste e risolte, nessun item regredito. Modifiche: SC-001 e SC-005 riscritti su un revisore senza contesto pregresso (erano non eseguibili in un progetto a un solo autore) con nuovo FR-019 che impone un verbale di revisione versionato; FR-008 vincola la natura della North Star e FR-020 vieta l'indice composito; FR-005a fissa lo schema di identificazione dei KPI e FR-005b la forma del catalogo; FR-016 chiarisce che il divieto di numeri riguarda gli esiti e non gli input, con FR-017a che colloca l'incertezza di BQ3 nel tasso di adozione e non nel prezzo. Riformulazioni per non introdurre dettagli implementativi nei criteri: i riferimenti a "agent AI" e "misura DAX" sono stati spostati fuori da Success Criteria e Clarifications. **16/16 item passano.**
- **Iterazione 4 (2026-08-07, dopo `/speckit.implement`)**: `docs/business_case.md` scritto, 27 task su 29 completati. Verifica strutturale superata: 8 KPI (3+3+2 per domanda), 8 sezioni, 6 voci fuori scope, nessuna sintassi tecnica nelle formule, entrambi i KPI a confidenza bassa espressi come range. Ispezione dei numeri (T025): 3 prezzi di scenario marcati come assunzioni in §2 e 2 caratteristiche dei dati di origine, nessun esito di calcolo. **Restano aperti T026 e T027**, la sessione di revisione in contesto pulito e il relativo verbale: non può condurla chi ha scritto il documento.
- **Nota sulla North Star**: in fase di scrittura è emerso un conflitto tra FR-008 (North Star a confidenza alta) e la decisione D1 (l'overlap di mood richiede una mappatura, quindi confidenza media). Risolto ridefinendo la North Star su un dato osservato direttamente — la quota di catalogo video già classificato come musicale — come prescrive T022: si ridefinisce la metrica, non si abbassa il criterio di confidenza.
