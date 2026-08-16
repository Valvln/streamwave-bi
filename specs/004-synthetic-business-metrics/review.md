# Revisione in contesto pulito — `docs/bq3_scenarios.md`

**Data della revisione**: 2026-08-16
**Data della trascrizione**: 2026-08-17
**Oggetto**: `docs/bq3_scenarios.md` alla versione del commit **`b5e2b0e`** — sha256 del contenuto letto: `4f980707c3308d5a82679e4d9fcc357eed82252f31b10a69a38ea6a374c0c624`

```bash
git show b5e2b0e:docs/bq3_scenarios.md
```

Il documento è stato **riscritto in profondità** per chiudere questi rilievi: chi legge il verbale contro la versione attuale non ritrova i passaggi citati. Vanno confrontati con la versione qui sopra, che è quella che il revisore ha letto.

## Come è stata condotta, e la sua debolezza

**Natura**: contesto pulito. La revisione è stata affidata a una sessione separata che ha ricevuto **un solo file** — una copia del documento in una cartella isolata — con il vincolo esplicito di non aprire nient'altro: niente `specs/`, niente artefatti, niente `git`, niente rete. Il revisore non ha partecipato alla stesura e non ha potuto chiedere chiarimenti.

Questa forma è **più stretta** di una sessione umana a cui si incolla il testo: una sessione vuota vede ciò che le si dà, ma potrebbe raggiungere il resto; questa non aveva modo di sapere che il resto esistesse. La sezione «Che cosa non ho potuto valutare», in coda al verbale, è scritta dal revisore stesso e dichiara i limiti che ne discendono.

**La debolezza, dichiarata perché non è eliminabile.** Questo verbale è stato trascritto **dopo** la chiusura dei rilievi, e a trascriverlo è stata **la sessione esecutiva, cioè la parte revisionata**. È un'omissione di processo: il verbale andava scritto e committato quando la revisione è tornata, prima di toccare il documento, come è avvenuto per la `001`, la `002` e la `003`. Non è stato fatto, e recuperarlo dopo vale meno dell'originale per una ragione precisa: chi legge deve fidarsi che chi trascrive non abbia ammorbidito nulla, e questo progetto altrove rifiuta esattamente questo tipo di garanzia.

Ciò che si può offrire in compenso è l'ancoraggio dell'oggetto — commit e impronta del contenuto letto — che i tre verbali precedenti non hanno: dichiarano quale file, non quale versione.

**Il testo fra le due righe orizzontali qui sotto è la trascrizione integrale dell'output del revisore**, senza tagli, senza correzioni e senza modifiche ai livelli di intestazione. Include i punti in cui il revisore sbaglia — vedi R5 — perché un verbale corretto da chi è stato revisionato non è più un verbale.

---

# Verbale di revisione — «Gli scenari di adozione del tier premium»

## Valutazione complessiva

Il documento è costruito con cura e dichiara più di quanto quasi ogni pagina analoga dichiari: sa che il numero è debole, lo dice, e prova a rendere ispezionabile il proprio metodo. Regge come racconto onesto di una derivazione; **non regge come garanzia**, ed è esattamente questo che promette nel punto in cui alza di più la voce. La debolezza principale è che l'unico presidio offerto in sostituzione della fiducia — la precedenza temporale dei fattori sul benchmark, provata dalla cronologia dei commit — dimostra qualcosa di diverso da ciò che il documento afferma, mentre l'apparato di rigore più visibile (determinismo, aritmetica decimale, arrotondamento dichiarato) è dispiegato attorno a una moltiplicazione di due numeri e non tocca nessuna delle assunzioni che portano il peso. La seconda debolezza, meno visibile, è che la banda 0,50–1,50 dichiara di misurare la fiducia nel trasferimento del benchmark ma non può rappresentare il caso in cui quel trasferimento fallisce: il pessimismo massimo esprimibile è «metà di Netflix». Ne esce un documento la cui trasparenza svolge il lavoro persuasivo che le prove non svolgono — e il lettore che gli dà cinque minuti porta via `30%` e `1,20 €`, cioè la parte che il documento stesso prevede verrà usata male.

---

## Rilievi

### R1 — La cronologia dei commit non prova ciò che il documento le fa provare

> «È il punto di metodo di questa feature, e l'unico che il documento chiede di verificare invece che di credere.»
> «La garanzia non è quindi un'affermazione, è la cronologia dei commit»
> Titolo: «I fattori sono stati fissati prima di conoscere il benchmark»

Il titolo asserisce un fatto sullo **stato di conoscenza dell'analista**. La cronologia dei commit stabilisce un fatto sullo **stato di un file**: che al primo commit la chiave del benchmark non c'era. Le due cose non coincidono. Il valore adottato è un dato pubblico dal 2018, il primo risultato di una ricerca ovvia sull'argomento; nulla nella storia di quel file esclude che l'analista lo conoscesse — o lo avesse già letto — mentre scriveva `0.50` e `1.50`. L'assenza deliberata del campo segnaposto, argomentata bene, chiude solo la variante più grossolana del problema (riempire un buco predisposto), non il problema.

Va aggiunto che la cronologia git è un artefatto riscrivibile dallo stesso autore che la produce (`rebase`, `amend`, date d'autore arbitrarie) e che qui autore dei commit e autore della rivendicazione sono la stessa persona. Un lettore esterno che esegue `git log --follow` osserva un ordine dichiarato da chi ha interesse a quell'ordine.

**Perché conta**: è l'unica cosa che il documento chiede di *verificare* invece che di *credere*. Se quella verifica non stabilisce l'enunciato che le sta sopra, l'intera pagina torna a essere una richiesta di fiducia, e va letta come tale.

**Che cosa lo chiuderebbe**: riformulare la rivendicazione a ciò che l'evidenza sostiene («i fattori esistono nel repository in un commit anteriore all'ingresso del valore, e non sono stati modificati dopo»), oppure ancorare la precedenza a un riferimento temporale non riscrivibile dall'autore.

---

### R2 — La banda non può esprimere l'incertezza che dichiara di esprimere

> «Dichiara quanta fiducia l'analista ripone nel trasferimento del benchmark — nient'altro.»

Se questo è il contenuto della banda, allora la banda dichiara che, nello scenario peggiore concepito, il trasferimento vale ancora metà. Ma il §3 sostiene che il segno netto delle divergenze **non è noto**, che una divergenza è «di definizione» (composizione contro flusso: grandezze diverse) e che un'altra è ignota «nemmeno in linea di principio». L'insieme di queste ammissioni include il caso in cui l'analogia semplicemente non tenga — un verticale musicale a 4 € che raccoglie il 3% invece del 15%. Quel caso non ha alcuna rappresentazione nei tre scenari.

Il risultato è un'asimmetria a senso unico: il documento riconosce l'incertezza in prosa e la neutralizza nella struttura numerica, perché il pavimento della banda è fissato a `0,5 ×` benchmark e non a «il benchmark non si trasferisce».

Nota collaterale sulla stessa riga: la banda è definita «**moltiplicativa e relativa**», ma i fattori `0.50`/`1.50` la rendono aritmeticamente **simmetrica** (15/30/45, ampiezza uguale in su e in giù). La distinzione rivendicata non compie alcun lavoro con questi valori; una banda genuinamente moltiplicativa userebbe fattori reciproci. È un'etichetta che suggerisce una scelta metodologica che non c'è.

**Perché conta**: chi legge la tabella del §5 crede di vedere il ventaglio dei mondi possibili. Vede il ventaglio dei mondi in cui il benchmark si trasferisce almeno a metà.

---

### R3 — «Rifare ogni numero» non è ciò che il lettore può fare, ed è l'ultima cosa che legge

> «Chi clona il repository può quindi rifare ogni numero di questa pagina.»

Il lettore può **ricalcolare** i numeri derivati: `30 × 0,5`, `15 × 4,00`. Non può rifare l'unico numero che porta il peso. Il `30` non si ricalcola: si rilegge da un file JSON curato a mano nello stesso repository, cioè si riprende per buono. La verifica genuinamente esterna — che quel `30` corrisponda a ciò che Parks Associates ha pubblicato — dipende interamente da un URL di comunicato stampa del 2018 e da nient'altro: nessuna copia archiviata, nessuno snapshot, nessun identificativo permanente. Il documento stesso ammette che «il comunicato non nomina lo studio né la numerosità campionaria», quindi anche seguendo il link il lettore verifica solo che un comunicato promozionale riporti quella cifra, non che la cifra sia stata misurata in un modo che lui possa giudicare.

Aggravante di posizione: questa frase è al §9, ultima sezione, ed è la promessa più forte della pagina. Chi smette di leggere lì porta via «riproducibile da chiunque». Il documento non ha detto il falso, ma ha lasciato che «rifare» significasse, nel punto di massima memorabilità, ciò che non significa.

**Che cosa lo chiuderebbe**: distinguere in quella frase riesecuzione da verifica, e dichiarare che il benchmark è congelato e non ricalcolabile — cosa che il §2 dice, ma cinque sezioni prima e con altro scopo.

---

### R4 — «La più grande»: superlativo non ancorato, e due divergenze su cinque escono di scena

> «Le due<!--#--> divergenze di cui si conosce la direzione puntano in verso opposto, e la terza — la più grande — non ha un verso noto nemmeno in linea di principio.»

Tre problemi distinti nella stessa frase.

**(a)** «la più grande» è una graduatoria costruita su fatti misurati, senza ancora e senza alcun valore che la sostenga. Nessuna delle cinque divergenze è quantificata in nessun punto del documento: non c'è modo di sapere che quella sull'attributo di servizio sia più grande di quella sull'accumulo pluriennale. Il documento enuncia il principio contrario tre sezioni più avanti — «un confronto costruito su valori misurati **è esso stesso un valore misurato**» — e lo viola qui. È anche il tipo di affermazione che i marcatori non intercettano: non è un numerale, quindi nessun controllo la vede.

**(b)** Il ragionamento sul segno netto usa **tre** divergenze su cinque. Escono di scena, senza una parola, la prima («composizione contro flusso: sono grandezze diverse») e la quinta (numerosità campionaria ignota). La prima è quella che il documento stesso qualifica come differenza *di definizione*, cioè la più radicale: non un bias di cui stimare il verso, ma il fatto che il benchmark non misura la grandezza richiesta. Ometterla dal bilancio dei segni fa apparire il quadro più governato di quanto sia.

**(c)** «la terza» è ambiguo per posizione: dopo «le due divergenze», l'ordinale può leggersi come terza *della tabella* o come *una terza oltre le due citate*. Coincidono solo per accidente dell'ordine di riga.

**Perché conta**: il §3 è la sezione che il documento indica come prerequisito per leggere i valori del §5. È anche la sezione in cui l'autore calcola a mente, ed è lì che il difetto si concentra.

---

### R5 — Il verso della divergenza di prezzo è asserito senza argomento, e la lettura economica ovvia lo inverte

> «il differenziale di prezzo osservato era superiore a quello di A4 | spinge il valore **in basso**»

Se il salto di prezzo verso il tier alto osservato da Parks Associates era **maggiore** dei 4,00 € di StreamWave, la lettura economica immediata è che quel 30% è stato raggiunto **nonostante** un ostacolo di prezzo più alto: a parità d'altro, un salto più economico produce più adozioni, quindi il benchmark **sottostima** e la divergenza spinge il valore **in alto**. Il documento afferma il contrario in una casella di tabella, senza una riga di motivazione.

Le conseguenze non sono cosmetiche. Questa è **l'unica** divergenza dichiarata in direzione discendente. Se il suo verso è invertito, entrambe le divergenze a direzione nota puntano verso l'alto, il valore centrale è distorto in eccesso lungo tutti i canali identificati, e la frase «puntano in verso opposto» — con la rassicurazione implicita di compensazione che porta — cade.

Aggravante: il valore del differenziale osservato **non viene mai pubblicato**, mentre il confronto costruito su di esso sì. Il documento lascia intendere di possederlo («Il primo commit contiene i fattori, la loro ragione e il differenziale di prezzo»). Un confronto pubblicato il cui operando resta nel file è precisamente la categoria che il §5 dichiara inammissibile.

**Che cosa lo chiuderebbe**: pubblicare il differenziale osservato con la sua ancora, e argomentare il verso in una riga.

---

### R6 — Lo stesso numero è dichiarato non-misura al §4 e valore misurato al §5

> §4: «**L'ampiezza della banda non misura nulla.** Non è una varianza osservata, non è un intervallo di confidenza, non ha interpretazione probabilistica.»
> §5: «l'ampiezza vale 30<!--@BQ3.band.spread_pp--> punti percentuali», giustificata perché «un confronto costruito su valori misurati **è esso stesso un valore misurato**»

Il documento dice della medesima grandezza che non misura nulla e che è un valore misurato, a una sezione di distanza, e usa la seconda affermazione per motivare l'ancoraggio. Le due si possono conciliare solo distinguendo due assi che il documento tiene sovrapposti — «prodotto da un artefatto tracciabile» contro «misura qualcosa del mondo» — ma quella distinzione non è mai fatta, ed è la distinzione su cui poggia l'intera grammatica dei marcatori: `@` da una parte, `#` dall'altra. Si nota anche che `cinque<!--#--> condizioni` porta il marcatore di non-misura mentre `30<!--@BQ3.band.spread_pp-->`, che per stessa ammissione del §4 non misura nulla, porta un'ancora.

**Perché conta**: la chiave di lettura di ogni numero della pagina è quella coppia di marcatori. Se il documento non la applica coerentemente a se stesso, il lettore non sa che cosa gli stia dicendo un'ancora.

Piccolo effetto collaterale nella stessa sezione: nel §5 il numero `30` compare due volte con due significati diversi (valore centrale e ampiezza della banda), che sono numericamente uguali solo per effetto della scelta `0,5`/`1,5`. È un'occasione di confusione gratuita in poche righe.

---

### R7 — Tre semantiche temporali per lo stesso numero, e una frase falsa nella sezione che dovrebbe impedire l'abuso

Il documento attribuisce al medesimo `30` tre significati temporali distinti, in tre sezioni, senza mai riconciliarli:

> §3: «È una composizione della base a un istante.»
> §3: «quale quota di una base preesistente adotti il tier premium entro 12<!--#--> mesi dal lancio»
> §8: «l'uplift è un valore **a regime**, non un ricavo cumulato sui 12<!--#--> mesi dell'orizzonte»

Uno stock istantaneo, un flusso cumulato su dodici mesi, un livello di regime mensile non sono la stessa grandezza, e la scelta fra le tre cambia il numero che qualcuno userà. Se il 30% è l'adozione *raggiunta al dodicesimo mese*, allora 1,20 € è il livello a fine periodo e non il livello medio del periodo; se è un regime, non si capisce che ruolo abbia l'orizzonte di 12 mesi. Il §8 sceglie la terza lettura in una riga, dopo che le prime due sono state stabilite altrove, senza dire che sta scegliendo.

Peggio, la frase immediatamente successiva è **falsa come scritta**:

> «Le due<!--#--> grandezze coinciderebbero solo se nessuno disdicesse.»

Un valore mensile a regime e un ricavo cumulato su dodici mesi non coincidono **mai**, con o senza disdette: differiscono per un fattore di circa dodici. Ciò che l'autore intende — che il cumulato uguaglierebbe dodici volte il livello solo con churn nullo e adozione immediata — non è ciò che la frase dice. Un lettore che la prenda alla lettera conclude che, in assenza di disdette, 1,20 € *è* la grandezza annua, che è l'errore opposto a quello che la sezione vuole prevenire.

**Perché conta**: è l'unica sezione della pagina il cui scopo dichiarato è impedire un uso sbagliato, e contiene un enunciato che ne autorizza uno.

---

### R8 — L'età della fonte non compare fra le divergenze

La tabella del §2 data la pubblicazione al `2018-07-19` e l'accesso al `2026-08-16`. Otto anni. In quegli otto anni il mercato di riferimento ha visto comparire i tier con pubblicità, cambiare le politiche di condivisione degli account e muoversi ripetutamente i listini — tutti fattori che agiscono direttamente sulla composizione della base per tier, che è precisamente ciò che la fonte misura.

La tabella delle divergenze, che è costruita per essere **esaustiva** e per assegnare a ciascuna voce un verso, non contiene questa riga. Il §3.1 la sfiora («su un mercato e in un periodo che non sono quelli di StreamWave») e passa oltre, e il divario temporale non compare mai come quantità in nessun punto della pagina.

**Perché conta**: in una tabella che deve la propria credibilità all'esaustività, un'assenza vale quanto un errore — e questa è l'obiezione che a un lettore esterno viene per prima. Trovarla non elencata mette in dubbio che l'elenco sia l'inventario che dichiara di essere.

---

### R9 — «Due cifre significative» è asserito, non argomentato, ed è l'unica ipotesi di precisione che si propaga ovunque

> «Il benchmark è noto a due<!--#--> cifre significative, e nessun valore che ne discende può esserne noto a più.»

Il `30%` proviene dal **titolo di un comunicato stampa**. Un `30` tondo in quella posizione è quasi certamente arrotondato, e il fatto che lo zero finale sia significativo non è deducibile da nulla di ciò che il documento mostra: potrebbe essere una cifra significativa sola, e la fonte — per ammissione del documento stesso — non nomina lo studio né la numerosità che permetterebbero di deciderlo. L'affermazione è presentata come constatazione ed è un'assunzione.

Il contrasto con il resto del §7 è netto. La sezione dispiega aritmetica decimale esatta, modalità di arrotondamento dichiarata, e l'osservazione che «sul confine, la virgola mobile e la modalità predefinita sbagliano ciascuna un valore diverso»; il §6 aggiunge assenza di generatori casuali, assenza di letture dell'orologio, identità bit a bit fra due esecuzioni. Tutto questo presidia una catena di calcolo che consiste in due moltiplicazioni per costanti tonde, e sarebbe pienamente eseguibile a mente. Nessuno di quei presidi tocca l'unica ipotesi — la precisione dell'input — da cui dipende la precisione di ogni cifra pubblicata.

**Perché conta**: la densità di rigore su ciò che non può sbagliare produce, in chi legge, fiducia trasferibile a ciò che può. È rigore ben speso in sé e mal collocato retoricamente, e in un documento che chiede di essere giudicato sul metodo, la collocazione è metodo.

---

### R10 — «La migliore disponibile» si autocertifica

> «Un rigetto non registrato renderebbe non verificabile l'affermazione che la fonte adottata fosse la migliore disponibile, e quella affermazione è parte di ciò che si sta chiedendo di credere.»

Il registro dei rigetti è compilato dalla stessa persona che sceglie, nello stesso file che congela la scelta, e contiene per costruzione solo le fonti che quella persona ha **trovato** e ha **deciso di annotare**. Non può rendere verificabile una superlatività («la migliore disponibile»), perché lo spazio delle fonti mai incontrate non lascia traccia nel registro. La frase ha la forma di una condizione di verificabilità e ne fornisce solo la metà controllabile: rende ispezionabile il perché di ciò che è stato scartato, non l'estensione della ricerca.

C'è poi il fatto che «la migliore disponibile» è una graduatoria su fonti, cioè un'affermazione derivata, formulata en passant e senza criterio dichiarato: migliore per che cosa — vicinanza al caso d'uso, ispezionabilità del metodo, attualità?

**Che cosa lo chiuderebbe**: dichiarare il criterio di preferenza e il perimetro della ricerca, e ridurre la rivendicazione a ciò che il registro sostiene («la migliore fra quelle esaminate, secondo il criterio X»).

---

### R11 — «Non è scalabile» descrive un'omissione come se fosse una proprietà

> «**`BQ3-K2` è euro per utente al mese, e non è scalabile.** Nessuna base utenti viene quantificata in questo progetto, e l'artefatto non offre alcuna chiave con cui moltiplicare l'uplift. È deliberato»

Il numero **è** scalabile: è una grandezza per utente al mese, e chiunque disponga di una qualunque stima di utenti la moltiplicherà in dieci secondi. Ciò che il documento può dire è che *lui* non fornisce il moltiplicatore. La forma «non è scalabile» attribuisce al valore una proprietà protettiva che ha invece la pagina, e non la trattiene: nulla in questa scelta impedisce l'operazione che la scelta dice di scoraggiare, in una sala riunioni dove un numero di abbonati è a disposizione di tutti.

Il paragrafo si guadagna così il credito della rinuncia deliberata mentre l'abuso resta interamente disponibile — e resta disponibile in un modo che il documento non presidia, perché a valle nessuno saprà che quel prodotto non doveva essere fatto.

---

### R12 — La regola che ammette il benchmark non riceve lo stesso trattamento che il documento pretende per i fattori

> «È un benchmark pubblico di settore, ammesso come quarta<!--#--> fonte dati dalla constitution a cinque<!--#--> condizioni»

Il documento insegna al lettore, con notevole insistenza al §4, che l'ordine fra la regola e il caso conta: un parametro scelto dopo aver visto il valore non vale come un parametro scelto prima. Applicando quello stesso standard a questa frase, il lettore dovrebbe poter sapere se la constitution ammetteva la quarta fonte **prima** che questa feature ne avesse bisogno, o se è stata emendata perché ne aveva bisogno. Il documento non lo dice, e la cosa non è recuperabile dalla pagina.

**Perché conta**: la formulazione «ammesso dalla constitution» presenta un vincolo esterno soddisfatto. Se la regola e il suo primo uso sono contemporanei, è un vincolo interno costruito attorno al caso, e la parola «ammesso» sta facendo un lavoro che non le spetta. Una riga — data e versione dell'emendamento, come al §4 si dà il comando `git log` — chiuderebbe il punto.

---

### R13 — «Operazione priva di oggetto»: una scelta di perimetro promossa a impossibilità

> «Senza una numerosità, la generazione stocastica non è una scelta scartata: è un'operazione priva di oggetto.»

L'assenza di una base utenti non è un fatto del mondo: è, per esplicita ammissione del documento, «una decisione presa nella revisione della `001`», cioè una scelta dello stesso progetto. Il ragionamento è quindi circolare in una forma precisa: si decide di non quantificare N, poi si usa l'assenza di N per dimostrare che ciò che la roadmap prescriveva era logicamente impossibile. La formula «non è una scelta scartata» toglie al lettore proprio la cosa che gli servirebbe per giudicare — che una scelta c'è stata, e che è stata fatta a monte.

Va detto che le altre due ragioni del §6 (nessun consumatore legge righe; un campionamento fabbricherebbe dispersione apparente) sono buone e bastano da sole; e che dichiarare lo scostamento dalla roadmap invece di assorbirlo è la cosa giusta, fatta bene. È la terza ragione — quella che il documento presenta come la più forte — a essere la più debole.

Nella stessa sezione: «Le ragioni sono tre<!--#-->, in ordine crescente di forza» asserisce una graduatoria fra argomenti senza alcun criterio, in un documento che al §5 dichiara le graduatorie bisognose di fondamento.

---

### R14 — Ciò che si porta via in cinque minuti non è ciò che il documento vuole trasmettere

Le due tabelle del §5 sono, di gran lunga, l'oggetto più estraibile della pagina: pulite, brevi, prive di qualsiasi cautela **al loro interno**, con una riga «centrale» che si copia da sola. Le riserve che le governano stanno in parte prima (§4, bene: la banda non misura nulla) e in parte dopo (§8, tre sezioni più in là). Il documento prevede con precisione ciò che accadrà —

> «Un valore singolo preso da questa tabella — tipicamente quello centrale, perché sta meglio in una dashboard — comunicherebbe una certezza che il dato non ha, ed è la violazione più facile da commettere e la più difficile da vedere a valle»

— e non fa nulla di strutturale per impedirlo. Prevedere un abuso e poi formattare il contenuto nel modo che lo agevola è un'asimmetria fra ciò che il documento dice di volere e ciò che il documento rende facile.

Collegato, e conclusivo. Il documento chiude offrendo la propria trasparenza come rimedio:

> «tre<!--#--> questioni su cui non esiste presidio automatico, e su cui questo documento offre soltanto la propria trasparenza»

L'autoconsapevolezza è reale e va riconosciuta, ma non estingue il problema che nomina. L'effetto cumulato di una pagina in cui ogni sezione contiene un'ammissione — e in cui più di una debolezza viene convertita in virtù nella frase successiva («curato a mano, versionato, e **mai riscritto da alcuno script**»; «la rotondità è la ragione e non la sua assenza») — è che il lettore chiude con un grado di fiducia sproporzionato rispetto alle prove che gli sono state effettivamente esibite, e proporzionato invece al candore con cui gli è stato detto che non ce ne sono. Un `30%` di otto anni fa, preso da un comunicato promozionale che non nomina il proprio studio, applicato a una grandezza diversa da quella misurata, su un mercato diverso, per un prodotto che non esiste: questa frase non compare mai nel documento, e tutte le sue componenti sì.

---

## Ciò che funziona

- **§3 nel suo impianto**: separare esplicitamente «che cosa la fonte misura» da «che cosa serve al KPI», e tabulare le divergenze con un verso, è la cosa migliore della pagina. È anche il motivo per cui le omissioni della tabella (R4, R8) pesano tanto: lo strumento è giusto ed è stato usato a metà.
- **«L'ancoraggio a una fonte citabile rende il parametro verificabile, non vero per StreamWave»** è la distinzione centrale del documento, formulata con esattezza e senza scappatoie, e la frase che la accompagna («un numero con una citazione sembra più solido... ma la distanza fra quella fonte e questo caso resta intera») non attenua: è una delle poche in cui l'ammissione non viene riequilibrata.
- **La difesa del fattore tondo** («un fattore come `0,37` comunicherebbe a chi legge che il valore viene da un calcolo, e non ne viene») è un argomento vero e poco ovvio, e sopravvive a R1: qualunque cosa si pensi della precedenza temporale, la scelta di *non* mascherare una stipulazione da stima è corretta.
- **Il §5 sul rapporto**: dire che il rapporto 3 «non dipende dal benchmark» e «resterebbe lo stesso qualunque valore fosse stato adottato» è un'osservazione che disinnesca un'illusione reale, e ancorarla invece di lasciarla in prosa è coerente con il principio dichiarato.
- **Lo scostamento dalla roadmap dichiarato invece che assorbito** (§6.1), con l'argomento sul seed che «dichiara il falso» dove non c'è estrazione. È il tipo di annotazione che quasi nessun documento di questo genere si prende la briga di scrivere.
- **Il §8 nel complesso** dice cose corrette e scomode — nessun intervallo di confidenza, confidenza bassa non innalzata dalla citazione, nessuna verifica automatica guarda il mondo — con l'eccezione dei due punti rilevati in R7 e R11.

---

## Che cosa non ho potuto valutare

- **Nessun file esterno.** Non ho aperto `bq3_tier_upgrade.json`, gli script, il quickstart, il business case, la constitution, le convenzioni di marcatura né alcuna spec. Tutto ciò che il documento attribuisce a quei file — il registro dei rigetti, le cinque divergenze «per esteso», le assunzioni A4/A5/A6, le condizioni della constitution, la regola di precisione «dichiarata per esteso fra le convenzioni» — è per me asserzione non verificata. Diversi rilievi (R5, R10, R12) potrebbero essere già chiusi *in quei file*: resterebbero comunque rilievi su **questa pagina**, che è ciò che il lettore esterno legge.
- **Nessuna cronologia git.** Non ho eseguito `git log --follow` né ispezionato alcun commit. R1 è un rilievo sulla forza logica della rivendicazione, non sulla sua veridicità: non affermo che i fattori siano stati scelti dopo.
- **La fonte esterna.** Non ho aperto il comunicato PR Newswire né verificato che riporti il 30%, che l'URL sia vivo, o che il titolo sia trascritto correttamente. R9 poggia su ciò che il documento stesso dichiara della fonte, non su un'ispezione.
- **Il verso della divergenza di prezzo (R5).** Senza il valore del differenziale osservato e senza la motivazione — nessuno dei due è nel documento — non posso stabilire quale delle due letture sia quella intesa. Segnalo che il testo non permette a chi legge di deciderlo, e che le due letture portano a conclusioni opposte sul valore centrale.
- **Il comportamento reale dei controlli.** Che `check_audit_coherence.py` faccia ciò che il §9 dice, che la severità stretta sia effettivamente attiva su questo documento, e che i marcatori siano coerenti con la grammatica dichiarata altrove, sono cose che non ho potuto verificare. Ho usato i marcatori solo come informazione interna al testo, ed è su quella base che nasce R6.

---

## Chiusura dei rilievi

**Questa sezione non fa parte del verbale.** È scritta dalla sessione esecutiva il 2026-08-17 e registra come ciascun rilievo è stato chiuso. La distinzione che riporta è quella che conta per chi verifica: un rilievo chiuso **risolvendo** il difetto vale diversamente da uno chiuso **indebolendo l'affermazione** che lo aveva attirato — la seconda è una chiusura legittima, ma il documento perde una rivendicazione invece di guadagnare una proprietà.

Due rilievi hanno richiesto decisioni che non spettavano a chi esegue e sono state prese da Valerio: la rimozione della divergenza di prezzo (R5) e il cambio dei fattori della banda (R2).

| # | Come è stato chiuso | Dove |
|---|---|---|
| R1 | **indebolendo l'affermazione** — il documento dichiara ora che la history prova lo stato del file e non lo stato di conoscenza di chi scrive, e che è riscrivibile da chi la produce. Il meccanismo non è migliorabile: la rivendicazione è stata portata a ciò che l'evidenza sostiene | §4, `bq3_band_fixed_before` |
| R2 (simmetria) | **risolvendolo** — i fattori sono ora reciproci, `0.50` e `2.00`, e il loro prodotto vale l'unità. La banda è simmetrica in termini relativi, che è ciò che D2 prescriveva. *Decisione di Valerio* | file dei parametri, §4, D2, T6 |
| R2 (pavimento) | **dichiarandolo** — nessuna banda moltiplicativa può rappresentare il fallimento del trasferimento. Non è correggibile dentro questa forma, ed è ora una sezione propria | §4, «Che cosa la banda non può rappresentare» |
| R3 | **indebolendo l'affermazione** — §9 distingue ora *ricalcolare* da *verificare*, e dichiara che il benchmark non si rifà e che non esiste copia archiviata | §9 |
| R4 (a) | **indebolendo l'affermazione** — il superlativo è dichiarato come giudizio di chi scrive, non come constatazione, con la nota che nessuna divergenza è quantificata | §3 |
| R4 (b) | **risolvendolo** — il bilancio dei segni copre ora tutte e cinque le divergenze e dichiara perché quattro non hanno verso | §3 |
| R4 (c) | **risolvendolo** — l'elenco è numerato e l'ordinale non è più ambiguo | §3 |
| R5 (verso) | **rilievo non accolto nel merito, difetto reale chiuso risolvendolo.** La convenzione usata era coerente — *in basso* significa che la fonte sta sotto il vero — ma non era dichiarata, e un lettore competente l'ha letta al contrario. La convenzione è ora esplicita prima dell'elenco | §3 |
| R5 (operando) | **risolvendolo per rimozione** — la divergenza di prezzo è stata eliminata: il differenziale non è dichiarato dalla fonte citata e non era ancorato da nessuna parte. Era l'unica a far apparire il valore conservativo, e la rimozione è dichiarata come non neutrale. *Decisione di Valerio* | §3, `bq3_benchmark_measurement_gap` |
| R6 | **risolvendolo** — il documento distingue ora *tracciabile* da *misura qualcosa del mondo*: «i marcatori dichiarano l'origine di un numero, non la sua verità». L'effetto collaterale sul doppio `30` è rientrato da sé con il cambio dei fattori | §4 |
| R7 (frase falsa) | **risolvendolo** — l'enunciato era falso e non ambiguo. Riscritto: un livello mensile e un cumulato non coincidono mai | §8 |
| R7 (semantica) | **risolvendolo** — §8 dichiara ora quale delle tre grandezze i valori rappresentano, invece di lasciarne tre in circolazione | §8 |
| R8 | **risolvendolo** — l'età della fonte è entrata come quarta divergenza, con verso non determinabile | §3 |
| R9 | **indebolendo l'affermazione** — le due cifre significative sono dichiarate come assunzione, con la ragione e la conseguenza se fosse una sola. Aggiunta l'osservazione che il rigore è dispiegato dove non può sbagliare | §7, `bq3_benchmark_precision_note` |
| R10 | **indebolendo l'affermazione** — ridotta a «la migliore fra quelle esaminate», con il criterio di preferenza dichiarato | §2 |
| R11 | **indebolendo l'affermazione** — «non è scalabile» è diventato «questa pagina non fornisce il moltiplicatore», ed è dichiarato che non è un presidio ma una rinuncia | §8 |
| R12 | **aggiungendo un fatto** — è scritto che la constitution è stata emendata per questa feature e che regola e primo uso sono contemporanei | §2 |
| R13 | **indebolendo l'affermazione** — la terza ragione è dichiarata più debole di come suona, e le prime due sono indicate come sufficienti da sole | §6 |
| R14 | **parzialmente** — la cautela sull'effetto cumulativo è ora in cima e non in fondo, e le tabelle portano il vincolo al proprio interno. La struttura resta però estraibile, e il rilievo non è chiudibile del tutto in un documento che deve pubblicare quei valori | §5, preambolo |

**Nessun rilievo è stato respinto.** R5 è l'unico in cui il difetto dichiarato non c'era; il difetto reale che l'ha prodotto — una convenzione non dichiarata — è stato chiuso, e l'aggravante su cui il rilievo insisteva ha portato alla rimozione di un'intera divergenza.
