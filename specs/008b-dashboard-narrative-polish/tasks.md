---

description: "Task list template for feature implementation"
---

# Tasks: Dashboard — narrazione, limiti a schermo, rifiniture

**Input**: Documenti di progettazione da `/specs/008b-dashboard-narrative-polish/`

**Prerequisiti**: plan.md, spec.md, research.md, data-model.md, quickstart.md — tutti presenti. I due contratti **non** esistono ancora: `contracts/narrative-contract.md` è il prodotto della Fase 2, `contracts/publishability-contract.md` della Fase 7.

**Test**: nessun task di test in senso software. La correttezza si verifica con le dodici prove di [quickstart.md](./quickstart.md) — una eseguibile, undici manuali — incorporate come task lungo le fasi, più la revisione in contesto pulito (T035-T037).

**Una lista che si legge come quella della `008a`, con una differenza sostanziale.** Diciotto task su quaranta sono marcati **(manuale, Valerio)** e stanno dentro la GUI: è il principio V, e la constitution lo prescrive esplicitamente. La differenza è **quali** siano i task manuali. Nella `008a` erano di costruzione, e la sessione ne raccoglieva l'esito; qui otto di essi sono di **verifica di un testo contro un altro testo** — le prove 4-11 — e nessuno strumento potrà mai eseguirli, perché confrontano due prose.

**La marcatura `[P]` è quasi assente**, per la stessa ragione della `008a`: la Fase 2 scrive per intero un solo file, e le Fasi 3-6 toccano tutte lo stesso `.pbix`, che non ammette lavoro parallelo. `[P]` compare solo dove due task toccano file davvero distinti.

## Path Conventions

Repository singolo. Contratto di narrazione in `specs/008b-dashboard-narrative-polish/contracts/narrative-contract.md`; esito in `specs/008b-dashboard-narrative-polish/quickstart.md`, sezione «Esito della costruzione»; contratto di pubblicabilità in `specs/008b-dashboard-narrative-polish/contracts/publishability-contract.md`; verbale in `specs/008b-dashboard-narrative-polish/review.md`. Il deliverable vive nel `.pbix`, **non versionato**, sulla macchina di Valerio. Fuori dalla cartella della feature si toccano solo `README.md` e — unicamente in caso di ritrovamento — un documento sotto `docs/`.

---

## Phase 1: Setup

**Purpose**: fissare i **vincoli** del contratto prima di scriverne il testo. L'ordine non è formale: un blocco scritto prima che la lista chiusa esista è un blocco scritto senza il vincolo che dovrebbe averlo governato, e riscriverlo dopo non è la stessa cosa.

- [x] T001 Scrivi l'intestazione di `specs/008b-dashboard-narrative-polish/contracts/narrative-contract.md`: il destinatario dichiarato (un decisore che non ha letto alcun documento del repository), che cosa il contratto è e che cosa non è, e la regola che ogni blocco porta quattro cose — pagina e spazio, testo letterale, obbligo, fonte (`N1`, `FR-002`)
- [x] T002 Scrivi in `specs/008b-dashboard-narrative-polish/contracts/narrative-contract.md`, **prima di qualunque blocco**, la sezione dei vincoli: la **lista chiusa dei numerali** con la fonte di ciascuna voce (`N2`, `FR-016`), i tre divieti di `N7` (`FR-020`), il divieto di comporre `C1` e `C3` (`N6`, `FR-019`), e le **tre formulazioni escluse** obbligatorie di `FR-003`

**Checkpoint**: i vincoli esistono. Ogni blocco scritto da qui in poi nasce dentro di essi.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: il contratto di narrazione completo, e la sua approvazione. È il terzo punto di fermata della feature.

**⚠️ CRITICAL**: nessun task della Fase 3 o successive inizia prima che T009 abbia ricevuto risposta. Riaprire Power BI prima dell'approvazione significa scrivere il deliverable senza che nessuno l'abbia letto — e il deliverable, qui, è il testo.

- [x] T003 Scrivi in `specs/008b-dashboard-narrative-polish/contracts/narrative-contract.md` i blocchi della **pagina di ingresso**, `OB-01`-`OB-04` di [data-model.md](./data-model.md) §3.1: l'assunzione dei proxy, che cosa la dashboard non risponde, la scala di confidenza con ciò che essa non misura, la copertura temporale con i due statuti distinti (`FR-006`-`FR-008`, `FR-018`)
- [x] T004 Scrivi i blocchi della **pagina `BQ1`**, `OB-05`-`OB-12`: le tre ragioni di confidenza; la distinzione fra la quota e `C1`; `C1` nominata da sola con la dichiarazione che da sola non decide; l'asimmetria del confronto di durata con la lettura esclusa; la stima per eccesso della sovrapposizione e l'ampiezza degli intervalli di mood (`FR-009`-`FR-011`, `FR-019`)
- [x] T005 Scrivi i blocchi della **pagina `BQ2`**, `OB-13`-`OB-23` e `OB-33`: le tre ragioni di confidenza; i segmenti marcati come domanda non misurata dalla fonte e la loro esclusione dalla lettura della coda; la non interpretabilità assoluta dell'affinità; perché punteggio e quadrante non si fondono; la sovrapposizione dei segmenti e il divieto di sommare o contare; `C3` nominata da sola; che le due visuali non si filtrano a vicenda; che «domanda» nomina un indice della fonte (`FR-009`-`FR-012`, `FR-015`, `FR-019`, `FR-020`)
- [x] T006 Scrivi i blocchi della **pagina `BQ3`**, `OB-24`-`OB-32`: perché la confidenza è bassa e perché i tre scenari si leggono insieme; le assunzioni `A4`, `A5`, `A6` **senza i propri numeri** ([data-model.md](./data-model.md) §5); che l'intervallo non è un intervallo di confidenza; che l'uplift è un livello mensile e non un cumulato; che il tasso è lordo; che nessuna base utenti è quantificata e la dashboard non fornisce il moltiplicatore, con la formulazione «non è scalabile» esclusa; il debito sulla verificabilità del benchmark dichiarato aperto (`FR-013`, `FR-014`)
- [x] T007 Scrivi in `specs/008b-dashboard-narrative-polish/contracts/narrative-contract.md` la sezione **«che cosa questa feature può e non può toccare nel file»**: le rifiniture ammesse (titolo, allineamento, colore, etichetta d'asse, formato già dichiarato dalla `008a` §1.2); i divieti di `N3` — nessuna pagina-tooltip, nessun segnalibro, nessun pannello a scomparsa; `segment_display` e mai `segment` su qualunque visuale di segmenti (`FR-025`); nessun filtro di categoria su alcuna pagina che espone `BQ1-K3` (`FR-026`); nessuna visuale legata a un campo, nessun filtro, nessuna modifica al modello (`FR-024`)
- [x] T008 Rileggi `specs/008b-dashboard-narrative-polish/contracts/narrative-contract.md` contro l'inventario di [data-model.md](./data-model.md) §3 **in entrambe le direzioni**: ogni `OB` ha almeno un blocco, ogni blocco serve almeno un `OB`. Rileggilo poi contro i vincoli di T002: nessuna cifra fuori lista, nessuna composizione, nessuna conclusione
- [x] T009 **PUNTO DI FERMATA 3** — proponi il commit del contratto di narrazione e **fermati**: il contratto torna a Valerio per approvazione o correzione, prima che Power BI Desktop venga riaperto (`FR-001`, `FR-005`, `N1`). Riporta che cosa il contratto dice, quali formulazioni esclude e su che cosa chiede una conferma

**Checkpoint**: contratto approvato e committato. Il repository è in uno stato coerente e nulla di ciò che esiste può ancora contraddirlo. **È il confine di sosta se la giornata si spezza.**

---

## Phase 3: User Story 4 - Le tre impostazioni fragili verificate prima di ogni altra cosa (Priority: P1) 🎯

**Goal**: che nessuna narrazione venga scritta accanto a un numero che non è più quello pubblicato.

**Independent Test**: prova 2 di [quickstart.md](./quickstart.md).

**⚠️ Questa fase precede ogni altra operazione nel file.** È il costo di una lettura contro il costo di scrivere «questo valore misura X» sotto un numero che non misura più X.

- [ ] T010 **(manuale, Valerio)** Riapri il `.pbix` e verifica le tre impostazioni dell'issue `#20`, nell'ordine: (a) `energy`, `valence`, `danceability` di `dim_track` nel dominio `0-1`; (b) il conteggio di riga di `dim_title` coincidente con quello lasciato dalla `008a`; (c) la colonna che nomina lo scenario presente su `bq3_scenarios`. Se una è persa, **fermati**, correggila e annota l'accaduto come ricomparsa (`FR-027`)
- [ ] T011 **(manuale, Valerio)** Annota l'esito delle tre verifiche in forma grezza, per la trascrizione della Fase 7: per ciascuna, difetto assente oppure presente e corretto
- [ ] T012 **(manuale, Valerio, condizionale)** **Solo se** T010 ha imposto una correzione che tocca un valore a schermo: riconfronta gli otto valori a schermo con `docs/kpi_measures.md` alla stessa grana e annota l'esito. Se nessuna correzione è servita, questa prova **non si esegue** e la sua non esecuzione va dichiarata (`FR-028`, prova 12)

**Checkpoint**: le tre impostazioni sono nello stato atteso. Solo ora si scrive.

---

## Phase 4: User Story 1 - Il lettore esterno sa, prima di leggere un numero, che i dati non sono di StreamWave (Priority: P1) 🎯

**Goal**: la pagina di ingresso porta l'assunzione strutturale che la constitution impone in ogni artefatto rivolto all'utente finale.

**Independent Test**: si apre la pagina di ingresso e si legge; se l'assunzione dei proxy non è lì, la storia fallisce indipendentemente da tutto il resto.

**Perché questa storia viene prima delle altre di pari priorità**: è l'unica il cui fallimento rende il file non mostrabile a nessuno. Le altre lo renderebbero incompleto.

- [ ] T013 **(manuale, Valerio)** Inserisci nella fascia sotto la scheda della North Star e nella striscia a piè di pagina dell'**ingresso** i blocchi `OB-01`-`OB-04` come il contratto li scrive, alla lettera. Il testo non si sovrappone alla scheda, non ne riduce l'area e non sposta la barra di navigazione (`FR-022`)
- [ ] T014 **(manuale, Valerio)** Annota **mentre accade** ogni differenza fra il contratto e ciò che hai inserito: testo tagliato per farlo entrare, riformulazione, blocco spostato in un altro spazio. Non ricostruirle a memoria alla fine (`N4`, `FR-029`)

**Checkpoint**: la pagina di ingresso è pubblicabile per la propria parte. Il file, non ancora.

---

## Phase 5: User Story 2 - Chi legge un KPI incontra il suo limite accanto al valore (Priority: P1) 🎯

**Goal**: il principio IV nella sua metà «nella dashboard», per tutti e otto i KPI.

**Independent Test**: si percorrono le tre pagine di domanda e si verifica, KPI per KPI, che il limite che il documento canonico dichiara sia leggibile a schermo senza gergo.

- [ ] T015 **(manuale, Valerio)** Inserisci nella fascia della pagina **`BQ1`**, nelle tre aree allineate alle schede, i blocchi `OB-05`-`OB-12` come il contratto li scrive
- [ ] T016 **(manuale, Valerio)** Inserisci nella fascia della pagina **`BQ2`** i blocchi `OB-13`-`OB-23` e `OB-33`. È la fascia più carica per numero di obblighi: se non basta, taglia il testo e annota che cosa hai tolto, **non** allargare la fascia a spese della graduatoria (`N4`)
- [ ] T017 **(manuale, Valerio)** Inserisci nella fascia della pagina **`BQ3`** i blocchi `OB-24`-`OB-32`. È la fascia più densa per peso — tre assunzioni, quattro limiti, un debito di governance — e il blocco che non si taglia in nessun caso è `OB-32`, il debito sulla verificabilità del benchmark (`FR-014`)
- [ ] T018 **(manuale, Valerio)** Esegui le sole rifiniture ammesse dal contratto, sezione di T007. Qualunque intervento che tocchi un campo, un filtro o una formula **non si esegue**: si annota come ritrovamento e si rinvia (`FR-024`, `FR-030`)
- [ ] T019 **(manuale, Valerio)** Annota **mentre accadono** gli scostamenti delle tre pagine e i tagli eseguiti, con l'obbligo che ciascun taglio ha ridotto o scoperto

**Checkpoint**: il testo è a schermo su tutte e quattro le pagine. Nessuna verifica è ancora stata fatta.

---

## Phase 6: User Story 3 - Nessun testo a schermo afferma più di quanto un artefatto sostenga (Priority: P1) 🎯

**Goal**: che la narrazione sia un artefatto del progetto invece di un commento.

**Independent Test**: la lettura del contratto accanto allo schermo, blocco per blocco.

**★3 — è la prova che questa feature aggiunge al progetto**, e le otto verifiche che seguono sono la sua articolazione. Vanno eseguite **come lettura e non come ricordo**: chi ha appena scritto un testo lo rilegge sapendo che cosa intendeva, ed è la condizione in cui una cifra di troppo è più difficile da vedere.

- [ ] T020 **(manuale, Valerio)** Prova 4 — esaustività: percorri l'inventario di [data-model.md](./data-model.md) §3 e trova per ciascun `OB` il blocco che lo soddisfa; poi percorri i blocchi a schermo e trova per ciascuno l'obbligo che lo richiede. Annota ogni obbligo scoperto e ogni blocco senza obbligo
- [ ] T021 **(manuale, Valerio)** Prova 5 — fedeltà: leggi il contratto approvato accanto allo schermo e verifica la coincidenza **alla lettera** di ogni blocco. Una differenza è uno scostamento e si dichiara; non si corregge in silenzio
- [ ] T022 **(manuale, Valerio)** Prova 6 — cifre: percorri ogni blocco cercando le cifre. Nessuna, salvo le voci della lista chiusa. Dove i due anni di copertura compaiono, verifica che il loro statuto sia distinto (`FR-016`, `FR-018`)
- [ ] T023 **(manuale, Valerio)** Prova 7 — regola di decisione: verifica che `C1` e `C3` siano nominate da sole, ciascuna con la dichiarazione che da sola non decide, e che nessuna pagina le conti, nomini `C2`, o pubblichi un esito complessivo (`FR-019`)
- [ ] T024 **(manuale, Valerio)** Prova 8 — registro: verifica che nessun blocco concluda, raccomandi, preveda o attribuisca una causa, e che la parola «domanda» sia dichiarata su `BQ2` come indice della fonte e non come comportamento osservato (`FR-020`)
- [ ] T025 **(manuale, Valerio)** Prova 9 — formulazioni escluse: verifica che nessuna delle tre compaia, in nessuna variante (`FR-003`)
- [ ] T026 **(manuale, Valerio)** Prove 10 e 3 — visibilità e perimetro: verifica che nessun blocco stia dietro un tooltip di pagina, un segnalibro o un pannello, che le pagine siano quattro, e che tabelle, relazioni e misure siano quelle che la `008a` ha lasciato (`FR-023`, `FR-024`)
- [ ] T027 **(manuale, Valerio)** Prova 11 — sigle: verifica che ogni sigla introdotta dai blocchi di questa feature sia sciolta sulla stessa pagina (`FR-021`)

**Checkpoint**: il deliverable è verificato per quanto una lettura può verificare. Ciò che resta scoperto — che le frasi si capiscano — è della revisione.

---

## Phase 7: User Story 5 - Chi legge il repository sa che cosa c'è a schermo senza poterlo aprire (Priority: P2)

**Goal**: l'esito e il contratto di lettura per la `010`.

**Independent Test**: si leggono contratto ed esito in sequenza, senza aprire il file, e si sa che cosa il lettore della dashboard incontra.

- [ ] T028 Compila in `specs/008b-dashboard-narrative-polish/quickstart.md` la sezione «Che cosa è a schermo, pagina per pagina»: per ciascuna pagina gli obblighi che vi atterrano, quanti blocchi, se la fascia è bastata
- [ ] T029 Compila le sezioni «Gli scostamenti dal contratto approvato» e «Che cosa è stato tagliato, e perché», dalle annotazioni di T014 e T019. Zero scostamenti è un esito possibile e va dichiarato come tale, non lasciato vuoto (`FR-029`)
- [ ] T030 Compila «L'esito di ★1», «I ritrovamenti» e «Lo stato delle cinque issue» dalle annotazioni di T011, T012 e T018: per `#11`, `#17`, `#18`, `#20`, `#21` dichiara che restano aperte e quale evidenza manca a ciascuna (`FR-031`)
- [ ] T031 Compila «L'esito delle dodici prove»: tabella prova / chiusa da / esito. Se la prova 12 non è stata eseguita, dichiara che non lo è stata e perché — non attribuirle un esito che nessuno ha osservato
- [ ] T032 Compila «La dichiarazione di pubblicabilità»: le cinque condizioni di `N8` verificate una per una con il task che le chiude, e l'elenco di ciò che «pubblicabile» **non** significa (`FR-032`)
- [ ] T033 Scrivi una nota in loco sul documento di `docs/` che lo richiede, **solo se** T018 o T030 hanno registrato un ritrovamento: data, feature, affermazione precedente, affermazione corretta, causa, fonte verificabile — senza riscrivere il testo originale (`FR-030`). Zero note se nessun ritrovamento, ed è l'esito atteso
- [ ] T034 Scrivi `specs/008b-dashboard-narrative-polish/contracts/publishability-contract.md`: che cosa la `010` può presupporre sul `.pbix`, che cosa «pubblicabile» non significa, quali issue restano aperte, e che la garanzia poggia su tre presidi umani e su nessuno script

**Checkpoint**: il repository descrive un file che nessuno dei suoi lettori può aprire, ed è coerente con esso.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: la revisione, la chiusura e l'allineamento del README.

- [ ] T035 Esegui la **revisione in contesto pulito** su `contracts/narrative-contract.md` e sulla sezione «Esito della costruzione» di `quickstart.md`, in sessione separata o subagent isolato che riceva **solo** i due documenti. Il metro dichiarato non è la conformità agli obblighi ma la **leggibilità per il destinatario**: un blocco esatto e incomprensibile è un difetto, e nessun altro presidio di questa feature può vederlo
- [ ] T036 Scrivi `specs/008b-dashboard-narrative-polish/review.md` con l'esito della revisione e **proponine il commit prima di toccare qualunque artefatto revisionato**: i quattro obblighi di `CLAUDE.md` — verbale prima delle correzioni, dichiarazione di che cosa è stato letto e cosa no, ancoraggio della versione revisionata con commit e impronta, testo del revisore mai corretto (`FR-034`)
- [ ] T037 Chiudi i **soli rilievi strettamente necessari** — quelli senza i quali il deliverable afferma il falso o pubblica un valore che non regge — e registra gli altri come issue sul tracker. Aggiungi in coda al verbale il blocco di chiusura che distingue *risolto*, *indebolito* e *rinviato*, e per ogni rinvio nomina l'issue
- [ ] T038 Allinea `README.md`: riga di stato della `008b` con link al verbale, deliverable elencato, prosa dei deliverable estesa, `Setup` e `Struttura` dove serve. **Correggi in particolare la frase «Il file è leggibile, non pubblicabile»**, che senza questo task resterebbe su `main` come affermazione falsa (`FR-033`)
- [ ] T039 Esegui `python3 scripts/check_audit_coherence.py` e verifica l'esito verde. Dichiara nel riporto che cosa quel verde certifica — che nessuna ancora è stata rotta — e che cosa non certifica: nulla del deliverable di questa feature (`FR-035`)
- [ ] T040 **Riporto finale a Valerio**, prima del merge: il contratto approvato, l'esito con gli scostamenti, l'esito della verifica su `#20`, i rilievi della revisione con chiuso/rinviato, il verde del controllo, e la dichiarazione esplicita che il file è pubblicabile con la ragione. Il `.pbix` non si committa (`FR-036`)

---

## Dependencies & Execution Order

```
Fase 1 (T001-T002)
   └─> Fase 2 (T003-T008) ──> ⏸ T009 PUNTO DI FERMATA 3
                                  └─> Fase 3 (T010-T012)  ★1, prima di ogni scrittura
                                        └─> Fase 4 (T013-T014)  ingresso
                                              └─> Fase 5 (T015-T019)  BQ1, BQ2, BQ3
                                                    └─> Fase 6 (T020-T027)  ★3, le otto verifiche
                                                          └─> Fase 7 (T028-T034)  esito e contratto
                                                                └─> Fase 8 (T035-T040)  revisione e chiusura
```

**Tre vincoli d'ordine non negoziabili**, e ciascuno ha un precedente nel repository:

1. **T009 prima di T010.** Riaprire il file prima dell'approvazione significa scrivere il deliverable senza che nessuno l'abbia letto. È `F1` della `008a`, applicata a un contratto che invece di descrivere il deliverable lo contiene.
2. **T010 prima di T013.** Tre impostazioni fragili si sono già perse una volta ciascuna, e nessun controllo del repository può vederle. È la lezione di `E9` nella `007b`, che costò due letture invece delle pagine di una feature intera.
3. **T036 prima di T037.** Il verbale si committa quando la revisione torna, prima di toccare l'artefatto. È l'omissione della `004`, recuperata dopo e dichiarata come recupero.

**Le storie non sono indipendenti fra loro**, e vale la pena dirlo invece di fingere che lo siano: US1, US2 e US3 vivono nello stesso file e la terza verifica le prime due. L'unica indipendenza reale è quella di US4, che si esegue e si chiude prima che qualunque altra cosa accada.

**Opportunità di parallelismo**: nessuna dentro le Fasi 3-6, che toccano tutte lo stesso `.pbix`. T033 e T034 della Fase 7 toccano file distinti e sono `[P]` fra loro, ma entrambi dipendono da T030.

---

## Implementation Strategy

**MVP**: US4 più US1. Le tre verifiche dell'issue `#20` e l'assunzione dei proxy sulla pagina di ingresso sono, insieme, il minimo che trasformi un file non mostrabile in un file mostrabile con una riserva. Non è la consegna — US2 è il deliverable dichiarato — ma è il punto in cui il valore comincia a esistere.

**Consegna incrementale**: le fasi sono già l'incremento, e il confine di sosta è ⏸ T009. Ogni altra interruzione cade dentro la costruzione, dove metà delle fasce sono piene e l'esito non è scrivibile — che è precisamente lo stato che il principio III vieta alla fine di una sessione.

**Che cosa non va compresso se il tempo stringe.** Non la Fase 6: è l'unica verifica che il deliverable riceverà, e comprimerla significa consegnare una prosa che nessuno ha riletto. Non T036: il verbale prima delle correzioni è l'ordine che rende la revisione una revisione. Se qualcosa deve cedere, cedono le rifiniture di T018, che sono l'unica parte di questa feature che nessun obbligo richiede.
