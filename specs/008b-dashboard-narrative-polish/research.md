# Research: Dashboard — narrazione, limiti a schermo, rifiniture

**Feature**: 008b-dashboard-narrative-polish | **Data**: 2026-08-27

## Perché questo documento è corto

Il Technical Context di [plan.md](./plan.md) non contiene alcun `NEEDS CLARIFICATION`: le otto decisioni `N1`-`N8` sono già argomentate per intero in [spec.md](./spec.md), approvata dalla regia il 2026-08-27. Questo file le consolida nel formato Decisione/Motivazione/Alternative richiesto dalla Fase 0, con puntatore alla sezione di spec che le argomenta per esteso.

**Che cosa distingue questa Fase 0 da quella della `008a`.** Là le decisioni sceglievano fra modi di **mostrare** un numero già fissato, e il difetto tipico era un valore giusto letto male. Qui scelgono fra modi di **dire** un limite già dichiarato altrove, e il difetto tipico è un limite dichiarato in una forma che non lo dichiara a nessuno: esatto contro la fonte, illeggibile per il destinatario. È una classe di difetto più sfuggente della precedente, perché supera ogni controllo di conformità — la frase *c'è*, e corrisponde al documento che la origina.

**Tre decisioni fanno eccezione e non riguardano il registro**: `N1`, che riguarda il processo; `N2`, che riguarda la provenienza dei numeri che finiscono in prosa; `N8`, che riguarda il criterio con cui la feature si dichiara conclusa.

## Le otto decisioni, in formato Fase 0

### N1 — Il contratto porta il testo letterale

- **Decisione**: `contracts/narrative-contract.md` contiene, per ogni blocco, quattro cose — pagina e spazio riservato di destinazione, testo letterale, obbligo che lo richiede, fonte documentale — più la formulazione esclusa dove ne esiste una vicina e sbagliata.
- **Motivazione**: il presidio di questo progetto sulla prosa è la revisione in contesto pulito, e un revisore che ricevesse un elenco di obblighi revisionerebbe l'elenco, non il testo che il lettore incontrerà. Il testo, scritto poi davanti allo schermo, entrerebbe nel deliverable senza passare da alcun controllo.
- **Alternative scartate**: un contratto che dichiara solo gli obblighi e lascia la formulazione a chi costruisce (è la forma corretta per una struttura e sbagliata per una prosa, perché lascia il deliverable fuori dal repository); pubblicare il testo anche sotto `docs/` come nono documento (una seconda copia di affermazioni già pubblicate, che può divergere dall'originale senza che nulla lo segnali).
- **Che cosa non rende**: non rende il contratto un manuale di clic. Carattere, dimensione, colore e sequenza di operazioni restano di chi costruisce (principio V).
- **Riferimento**: spec.md, `N1`.

### N2 — Nessun numero digitato, salvo una lista chiusa

- **Decisione**: nessuna cifra in un blocco di narrazione, salvo le voci di una lista dichiarata nel contratto; ogni voce nomina la propria fonte e la ragione per cui non può provenire da una misura. Dove la narrazione nomina una quantità, rimanda alla marcatura che il lettore ha davanti invece di ripetere il conteggio.
- **Motivazione**: un numero digitato in una casella di testo è un valore la cui unica fonte è che qualcuno lo ha scritto — ciò che il principio I vieta e che `F7` della `008a` ha già rifiutato per le due soglie del quadrante. Non ha alcun legame con l'artefatto che lo produce: sopravvive a un ricalcolo e resta a schermo a dire una cosa che non è più vera.
- **Alternative scartate**: ammettere i numeri purché coincidano con i pubblicati («coincide oggi» è un'osservazione, non una proprietà — è il regime che il progetto ha già scartato tre volte); vietarli in assoluto (comprerebbe la severità al prezzo di un limite dichiarato peggio: «i dati sono fermi a qualche anno fa» è più vago e non più onesto).
- **Obbligo che la lista si porta dietro**: i due anni di copertura non hanno lo stesso statuto — osservato e ancorato sul lato video, dichiarato dalla fonte e non verificabile sul lato musicale (`data_model.md` §18). Il testo li distingue, o pubblica come misurata una cosa che nessuno ha misurato.
- **Riferimento**: spec.md, `N2`.

### N3 — Il testo è sempre visibile

- **Decisione**: nessuna pagina-tooltip, nessun segnalibro, nessun pannello a scomparsa. Resta ammesso il solo tooltip statico d'intestazione, per definire un termine tecnico dove la fascia porta già il limite.
- **Motivazione**: il principio IV impone che il limite sia dichiarato, e un limite raggiungibile con un clic si legge solo se qualcuno sospetta che esista. Una pagina-tooltip è inoltre una **pagina**, quindi una quinta pagina in un report chiuso a quattro, e ospita visuali, quindi può calcolare a una grana qualunque.
- **Alternative scartate**: ammetterli tutti e tre (produce una dashboard che sembra pulita perché ha spostato altrove ciò che disturba, in una feature il cui deliverable è precisamente ciò che disturba); vietarli tutti e tre (toglierebbe l'unico posto in cui una definizione può stare senza rubare spazio a un limite).
- **Precedente**: `008a` §5.4, che vieta di rendere nascondibile la colonna della quota di zeri con lo stesso argomento.
- **Riferimento**: spec.md, `N3`.

### N4 — Il testo entra negli spazi riservati, e uno spazio insufficiente è uno scostamento

- **Decisione**: la narrazione abita le quattro fasce riservate dalla `008a` §8. Nessun blocco si sovrappone a una visuale, ne riduce l'area o sposta un elemento. Se una fascia non basta si taglia il testo e si dichiara che cosa è stato tagliato; solo se nemmeno il minimo entra si registra uno scostamento dal disegno della `008a`.
- **Motivazione**: il perimetro dichiara le pagine chiuse, e «chiuse» ha valore solo se esiste una reazione dichiarata al caso in cui la chiusura è scomoda. L'ordine — prima taglia il testo, poi dichiara — mette il costo dove sta la libertà di questa feature, che è la prosa, e non dove sta la garanzia della precedente, che è la struttura.
- **Alternative scartate**: allargare la fascia a spese di una visuale (rimette in discussione scelte già approvate e già verificate a schermo, che è esattamente ciò che la `008a` §8 riservava lo spazio per evitare); spostare il testo eccedente in un pannello (vietato da `N3`).
- **Riferimento**: spec.md, `N4`.

### N5 — La scala una volta, il *perché* dove il KPI vive

- **Decisione**: la scala di confidenza a tre livelli si spiega una volta sola sulla pagina di ingresso, insieme a ciò che essa **non** misura; la ragione del livello di ciascun KPI sta nella fascia della pagina che lo ospita. Per `BQ1-K1`, che compare su due pagine, la ragione compare una volta sola, sulla pagina `BQ1`.
- **Motivazione**: una spiegazione ripetuta per ciascuna delle otto etichette occuperebbe lo spazio che i limiti devono occupare. La frase che conta di più — *anche un KPI a confidenza alta è alta rispetto al catalogo di riferimento, non rispetto a StreamWave* — riguarda la scala e non il singolo KPI, quindi appartiene al luogo in cui la scala si spiega (`business_case.md` §6).
- **Alternative scartate**: una riga accanto a ciascuna delle otto etichette (satura le fasce e duplica su `BQ1-K1`); la sola spiegazione generale sull'ingresso (lascia scoperto l'obbligo che il contratto di dashboard della `008a`, punto 2, assegna per nome a questa feature).
- **Asimmetria dichiarata**: sull'ingresso la North Star porta le etichette e la scala generale; il suo *perché* specifico sta su `BQ1`, accanto a `C1`, dove `kpi_measures.md` §2.3 distingue la quota dalla condizione.
- **Riferimento**: spec.md, `N5`.

### N6 — `C1` e `C3` si nominano da sole

- **Decisione**: il testo nomina `C1` su `BQ1` e `C3` su `BQ2`, ciascuna singolarmente, dichiara che ciascuna è una condizione della regola di decisione del business case e che la dashboard non compone le condizioni in un esito. Non le conta, non nomina `C2`, non usa ordinali né frazioni.
- **Motivazione**: un indicatore che dice `C1: sì` accanto alla North Star invita a concludere che l'argomento sia sostenuto. La `008a` poteva tacere perché non aveva prosa; una feature che scrive prosa e tace lascia in piedi l'inferenza senza contraddirla. `(c)` è l'unica formulazione che nega l'inferenza **senza costruire l'affermazione che la nega**: dire che una condizione da sola non decide non richiede di sapere quante siano.
- **Alternative scartate**: tacere come la `008a` (contro un'inferenza che la geometria della pagina suggerisce, il silenzio non è neutrale); dichiarare che le condizioni sono tre e che una non è misurata (vietato alla lettera dal contratto di dashboard della `008a`, punto 3, e da `convenzioni-marcatura.md` §7 — «tre» sarebbe un numerale non ancorato in posizione di fatto, e «una non è misurata» un'affermazione derivata dal conteggio).
- **Che cosa non chiude**: l'issue `#17` resta aperta. Questa feature non pubblica `C2` e non ne discute il valore.
- **Riferimento**: spec.md, `N6`.

### N7 — La narrazione descrive e avverte, non conclude

- **Decisione**: nessun blocco formula una raccomandazione, un verdetto o una previsione. I registri ammessi sono tre: che cosa il valore misura, che cosa non permette di concludere, quale assunzione lo regge. Tre divieti lessicali espliciti: nessun lessico causale, nessun superlativo o ordinale su un fatto misurato non visibile a schermo, nessuna affermazione sul comportamento delle persone.
- **Motivazione**: `business_case.md` §8 dichiara che la decisione è di chi legge; una dashboard che concludesse al posto suo contraddirebbe il documento che la genera. La sintesi è inoltre la porta di servizio da cui `C1` e `C3` tornerebbero a comporsi, e da cui una graduatoria di insiemi che si sovrappongono diventerebbe una raccomandazione.
- **Alternative scartate**: una sintesi conclusiva per pagina (è la forma più naturale per una fascia di testo e la sola che il perimetro vieta due volte, per `N6` e per il business case); una raccomandazione dichiarata come opinione dell'analista (sposterebbe l'etichetta, non il problema: resterebbe a schermo, con l'autorevolezza della pagina che la ospita).
- **Riferimento**: spec.md, `N7`.

### N8 — Il criterio di pubblicabilità si fissa prima di costruire

- **Decisione**: cinque condizioni verificabili — le tre assenze del contratto di dashboard della `008a` colmate su pagine nominate; il *perché* di ogni confidenza a schermo per tutti e otto i KPI; i limiti assegnati per nome da `kpi_operators.md` §12 e `data_model.md` §18 a schermo in forma leggibile; nessuna violazione di `N2`, `N6`, `N7`; le tre impostazioni di `#20` riverificate. Accanto, l'elenco di ciò che «pubblicabile» **non** significa.
- **Motivazione**: un'affermazione formulata dopo aver guardato il risultato è una ratifica; formulata prima, è un criterio. Senza il secondo elenco, «pubblicabile» prometterebbe più di ciò che la feature consegna — e la promessa in eccesso è il difetto che questo progetto ha speso otto feature a evitare.
- **Alternative scartate**: dichiarare la pubblicabilità a fine feature sulla base dell'esito osservato (ratifica); non dichiararla affatto e lasciare che il lettore deduca (lascerebbe su `main` la frase della `008a` — *il file è leggibile, non pubblicabile* — senza nulla che la ritiri, cioè un'affermazione falsa in un README).
- **Che cosa il criterio non copre, dichiarato qui**: la comprensibilità del testo. Le cinque condizioni sono verificabili; che una frase si capisca non lo è, e resta interamente alla revisione in contesto pulito.
- **Riferimento**: spec.md, `N8`.

## Che cosa questa Fase 0 non ha dovuto ricercare, e perché va detto

**Nessuna ricognizione su come si scrive una dashboard.** Il registro, la lunghezza, il tono non sono stati cercati fuori dal progetto: discendono dal criterio di accettazione che la constitution fissa in apertura — reggere la presentazione a un board reale — e dal lettore che la spec dichiara, un decisore che non ha letto alcun documento del repository.

**Nessuna ricognizione sulle capacità di Power BI.** Questa feature aggiunge caselle di testo e forme, che è la funzione più elementare dello strumento. L'unica affermazione sullo strumento che il piano contiene è che una pagina-tooltip è una pagina, ed è una proprietà dichiarata dalla `008a` §3.1, non una constatazione nuova.

**È la prima Fase 0 del progetto in cui il materiale di ricerca è interamente interno.** Tutte le affermazioni che andranno a schermo esistono già, per esteso e con la propria ancora, in sette documenti sotto `docs/`. Il lavoro non è scoprirle: è ridurle senza che la riduzione le renda false — che è il rischio che `plan.md` registra per primo e la ragione per cui la revisione riceve un metro diverso dalla conformità.
