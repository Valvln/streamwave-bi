---

description: "Task list — Feature 002: Data Audit & Profiling"
---

# Tasks: Data Audit & Profiling

**Input**: documenti di design da `/specs/002-data-audit-profiling/`

**Prerequisiti**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/profile-artifact.md](./contracts/profile-artifact.md), [quickstart.md](./quickstart.md)

**Test**: nessun framework di test introdotto. La spec non richiede TDD e la feature ha quattro comportamenti verificabili da riga di comando — determinismo, immutabilità delle sorgenti, fallimento del controllo su documento alterato, esecuzione senza `data/raw/`. La verifica è quella di [quickstart.md](./quickstart.md) ed è distribuita nei task di verifica in coda a ciascuna fase. Un framework sarebbe più grande di ciò che verifica.

**Organizzazione**: i task sono raggruppati per user story, così ogni storia resta implementabile e verificabile in autonomia.

## Format: `[ID] [P?] [Story] Descrizione`

- **[P]**: eseguibile in parallelo (file diverso, nessuna dipendenza)
- **[Story]**: a quale user story appartiene (US1, US2, US3)
- Ogni descrizione riporta il percorso del file

## Nota sul parallelismo

Le tre storie scrivono in **tre file diversi**, quindi il parallelismo sarebbe teoricamente ampio. Non lo è nei fatti, per due ragioni: le storie sono in dipendenza stretta — il documento cita valori che devono esistere, il controllo verifica marcatori che devono essere scritti — e l'autore è uno solo. I `[P]` sono quindi marcati solo dove il file è diverso **e** la dipendenza è effettivamente assente: in pratica la sola Phase 6. Dentro ciascuna delle tre storie i task scrivono nello stesso file e vanno in sequenza.

---

## Phase 1: Setup

**Scopo**: predisporre la destinazione dell'artefatto e verificare subito il vincolo che potrebbe annullarsi in silenzio.

- [X] T001 Creare la cartella `reports/` e verificare con `git check-ignore -v reports/data_profile.json` che il percorso **non** sia intercettato da `.gitignore` (FR-007, SC-012). Se lo fosse, fermarsi: la collocazione va cambiata prima di scrivere una riga di script

---

## Phase 2: Foundational (prerequisiti bloccanti)

**Scopo**: fissare in codice le convenzioni del contratto. **Bloccano tutte e tre le storie**: sia l'artefatto sia il controllo di coerenza dipendono dalla stessa forma del record e dalla stessa formattazione.

- [X] T002 Creare `scripts/profile_data.py` con il blocco delle convenzioni di [research.md](./research.md) D9 — definizione di valore mancante, soglia di alta cardinalità, decimali di arrotondamento — destinato a finire nella chiave `conventions` dell'artefatto secondo [contracts/profile-artifact.md](./contracts/profile-artifact.md) §3
- [X] T003 Implementare in `scripts/profile_data.py` la serializzazione deterministica secondo le quattro regole di [research.md](./research.md) D5: chiavi ordinate, nessun timestamp di esecuzione, arrotondamento dichiarato, ordinamenti espliciti e senza pareggi ambigui (FR-003)
- [X] T004 Implementare in `scripts/profile_data.py` il costruttore del record di valore e il formattatore italiano che produce il campo `display` — separatore di migliaia `.`, decimale `,` — secondo [contracts/profile-artifact.md](./contracts/profile-artifact.md) §2. È la decisione D3: la formattazione vive qui e in nessun altro posto
- [X] T005 Implementare in `scripts/profile_data.py` l'impronta delle sorgenti (nome, byte, digest) per la chiave `sources` (FR-005) e la guardia di fallimento esplicito su file mancante o colonna assente, che non deve lasciare artefatti parziali (FR-004)

**Checkpoint**: contratto implementato. Le tre storie possono partire.

---

## Phase 3: User Story 1 — Chiunque può rigenerare i numeri invece di crederci (Priority: P1) 🎯 MVP

**Goal**: `python3 scripts/profile_data.py` produce `reports/data_profile.json`, artefatto versionato di soli numeri, deterministico, che rigenera tutti i valori che la 001 cita in prosa e risponde a R11.

**Independent Test**: eseguire lo script due volte e diffare i due artefatti; cercare poi nell'artefatto ciascuno dei quattordici valori dell'inventario di FR-020. Superata se le due esecuzioni coincidono e ogni sigla si risolve.

- [X] T006 [US1] Implementare in `scripts/profile_data.py` la lettura in sola lettura dei due CSV di `data/raw/` e il profilo di forma — righe, numero e nome dei campi, tipo osservato di ciascuno (FR-012). Il catalogo musicale ha una prima colonna **priva di nome**: va gestita come campo, non ignorata (ritrovamento F5)
- [X] T007 [US1] Implementare in `scripts/profile_data.py` la completezza per campo su **tutti** i campi dei due dataset — 12 sul lato video, 21 sul lato musicale — con conteggio e quota di valori mancanti secondo la convenzione di T002, più l'elenco esplicito dei campi non profilati con la ragione (FR-013, FR-019, SC-004)
- [X] T008 [US1] Implementare in `scripts/profile_data.py` cardinalità e frequenze dei campi categorici, con l'enumerazione completa sotto la soglia dichiarata e i soli valori più frequenti sopra (FR-014)
- [X] T009 [US1] Implementare in `scripts/profile_data.py` il trattamento del campo multi-valore delle categorie video: conteggi sia sulla stringa intera sia sull'insieme di etichette atomiche, ciascuno con la propria granularità dichiarata (FR-018)
- [X] T010 [US1] Implementare in `scripts/profile_data.py` la duplicazione degli identificativi di traccia — righe totali, identificativi distinti, quanti ripetuti — emettendo **entrambe** le letture della sovrapposizione come valori distinti: quota di righe che sono ripetizioni ed eccesso del totale non deduplicato sul deduplicato (FR-015, ritrovamento F2)
- [X] T011 [US1] Implementare in `scripts/profile_data.py` la struttura del campionamento: righe per genere musicale, in forma che renda visibile se il campione è bilanciato per costruzione (FR-016)
- [X] T012 [US1] Implementare in `scripts/profile_data.py` le distribuzioni delle variabili numeriche di entrambi i dataset con misure di posizione (minimo, quartili, mediana, massimo, media) e di dispersione (scarto interquartile e deviazione standard, entrambi — D9) (FR-017)
- [X] T013 [US1] Implementare in `scripts/profile_data.py` il conteggio dei valori sentinella e degeneri: zeri dell'indice di popolarità complessivi e per genere, valori fuori dal dominio della classificazione per età (F4), durate nulle o assenti (F6) (FR-017)
- [X] T014 [US1] Implementare in `scripts/profile_data.py` il **censimento completo** delle categorie del catalogo video — tutte, con i titoli distinti di ciascuna, nessuna selezione a monte — più il conteggio di quante hanno contenuto musicale dichiarato secondo un criterio esplicito registrato nell'artefatto (FR-021, ritrovamento F1)
- [X] T015 [US1] Implementare in `scripts/profile_data.py` il conteggio delle corrispondenze lessicali fra nomi di genere musicale e categorie video, con la **regola di confronto dichiarata** insieme al valore. Il conteggio cambia con la regola: è il ritrovamento F3 (FR-022)
- [X] T016 [US1] Implementare in `scripts/profile_data.py` la mappa `inventory_001` che risolve le sigle `V01`-`V14` di FR-020 sugli identificativi che le rigenerano (SC-003)
- [X] T017 [US1] Codificare in `scripts/profile_data.py` la tabella delle affermazioni della 001 — ciascuna con enunciato e collocazione — e produrre il blocco `divergences` confrontando ogni affermazione con i valori rigenerati, con stato `coincide`, `diverge` o `ambiguo` (decisione D6, FR-030). F2 e F3 sono già due ingressi attesi
- [X] T018 [US1] Completare `scripts/profile_data.py` con l'emissione di `reports/data_profile.json` secondo la struttura di [contracts/profile-artifact.md](./contracts/profile-artifact.md) §3
- [X] T019 [US1] Verificare US1 secondo [quickstart.md](./quickstart.md): doppia esecuzione e diff (SC-001), immutabilità di `data/raw/` (SC-002), risoluzione delle quattordici sigle (SC-003), copertura di tutti i campi (SC-004), presenza della risposta a R11 (SC-008), artefatto tracciato (SC-012)

**Checkpoint**: l'artefatto esiste, è versionabile e rigenerabile. Il rilievo R8 è chiuso sul piano della riproducibilità anche se nessuno ha ancora scritto una riga di prosa.

---

## Phase 4: User Story 2 — Chi legge capisce cosa i dati permettono e cosa impediscono (Priority: P2)

**Goal**: `docs/data_audit.md` interpreta il profilo, cita ogni numero tramite marcatore e dichiara cosa i ritrovamenti vincolano a valle.

**Independent Test**: consegnare il solo documento a chi non ha visto i dati e chiedergli, per due misure del framework 001 a scelta, se i campi che servono esistono, più due fragilità dei dataset con il numero che le sostiene.

- [X] T020 [US2] Creare `docs/data_audit.md` con la sola struttura di heading: inquadramento, profilo del catalogo video, profilo del catalogo musicale, ritrovamenti e conseguenze, copertura delle misure del framework 001, divergenze rispetto alla 001, provenienza e confidenza, limiti dichiarati
- [X] T021 [US2] Scrivere in `docs/data_audit.md` l'inquadramento, includendo la nota breve che spiega perché questo documento è pieno di numeri mentre `docs/business_case.md` dichiara di non contenerne: il divieto FR-016 della 001 era locale a quel documento (FR-029)
- [X] T022 [US2] Scrivere in `docs/data_audit.md` il profilo del catalogo video — dimensioni, completezza, categorie, durate, valori fuori dominio — marcando ogni valore con la sintassi `valore<!--@ID-->` di [contracts/profile-artifact.md](./contracts/profile-artifact.md) §4 (FR-024, FR-025)
- [X] T023 [US2] Scrivere in `docs/data_audit.md` il profilo del catalogo musicale — dimensioni, completezza, duplicazione degli identificativi, struttura del campionamento, distribuzioni, massa di zeri — con la stessa marcatura (FR-024)
- [X] T024 [US2] Scrivere in `docs/data_audit.md` la sezione dei ritrovamenti: per ciascuno, cosa vincola a valle — quale granularità è obbligata, dove un totale ingenuo sbaglierebbe, quale fragilità un KPI erediterà (FR-026)
- [X] T025 [US2] Scrivere in `docs/data_audit.md` la risposta a R11: quante e quali categorie hanno contenuto musicale dichiarato, il criterio di riconoscimento applicato, e la conseguenza per la confidenza di `BQ1-K1` — una sola categoria significa nessuna mappatura e confidenza alta confermata (FR-021, SC-008). **Registrare l'esito, non ridefinire la North Star**
- [X] T026 [US2] Scrivere in `docs/data_audit.md` la copertura delle otto misure del framework 001: per ciascuna, se i campi che la alimentano esistono e con quale completezza. È una constatazione sui campi, **non** un giudizio di idoneità della misura (FR-027, FR-040, SC-009)
- [X] T027 [US2] Scrivere in `docs/data_audit.md` la sezione delle divergenze rispetto alla 001, alimentata dal blocco `divergences` dell'artefatto: valore citato, valore rigenerato, dove compariva, ipotesi sulla causa (FR-030, SC-010)
- [X] T028 [US2] Scrivere in `docs/data_audit.md` le sezioni di provenienza e confidenza e di limiti dichiarati, riprendendo le otto famiglie di valori della spec e le dieci voci di limite, inclusa la distinzione di `business_case.md` §6 su ciò che la scala non misura (FR-028)
- [X] T029 [US2] Verificare US2 per lettura: nessun valore di KPI e nessuna risposta anche parziale a BQ1, BQ2 o BQ3 nel documento (FR-039, SC-011)

**Checkpoint**: il profilo è leggibile e interpretato. Il documento sta in piedi anche prima che il controllo di coerenza esista.

---

## Phase 5: User Story 3 — Prosa e numeri non possono divergere in silenzio (Priority: P3)

**Goal**: `python3 scripts/check_audit_coherence.py` confronta ogni valore marcato con l'artefatto e fallisce se qualcosa non torna.

**Independent Test**: alterare un singolo valore marcato nel documento ed eseguire il comando. Superata se fallisce e nomina il valore.

- [X] T030 [US3] Creare `scripts/check_audit_coherence.py` con il riconoscimento dei marcatori `valore<!--@ID-->` secondo la grammatica di [contracts/profile-artifact.md](./contracts/profile-artifact.md) §4 e il confronto carattere per carattere fra il testo che precede il marcatore e il campo `display` (FR-033)
- [X] T031 [US3] Implementare in `scripts/check_audit_coherence.py` l'uscita con stato di errore su divergenza, con messaggio che riporta identificativo, valore atteso e valore trovato (FR-034)
- [X] T032 [US3] Implementare in `scripts/check_audit_coherence.py` l'errore su riferimento non risolvibile — marcatore che punta a un identificativo assente da `values` — e su sigla di `inventory_001` che non si risolve (FR-035)
- [X] T033 [US3] Implementare in `scripts/check_audit_coherence.py` l'avviso **non bloccante** sui gruppi di cifre non adiacenti ad alcun marcatore, come lista da vagliare a occhio (decisione D8). È il primo elemento a cadere se il tempo stringe
- [X] T034 [US3] Verificare US3 secondo [quickstart.md](./quickstart.md): esito positivo su documento intatto e negativo su documento alterato (SC-006), esecuzione con `data/raw/` rimossa (SC-007, FR-036), lettura degli avvisi per la parte assistita di SC-005

**Checkpoint**: l'ibrido documento-più-artefatto è protetto. Tutte e tre le storie sono complete.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Scopo**: chiudere il debito verso la 001 e lasciare il repository coerente.

- [X] T035 [P] Applicare agli artefatti della 001 una nota datata per ciascuna divergenza con stato `diverge` o `ambiguo`, con il valore corretto e la ragione del cambiamento, **senza cancellare il valore originale** (FR-031). I file interessati sono `docs/business_case.md` e `specs/001-business-case-kpi/research.md`
- [X] T036 [P] Aggiornare `README.md` con i due comandi della feature — rigenerazione del profilo e controllo di coerenza — nella sezione Setup, accanto a `scripts/download_data.sh`
- [X] T037 [P] Aggiornare `specs/002-data-audit-profiling/checklists/requirements.md` con l'iterazione di implementazione: cosa è stato prodotto, quali criteri sono verificati da comando e quali per lettura
- [X] T038 Eseguire integralmente [quickstart.md](./quickstart.md) nell'ordine consigliato e registrare l'esito dei dodici criteri di successo
- [X] T039 Verificare il perimetro: nessuna trasformazione persistente prodotta (FR-037), nessuna decisione presa sulle tracce a popolarità zero (FR-038), §3 di `docs/business_case.md` **non** corretta perché è debito testuale assegnato altrove (FR-032)

---

## Dependencies & Execution Order

### Dipendenze di fase

- **Phase 1 (Setup)**: nessuna dipendenza. È il primo task perché verifica il vincolo che, se violato, invalida tutto il resto
- **Phase 2 (Foundational)**: dipende da Phase 1. **Blocca tutte e tre le storie**
- **Phase 3 (US1)**: dipende da Phase 2
- **Phase 4 (US2)**: dipende da US1 — non si citano valori che non esistono
- **Phase 5 (US3)**: dipende da Phase 2 per il contratto e da US2 per avere marcatori da verificare
- **Phase 6 (Polish)**: dipende da US1 per il blocco delle divergenze e da US2 per la sezione che le registra

### Dipendenze fra storie

Le tre storie sono **incrementali, non indipendenti**, e la ragione è strutturale: US2 cita ciò che US1 produce, US3 verifica ciò che US2 scrive. Ciascuna lascia però il repository in uno stato consegnabile, che è ciò che il principio III richiede.

### Opportunità di parallelizzazione

Reali solo in Phase 6, dove i tre task marcati `[P]` toccano file diversi e non dipendono l'uno dall'altro:

```bash
# T035 -> docs/business_case.md, specs/001-business-case-kpi/research.md
# T036 -> README.md
# T037 -> specs/002-data-audit-profiling/checklists/requirements.md
```

Dentro Phase 3, Phase 4 e Phase 5 i task scrivono ciascuno nello stesso file della propria fase: vanno in sequenza.

---

## Strategia di implementazione

### Ordine di esecuzione consigliato, diverso dall'ordine di priorità

Le fasi sono numerate in ordine di priorità delle storie, come vuole il formato. L'ordine di **esecuzione** che consiglio devia in un punto: costruire il controllo di coerenza (T030-T032) **subito dopo** T018, prima di scrivere il corpo del documento.

La ragione è pratica. Il documento conterrà qualche decina di marcatori scritti a mano; averli verificati mentre si scrive significa correggere un marcatore sbagliato nel paragrafo in cui lo si è scritto, invece di scoprirne otto insieme a fine giornata. Il controllo dipende solo dal contratto e dall'artefatto, non dal documento, quindi è costruibile appena l'artefatto esiste.

Ordine consigliato: **T001-T019 → T030-T032 → T020-T029 → T033-T034 → T035-T039**.

### MVP: solo User Story 1

Phase 1 → Phase 2 → Phase 3 → verifica T019. Il risultato è lo script e l'artefatto versionato: nessun numero sui dati reali resta affidato alla parola dell'analista, e il rilievo R8 è chiuso sul piano della riproducibilità. È già consegnabile e già difendibile, anche senza una riga di prosa.

### Consegna incrementale

1. **Phase 1 + 2 + 3** → script e artefatto (MVP)
2. **Phase 4** → documento di audit leggibile
3. **Phase 5** → protezione contro la divergenza
4. **Phase 6** → debito verso la 001 chiuso e repository coerente

Ogni stadio lascia il repository in uno stato presentabile, come richiede il principio III.

### Vincolo di tempo

39 task per una feature stimata **~4 ore**. La ripartizione del piano: ~1,75 ore su Phase 2 e 3, ~0,25 sul confronto con le affermazioni della 001 (T017), ~0,5 su Phase 5, ~1,5 su Phase 4.

Il blocco che può sforare è la Phase 3, perché il ritrovamento F5 la allarga a dodici campi invece dei nove che la 001 profilava e perché i casi particolari — colonna senza nome, campo multi-valore, valori fuori dominio — vanno gestiti ognuno esplicitamente.

**Se il tempo stringe, l'ordine di caduta è dichiarato in anticipo**:

1. cade **T033**, l'avviso sui gruppi di cifre non marcati: è un ausilio alla revisione, e FR-033-FR-036 restano soddisfatti senza;
2. cade il dettaglio **per genere** della concentrazione degli zeri dentro T013, riducendolo ai generi che la 001 cita invece che a tutti e 114.

**Non cadono in nessun caso** il determinismo (T003), il censimento completo delle categorie (T014), il registro delle divergenze (T017) e la marcatura (T004, T022-T023): sono i quattro punti per cui la feature esiste. Se dovessero essere loro a non entrare nella giornata, la risposta corretta è scomporre la feature, non consegnarla monca.

---

## Note

- Nessun task presuppone l'interazione con GUI di Power BI o Tableau (principio V)
- Nessun task scrive in `data/raw/`, che resta in sola lettura (principio II, FR-002)
- I riferimenti `F1`-`F6` e `D1`-`D9` rimandano ai ritrovamenti e alle decisioni di [research.md](./research.md)
- I riferimenti `FR-xxx` e `SC-xxx` rimandano ai requisiti e ai criteri di successo di [spec.md](./spec.md)
- I riferimenti `R8`, `R11` e `V01`-`V14` rimandano rispettivamente ai rilievi di [`specs/001-business-case-kpi/review.md`](../001-business-case-kpi/review.md) e all'inventario di FR-020
