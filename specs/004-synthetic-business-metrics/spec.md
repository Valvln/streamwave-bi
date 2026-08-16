# Feature Specification: Synthetic Business Metrics

**Feature Branch**: `004-synthetic-business-metrics`

**Created**: 2026-08-16

**Status**: Draft

**Input**: User description: "Parametri e valori di scenario per BQ3 (Impatto stimato), ancorati a un benchmark pubblico di settore. La feature produce i parametri che alimentano `BQ3-K1` (`premium_tier_adoption_rate`) e `BQ3-K2` (`arpu_uplift`); non calcola i KPI, che sono della 007. Un solo benchmark: il tasso di conversione a un tier superiore in servizi di streaming, congelato in un file versionato con citazione puntuale, senza chiamate di rete a runtime, con assunzione di trasferimento dichiarata e senza promozione di confidenza. Fuori perimetro: churn (FR-018), engagement (nessun KPI lo consuma), determinazione dei prezzi (A4/FR-017a), quantificazione della base utenti (divergenza 9). Include il debito testuale su `docs/business_case.md`. Chiude R13 della revisione 001 per la parte BQ3."

*(Il prompt di consegna integrale è più esteso di questa sintesi. Ogni vincolo che conteneva compare qui sotto come decisione, requisito, criterio di successo o limite dichiarato: questa spec è il testo autorevole, non il prompt.)*

---

## La domanda a cui questa spec risponde per prima

Il prompt di consegna chiedeva di stabilire, prima di ogni altra cosa, **quanto resta davvero da generare** una volta tolti dal perimetro churn, engagement, prezzi e base utenti. La risposta determina la forma dell'intera feature, e va data qui e non in fase di piano.

**Resta un numero soltanto.**

Tutto ciò che la terza domanda di business produce si riduce a questo: un tasso di adozione del tier premium, dichiarato in tre scenari, e il suo prodotto per un differenziale di prezzo che A4 ha già fissato a 4,00 €. Sei valori pubblicati, di cui tre sono una moltiplicazione degli altri tre per una costante nota. A monte dei sei c'è un solo parametro libero — il tasso di adozione dello scenario centrale — più la regola, dichiarata dall'analista, che da quello ricava gli altri due.

Non è una generazione di dati. È la **derivazione di sei valori da un parametro e una costante**, ed è la ragione per cui questa spec prende la decisione D1 qui sotto.

Il nome della feature resta `Synthetic Business Metrics`, ed è **esatto**. I sei valori sono metriche di business sintetiche in senso proprio: non sono osservati su StreamWave, non lo saranno mai con i dati disponibili, e discendono da un benchmark trasferito da un operatore terzo e da una banda stipulata dall'analista. Sintetico è ciò che descrive la loro provenienza, e la descrive bene.

Ciò che non esiste è il **dataset**. Chi arriva qui aspettandosi righe generate — utenti simulati, mesi simulati, un file da cui i valori si ricavano per aggregazione — non le troverà, e la sezione «Perimetro» lo dichiara. La distinzione conta perché è l'unica cosa che il nome potrebbe far credere e che non è vera: non «sintetico», che è giusto, ma «dataset», che non c'è.

---

## Le decisioni che questa spec prende

Sono sei. Ciascuna è riportata con le opzioni sul tavolo, la decisione, la sua ragione e dove va dichiarata. I requisiti che le rendono verificabili stanno più sotto.

Questa sezione è il punto di massima leva della spec. Se la revisione deve contestare qualcosa, è qui — e in particolare D1 e D2.

---

### D1 — La derivazione è deterministica, e il seed va tolto

**Le opzioni**: (a) uno script con seed fisso che genera un dataset sintetico di utenti o di mesi, da cui i sei valori si ricavano per aggregazione; (b) una derivazione deterministica che calcola i sei valori direttamente dal parametro e dalla costante, senza alcuna estrazione casuale.

**La decisione**: **(b), derivazione deterministica.** Nessun generatore di numeri casuali, nessun seed, nessun dataset di righe sintetiche. Lo script legge un file di parametri e scrive un artefatto di sei valori.

**La ragione**, in tre passaggi, il terzo dei quali è dirimente:

1. **Nessuna misura consuma righe.** `BQ3-K1` è una quota entro un orizzonte di 12 mesi — un valore di arrivo, non una serie mensile — e `BQ3-K2` è il suo prodotto per una costante. Il framework KPI non contiene alcuna misura che legga un dettaglio per utente, per mese o per segmento: churn è vietato da FR-018 della 001, engagement non ha KPI, i prezzi sono fissati da A4. Un dataset di righe sarebbe letto da nessuno.
2. **Un'estrazione casuale non aggiungerebbe informazione.** Simulare l'adozione di N utenti con probabilità *p* e poi calcolarne la quota restituisce *p* più un errore di campionamento che è artefatto della simulazione, non incertezza del mondo. L'incertezza reale di BQ3 vive nel valore di *p*, ed è già rappresentata — per obbligo del principio I e di §6 del business case — dal range best/base/worst. Un secondo strato di rumore sopra il primo non lo misura: lo sporca.
3. **Non esiste alcun N da cui estrarre.** La divergenza 9 della revisione 001, chiusa il 2026-08-10, stabilisce che la base utenti **non viene quantificata** e che `BQ3-K2` resta euro per utente al mese, non scalabile. Una simulazione a livello di individuo richiede una numerosità della popolazione. Non averla non è un dettaglio implementativo mancante: è una decisione presa a monte, che rende la generazione stocastica **impossibile in linea di principio** e non semplicemente superflua.

**Il seed è quindi decorativo e va tolto, non tenuto per apparenza.** Un seed fisso su uno script che non estrae nulla comunica al lettore che da qualche parte c'è del caso sotto controllo, ed è falso. La riproducibilità che il principio II richiede è qui garantita dalla forma stessa del calcolo: gli stessi input producono gli stessi output perché non c'è nient'altro in mezzo.

**Lo scostamento dalla roadmap va dichiarato.** La nota sulla `004` in [`docs/roadmap.md`](../../docs/roadmap.md) prescrive che «uno script con seed fisso genera il dataset a partire da quel file». Questa spec non lo esegue e ne dichiara la ragione: la formulazione della roadmap precede l'uscita di engagement e base utenti dal perimetro, cioè precede le due decisioni che tolgono al seed il proprio oggetto. Non è un aggiramento — è la registrazione di una prescrizione superata dai fatti, e vale il vincolo di FR-024.

---

### D2 — Da un benchmark a tre scenari

Questa è la decisione con più contenuto metodologico della feature, ed è quella su cui il lettore critico si fermerà per primo. Il benchmark fornisce **un** valore; `BQ3-K1` ne pretende **tre**. Ciò che sta in mezzo non è misurato da nessuno.

**Le opzioni**: (a) il benchmark è lo scenario *base*, e *best*/*worst* si ottengono da una banda dichiarata attorno a esso; (b) il benchmark è lo scenario *best*, cioè un tetto che un operatore maturo raggiunge e un nuovo entrante no, con *base* e *worst* come frazioni dichiarate; (c) tre benchmark distinti, uno per scenario.

**La decisione**: **(a)**. Il valore del benchmark è adottato come **scenario base**; *worst* e *best* si ottengono applicandogli una coppia di fattori dichiarati, **simmetrici in termini relativi**.

> **Nota del 2026-08-16 — la simmetria relativa richiede fattori reciproci.** L'implementazione aveva letto «simmetrici in termini relativi» come `1 − k` e `1 + k`, che non lo sono: con k = 0,50 il rapporto fra centrale e pessimista vale 2 e quello fra ottimista e centrale vale 1,50, cioè la banda è simmetrica in termini **assoluti**. La simmetria relativa vale se e solo se il prodotto dei due fattori è l'unità. Ritrovamento della revisione in contesto pulito, che leggeva il solo documento pubblicato; i fattori sono ora `0,50` e `2,00`. La decisione D2 non cambia — cambia la forma che la realizza, e la lezione è che una proprietà dichiarata in una decisione va **verificata** sull'implementazione, perché nessun controllo di questo progetto la presidia.

**La ragione, e ciò che la decisione ammette di non sapere**:

- **(c) è esclusa dal perimetro**, che ammette un solo benchmark. Tre benchmark su tre operatori diversi non descriverebbero comunque tre scenari dello stesso operatore: descriverebbero la dispersione fra operatori, che è una grandezza diversa e che nessuna delle due misure di BQ3 consuma.
- **(b) è respinta perché contrabbanda un'affermazione per una scelta di forma.** Dire che il valore osservato è un tetto significa affermare che StreamWave farà peggio di chi il verticale ce l'ha già. È un'affermazione sul mondo, plausibile quanto la sua contraria — un catalogo adiacente già posseduto potrebbe convertire meglio, non peggio — e nessun dato di questo progetto la sostiene. Collocarla dentro la scelta della forma degli scenari la renderebbe invisibile a chi legge il risultato.
- **(a) tiene separate le due cose che vanno tenute separate**: il centro della banda è ciò che il benchmark dice, la sua ampiezza è ciò che l'analista stipula. Il lettore può contestare l'uno senza contestare l'altra.

**L'ampiezza della banda non misura nulla, e la spec lo dichiara.** Non è una stima di varianza, non è un intervallo di confidenza e non deriva da alcuna osservazione: è la dichiarazione di **quanta fiducia l'analista ripone nel trasferimento** del benchmark a StreamWave. Va quindi trattata come una soglia nel senso di [`docs/convenzioni-marcatura.md`](../../docs/convenzioni-marcatura.md) §2 — stipulazione di chi analizza — con l'obbligo, che quel documento impone, di **ancorarla** anziché limitarsi a dichiararla: il valore dei due fattori vive fra le convenzioni dell'artefatto prodotto, non nella prosa.

**La simmetria relativa è la forma che non aggiunge affermazioni.** Una banda asimmetrica dichiarerebbe che l'errore di trasferimento è più probabile in una direzione che nell'altra, ed è un'ulteriore affermazione sul mondo che i dati non sostengono. Fra le forme disponibili, la simmetrica è l'unica che non ne fa nessuna.

**I due fattori si fissano prima di conoscere il benchmark, ed è la parte della decisione che costa meno e vale di più.** L'ampiezza della banda è l'unico numero davvero libero di questa feature. Sceglierla dopo aver visto il valore del benchmark significa sceglierla — anche in perfetta buona fede — in modo che l'intervallo risultante «sembri giusto», e **nessun controllo di questo progetto potrebbe mai accorgersene**: i fattori sarebbero ancorati, la derivazione riproducibile, l'esito verde, e il numero comunque scelto a valle del risultato che doveva produrre.

Il progetto ha già il precedente e la formula. §3 del business case fissa la regola di decisione **prima** di misurare, e ne dichiara la natura della garanzia: non l'ignoranza di chi scrive, ma il fatto che la regola sia pubblica e immutabile prima dei risultati, così che ogni scostamento successivo sia visibile a chiunque confronti. Qui vale identica. I fattori sono scritti nel file dei parametri **prima che la ricognizione si concluda**; se dopo cambiano, il cambiamento è dichiarato con la sua ragione, non applicato in silenzio. Vedi FR-011a.

Ne discende che il file dei parametri nasce in **due momenti**, e la cosa è un pregio e non un incidente: prima i fattori e la loro ragione, poi il valore del benchmark e la citazione. La history git è la traccia che rende la precedenza verificabile invece che asserita — chi dubita apre il log e guarda l'ordine. Come i due momenti si traducano in commit è materia del piano, non di questa spec.

**Un obbligo di lettura discende da qui, e va scritto accanto ai valori**: `BQ3-K1` non è un intervallo di confidenza e la sua ampiezza non ha interpretazione probabilistica. §7 del business case istruisce il board a considerare lo scenario *worst* come il caso da poter sostenere; quella lettura resta valida e non richiede che l'intervallo sia probabilistico, ma richiede che nessuno lo tratti come tale.

---

### D3 — La precisione con cui i sei valori si pubblicano

**Il vincolo**: il principio I della constitution vieta di presentare un valore sintetico con precisione superiore a quanto la metodologia giustifica — «se la generazione poggia su un'assunzione a una cifra significativa, il risultato non può esserne mostrato con tre».

**La decisione**: **i sei valori si pubblicano con lo stesso numero di cifre significative del benchmark da cui discendono**, e mai più di due. La regola di arrotondamento è dichiarata fra le convenzioni dell'artefatto e applicata dallo script, non a mano.

**La ragione**: il prodotto per il differenziale di prezzo è l'operazione che più facilmente inganna, perché 4,00 € è un valore esatto per costruzione — è una decisione di scenario, non una misura — e moltiplicare per un valore esatto conserva l'illusione di precisione dell'altro fattore. Un tasso noto a due cifre moltiplicato per 4,00 € produce un uplift noto a due cifre, non a quattro, per quanti decimali la divisione in virgola mobile restituisca.

**Nota del 2026-08-16, in fase di implementazione — la regola si sdoppia.** La formulazione originale della decisione e di FR-015 era: «i sei valori si pubblicano con lo stesso numero di cifre significative del benchmark da cui discendono, e mai più di due». Applicata alla lettera agli importi è sbagliata, e il benchmark adottato lo ha reso visibile: `uplift.base` vale 1,20 € e `uplift.best` vale 2,40 €, che portano **tre** cifre significative ciascuno; `uplift.worst`, che vale 0,60 €, era l'unico dei tre già conforme.

La correzione **non** è pubblicare `1,2 €` e `2,4 €`. La seconda cifra decimale di un importo è il centesimo, cioè l'unità in cui la valuta è denominata: è convenzione di scrittura, non una cifra di precisione rivendicata, e un importo scritto senza di essa si legge come malformato invece che come prudente. La regola distingue quindi **cifre significative per i tassi** e **posizioni decimali fisse per gli importi**, e `bq3_rounding` dichiara che la precisione effettiva degli importi resta quella del benchmark — due cifre — perché nessuno legga `1,20 €` come una conoscenza a tre.

Il caso vale oltre questa feature: la regola sulle cifre significative del principio I è scritta per grandezze misurate, e una valuta non è una di quelle. Senza la distinzione, la feature che esiste per non violare il principio I lo avrebbe violato in silenzio proprio nella riga che pubblica.

---

### D4 — Le disdette sono escluse *(chiusura di R13 della revisione 001, parte BQ3)*

**Il rilievo**: `BQ3-K1` «misura una quota entro dodici mesi su una base assunta stabile: le disdette non sono menzionate né come incluse né come escluse».

**La decisione**: **escluse**, e la scheda deve dirlo.

**La ragione**: non è una scelta di questa feature, è una conseguenza già scritta altrove che nessuno aveva ancora tratto. FR-018 della 001 vieta al modello di presupporre una riduzione di churn; A5 assume la base utenti stabile per l'orizzonte considerato. Ne discende che il tasso di adozione è **lordo su una base costante**: descrive quanta parte della base sottoscrive il tier premium entro 12 mesi, non quanta parte lo sottoscrive e lo mantiene. Un abbonato che passa al premium e poi disdice conta nel tasso.

**La conseguenza sulla lettura, che è la parte che vale la pena scrivere**: ne segue che `BQ3-K2` è un **uplift di ricavo a regime sotto l'ipotesi di base costante**, e non un ricavo incrementale cumulato sui 12 mesi. Le due grandezze coincidono solo se nessuno disdice, che è esattamente ciò che A5 assume e che il mondo non fa. È un limite del modello, non un difetto del calcolo, e va dichiarato fra i Limiti.

**Dove va dichiarata**: nota datata sulla scheda `BQ3-K1` in §5.5 di `docs/business_case.md`, secondo la prassi sugli artefatti già mergiati. La parte di R13 che riguarda `BQ2-K3` e `BQ1-K2` **non** è di questa feature: è della `007`.

---

### D5 — Che cosa diventa l'etichetta di fonte di `BQ3-K1`

**Il problema**: la scheda di `BQ3-K1` dichiara oggi «**Fonte**: Sintetico». Dopo l'ancoraggio la catena che porta al valore è composta: un benchmark osservato su un operatore terzo, più una banda stipulata dall'analista.

**La decisione**: la riga di fonte originale **non viene riscritta**. Una **nota datata** accanto alla scheda dichiara la composizione risultante — `Derivato` (`Benchmark (esterno)` per il centro della banda + assunzione di scenario dell'analista per l'ampiezza) — e la ragione per cui l'etichetta cambia.

**La ragione**: `CLAUDE.md` prescrive che il valore originale resti come traccia di ciò che quella feature aveva osservato, e la prassi vale per le affermazioni quanto per i numeri. L'etichetta `Sintetico` non era sbagliata quando è stata scritta: era esatta sotto la constitution v1.0.2, dove i benchmark non erano una fonte ammessa. È **superata da un emendamento**, il che è un caso diverso dall'errore e non autorizza la riscrittura silenziosa.

**Ciò che la decisione esplicitamente non fa**: non tocca il **livello di confidenza**, che resta `bassa`, né il formato, che resta range best/base/worst. Il principio I lo vieta espressamente — l'ancoraggio rende il parametro verificabile, non certo — e §6 del business case lo colloca fuori scala per costruzione, come A1. Vedi FR-021.

---

### D6 — La feature produce un documento di lettura

**Le opzioni**: (a) nessun documento — i valori e la citazione vivono nel file dei parametri e nell'artefatto, e le note sul business case bastano; (b) un documento sotto `docs/`, marcato e sotto severità stretta.

**La decisione**: **(b)**, un documento di lettura.

**La ragione**: ciò che questa feature produce di più contestabile non sono i sei valori — sono una moltiplicazione — ma il **ragionamento che porta da un tasso osservato su un altro operatore a tre scenari su StreamWave**. Quel ragionamento è prosa: non entra in un file di parametri senza diventare un commento, e un commento è esattamente ciò che la condizione 2 della constitution esclude come sede. BQ3 è inoltre la domanda su cui un board eserciterebbe per prima il proprio scetticismo, ed è l'unica del progetto interamente non osservata: lasciarla senza un documento che ne dichiari il metodo e i limiti sarebbe l'omissione più costosa del progetto.

**Il costo che la decisione accetta**: il documento è nuovo, quindi entra in `DOCUMENTS` di `scripts/check_audit_coherence.py` **sotto severità stretta**. La regola di non retroattività vale a favore dei documenti vecchi, non dei nuovi.

---

## Rapporto con le feature vicine

Tre precisazioni per chi legge le spec in sequenza.

**Questa feature non calcola KPI.** Produce i **parametri e i valori di scenario** che `BQ3-K1` e `BQ3-K2` consumeranno. La misura DAX, il suo nome nel modello e il valore che comparirà in dashboard sono della `007`. Il confine è netto e verificabile: questa feature non scrive alcuna espressione DAX e non stabilisce alcuna granularità di modello.

**Questa feature è indipendente dai dati della `002` e della `003`, non dai loro strumenti.** La distinzione va fatta perché la roadmap chiama la 004 «l'unica feature parallelizzabile» e la formulazione più larga sarebbe falsa.

*Indipendente dai dati*, e questa è la proprietà da preservare: non legge alcun dataset reale, non apre `data/raw/`, non riesegue la pipeline di cleaning e non cita alcun identificativo di `reports/data_profile.json` o `reports/cleaning_report.json`. È ciò che la rende eseguibile in una giornata in cui il contesto sui dati reali non è fresco, ed è ciò che rende respingibile qualunque requisito che introducesse una dipendenza dai dati reali.

*Dipendente dagli strumenti*, e va detto: FR-019 e FR-020 modificano [`docs/convenzioni-marcatura.md`](../../docs/convenzioni-marcatura.md) e `scripts/check_audit_coherence.py`, che sono artefatti della `002` e della `003`. La feature ne eredita la grammatica e ne estende lo spazio dei nomi. Chi la esegue deve conoscere quei due artefatti, anche senza conoscere i dati che descrivono.

**Questa feature aggiunge un terzo artefatto allo spazio dei nomi della marcatura.** Oggi il controllo unisce le mappe `values` di due artefatti; da qui in avanti sono tre. La verifica di collisione che il controllo già esegue non va indebolita, e la fonte unica della grammatica va aggiornata di conseguenza: vedi FR-018 e FR-019.

---

## Perimetro

Ciò che questa feature **non** fa, e a chi spetta.

| Fuori perimetro | Ragione | A chi spetta |
|---|---|---|
| **Churn e retention** | FR-018 della 001 vieta al modello di presupporre una riduzione di churn. Un benchmark di churn finanzierebbe un parametro vietato | a nessuno: è escluso dal modello, non rinviato |
| **Engagement** | BQ3 ha due sole misure e nessuna lo consuma. Un dataset di engagement produrrebbe numeri che nessuna misura legge | a nessuno: escluso |
| **Determinazione dei prezzi** | A4 li fissa come valori puntuali di scenario e FR-017a della 001 vieta di esprimerli a range | a nessuno: già decisi in 001 |
| **Quantificazione della base utenti** | divergenza 9 della revisione 001, chiusa il 2026-08-10 | a nessuno: `BQ3-K2` resta euro per utente al mese e **non è scalabile** (FR-009) |
| **Generazione di un dataset sintetico di righe** | decisione D1 | a nessuno: non esiste consumatore |
| **Modello dati, tabelle, relazioni, granularità** | | `005` |
| **Misure DAX e valori calcolati dei KPI** | | `007` |
| **Dashboard e presentazione** | | `008` |
| **R13 per le parti `BQ2-K3` e `BQ1-K2`** | questa feature chiude la sola parte BQ3 | `007` |
| **Dataset reali e pipeline della 003** | nessuna lettura, nessuna riesecuzione | — |

---

## User Scenarios & Testing *(mandatory)*

Gli attori sono due: **chi rilegge** — un membro del board, un revisore, chiunque riceva il repository — e **chi esegue**, cioè la `007` che consumerà i valori.

### User Story 1 — Il parametro è verificabile alla fonte (Priority: P1)

Chi legge il valore dello scenario base vuole sapere da dove viene. Apre il file dei parametri e vi trova il numero adottato insieme all'organizzazione che l'ha pubblicato, il titolo, la data di pubblicazione, un riferimento recuperabile e la data in cui è stato consultato. Può contestare il trasferimento a StreamWave, ma non può chiedersi se il numero sia stato inventato.

**Why this priority**: è l'intera ragione per cui la constitution è stata emendata a v1.1.0. Senza questa storia la feature resta conforme ma incoerente con la tesi che il progetto sostiene.

**Independent Test**: si apre il file dei parametri senza rete e senza rieseguire nulla; i cinque elementi della citazione sono tutti presenti e il riferimento è raggiungibile da chi ha rete.

**Acceptance Scenarios**:

1. **Given** una copia pulita del repository e nessun accesso a internet, **When** si apre il file dei parametri, **Then** il valore adottato e la sua citazione completa sono leggibili senza eseguire alcuno script.
2. **Given** il file dei parametri, **When** si cerca l'assunzione di trasferimento, **Then** è scritta accanto al valore e non altrove.
3. **Given** una fonte candidata che non soddisfa una delle cinque condizioni della constitution, **When** si valuta se adottarla, **Then** viene respinta e il fatto è registrato.

---

### User Story 2 — I sei valori si rigenerano da una copia pulita (Priority: P1)

Chi clona il repository esegue un solo comando, senza rete e senza `data/raw/`, e ottiene i sei valori identici a quelli versionati.

**Why this priority**: è il principio II, ed è la condizione 3 della constitution — la ricerca è congelata, la derivazione è rieseguibile. Senza questa storia il valore ancorato non varrebbe più di un numero scritto a mano.

**Independent Test**: si esegue la derivazione due volte su una copia pulita e si confrontano gli output byte per byte.

**Acceptance Scenarios**:

1. **Given** una copia pulita del repository senza `data/raw/` e senza rete, **When** si esegue la derivazione, **Then** produce l'artefatto dei sei valori senza errori.
2. **Given** due esecuzioni consecutive, **When** si confrontano gli artefatti prodotti, **Then** sono identici.
3. **Given** lo script della derivazione, **When** lo si ispeziona, **Then** non contiene alcuna chiamata di rete e alcun generatore di numeri casuali.
4. **Given** un file dei parametri modificato nel valore del benchmark, **When** si riesegue, **Then** tutti e sei i valori cambiano di conseguenza — nessuno è scritto a mano nell'artefatto.

---

### User Story 3 — Il documento dichiara metodo e limiti, e ogni suo numero è ancorato (Priority: P2)

Chi legge il documento capisce come si passa da un tasso osservato altrove a tre scenari su StreamWave, che cosa quei numeri non dicono, e può risalire da ogni cifra pubblicata all'artefatto che la produce.

**Why this priority**: senza le due storie precedenti il documento non avrebbe di che parlare. Con esse, è ciò che rende il lavoro leggibile da fuori.

**Independent Test**: si esegue il controllo di coerenza sul documento; passa sotto severità stretta.

**Acceptance Scenarios**:

1. **Given** il documento, **When** si esegue `scripts/check_audit_coherence.py`, **Then** l'esito è verde sotto severità stretta.
2. **Given** una cifra del documento resa non corrispondente all'artefatto, **When** si riesegue il controllo, **Then** fallisce indicando identificativo, atteso e trovato.
3. **Given** un numerale privo di marcatore in posizione di fatto misurato, **When** si riesegue il controllo, **Then** **fallisce** e non si limita ad avvisare.

---

### User Story 4 — Il business case porta l'assunzione di trasferimento (Priority: P2)

Chi legge il business case incontra `A6` fra le assunzioni strutturali, la ritrova richiamata in §6 accanto ad `A1`, e trova sulle schede `BQ3-K1` e `BQ3-K2` le note datate che dichiarano che cosa è cambiato e quando.

**Why this priority**: è il debito testuale dell'ancoraggio, tracciato in roadmap e da chiudere dentro questa feature. Senza, l'emendamento alla constitution resterebbe senza riscontro nell'artefatto che il board legge.

**Independent Test**: si legge `docs/business_case.md` dall'inizio; `A6` compare in §2 con la stessa forma di `A1`, è richiamata in §6, e le due schede portano note datate.

**Acceptance Scenarios**:

1. **Given** §2 del business case, **When** si cerca `A6`, **Then** istituisce l'assunzione di trasferimento dei benchmark ed è formulata sul modello di `A1`.
2. **Given** §6, sottosezione «Cosa questa scala non misura», **When** la si legge, **Then** `A6` vi è affiancata ad `A1` come seconda assunzione fuori scala.
3. **Given** le schede `BQ3-K1` e `BQ3-K2`, **When** le si legge, **Then** ciascuna porta una nota datata e **nessun valore o affermazione originale risulta cancellato o riscritto**.

---

### Edge Cases

- **Nessuna fonte soddisfa tutte e cinque le condizioni.** È l'esito che il prompt di consegna prevede esplicitamente e che la ricognizione preliminare rende possibile: la metrica esatta — quota della base esistente che passa a un tier superiore — non risulta pubblicata in forma direttamente citabile e gratuitamente recuperabile. La feature **non ripiega su un valore plausibile** e **non allarga la definizione della metrica** per far entrare una fonte che misura altro. Si ferma, registra le fonti valutate e il motivo del rigetto, e la decisione se dichiarare il parametro come scelta dell'analista **spetta a Valerio**, non a chi esegue. Vedi FR-005 e FR-006.
- **La fonte è recuperabile ma il numero sta dentro un PDF o una pagina che potrebbe sparire.** Il valore è comunque congelato nel file dei parametri con la data di accesso: è precisamente ciò che la condizione 2 impone e la ragione per cui lo impone.
- **Il benchmark misura una cosa vicina ma non identica** — per esempio movimenti fra piani con e senza pubblicità anziché l'aggiunta di un verticale. Lo scostamento fra ciò che la fonte misura e ciò per cui viene usato è **parte dell'assunzione di trasferimento** e va scritto lì, esplicitamente, non taciuto perché scomodo.
- **Il valore del benchmark è espresso come intervallo nella fonte.** Si adotta come scenario base un valore puntuale ricavato con una regola dichiarata, e l'ampiezza dell'intervallo della fonte **non** si confonde con la banda di D2, che ha tutt'altra natura.
- **Uno scenario produce un tasso negativo o superiore al 100%.** La derivazione si ferma con errore: un tasso di adozione fuori da 0-100 non è uno scenario pessimista, è un difetto della regola.
- **Un identificativo del nuovo artefatto collide con uno dei due esistenti.** Il controllo già verifica le collisioni invece di assumerne l'assenza; la verifica non va indebolita per far entrare il terzo artefatto.

---

## Requirements *(mandatory)*

### Il benchmark e la sua citazione

- **FR-001**: La feature MUST adottare **un solo** benchmark pubblico di settore: il tasso di conversione a un tier superiore in servizi di streaming. NON DEVE raccogliere benchmark per churn, engagement, prezzi o dimensione della base utenti.
- **FR-002**: Il valore adottato MUST vivere in un **file versionato** del repository insieme alla propria citazione. NON DEVE vivere nella prosa di un documento né in un commento del codice.
- **FR-003**: La citazione MUST contenere tutti e cinque gli elementi: organizzazione che pubblica, titolo, data di pubblicazione, riferimento recuperabile, data di accesso. Un valore attribuito a «ricerche di settore» o a una fonte non nominata NON DEVE essere adottato.
- **FR-004**: Il file dei parametri MUST dichiarare, accanto al valore, **che cosa la fonte misura esattamente** e in che modo differisce da ciò per cui viene usato. Lo scostamento è parte dell'assunzione di trasferimento (FR-007).
- **FR-005**: La feature MUST registrare le fonti valutate e respinte con il motivo del rigetto, non solo quella adottata. Un rigetto non registrato rende non verificabile l'affermazione che la fonte adottata fosse la migliore disponibile.
- **FR-006**: Se **nessuna** fonte soddisfa tutte e cinque le condizioni della constitution, la feature MUST fermarsi e riportarlo. NON DEVE adottare un valore «plausibile» presentandolo come benchmark, e NON DEVE dichiarare autonomamente il parametro come scelta dell'analista: quella è una decisione fuori dal perimetro di chi esegue.
- **FR-006a**: La fonte **adottata**, con il proprio scarto di misura (FR-004), MUST essere riportata allo stesso punto di stop e allo stesso revisore in cui si riporterebbe il fallimento di FR-006. L'adozione non è un esito silenzioso. *Ragione*: il rischio principale non è il fallimento rumoroso, che si vede da solo, ma l'**adozione di una fonte «abbastanza vicina»**. FR-004 e il terzo Edge Case ammettono correttamente una metrica adiacente purché lo scarto sia dichiarato, e non esiste né può esistere un presidio automatico su *quanto* adiacente sia troppo. Senza questo requisito la valutazione la fa da solo chi esegue, e lo scarto finisce dichiarato in un file che nessuno rilegge prima del merge.
- **FR-007**: L'**assunzione di trasferimento** MUST essere scritta accanto al valore nel file dei parametri, e MUST dichiarare che il valore descrive un operatore terzo e non StreamWave.
- **FR-008**: Nessuno script della feature MUST contattare una fonte esterna durante l'esecuzione. La raccolta è un passaggio umano il cui esito è congelato.

### La derivazione

- **FR-009**: La derivazione MUST produrre esattamente sei valori: tre tassi di adozione (*worst*, *base*, *best*) e i tre uplift di ricavo corrispondenti, espressi in **euro per utente al mese**. NON DEVE produrre alcun valore aggregato sulla base utenti, che non è quantificata.
- **FR-010**: Lo scenario *base* MUST assumere il valore del benchmark. Gli scenari *worst* e *best* MUST ottenersi applicandogli una coppia di fattori dichiarati e simmetrici in termini relativi.
- **FR-011**: I due fattori della banda MUST essere **ancorati** fra le convenzioni dell'artefatto prodotto, non solo dichiarati in prosa, e MUST essere accompagnati dalla dichiarazione che l'ampiezza della banda **non misura nulla**: è la fiducia dell'analista nel trasferimento, non una varianza osservata.
- **FR-011a**: I due fattori MUST essere fissati e scritti nel file dei parametri **prima che la ricognizione sul benchmark si concluda**, e la loro precedenza temporale MUST essere dichiarata. Se dopo la ricognizione vengono cambiati, il cambiamento MUST essere dichiarato con la propria ragione; NON DEVE essere applicato in silenzio. *Ragione*: l'ampiezza della banda è l'unico numero libero della feature, e sceglierla a valore del benchmark noto la piega verso l'intervallo che «sembra giusto» senza che alcun controllo possa rilevarlo. È la stessa garanzia che §3 del business case ottiene fissando la regola di decisione prima di misurare.
- **FR-012**: I tre uplift MUST essere il prodotto del rispettivo tasso per il differenziale di **4,00 €** fissato in A4. Il differenziale MUST essere letto dal file dei parametri, non scritto nel codice.
- **FR-013**: La derivazione MUST essere **deterministica**: nessun generatore di numeri casuali, nessun seed, nessuna dipendenza dall'ora di esecuzione. Due esecuzioni consecutive MUST produrre artefatti identici.
- **FR-014**: Nessun valore dell'artefatto MUST essere scritto a mano. Modificare il benchmark nel file dei parametri e rieseguire MUST cambiare tutti e sei i valori.
- **FR-015**: I sei valori MUST essere pubblicati alla precisione che il benchmark giustifica, che è di **al più le sue cifre significative e mai più di due**. La regola MUST distinguere due famiglie: i **tassi** — `BQ3.adoption.*` e `BQ3.band.spread_pp` — si pubblicano a cifre significative; gli **importi in euro** — `BQ3.uplift.*` — si pubblicano a **due posizioni decimali fisse**, che sono la convenzione della valuta e non una pretesa di precisione. La convenzione `bq3_rounding` MUST dichiarare entrambe le famiglie e MUST dichiarare che la precisione effettiva degli importi resta quella del benchmark. `BQ3.band.ratio` non discende dal benchmark ed è esatto per costruzione. La regola di arrotondamento MUST essere dichiarata fra le convenzioni dell'artefatto e applicata dallo script. *Vedi la nota di emendamento in D3.*
- **FR-016**: La derivazione MUST fermarsi con errore se un tasso risultante cade fuori dall'intervallo 0-100.
- **FR-017**: La derivazione MUST essere eseguibile su una copia pulita del repository **senza rete e senza `data/raw/`**, e NON DEVE leggere alcun dataset reale né alcun output della `003`.

### Marcatura e artefatti

- **FR-018**: L'artefatto dei sei valori MUST esporre una mappa `values` con identificativi stabili, secondo la struttura degli artefatti esistenti, così da entrare nello spazio dei nomi della marcatura. La verifica di collisione fra artefatti NON DEVE essere indebolita.
- **FR-018a**: L'artefatto dei sei valori MUST essere **versionato nel repository**. *Ragione*: FR-020 e SC-004 presuppongono che il controllo di coerenza lo risolva su una copia pulita, e un artefatto rigenerabile ma non versionato renderebbe il controllo eseguibile solo dopo aver eseguito la derivazione. È il precedente di `reports/cleaning_report.json`, versionato perché la 003 lo aveva scritto come requisito e non perché fosse ovvio. Se non è scritto, non accade.
- **FR-019**: [`docs/convenzioni-marcatura.md`](../../docs/convenzioni-marcatura.md) MUST essere aggiornato: §3 elenca oggi due artefatti e da qui in avanti sono tre, e la tabella di provenienza in coda MUST registrare la data e la feature. È la fonte unica e non può descrivere uno stato superato.
- **FR-020**: Il documento di lettura prodotto dalla feature MUST essere aggiunto a `DOCUMENTS` in `scripts/check_audit_coherence.py` **sotto severità stretta**, e MUST passare il controllo. Ogni numero che pubblica MUST portare o l'ancora o il marcatore di non-misurato.

### Confidenza, formato e limiti

- **FR-021**: `BQ3-K1` e `BQ3-K2` MUST restare a confidenza **bassa** e in formato **range best/base/worst**. L'ancoraggio a un benchmark NON DEVE essere trattato come innalzamento della confidenza, in nessun artefatto della feature.
- **FR-022**: Il documento e l'artefatto MUST dichiarare che il range **non è un intervallo di confidenza** e che la sua ampiezza non ha interpretazione probabilistica.
- **FR-023**: La feature MUST dichiarare esplicitamente che `BQ3-K2` è **euro per utente al mese e non è scalabile** a un totale di ricavo, e che nessuna base utenti viene quantificata. La dichiarazione va scritta, non solo rispettata.
- **FR-024**: Lo scostamento dalla prescrizione della roadmap sul seed fisso (decisione D1) MUST essere dichiarato negli artefatti della feature. Una prescrizione superata dai fatti va registrata come tale, non lasciata cadere in silenzio.

### Debito testuale su `docs/business_case.md`

- **FR-025**: §2 MUST accogliere una nuova assunzione strutturale **`A6`**, che istituisce l'assunzione di trasferimento dei benchmark, formulata sul modello di `A1` e con la stessa forma grafica delle altre.
- **FR-025a**: `A6` **NON DEVE contenere il valore del benchmark**, né alcuna delle sei cifre derivate. Istituisce l'assunzione e rimanda al file dei parametri, dove il numero vive ancorabile. *Ragione*: `docs/business_case.md` non è fra i documenti sotto controllo di coerenza, quindi un numero scritto nella sua prosa non porta ancora e nessuno lo verifica. È esattamente il rilievo R8 della revisione 001 — un numero che compare solo in prosa, senza uno script che lo rigeneri, è un debito — che la 002 ha chiuso e che questa feature non deve riaprire.
- **FR-026**: §6, sottosezione «Cosa questa scala non misura», MUST richiamare `A6` accanto ad `A1` come seconda assunzione che resta fuori dalla scala di confidenza per costruzione.
- **FR-027**: Le schede `BQ3-K1` e `BQ3-K2` in §5.5 MUST portare ciascuna una **nota datata** che dichiari data, feature, che cosa è cambiato e la fonte verificabile.
- **FR-027a**: Le note di FR-027 MUST rispettare lo stesso vincolo di FR-025a: **nessun valore di benchmark e nessuna delle sei cifre derivate nella prosa del business case**. La «fonte verificabile» che la nota dichiara è il rimando al file dei parametri e all'artefatto, non il numero trascritto. Vale anche per il differenziale di 4,00 €, che però **è già in A4** e resta dov'è: la nota lo cita come riferimento ad A4, non lo riafferma.
- **FR-028**: La nota su `BQ3-K1` MUST chiudere R13 per la parte BQ3 dichiarando che **le disdette sono escluse** e che il tasso è lordo su base costante, con il rimando a FR-018 della 001 e ad A5.
- **FR-029**: La nota su `BQ3-K1` MUST dichiarare la composizione della fonte dopo l'ancoraggio (decisione D5) **senza riscrivere** la riga «Fonte: Sintetico» esistente.
- **FR-030**: **Nessun valore o affermazione originale di `docs/business_case.md` MUST essere cancellato o sovrascritto.** Gli interventi sono aggiunte; vale comunque la prassi di `CLAUDE.md` sugli artefatti già mergiati.

### Regola D5 sulle affermazioni derivate

- **FR-031**: Ogni confronto, rapporto, differenza o graduatoria che gli artefatti della feature costruiscono su valori misurati MUST avere un identificativo proprio nell'artefatto ed essere ancorato, oppure non essere scritto. In particolare, l'ampiezza della banda e il rapporto fra scenario *best* e scenario *worst* sono essi stessi valori.
- **FR-032**: I numerali scritti in lettere NON DEVONO essere usati per alcun fatto misurato nei documenti nuovi della feature.

### Key Entities

- **File dei parametri**: artefatto versionato, curato a mano e mai riscritto da uno script. Contiene il valore del benchmark, la citazione nei suoi cinque elementi, che cosa la fonte misura, l'assunzione di trasferimento, i due fattori della banda, il differenziale di prezzo di A4 e le fonti respinte con il motivo.
- **Artefatto dei valori di scenario**: prodotto dalla derivazione. Contiene i sei valori con identificativi stabili, le convenzioni adottate (fattori della banda, regola di arrotondamento) e i riferimenti al file dei parametri da cui discendono. Entra nello spazio dei nomi della marcatura come terzo artefatto.
- **Documento di lettura**: prosa che dichiara metodo, assunzione di trasferimento, che cosa i sei valori non dicono e come si leggono. Ogni numero ancorato, severità stretta.
- **Note sul business case**: aggiunte in loco a un artefatto già mergiato — `A6`, il richiamo in §6, le due note datate sulle schede.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chi riceve il repository può risalire dal valore dello scenario base alla sua fonte pubblicata **senza eseguire alcuno script e senza accesso a internet**, e trova tutti e cinque gli elementi della citazione.
- **SC-002**: La derivazione, eseguita due volte su una copia pulita priva di `data/raw/` e senza rete, produce artefatti **identici**.
- **SC-003**: Modificare il solo valore del benchmark nel file dei parametri e rieseguire cambia **tutti e sei** i valori pubblicati: nessuno è scritto a mano.
- **SC-004**: Il controllo di coerenza passa sul documento nuovo **sotto severità stretta**, e continua a passare sui due documenti esistenti senza che la loro severità sia stata modificata.
- **SC-005**: Nessun artefatto della feature presenta `BQ3-K1` o `BQ3-K2` come valore singolo, e nessuno ne innalza la confidenza sopra `bassa`.
- **SC-006**: Un lettore del business case incontra `A6` in §2, la ritrova in §6 e trova le due note datate in §5.5, **senza che alcun valore o affermazione preesistente risulti rimosso** — verificabile confrontando il diff, che deve essere di sole aggiunte sul testo preesistente.
- **SC-007**: Nessuno script della feature contiene una chiamata di rete, un generatore di numeri casuali o un seed — verificabile per ispezione.

I sette criteri sono tutti verificabili **sul prodotto**, da chi riceve il repository e senza sapere come è stato costruito. La **stima di 6 ore**, revisione in contesto pulito e chiusura dei rilievi incluse, non compare fra loro: è un vincolo di processo, appartiene alla stima della roadmap e al gate del principio III, e non è una proprietà dell'artefatto. Una feature consegnata in otto ore non è per questo difettosa; una che fallisse SC-004 lo sarebbe.

---

## Assumptions

- **Esiste una fonte pubblica citabile** per il tasso di conversione a un tier superiore. È l'assunzione più esposta della feature: la ricognizione preliminare non l'ha confermata, e FR-006 governa il caso in cui cada.
- **Il differenziale di 4,00 € è esatto per costruzione**, non stimato: è una decisione di scenario di A4 e non porta incertezza propria.
- **L'orizzonte è 12 mesi** e la base è assunta stabile, per A5. Questa feature non riapre né l'uno né l'altra.
- **La `007` consumerà i sei valori così come sono pubblicati**, senza ricalcolarli. Se dovesse ricalcolarli, l'artefatto di questa feature diventerebbe una seconda fonte di verità, ed è la cosa che FR-014 e la struttura dell'artefatto esistono per evitare.
- **Il documento nuovo non sostituisce le note sul business case.** Sono due destinatari diversi: il business case è il documento che il board legge, il documento di questa feature è quello che chi contesta il metodo apre.

---

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: **BQ3 — Impatto stimato**.
- **Contributo**: BQ3 chiede quale intervallo di tasso di adozione del tier premium e quale conseguente intervallo di variazione del ricavo medio per utente siano compatibili con le assunzioni dichiarate. Questa feature produce **i parametri e i valori di scenario** che rendono quella risposta calcolabile, e li ancora a una fonte esterna verificabile invece di stabilirli per scelta dell'analista. Non calcola i KPI — quelli sono della `007` — ma senza di essa la `007` non avrebbe da che partire, e BQ3 resterebbe l'unica domanda del progetto la cui risposta poggia interamente su numeri decisi a tavolino.

---

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

| Metrica | Fonte | Confidenza | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| Tasso di conversione a tier superiore (valore adottato) | `Benchmark (esterno)` | **bassa** | osservato su un operatore terzo e trasferito a StreamWave; l'ancoraggio rende il valore verificabile, non trasferibile (principio I, v1.1.0) | valore puntuale **nel file dei parametri**, mai pubblicato da solo come previsione |
| Fattori della banda di scenario (*worst*, *best*) | `Sintetico` | **bassa** | stipulazione dell'analista: dichiara la fiducia nel trasferimento, non misura alcuna varianza | coppia di fattori dichiarata e ancorata fra le convenzioni |
| Parametro di `BQ3-K1` — tre scenari di adozione | `Derivato` (`Benchmark (esterno)` + fattori sintetici) | **bassa** | dipende da un valore osservato altrove e da un'assunzione non verificabile con i dati disponibili | **range best/base/worst** — obbligatorio |
| Parametro di `BQ3-K2` — tre uplift di ricavo | `Derivato` (parametro di `BQ3-K1` + differenziale di A4) | **bassa** | eredita l'incertezza del tasso, unica variabile; il differenziale è esatto per costruzione | **range best/base/worst** — obbligatorio, in **euro per utente al mese** |

**Assunzioni dietro i dati sintetici**, dichiarate per iscritto e versionate insieme allo script che le implementa:

1. **Assunzione di trasferimento** (`A6`): il tasso osservato su un operatore terzo si applica a StreamWave. Non verificabile con i dati disponibili, e resta **fuori dalla scala di confidenza** per costruzione, come `A1`.
2. **Assunzione sullo scarto di misura**: ciò che la fonte misura non coincide esattamente con l'aggiunta di un verticale musicale a un catalogo video. Lo scarto è dichiarato accanto al valore (FR-004).
3. **Assunzione sulla forma degli scenari**: il benchmark è il centro e non un tetto (D2). La banda è simmetrica in termini relativi perché ogni asimmetria sarebbe un'affermazione sul mondo che nessun dato sostiene.
4. **Assunzione di base costante**: il tasso è lordo, le disdette sono escluse (D4, A5, FR-018 della 001).

**Nessuna promozione di confidenza**: tutti e quattro i parametri restano a confidenza `bassa`. Nessun artefatto della feature può presentarli come valore singolo.

---

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Non risponde a**: quanti abbonati StreamWave passerebbe davvero al tier premium. Nessun dato comportamentale su StreamWave esiste (`A3`), e un tasso osservato su un altro operatore **non è una previsione**: è il valore che qualcun altro ha misurato su un'offerta diversa, un pubblico diverso e un momento diverso.
- **Non risponde a**: quanto ricavo aggiuntivo l'iniziativa produrrebbe in totale. `BQ3-K2` è **euro per utente al mese e non è scalabile**: moltiplicarlo per una base utenti richiederebbe di quantificarla, e la divergenza 9 della revisione 001 ha deciso di non farlo.
- **Non risponde a**: quanto costerebbe costruire il verticale. Resta fuori come dichiarato in §8 del business case: questo è un business case di opportunità, non finanziario.
- **Inferenza da evitare — il range non è un intervallo di confidenza.** La sua ampiezza dichiara quanta fiducia l'analista ripone nel trasferimento del benchmark, non una probabilità. Non esiste un «95%» dentro questi tre numeri, e leggerli come se ci fosse è l'errore più probabile che un lettore tecnico possa commettere qui.
- **Inferenza da evitare — l'ancoraggio non è una validazione.** Che il parametro venga ora da una fonte citabile lo rende **verificabile**, non **vero per StreamWave**. È esattamente la distinzione che il principio I chiama assunzione di trasferimento, ed è la ragione per cui la confidenza resta `bassa`.
- **Inferenza da evitare — nessuna relazione causale.** Nulla in questi valori dice che l'aggiunta del verticale musicale *causerebbe* l'adozione osservata altrove. È un trasferimento dichiarato di un valore osservato, e va letto come tale.
- **Copertura del dato**: il benchmark descrive il mercato e il periodo che la fonte dichiara, che non coincidono né con la copertura dei dati reali del progetto (`A2`: video al 2021, musica al 2022) né con l'orizzonte ipotetico di lancio. Lo scarto temporale è parte dell'assunzione di trasferimento e va dichiarato accanto al valore.
- **Dove è esposto all'utente finale**: nelle note datate sulle schede `BQ3-K1` e `BQ3-K2` del business case, in `A6` di §2 e nel suo richiamo in §6; nel documento di lettura della feature; e — per la `008`, che eredita l'obbligo e non la scelta — accanto a ogni presentazione dei due KPI in dashboard.
