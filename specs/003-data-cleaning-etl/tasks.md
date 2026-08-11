---

description: "Task list — Feature 003: Data Cleaning & ETL"
---

# Tasks: Data Cleaning & ETL

**Input**: documenti di design da `/specs/003-data-cleaning-etl/`

**Prerequisiti**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/output-datasets.md](./contracts/output-datasets.md), [quickstart.md](./quickstart.md)

**Test**: nessun framework di test introdotto, per la stessa ragione della 002. I comportamenti verificabili sono una decina e si verificano da riga di comando: determinismo, immutabilità delle sorgenti, coincidenza delle impronte, unicità delle grane, fallimento del controllo su documento alterato, esecuzione senza `data/raw/`. La verifica è quella di [quickstart.md](./quickstart.md) ed è distribuita nei task di verifica in coda a ciascuna fase.

**Organizzazione**: i task sono raggruppati per user story, così ogni storia resta implementabile e verificabile in autonomia.

## Format: `[ID] [P?] [Story] Descrizione`

- **[P]**: eseguibile in parallelo (file diverso, nessuna dipendenza)
- **[Story]**: a quale user story appartiene (US1, US2, US3)
- Ogni descrizione riporta il percorso del file

## Nota sul parallelismo

Vale la stessa constatazione della 002 e per gli stessi motivi: le tre storie scrivono in file diversi, ma sono in dipendenza stretta — il documento cita valori che devono esistere, il controllo verifica marcatori che devono essere scritti — e l'autore è uno solo. I `[P]` sono marcati dove il file è diverso **e** la dipendenza è effettivamente assente. Dentro ciascuna storia i task scrivono nello stesso file e vanno in sequenza.

## Nota sulle sigle

`D1`-`D5` sono le **decisioni ereditate** dalle revisioni della 001 e della 002, chiuse nella [spec](./spec.md). `F1`-`F8` e `T1`-`T11` sono i **ritrovamenti** e le **decisioni tecniche** di [research.md](./research.md). `FR-xxx` e `SC-xxx` rimandano a requisiti e criteri di successo della spec.

---

## Phase 1: Setup

**Scopo**: verificare i due vincoli di collocazione prima di scrivere una riga, perché entrambi si annullerebbero in silenzio.

- [X] T001 Verificare con `git check-ignore -v reports/cleaning_report.json` che il percorso **non** sia intercettato da `.gitignore` (FR-025, SC-004). Se lo fosse, fermarsi: la collocazione va cambiata prima di scrivere la pipeline
- [X] T002 Verificare con `git check-ignore -v data/processed/netflix_titles.csv` che gli output **siano** intercettati, e che `data/processed/.gitkeep` resti tracciato (FR-007, SC-004). È il vincolo speculare al precedente e va verificato con la stessa cura: un output che finisce nella history è un output che qualcuno citerà invece di rigenerarlo

---

## Phase 2: Foundational (prerequisiti bloccanti)

**Scopo**: fissare in codice le convenzioni del contratto e le guardie che rendono difendibile tutto il resto. **Bloccano tutte e tre le storie**: pipeline, artefatto di rendicontazione e controllo dipendono dalla stessa forma del record e dalle stesse invarianti.

- [X] T003 Creare `scripts/build_datasets.py` con il blocco delle convenzioni di questa feature, destinato alla chiave `conventions` di `reports/cleaning_report.json` secondo [contracts/output-datasets.md](./contracts/output-datasets.md) §2.2: soglia del 50% di D4, regola del massimo di T5, forma sintattica riconosciuta dalla riparazione di D2, mappa esplicita dei dodici mesi di T6
- [X] T004 Implementare in `scripts/build_datasets.py` la lettura in sola lettura dei due CSV di `data/raw/` e la **verifica dell'impronta** contro il blocco `sources` di `reports/data_profile.json` (T10, data-model §1). Se le impronte divergono, segnalarlo in modo esplicito: ogni identificativo del profilo che il documento citerà descriverebbe altri dati
- [X] T005 Implementare in `scripts/build_datasets.py` lo scrittore CSV deterministico secondo T4 — terminatore `\n`, quoting minimale, UTF-8 senza BOM, intestazione, nessuna riga finale vuota. Due campi del catalogo video contengono un a capo incorporato (F8): la scrittura deve quotare correttamente, ed è l'unica ragione per cui non si può concatenare stringhe
- [X] T006 Implementare in `scripts/build_datasets.py` il costruttore del record di valore e il formattatore italiano del campo `display`, riusando le convenzioni del contratto della 002 §2. Il prefisso degli identificativi è `CL.` e la pipeline **verifica** che non collida con alcun identificativo del profilo (T8, data-model §4)
- [X] T007 Implementare in `scripts/build_datasets.py` il motore delle invarianti di T10: una funzione che asserisce e, in caso di violazione, ferma l'esecuzione con un messaggio che nomina l'invariante e i valori trovati, **senza** lasciare output parziali (FR-004). È il pezzo su cui poggia la difendibilità di D2

**Checkpoint**: convenzioni, determinismo e guardie in piedi. Le tre storie possono partire.

---

## Phase 3: User Story 1 — Chiunque abbia i dati di origine ottiene gli stessi dataset (Priority: P1) 🎯 MVP

**Goal**: `python3 scripts/build_datasets.py` produce quattro CSV sotto `data/processed/` e `reports/cleaning_report.json` versionato, in modo deterministico, lasciando `data/raw/` intatto.

**Independent Test**: eseguire la pipeline due volte e diffare gli output; confrontare le impronte registrate con quelle dei file rigenerati; verificare che le quattro grane siano uniche. Superata se le due esecuzioni coincidono, le impronte tornano e nessuna chiave si ripete.

### Catalogo video

- [X] T008 [US1] Implementare in `scripts/build_datasets.py` la separazione del campo `duration` in `movie_duration_min` e `tvshow_seasons` (FR-014), con l'invariante di F5: ogni `Movie` porta minuti, ogni `TV Show` porta stagioni, nessuna forma terza. È una **verifica**, non una deduzione dalla stringa: se fallisce, la fonte è cambiata e la pipeline si ferma
- [X] T009 [US1] Implementare in `scripts/build_datasets.py` la riparazione dello scivolamento di colonna della decisione ereditata **D2**: spostare nel campo durata il valore del campo di classificazione che soddisfa la forma dichiarata, su righe con durata vuota; porre a mancante la classificazione di quelle righe; marcarle con `is_repaired_duration`. Il raggio d'azione atteso è di **tre** righe (F1) e la pipeline si ferma se ne tocca un numero diverso (FR-016, FR-004)
- [X] T010 [US1] Implementare in `scripts/build_datasets.py` il controllo di dominio sul campo di classificazione contro `conventions.rating_domain` del profilo: i valori fuori dominio residui vanno posti a mancante e contati, mai indovinati (FR-015). Il controllo di dominio e la riparazione di T009 sono **due operazioni distinte**, e la seconda non è la conseguenza automatica della prima
- [X] T011 [US1] Implementare in `scripts/build_datasets.py` la conversione di `date_added` in ISO 8601 usando la mappa dei mesi di T003 e normalizzando lo spazio iniziale degli 88 valori di F6. **Vietato** `strptime` con `%B`, che dipende dal locale e produrrebbe risultati diversi su macchine diverse (T6, FR-003)
- [ ] T012 [US1] Produrre `data/processed/netflix_titles.csv` secondo [contracts/output-datasets.md](./contracts/output-datasets.md) §1.1, con tutti e quattordici i campi, l'ordine di sorgente (T3) e l'invariante di grana su `show_id` (FR-011). **Nessuna riga eliminata**, incluse le tre riparate (FR-017, SC-010)
- [ ] T013 [US1] Produrre `data/processed/netflix_title_category.csv` normalizzando il solo campo `listed_in` (FR-012, T7), con l'invariante di grana su `show_id` + `category` e il conteggio delle righe che deve coincidere con `NF.cat.assignments` del profilo

### Catalogo musicale

- [ ] T014 [US1] Implementare in `scripts/build_datasets.py` la deduplicazione della grana **coppia traccia-genere** (F2): rimuovere le 450 righe eccedenti conservando la prima occorrenza (T3), dopo aver **verificato** che le repliche siano identiche su ogni attributo. Se non lo fossero, la deduplicazione non sarebbe più priva di perdita e la pipeline deve fermarsi
- [ ] T015 [US1] Implementare in `scripts/build_datasets.py` le marcature della decisione ereditata **D1** — `is_popularity_zero` — e di `is_duration_zero` (FR-020, FR-023). **Nessuna riga eliminata** per il valore di popolarità (FR-022, SC-010)
- [ ] T016 [US1] Implementare in `scripts/build_datasets.py` il criterio della decisione ereditata **D4**: ricalcolare la quota di righe a popolarità zero per genere **sulla grana coppia del dataset trasformato**, non riprenderla dal profilo, e marcare con `is_high_zero_genre` i generi che superano il 50% (FR-021, F4). Registrare anche la quota del genere più vicino da sotto, che serve alla dichiarazione di sensibilità obbligatoria
- [ ] T017 [US1] Produrre `data/processed/spotify_track_genre.csv` secondo il contratto §1.3, senza la colonna indice priva di nome (T11), con l'invariante di grana su `track_id` + `track_genre`
- [ ] T018 [US1] Implementare in `scripts/build_datasets.py` la deduplicazione alla grana **traccia** con la regola di T5: dove le repliche discordano su `popularity` si conserva il **massimo osservato**. Marcare le righe interessate con `has_conflicting_popularity` e calcolare `genre_count`. Verificare che il disaccordo riguardi **solo** `popularity` (F3): se toccasse altri attributi, la regola dichiarata non li coprirebbe e la pipeline deve fermarsi
- [ ] T019 [US1] Produrre `data/processed/spotify_tracks.csv` secondo il contratto §1.4, con l'invariante di grana su `track_id` e il conteggio che deve coincidere con `SP.id.distinct` del profilo

### Artefatto di rendicontazione

- [ ] T020 [US1] Implementare in `scripts/build_datasets.py` il blocco `values` di `reports/cleaning_report.json`: **almeno un** valore `CL.` per ciascuna delle nove decisioni di trattamento di [data-model.md](./data-model.md) §2, incluse quelle che toccano zero righe (FR-024, FR-029). Una decisione che tocca zero righe si dichiara con il suo zero: il lettore non può distinguere «non è stato necessario» da «non è stato fatto»
- [ ] T021 [US1] Implementare in `scripts/build_datasets.py` i blocchi `sources`, `conventions`, `catalogs` e `outputs` secondo il contratto §2.2. `outputs` registra per ciascun file percorso, righe, colonne, byte e `sha256` (FR-008): è ciò che sostituisce la versionatura degli output
- [ ] T022 [US1] Implementare in `scripts/build_datasets.py` il blocco `denominators` **per ricalcolo e confronto** (data-model §5): ricalcolare sul dato trasformato i valori del profilo esposti al cambiamento, confrontarli, e registrare automaticamente quelli che differiscono con `profile_id`, `cleaning_id`, ragione e ambito. Le voci attese dalla Fase 0 sono le durate dei film, la completezza della classificazione, le righe del catalogo musicale e le quote di zeri dei 48 generi di F4 — ma l'elenco lo produce l'esecuzione, non la memoria di chi scrive (FR-030)
- [ ] T023 [US1] Implementare in `scripts/build_datasets.py` la serializzazione deterministica di `reports/cleaning_report.json` con le stesse quattro regole del profilo: chiavi ordinate, nessun timestamp di esecuzione, arrotondamento dichiarato, ordinamenti espliciti (FR-003)
- [ ] T024 [US1] Implementare in `scripts/build_datasets.py` la validazione dei tipi dichiarati nel contratto §1.1-§1.4 su ogni campo di ogni output (T2, FR-009): un valore che non rispetta il tipo dichiarato ferma la pipeline. È ciò che rende vero il contratto in un formato che i tipi non li porta

### Verifica della storia

- [ ] T025 [US1] Eseguire le verifiche SC-001, SC-002, SC-003, SC-009 e SC-010 di [quickstart.md](./quickstart.md): doppia esecuzione e diff, immutabilità di `data/raw/`, coincidenza delle impronte, unicità delle quattro grane, nessuna riga eliminata oltre alla deduplicazione. Registrare l'esito
- [ ] T026 [US1] Verificare con `git status --porcelain data/` che nessun output sia tracciato e con `git check-ignore` che `reports/cleaning_report.json` non lo sia (SC-004)

**Checkpoint**: la pipeline esiste ed è verificabile. Il repository è coerente e consegnabile anche senza una riga di prosa.

---

## Phase 4: User Story 2 — Chi legge sa cosa è stato fatto ai dati e quanto pesa (Priority: P2)

**Goal**: `docs/data_cleaning.md` dichiara le nove decisioni di trattamento e le cinque ereditate, ciascuna con ragione, effetto quantificato e ancora al profilo.

**Independent Test**: consegnare il solo documento a un lettore che non ha i dati e chiedergli, per tre decisioni a scelta, quante righe toccano e su quale osservazione del profilo poggiano. Superata se ci riesce senza eseguire nulla.

> **Ordine di esecuzione consigliato**: costruire prima la Phase 5. Vedi «Strategia di implementazione».

- [ ] T027 [US2] Creare `docs/data_cleaning.md` con l'impianto: perché esiste, cosa contiene, quali artefatti cita, e la dichiarazione di FR-033 su **cosa il controllo di coerenza copre e cosa no**. Il confine va scritto qui perché estendere la copertura lo sposta invece di eliminarlo — è la lezione che la 002 ha già pagato
- [ ] T028 [US2] Scrivere in `docs/data_cleaning.md` la sezione delle **cinque decisioni ereditate** D1-D5, ciascuna dichiarata chiusa con opzioni, decisione, ragione ed effetto (FR-031, SC-006). Nessuna può essere rinviata a una feature successiva
- [ ] T029 [US2] Scrivere in `docs/data_cleaning.md` le **nove decisioni di trattamento** di [data-model.md](./data-model.md) §2, ciascuna con enunciato, ragione, effetto quantificato ancorato a un identificativo `CL.` e riferimento all'identificativo del profilo che la motiva (FR-029, SC-005)
- [ ] T030 [US2] Scrivere in `docs/data_cleaning.md` la sezione dei **valori che cambiano**, alimentata dal blocco `denominators`: ogni valore che dopo la trasformazione differisce dal profilo, accanto all'identificativo del profilo da cui differisce, con la ragione (FR-030, SC-007). È la sezione che protegge dal citare l'uno credendo di citare l'altro
- [ ] T031 [US2] Scrivere in `docs/data_cleaning.md` la quantificazione della **perdita della deduplicazione** (FR-019): quante tracce hanno repliche in disaccordo, su quale attributo, con quale dispersione, e la distorsione verso l'alto che la regola del massimo introduce. Dichiarare la regola senza dichiarare quanto pesa non è dichiararla
- [ ] T032 [US2] Scrivere in `docs/data_cleaning.md` la dichiarazione di **sensibilità della soglia** di D4: i generi selezionati, la distanza del più vicino da sotto e da sopra, e il fatto che una lista prodotta da un taglio non è una proprietà naturale dei dati. Registrare che l'insieme è invariante alla trasformazione (F4) come constatazione, non come giustificazione della soglia
- [ ] T033 [US2] Scrivere in `docs/data_cleaning.md` l'elenco dei **campi esclusi dagli output** con la ragione — la sola colonna indice priva di nome (T11) — e la nota su `country`, `cast` e `director`, che restano non normalizzati e lasciano aperto lo stesso problema di sommabilità (T7, FR-010, SC-008)
- [ ] T034 [US2] Scrivere in `docs/data_cleaning.md` le sezioni obbligatorie dei principi I e IV: provenienza e confidenza delle sei famiglie di valori, incluse le due a confidenza **media** con la ragione della distinzione, e i limiti dichiarati della spec — pulizia non è correttezza semantica, copertura 2021 e 2022, output non ispezionabili da chi non può rigenerarli, quattro inferenze da evitare (FR-034)
- [ ] T035 [US2] Marcare **ogni** numerale del documento secondo il contratto §3: ancora a un identificativo per i fatti misurati, `<!--#-->` per i non misurati (FR-032, T9). È il task più lento della fase e il più facile da rimandare a dopo: rimandarlo significa rileggere il documento intero invece di decidere una frase alla volta

**Checkpoint**: il documento esiste e le decisioni sono contestabili.

---

## Phase 5: User Story 3 — Prosa, pipeline e profilo non possono divergere in silenzio (Priority: P3)

**Goal**: `python3 scripts/check_audit_coherence.py` verifica `docs/data_cleaning.md` contro i due artefatti, fallisce sulle divergenze e sui numerali non marcati, e funziona senza `data/raw/`.

**Independent Test**: alterare un valore ancorato ed eseguire il comando; aggiungere poi una cifra priva di entrambi i marcatori ed eseguirlo di nuovo. Superata se fallisce in entrambi i casi e dice cosa non va.

- [ ] T036 [US3] Estendere `scripts/check_audit_coherence.py` alla risoluzione su **spazio di nomi unito** dei due artefatti, verificando l'assenza di collisioni fra i prefissi (contratto §3.3, T8) invece di assumerla
- [ ] T037 [US3] Implementare in `scripts/check_audit_coherence.py` la **quarta forma di marcatura**, `<!--#-->`, secondo il contratto §3.1: non verifica il valore, registra che la decisione è stata presa
- [ ] T038 [US3] Implementare in `scripts/check_audit_coherence.py` la **severità per documento** del contratto §3.2: su `docs/data_cleaning.md` una cifra o un numerale privo di entrambi i marcatori è un **errore**; su `docs/data_audit.md` resta un avviso. È il corollario (c) della decisione ereditata D5 (FR-040)
- [ ] T039 [US3] Verificare che `scripts/check_audit_coherence.py` continui a trattare `docs/data_audit.md` esattamente come prima: stesso esito, stessi avvisi. Una modifica che rompe la verifica di un documento già mergiato è una regressione, non un'estensione
- [ ] T040 [US3] Eseguire le verifiche SC-011, SC-012 e SC-013 di [quickstart.md](./quickstart.md), incluse le **due prove di alterazione** e la prova senza `data/raw/`. Se la prova sul numerale non discrimina fra i due documenti, la severità non è stata implementata per documento

**Checkpoint**: il documento non può più divergere dagli artefatti in silenzio.

---

## Phase 6: Polish & debito verso gli artefatti mergiati

**Scopo**: chiudere ciò che questa feature deve agli artefatti già mergiati e lasciare il repository coerente.

- [ ] T041 [P] Aggiungere in §5.2 di `docs/business_case.md` la **nota in loco** della decisione ereditata D3, accanto alla nota di correzione del 2026-08-09: data, feature, letture possibili, lettura adottata, ragione, fonte verificabile. Il testo originale e la nota precedente **non** vanno cancellati né riscritti (FR-035)
- [ ] T042 [P] Aggiungere in §3.5 di `docs/data_audit.md` la **nota in loco** della decisione ereditata D4, dove il criterio riclassifica l'insieme dei generi rispetto a quanto quella sezione presentava, con la stessa prassi (FR-036)
- [ ] T043 Verificare con `git diff main -- docs/business_case.md docs/data_audit.md` che il diff contenga **solo righe aggiunte**: zero rimosse, zero modificate (SC-015). Una riga rimossa è una violazione della prassi di `CLAUDE.md`, non una rifinitura
- [ ] T044 Registrare in `docs/data_cleaning.md` i **ritrovamenti che questa feature non chiude**: la grana coppia non unica come fatto non registrato dalla 002 (F2), e la severità del controllo non estesa a `docs/data_audit.md` (T9), che richiederebbe di rimarcare un documento mergiato. Precedente: FR-032 della 002 — si registra e ci si ferma
- [ ] T045 Eseguire le verifiche SC-005, SC-006, SC-008 e SC-014 di [quickstart.md](./quickstart.md), incluse le due che si verificano **per lettura** e non per comando
- [ ] T046 Sottoporre `docs/data_cleaning.md` a **revisione in contesto pulito** secondo la prassi di `CLAUDE.md`: sessione separata, solo l'artefatto, senza spec, senza piano, senza history git. Produrre `specs/003-data-cleaning-etl/review.md`
- [ ] T047 Chiudere i rilievi della revisione dentro questa feature, prima del merge, come ha fatto la 002. Dove un rilievo richiede una decisione oltre la correzione, registrarla in coda al verbale senza modificare il verbale stesso
- [ ] T048 Riportare alla regia la **regola sulle affermazioni derivate** nel testo che ne è uscito (decisione ereditata D5), perché la porti in `CLAUDE.md`. È atto di governance e non appartiene a questa feature

---

## Dipendenze e ordine delle storie

```text
Phase 1 (Setup) ──> Phase 2 (Foundational) ──┬──> Phase 3 (US1) ──> Phase 4 (US2)
                                             │                          │
                                             └──> Phase 5 (US3) <───────┘
                                                          │
                                                          └──> Phase 6 (Polish)
```

- **US1** non dipende da nulla oltre la Phase 2. È il MVP
- **US2** dipende da US1: ogni effetto quantificato deve provenire da un'esecuzione reale
- **US3** dipende dalla Phase 2 e dall'esistenza dell'artefatto di rendicontazione, **non** dal documento. È la ragione dell'ordine consigliato qui sotto
- **Phase 6** dipende da tutte

### Opportunità di parallelismo

Poche e tutte in Phase 6: **T041 e T042** toccano file diversi e non dipendono l'uno dall'altro. Altrove il parallelismo è teorico — file diversi, ma dipendenza reale e un solo autore.

---

## Strategia di implementazione

### Ordine di esecuzione consigliato, diverso dall'ordine di priorità

Le fasi sono numerate in ordine di priorità delle storie, come vuole il formato. L'ordine di **esecuzione** devia in un punto, esattamente come nella 002: costruire il controllo di coerenza (**T036-T039**) subito dopo T023, prima di scrivere il corpo del documento.

La ragione è la stessa e vale di più qui. T035 impone di marcare **ogni** numerale del documento, non solo i valori: sono qualche centinaio di micro-decisioni. Averle verificate mentre si scrive significa correggere un marcatore nel paragrafo in cui lo si è scritto; scoprirle a fine giornata significa rileggere tutto. Il controllo dipende solo dal contratto e dagli artefatti, non dal documento, quindi è costruibile appena `cleaning_report.json` esiste.

Ordine consigliato: **T001-T026 → T036-T039 → T027-T035 → T040 → T041-T048**.

### MVP: solo User Story 1

Phase 1 → Phase 2 → Phase 3 → verifica T025-T026. Il risultato è la pipeline e l'artefatto di rendicontazione versionato: i dataset esistono, sono rigenerabili identici, e ogni decisione di trattamento è misurata. È già consegnabile, anche senza una riga di prosa — e le feature 005 e 007 potrebbero già partirci sopra leggendo il contratto.

### Consegna incrementale

1. **Phase 1 + 2 + 3** → pipeline e artefatto di rendicontazione (MVP)
2. **Phase 5** → protezione contro la divergenza, costruita prima di ciò che protegge
3. **Phase 4** → documento leggibile e decisioni contestabili
4. **Phase 6** → debito verso gli artefatti mergiati chiuso, revisione, repository coerente

Ogni stadio lascia il repository in uno stato presentabile, come richiede il principio III.

### Vincolo di tempo

48 task per una feature stimata **7 ore, revisione inclusa**. Ripartizione dal piano: ~2,5 ore su Phase 2 e 3, ~0,5 sull'artefatto di rendicontazione (T020-T024), ~0,75 su Phase 5, ~1,75 su Phase 4, ~0,25 su T041-T043, ~1,0 su T046-T047.

**Il margine è nullo.** Sette ore su un limite di sei-sette, e la Fase 0 ha aggiunto una decisione di trattamento che la spec non prevedeva (F2, task T014).

**Se il tempo stringe, l'ordine di caduta è dichiarato in anticipo**:

1. cade il **dettaglio per genere** in `cleaning_report.json` dentro T016: le quote ricalcolate dei 114 generi si riducono ai sette selezionati più i due limitrofi, che è ciò di cui T032 ha bisogno;
2. cade la colonna **`is_duration_zero`** dentro T015, che marca una riga sola e il cui conteggio in `values` basta.

**Non cadono in nessun caso** il determinismo (T005, T023), il blocco `denominators` (T022), la severità del controllo sul nuovo documento (T038) e le cinque decisioni ereditate (T009, T015, T016, T028). Sono i punti per cui la feature esiste, e i primi tre sono anche quelli che nessuna feature successiva potrebbe aggiungere a posteriori senza rifare il lavoro. Se dovessero essere loro a non entrare, la risposta corretta è scomporre la feature lungo la linea dichiarata nella spec — pipeline da una parte, documento e controllo dall'altra — non consegnarla monca.

### La sessione si chiude qui

Il punto di stop 2 di `CLAUDE.md` cade su questo file. L'implementazione parte in una sessione successiva, con tre giorni non pianificati in mezzo: è la ragione per cui [research.md](./research.md) conserva i numeri della ricognizione e [contracts/output-datasets.md](./contracts/output-datasets.md) fissa gli schemi. Riprendere non deve costare una seconda ricognizione.

---

## Note

- Nessun task presuppone l'interazione con GUI di Power BI o Tableau (principio V)
- Nessun task scrive in `data/raw/`, che resta in sola lettura (principio II, FR-002)
- Nessun task versiona un dataset di output (FR-007). L'unico artefatto di dati versionato è `reports/cleaning_report.json`, che non contiene dati ma numeri sui dati
- Nessun task calcola un KPI, definisce un segmento, disegna il modello dati o genera dati sintetici (FR-042-FR-046)
- `data/interim/` non viene usata: la pipeline è un passaggio solo e uno stadio intermedio che nessuno legge sarebbe un file orfano
