# Feature Specification: Dashboard — narrazione, limiti a schermo, rifiniture

**Feature Branch**: `008b-dashboard-narrative-polish`

**Created**: 2026-08-27

**Status**: Draft

**Input**: User description: "Narrazione, limiti dichiarati portati a schermo, e le rifiniture che rendono il `.pbix` pubblicabile — che non lo è ancora, per dichiarazione esplicita della `008a`. Nessuna pagina nuova, nessuna misura nuova, nessun KPI nuovo: questa feature scrive sopra un modello e una struttura già chiusi. Il deliverable vive nella GUI: la sessione scrive un contratto di narrazione, Valerio esegue, la sessione documenta l'esito. Requisiti dalla sezione «Che cosa la `008a` non garantisce». `C2` non esiste e non deve comparire; `C1` e `C3` non si compongono. Le issue `#18` e `#11` restano aperte; se il file si riapre, la verifica delle tre impostazioni di `#20` viene prima di qualunque rifinitura. `segment_display`, non `segment`. Il debito della `004` sul benchmark resta aperto e dichiarato. La feature si ferma prima del merge e riporta, per la prima volta nel progetto, che il file è pubblicabile e perché."

*(Il prompt di consegna integrale è più esteso di questa sintesi. Ogni vincolo che conteneva compare qui sotto come decisione, requisito, criterio di successo o limite dichiarato: questa spec è il testo autorevole, non il prompt.)*

---

## La domanda a cui questa spec risponde per prima

La `008a` ha lasciato scritta, in una sezione che nessun'altra feature del progetto ha mai avuto, la lista dei propri difetti dichiarati: *«Il file è leggibile, non pubblicabile, e non va mostrato a un lettore esterno prima che la `008b` chiuda.»* Questa feature esiste per chiudere quella frase, e la domanda che precede ogni scelta di testo è: **che cosa deve essere vero perché quella frase possa essere ritirata, e chi lo verifica?**

La risposta di questa spec ha due metà, e la seconda conta quanto la prima.

La prima metà è il contenuto: mancano a schermo i limiti dichiarati che il principio IV impone, l'assunzione strutturale dei proxy che la constitution impone in **ogni** artefatto rivolto all'utente finale, e il *perché* delle etichette di confidenza che la `008a` ha portato a schermo senza spiegarle. Sono tre assenze nominate, non un giudizio estetico su una dashboard spoglia.

La seconda metà è il presidio. Nelle otto feature precedenti ogni numero pubblicato aveva un'ancora e uno script che la verificava; **la prosa non ha ancore.** Un blocco di testo su una pagina è la prima cosa che questo progetto pubblica che nessun controllo può leggere e nessun artefatto può contraddire, e vive per giunta dentro un file binario non versionato. Ne discende il vincolo che governa l'intera feature: **il testo che andrà a schermo si scrive qui, alla lettera, prima che Power BI venga riaperto** — non si descrive, non si riassume, non si delega a chi costruisce. Un contratto che dicesse «spiegare l'asimmetria di `BQ1-K2`» lascerebbe le parole vere fuori dal repository, fuori dalla revisione e fuori da qualunque verifica: sarebbe la stessa dashboard senza narrazione, con in più un documento che dichiara di averla.

E ne discende il secondo vincolo, che è il rovescio del primo: **nessun numero si digita in un blocco di narrazione.** I numeri a schermo sono quelli che le misure della `008a` producono; un numero scritto dentro una casella di testo è un valore la cui unica fonte è che qualcuno lo ha scritto, che è ciò che il principio I vieta e che la decisione `F7` della `008a` ha già rifiutato una volta per le due soglie del quadrante.

---

## Le decisioni che questa feature prende

Otto decisioni, numerate `N1`-`N8` per non collidere con le `D1`-`D11` della `007a`/`007b`, le `E1`-`E9` della `007b`, le `F1`-`F9` e le `CP-1`-`CP-3` della `008a`. Ciascuna riporta il contesto che l'ha sollevata, le opzioni sul tavolo, la scelta e la ragione.

### N1 — Il contratto porta il testo letterale, non la sua descrizione

**Il contesto**: il contratto di pagina della `008a` è un documento di **disegno** — quali KPI, quale visuale, quali filtri — e dichiara esplicitamente di non decidere «la prosa, i limiti in forma divulgativa, il tono», perché sono di questa feature. Il deliverable della `008a` era una struttura, e una struttura si descrive; il deliverable di questa feature **è prosa**, e una prosa descritta non è una prosa.

**Le opzioni**: (a) un contratto che dichiara, per ciascuno spazio riservato, quali obblighi il testo deve soddisfare, lasciando a chi costruisce la formulazione; (b) un contratto che porta il **testo letterale** di ogni blocco, pronto da incollare, con accanto l'obbligo che lo richiede e la fonte da cui discende; (c) come (b), ma pubblicando il testo anche sotto `docs/` come nono documento del progetto.

**La decisione**: **(b)**. Il contratto di narrazione contiene, per ogni blocco, quattro cose: **dove va** (pagina e spazio riservato della `008a` §8), **che cosa dice** alla lettera, **quale obbligo lo richiede** (principio, sezione di documento o issue), e **che cosa non dice** dove esiste una formulazione vicina e sbagliata da escludere.

**La ragione**: (a) è la forma che la `008a` ha usato correttamente per le visuali, e sbagliata qui per una ragione di verificabilità, non di gusto. Il presidio di questo progetto sulla prosa è la revisione in contesto pulito; un revisore che ricevesse (a) revisionerebbe un elenco di obblighi, non il testo che il lettore incontrerà — e il testo, scritto poi da una persona davanti allo schermo, entrerebbe nel deliverable senza essere passato da alcun controllo. È lo stesso difetto che la condizione 1 delle assegnazioni dell'analista (constitution, Vincoli di Dominio e di Dato) vieta per i valori: ciò che si scrive dopo aver visto l'esito si piega a giustificarlo.

(c) è respinta perché aggiungerebbe un documento pubblicato che non pubblica nulla di nuovo: ogni affermazione della narrazione è già in uno dei sette documenti sotto `docs/`, e una seconda copia è una copia che può divergere dall'originale senza che nulla lo segnali — il difetto che la `008a` §"Che cosa questo documento non contiene" nomina per i valori e che vale identico per le affermazioni. Il contratto vive dove vivono gli altri artefatti di disegno di questa famiglia, sotto `specs/`, e il README dice a chi legge da fuori che è lì.

**Che cosa questo non rende**: non rende il contratto un manuale di clic. Dove il testo va è dichiarato in termini di spazio riservato e di pagina; **come** si crea una casella di testo, quale carattere, quale allineamento, appartiene a chi costruisce, e prescriverlo sarebbe pilotare la GUI per interposta prosa (principio V).

---

### N2 — Nessun numero digitato nella narrazione, e una lista chiusa di eccezioni dichiarate

**Il contesto**: il principio I vieta il valore senza fonte. Una casella di testo è il luogo in cui quel divieto è più facile da violare e più difficile da vedere: nessuno script del repository entra nel `.pbix`, nessuna misura contraddice un numero scritto a mano, e un numero in prosa accanto a una scheda sembra provenire dalla scheda. La `008a` ha già rifiutato questa scorciatoia una volta — `F7`, le due soglie del quadrante esposte come misure invece che digitate come costanti.

**Le opzioni**: (a) i numeri si possono scrivere, purché coincidano con quelli pubblicati; (b) nessun numero, mai, in alcun blocco di narrazione; (c) nessun numero, salvo una **lista chiusa** dichiarata nel contratto, in cui ogni voce nomina l'artefatto che la pubblica e la ragione per cui non può provenire da una misura.

**La decisione**: **(c)**. La regola operativa è: **la narrazione rimanda a ciò che il lettore vede nella visuale, invece di ripeterlo.** Dove deve nominare una quantità, la nomina per la marcatura che il lettore ha davanti — «i segmenti che portano l'avvertimento in graduatoria» e non «i sette segmenti» — perché quella marcatura viene da `segment_display`, cioè da una colonna del modello, e si aggiorna con essa.

La lista chiusa contiene le sole quantità che **non sono misure e non lo saranno**: gli anni di copertura dei due cataloghi, che il principio IV nomina per estensione fra ciò che va dichiarato, e che non esistono come misura perché il modello non ha dimensione di calendario (`data_model.md` §16). Ogni voce della lista sta nel contratto con la propria fonte, e ogni voce che qualcuno volesse aggiungere è una modifica del contratto, non una scelta di chi costruisce.

**La ragione**: (a) è il regime che questo progetto ha già scartato tre volte, e la ragione è che «coincide oggi» non è una proprietà, è un'osservazione. Un numero digitato non ha alcun legame con l'artefatto che lo produce: sopravvive a un ricalcolo, a una correzione, a una nota in loco, e resta a schermo a dire una cosa che non è più vera. (b) è più severa del necessario e comprerebbe la severità al prezzo di un limite dichiarato peggio: «i dati sono fermi a qualche anno fa» dice meno di «il catalogo video è fermo al 2021» e non è più onesto, è solo più vago.

**Un obbligo che la lista si porta dietro.** I due anni **non hanno lo stesso statuto**, e `data_model.md` §18 lo dichiara per esteso: quello del lato video è un fatto osservato e ancorato, quello del lato musicale è un'affermazione presa dalla documentazione della fonte, che il profilo dei dati dichiara di non poter verificare. Il testo che li porta a schermo deve distinguerli, o pubblica come misurata una cosa che nessuno ha misurato — che è la sola categoria di errore contro cui, per `convenzioni-marcatura.md` §8, non esiste presidio automatico.

---

### N3 — Il testo è sempre visibile: nessuna pagina-tooltip, nessun segnalibro, nessun pannello a scomparsa

**Il contesto**: gli strumenti offrono tre modi comodi di aggiungere testo senza occupare spazio — la pagina-tooltip che compare al passaggio del mouse, il segnalibro che scopre un pannello, il pulsante che apre una scheda di aiuto. Tutti e tre mettono il testo **dietro un'azione dell'utente**.

**Le opzioni**: (a) tutti e tre ammessi, perché il testo esiste comunque; (b) nessuno dei tre; (c) ammesso il solo tooltip statico d'intestazione, per il testo che *aggiunge* a un limite già visibile, mai per il limite stesso.

**La decisione**: **(c)**, con due divieti espliciti che ne discendono.

**Nessuna pagina-tooltip.** Una pagina-tooltip di Power BI è una **pagina**: sarebbe una quinta pagina in un report che il contratto della `008a` chiude a quattro, e — cosa più grave — è una pagina che ospita visuali, quindi può calcolare a una grana qualunque. È già vietata dalla `008a` §3.1 in termini di misure; qui il divieto si estende alla narrazione, che non ha ragione di abitarla.

**Nessun segnalibro e nessun pannello che nasconda un limite.** Il principio IV impone che il limite sia dichiarato, e un limite raggiungibile con un clic è un limite che si legge solo se qualcuno sospetta che esista. È lo stesso argomento con cui la `008a` §5.4 vieta di rendere nascondibile la colonna della quota di zeri: *«separarle in due colonne distanti, o renderne una nascondibile dall'utente, ricrea il difetto che la separazione esisteva per impedire.»*

**Il tooltip statico d'intestazione resta ammesso** per una funzione sola: chiarire un termine tecnico già a schermo — che cosa sia un segmento, che cosa misuri l'indice di domanda — dove la fascia porta già il limite e il tooltip porta la definizione. Non è dove un limite può abitare.

**La ragione**: (a) è comoda e produce una dashboard che *sembra* pulita perché ha spostato altrove ciò che disturba, e in una feature il cui deliverable è precisamente ciò che disturba sarebbe un'autocontraddizione. (b) sarebbe difendibile, ma toglierebbe l'unico posto in cui una definizione può stare senza rubare spazio a un limite.

---

### N4 — Il testo abita gli spazi che la `008a` ha riservato, e uno spazio insufficiente è uno scostamento

**Il contesto**: la `008a` §8 ha riservato quattro fasce — una per pagina, più una striscia a piè di pagina sull'ingresso — e ha dichiarato perché: *«una pagina disegnata senza questo spazio costringerebbe la feature successiva a ridisegnare le pagine per farvi entrare il proprio testo, e ridisegnare significa rimettere in discussione scelte già approvate e già verificate a schermo.»*

**La decisione**: la narrazione abita **quegli** spazi. Nessun blocco di testo si sovrappone a una visuale, ne riduce l'area, o sposta un elemento esistente.

**Se una fascia non basta**, la reazione non è allargarla a spese di una visuale: è **tagliare il testo** fino a farlo entrare, e dichiarare nell'esito che cosa è stato tagliato e perché. Se anche il testo tagliato al minimo non entra, allora è uno **scostamento** dal disegno della `008a` e si dichiara come tale, con la propria ragione — non si assorbe modificando una pagina già verificata.

**La ragione**: il perimetro di questa feature dice che le pagine sono chiuse. «Chiuse» ha valore solo se esiste una reazione dichiarata al caso in cui la chiusura è scomoda, altrimenti è una dichiarazione che cede alla prima difficoltà pratica. L'ordine — prima taglia il testo, poi dichiara — mette il costo dove sta la libertà di questa feature, che è la prosa, e non dove sta la garanzia di quella precedente, che è la struttura.

---

### N5 — Il *perché* della confidenza sta dove il KPI vive, e la scala si spiega una volta sola

**Il contesto**: il contratto di dashboard della `008a`, punto 2, assegna a questa feature un obbligo preciso: *«Le etichette di fonte e confidenza ci sono; il* perché *di quella confidenza no.»* `kpi_operators.md` §12 lo ripete. Il rischio, se la spiegazione si ripete per ogni KPI, è che occupi tutto lo spazio che i limiti dovrebbero occupare.

**Le opzioni**: (a) una riga di spiegazione accanto a ciascuna delle otto etichette; (b) una spiegazione della scala a tre livelli sulla pagina di ingresso, e nient'altro; (c) la scala spiegata una volta sull'ingresso, più una riga per KPI nella fascia della pagina che lo ospita.

**La decisione**: **(c)**.

Sull'ingresso va la scala: che cosa distingue *alta*, *media* e *bassa*, che è il numero di strati interpretativi fra il dato osservato e il numero mostrato (`business_case.md` §6). Sull'ingresso va anche la frase che quella scala **non** dice, ed è la più importante delle due: *anche un KPI a confidenza alta è alta rispetto al catalogo di riferimento, non rispetto a StreamWave.* La scala misura la solidità del calcolo, non la trasferibilità, e le due assunzioni di trasferimento — i proxy e il benchmark esterno — restano fuori dalla scala per costruzione.

Nelle fasce delle pagine di domanda va, per ciascun KPI ospitato, la ragione del proprio livello: che cosa si interpone fra il dato e il numero.

**Una asimmetria da dichiarare invece di lasciarla scoprire**: `BQ1-K1` compare su due pagine (`CP-3` della `008a`), ma la ragione della sua confidenza compare **una volta sola**, sulla pagina `BQ1`. Sull'ingresso la North Star porta le etichette e la scala che le spiega in generale; il suo *perché* specifico sta accanto a `C1`, dove `kpi_measures.md` §2.3 distingue la quota dalla condizione e dove quella distinzione serve a leggerlo.

---

### N6 — `C1` e `C3` si nominano da sole, e la dashboard non pubblica alcun verdetto

**Il contesto**: `C2` non esiste come valore ancorato in alcun artefatto — è parte dell'issue `#17` — e la `008a` `F6` ha deciso di portare a schermo `C1` e `C3` accanto ai rispettivi KPI senza alcun verdetto congiunto. Il contratto di dashboard è esplicito: *«La `008b` non può scrivere "due condizioni su tre" né "tre su tre" finché `C2` non è pubblicata: sarebbe un'affermazione derivata senza ancora, che la regola di `convenzioni-marcatura.md` §7 vieta.»*

**Il problema che la narrazione eredita**, e che la `008a` non aveva: un indicatore che dice `C1: sì` accanto alla North Star **invita** il lettore a concludere che l'argomento sia sostenuto. La `008a` poteva permettersi di tacere perché non aveva prosa; una feature che scrive prosa e tace su questo lascia in piedi l'inferenza senza contraddirla.

**Le opzioni**: (a) tacere, come la `008a`; (b) dichiarare che le condizioni sono tre e che una non è misurata; (c) dichiarare, accanto a ciascuna condizione, che **da sola non decide** e che questa dashboard non pubblica alcun esito complessivo.

**La decisione**: **(c)**. Il testo nomina `C1` sulla pagina `BQ1` e `C3` sulla pagina `BQ2`, ciascuna **singolarmente**, dice che ciascuna è una condizione della regola di decisione dichiarata nel business case, e dice che questa dashboard non compone le condizioni in un esito. Non conta quante siano, non nomina `C2`, non usa ordinali né frazioni.

**La ragione**: (b) è vietata alla lettera dal contratto e dalla regola — «tre» in posizione di fatto sarebbe un numerale non ancorato, e «una non è misurata» un'affermazione derivata dal conteggio. (a) è insufficiente per la ragione detta sopra: contro un'inferenza che la geometria della pagina suggerisce, il silenzio non è neutrale. (c) è l'unica formulazione che nega l'inferenza **senza costruire l'affermazione che la nega**: dire che una condizione da sola non decide non richiede di sapere quante siano.

**Che cosa questa decisione non chiude**: l'issue `#17` resta aperta. Questa feature non pubblica `C2` e non ne discute il valore; dichiara che l'esito congiunto non è a schermo, il che è vero indipendentemente da quante condizioni esistano.

---

### N7 — La narrazione descrive e avverte; non conclude, non raccomanda

**Il contesto**: la tentazione naturale di una fascia di testo sotto una dashboard è la sintesi — *«il segmento X è il candidato migliore»*, *«l'espansione è coerente»*. È anche la forma in cui `C1` e `C3` tornerebbero a comporsi per la porta di servizio, e in cui una graduatoria di insiemi che si sovrappongono diventerebbe una raccomandazione.

**La decisione**: nessun blocco di narrazione formula una raccomandazione, un verdetto, o una previsione. I registri ammessi sono tre: **che cosa il valore misura**, **che cosa il valore non permette di concludere**, **quale assunzione lo regge**.

Ne discendono tre divieti lessicali espliciti, ciascuno con un precedente nel repository:

- **nessun lessico causale** su una relazione fra attributi di catalogo (constitution, principio IV; `business_case.md` §8: *«la somiglianza di mood non descrive il comportamento delle persone»*);
- **nessun superlativo né ordinale** riferito a un fatto misurato, se non ancorato a un valore che il lettore vede — è `convenzioni-marcatura.md` §7 corollario (a), e vale a schermo esattamente come su una pagina;
- **nessuna affermazione sul pubblico**: il modello non contiene alcuna entità che rappresenti una persona (`data_model.md` §18), e la parola «domanda» a schermo nomina un indice della fonte, non un comportamento osservato.

**La ragione**: la constitution fissa un criterio di accettazione solo, *reggere la presentazione a un board reale*, e ciò che regge davanti a un board non è la sintesi — è la distinzione fra ciò che è stato misurato e ciò che è stato assunto. `business_case.md` §8 dichiara che la decisione è di chi legge; una dashboard che concludesse al posto suo contraddirebbe il documento che la genera.

---

### N8 — Il criterio di pubblicabilità si fissa prima di costruire, e dichiara anche ciò che non significa

**Il contesto**: questa feature deve chiudersi con un'affermazione che il progetto non ha mai fatto — *il file è pubblicabile*. Un'affermazione formulata dopo aver guardato il risultato è una ratifica; formulata prima, è un criterio.

**La decisione**: il file è pubblicabile quando, e solo quando, tutte e cinque le condizioni seguenti sono verificate a schermo e dichiarate nell'esito:

1. le tre assenze nominate dal contratto di dashboard della `008a`, punto 1, sono colmate: i limiti dichiarati, l'assunzione strutturale dei proxy, la narrazione — ciascuna verificabile su una pagina nominata;
2. il *perché* di ogni livello di confidenza è a schermo, per tutti e otto i KPI (punto 2 dello stesso contratto);
3. i limiti che `kpi_operators.md` §12 e `data_model.md` §18 assegnano esplicitamente a questa feature sono a schermo, in forma leggibile da un non tecnico;
4. nessun blocco di narrazione viola `N2`, `N6` o `N7`;
5. le tre impostazioni dell'issue `#20` sono state riverificate all'apertura del file e il loro esito è dichiarato.

**Che cosa «pubblicabile» non significa**, dichiarato con la stessa precisione, perché è la metà su cui un lettore esterno si può ingannare:

- **non** significa pubblicato: il `.pbix` resta un file locale non versionato, e nessuna pubblicazione sul servizio è nel perimetro di alcuna feature di questo progetto;
- **non** significa che le issue aperte siano chiuse. `#11`, `#17`, `#18`, `#20`, `#21` restano aperte, e `#20` in particolare dichiara che tre impostazioni possono riperdersi a ogni riapertura;
- **non** significa che il debito della `004` sulla verificabilità del benchmark sia risolto. Non lo è, e la pagina `BQ3` lo dice invece di nasconderlo — che è precisamente ciò che rende il file pubblicabile invece di impedirlo;
- **non** significa che i numeri descrivano StreamWave. Non lo fanno, e la pagina di ingresso lo dice per prima.

**La ragione**: senza il secondo elenco, «pubblicabile» diventa una parola che promette più di ciò che la feature consegna, e la promessa in eccesso è il difetto che questo progetto ha speso otto feature a evitare. Fissarlo prima di costruire è ciò che rende l'affermazione finale una verifica invece che un'opinione.

---

## Rapporto con le feature vicine

**Riceve dalla `008a`** un `.pbix` a quattro pagine, otto KPI a schermo con le proprie etichette, quattordici misure, otto tabelle, e quattro fasce vuote esplicitamente riservate. Riceve anche l'elenco di ciò che quella feature **non** garantisce, che è la lista dei requisiti di questa.

**Non anticipa nulla della `010`.** Il case study leggerà il repository da fuori e raccoglierà l'arretrato del tracker; questa feature non lo svuota e non lo giudica. Ciò che le lascia è un `.pbix` mostrabile e due documenti — contratto ed esito — che dicono a chi non può aprirlo che cosa contiene.

**Non tocca la `009`.** Tableau resta fuori.

---

## Perimetro

**Che cosa questa feature non fa**, e a chi spetta:

| Fuori dal perimetro | A chi spetta |
|---|---|
| qualunque modifica a una misura, a una relazione, a una colonna del modello | a nessuno in questa feature; una modifica necessaria è un **ritrovamento** da dichiarare |
| aggiungere, togliere o fondere una pagina | il numero di pagine è chiuso dalla `008a` |
| aggiungere una visuale legata a un campo, un filtro, uno slicer, un segnalibro o un'interazione incrociata | vietato da `N3` e dal perimetro; questa feature aggiunge caselle di testo, forme e formattazione |
| chiudere l'issue `#18` (`ALL` mancante su `mood_profile_overlap`) | a chi vorrà esporre `BQ1-K3` in un contesto filtrabile per categoria |
| chiudere l'issue `#11` (tipizzazione delle colonne di mood) | a nessuno: è assorbita da `#20`, che è strutturale e non chiudibile finché il `.pbix` non è versionato |
| riattivare l'interazione fra dispersione e graduatoria (issue `#21`) | a chi risolverà il vincolo dello strumento; qui si **dichiara** a schermo che le due visuali non si filtrano, il che non la riapre |
| risolvere il debito della `004` sulla verificabilità del benchmark | alla regia: è una decisione di governance. Qui si dichiara a schermo che è aperto |
| comporre `C1` e `C3` in un verdetto | a nessuno finché `C2` non è pubblicata (`N6`, issue `#17`) |
| modificare `docs/roadmap.md` | alla regia |
| scrivere in `data/raw/` o `data/processed/` | a nessuno: sola lettura (principio II) |
| pubblicare il `.pbix` nel repository | a nessuno (`FR-029` della `008a`, invariato) |

**Una precisazione sul confine fra rifinitura e riapertura.** Una rifinitura è una modifica che non cambia che cosa una visuale calcola né quali dati mostra: un titolo, un allineamento, un colore, un'etichetta di asse, un formato di numero **già dichiarato** dal contratto della `008a` §1.2. Tutto ciò che tocca un campo, un filtro o una formula è una riapertura, e una riapertura è un ritrovamento da dichiarare — non una libertà di chi costruisce.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Un lettore esterno apre il file e sa, prima di leggere un numero, che i dati non sono di StreamWave (Priority: P1)

Chi apre la dashboard senza aver letto alcun documento del repository incontra sulla prima pagina, insieme alla North Star, l'assunzione che regge tutto il resto: i due cataloghi sono pubblici e usati come riferimento, StreamWave non esiste, e nessun numero delle pagine seguenti descrive letteralmente StreamWave.

**Why this priority**: è l'obbligo che la constitution formula più duramente di ogni altro — l'uso dei proxy *«DEVE essere dichiarato in ogni artefatto rivolto all'utente finale, non solo nella documentazione tecnica»*. Finché manca, il file non è mostrabile a nessuno, e ogni altro miglioramento è ininfluente.

**Independent Test**: si apre la pagina di ingresso e si legge; se l'assunzione dei proxy non è lì, la storia fallisce indipendentemente da tutto il resto.

**Acceptance Scenarios**:

1. **Given** il file aperto sulla pagina di ingresso, **When** il lettore legge la fascia sotto la North Star, **Then** trova dichiarato che i cataloghi sono di riferimento e non di StreamWave, e che nessun valore della dashboard descrive StreamWave.
2. **Given** la stessa pagina, **When** il lettore cerca che cosa la dashboard non risponde, **Then** lo trova dichiarato: la decisione di entrare o no, il lato costi, il comportamento degli utenti.
3. **Given** la stessa pagina, **When** il lettore incontra un'etichetta di confidenza su una pagina successiva, **Then** ha già letto che cosa distingue i tre livelli e che nessuno di essi si riferisce a StreamWave.

---

### User Story 2 — Chi legge un KPI incontra il suo limite accanto al valore, non in un documento tecnico (Priority: P1)

Ciascuno degli otto KPI porta, nella fascia della propria pagina, la ragione della propria confidenza e il limite che il valore si porta dietro, scritti per chi non ha letto `kpi_measures.md`: la sovrapposizione di mood è una stima per eccesso; l'affinità confronta i segmenti fra loro e non ha una grandezza assoluta interpretabile; il confronto di durata mette i soli film contro l'intero catalogo musicale; i segmenti marcati in graduatoria non hanno domanda bassa, hanno domanda non misurata dalla fonte.

**Why this priority**: è il principio IV nella sua metà «nella dashboard», che nessuna feature del progetto ha ancora onorato, ed è l'obbligo che `kpi_operators.md` §12 e `kpi_measures.md` §10 assegnano esplicitamente per nome a questa feature.

**Independent Test**: si percorrono le tre pagine di domanda e si verifica, KPI per KPI, che il limite che il documento canonico dichiara sia leggibile a schermo senza gergo.

**Acceptance Scenarios**:

1. **Given** la pagina `BQ1`, **When** il lettore legge accanto alla sovrapposizione di mood, **Then** trova che il valore è una stima per eccesso e che gli intervalli di mood sono ampi per costruzione del criterio.
2. **Given** la pagina `BQ1`, **When** il lettore legge accanto al divario di durata, **Then** trova che il confronto è asimmetrico e che leggerlo come «catalogo video contro catalogo musicale» è sbagliato.
3. **Given** la pagina `BQ2`, **When** il lettore osserva i segmenti marcati in coda alla graduatoria, **Then** trova scritto che la loro posizione misura la copertura della fonte e non una priorità bassa, e che vanno esclusi da qualunque lettura della coda.
4. **Given** la pagina `BQ2`, **When** il lettore guarda la graduatoria come un elenco di alternative, **Then** trova scritto che i segmenti si sovrappongono, che le quantità non si sommano e che contare le righe di un segmento non lo dimensiona.
5. **Given** la pagina `BQ3`, **When** il lettore vede tre scenari affiancati, **Then** trova che l'intervallo non è un intervallo di confidenza, che l'uplift è un livello mensile e non un cumulato, e che questa dashboard non fornisce il moltiplicatore per una base utenti.

---

### User Story 3 — Nessun testo a schermo afferma più di quanto un artefatto sostenga (Priority: P1)

Ogni blocco di narrazione è riconducibile a una fonte nominata nel contratto; nessuno contiene un numero fuori dalla lista chiusa; nessuno compone `C1` e `C3`; nessuno raccomanda, conclude o attribuisce una causa.

**Why this priority**: è il presidio che rende la narrazione un artefatto del progetto invece di un commento. Senza di esso questa feature aggiungerebbe alla dashboard l'unico strato che nessun controllo verifica e nessuna ancora vincola.

**Independent Test**: si legge il contratto accanto allo schermo e si verifica riga per riga; è la prova che la revisione in contesto pulito esercita sul contratto e che l'esito esercita sul costruito.

**Acceptance Scenarios**:

1. **Given** il contratto approvato, **When** si confronta ogni blocco a schermo con la propria voce, **Then** il testo coincide alla lettera, o la differenza è dichiarata nell'esito come scostamento.
2. **Given** un blocco qualunque, **When** vi si cerca una cifra, **Then** o non ce n'è, o è una voce della lista chiusa di `N2`.
3. **Given** le pagine `BQ1` e `BQ2`, **When** vi si cerca un conteggio delle condizioni della regola di decisione, **Then** non ce n'è, e ciascuna condizione è nominata da sola.

---

### User Story 4 — Chi riapre il file trova le tre impostazioni fragili verificate prima di ogni altra cosa (Priority: P1)

L'apertura del `.pbix` comincia dalla verifica delle tre impostazioni dell'issue `#20` — la tipizzazione delle tre colonne di mood, la lettura dei CSV sull'origine di `dim_title`, la colonna di scenario di `bq3_scenarios` — e l'esito è dichiarato prima che qualunque testo venga scritto.

**Why this priority**: è il rischio che si è già manifestato tre volte, ciascuna in una feature diversa, e l'unica volta in cui è stato trovato tardi (`E9` della `007b`) tre KPI su otto erano sbagliati di due ordini di grandezza sotto un esito verde di ogni controllo. La verifica costa una lettura; non farla costa di scrivere una narrazione corretta accanto a numeri sbagliati.

**Independent Test**: l'esito riporta le tre voci con il proprio stato; se una risulta persa, la correzione precede la narrazione e si dichiara.

**Acceptance Scenarios**:

1. **Given** il file appena riaperto, **When** si ispezionano le tre colonne di mood, **Then** i valori stanno nel dominio `0-1`, oppure la costruzione si ferma e il difetto si corregge prima di procedere.
2. **Given** il file appena riaperto, **When** si legge il conteggio di riga di `dim_title` e la presenza della colonna di scenario, **Then** coincidono con quanto la `008a` ha lasciato, oppure la divergenza è dichiarata e corretta prima della narrazione.
3. **Given** una delle tre verifiche fallita e corretta, **When** la correzione tocca un valore a schermo, **Then** gli otto valori vengono riconfrontati con `docs/kpi_measures.md` e l'esito è dichiarato.

---

### User Story 5 — Chi legge il repository sa che cosa c'è scritto sulla dashboard senza poterla aprire (Priority: P2)

Il contratto di narrazione porta il testo letterale di ogni blocco; l'esito dichiara che cosa è stato costruito e in che cosa differisce. Chi non ha il `.pbix` — che è chiunque cloni il repository — legge i due documenti in sequenza e sa che cosa il lettore della dashboard incontra.

**Why this priority**: è la stessa ragione per cui la `008a` ha trascritto il testo delle due colonne calcolate nel proprio esito. Il file non è versionato; ciò che non è scritto nel repository non esiste per chi legge da fuori.

**Independent Test**: si legge il contratto senza aprire il file e si verifica che ogni blocco abbia posizione, testo, obbligo e fonte.

**Acceptance Scenarios**:

1. **Given** una copia pulita del repository, **When** si apre il contratto di narrazione, **Then** ogni blocco dichiara pagina, spazio, testo letterale, obbligo che lo richiede e fonte documentale.
2. **Given** gli stessi documenti, **When** si cerca che cosa è cambiato rispetto al disegno, **Then** l'esito lo elenca con la propria ragione.

---

### Edge Cases

- **Una fascia non basta per il testo previsto.** Si taglia il testo, non lo spazio (`N4`); ciò che si taglia si dichiara. Se nemmeno il minimo entra, è uno scostamento dal disegno della `008a`.
- **Una verifica dell'issue `#20` fallisce.** La narrazione si ferma; la correzione precede; se un valore a schermo cambia, gli otto valori si riconfrontano e l'esito lo dichiara.
- **Un limite da portare a schermo richiederebbe un numero non pubblicato.** Non si scrive. O si riformula per rimandare a ciò che il lettore vede, o resta fuori dallo schermo e l'esito dichiara che resta fuori e perché.
- **Il testo di una fascia risulta esatto ma illeggibile a un non tecnico.** È il caso che nessun controllo può segnalare: si chiude in revisione in contesto pulito, che è l'unico presidio contro una dichiarazione formalmente vera e materialmente inutile.
- **Una rifinitura sembra richiedere di toccare un campo o un filtro.** Non si esegue: è una riapertura, si dichiara come ritrovamento e si rinvia.
- **Il testo di un blocco contraddice un documento pubblicato.** È un ritrovamento: si dichiara con nota in loco sul documento che lo riguarda, senza riscrivere il testo originale, e il blocco si riformula.

---

## Requirements *(mandatory)*

### Il contratto di narrazione (`N1`)

- **FR-001**: Il contratto di narrazione DEVE essere scritto e committato **prima** che Power BI Desktop venga riaperto.
- **FR-002**: Ogni blocco DEVE dichiarare quattro cose: pagina e spazio riservato di destinazione, **testo letterale**, obbligo che lo richiede, fonte documentale da cui l'affermazione discende.
- **FR-003**: Dove esiste una formulazione vicina e sbagliata, il blocco DEVE dichiararla come esclusa. Almeno tre sono obbligatorie e nominate: «catalogo video contro catalogo musicale» per `BQ1-K2` (`data_model.md` §18); «domanda bassa» per i segmenti marcati (`kpi_measures.md` §5.3); «l'uplift non è scalabile» per `BQ3-K2` (`bq3_scenarios.md` §8, che dichiara falsa quella formulazione più comoda).
- **FR-004**: Il contratto NON DEVE prescrivere la sequenza di operazioni nella GUI, il carattere, la dimensione o il colore: sono di chi costruisce (principio V).
- **FR-005**: Il contratto DEVE essere approvato da Valerio prima della costruzione; l'approvazione è tracciabile nella history git.

### Che cosa va a schermo

- **FR-006**: L'assunzione strutturale dei proxy DEVE comparire sulla pagina di ingresso, in forma leggibile da chi non ha letto alcun documento (constitution, Vincoli di Dominio e di Dato).
- **FR-007**: La pagina di ingresso DEVE dichiarare che cosa la dashboard non risponde, coprendo almeno: la decisione di entrare o no nel mercato, l'assenza del lato costi, l'assenza di dati comportamentali, la copertura temporale dei due cataloghi.
- **FR-008**: La pagina di ingresso DEVE spiegare la scala di confidenza a tre livelli e dichiarare che essa non misura la trasferibilità a StreamWave (`business_case.md` §6).
- **FR-009**: Ciascuno degli otto KPI DEVE avere a schermo la ragione del proprio livello di confidenza, nella fascia della pagina che lo ospita. Per `BQ1-K1`, che compare su due pagine, la ragione compare una volta sola, sulla pagina `BQ1` (`N5`).
- **FR-010**: I tre limiti che `kpi_operators.md` §12 assegna esplicitamente a questa feature DEVONO essere a schermo: la stima per eccesso di `BQ1-K3` (§4), la non interpretabilità della grandezza assoluta di `BQ2-K2` (§6), la ragione per cui punteggio e quadrante di `BQ2-K3` non si fondono (§7.2).
- **FR-011**: I limiti della categoria «sconsigliato» di `data_model.md` §18 DEVONO essere a schermo, perché sono gli unici contro cui nulla nel modello segnala: l'asimmetria di `BQ1-K2` con la lettura sbagliata che rende possibile; il divieto di sommare una quantità su più segmenti; il divieto di contare le righe di un segmento per dimensionarlo; l'assenza di qualunque entità che rappresenti una persona.
- **FR-012**: La pagina `BQ2` DEVE dichiarare che i segmenti marcati portano domanda **non misurata dalla fonte** e non domanda bassa, e che vanno esclusi da qualunque lettura della coda della graduatoria (`kpi_measures.md` §5.3 e §7.4).
- **FR-013**: La pagina `BQ3` DEVE dichiarare: che l'intervallo non è un intervallo di confidenza; che l'uplift è un livello mensile a fine orizzonte e non un cumulato né un dato annuo; che il tasso è lordo di disdette; che nessuna base utenti è quantificata in questo progetto e che la dashboard non ne fornisce il moltiplicatore; le assunzioni `A4`, `A5` e `A6` in forma leggibile.
- **FR-014**: La pagina `BQ3` DEVE dichiarare che il debito sulla verificabilità del benchmark è **aperto**, con la ragione: il valore centrale poggia su un comunicato di un terzo che non nomina lo studio, congelato nel repository, e la verifica esterna dipende da un indirizzo che potrebbe smettere di rispondere (`bq3_scenarios.md` §9).
- **FR-015**: La pagina `BQ2` DEVE dichiarare che dispersione e graduatoria non si filtrano a vicenda e che la graduatoria mostra sempre tutti i segmenti. È una dichiarazione dello stato costruito, non una riapertura dell'issue `#21`.

### I divieti sul testo

- **FR-016**: Nessun blocco di narrazione DEVE contenere una cifra, salvo le voci della lista chiusa dichiarata nel contratto (`N2`); ogni voce della lista nomina la propria fonte e la ragione per cui non proviene da una misura.
- **FR-017**: Dove la narrazione nomina una quantità, DEVE rimandare alla marcatura che il lettore ha davanti, non ripetere il conteggio.
- **FR-018**: I due anni di copertura, se portati a schermo, DEVONO essere distinti per statuto: osservato sul lato video, dichiarato dalla fonte e non verificabile sul lato musicale (`data_model.md` §18).
- **FR-019**: Nessun blocco DEVE comporre `C1` e `C3`, contarle, nominare `C2`, o pubblicare un esito complessivo della regola di decisione (`N6`).
- **FR-020**: Nessun blocco DEVE formulare una raccomandazione, un verdetto o una previsione; nessun lessico causale su una relazione fra attributi di catalogo; nessun superlativo o ordinale riferito a un fatto misurato non visibile a schermo; nessuna affermazione sul comportamento delle persone (`N7`).
- **FR-021**: Ogni sigla che il testo di questa feature usa DEVE essere sciolta sulla stessa pagina in cui compare. L'obbligo copre il testo nuovo; non chiude le issue `#16` e `#24`, che riguardano la leggibilità dei documenti e non dello schermo.

### La forma e il perimetro della costruzione

- **FR-022**: Il testo DEVE stare negli spazi riservati dalla `008a` §8; nessun blocco si sovrappone a una visuale, ne riduce l'area o sposta un elemento esistente.
- **FR-023**: Nessuna pagina-tooltip, nessun segnalibro, nessun pannello a scomparsa (`N3`). Nessun limite dichiarato DEVE essere raggiungibile solo con un'azione dell'utente.
- **FR-024**: Questa feature NON DEVE aggiungere alcuna visuale legata a un campo, alcun filtro, alcuno slicer, alcuna interazione incrociata; NON DEVE modificare alcuna misura, relazione o colonna del modello, né il numero di pagine.
- **FR-025**: Dove una rifinitura tocchi una visuale sui segmenti, il campo usato DEVE restare `segment_display` e mai `segment`, o l'avvertimento sparisce dal nome (contratto di dashboard `008a`, punto 11).
- **FR-026**: Nessuna pagina che espone `BQ1-K3` DEVE acquisire un filtro di categoria video, in alcuna rifinitura: l'issue `#18` resta aperta e il difetto si manifesterebbe.

### La verifica del file e il riporto

- **FR-027**: All'apertura del `.pbix`, e **prima di qualunque altra operazione**, DEVONO essere verificate le tre impostazioni dell'issue `#20`: dominio `0-1` sulle tre colonne di mood di `dim_track`, conteggio di riga atteso su `dim_title`, presenza della colonna di scenario su `bq3_scenarios`. L'esito di ciascuna è dichiarato.
- **FR-028**: Se una delle tre verifiche fallisce, la correzione DEVE precedere la narrazione, e se tocca un valore a schermo gli otto valori DEVONO essere riconfrontati con `docs/kpi_measures.md`.
- **FR-029**: Ogni scostamento fra contratto approvato e costruito DEVE essere elencato con la propria ragione. Un adattamento non dichiarato è un difetto della feature, non una libertà di chi costruisce.
- **FR-030**: Ogni ritrovamento DEVE essere dichiarato con nota in loco sull'artefatto che lo riguarda, senza riscrivere il testo o il valore originale.
- **FR-031**: Le issue `#11`, `#17`, `#18`, `#20`, `#21` DEVONO restare in uno stato dichiarato nell'esito; nessuna viene chiusa da questa feature.
- **FR-032**: L'esito DEVE contenere la dichiarazione esplicita di pubblicabilità, verificata contro le cinque condizioni di `N8` e accompagnata dall'elenco di ciò che «pubblicabile» non significa.

### Obblighi che nessun automatismo esegue

- **FR-033**: Il README DEVE essere allineato: riga di stato della `008b` con link al verbale, deliverable elencato, prosa dei deliverable estesa, `Setup` e `Struttura` allineati dove qualcosa cambia. In particolare, la frase *«Il file è leggibile, non pubblicabile»* DEVE essere aggiornata, o resterebbe su `main` un'affermazione falsa.
- **FR-034**: La revisione in contesto pulito DEVE produrre `specs/008b-dashboard-narrative-polish/review.md`, con i quattro obblighi di `CLAUDE.md`; l'oggetto della revisione è il contratto di narrazione e la documentazione dell'esito, non il `.pbix`.
- **FR-035**: `python3 scripts/check_audit_coherence.py` DEVE restare verde. Questa feature non aggiunge documenti a `DOCUMENTS` e non modifica alcun artefatto versionato, salvo eventuali note in loco.
- **FR-036**: Il `.pbix` NON DEVE essere committato.

### Key Entities

- **Blocco di narrazione**: un'unità di testo a schermo, con una posizione, un testo letterale, un obbligo che lo richiede e una fonte. È l'entità che questa feature produce.
- **Spazio riservato**: una delle fasce dichiarate dalla `008a` §8; è il contenitore, e non si allarga.
- **Lista chiusa dei numerali**: l'elenco, dichiarato nel contratto, delle sole cifre ammesse in un blocco di narrazione.
- **Formulazione esclusa**: una frase vicina a quella corretta e sbagliata, dichiarata nel contratto perché chi costruisce non la scelga per comodità.
- **Scostamento**: differenza dichiarata fra contratto approvato e costruito; non tocca alcun valore.
- **Ritrovamento**: differenza fra ciò che un documento pubblicato afferma e ciò che si osserva; obbliga a una nota in loco.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: L'assunzione dei proxy è leggibile sulla pagina di ingresso senza aprire alcun documento del repository.
- **SC-002**: Tutti e otto i KPI hanno a schermo la ragione della propria confidenza; il conteggio si verifica percorrendo le pagine.
- **SC-003**: I tre limiti di `kpi_operators.md` §12 e i quattro limiti «sconsigliati» di `data_model.md` §18 sono a schermo, ciascuno su una pagina nominata nell'esito.
- **SC-004**: Nessun blocco di narrazione contiene una cifra fuori dalla lista chiusa; la verifica è una lettura del contratto contro lo schermo.
- **SC-005**: Nessuna pagina compone `C1` e `C3`, ne conta le condizioni o nomina `C2`.
- **SC-006**: Le pagine restano quattro, le misure quattordici, le tabelle otto, le relazioni cinque: la struttura della `008a` è invariata.
- **SC-007**: Le tre impostazioni dell'issue `#20` sono state verificate all'apertura del file, prima di ogni altra operazione, e il loro esito è dichiarato.
- **SC-008**: Il contratto di narrazione è stato approvato prima della riapertura di Power BI, e l'approvazione è tracciabile nella history git.
- **SC-009**: Ogni differenza fra contratto ed esito è elencata con la propria ragione.
- **SC-010**: `python3 scripts/check_audit_coherence.py` esce verde.
- **SC-011**: Il verbale di revisione esiste ed è stato committato prima che l'artefatto revisionato venisse modificato.
- **SC-012**: Il README dichiara lo stato della feature, il deliverable e il link al verbale, e non contiene più l'affermazione che il file non è pubblicabile.
- **SC-013**: L'esito dichiara il file pubblicabile contro le cinque condizioni di `N8`, e dichiara che cosa quella parola non significa.

---

## Stima e scomposizione

**Stima**: ~4 ore, revisione e chiusura dei rilievi incluse, come da `docs/roadmap.md`.

Distribuzione attesa: ~1,5 h per il contratto di narrazione, ~1 h per la costruzione manuale (fuori da questa sessione), ~1,5 h per riporto, revisione e chiusura.

**Se dopo il punto di fermata sul contratto il lavoro sembra più grande**, la sessione si ferma e lo riporta invece di comprimere. La parte comprimibile sarebbe la revisione, che sulla `008a` ha prodotto venticinque rilievi ed è la sola cosa che presidia un deliverable di cui nessuno script può leggere una riga.

---

## Assumptions

- Il `.pbix` esiste sulla macchina di Valerio nello stato in cui la `008a` lo ha lasciato: quattro pagine, otto KPI a schermo, quattordici misure, otto tabelle, cinque relazioni, quattro fasce vuote riservate.
- `data/processed/` è presente sulla macchina che riapre il file. Se il modello va ricaricato, `scripts/build_datasets.py` lo rigenera dai dati raw.
- Le fasce riservate dalla `008a` §8 sono sufficienti per il testo previsto. È un'assunzione di disegno e non un fatto verificato: la `008a` ha riservato lo spazio senza sapere quanto testo lo avrebbe occupato, e `N4` dichiara che cosa fare se non basta.
- Il lettore per cui la narrazione è scritta è un decisore non tecnico che non ha letto alcun documento del repository e non lo leggerà: è il criterio di accettazione della constitution — reggere la presentazione a un board reale.
- La costruzione avviene sullo stesso schermo su cui la `008a` è stata costruita, in rapporto 16:9: la leggibilità del testo si giudica lì.
- Nessuna licenza Power BI Pro è necessaria. «Pubblicabile» qui significa mostrabile a un lettore esterno, non pubblicato su un servizio (`N8`).

---

## Debito ereditato

Ogni voce riporta il rilievo, la issue o la divergenza puntuale, non un rimando generico.

| Voce | Da dove viene | Che cosa questa feature ne fa |
|---|---|---|
| le tre assenze che rendono il `.pbix` non pubblicabile — limiti a schermo, assunzione dei proxy, narrazione | contratto di dashboard `008a`, «Che cosa la `008a` non garantisce» punto 1; Complexity Tracking di `plan.md` della `008a` | **le chiude**: sono il deliverable di questa feature (`FR-006`-`FR-015`) |
| il *perché* di ogni confidenza, assente a schermo | contratto di dashboard `008a` punto 2; `kpi_operators.md` §12 | **lo chiude** (`N5`, `FR-008`, `FR-009`) |
| i limiti di `kpi_operators.md` §4, §6, §7.2, assegnati per nome a questa feature | `kpi_operators.md` §12, «devono essere ereditati e ripresentati in forma comprensibile da chi costruirà la narrazione» | **li chiude** (`FR-010`) |
| i limiti «sconsigliati» di `data_model.md` §18, gli unici che «richiedono un intervento, perché nulla lo segnala» | `data_model.md` §18; `data_model.md` §19, righe assegnate alla dashboard | **li chiude** (`FR-011`) |
| issue `#20` — tre impostazioni vivono solo dentro il `.pbix` non versionato | `008a`, esito della costruzione | **verifica e dichiara**, non chiude: è strutturale finché il file non è versionato (`FR-027`) |
| issue `#11` — la tipizzazione delle colonne di mood può ripresentarsi | `007b`, `E9`; assorbita da `#20` | verificata come parte di `#20`; resta aperta |
| issue `#18` — `mood_profile_overlap` senza `ALL` sul filtro di categoria | revisione `007b`, rilievo `R13` | resta aperta e **non aggirata di nuovo**: nessuna rifinitura introduce un filtro di categoria (`FR-026`) |
| issue `#17` — `C2` non è pubblicata come valore ancorato | revisione `007b`, rilievo `R12` | è la ragione di `N6`; resta aperta |
| issue `#21` — dispersione e graduatoria non si evidenziano a vicenda | `008a`, scostamento T028 | resta aperta; lo stato costruito si **dichiara a schermo** (`FR-015`), il che non la riapre |
| debito della `004` sulla verificabilità del benchmark | debito della `004`; roadmap: «va deciso prima che `008a` pubblichi quei numeri in una dashboard» | **non decidibile da questa feature**: è governance. Va a schermo dichiarato come aperto (`FR-014`) |
| issue `#22`-`#25` — i quattro raggruppamenti di rilievi della revisione della `008a` | revisione `008a` | fuori perimetro: riguardano i documenti della `008a`, non lo schermo. Restano al tracker e alla `010` |
| il `.pbix` non è versionato e non è rigenerabile da una copia pulita | contratto di dashboard `008a` punto 9; principio V | invariato: ciò che il repository contiene è il contratto e l'esito, non il file |

---

## I punti di fermata

Tre, come sulla `008a`, e per la stessa ragione.

1. **dopo `/speckit.specify`** — la spec torna in revisione alla regia prima di diventare un piano;
2. **dopo `/speckit.tasks`** — piano e task tornano insieme, e non si implementa senza che siano stati visti;
3. **il contratto di narrazione, dentro l'implementazione**, prima che Power BI Desktop venga riaperto (`N1`, `FR-001`, `FR-005`).

---

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: **BQ1, BQ2 e BQ3** — tutte e tre, come la `008a`, perché la dashboard le espone tutte.
- **Contributo**: non produce alcuna risposta nuova e non cambia alcuna risposta esistente. Rende leggibili le risposte già a schermo da parte di chi non ha letto i documenti tecnici che le producono — che è la condizione perché una risposta *sia* una risposta. Una misura corretta accanto a un lettore che non sa che cosa non le si può chiedere non ha ancora risposto a nulla: è il passaggio da *valore letto* a *valore compreso con il proprio limite*, ed è la metà del principio IV che nessuna feature del progetto aveva finora onorato.

---

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

**Questa feature non introduce alcuna metrica, non ricalcola alcun valore e non altera alcuna classificazione di confidenza.** La tabella riporta quella già fissata da `business_case.md` §5.4 e ripetuta invariata da `kpi_operators.md` §11, `kpi_measures.md` e il contratto di pagina della `008a` §1.1. Le due colonne che contano per questa feature sono le ultime due: la ragione della confidenza, che è ciò che va portato a schermo, e la formulazione da escludere, che è ciò che non deve andarci.

| Metrica | Fonte | Confidenza | Perché quel livello — la ragione che va a schermo | Formulazione esclusa |
|---|---|---|---|---|
| `music_adjacent_catalog_share` 🎯 | Netflix (reale) | alta | si conta quanto del catalogo di riferimento è già musicale, senza alcuna mappatura interposta | che la quota dica se la condizione `C1` è soddisfatta: sono due letture diverse dello stesso catalogo (`kpi_measures.md` §2.3) |
| `format_duration_gap` | Derivato (Netflix + Spotify) | alta | due durate osservate e una sottrazione, nessuna assunzione interposta | «differenza fra la durata del catalogo video e quella del catalogo musicale»: il lato video sono i soli film (`data_model.md` §18) |
| `mood_profile_overlap` | Derivato (Netflix + Spotify) | media | dipende dalla tabella dei profili di mood, che l'analista assegna e nessuna fonte osserva | che la sovrapposizione misurata sia quella reale: è una stima **per eccesso** (`kpi_measures.md` §4.3) |
| `segment_demand_index` | Spotify (reale) | media | è un indice di popolarità pubblicato dalla fonte, che non ne dichiara la costruzione, usato come proxy della domanda | «domanda bassa» per i segmenti marcati: è domanda **non misurata dalla fonte** (`kpi_measures.md` §5.3) |
| `segment_catalog_affinity` | Derivato (Netflix + Spotify) | media | confronta un profilo osservato con uno assegnato, e la scala è ancorata solo agli estremi | qualunque lettura della grandezza assoluta: confronta i segmenti fra loro, non in assoluto (`kpi_measures.md` §6.3) |
| `segment_entry_priority` | Derivato (`BQ2-K1` + `BQ2-K2`) | media | eredita il livello dei due valori che compone | che punteggio alto significhi «nel quadrante»: sono due valori distinti e non intercambiabili (`kpi_operators.md` §7.2) |
| `premium_tier_adoption_rate` | Sintetico | bassa | nessun dato di StreamWave lo sostiene; poggia su un benchmark osservato su un operatore terzo | che uno dei tre scenari sia il valore atteso; che l'ampiezza sia un intervallo di confidenza (`bq3_scenarios.md` §8) |
| `arpu_uplift` | Derivato (`BQ3-K1` + prezzi assunti) | bassa | come sopra, moltiplicato per un differenziale di prezzo assunto e non osservato | «non è scalabile»: è falsa. Nessuna base utenti è quantificata qui, e la dashboard non fornisce il moltiplicatore (`bq3_scenarios.md` §8) |

**Assunzioni dietro i dati sintetici**: nessun dato sintetico è generato da questa feature. Quelli di `BQ3` sono citati dall'artefatto della `004` senza ricalcolo, con le assunzioni dichiarate lì; il debito sulla verificabilità del benchmark resta aperto e va a schermo dichiarato come tale (`FR-014`).

**Le due assunzioni di trasferimento restano fuori dalla scala**, e la pagina di ingresso lo dichiara: i proxy si applicano identici a tutti e otto i KPI, il benchmark esterno ai soli valori di `BQ3`. Nessun livello di confidenza, nemmeno il più alto, autorizza a leggere un numero di questa dashboard come una misura di StreamWave (`business_case.md` §6).

---

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Non risponde a**: se StreamWave debba entrare nel mercato musicale. Questa feature rende i limiti leggibili; non aggiunge alcun elemento di giudizio, e nessuna pagina formula una raccomandazione (`N7`).
- **Non risponde a**: che cosa valga `C2`, né quale sia l'esito della regola di decisione della North Star. `C2` non è pubblicata come valore ancorato e la dashboard non compone alcun verdetto (`N6`, issue `#17`).
- **Inferenza da evitare**: che un limite scritto a schermo sia un limite risolto. Il testo dichiara; non corregge nulla. La sovrapposizione di `BQ1-K3` resta una stima per eccesso dopo che la pagina lo dice, e il benchmark di `BQ3` resta non verificabile in modo indipendente dopo che la pagina lo dichiara.
- **Inferenza da evitare**: che «pubblicabile» significhi verificato da un controllo. Nessuno script di questo repository legge il `.pbix`: la dichiarazione poggia sul contratto scritto prima, sull'esito scritto dopo e sulla revisione in contesto pulito su entrambi. È la forma più forte disponibile e non la più forte immaginabile — il principio V, non una lacuna di questa feature.
- **Inferenza da evitare**: che la narrazione sostituisca i documenti. Ogni blocco è una riduzione di un'affermazione più precisa che vive sotto `docs/`; chi deve citare, cita il documento, non la fascia.
- **Copertura del dato**: invariata — catalogo video fermo al 2021, catalogo musicale al 2022, nessun dato comportamentale, due cataloghi pubblici usati come riferimento. I due anni non hanno lo stesso statuto, e il testo che li porta a schermo lo distingue (`FR-018`).
- **Quali limiti restano comunque fuori dallo schermo, e perché**: la convenzione di arrotondamento per unità di misura (`kpi_measures.md` §1.2); il vincolo di versione sulla tabella dei mood (`content_taxonomy_bridge.md` §5); la scelta del prodotto cartesiano contro l'inviluppo convesso (`kpi_operators.md` §4); la ragione per cui la distanza media assoluta è compensativa (`kpi_operators.md` §6). Sono limiti **del metodo**, non del valore: chi li deve valutare apre il documento, e portarli a schermo occuperebbe lo spazio dei limiti che cambiano la lettura di un numero. È una selezione dichiarata, non una dimenticanza, e l'esito la ripete.
- **Dove è esposto all'utente finale**: su tutte e quattro le pagine, negli spazi che la `008a` ha riservato. È la prima feature del progetto in cui la risposta a questa riga non è «da nessuna parte».

---

## Come si verifica

Le prove eseguibili da chiunque abbia clonato il repository:

```bash
# le ancore dei documenti pubblicati restano verdi: questa feature non ne tocca alcuno
python3 scripts/check_audit_coherence.py
```

Le prove che richiedono il `.pbix` non sono eseguibili da uno script e non lo saranno mai — è il principio V. Sono elencate come prove manuali nel quickstart della feature, e il loro esito vive nel riporto, nella stessa forma di `E9` della `007b` e delle dodici prove della `008a`: un'osservazione umana è un dato purché sia dichiarata come tale.

**La prova che questa feature aggiunge, e che nessuna precedente aveva**: la lettura del contratto accanto allo schermo, blocco per blocco. È l'unica forma in cui una prosa a schermo si può verificare, e la ragione per cui `N1` impone che il testo esista alla lettera nel repository prima di esistere nel file.
