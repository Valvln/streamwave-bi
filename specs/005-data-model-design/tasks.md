# Tasks: Data Model Design

**Input**: documenti di progetto in `specs/005-data-model-design/`

**Prerequisiti**: [spec.md](./spec.md) (approvata al primo punto di stop), [plan.md](./plan.md), [research.md](./research.md), [contracts/model-contract.md](./contracts/model-contract.md), [quickstart.md](./quickstart.md)

**Test**: nessun test automatico. La feature non produce codice eseguibile: le sue verifiche sono le **nove prove** del quickstart, sei eseguibili e tre di lettura. Ogni fase dichiara quale prova la chiude.

**Organizzazione**: i task delle fasi 3, 4 e 5 sono raggruppati per storia utente, in ordine di priorità. Le fasi successive sono trasversali.

## Formato: `[ID] [P?] [Story] Descrizione`

- **[P]**: eseguibile in parallelo — file diversi, nessuna dipendenza da task incompleti
- **[Story]**: a quale storia utente appartiene (`US1`, `US2`, `US3`)

## Una nota sulla parallelizzabilità, che qui è quasi nulla

Quasi tutti i task scrivono **lo stesso file**, `docs/data_model.md`. Il marcatore `[P]` compare quindi solo quattro volte su quarantaquattro, e non è una carenza del piano: è la forma di una feature che produce un documento invece di un albero di sorgenti. Segnalare come parallelo ciò che non lo è produrrebbe conflitti di scrittura e un piano che mente sulla propria durata.

## Il confine di pausa

Il tratto **T023 → T026** non va interrotto. Fra la registrazione del documento nel controllo e il primo esito verde, il repository ha un controllo che fallisce — e il principio III chiede che lo stato sia coerente **alla fine di ogni sessione**, non solo a fine feature.

Ogni altro confine fra fasi è sicuro. I punti di sosta migliori sono la fine della Fase 5, dove il documento è completo ma non ancora marcato, e la fine della Fase 8, dove tutto è scritto e resta solo la revisione.

---

## Fase 1: Preparazione

**Scopo**: mettere in fila ciò che serve prima di scrivere, così che nessuna sezione debba fermarsi a cercare un identificativo.

- [X] T001 Creare `docs/data_model.md` con la sola struttura delle sezioni previste dal piano, senza contenuto: intestazione, titoli, e un segnaposto per sezione che nomini il task che la riempie
- [X] T002 [P] Consolidare in `specs/005-data-model-design/research.md`, in coda a `T2`, l'elenco operativo degli identificativi che il documento userà come ancore, verificando con `python3 -c` che ciascuno esista negli spazi dei nomi uniti di `reports/data_profile.json` e `reports/cleaning_report.json`

**Verifica di fase**: ogni identificativo dell'elenco di `T002` si risolve. Un'ancora che non si risolve va scoperta ora, non quando il controllo fallisce su un documento di sedici sezioni.

---

## Fase 2: Fondamenta (prerequisito bloccante)

**Scopo**: scrivere le due sezioni che tutte le altre presuppongono. Nessuna storia utente può cominciare prima.

- [X] T003 Scrivere in `docs/data_model.md` la sezione di apertura: che cosa è il documento, che il modello è **progettato e non materializzato** e che nessuna sua affermazione è stata verificata eseguendola (`FR-003`), l'assunzione strutturale A1 richiamata e non sottintesa, e il rinvio a `docs/convenzioni-marcatura.md` per la chiave di lettura delle ancore
- [X] T004 Scrivere in `docs/data_model.md` la sezione con la **definizione operativa di «segmento»** (`FR-011`), l'alternativa scartata con le sue conseguenze sulla confidenza dei KPI di BQ2 (`FR-012`), e la dichiarazione che il mood resta nel framework come attributo di confronto e non come criterio di formazione

**Verifica di fase**: un lettore che si fermi qui sa che cosa il documento sta per descrivere e che cosa è un segmento. È la prima delle tre domande della Prova 7.

---

## Fase 3: Storia utente 1 — L'ossatura del modello (Priorità P1) 🎯 MVP

**Obiettivo**: grane, chiavi, relazioni e direzioni di filtro dichiarate, così che la `007` possa sapere su quale tabella una misura è corretta e su quale è gonfiata.

**Prova di indipendenza**: per tutti e otto i KPI il documento dichiara le tre grane, le tabelle coinvolte e la giunzione che darebbe un valore sbagliato. Chiusa dalla **Prova 3**.

- [X] T005 [US1] Scrivere in `docs/data_model.md` la sezione delle **sette tabelle**, divise nelle due stelle disgiunte, ciascuna con ruolo, grana espressa come frase che dice che cosa è una riga, chiave, cardinalità **ancorata** e dataset di provenienza (`FR-006`)
- [X] T006 [US1] Scrivere in `docs/data_model.md` la ragione per cui le due stelle **non si toccano**: nessuna chiave comune, tassonomie disgiunte per §5.3 del business case, e il confronto fra cataloghi che avviene fra misure e mai fra righe
- [X] T007 [US1] Scrivere in `docs/data_model.md` la sezione **regola di lettura come proprietà dello schema**: per ogni calcolo, la tabella corretta e quella che darebbe un valore sbagliato, con entrambe le cardinalità ancorate (`FR-009`, `FR-010`)
- [X] T008 [US1] Scrivere in `docs/data_model.md` la sezione delle **cinque relazioni** con cardinalità e direzione di filtro, la ragione di ciascuna direzione, e la condizione strutturale che rende sicura l'unica bidirezionale, con l'obbligo per chi aggiungesse una relazione in futuro (`FR-007`)
- [X] T009 [US1] Scrivere in `docs/data_model.md` la sezione delle **tre grane** — appartenenza, calcolo, risultato — con la ragione per cui due non bastavano, e la chiusura esplicita di `R7` e della divergenza 7 sulla granularità ibrida di `BQ2-K1` e su quella dichiarata di `BQ2-K2` (`FR-008`, `FR-014`)
- [X] T010 [US1] Scrivere in `docs/data_model.md` la **matrice degli otto KPI** sulle tre grane, con le tabelle coinvolte, includendo i due di BQ3 dichiarati fuori dal modello (`FR-009`, `FR-029`)

**Verifica di fase**: eseguire la **Prova 3**. Otto righe, nessuna con conteggio zero.

---

## Fase 4: Storia utente 2 — Il mapping dei campi (Priorità P2)

**Obiettivo**: da quale colonna di quale dataset viene ogni cosa, e dove il modello deriva invece di leggere.

**Prova di indipendenza**: ogni colonna del modello dichiara dataset e campo di origine, oppure una regola di derivazione. Verifica per campionamento incrociando con il contratto della `003`.

- [X] T011 [US2] Scrivere in `docs/data_model.md` la **regola di ammissione delle colonne** — una colonna entra se una misura la legge, se identifica una riga per un lettore umano, o se rende visibile una proprietà strutturale — e dichiarare che l'assenza di una colonna è una decisione
- [X] T012 [US2] Scrivere in `docs/data_model.md` il **mapping delle colonne** delle sette tabelle, con campo di origine, tipo e ragione di ammissione (`FR-018`)
- [X] T013 [US2] Scrivere in `docs/data_model.md` le **esclusioni motivate**: `listed_in`, sostituito dal ponte; le caratteristiche audio fuori dai tre assi; `tvshow_seasons`, `date_added` e gli attributi anagrafici del catalogo video (`FR-026`)
- [X] T014 [US2] Scrivere in `docs/data_model.md` la sezione dei **tre assi di mood**, con il campo che realizza ciascuno, la scala, e la ragione per cui il candidato alternativo dell'asse ritmo è stato scartato (`FR-019`), insieme al limite che «misurato direttamente» significa letto senza trasformazione e non misura fisica
- [X] T015 [US2] Scrivere in `docs/data_model.md` la sezione sulla **popolarità**: da quale tabella la misura la legge, che cosa cambierebbe leggendola dall'altra, le tracce discordi e lo scarto massimo, entrambi ancorati (`FR-020`)
- [X] T016 [US2] Scrivere in `docs/data_model.md` la sezione delle **tre derivazioni interne al modello** con la regola di ciascuna, il divieto di arrotondamento sulla conversione di unità, l'invariante da verificare al caricamento su `dim_segment`, e la dichiarazione che il codice non è scritto da questa feature (`FR-021`)
- [X] T017 [US2] Scrivere in `docs/data_model.md` la sezione delle **cinque marcature della `003`**, con la grana di cui ciascuna è proprietà, la tabella su cui sale e la misura che condiziona, incluso che la quota di zeri per segmento diventa calcolabile (`FR-022`, `FR-023`)

**Verifica di fase**: prendere a campione cinque colonne del documento e ritrovarle nel contratto della `003` con lo stesso nome e lo stesso tipo. Una colonna che il contratto non descrive è un difetto.

---

## Fase 5: Storia utente 3 — I posti vuoti e le decisioni negative (Priorità P3)

**Obiettivo**: dichiarare la forma di ciò che questa feature non riempie, e le assenze che sono decisioni.

**Prova di indipendenza**: il documento dichiara la forma della tabella di corrispondenza senza dichiararne alcun contenuto, e `DA-1` non risulta né risolta né toccata.

- [X] T018 [US3] Scrivere in `docs/data_model.md` la sezione della tabella **`dim_category_mood`**: chiave, colonne, scala, cardinalità attesa, direzione della relazione, zero righe oggi, e i quattro obblighi che la `006` eredita dalla forma — inclusi che la confidenza non sale e che `DA-1` resta aperta (`FR-017`, `FR-028`)
- [X] T019 [US3] Scrivere in `docs/data_model.md` la sezione delle **decisioni negative**: nessuna dimensione di calendario e perché la sua assenza è la forma strutturale di un limite già dichiarato a parole; il profilo di mood in tabella separata e perché fonderlo nasconderebbe una giuntura (`FR-027`)
- [X] T020 [US3] Scrivere in `docs/data_model.md` la sezione **naming**: prefissi, lingua, e la ragione per cui i nomi delle misure sono quelli semantici già pubblicati in §5.4 del business case invece di una convenzione nuova (`FR-024`, `FR-025`)
- [X] T021 [US3] Scrivere in `docs/data_model.md` la sezione **limiti dichiarati**: cosa il modello rende impossibile misurare, incluse l'assenza di ogni entità che rappresenti una persona, l'inutilizzabilità del conteggio di righe per dimensionare un segmento — con il ritrovamento `T11` sul campione non più bilanciato — e le due inferenze da evitare
- [X] T022 [US3] Scrivere in `docs/data_model.md` la sezione dei **vincoli ereditati** dalle feature a valle, ciascuno con la feature a cui è assegnato, inclusa la divergenza 1 della revisione `003` registrata e **non chiusa** (`FR-016`, `FR-030`)

**Verifica di fase**: il documento è completo. È un buon punto di sosta: nulla è ancora marcato e nessun controllo è registrato.

---

## Fase 6: Marcatura e controllo ⚠️ tratto non interrompibile

**Scopo**: legare ogni quantità del documento all'artefatto che la produce, e portare il controllo al verde.

> **Non interrompere fra T023 e T026.** Fra la registrazione e il primo verde il repository ha un controllo che fallisce.

- [X] T023 Marcare ogni cifra e ogni numerale di `docs/data_model.md` con l'ancora al valore che lo produce, oppure con il marcatore di non-misurato, secondo la grammatica di `docs/convenzioni-marcatura.md` (`FR-004`)
- [X] T024 Registrare `docs/data_model.md` in `DOCUMENTS` di `scripts/check_audit_coherence.py` con `strict = True` e proprietario `feature 005`
- [X] T025 Eseguire `python3 scripts/check_audit_coherence.py` e correggere le sole **marcature**, mai i valori, fino all'esito verde
- [X] T026 Eseguire la **Prova 1** e la **Prova 2** del quickstart e verificare che il conteggio dei documenti passi da tre a quattro

**Verifica di fase**: Prova 1 e Prova 2 superate. Nessun avviso residuo sul documento nuovo, che è sotto severità stretta e non ne ammette.

---

## Fase 7: Note in loco su `docs/business_case.md`

**Scopo**: chiudere sull'artefatto già mergiato i due debiti che questa feature ha risolto, senza riscriverne il testo.

- [X] T027 Aggiungere a §5.2 di `docs/business_case.md` la **nota in loco** che dichiara l'insufficienza delle due granularità, con data, feature, affermazione precedente, affermazione corretta, causa della divergenza e fonte verificabile, coprendo sia la granularità ibrida di `BQ2-K1` sia la grana del risultato di `BQ2-K2` (`FR-013`, `FR-014`)
- [X] T028 Aggiungere a §4, domanda BQ2, di `docs/business_case.md` la **nota in loco** che dichiara come la barra «genere/mood» è stata sciolta e che il mood resta come attributo di confronto (`FR-015`)
- [X] T029 Eseguire la **Prova 4** e verificare che il testo originale di entrambi i passaggi sia ancora presente
- [X] T030 Rieseguire `python3 scripts/check_audit_coherence.py`, perché `docs/business_case.md` non è fra i documenti controllati ma le note citano identificativi che devono esistere

**Verifica di fase**: Prova 4 superata con `2`, `1`, `1`. Un valore diverso da `1` sulle ultime due significa che il testo originale è stato riscritto invece che annotato.

---

## Fase 8: Chiusura del drift sul README

**Scopo**: l'unico artefatto che ogni feature modifica e che nessuna spec possiede.

- [X] T031 Aggiungere in `README.md` la riga della `005` nella tabella di stato, con i deliverable e il collegamento a `specs/005-data-model-design/review.md` (`FR-031`)
- [X] T032 Estendere in `README.md` la prosa dei deliverable con il paragrafo sul modello dati, e allineare le sezioni `Setup` e `Struttura` a ciò che la feature aggiunge
- [ ] T033 Eseguire la **Prova 5**

**Verifica di fase**: Prova 5 superata con `1` a entrambe le righe. È il drift che si è già ripetuto due volte, sulla `003` e sulla `004`.

> **Aggiunta in corsa — 2026-08-18, `T045`.** La riga del README non può dichiarare `✅ conclusa, revisionata` in questa fase, perché la revisione avviene nella Fase 9 e il verbale non esiste ancora. Scriverlo qui lascerebbe nel repository, alla fine di questa sessione, **un'affermazione falsa su un artefatto pubblico** — che è esattamente il difetto che la `004` ha rischiato di portare su `main`.
>
> La riga viene quindi scritta ora in stato `🚧 in corso`, **senza il collegamento al verbale**, e `T045` la porta allo stato finale dopo la Fase 9. Il precedente dell'aggiunta di un task in corsa è `T049` della `003`.
>
> **Conseguenza sulla Prova 5**, che va detta perché altrimenti sembrerebbe fallita: la sua prima riga cerca il collegamento al verbale e in questa fase restituisce `0`. Non è un difetto del README, è la conseguenza di non poter linkare un file che non esiste — un collegamento morto su un artefatto pubblico è peggio di un collegamento assente. `T033` resta quindi **aperto** e si esegue dopo `T045`, quando entrambe le righe della prova possono essere vere insieme.

---

## Fase 9: Revisione in contesto pulito

**Scopo**: l'unico presidio contro un fatto misurato dichiarato come non-misurato, che nessun controllo automatico può vedere.

> **L'ordine di questa fase non è negoziabile.** Il verbale si scrive e si committa **prima** di toccare l'artefatto. È l'omissione della `004`, recuperata dopo e dichiarata come recupero.

- [X] T034 Consegnare a un revisore in contesto pulito — sessione separata o subagent isolato — una copia del **solo** `docs/data_model.md` in una cartella priva di ogni altro artefatto, con le tre domande della **Prova 7** e senza spec, piano, contratto o history git
- [X] T035 Scrivere `specs/005-data-model-design/review.md` con il verbale ricevuto, dichiarando in apertura che cosa è stato letto e cosa no, incluse le eventuali uscite dal perimetro, e ancorando la versione revisionata con commit e impronta del contenuto
- [ ] T036 **Committare il verbale prima di modificare `docs/data_model.md`**. Nessun rilievo va chiuso prima di questo commit
- [ ] T037 Chiudere i rilievi su `docs/data_model.md`, senza toccare il testo del revisore
- [ ] T038 Aggiungere in coda a `specs/005-data-model-design/review.md` il blocco di chiusura, dichiarando per **ogni** rilievo come è stato chiuso e distinguendo *risolvendolo* da *indebolendo l'affermazione*
- [ ] T039 Rieseguire la **Prova 1**, perché le correzioni possono aver mosso o rotto un'ancora
- [ ] T040 Eseguire la **Prova 8**

**Verifica di fase**: Prova 7 e Prova 8 superate. La Prova 8 fallisce se il verbale è stato committato dopo la modifica del documento, e non è verificabile leggendo il verbale: lo è solo dalla history.

---

## Fase 10: Rifinitura e riporto

- [ ] T041 [P] Eseguire la **Prova 6** e verificare che nessun artefatto della feature contenga una funzione DAX o una menzione di `.pbix` come file prodotto (`SC-006`)
- [ ] T042 [P] Eseguire la **Prova 9**, rileggendo la sezione dei limiti alla ricerca di un'affermazione che il documento non avrebbe avuto alcun vantaggio a scrivere
- [ ] T043 [P] Spuntare in `specs/005-data-model-design/checklists/requirements.md` il riquadro del principio III, ora che la stima è verificata sul piano
- [ ] T045 Portare la riga della `005` in `README.md` allo stato `✅ conclusa, revisionata`, con il collegamento al verbale ora esistente
- [ ] T044 Preparare il **riporto alla regia** con: il ritrovamento `F2` sulla materializzazione, rinviato per decisione del 2026-08-17 e da portare ora che la feature chiude; il ritrovamento `F3` sulle 114 voci della graduatoria, che è un vincolo per la `008`; il ritrovamento `T11` sul campione non più bilanciato; e lo scostamento di stima da 5 a ~6,25 ore con la sua causa

**Verifica di fase**: tutte e nove le prove superate.

---

## Dipendenze fra le fasi

```
Fase 1 (preparazione)
   └─> Fase 2 (fondamenta: apertura + definizione di segmento)
          ├─> Fase 3 — US1  ossatura            [MVP]
          │      └─> Fase 4 — US2  mapping
          │             └─> Fase 5 — US3  posti vuoti e decisioni negative
          │                    └─> Fase 6 (marcatura e controllo)  ⚠️ non interrompibile
          │                           ├─> Fase 7 (note in loco)
          │                           └─> Fase 8 (README)
          │                                  └─> Fase 9 (revisione)
          │                                         └─> Fase 10 (rifinitura e riporto)
```

Le tre storie utente sono in **sequenza e non in parallelo**, perché scrivono lo stesso file e perché la `US2` mappa colonne su tabelle che la `US1` deve aver dichiarato. La `US1` resta però indipendentemente verificabile: la Prova 3 la chiude senza che la `US2` esista.

Fase 7 e Fase 8 sono indipendenti fra loro e potrebbero invertirsi. Sono tenute in quest'ordine perché la riga del README rinvia al verbale, che la Fase 9 produce: scrivere il rinvio prima rende visibile subito se il collegamento è sbagliato.

## Opportunità di parallelizzazione

Quattro task su quarantaquattro. `T002` tocca `research.md` mentre `T001` crea il documento; `T041`, `T042` e `T043` sono verifiche su artefatti diversi e nessuna scrive sul documento.

Tutto il resto è sequenziale, e la ragione è dichiarata in testa a questo file.

## Ambito del MVP

**La Fase 3 conclusa è già consegnabile.** Un documento con l'apertura, la definizione operativa di segmento, le sette tabelle, la regola di lettura, le relazioni e la matrice delle tre grane sugli otto KPI è sufficiente perché la `007` sappia su quale tabella calcolare ogni misura e a che cosa si riferisce ogni risultato.

Ciò che mancherebbe — mapping dei campi, assi di mood, popolarità, naming — è la Fase 4 e oltre. È il taglio `005a`/`005b` che la regia aveva preparato in caso di sforamento, e che **non si attiva**: la stima rivista di ~6,25 ore sta dentro le 6-7 del principio III. Resta descritto qui perché un piano che conosce il proprio punto di taglio è più sicuro di uno che dovrebbe inventarlo a metà.
