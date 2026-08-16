---

description: "Task list — Feature 004: Synthetic Business Metrics"
---

# Tasks: Synthetic Business Metrics

**Input**: documenti di design da `/specs/004-synthetic-business-metrics/`

**Prerequisiti**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/parameters-and-scenarios.md](./contracts/parameters-and-scenarios.md), [quickstart.md](./quickstart.md)

**Test**: nessun framework introdotto (T9), per la stessa ragione della 002 e della 003. I comportamenti verificabili sono nove e si verificano da riga di comando secondo [quickstart.md](./quickstart.md); i task di verifica stanno in coda a ciascuna fase.

**Organizzazione**: per user story, così ogni storia resta verificabile in autonomia. La corrispondenza con i cinque blocchi del piano è: Fase 2 = **A**, US1 = **B**, US2 = **C**, US3 = **D**, US4 + Polish = **E**.

## Format: `[ID] [P?] [Story] Descrizione`

- **[P]**: eseguibile in parallelo (file diverso, nessuna dipendenza)
- **[Story]**: a quale user story appartiene (US1-US4)
- Ogni descrizione riporta il percorso del file

## Nota sul parallelismo

Come nella 002 e nella 003: l'autore è uno solo e le storie sono in dipendenza stretta — il documento cita valori che devono esistere, il controllo verifica marcatori che devono essere scritti. I `[P]` sono marcati dove il file è diverso **e** la dipendenza è effettivamente assente, che qui accade poche volte.

## Nota sulle sigle

`D1`-`D6` sono le decisioni della [spec](./spec.md). `F1`-`F4` e `T1`-`T9` sono ritrovamenti e decisioni tecniche di [research.md](./research.md). `FR-xxx` e `SC-xxx` rimandano a requisiti e criteri di successo della spec.

## ⚠️ Il vincolo che governa l'ordine

**La Fase 2 deve essere completata e committata prima che la Fase 3 cominci.** Non è una preferenza di sequenza: è FR-011a. I due fattori della banda sono l'unico numero libero della feature, e fissarli dopo aver visto il benchmark li piegherebbe verso l'intervallo che «sembra giusto» in un modo che **nessun controllo di questo progetto potrebbe rilevare**. La garanzia è data dai due commit separati, non dalla buona fede di chi esegue.

Chi riprende questa lista a metà e non sa a che punto è: `git log --follow data/benchmarks/bq3_tier_upgrade.json` lo dice.

---

## Phase 1: Setup

**Scopo**: verificare le tre trappole di collocazione e di spazio dei nomi **prima** di scrivere una riga. Tutte e tre si annullerebbero in silenzio.

- [X] T001 Verificare con `git check-ignore -v data/benchmarks/bq3_tier_upgrade.json` che il percorso **non** sia intercettato da `.gitignore`. È il ritrovamento F1: `data/external/*` è ignorato, e la cartella che il nome suggeriva non avrebbe versionato il congelamento richiesto dalla condizione 2 della constitution. Se il percorso risultasse intercettato, fermarsi e cambiare collocazione prima di scrivere il file
- [X] T002 [P] Verificare con `git check-ignore -v reports/bq3_scenarios.json` che il percorso **non** sia intercettato (FR-018a, SC-004). Il controllo di coerenza deve poterlo risolvere su una copia pulita senza aver prima eseguito la derivazione
- [X] T003 [P] Verificare sui due artefatti esistenti che il prefisso `BQ3.` sia disgiunto da `NF.`, `SP.`, `CL.`, `X.` nello spazio `values`, e che nessuna delle chiavi `bq3_*` previste da [data-model.md](./data-model.md) collida in `conventions`. È il ritrovamento F2: lo spazio di `conventions` è **piatto** e `rounding_decimals` è già occupato con contenuto diverso

**Checkpoint**: le collocazioni reggono e i nomi non collidono. Si può scrivere.

---

## Phase 2: Foundational — i fattori, prima di tutto *(blocco A)*

**Scopo**: fissare la banda **prima che la ricognizione cominci**, e renderlo verificabile. Blocca ogni fase successiva.

- [X] T004 Creare `data/benchmarks/bq3_tier_upgrade.json` con i **soli** blocchi `band`, `price` e `schema_version` secondo [data-model.md](./data-model.md) §1: `bq3_band_factor_low` a `0.50`, `bq3_band_factor_high` a `1.50`, il differenziale di `4.00` con rimando ad A4, e la prosa che dichiara che l'ampiezza **non misura nulla** (FR-011). Tutti i numeri come **stringhe**, per T5
- [X] T005 Scrivere dentro lo stesso file la **ragione** della scelta di k = 0,50 (T6): che è una stipulazione e non una derivazione, che la rotondità è la ragione e non la sua assenza, e che dichiara un rapporto 3 fra gli estremi qualunque sia il benchmark
- [X] T006 Verificare che il file **non contenga** la chiave `benchmark`, nemmeno vuota o con un segnaposto ([data-model.md](./data-model.md) §1). Un campo pronto da riempire renderebbe indistinguibile «fissato prima» da «riempito dopo» e vanificherebbe FR-011a
- [X] T007 Proporre a Valerio il commit del solo file dei parametri. **È questo commit a costituire la prova di precedenza**: senza di esso FR-011a resta un'affermazione. Non proseguire alla Fase 3 prima che sia stato eseguito

**Checkpoint**: la banda è fissata e la history lo testimonia (quickstart, Prova 1). La ricognizione può cominciare.

---

## Phase 3: User Story 1 — Il parametro è verificabile alla fonte (Priority: P1) *(blocco B)*

**Goal**: `data/benchmarks/bq3_tier_upgrade.json` contiene il valore adottato con una citazione che soddisfa tutte e cinque le condizioni della constitution, oppure la feature si ferma con il registro dei rigetti.

**Independent Test**: aprire il file senza rete e senza eseguire nulla; i cinque elementi della citazione sono presenti e il riferimento è raggiungibile da chi ha rete (quickstart, Prova 2).

**⚠️ Nessuna rete a runtime**: la ricognizione è un passaggio **umano** che precede la pipeline. Nessuno script scritto in questa fase o in quelle successive contatta una fonte esterna (FR-008, condizione 3).

- [X] T008 [US1] Condurre la ricognizione sul **tasso di conversione a un tier superiore in servizi di streaming**, valutando ogni fonte candidata contro tutte e cinque le condizioni della constitution. **Un solo benchmark** (FR-001): nessuna raccolta su churn, engagement, prezzi o dimensione della base
- [X] T009 [US1] Registrare in `data/benchmarks/bq3_tier_upgrade.json`, blocco `rejected`, ogni fonte valutata e **respinta con il motivo** (FR-005). Un rigetto non registrato rende non verificabile l'affermazione che la fonte adottata fosse la migliore disponibile
- [X] T010 [US1] Scrivere nel blocco `benchmark` il valore adottato e i cinque elementi della citazione — organizzazione, titolo, data di pubblicazione, riferimento recuperabile, data di accesso (FR-003). Il valore come **stringa** (T5). «Ricerche di settore» o formule equivalenti non sono citazioni e non si adottano
- [X] T011 [US1] Scrivere accanto al valore **che cosa la fonte misura esattamente** e in che modo differisce da ciò per cui viene usato (FR-004), e l'**assunzione di trasferimento** che dichiara che il valore descrive un operatore terzo e non StreamWave (FR-007). Lo scarto di misura va scritto anche — e soprattutto — se è scomodo
- [X] T012 [US1] Verificare che il file dichiari la copertura temporale e di mercato della fonte, e il suo scarto rispetto ad A2 e all'orizzonte ipotetico di lancio (spec, "Limiti Dichiarati")
- [X] T013 [US1] **Punto di riporto obbligatorio.** Riportare a Valerio la fonte adottata **con il proprio scarto di misura**, oppure il fallimento con il registro dei rigetti (FR-006, FR-006a). Vale in **entrambi** gli esiti: il rischio non è il fallimento rumoroso, è l'adozione silenziosa di una fonte «abbastanza vicina», su cui nessun presidio automatico può esistere. Se nessuna fonte regge, **fermarsi**: dichiarare il parametro come scelta dell'analista è decisione di Valerio, non di chi esegue (FR-006)
- [X] T014 [US1] Proporre il commit del blocco `benchmark`, **separato** da quello della Fase 2 (T7 di research)

**Checkpoint**: SC-001 verificabile. La derivazione ha i propri ingressi.

---

## Phase 4: User Story 2 — I sei valori si rigenerano da una copia pulita (Priority: P1) 🎯 **l'MVP si completa qui** *(blocco C)*

**Goal**: `python3 scripts/build_bq3_scenarios.py` produce `reports/bq3_scenarios.json` in modo deterministico, senza rete e senza `data/raw/`.

**Independent Test**: doppia esecuzione e diff vuoto su una copia pulita; alterare il benchmark muove tutti e sei i valori (quickstart, Prove 3, 4, 6).

- [X] T015 [US2] Creare `scripts/build_bq3_scenarios.py` con la lettura del file dei parametri e la conversione dei numeri **da stringa a `decimal.Decimal`**, mai passando per `float` (T5, F3)
- [X] T016 [US2] Implementare la catena di derivazione di [data-model.md](./data-model.md) §"La catena": `adoption.base` dal benchmark, `worst` e `best` per i due fattori, i tre `uplift` come prodotto per il differenziale diviso 100 (FR-010, FR-012). Il differenziale si **legge dal file**, non si scrive nel codice
- [X] T017 [US2] Implementare l'arrotondamento con `ROUND_HALF_UP` **dichiarato esplicitamente**, e non la modalità predefinita di `Decimal`, che è `ROUND_HALF_EVEN` (T5). Le cifre significative sono quelle del benchmark e mai più di due (FR-015, D3)
- [X] T018 [US2] Implementare il formattatore del campo `display` con separatore decimale italiano, per formattazione **esplicita** e mai con funzione dipendente dal locale (vincolo ereditato da F6 della 003)
- [X] T019 [US2] Implementare la guardia di FR-016: la derivazione **si ferma con errore** se un tasso risultante cade fuori dall'intervallo 0-100, senza lasciare un artefatto parziale. Il messaggio di errore **deve instradare l'uscita, non limitarsi a fermare**: con k = 0,50 lo scenario ottimista supera il 100% per qualunque benchmark oltre il **66,67%**, e poiché i fattori sono fissati prima della ricognizione (FR-011a) l'incompatibilità è scopribile solo qui, a commit già fatti. L'uscita esiste già dentro FR-011a — i fattori possono cambiare dopo, purché il cambiamento sia **dichiarato con la propria ragione** — e il messaggio deve nominarla, perché chi la incontra non sia costretto a dedurla. La probabilità è bassa (un tasso di passaggio a tier superiore oltre due terzi della base sarebbe una notizia); il costo di scriverlo è una riga, quello di incontrarlo impreparati è uno stallo a metà feature
- [X] T020 [US2] Calcolare e scrivere le due affermazioni derivate con identificativo proprio — `BQ3.band.spread_pp` e `BQ3.band.ratio` — perché un confronto costruito su valori misurati è esso stesso un valore misurato (FR-031, regola D5)
- [X] T021 [US2] Scrivere `reports/bq3_scenarios.json` con `values`, `conventions` (tutte con prefisso `bq3_`, per F2), `sources` con l'impronta del file dei parametri, e `schema_version`. **Nessun timestamp di esecuzione**: se serve datare, si data la fonte, che è un fatto
- [X] T022 [US2] Estendere `load_artifacts()` in `scripts/check_audit_coherence.py` al terzo artefatto, **senza indebolire la verifica di collisione** (FR-018). La funzione è già scritta in forma generica su una lista: la modifica è l'aggiunta di un percorso, e va tenuta tale
- [X] T023 [US2] Aggiornare l'intestazione e la docstring di `scripts/check_audit_coherence.py`, che oggi nominano due artefatti e due documenti
- [X] T024 [US2] **Verifica**: eseguire le Prove 3, 4, 5 e 7 di [quickstart.md](./quickstart.md) — copia pulita, doppia esecuzione con diff vuoto, ispezione per assenza di rete e di generatori casuali, e il **caso di confine a 29 punti percentuali**, che è quello che una prova casuale non troverebbe (F3)
- [X] T025 [US2] **Verifica**: eseguire la Prova 6 — alterare il solo benchmark e confermare che tutti e sei i valori si muovono, e che `BQ3.band.ratio` **non** si muove, perché dipende solo dalla stipulazione (SC-003, FR-014)

**Checkpoint**: SC-002, SC-003 e SC-007 verificati. I sei valori esistono e sono congelati. **È il confine di sosta migliore della feature** (plan, "Ordine di lavoro"): da qui in avanti è tutta prosa, che non invecchia.

---

## Phase 5: User Story 3 — Il documento dichiara metodo e limiti (Priority: P2) *(blocco D)*

**Goal**: `docs/bq3_scenarios.md` passa il controllo in severità stretta, e ogni cifra che pubblica è ancorata.

**Independent Test**: il controllo è verde; alterare una cifra lo fa fallire; una quantità priva di marcatore è **errore** e non avviso (quickstart, Prova 8).

- [X] T026 [US3] Scrivere `docs/bq3_scenarios.md`: il metodo (come un tasso osservato altrove diventa tre scenari), l'assunzione di trasferimento, la precedenza dei fattori sulla ricognizione, e i limiti. È il documento che chi contesta il metodo apre, mentre il business case è quello che il board legge (spec, Assumptions)
- [X] T027 [US3] Ancorare **ogni** cifra del documento secondo [`docs/convenzioni-marcatura.md`](../../docs/convenzioni-marcatura.md): o l'ancora a un identificativo, o il marcatore di non-misurato. Nessun numerale in lettere per un fatto misurato (FR-032, corollario (b))
- [X] T028 [US3] Dichiarare nel documento che il range **non è un intervallo di confidenza** e che la sua ampiezza non ha interpretazione probabilistica (FR-022); che `BQ3-K2` è **euro per utente al mese e non è scalabile** e che nessuna base utenti viene quantificata (FR-023); e che le disdette sono **escluse**, con la conseguenza che l'uplift è a regime e non cumulato sui 12 mesi (D4)
- [X] T029 [US3] Aggiungere `docs/bq3_scenarios.md` a `DOCUMENTS` in `scripts/check_audit_coherence.py` con `strict=True` (FR-020). La regola di non retroattività vale a favore dei documenti vecchi, non dei nuovi
- [X] T030 [US3] Aggiornare [`docs/convenzioni-marcatura.md`](../../docs/convenzioni-marcatura.md) in tre punti (FR-019, T8): §3, che dichiara «oggi due artefatti» e da qui sono tre; la tabella di §5, che elenca i documenti con la propria severità; la tabella di provenienza in coda, con data e feature. È la **fonte unica** e non può descrivere uno stato superato
- [X] T031 [US3] Aggiornare [`data/README.md`](../../data/README.md) con la quarta cartella e **il motivo per cui si comporta al contrario delle altre**: le sorelle non sono versionate perché riproducibili, `benchmarks/` lo è perché non lo è (T1). Senza questa riga il prossimo lettore la prende per un errore
- [X] T032 [US3] **Verifica**: eseguire la Prova 8 di [quickstart.md](./quickstart.md), incluse **entrambe** le alterazioni. La seconda — quantità priva di marcatore — è la sola che dimostra che la severità stretta è davvero attiva: con la severità sbagliata l'esito resterebbe verde e nessuno se ne accorgerebbe (SC-004)

**Checkpoint**: SC-004 verificato. Il documento non può più divergere dall'artefatto in silenzio.

---

## Phase 6: User Story 4 — Il business case porta l'assunzione di trasferimento (Priority: P2) *(blocco E, prima parte)*

**Goal**: `A6` esiste in §2, è richiamata in §6, e le schede `BQ3-K1` e `BQ3-K2` portano note datate — tutto per **sole aggiunte**.

**Independent Test**: il diff su `docs/business_case.md` non contiene righe che rimuovano un valore o un'affermazione preesistente (quickstart, Prova 9).

**⚠️ Vincolo che vale per tutta la fase**: `docs/business_case.md` **non è** sotto controllo di coerenza (F4). Un numero scritto nella sua prosa non porta ancora e nessuno lo verifica — è il rilievo R8 della 001, chiuso dalla 002 e da non riaprire. Vale la prassi di [`CLAUDE.md`](../../CLAUDE.md) sugli artefatti già mergiati: **nessun valore originale si cancella o si riscrive**.

- [X] T033 [US4] Aggiungere in §2 di `docs/business_case.md` l'assunzione strutturale **`A6`**, che istituisce l'assunzione di trasferimento dei benchmark, formulata sul modello di `A1` e con la stessa forma grafica delle altre (FR-025)
- [X] T034 [US4] Verificare che `A6` **non contenga** il valore del benchmark né alcuna delle sei cifre derivate: istituisce l'assunzione e rimanda al file dei parametri, dove il numero vive ancorabile (FR-025a)
- [X] T035 [US4] Aggiungere in §6, sottosezione «Cosa questa scala non misura», il richiamo ad `A6` **accanto ad `A1`** come seconda assunzione che resta fuori dalla scala di confidenza per costruzione (FR-026)
- [X] T036 [US4] Aggiungere una **nota datata** sulla scheda `BQ3-K1` in §5.5 che dichiari data, feature, che cosa è cambiato e la fonte verificabile (FR-027); che **le disdette sono escluse** e il tasso è lordo su base costante, con il rimando a FR-018 della 001 e ad A5 — è la chiusura di **R13 per la parte BQ3** (FR-028); e la composizione della fonte dopo l'ancoraggio **senza riscrivere** la riga «Fonte: Sintetico» esistente (FR-029, D5)
- [X] T037 [US4] Aggiungere una **nota datata** sulla scheda `BQ3-K2` in §5.5, che dichiari che il valore è euro per utente al mese e **non è scalabile**, e che l'uplift è a regime e non un ricavo cumulato sui 12 mesi (FR-027, D4)
- [X] T038 [US4] Verificare che le due note rispettino FR-027a: nessun valore di benchmark e nessuna delle sei cifre derivate nella prosa. Il differenziale di 4,00 € si cita **come rimando ad A4**, dove già vive, e non si riafferma come numero nuovo
- [X] T039 [US4] **Verifica**: eseguire la Prova 9 di [quickstart.md](./quickstart.md) — il diff contro `main` è di sole aggiunte sul testo preesistente, e non introduce cifre vietate (SC-006, FR-030)

**Checkpoint**: SC-006 verificato. Il debito testuale dell'ancoraggio è chiuso e R13-BQ3 con esso.

---

## Phase 7: Polish e questioni trasversali *(blocco E, seconda parte)*

**Scopo**: chiudere ciò che riguarda il progetto e non la feature, e sottoporre l'artefatto a un lettore che non l'ha costruito.

- [X] T040 Dichiarare lo **scostamento dalla roadmap sul seed fisso** (FR-024, D1) **dentro `docs/bq3_scenarios.md`**, nella sezione in cui il documento spiega perché la derivazione è deterministica. La nota sulla `004` in `docs/roadmap.md` prescrive che «uno script con seed fisso genera il dataset», e questa feature non lo fa: la formulazione precede l'uscita di engagement e base utenti dal perimetro, cioè precede le decisioni che tolgono al seed il proprio oggetto. **Non toccare `docs/roadmap.md`**: è artefatto di governance e appartiene alla regia, che vi ha già scritto la nota in loco il 2026-08-16. Una prescrizione superata dai fatti si registra dove la feature parla, non nel documento che la prescriveva
- [X] T041 [P] Verificare che nessun artefatto della feature presenti `BQ3-K1` o `BQ3-K2` come valore singolo e che nessuno ne innalzi la confidenza sopra `bassa` (SC-005, FR-021). È il divieto più facile da violare per distrazione, perché un valore singolo sta meglio in ogni frase
- [X] T042 [P] Rileggere i **cinque divieti** di [contracts/parameters-and-scenarios.md](./contracts/parameters-and-scenarios.md) §3 contro ciò che la feature ha effettivamente prodotto, e correggere il contratto se l'implementazione ne diverge. È la lezione della 003: dove contratto e implementazione divergono, è il contratto a dover essere corretto, non il lettore a doverlo indovinare
- [X] T043 Eseguire **l'intero** [quickstart.md](./quickstart.md) dalla Prova 1 alla Prova 9 su una copia pulita, in sequenza. Le verifiche di fase hanno coperto le prove una alla volta; questa copre la loro composizione
- [X] T044 **Revisione in contesto pulito** di `docs/bq3_scenarios.md`: una sessione che riceve **solo** il documento, senza spec, senza piano, senza history git. È l'unica configurazione in cui la revisione dice qualcosa, ed è nella stima (plan, blocco E). Precedenti: le revisioni della 001, 002 e 003
- [X] T045 Chiudere i rilievi della revisione. Quelli che non si chiudono riscrivendo una frase richiedono **nuovi valori** nell'artefatto, perché la regola D5 non ammette altra strada: un confronto o ha un identificativo o non si scrive
- [ ] T046 Aggiornare [`docs/roadmap.md`](../../docs/roadmap.md) con l'esito della feature — ore spese contro le 6 stimate, debito residuo, esiti che valgono oltre la feature. **Solo se Valerio lo chiede**: la roadmap è artefatto di governance e appartiene alla regia ([`CLAUDE.md`](../../CLAUDE.md))

---

## Dipendenze

```
Fase 1 (Setup)
   ↓
Fase 2 (blocco A — i fattori)  ⚠️ COMMIT OBBLIGATORIO PRIMA DI PROSEGUIRE
   ↓
Fase 3 US1 (blocco B — la ricognizione)  ⚠️ RIPORTO A VALERIO IN ENTRAMBI GLI ESITI (T013)
   ↓
Fase 4 US2 (blocco C — la derivazione)  ← confine di sosta migliore
   ↓
Fase 5 US3 (blocco D — il documento)
   ↓
Fase 6 US4 (blocco E — il business case)
   ↓
Fase 7 (Polish, revisione)
```

**Le storie non sono indipendenti fra loro**, e va detto invece di fingere il contrario: US2 non ha ingressi senza US1, US3 non ha cifre da ancorare senza US2. L'indipendenza che il template chiede è qui **verticale e non orizzontale** — ogni storia è verificabile in autonomia con le proprie prove, ma non è eseguibile fuori ordine.

**L'unica eccezione reale è US4**, che dipende dalla decisione D4 e dall'esistenza del benchmark ma **non dai sei valori**, visto che FR-025a e FR-027a le vietano di citarli. Se la ricognizione riuscisse e la derivazione fosse rinviata, US4 sarebbe comunque completabile.

## Opportunità di parallelismo

Poche e tutte piccole, come nella 002 e nella 003: T002 e T003 in Fase 1, T041 e T042 in Fase 7. Dentro le fasi i task scrivono quasi sempre nello stesso file e vanno in sequenza.

## Strategia di consegna

**MVP**: Fasi 1-4. A quel punto esistono un parametro citato e verificabile e sei valori riproducibili, che è tutto ciò che la `007` consuma. Il documento e le note del business case sono ciò che rende il lavoro leggibile da fuori — indispensabile per un progetto da portfolio, ma non per la catena tecnica.

**Se il tempo stringe**, la linea di taglio dichiarata dal prompt di consegna cade fra Fase 3 e Fase 4: *ricerca e file dei parametri* da una parte, *derivazione e documento* dall'altra.

**Se la ricognizione fallisce** (T013), si fermano le Fasi 4, 5 e 6. Restano consegnabili la Fase 2, il registro dei rigetti, e il chore della roadmap in Fase 7. La decisione su come procedere è di Valerio.
