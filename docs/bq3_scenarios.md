# Gli scenari di adozione del tier premium

Come i parametri della terza domanda di business passano da un valore osservato su un operatore terzo a tre<!--#--> scenari, e che cosa quei numeri non dicono.

Questo è il documento in cui si contesta il metodo. Il numero che il board legge sta nel [business case](business_case.md); qui c'è come è stato costruito, quali sono le sue debolezze note, e dove si romperebbe. È scritto perché chi non si fida possa avere torto per una ragione precisa invece che per diffidenza generica.

---

## 1. Che cosa questa feature produce

Due<!--#--> parametri, che alimentano `BQ3-K1` — il tasso di adozione del tier premium — e `BQ3-K2`, la variazione del ricavo medio per utente. La feature **non calcola i due<!--#--> KPI**: quelli appartengono alla `007`, che legge questi valori e non li ricalcola.

Non produce alcun dataset. Non esiste un file di righe generate, e non è una semplificazione: è una conseguenza, spiegata in §6.

Restano fuori dal perimetro, ciascuno per una ragione dichiarata altrove: il churn (FR-018 della `001`), l'engagement — nessun KPI del framework lo consuma — la determinazione dei prezzi (A4, e `FR-017a` della `001`), e la quantificazione della base utenti, che la revisione della `001` ha deciso di non fare.

## 2. Il parametro viene da fuori, e si può verificare

Il valore centrale non è una scelta dell'analista. È un benchmark pubblico di settore, ammesso come quarta<!--#--> fonte dati dalla constitution a cinque<!--#--> condizioni: citazione puntuale, valore congelato in un file versionato, nessuna chiamata di rete durante l'esecuzione, assunzione di trasferimento dichiarata, nessuna promozione del livello di confidenza.

| | |
|---|---|
| **Organizzazione** | Parks Associates |
| **Titolo** | `Parks Associates: 30% of Netflix Subscribers in Premium Service Tier` |
| **Pubblicazione** | 2018-07-19 |
| **Riferimento** | [comunicato su PR Newswire](https://www.prnewswire.com/news-releases/parks-associates-30-of-netflix-subscribers-in-premium-service-tier-300683486.html) |
| **Accesso** | 2026-08-16 |

Il valore adottato è 30<!--@BQ3.adoption.base--> punti percentuali della base abbonati. Il file che lo congela è [`data/benchmarks/bq3_tier_upgrade.json`](../data/benchmarks/bq3_tier_upgrade.json), che è curato a mano, versionato, e **mai riscritto da alcuno script**: la raccolta di un benchmark è un passaggio umano che nessuno rieseguirà, ed è precisamente la ragione per cui il suo esito va congelato invece che rifatto.

Lo stesso file porta il registro delle fonti valutate e **respinte**, ciascuna con il proprio motivo. Un rigetto non registrato renderebbe non verificabile l'affermazione che la fonte adottata fosse la migliore disponibile, e quella affermazione è parte di ciò che si sta chiedendo di credere.

## 3. Che cosa la fonte misura davvero

Non ciò per cui viene usata. Lo scarto è ampio, ha più di una direzione, e va conosciuto prima di leggere i valori di §5.

**Che cosa Parks Associates ha misurato**: la quota di abbonati Netflix che si trovava sul piano al prezzo più alto del listino, rilevata sui consumatori degli Stati Uniti e pubblicata nel 2018-07-19. È una composizione della base a un istante.

**Che cosa serve a `BQ3-K1`**: quale quota di una base preesistente adotti il tier premium entro 12<!--#--> mesi dal lancio di un verticale musicale che ancora non esiste.

Le divergenze fra le due<!--#--> cose sono cinque<!--#-->, e il file dei parametri le riporta per esteso. In sintesi:

| Divergenza | Verso |
|---|---|
| composizione contro flusso: sono grandezze diverse, e non lo smettono di essere perché la base parte tutta dal tier base | di definizione |
| la composizione ha avuto anni per accumularsi e comprende chi ha sottoscritto il piano più caro all'iscrizione, senza essere mai salito da nulla | spinge il valore **in alto** |
| ciò che distingue i piani è il numero di schermi e la qualità video, cioè un attributo di servizio; da noi è un verticale di contenuto | **ignoto** |
| il differenziale di prezzo osservato era superiore a quello di A4 | spinge il valore **in basso** |
| il comunicato non nomina lo studio né la numerosità campionaria | non ispezionabile |

**Il segno netto non è noto.** Le due<!--#--> divergenze di cui si conosce la direzione puntano in verso opposto, e la terza — la più grande — non ha un verso noto nemmeno in linea di principio. Dichiararne una sola farebbe apparire il valore conservativo oppure ottimista a seconda di quale si tace.

### L'assunzione di trasferimento

Il valore descrive Netflix, su un mercato e in un periodo che non sono quelli di StreamWave. Assumere che si trasferisca è **un'assunzione dell'analista, non un fatto misurato su StreamWave**: è l'assunzione `A6` del business case.

L'ancoraggio a una fonte citabile rende il parametro **verificabile**, non **vero per StreamWave**. Sono due<!--#--> proprietà diverse, e confonderle è il modo più elegante di sbagliare qui: un numero con una citazione sembra più solido di un numero senza, e in un senso preciso lo è — si può contestare la fonte — ma la distanza fra quella fonte e questo caso resta intera.

## 4. Da un valore a tre scenari

La banda è **moltiplicativa e relativa**: lo scenario pessimista vale il valore centrale per `0.50`<!--@conventions.bq3_band_factor_low-->, l'ottimista per `1.50`<!--@conventions.bq3_band_factor_high-->.

**L'ampiezza della banda non misura nulla.** Non è una varianza osservata, non è un intervallo di confidenza, non ha interpretazione probabilistica. Dichiara quanta fiducia l'analista ripone nel trasferimento del benchmark — nient'altro. Chi la legge come dispersione statistica le attribuisce un contenuto che non ha.

**Perché un fattore tondo.** Non esiste alcun criterio che ricavi quel numero da qualcosa: è una stipulazione. In questa condizione la rotondità è la ragione e non la sua assenza — un fattore come `0,37` comunicherebbe a chi legge che il valore viene da un calcolo, e non ne viene. Una stipulazione grossolana deve avere l'aspetto di una stipulazione grossolana.

### I fattori sono stati fissati prima di conoscere il benchmark

È il punto di metodo di questa feature, e l'unico che il documento chiede di verificare invece che di credere.

L'ampiezza della banda è **l'unico numero libero** dell'intera derivazione: tutto il resto discende dal benchmark. Sceglierla dopo aver visto il valore adottato la piegherebbe verso l'intervallo che sembra giusto, in un modo che nessun controllo automatico di questo progetto potrebbe rilevare — perché non c'è nulla, in un file, che distingua un fattore scelto prima da uno scelto dopo.

La garanzia non è quindi un'affermazione, è la cronologia dei commit:

```bash
git log --follow data/benchmarks/bq3_tier_upgrade.json
```

Il primo commit contiene i fattori, la loro ragione e il differenziale di prezzo, e **non contiene la chiave del benchmark**, nemmeno vuota o come segnaposto: un campo pronto da riempire renderebbe indistinguibile *fissato prima* da *riempito dopo*. Il secondo aggiunge il valore e la citazione.

I fattori possono cambiare dopo — nulla lo vieta — purché il cambiamento sia dichiarato con la propria ragione. Ciò che la precedenza rende impossibile è cambiarli in silenzio.

## 5. I valori

Il tasso di adozione, in punti percentuali della base:

| Scenario | Tasso |
|---|---|
| pessimista | 15<!--@BQ3.adoption.worst--> |
| centrale | 30<!--@BQ3.adoption.base--> |
| ottimista | 45<!--@BQ3.adoption.best--> |

La variazione del ricavo medio per utente, in euro per utente al mese, ottenuta moltiplicando ciascun tasso per il differenziale di `4.00`<!--@conventions.bq3_price_delta_eur--> euro dichiarato in A4:

| Scenario | Uplift |
|---|---|
| pessimista | 0,60<!--@BQ3.uplift.worst--> |
| centrale | 1,20<!--@BQ3.uplift.base--> |
| ottimista | 1,80<!--@BQ3.uplift.best--> |

Due<!--#--> proprietà della banda, che hanno un identificativo proprio perché un confronto costruito su valori misurati **è esso stesso un valore misurato**: l'ampiezza vale 30<!--@BQ3.band.spread_pp--> punti percentuali, e il rapporto fra scenario ottimista e pessimista vale 3<!--@BQ3.band.ratio-->.

Il rapporto **non dipende dal benchmark**. Discende dai soli fattori, e resterebbe lo stesso qualunque valore fosse stato adottato: è una proprietà della stipulazione, non del mondo. Cambiare il benchmark e rieseguire muove ogni altro numero di questa sezione e lascia fermo quello.

## 6. Non c'è alcuna estrazione casuale, e non è una scorciatoia

Nessuno dei valori è estratto. La derivazione è deterministica: nessun generatore casuale, nessuna lettura dell'orologio, nessun contatto con l'esterno. Due<!--#--> esecuzioni consecutive producono file identici, e la verifica è nel [quickstart della feature](../specs/004-synthetic-business-metrics/quickstart.md).

Le ragioni sono tre<!--#-->, in ordine crescente di forza:

1. nessun consumatore legge righe. La `007` legge valori aggregati, e righe generate non alimenterebbero nulla;
2. un'estrazione non aggiungerebbe informazione. Campionare attorno a una banda che dichiara la fiducia dell'analista produrrebbe dispersione che sembra misurata e non lo è — cioè peggiorerebbe il documento, non lo migliorerebbe;
3. **non esiste alcun N da cui estrarre.** La base utenti non è quantificata, per una decisione presa nella revisione della `001`. Senza una numerosità, la generazione stocastica non è una scelta scartata: è un'operazione priva di oggetto.

### Scostamento dichiarato dalla roadmap

La roadmap prescrive per questa feature «uno script con seed fisso genera il dataset». **Non è stato fatto**, e la divergenza va registrata invece che assorbita.

La formulazione precede le decisioni di perimetro che le hanno tolto l'oggetto: quando è stata scritta, engagement e base utenti erano ancora dentro. Usciti quelli, non resta nulla da generare — e un seed fisso in una derivazione che non estrae nulla sarebbe decorativo. Un seed dichiara che esiste un'estrazione riproducibile; dove l'estrazione non c'è, dichiara il falso.

## 7. Con quanta precisione si pubblicano

Il benchmark è noto a due<!--#--> cifre significative, e nessun valore che ne discende può esserne noto a più. Il prodotto per il differenziale di prezzo è l'operazione che più facilmente inganna, perché quel differenziale è **esatto per costruzione** — è una decisione di scenario, non una misura — e moltiplicare per un valore esatto conserva l'illusione di precisione dell'altro fattore.

La regola distingue quindi due<!--#--> famiglie, ed è dichiarata per esteso fra le convenzioni dell'artefatto:

- i **tassi** si pubblicano alle cifre significative del benchmark;
- gli **importi in euro** si pubblicano a due<!--#--> posizioni decimali fisse. È la convenzione con cui si scrive una valuta, non una pretesa di precisione: il centesimo è l'unità in cui la valuta è denominata, e toglierlo non renderebbe il numero più prudente, lo renderebbe malformato. La precisione effettiva degli importi resta quella del benchmark, e `1,20` non va letto come una conoscenza a tre<!--#--> cifre.

L'aritmetica è in decimale esatto e mai in virgola mobile, con la modalità di arrotondamento dichiarata invece che ereditata. Non è pedanteria: sul confine, la virgola mobile e la modalità predefinita sbagliano ciascuna un valore diverso, e nessuno dei due<!--#--> errori si presenterebbe come errore.

## 8. Limiti dichiarati

**Il range non è un intervallo di confidenza.** Non c'è alcun «95<!--#-->%» dentro questi numeri, e l'ampiezza non ha interpretazione probabilistica. Chiedere «con che probabilità il vero valore cade nella banda» è una domanda a cui questo documento non risponde, e nessuna versione futura di questo documento risponderà finché nulla di osservato su StreamWave la sostenga.

**`BQ3-K2` è euro per utente al mese, e non è scalabile.** Nessuna base utenti viene quantificata in questo progetto, e l'artefatto non offre alcuna chiave con cui moltiplicare l'uplift. È deliberato: un totale di ricavo costruito su questi numeri sarebbe un numero che nessuno ha misurato, presentato con l'autorevolezza di uno che qualcuno ha misurato.

**Le disdette sono escluse.** Il tasso è lordo, su base assunta costante (A5). Ne discende una conseguenza che va detta perché è facile leggere il contrario: l'uplift è un valore **a regime**, non un ricavo cumulato sui 12<!--#--> mesi dell'orizzonte. Le due<!--#--> grandezze coinciderebbero solo se nessuno disdicesse.

**La confidenza resta bassa**, e i valori vanno sempre presentati come range. L'ancoraggio a una fonte citabile non la innalza: la trasferibilità è una questione diversa dalla solidità del calcolo. Un valore singolo preso da questa tabella — tipicamente quello centrale, perché sta meglio in una dashboard — comunicherebbe una certezza che il dato non ha, ed è la violazione più facile da commettere e la più difficile da vedere a valle.

**Che cosa nessuna verifica di questo progetto garantisce.** Il controllo di coerenza confronta questo documento con l'artefatto che lo alimenta: verifica che i numeri non divergano fra loro. Nessuno dei due<!--#--> guarda il mondo. Che il benchmark sia il valore giusto, che l'assunzione di trasferimento regga, e che la fonte adottata sia abbastanza vicina a ciò per cui viene usata sono tre<!--#--> questioni su cui non esiste presidio automatico, e su cui questo documento offre soltanto la propria trasparenza.

## 9. Come si verifica

```bash
python3 scripts/build_bq3_scenarios.py    # rigenera i valori
python3 scripts/check_audit_coherence.py  # verifica che documento e artefatto non divergano
```

Nessuno dei due<!--#--> comandi richiede rete, credenziali o i dataset di origine: leggono soltanto artefatti versionati. Chi clona il repository può quindi rifare ogni numero di questa pagina.

Ogni cifra pubblicata qui porta un'ancora invisibile all'identificativo che la produce, secondo le [convenzioni di marcatura](convenzioni-marcatura.md). Su questo documento vale la severità stretta: una quantità priva di marcatore è un **errore** e non un avviso. Ciò che il controllo garantisce, e ciò che non può garantire, è dichiarato nella stessa pagina.
