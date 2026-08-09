# Specification Quality Checklist: Data Audit & Profiling

- **Purpose**: Validate specification completeness and quality before proceeding to planning
- **Created**: 2026-08-08
- **Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs) — con una deroga dichiarata, vedi nota 1
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details) — vedi nota 2
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Constitution Gate (principi I, II, III, IV, VI)

- [x] Sezione "Domanda di Business" compilata — la feature serve BQ1+BQ2+BQ3 come feature fondativa e strumentale, con il contributo dichiarato domanda per domanda
- [x] Sezione "Limiti Dichiarati" compilata — 10 voci, incluse tre inferenze da evitare
- [x] Sezione "Provenienza e Confidenza dei Dati" compilata — 8 famiglie di valori, tutte a confidenza alta per il criterio D5 della 001, più il richiamo alla distinzione di `business_case.md` §6 su ciò che la scala non misura
- [x] Principio II presidiato dai requisiti, non solo citato — FR-002 (sola lettura di `data/raw/`), FR-003 (determinismo), FR-011 (artefatto rigenerato, mai modificato a mano), FR-007 (artefatto effettivamente tracciato da git)
- [x] Feature completabile in una giornata lavorativa (principio III) — stima ~4 ore, entro il limite di 6-7; il rischio di sforamento è dichiarato in Assumptions con il ripiego previsto, vedi nota 3

## Notes

1. **Deroga su "no implementation details"**: FR-001 nomina esplicitamente Python. Non è una scelta lasciata trapelare nella spec: il principio II della constitution ammette solo Python o Power Query M per le trasformazioni, e il prompt di consegna vincola alla prima. Restano fuori dalla spec, e demandate a `/speckit.plan`, tutte le scelte che erano davvero libere: formato dell'artefatto, sintassi della marcatura dei valori nel documento, forma del comando di coerenza, librerie.

2. **Nota su "technology-agnostic success criteria"**: SC-001 ("byte per byte"), SC-006 e SC-012 (`.gitignore`, copia pulita del repository) citano meccaniche di git e del filesystem. Non sono dettagli di stack: sono i vincoli di progetto entro cui la feature esiste — l'artefatto è utile solo se versionato, ed è precisamente ciò che `.gitignore` può annullare in silenzio. Renderli generici li avrebbe resi non verificabili.

3. **Rischio di stima**: la voce più esposta a crescere oltre le 4 ore è il controllo di coerenza fra prosa e numeri (FR-033-FR-036). La spec ne fissa l'esistenza e il comportamento osservabile, non il meccanismo, e dichiara in Assumptions il ripiego da adottare se in fase di piano dovesse gonfiarsi: la forma più semplice che soddisfa i quattro requisiti, mai l'abbandono del requisito. Da presidiare in `/speckit.plan`.

4. **Iterazione 1 (2026-08-08)**: tutti gli item passano alla prima scrittura, nessun marker [NEEDS CLARIFICATION] emesso. Le decisioni che il prompt di consegna non vincolava sono state prese come default e registrate in Assumptions anziché rimandate al lettore: collocazione dei tre artefatti (`scripts/`, `reports/`, `docs/`), esclusione delle figure, assenza di una revisione in contesto pulito. Nessuna di esse cambia il perimetro della feature; tutte sono reversibili in fase di piano.

5. **Verifica meccanica eseguita in fase di spec**: `git check-ignore` sui tre percorsi ipotizzati (`reports/data_profile.json`, `docs/data_audit.md`, `scripts/profile_data.py`) non ne intercetta nessuno. Il vincolo di FR-007 è quindi soddisfacibile sotto `reports/`, e l'avvertimento del prompt di consegna — un artefatto collocato sotto `data/interim/` o `data/processed/` sarebbe invisibile a git — è confermato dal contenuto di `.gitignore`.

6. **Rilevato in fase di spec, da verificare in implementazione**: il file del catalogo musicale espone una prima colonna **senza nome** (indice di riga della fonte), e il catalogo video ha **12 campi** mentre `research.md` della 001 ne profilava 9. FR-019 (nessun campo escluso in silenzio) e V02 (completezza di *tutti* i campi, non solo di quelli citati) coprono entrambi i casi: il profilo di questa feature sarà più ampio di quello che rigenera. **Confermato in implementazione**: 12 e 21 campi profilati, nessuna esclusione.

7. **Iterazione di implementazione (2026-08-08)**: 39 task su 39 completati. Prodotti `scripts/profile_data.py`, `scripts/check_audit_coherence.py`, `reports/data_profile.json` (1.025 valori) e `docs/data_audit.md` (103 marcatori). Nessuna voce dell'ordine di caduta dichiarato nel piano è stata usata: T033 è stato implementato e il dettaglio per genere degli zeri copre tutti e 114 i generi.

   **Verificati da comando**: SC-001 (due esecuzioni identiche byte per byte), SC-002 (sorgenti immutate, confronto di digest prima e dopo), SC-003 (14/14 sigle risolte), SC-004 (12+21 campi, zero esclusioni), SC-006 (esito 1 su valore alterato e su riferimento non risolvibile, esito 0 su documento intatto), SC-007 (controllo eseguito con `data/raw/` rimossa; il profiling fallisce con errore esplicito senza lasciare artefatti parziali), SC-012 (`git check-ignore` non intercetta l'artefatto).

   **Verificati per lettura**: SC-005 parte assistita (13 avvisi vagliati: 3 sono etichette di valori fuori dominio che vivono in `catalogs` e non in `values`, 2 sono percentuali retoriche, 1 è una soglia interna alla definizione di un valore, 4 sono riferimenti strutturali, 2 sono cifre citate dalla 001 e non dal profilo, 1 è la copertura temporale del catalogo musicale che il profilo dichiara di non poter verificare); SC-008, SC-009, SC-010, SC-011.

   **Due correzioni di perimetro applicate durante l'implementazione**. La prima: il valore `NF.cat.music.share` era stato prodotto ed è stato rimosso, perché titoli musicali diviso titoli totali **è** la formula di `BQ1-K1` e FR-039 vieta di calcolare KPI. Il profilo espone numeratore e denominatore, non il rapporto. La seconda: il contratto è stato esteso con un blocco `catalogs` per gli elenchi di etichette — nomi di categoria, di genere, valori fuori dominio — che non sono numeri e non potevano stare in `values` senza violare FR-006, ma servono a rendere auditabile un criterio che altrimenti resterebbe un conteggio senza referente.

8. **Debito dichiarato**: nessuna revisione in contesto pulito è stata condotta sul documento di audit, coerentemente con quanto la spec dichiarava in Assumptions. Resta un debito noto, non un'omissione.
