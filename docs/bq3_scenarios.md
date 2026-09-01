# Gli scenari di adozione del tier premium

Come i parametri della terza domanda di business passano da un valore osservato su un operatore terzo a tre<!--#--> scenari, e che cosa quei numeri non dicono.

Questo è il documento in cui si contesta il metodo. Il numero che il board legge sta nel [business case](business_case.md); qui c'è come è stato costruito, quali sono le sue debolezze note, e dove si romperebbe. È scritto perché chi non si fida possa avere torto per una ragione precisa invece che per diffidenza generica.

**Una cautela sull'effetto complessivo, in cima e non in fondo.** Questa pagina dichiara molti limiti. Dichiararli non li elimina, e un documento che ne ammette molti può risultare più persuasivo di quanto meriti proprio per questo. Il riassunto onesto di ciò che segue è: *una quota rilevata otto<!--#--> anni fa, presa da un comunicato stampa che non nomina il proprio studio né la propria numerosità campionaria, applicata a una grandezza diversa da quella misurata, su un mercato diverso, per un prodotto che non esiste.* Tutte le componenti di questa frase sono argomentate sotto. La frase intera va tenuta insieme.

---

## 1. Che cosa questa feature produce

Due<!--#--> parametri, che alimentano `BQ3-K1` — il tasso di adozione del tier premium — e `BQ3-K2`, la variazione del ricavo medio per utente. La feature **non calcola i due<!--#--> KPI**: quelli appartengono alla `007`, che legge questi valori e non li ricalcola.

Non produce alcun dataset. Non esiste un file di righe generate, e non è una semplificazione: è una conseguenza, spiegata in §6.

Restano fuori dal perimetro, ciascuno per una ragione dichiarata altrove: il churn (FR-018 della `001`), l'engagement — nessun KPI del framework lo consuma — la determinazione dei prezzi (A4, e `FR-017a` della `001`), e la quantificazione della base utenti, che la revisione della `001` ha deciso di non fare.

## 2. Il parametro viene da fuori, e si può verificare

Il valore centrale non è una scelta dell'analista. È un benchmark pubblico di settore, ammesso come quarta<!--#--> fonte dati dalla constitution a cinque<!--#--> condizioni: citazione puntuale, valore congelato in un file versionato, nessuna chiamata di rete durante l'esecuzione, assunzione di trasferimento dichiarata, nessuna promozione del livello di confidenza.

**Va detto che quella regola e il suo primo uso sono contemporanei.** La constitution è stata emendata il 2026-08-16 per ammettere i benchmark come fonte, e questa feature è la ragione dell'emendamento e il suo primo caso d'uso. «Ammesso dalla constitution» non descrive quindi un vincolo esterno preesistente che il lavoro ha incontrato e soddisfatto: descrive una regola scritta sapendo quale sarebbe stato il caso. La regola resta più stringente di ciò che sostituiva — prima il parametro sarebbe stato una scelta dell'analista senza alcuna condizione — ma chi legge deve poter pesare la differenza da sé.

| | |
|---|---|
| **Organizzazione** | Parks Associates |
| **Titolo** | `Parks Associates: 30% of Netflix Subscribers in Premium Service Tier` |
| **Pubblicazione** | 2018-07-19 |
| **Riferimento** | [comunicato su PR Newswire](https://www.prnewswire.com/news-releases/parks-associates-30-of-netflix-subscribers-in-premium-service-tier-300683486.html) |
| **Accesso** | 2026-08-16 |

Il valore adottato è 30<!--@BQ3.adoption.base--> punti percentuali della base abbonati. Il file che lo congela è [`data/benchmarks/bq3_tier_upgrade.json`](../data/benchmarks/bq3_tier_upgrade.json), che è curato a mano, versionato, e **mai riscritto da alcuno script**: la raccolta di un benchmark è un passaggio umano che nessuno rieseguirà, ed è precisamente la ragione per cui il suo esito va congelato invece che rifatto.

Lo stesso file porta il registro delle fonti valutate e **respinte**, ciascuna con il proprio motivo.

**Che cosa quel registro può certificare, e che cosa no.** Rende ispezionabile *perché* una fonte è stata scartata: chi non è d'accordo con un rigetto lo vede e lo contesta. Non può certificare che la fonte adottata fosse «la migliore disponibile», perché è compilato da chi sceglie e contiene solo le fonti che chi sceglie ha incontrato — lo spazio di quelle mai trovate non lascia traccia. La rivendicazione che questo documento può sostenere è più stretta: *la migliore fra quelle esaminate*, dove il criterio di preferenza è stato la solidità della citazione prima della vicinanza al caso d'uso. Quel criterio ha conseguenze visibili nel registro, dove una fonte più vicina per misura è stata respinta perché la sua citazione non reggeva.

## 3. Che cosa la fonte misura davvero

Non ciò per cui viene usata. Lo scarto è ampio e va conosciuto prima di leggere i valori di §5.

**Che cosa Parks Associates ha misurato**: la quota di abbonati Netflix che si trovava sul piano al prezzo più alto del listino, rilevata sui consumatori degli Stati Uniti e pubblicata nel 2018-07-19. È una composizione della base a un istante.

**Che cosa serve a `BQ3-K1`**: quale quota di una base preesistente adotti il tier premium entro 12<!--#--> mesi dal lancio di un verticale musicale che ancora non esiste.

**Convenzione sul verso**, da leggere prima dell'elenco perché senza di essa è ambiguo, e l'ambiguità cambia la conclusione: *verso l'alto* significa che il valore della fonte sta **sopra** ciò che sarebbe vero per StreamWave, cioè che è ottimista; *verso il basso* che vi sta **sotto**, cioè che è conservativo.

Le divergenze sono cinque<!--#-->, e il file dei parametri le riporta per esteso.

| | Divergenza | Verso |
|---|---|---|
| 1<!--#--> | composizione contro flusso: la fonte misura uno stato, il KPI chiede un movimento. Non è un bias di grado, è una differenza di grandezza | nessuno: non è di segno |
| 2<!--#--> | la composizione ha avuto anni per accumularsi e comprende chi ha sottoscritto il piano più caro all'iscrizione, senza essere mai salito da nulla | **in alto** |
| 3<!--#--> | ciò che distingue i piani della fonte è il numero di schermi e la qualità video, cioè un attributo di servizio; da noi è un verticale di contenuto | ignoto |
| 4<!--#--> | fra la rilevazione e l'uso corrono otto<!--#--> anni, in cui sono comparsi i piani con pubblicità, sono cambiate le politiche di condivisione degli account e i listini si sono mossi più volte | non determinabile qui |
| 5<!--#--> | il comunicato non nomina lo studio né la numerosità campionaria | nessuno: riguarda l'ispezionabilità |

Sulla terza: chi scrive ritiene che sia quella che pesa di più. **È un giudizio dichiarato come tale, non un fatto**: nessuna delle cinque<!--#--> è quantificata, e una graduatoria fra esse non è sostenuta da alcuna misura. Chi la legge come una constatazione le attribuisce un fondamento che non ha.

**Il segno netto non è noto, e non per compensazione.** Una sola<!--#--> divergenza ha un verso conosciuto — la seconda — e spinge il valore **in alto**. Le altre quattro<!--#--> non ne hanno uno: la prima perché è di definizione e non di grado, la terza e la quarta perché il verso è ignoto o non stabilibile con i dati di questo progetto, la quinta perché riguarda ciò che della fonte non si può ispezionare. Non ci sono quindi forze contrapposte che si bilanciano: c'è **una spinta nota verso l'alto e ignoto attorno**.

**Una divergenza rimossa, e la rimozione non è neutrale.** Una versione precedente di questo elenco dichiarava anche uno scarto di prezzo di verso opposto, costruito sul differenziale fra i tier della fonte. È stato rimosso il 2026-08-16 perché quel differenziale **non è dichiarato dal comunicato citato** e questo progetto non lo ha verificato presso alcuna fonte citabile: un confronto costruito su un operando che nessuno ha ancorato non è una divergenza dichiarata, è un'affermazione dell'analista. Era anche l'unica<!--#--> delle voci a far apparire il valore conservativo, quindi toglierla peggiora il quadro invece di migliorarlo — che è la ragione per cui la rimozione è scritta qui e non eseguita in silenzio.

### L'assunzione di trasferimento

Il valore descrive Netflix, su un mercato e in un periodo che non sono quelli di StreamWave. Assumere che si trasferisca è **un'assunzione dell'analista, non un fatto misurato su StreamWave**: è l'assunzione `A6` del business case.

L'ancoraggio a una fonte citabile rende il parametro **verificabile**, non **vero per StreamWave**. Sono due<!--#--> proprietà diverse, e confonderle è il modo più elegante di sbagliare qui: un numero con una citazione sembra più solido di un numero senza, e in un senso preciso lo è — si può contestare la fonte — ma la distanza fra quella fonte e questo caso resta intera.

## 4. Da un valore a tre scenari

I due<!--#--> fattori della banda sono **reciproci**: lo scenario pessimista vale il valore centrale diviso per il moltiplicatore, l'ottimista moltiplicato per lo stesso. Con `0.50`<!--@conventions.bq3_band_factor_low--> e `2.00`<!--@conventions.bq3_band_factor_high--> il prodotto dei due<!--#--> fattori vale esattamente l'unità, ed è quella la proprietà che conta: il rapporto fra centrale e pessimista e quello fra ottimista e centrale sono lo stesso numero. La banda è cioè simmetrica **in termini relativi**, che è quanto il metodo prescriveva.

**Che cosa c'era prima, e perché è cambiato.** I fattori erano `0,50` e `1,50`. Con quelli il rapporto fra centrale e pessimista valeva il doppio di quello fra ottimista e centrale: la banda era simmetrica in termini **assoluti** e si dichiarava relativa. Se ne è accorta una revisione condotta in contesto pulito, sul solo documento pubblicato. La correzione è stata applicata **dopo** che il benchmark era già stato adottato, il che è la mossa che §4.1 esiste per rendere visibile, ed è dichiarata per esteso nel file dei parametri: non guarda il valore adottato, sarebbe stata identica qualunque esso fosse, e allarga lo scenario ottimista invece di renderlo più comodo.

**L'ampiezza della banda non misura nulla.** Non è una varianza osservata, non è un intervallo di confidenza, non ha interpretazione probabilistica. Dichiara quanta fiducia l'analista ripone nel trasferimento del benchmark — nient'altro.

**Due<!--#--> sensi di «misurato», che questo documento tiene distinti** perché altrimenti la frase qui sopra contraddice le ancore di §5. Un numero può essere *tracciabile* — prodotto da un artefatto versionato, ricalcolabile da chiunque, e perciò ancorabile — senza per questo *misurare qualcosa del mondo*. L'ampiezza della banda è tracciabile e non misura nulla: discende per aritmetica esatta da una stipulazione, quindi porta un'ancora, ma ciò che l'ancora garantisce è che il numero non sia stato scritto a mano, non che esista là fuori una grandezza che valga quel tanto. **I marcatori di questa pagina dichiarano l'origine di un numero, non la sua verità.**

**Perché un moltiplicatore tondo.** Non esiste alcun criterio che lo ricavi da qualcosa: è una stipulazione. In questa condizione la rotondità è la ragione e non la sua assenza — un moltiplicatore come `1,73` comunicherebbe a chi legge che il valore viene da un calcolo, e non ne viene. Una stipulazione grossolana deve avere l'aspetto di una stipulazione grossolana.

### Che cosa la banda non può rappresentare

Nessuna banda moltiplicativa contiene il caso in cui **il trasferimento fallisce**, perché lo scenario pessimista resta proporzionale al benchmark e non raggiunge mai lo zero<!--#-->. Il pessimismo massimo esprimibile è *metà di quanto ha ottenuto chi il verticale musicale ce l'ha già*; l'ipotesi che l'analogia non valga affatto — che un verticale musicale a pagamento raccolga una quota trascurabile — **non ha alcuna rappresentazione nei tre<!--#--> scenari**.

È il limite più serio della struttura, ed è in tensione diretta con §3: se la prima divergenza dice che il benchmark non misura la grandezza richiesta, allora il caso «non si trasferisce» è fra quelli che restano aperti, e non compare nella tabella dei valori. Chi legge i tre<!--#--> scenari come il ventaglio dei mondi possibili sta leggendo il ventaglio dei mondi in cui il benchmark si trasferisce almeno in parte.

### I fattori precedono la ricognizione — che cosa lo prova e che cosa no

L'ampiezza della banda è **l'unico numero libero** dell'intera derivazione: tutto il resto discende dal benchmark. Sceglierla dopo aver visto il valore adottato la piegherebbe verso l'intervallo che sembra giusto, e nulla dentro un file distingue un fattore scelto prima da uno scelto dopo. La cronologia dei commit è ciò che il documento offre al posto della parola:

```bash
git log --follow data/benchmarks/bq3_tier_upgrade.json
```

Il primo commit contiene i fattori e la loro ragione, e **non contiene la chiave del benchmark**, nemmeno vuota o come segnaposto: un campo pronto da riempire renderebbe indistinguibile *fissato prima* da *riempito dopo*. Il secondo aggiunge il valore e la citazione.

**Che cosa questa prova stabilisce**: un fatto sullo stato del file — che i fattori vi compaiono in un commit anteriore a quello che introduce il valore.

**Che cosa non stabilisce**, e va detto perché il titolo di questa sezione potrebbe far credere il contrario: un fatto sullo stato di **conoscenza** di chi ha scritto. Il valore adottato è pubblico dal 2018<!--#--> e nulla esclude che fosse già noto mentre i fattori venivano fissati. Va aggiunto che una cronologia git è riscrivibile da chi la produce, e che qui l'autore dei commit e l'autore di questa rivendicazione sono la stessa persona. La garanzia è reale ma limitata: vale contro la variante più comune del difetto — il campo lasciato pronto e riempito dopo — non contro tutte, e chi la legge come una prova di buona fede le chiede più di quanto possa dare.

## 5. I valori

**I tre<!--#--> valori di ciascuna tabella vanno insieme.** Nessuno dei due<!--#--> gruppi ha una riga che possa essere estratta da sola: prendere il valore centrale perché sta meglio in una dashboard comunica una certezza che il dato non ha, ed è la violazione più facile da commettere e la più difficile da vedere a valle.

Il tasso di adozione, in punti percentuali della base — a confidenza **bassa**, sotto l'assunzione di trasferimento `A6`:

| Scenario | Tasso |
|---|---|
| pessimista | 15<!--@BQ3.adoption.worst--> |
| centrale | 30<!--@BQ3.adoption.base--> |
| ottimista | 60<!--@BQ3.adoption.best--> |

La variazione del ricavo medio per utente, in euro per utente al mese, ottenuta moltiplicando ciascun tasso per il differenziale di `4.00`<!--@conventions.bq3_price_delta_eur--> euro dichiarato in A4 — stessa confidenza, stessa assunzione, e **non moltiplicabile per una base utenti** (§8):

| Scenario | Uplift |
|---|---|
| pessimista | 0,60<!--@BQ3.uplift.worst--> |
| centrale | 1,20<!--@BQ3.uplift.base--> |
| ottimista | 2,40<!--@BQ3.uplift.best--> |

Due<!--#--> proprietà della banda hanno un identificativo proprio, perché un confronto costruito su valori pubblicati **è esso stesso un valore pubblicato** e non si scrive a mente: l'ampiezza vale 45<!--@BQ3.band.spread_pp--> punti percentuali, e il rapporto fra scenario ottimista e pessimista vale 4<!--@BQ3.band.ratio-->.

Il rapporto **non dipende dal benchmark**. Discende dai soli fattori, e resterebbe lo stesso qualunque valore fosse stato adottato: è una proprietà della stipulazione, non del mondo. Cambiare il benchmark e rieseguire muove ogni altro numero di questa sezione e lascia fermo quello.

## 6. Non c'è alcuna estrazione casuale

Nessuno dei valori è estratto. La derivazione è deterministica: nessun generatore casuale, nessuna lettura dell'orologio, nessun contatto con l'esterno. Due<!--#--> esecuzioni consecutive producono file identici, e la verifica è nel [quickstart della feature](../specs/004-synthetic-business-metrics/quickstart.md).

Le ragioni sono tre<!--#-->:

1. nessun consumatore legge righe. La `007` legge valori aggregati, e righe generate non alimenterebbero nulla;
2. un'estrazione non aggiungerebbe informazione. Campionare attorno a una banda che dichiara la fiducia dell'analista produrrebbe dispersione che *sembra* misurata e non lo è — peggiorerebbe il documento, non lo migliorerebbe;
3. non esiste alcuna numerosità da cui estrarre, perché la base utenti non è quantificata.

**La terza ragione è più debole di come suona**, e conviene dirlo invece di lasciarla passare per la più forte. L'assenza di una numerosità non è un fatto del mondo: è una decisione presa nella revisione della `001`, cioè da questo stesso progetto. Usarla per concludere che la generazione stocastica era impossibile sarebbe circolare — si decide di non quantificare, e poi si usa l'assenza come dimostrazione. Ciò che si può dire onestamente è che, **date le decisioni di perimetro già prese**, quell'operazione non aveva più oggetto. Le prime due<!--#--> ragioni reggono da sole e non dipendono da alcuna scelta di perimetro.

### Scostamento dichiarato dal piano di lavoro

Il piano di lavoro prescriveva per questa feature «uno script con seed fisso genera il dataset». **Non è stato fatto**, e la divergenza va registrata invece che assorbita.

La formulazione precede le decisioni di perimetro che le hanno tolto l'oggetto: quando è stata scritta, engagement e base utenti erano ancora dentro. Usciti quelli, non resta nulla da generare — e un seed fisso in una derivazione che non estrae nulla sarebbe decorativo. Un seed dichiara che esiste un'estrazione riproducibile; dove l'estrazione non c'è, dichiara il falso.

## 7. Con quanta precisione si pubblicano

**La precisione del benchmark è essa stessa un'assunzione**, ed è l'ipotesi da cui dipende ogni cifra pubblicata qui. Il valore compare come una percentuale intera nel titolo di un comunicato stampa: lo zero<!--#--> finale può essere significativo oppure il prodotto di un arrotondamento, e la fonte non nomina lo studio né la numerosità campionaria che permetterebbero di deciderlo. Si sono assunte due<!--#--> cifre significative perché il comunicato lavora in punti percentuali interi anche altrove. Se la cifra significativa fosse una sola, **ogni valore derivato ne porterebbe una di troppo**.

Vale la pena notare dove va a finire il rigore di questa feature. L'aritmetica è in decimale esatto e mai in virgola mobile, la modalità di arrotondamento è dichiarata invece che ereditata, e sul confine le due<!--#--> insidie sbagliano ciascuna un valore diverso. Tutto ciò presidia una catena di calcolo fatta di due<!--#--> moltiplicazioni per costanti tonde, che si farebbe a mente. **Nessuno di quei presidi tocca l'assunzione sulla precisione dell'ingresso**, che è l'unica da cui il risultato dipende davvero.

La regola distingue due<!--#--> famiglie, dichiarate per esteso fra le convenzioni dell'artefatto:

- i **tassi** si pubblicano alle cifre significative del benchmark;
- gli **importi in euro** si pubblicano a due<!--#--> posizioni decimali fisse. È la convenzione con cui si scrive una valuta, non una pretesa di precisione: il centesimo è l'unità in cui la valuta è denominata, e toglierlo non renderebbe il numero più prudente, lo renderebbe malformato. La precisione effettiva resta quella del benchmark, e `1,20` non va letto come una conoscenza a tre<!--#--> cifre.

## 8. Limiti dichiarati

**Il range non è un intervallo di confidenza.** Non c'è alcun «95<!--#-->%» dentro questi numeri, e l'ampiezza non ha interpretazione probabilistica. Chiedere con che probabilità il vero valore cada nella banda è una domanda a cui questo documento non risponde.

**Quale grandezza temporale sia il tasso, dichiarata una volta per tutte.** Il documento nomina tre<!--#--> cose diverse — uno stato della base a un istante (§3, ciò che la fonte misura), un movimento entro l'orizzonte (§3, ciò che serve al KPI), e un livello a regime (qui sotto). Non sono la stessa grandezza, e la scelta cambia il numero che qualcuno userà. **Ciò che i valori di §5 rappresentano è il tasso raggiunto a fine orizzonte e mantenuto**: quindi l'uplift corrispondente è un livello mensile, non una media del periodo — nei primi mesi sarebbe minore — e non un totale.

**L'uplift non è un ricavo cumulato.** Un livello mensile e un cumulato sull'orizzonte non coincidono mai: differiscono per il numero di mesi. Ciò che l'esclusione delle disdette rende vero è più stretto — su una base che non perde nessuno, il livello a regime resta lo stesso mese dopo mese invece di erodersi — e non autorizza a leggere il valore mensile come una grandezza annua.

**Le disdette sono escluse.** Il tasso è lordo, su base assunta costante (A5). È una scelta di perimetro dichiarata, non una proprietà del mondo.

**`BQ3-K2` è euro per utente al mese, e questa pagina non fornisce il moltiplicatore.** La formulazione va presa alla lettera, perché la versione più comoda — «non è scalabile» — direbbe una cosa falsa: il valore **è** scalabile, chiunque disponga di una stima di abbonati lo moltiplica in pochi secondi. Ciò che è vero è che qui nessuna base utenti viene quantificata, per la decisione presa nella revisione della `001`, e che l'artefatto non offre alcuna chiave per farlo. Non è un presidio: è una rinuncia, e non impedisce a valle l'operazione che scoraggia. Un totale di ricavo costruito su questi numeri sarebbe un numero che nessuno ha misurato, con l'autorevolezza di uno misurato.

**La confidenza resta bassa**, e l'ancoraggio a una fonte citabile non la innalza: la trasferibilità è una questione diversa dalla solidità del calcolo.

**Che cosa nessuna verifica di questo progetto garantisce.** Il controllo di coerenza confronta questo documento con l'artefatto che lo alimenta: verifica che i numeri non divergano fra loro. Nessuno dei due<!--#--> guarda il mondo. Che il benchmark sia il valore giusto, che l'assunzione di trasferimento regga, e che la fonte adottata sia abbastanza vicina a ciò per cui viene usata sono tre<!--#--> questioni su cui non esiste presidio automatico — e la trasparenza con cui sono dichiarate qui non è una risposta, è solo il modo di non fingere che la domanda non esista.

## 9. Come si verifica

```bash
python3 scripts/build_bq3_scenarios.py    # rigenera i valori
python3 scripts/check_audit_coherence.py  # verifica che documento e artefatto non divergano
```

Nessuno dei due<!--#--> comandi richiede rete, credenziali o i dataset di origine: leggono soltanto artefatti versionati.

**Che cosa si può rifare, e che cosa no.** Si possono **ricalcolare** tutti i valori derivati: discendono dal benchmark per due<!--#--> moltiplicazioni, e chiunque cloni il repository ottiene gli stessi numeri. **Non si può rifare il benchmark.** Quello si rilegge da un file curato a mano nello stesso repository, cioè si prende per buono; la verifica genuinamente esterna consiste nell'aprire il comunicato citato e constatare che riporti quella cifra — e anche riuscendoci si constata che un comunicato la riporta, non che sia stata misurata in un modo che si possa giudicare, perché lo studio non è nominato. Non esiste copia archiviata né identificativo permanente: se quell'indirizzo smettesse di rispondere, la verifica esterna verrebbe meno e resterebbe solo il valore congelato qui.

Ogni cifra pubblicata in questa pagina porta un'ancora invisibile all'identificativo che la produce, secondo le [convenzioni di marcatura](convenzioni-marcatura.md). Vale la severità stretta: una quantità priva di marcatore è un **errore** e non un avviso. Ciò che il controllo garantisce, e ciò che non può garantire, è dichiarato nella stessa pagina.
