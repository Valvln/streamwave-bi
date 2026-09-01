<!--
SYNC IMPACT REPORT
==================
Emendamento 1.1.0 → 1.2.0 (2026-08-20)
--------------------------------------
Bump rationale: MINOR. Nessun principio rimosso ne' ridefinito in modo incompatibile: si amplia
l'elenco delle fonti dati ammesse con una classe che prima non c'era. E' lo stesso tipo di
modifica della 1.1.0 e prende lo stesso bump, invece del PATCH che la formulazione piu' comoda
avrebbe permesso di rivendicare come "chiarimento".
Modifica: ammesse le **assegnazioni dell'analista congelate in un artefatto versionato** come
quinta fonte dati, a cinque condizioni (criterio scritto e committato prima di qualunque valore,
valore congelato e mai rigenerato da uno script, numero di versione con obbligo di dichiarazione
a valle, revisione indipendente contro il criterio con esito quantificato, nessuna promozione di
confidenza). Corretta di conseguenza la frase del principio I che vincolava le assunzioni sui
dati sintetici a essere versionate "insieme allo script che le implementa": dove lo script non
esiste, e non deve esistere, il vincolo era inapplicabile alla lettera.
Nessuna nuova etichetta di fonte: la classe vive sotto `Sintetico`, che il principio I gia'
enumera. L'elenco delle etichette resta invariato.
Motivazione: la feature 006 costruisce `dim_category_mood`, la tabella che assegna un profilo di
mood a ciascuna categoria video. E' l'unico strato interpretativo del progetto e regge tre KPI su
otto. I suoi valori non sono osservati su alcuna fonte e non sono calcolati da alcuna formula:
li assegna una persona, su proposta di un LLM invocato manualmente una sola volta. La decisione
DA-1 della roadmap, risolta il 2026-08-19, ne ammette il metodo a condizione che nessuno script
chiami mai il modello — il che rende la tabella un artefatto curato a mano, esattamente come
data/benchmarks/bq3_tier_upgrade.json della 004.
La differenza e' che quel file e' ammesso perche' la 1.1.0 gli ha scritto un proprio comma. La
mano curata era ammessa **solo quando la fonte e' esterna**. Un'assegnazione dell'analista non lo
e', e l'etichetta `Sintetico` la escludeva alla lettera, perche' l'elenco delle fonti ammesse la
definiva come "dati sintetici generati da script versionati". Usare quell'etichetta senza
emendare sarebbe stato un aggiramento silenzioso, che e' la formula con cui la 1.1.0 ha motivato
se stessa.
Ritrovamento collaterale, che vale la pena registrare: la tabella era gia' promessa dalla D1
della feature 001 — "una tabella di corrispondenza curata e versionata" — senza che nessuno si
accorgesse che non era una fonte ammessa. L'emendamento regolarizza una promessa vecchia di
quattordici giorni, non solo una feature che sta per aprirsi.
Template dipendenti:
  ✅ .specify/templates/spec-template.md — aggiunta la condizione per l'assegnazione dell'analista
     accanto a quella dei benchmark, nello stesso commit
  ✅ .specify/templates/plan-template.md e tasks-template.md — nessuna modifica: non enumerano fonti
Artefatti gia' prodotti: nessuno viola il nuovo testo, che amplia e non restringe. I valori
sintetici della 004 sono generati da uno script e restavano conformi anche prima. La tabella che
il nuovo comma ammette non esiste ancora: e' il deliverable della 006.

Emendamento 1.0.2 → 1.1.0 (2026-08-15)
--------------------------------------
Bump rationale: MINOR. Nessun principio rimosso né ridefinito in modo incompatibile: si amplia
l'elenco delle fonti dati ammesse con una classe che prima non c'era, e si estende di conseguenza
l'enumerazione delle etichette di fonte del principio I. È un ampliamento sostanziale di una guida
esistente, non un chiarimento: prima dell'emendamento un parametro preso da una pubblicazione di
settore non era una fonte ammessa, e usarlo sarebbe stato un aggiramento silenzioso.
Modifica: ammessi i **benchmark pubblici di settore** come quarta fonte dati, a cinque condizioni
(citazione puntuale, valore congelato in un file versionato, nessuna chiamata di rete a runtime,
assunzione di trasferimento dichiarata, nessuna promozione automatica del livello di confidenza).
Aggiunta l'etichetta di fonte `Benchmark (esterno)` al principio I.
Motivazione: la feature 004 genera i dati sintetici di BQ3. Senza questo emendamento sarebbe
l'unico artefatto del progetto in cui la fonte di ogni parametro è "l'analista ha deciso così" —
formalmente conforme, perché i sintetici con assunzioni dichiarate a confidenza bassa erano già
ammessi, ma incoerente con la tesi che il progetto sostiene, che è il principio I. Un parametro
di scenario ancorato a una pubblicazione citabile è verificabile da chi legge; uno deciso a
tavolino no.
Perché non un quarto livello di confidenza: un benchmark è un dato osservato su un terzo e
trasferito a StreamWave, cioè la stessa natura di A1 del business case, che §6 tiene fuori scala
per costruzione. Un quarto livello cambierebbe l'asse su cui tutti e 8 i KPI sono già classificati
e obbligherebbe a rivederli uno per uno, per coprire un caso che il pattern esistente copre già.
Template dipendenti:
  ✅ .specify/templates/spec-template.md — aggiunta l'etichetta `Benchmark (esterno)` all'elenco
     delle fonti e la condizione di citazione, nello stesso commit
  ✅ .specify/templates/plan-template.md e tasks-template.md — nessuna modifica: non enumerano fonti
Artefatti già prodotti: nessuno viola il nuovo testo, che amplia e non restringe. Resta il debito
testuale già tracciato in docs/roadmap.md — assunzione di trasferimento in §2 di
docs/business_case.md, richiamo in §6, note datate sulle schede BQ3-K1 e BQ3-K2 — da chiudere
dentro la 004 o subito prima. È debito preesistente all'emendamento, non creato da esso.

Emendamento 1.0.1 → 1.0.2 (2026-08-08)
--------------------------------------
Bump rationale: PATCH. Nessun principio aggiunto, rimosso o ridefinito: si definisce l'unità di
misura di un vincolo già esistente nel principio III, che era espresso in "giornate lavorative"
senza dichiarare che cosa fosse una giornata.
Modifica: "una giornata lavorativa" è definita come 6-7 ore di lavoro effettivo e non come un
giorno di calendario; il vincolo di stato coerente del repository è esteso alla fine di ogni
sessione di lavoro, non solo alla chiusura della feature.
Motivazione: la feature 001 è costata circa 7 ore distribuite su tre giorni di calendario. Letta
alla lettera come giorno di calendario, la prima feature del progetto violava il principio che
la inaugurava; letta come sforzo, vi rientrava comodamente. L'ambiguità andava chiusa in un senso
o nell'altro prima che la capacità disponibile scendesse a circa 2 ore al giorno, condizione in
cui la lettura a calendario avrebbe reso non avviabile quasi ogni feature residua.
Template dipendenti: nessuno impattato. Verificato che nessun template sotto .specify/templates/
né prompt sotto .github/ citi la giornata lavorativa.
Artefatti già prodotti: nessuno da correggere. La feature 001 è conforme al testo emendato.

Emendamento 1.0.0 → 1.0.1 (2026-08-06)
--------------------------------------
Bump rationale: PATCH. Nessun principio aggiunto, rimosso o ridefinito: si esplicita una
convenzione operativa dentro una sottosezione già esistente ("Convenzioni", in Workflow di
Sviluppo e Quality Gate).
Modifica: fissata la lingua di progetto — prosa in italiano senza traduzione successiva,
identificativi tecnici (KPI, misure DAX, colonne, file, branch) in inglese.
Template dipendenti: nessuno impattato.

Ratifica iniziale (2026-08-06)
------------------------------
Version change: TEMPLATE (non ratificata) → 1.0.0
Bump rationale: prima ratifica. Nessuna versione precedente da confrontare, quindi MAJOR
                secondo la policy di versioning (adozione iniziale dell'impianto di governance).

Principi definiti (tutti nuovi, dai segnaposto 1-5 del template):
  - slot 1 → I. Provenienza e Confidenza dei Dati (NON NEGOZIABILE)
  - slot 2 → II. Riproducibilità Totale
  - slot 3 → III. Incrementalità
  - slot 4 → IV. Trasparenza sui Limiti
  - slot 5 → V. Confine dell'Automazione
  - aggiunto oltre i 5 del template → VI. Coerenza Narrativa

Sezioni aggiunte (dai segnaposto 2 e 3 del template):
  - slot 2 → Vincoli di Dominio e di Dato
  - slot 3 → Workflow di Sviluppo e Quality Gate

NOTA: questo report evita di citare letteralmente i token segnaposto del template
(fra parentesi quadre) perché l'estensione VSCode SpecKit Companion li cerca con una regex
sull'intero file e classificherebbe la constitution come non ancora compilata.

Sezioni rimosse: nessuna.

Template dipendenti:
  ✅ .specify/templates/spec-template.md — aggiunte due sezioni obbligatorie
     ("Provenienza e Confidenza dei Dati", "Limiti Dichiarati") a supporto dei principi I e IV
  ✅ .specify/templates/plan-template.md — nessuna modifica necessaria: il blocco
     "Constitution Check" è un segnaposto popolato in fase di /speckit.plan a partire da questo file
  ✅ .specify/templates/tasks-template.md — nessuna modifica necessaria: le categorie di task
     sono agnostiche e il vincolo di 1 giornata (principio III) si applica in fase di scomposizione
  ✅ .claude/skills/speckit-*/SKILL.md e .github/prompts/speckit.*.prompt.md — nessun riferimento
     obsoleto o agent-specifico da correggere
  ✅ README.md — allineato (licenza MIT, stato fasi)

TODO differiti: nessuno. Lo stack tecnico non è vincolato di proposito (vedi sezione
"Vincoli di Dominio e di Dato"): la scelta è demandata alla fase /speckit.plan.

NOTA IN LOCO — 2026-08-29
-------------------------
docs/roadmap.md non fa più parte del repository: era il piano di lavoro della regia, non un
artefatto pubblicato, ed è uscito dal versionamento il 2026-08-29. I due rinvii che i Sync
Impact Report qui sopra le fanno restano nel testo perché un verbale di emendamento non si
riscrive. Dove ora vive ciò che citavano:
  - la decisione DA-1, in docs/mood_assignment_criteria.md, sezione "La decisione di processo";
  - il debito testuale sull'assunzione di trasferimento, nel tracker delle issue.
-->

# StreamWave BI Constitution

Case study di Business Intelligence a supporto di una decisione strategica: StreamWave, piattaforma di streaming video, valuta l'ingresso nel verticale del music streaming. Il criterio di accettazione di ogni artefatto prodotto è uno solo: **deve reggere la presentazione a un board reale**. Chi legge può non fidarsi dell'analista, ma deve poter verificare da dove viene ogni numero.

## Core Principles

### I. Provenienza e Confidenza dei Dati (NON NEGOZIABILE)

Ogni KPI, metrica o numero mostrato in dashboard, report o documentazione DEVE dichiarare in modo leggibile dall'utente finale:

- **Fonte**: `Netflix (reale)`, `Spotify (reale)`, `Sintetico`, `Benchmark (esterno)` o `Derivato` (calcolato da più fonti — in tal caso vanno elencate le fonti a monte).
- **Livello di confidenza**: `alto`, `medio` o `basso`, con il criterio di attribuzione documentato nella feature che introduce la metrica.

Un valore etichettato `Benchmark (esterno)` è un dato osservato **su un operatore terzo** e trasferito a StreamWave. L'ancoraggio a una fonte citabile NON DEVE essere trattato come un innalzamento del livello di confidenza: la trasferibilità è una questione diversa dalla solidità del calcolo, e va dichiarata come **assunzione di trasferimento** insieme al valore, sul modello dell'assunzione strutturale che regge l'uso dei proxy. Un parametro di scenario ancorato resta a confidenza `bassa` finché nulla di osservato su StreamWave lo sostiene, e continua quindi a essere presentato come range best/base/worst.

Un valore sintetico NON DEVE essere presentato con precisione superiore a quanto la metodologia giustifica: se la generazione poggia su un'assunzione a una cifra significativa, il risultato non può esserne mostrato con tre.

Dove la confidenza è `bassa`, il valore DEVE essere espresso come **range best/base/worst case**, mai come numero singolo. Un numero singolo comunica una certezza che il dato non ha.

Le assunzioni dietro ogni dato sintetico DEVONO essere dichiarate per iscritto e versionate insieme allo script che le implementa, non solo nel commento del codice. Dove il valore sintetico è **assegnato e non generato** — e quindi nessuno script lo implementa — le assunzioni DEVONO essere versionate insieme al **criterio** che governa l'assegnazione, che ne prende il posto e ne assume gli obblighi.

*Rationale*: il progetto mescola dati reali di due domini diversi con dati simulati per un mercato in cui StreamWave non è ancora entrata. Senza etichettatura esplicita, la dashboard diventa indistinguibile da una previsione inventata — ed è esattamente l'obiezione che un board solleverebbe per primo.

### II. Riproducibilità Totale

Ogni trasformazione sui dati — cleaning, join, feature engineering, aggregazione, generazione sintetica — DEVE essere implementata come codice in **Python** o **Power Query M** e versionata nel repository.

Sono VIETATE le modifiche manuali one-off su file Excel o CSV. Se un dato è sbagliato, si corregge lo script che lo produce, non il file di output.

`data/raw/` è **immutabile e in sola lettura**: nessuno script scrive al suo interno. Il contenuto DEVE essere ricostruibile da fonte pubblica tramite `scripts/download_data.sh`.

Chiunque cloni il repository DEVE poter rigenerare ogni dataset intermedio e finale partendo solo dal codice versionato e dai dataset pubblici di origine.

*Rationale*: un'analisi che non si può rieseguire non si può nemmeno difendere. Una modifica manuale non tracciata rende l'intera catena non verificabile a valle.

### III. Incrementalità

Ogni feature DEVE essere completabile in **una giornata lavorativa**, dove per giornata lavorativa si intendono **6-7 ore di lavoro effettivo** e non un giorno di calendario. Se la stima supera quel limite, la feature NON DEVE essere avviata: va prima scomposta in unità più piccole, ciascuna con valore dimostrabile in autonomia.

La distinzione è operativa. Quando la capacità giornaliera disponibile è inferiore a una giornata piena, una feature conforme PUÒ occupare più giorni di calendario senza per questo violare il principio: ciò che il vincolo limita è la **dimensione della feature**, non la sua distensione nel tempo.

Ogni feature DEVE lasciare il repository in uno stato coerente e presentabile: niente rami di lavoro che restano aperti a metà tra due stati funzionanti. Quando una feature attraversa più sessioni di lavoro, questo vincolo si applica **alla fine di ogni sessione**, non soltanto alla chiusura della feature.

*Rationale*: vincolo di ritmo, non di ambizione. Feature piccole significano feedback frequente, history git leggibile e nessun blocco su lavori lunghi mai finiti — il modo tipico in cui un progetto da portfolio muore a metà. Misurare il limite in ore di lavoro anziché in giorni di calendario è ciò che gli permette di continuare a mordere quando la capacità disponibile cambia: letto come giorno di calendario, si allargherebbe e si stringerebbe da solo a ogni variazione dell'agenda, cioè smetterebbe di essere un limite. L'estensione del vincolo di coerenza a ogni fine sessione è il contrappeso: è ciò che impedisce alla distensione nel tempo, ora esplicitamente ammessa, di reintrodurre dalla finestra i rami aperti a metà che il principio esclude dalla porta.

### IV. Trasparenza sui Limiti

Ogni feature analitica DEVE dichiarare esplicitamente **cosa NON risponde**, in una sezione dedicata della propria spec e — dove il consumatore è l'utente finale — nella dashboard stessa.

La dichiarazione DEVE coprire almeno: domande fuori portata dei dati disponibili, conclusioni che il lettore potrebbe erroneamente inferire, e vincoli temporali o di copertura del dato (es. catalogo Netflix fermo al 2021).

Una correlazione NON DEVE mai essere presentata con lessico causale.

*Rationale*: l'omissione di un limite è di fatto un'affermazione implicita. Dichiarare il perimetro protegge sia il lettore sia la credibilità dell'analisi.

### V. Confine dell'Automazione

L'automazione — script, agent, Claude Code — copre: data prep, ETL, misure DAX, generazione di dati sintetici, documentazione e testing.

L'interazione con l'**interfaccia grafica di Power BI Desktop e Tableau Public** resta **manuale** ed è fuori dallo scope automatizzabile. Nessun task può presupporre che un agent pilota quelle GUI.

Ne consegue che i task di build della dashboard DEVONO essere formulati come istruzioni eseguibili da una persona, e che tutto ciò che è esprimibile come artefatto testuale versionabile (misure DAX, schema del modello dati, mapping dei campi) DEVE esserlo, invece di vivere solo dentro il file binario del report.

*Rationale*: confine onesto tra ciò che l'automazione fa davvero e ciò che richiede una persona davanti allo schermo. Massimizza al contempo la porzione di lavoro che resta versionata e ispezionabile.

### VI. Coerenza Narrativa

Ogni feature DEVE essere riconducibile a una delle tre domande di business (BQ1, BQ2, BQ3 definite nella sezione seguente). La spec di ogni feature DEVE indicare a quale domanda risponde e in che modo vi contribuisce.

Una feature che non è riconducibile a nessuna delle tre NON DEVE essere implementata: va prima motivata come estensione dello scope, con aggiornamento esplicito di questo documento.

*Rationale*: un case study da portfolio si giudica sul filo del discorso, non sul numero di grafici. Il vincolo di tracciabilità impedisce l'accumulo di analisi tecnicamente corrette ma narrativamente inerti.

## Vincoli di Dominio e di Dato

**Le tre domande di business** che l'intero progetto deve servire:

- **BQ1 — Posizionamento**: qual è il posizionamento del contenuto musicale rispetto a quello video in termini di caratteristiche "vincenti" (durata, genere, mood)? Esiste overlap di audience potenziale?
- **BQ2 — Segmento di ingresso**: quale segmento musicale (genere/mood) rappresenterebbe l'opportunità di ingresso più coerente con il catalogo attuale di StreamWave?
- **BQ3 — Impatto stimato**: che impatto stimato — simulato, con assunzioni dichiarate — avrebbe l'aggiunta del verticale musicale su engagement e revenue?

**Fonti dati ammesse**:

- `data/raw/netflix_titles.csv` — catalogo Netflix, proxy del catalogo StreamWave. Copertura fino al 2021: ogni conclusione temporale DEVE tenerne conto (principio IV).
- `data/raw/spotify_tracks_dataset.csv` — tracce Spotify con audio feature, proxy del mercato musicale.
- Dati sintetici generati da script versionati, esclusivamente dove i dati reali non esistono (tipicamente BQ3: engagement e revenue di un verticale non ancora lanciato).
- **Benchmark pubblici di settore** — valori osservati e pubblicati da terzi, usati per ancorare i parametri che alimentano la generazione sintetica invece di stabilirli per scelta dell'analista.
- **Assegnazioni dell'analista congelate in un artefatto versionato** — valori che nessuna fonte osserva e nessuna formula calcola, e che una persona attribuisce, esclusivamente dove il confronto che li richiede non esiste altrimenti nei dati.

Un benchmark è una fonte ammessa solo se soddisfa **tutte** le condizioni seguenti:

1. **Citazione puntuale**: organizzazione che pubblica, titolo, data di pubblicazione, riferimento recuperabile e data di accesso. Un valore attribuito a «ricerche di settore» non è citato ed è vietato.
2. **Valore congelato in un file versionato**: il numero adottato vive in un artefatto del repository insieme alla sua citazione, non nella prosa di un documento né in un commento del codice. Chi rilegge deve poter vedere il numero senza rieseguire la ricerca.
3. **Nessuna chiamata di rete a runtime**: nessuno script contatta una fonte esterna durante l'esecuzione della pipeline. La raccolta è un passaggio umano, non riproducibile, e per questo il suo esito va congelato; la generazione che ne discende resta rieseguibile da una copia pulita a partire dal file versionato (principio II).
4. **Assunzione di trasferimento dichiarata**: il benchmark descrive un operatore terzo, e l'assunzione che il suo valore si applichi a StreamWave va scritta accanto al valore, non sottintesa.
5. **Nessuna promozione di confidenza**: vedi principio I.

Un benchmark che non soddisfa una qualsiasi di queste condizioni NON DEVE essere usato: il parametro torna a essere una scelta dell'analista e va dichiarato come tale, il che è ammesso e sempre preferibile a una citazione che non regge il controllo.

Quella scelta dell'analista **è la quinta fonte**, e il comma che segue la regola. Il testo qui sopra la nominava già come ripiego ammesso senza mai porle una condizione, e la nominava per il caso in cui alimenta una generazione: uno script legge il parametro e produce il valore. Dove invece **il valore assegnato è esso stesso il dato pubblicato**, e nessuno script interviene, l'etichetta `Sintetico` non lo copriva — l'elenco delle fonti la definisce come dato generato da script versionati. È il caso della tabella che porta il lato video sugli assi di mood, e il comma esiste per esso.

Un'assegnazione dell'analista è una fonte ammessa solo se soddisfa **tutte** le condizioni seguenti:

1. **Criterio scritto prima del valore**: il criterio che governa l'assegnazione vive in un artefatto versionato ed è congelato in un commit **che non contiene alcun valore**, nemmeno di prova. Un criterio scritto dopo aver visto i valori si piega a giustificarli invece di vincolarli, anche in perfetta buona fede, e la differenza non è verificabile in prosa: lo è solo nell'ordine dei commit.
2. **Valore congelato e mai rigenerato**: i valori vivono in un artefatto versionato che **nessuno script scrive**. Se l'assegnazione è assistita da un modello, il modello NON DEVE essere invocato da alcuno script, né a runtime né in fase di build; la proposta che produce è versionata come artefatto distinto dall'esito, insieme al prompt, al nome del modello e alla data.
3. **Numero di versione dichiarato a valle**: l'artefatto porta una versione, e ogni valore pubblicato che ne dipende DEVE dichiarare su quale versione è stato calcolato. Senza questo legame una correzione lascia a valle numeri corretti quando sono stati scritti e mai più riverificati, indistinguibili da quelli ancora validi.
4. **Revisione indipendente contro il criterio**: l'assegnazione è verificata da chi non l'ha prodotta, contro il criterio della condizione 1 e nessun altro metro, e l'esito è versionato con la **misura di quanto la revisione ha corretto**. Una revisione che non dichiara quanto ha spostato non è distinguibile da una ratifica.
5. **Nessuna promozione di confidenza**: vedi principio I. Nessuna cura nella costruzione trasforma un giudizio in un'osservazione, e la confidenza dei valori che ne discendono non sale per il fatto che il processo sia stato accurato.

Un'assegnazione che non soddisfa una qualsiasi di queste condizioni NON DEVE essere pubblicata come dato. Non esiste per essa un ripiego ulteriore: è già l'ultimo, ed è la ragione per cui le sue condizioni sono più severe di quelle di un benchmark invece che più lasche.

L'uso di Netflix come proxy di StreamWave e di Spotify come proxy del mercato musicale è una **assunzione strutturale del case study** e DEVE essere dichiarata in ogni artefatto rivolto all'utente finale, non solo nella documentazione tecnica.

**Stack tecnico**: deliberatamente non vincolato da questa constitution, salvo per quanto imposto dai principi II (Python o Power Query M per le trasformazioni) e V (Power BI Desktop e Tableau Public come strumenti di presentazione a interazione manuale). Ogni ulteriore scelta tecnologica è demandata alla fase `/speckit.plan` e va motivata lì.

## Workflow di Sviluppo e Quality Gate

Il progetto segue il flusso spec-driven di Spec Kit: `/speckit.constitution` → `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`.

**Gate prima di iniziare l'implementazione di una feature**:

1. La spec dichiara a quale domanda di business risponde (principio VI).
2. La spec contiene la sezione "Limiti Dichiarati" compilata (principio IV).
3. La spec contiene la sezione "Provenienza e Confidenza dei Dati" per ogni metrica introdotta (principio I).
4. La stima è entro una giornata lavorativa, o la feature è già stata scomposta (principio III).

**Gate prima di considerare una feature conclusa**:

1. Ogni trasformazione è scriptata e versionata; nessun passaggio manuale non documentato (principio II).
2. La pipeline è rieseguibile da zero su una copia pulita del repository.
3. Ogni numero pubblicato è etichettato con fonte e confidenza; i valori a bassa confidenza sono espressi come range (principio I).
4. I task che richiedono la GUI di Power BI o Tableau sono scritti come istruzioni manuali verificabili da una persona (principio V).

**Convenzioni**:

- **Lingua**: tutta la prosa del progetto — documentazione, spec, commenti, commit, etichette di dashboard — è in **italiano**. Scelta deliberata e non soggetta a traduzione successiva: il progetto non verrà tradotto in inglese, e nessun artefatto va scritto in inglese "per sicurezza".
- **Identificativi in inglese**: nomi di KPI, misure DAX, colonne, tabelle, file, cartelle e branch sono in inglese, in ogni caso. Sono la parte più costosa da rinominare a valle e seguono la convenzione universale, indipendentemente dalla lingua della prosa.
- **Commit**: in italiano, imperativo, con prefisso convenzionale (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`). La history è parte dell'artefatto da portfolio e va tenuta leggibile.

## Governance

Questa constitution **prevale su ogni altra pratica di progetto**. In caso di conflitto tra una scelta di comodo e un principio qui dichiarato, prevale il principio; se il principio è davvero inapplicabile, si emenda il documento — non lo si aggira in silenzio.

**Procedura di emendamento**:

1. La modifica proposta è motivata per iscritto (principio interessato, ragione, impatto sugli artefatti già prodotti).
2. Il documento viene aggiornato insieme al Sync Impact Report in testa al file.
3. I template dipendenti sotto `.specify/templates/` vengono riallineati nello stesso commit.
4. Gli artefatti già prodotti che violano il nuovo testo vengono corretti o esplicitamente marcati come debito con scadenza.

**Policy di versioning** (semantic versioning):

- **MAJOR**: rimozione o ridefinizione incompatibile di un principio o della governance.
- **MINOR**: aggiunta di un nuovo principio o di una sezione, o ampliamento sostanziale di una guida esistente.
- **PATCH**: chiarimenti, riformulazioni, correzioni non semantiche.

**Verifica di conformità**: la conformità va verificata a ogni gate di feature (vedi sezione precedente) e durante `/speckit.analyze`. Ogni violazione consapevole DEVE essere registrata nella tabella "Complexity Tracking" del piano della feature, con la giustificazione e l'alternativa più semplice che è stata scartata.

**Version**: 1.2.0 | **Ratified**: 2026-08-06 | **Last Amended**: 2026-08-20
