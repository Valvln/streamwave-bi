# Contratto di narrazione: che cosa il report dice, alla lettera

**Feature**: `010b-report-costruzione` | **Data**: 2026-08-29 | **Stato**: **in attesa di approvazione** — punto di fermata 3

---

## A chi questo testo è rivolto

**Un decisore che non ha letto alcun documento di questo repository.** Non sa che cosa sia un segmento, non sa che cosa distingua una confidenza alta da una media, non ha modo di aprire `docs/` e non aprirebbe una nota a piè di schermo. Scorre dieci pagine e se ne va.

È il destinatario che il criterio di accettazione della constitution nomina — *reggere la presentazione a un board reale* — ed è il metro contro cui la `008b` è stata fermata e la `009` è passata.

**Ne discende una cosa sola, e governa ogni riga di questo documento**: un blocco esatto e incomprensibile è un difetto, e nessun presidio automatico di questo repository può vederlo.

---

## Che cosa questo documento è

**È il deliverable, non la sua descrizione.** Il contratto di pagina della `010a` disegnava una struttura, e una struttura si descrive; qui il deliverable **è prosa**, e una prosa descritta non è una prosa.

**È anche l'unico modo in cui la prosa del report esiste nel repository.** Il `.pbix` non è versionabile: chi legge questo progetto da fuori non potrà aprirlo. Senza questo documento la metà del deliverable che un lettore esterno può giudicare non esisterebbe.

Ogni blocco porta quattro cose, sempre nello stesso ordine:

1. **dove va** — pagina e spazio riservato dal contratto di pagina §17;
2. **che cosa dice** — il testo letterale, dentro un blocco delimitato;
3. **che cosa il lettore può concludere** — l'affermazione positiva che il blocco autorizza;
4. **da dove viene** — la sezione di documento pubblicato o il vincolo di contratto da cui discende.

**La terza voce è nuova rispetto alla `008b`**, ed è la ragione per cui questo documento è strutturato diversamente. Vedi §1.

---

## Che cosa questo documento non è

**Non è un manuale di clic.** Dove un testo va è dichiarato in termini di pagina e di spazio riservato; **come** si crea una casella di testo, quale carattere, quale corpo, quale colore appartiene a chi costruisce, e prescriverlo sarebbe pilotare la GUI per interposta prosa (principio V).

**Non è la fonte autorevole su ciò che esiste a schermo.** Questo documento dichiara che cosa si è deciso di scrivere; ciò che è stato scritto lo dirà la sezione «Esito della costruzione» di [quickstart.md](../quickstart.md), e dove i due divergono **quella prevale**.

**Non pubblica alcun valore.** Nessun numero di KPI è trascritto qui: i valori arrivano a schermo dalle misure, e una seconda copia è una copia che può divergere senza che nulla lo segnali.

---

# Parte I — I vincoli

Questa parte precede i blocchi e li governa tutti. È scritta per prima perché un blocco scritto prima che il proprio vincolo esista è un blocco scritto senza di esso, e riscriverlo dopo non è la stessa cosa.

## 1. La regola del permesso — `N1`

> **Ogni limite scritto a schermo sta accanto a ciò che il lettore può concludere nonostante quel limite.** Un limite da solo non è rigore: è una pagina che il lettore archivia.

**Da dove viene.** È il difetto per cui la `008b` è stata fermata, nominato alla lettera dal §5 del suo verbale:

> Trentadue blocchi dicono al lettore che cosa non concludere; nessuno gli dice che cosa può concludere. Il documento teme, giustamente, che il lettore concluda troppo; il risultato è un testo davanti al quale l'unica mossa razionale è non concludere niente, e un decisore che non conclude niente non ha usato la dashboard — l'ha archiviata.

È l'issue [`#28`](https://github.com/Valvln/streamwave-bi/issues/28), e **si chiude qui o non si chiude**.

**Come si verifica**: si prende ogni limite scritto e si cerca sulla stessa pagina l'affermazione positiva che gli sta accanto. **Zero limiti orfani** è l'esito atteso, ed è il criterio `SC-002` della spec.

**Perché la voce «che cosa il lettore può concludere» è obbligatoria in ogni blocco.** Il verbale della `008b` osserva che il registro giusto era **ammesso** dal contratto e non è stato usato: *il registro «che cosa il valore misura» è stato usato per dire con quali dati il numero è calcolato, quasi mai per dire che cosa dice del mondo*. Un registro ammesso non basta; questo contratto lo rende **una casella da compilare**, così che un blocco senza permesso sia visibilmente incompleto invece che semplicemente cauto.

### 1.1 Il corollario sull'ordine dentro il blocco

**Il permesso viene prima del limite, non dopo.** Il verbale della `008b` ha misurato che cosa cade quando lo spazio stringe:

> In otto casi su nove ciò che cade è la seconda metà del blocco. La seconda metà è quasi sempre la conseguenza pratica, e la prima metà è quasi sempre il meccanismo. Restano quindi a schermo, ripetutamente, la spiegazione difficile senza l'istruzione facile.

Se ciò che cade è la fine, allora ciò che deve stare in fondo è **la parte di cui si può fare a meno**. Il meccanismo — come un valore è costruito — è la parte sacrificabile; la conseguenza pratica non lo è.

**Ne discende la forma di ogni blocco**: prima che cosa si può concludere, poi a quali condizioni. Un blocco troncato a metà resta così una cosa vera e utile, invece di una spiegazione senza istruzione.

---

## 2. La lista chiusa dei numerali — `N2`

**Nessun blocco di narrazione contiene una cifra**, salvo le voci di questa lista. La lista è **chiusa**: aggiungervi una voce è una modifica di questo contratto, da riapprovare, non una scelta di chi costruisce.

| Voce | Dove compare | Perché non viene da una misura | Fonte |
|---|---|---|---|
| **2021** — copertura del catalogo video | pagina 10, e in nessun altro blocco | il modello non ha dimensione di calendario, quindi nessuna misura può produrlo. È però un fatto **osservato**: è il massimo del campo `release_year` | `NF.num.release_year.max`; `data_model.md` §16 e §18 |
| **2022** — copertura del catalogo musicale | pagina 10, e in nessun altro blocco | come sopra per l'assenza di calendario, ma **non è un fatto osservato**: il catalogo musicale non espone alcun campo di data, e l'anno è preso dalla documentazione della fonte | `data_model.md` §18, che lo dichiara non verificabile |
| **2018** — anno del benchmark economico | pagina 9, e in nessun altro blocco | è la data del comunicato che pubblica il valore centrale della terna di adozione | `bq3_scenarios.md`; `raccomandazione.md` §4 |
| **100.000** — l'unità del fattore di conversione | pagina 9, e in nessun altro blocco | è un'**unità dichiarata**, la stessa categoria delle soglie: non è una stima della base di StreamWave | contratto di pagina §11 |

**L'obbligo che la lista si porta dietro.** I tre anni **non hanno lo stesso statuto**, e il testo deve distinguerli. Pubblicare come osservata una cosa che nessuno ha osservato è la sola categoria di errore contro cui, per [`convenzioni-marcatura.md`](../../../docs/convenzioni-marcatura.md) §8, non esiste presidio automatico.

### 2.1 Le tre categorie di numerale, e che cosa ciascuna richiede

**Questa sezione è stata riscritta durante la stesura**, e la riscrittura va dichiarata perché è un difetto trovato e corretto invece che una scelta iniziale.

**La prima versione vietava ogni numerale in lettere**, sul modello della `008b`, che scriveva: *nessun blocco scrive «due», «tre», «sette», nemmeno riferito a cose che non sono misure*. Applicata a questo report, quella regola è risultata **violata dal testo stesso in una ventina di punti** — e non per sciatteria: un report costruito su **tre condizioni** non può nominarle senza contarle, e la pagina 3 non può dire che i cataloghi sostitutivi sono **due** senza il numerale.

**Perché la regola della `008b` funzionava là e non qui.** Quella dashboard non doveva mai enumerare: portava otto indicatori affiancati, e ogni numerale in prosa era con ottima probabilità un fatto misurato travestito. Questo report **è** un'enumerazione — tre condizioni, due prestiti, quattro condizioni di ribaltamento — e la regola severa vi diventa un divieto di dire ciò che la pagina esiste per dire.

**La regola vera è a tre categorie**, e la distinzione è verificabile leggendo:

| Categoria | Che cos'è | Che cosa richiede | Esempi in questo contratto |
|---|---|---|---|
| **struttura del discorso** | conta oggetti del ragionamento — condizioni, cataloghi, limiti, righe di una tabella — non osservazioni sui dati | **nulla**: è ammessa in lettere. È la prima categoria del marcatore di non-misurato di `convenzioni-marcatura.md` §2 | «tre condizioni», «i due cataloghi sostitutivi», «due conseguenze pratiche», «le due linee» |
| **lettura in parole di un valore a schermo** | dice in italiano corrente quanto vale un numero **che è a schermo, ancorato, sulla stessa pagina** | tre condizioni, tutte necessarie — vedi sotto | «poco più di quattro titoli su cento», «oltre il quaranta per cento», «quasi la metà», «ogni centomila abbonati» |
| **fatto misurato scritto in prosa** | un'osservazione sui dati che compare **solo** nel testo | **è vietata.** Il valore va a schermo come valore, con la propria etichetta e la propria ancora | nessuno, ed è ciò che `V2` verifica |

**Le tre condizioni della seconda categoria**, tutte e tre necessarie:

1. **il valore è a schermo, ancorato, sulla stessa pagina.** La parola non porta l'informazione: la rende leggibile. Chi verifica confronta il valore, non la parola;
2. **la parola è più larga del valore, mai più stretta.** «Poco più di quattro su cento» è vero per un intervallo che contiene il valore misurato; «quattro virgola ventisei su cento» sarebbe una seconda copia, ed è vietata;
3. **la stessa forma è già usata da `docs/raccomandazione.md`**, che è passato in severità stretta con quelle frasi.

**Perché la seconda categoria è necessaria e non una comodità.** Il destinatario di questo report non legge `0,0426`. Una pagina che porta la sola cifra e nessuna lettura in parole è esatta e muta, ed è il difetto contro cui questo intero contratto esiste.

**Che cosa resta vietato**, perché la categoria non si allarghi da sé: la lettura in parole di un valore che **non è a schermo su quella pagina**. Quella è una copia, e può divergere senza che nulla lo segnali.

**Non conta come numerale** un identificativo — `C1`, `C2`, `C3` sono nomi — né l'articolo indeterminativo: «una tabella», «un livello» introducono un oggetto, non ne dichiarano la quantità.

**Un'ultima esclusione.** I valori che le misure portano a schermo **sono cifre e non sono testo di narrazione**: arrivano dal modello, portano la propria etichetta, e questa regola non li tocca. La regola governa la prosa che sta accanto ai valori, non i valori.

**Come si verifica `V2`**: si scandiscono i blocchi delimitati, e per ogni numerale si dichiara a quale delle tre categorie appartiene. La terza categoria deve risultare **vuota**. È l'esito riportato in §9.

---

## 3. Le sigle si sciolgono sulla pagina in cui compaiono — `N3`

Nessun blocco usa una sigla senza scioglierla **sulla stessa pagina**.

**Da dove viene.** È il rilievo `R2` della `008b`, che descrive un modo di fallire non ovvio:

> I nomi `C1` e `C3` compongono da soli la regola che il contratto vieta di comporre: il lettore ricava che le condizioni sono almeno tre, ordinate, e che ne esiste una di mezzo che non gli viene mostrata. Il divieto di nominare `C2` la fa comparire come buco.

**La conseguenza per questo report è diversa e più semplice**, perché la `009` ha pubblicato `C2` e il verdetto: le tre condizioni esistono tutte, e nominarne una non lascia più un buco. Resta il vincolo di scioglierle.

**Le sigle `BQ1`, `BQ2`, `BQ3` non compaiono in alcun blocco.** Il report non è ordinato per esse (contratto di pagina §1.2), e nominarle reintrodurrebbe a schermo il framework che il disegno ha deliberatamente sciolto.

---

## 4. Le formulazioni escluse — `N4`

Sono le frasi che chi scrive sceglierebbe per comodità e che questo contratto vieta. Ciascuna ha alle spalle un difetto reale.

| Esclusa | Perché | Che cosa si scrive invece |
|---|---|---|
| «l'uplift non è scalabile» | `bq3_scenarios.md` §8 la dichiara **falsa**: il valore *è* scalabile, ed è ciò che il fattore di conversione insegna a fare. Sopravvive su due documenti (issue [`#26`](https://github.com/Valvln/streamwave-bi/issues/26) e [`#31`](https://github.com/Valvln/streamwave-bi/issues/31)), e questa feature **non la ripete** | la formulazione **stretta**: qui nessuna base viene quantificata e nessun artefatto del progetto offre una chiave per farlo |
| «la domanda è bassa», riferita ai segmenti marcati | la domanda **non è misurata dalla fonte**, che è diverso. Trasformerebbe un'assenza di misura in una misura sfavorevole | la fonte non ha registrato quanto questa musica venga ascoltata |
| «un debito aperto» come titolo | è il rilievo `R4`: *«debito» è gergo di repository, e su una pagina di impatto economico sarà letto come una passività* | ciò che di questo numero non si può verificare |
| «un indicatore a confidenza alta è alto» | è il rilievo `R13`: fa scivolare il lettore da **confidenza** a **valore**, che sono cose diverse | la confidenza dice quanto il numero è solido, non quanto è grande |
| «i cataloghi sono un proxy» | la parola «proxy» è gergo. Il verbale della `008b` indica la sostituzione concreta come modello: *«il catalogo video di Netflix sta al posto del catalogo attuale di StreamWave»* | la sostituzione detta per esteso, con i nomi delle due aziende |
| «intervallo di confidenza», riferito alla banda degli scenari | non c'è alcuna probabilità dentro quei numeri | la banda non dice con quale probabilità il valore vero vi cada |
| qualunque lessico causale su una corrispondenza | è il principio IV: *una correlazione NON DEVE mai essere presentata con lessico causale* | assomiglia, corrisponde, ricade nella stessa regione |

---

## 5. La parola «domanda» — `N5`

**È il rischio numero uno del vocabolario di questo report**, ed è il rilievo `R11` della `008b`: *la parola «domanda», dichiarata dal contratto il rischio numero uno, compare in tre significati diversi in quattro pagine*.

I significati che si contendono la parola sono tre:

| Significato | Dove compare | Come si scrive in questo report |
|---|---|---|
| la domanda di business — l'interrogativo per cui l'analisi esiste | pagine 1, 2 | **la domanda** |
| la domanda di mercato — quanto una musica è cercata | pagine 7, 8 | **quanto viene ascoltata**, oppure **il livello di ascolto** |
| la domanda come misura — `segment_demand_index` | pagine 7, 8 | non compare come parola: il valore porta la propria etichetta di colonna |

**La regola operativa**: dalla pagina 4 in avanti la parola «domanda» **non compare più** nel significato di mercato. Le pagine 7 e 8 usano il lessico dell'ascolto.

**Perché non si risolve con una glossa.** Una glossa spiega un termine; qui il problema è che lo stesso termine ha due referenti legittimi nello stesso report, e il lettore non ha modo di sapere quale sia attivo. Si risolve togliendo l'ambiguità, non spiegandola.

---

## 6. Il registro — `N6`

**Frasi brevi, un fatto ciascuna.** Il verbale della `008b` indica il modello:

> *«Sul lato video entrano i soli film. Le serie misurano la propria durata in stagioni. Sul lato musicale entra invece il catalogo intero.»* Tre frasi brevi, un fatto ciascuna, zero gergo, e la ragione tecnica dell'asimmetria resa senza nominarla.

**Si parla al lettore, non del numero.** È la proprietà che il verbale isola come la migliore dell'intera `008b`:

> *«Chiedere con quale probabilità il valore vero cada dentro la banda è una domanda a cui questi numeri non rispondono.»* Formula il divieto come la domanda che il lettore avrebbe davvero fatto, invece che come una proprietà dell'oggetto. È il solo blocco che parla al lettore invece che del numero.

**Ogni blocco finisce con un punto.** È il rilievo `R22`: *quattro blocchi finiscono senza punto, dentro caselle che scorrono: chi vede un testo finito non sa che è finito*.

**Nessun titolo si ripete nella stessa pagina.** È il rilievo `R10`.

---

## 7. Che cosa il testo non fa — `N7`

| Non fa | Perché |
|---|---|
| non nomina il framework degli otto indicatori | il report ne porta sette, ed è la decisione `CP-1`. Nominare il framework per dire che uno manca reintrodurrebbe l'inventario che il disegno ha sciolto |
| non rimanda a `docs/` né ad alcun file | il lettore non ha il repository. Un rimando che il lettore non può seguire è una frase lasciata a metà |
| non spiega come una misura è calcolata in DAX | è il meccanismo, e il meccanismo è la parte sacrificabile (§1.1) |
| non usa la prima persona plurale | «abbiamo trovato» sposta l'attenzione da ciò che il dato dice a chi lo ha guardato |
| non presenta un valore di `BQ3` isolato | il divieto di scheda singola: **sempre come terna**, nemmeno in una frase di sintesi |

---

## 8. La tabella di controllo dei permessi

Compilata riga per riga mentre i blocchi si scrivono. È la forma verificabile di `N1`, ed è ciò che rende `SC-002` un conteggio invece che un'impressione.

| Pagina | Limite scritto | Il permesso che gli sta accanto | Dove |
|---|---|---|---|
| 1 | non dice se l'operazione sarà redditizia; il lato dei costi è fuori perimetro | dice se sarebbe coerente, ed è la domanda che viene prima: entrare in un mercato vicino o in uno estraneo ha costi di partenza molto diversi | `BL-1-4`, stesso blocco |
| 2 | coerente non significa redditizia; i costi non sono stati guardati | entrerebbe in un mercato adiacente al proprio catalogo invece che in uno estraneo, e la differenza si paga in costi di acquisizione | `BL-2-3`, stesso blocco |
| 2 | la confidenza è media, non alta | dove sta l'anello debole è dichiarato, e la pagina che lo tratta dice quanto è debole | `BL-2-4`, stesso blocco |
| 3 | i numeri non descrivono StreamWave | sono cataloghi veri di servizi veri, e ogni misura li descrive correttamente | `BL-3-3`, stesso blocco |
| 3 | se i cataloghi non fossero rappresentativi, ogni numero diventerebbe muto su StreamWave | è l'unico giudizio che il lettore può esercitare meglio di chi ha fatto l'analisi | `BL-3-4` |
| 3 | i due prestiti non entrano nella scala di confidenza | si chiudono in un modo solo, ed è dichiarato: rifare l'analisi sui dati reali dell'azienda | `BL-3-6`, chiusura |
| 4 | «non residuale» non significa «grande»: è una porzione piccola del catalogo | la condizione dice che la musica non è marginale **fra le categorie**, che è una cosa diversa e verificabile nella distribuzione | `BL-4-3`, stesso blocco |
| 4 | — | il pubblico attuale incontra già contenuto musicale e non va educato a un genere nuovo; è la condizione più solida delle tre | `BL-4-4`, blocco di solo permesso |
| 5 | il rettangolo è più grande della regione reale; la stima è per eccesso | il vuoto dentro il rettangolo lo rende verificabile a occhio, invece di doverlo accettare | `BL-5-3`, stesso blocco |
| 5 | il dato del lato video è costruito, non osservato | — | `BL-5-4` → **il permesso è in `BL-5-5`, blocco seguente** |
| 5 | *(per i due limiti sopra)* | il grosso del catalogo musicale cade nella stessa regione, non ai margini; e la pagina seguente dà il metro per giudicare quanto i limiti pesino | `BL-5-5` |
| 5 | il grafico mostra due caratteristiche su tre | la terza esiste ed entra nel calcolo: non è disegnata perché una superficie ne porta due | `BL-5-6`, stesso blocco |
| 6 | il margine non è una stima dell'errore | è una condizione sull'errore, e dice quanto grande dovrebbe essere perché la conclusione si ribalti | `BL-6-4`, stesso blocco |
| 6 | la soglia è una stipulazione, non una misura | chi adottasse un criterio più severo troverebbe lo stesso esito, e fin dove regge è dichiarato | `BL-6-5`, stesso blocco |
| 7 | i punti contro il bordo sinistro non significano «poco ascoltato» | l'analisi ha preso posizione: non entrano in graduatoria e la pagina seguente li tiene separati | `BL-7-4`, stesso blocco |
| 7 | le quantità non si sommano; contare i brani non misura un mercato | — | `BL-7-5` → **il permesso è in `BL-7-3`, blocco precedente sulla stessa pagina** |
| 7 | *(per il limite sopra)* | la terza condizione è soddisfatta e non di misura: esiste un'area di scelta, non un caso isolato | `BL-7-3` |
| 8 | i tipi di musica non sono alternative; la prima riga non è la scelta | la tabella serve a descrivere l'area con dei nomi, che è ciò che la rende utilizzabile | `BL-8-2`, stesso blocco |
| 8 | la posizione non sostituisce una scelta di catalogo | i tipi in cima sono quelli su cui le due grandezze convergono meglio: è un punto di partenza ragionevole | `BL-8-3`, stesso blocco |
| 8 | per i tipi marcati la posizione non è costruibile | restano nella pagina con tutti gli altri valori, perché quelli esistono e vanno letti | `BL-8-4`, stesso blocco |
| 9 | sono scenari a confidenza bassa, non misure | si leggono come terna, ed è dichiarato come portarli via senza deformarli | `BL-9-2`, stesso blocco |
| 9 | il tasso è lordo; il ricavo è un livello e non un cumulato | è dichiarato che cosa esattamente misurano le due righe, in forma utilizzabile senza sbagliare l'ordine di grandezza | `BL-9-3`, stesso blocco |
| 9 | il report non quantifica la base e non offre chiavi per farlo | chi conosce la propria base divide per centomila e moltiplica: l'operazione è possibile e resta sua | `BL-9-4`, stesso blocco |
| 9 | del valore centrale non si può giudicare come sia stato misurato | se ne conosce il **verso** dello scarto: lo scenario centrale è probabilmente ottimista | `BL-9-5`, stesso blocco |
| 9 | il valore di riferimento descrive un altro operatore | vale per i numeri di questa pagina e per nessun altro del report | `BL-9-6`, stesso blocco |
| 10 | le quattro condizioni di ribaltamento | ciascuna porta la propria conseguenza, e la terza porta l'azione che la chiuderebbe | `BL-10-3`, per riga |
| 10 | i due prestiti, richiamati | la scala di confidenza dice quanto un numero è solido: resta valida per ciò che misura | `BL-10-4`, chiusura |
| 10 | non è un business case, non dice che il pubblico vorrebbe la musica, non è una previsione | ciascuna voce dichiara che cosa **invece** il report stabilisce | `BL-10-5`, per voce |
| 10 | i dati si fermano al 2021-2022, il riferimento economico al 2018 | la distinzione fra ciò che è osservato e ciò che è dichiarato dalla fonte è esplicita | `BL-10-6`, stesso blocco |

**Esito di `V1`: zero limiti orfani.**

**Due limiti hanno il proprio permesso in un blocco diverso**, sulla stessa pagina, e vanno dichiarati come i casi più esposti:

- `BL-5-4` (il dato costruito) trova il permesso in `BL-5-5`, che è il blocco **immediatamente successivo**;
- `BL-7-5` (le quantità non si sommano) trova il permesso in `BL-7-3`, che è **due blocchi prima**.

**Perché non è una violazione di `N1`.** La regola chiede che il permesso stia sulla **stessa pagina**, non nello stesso blocco: un lettore che guarda una schermata li vede insieme. **Perché va comunque dichiarato**: sono i due punti in cui un accorciamento in costruzione potrebbe far cadere il permesso lasciando il limite, ed è esattamente il modo in cui la `008b` ha fallito. Se lo spazio stringesse su quelle due pagine, **si taglia il limite prima del permesso**.

---

# Parte II — I blocchi

**Come leggere questa parte.** Ogni blocco porta un identificativo (`BL-<pagina>-<n>`), dove va, il testo letterale dentro un blocco delimitato, che cosa il lettore può concludere, e da dove viene.

**Il testo dentro i delimitatori è ciò che va a schermo, alla lettera.** Non è una parafrasi da adattare.

---

## Pagina 1 — La domanda

**Spazio riservato** (contratto di pagina §17): fascia sotto il diagramma delle condizioni.

**Che cosa questa pagina deve fare**: porre la domanda e dichiarare il criterio, **prima** che il verdetto compaia. È la sola pagina che non porta alcun valore.

### `BL-1-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
StreamWave può entrare nel music streaming?
```

**Che cosa il lettore può concludere**: che il report risponde a una domanda precisa, e quale.

**Da dove viene**: `raccomandazione.md`, «Che cosa è questo documento». È la domanda per cui l'analisi è stata commissionata, riportata alla lettera.

---

### `BL-1-2` — a che cosa serve questo report

**Dove**: fascia sotto il diagramma, primo blocco.

```
Questo report risponde a una domanda sola: se l'espansione nel music
streaming sia coerente con il catalogo che StreamWave ha già.

Risponde guardando che cosa StreamWave offre oggi e che cosa il pubblico
della musica cerca, e verificando tre condizioni fissate prima di
guardare i numeri. Le pagine che seguono portano la risposta, le tre
condizioni una per volta, da quale musica converrebbe cominciare, quanto
varrebbe, e a quali condizioni la risposta cambierebbe.
```

**Che cosa il lettore può concludere**: a che cosa serve guardare queste dieci pagine, e in quale ordine sono disposte.

**Da dove viene**: è la chiusura del rilievo `R1` della `008b` — *in quattro pagine nessun testo dice a che cosa la dashboard serva*. Il verbale lo mette fra le cinque cose che mancavano per un sì: *ritrovare una frase sola che dica a che cosa serve guardare queste quattro pagine*.

---

### `BL-1-3` — il criterio, e perché è stato fissato prima

**Dove**: fascia sotto il diagramma, secondo blocco, accanto al diagramma delle tre condizioni.

```
Il criterio è stato scritto e pubblicato prima che i numeri esistessero.
Sono tre condizioni, e l'argomento si considera sostenuto solo se valgono
tutte e tre.

È la proprietà più difendibile di questa analisi: chi la contesta può
verificare che le regole non siano state scelte dopo aver visto il
risultato.
```

**Che cosa il lettore può concludere**: che il criterio è verificabile in modo indipendente dal risultato, e che può contestarlo sapendo che non è stato costruito attorno alla conclusione.

**Da dove viene**: contratto di pagina §3 — *il criterio è stato pubblicato prima che i valori esistessero, ed è la proprietà più difendibile dell'intera analisi*. Il diagramma porta i **nomi** delle tre condizioni, non i loro esiti.

**Nota di forma**: «tre condizioni» e «tutte e tre» ricadono nella **prima categoria** di `N2.1` — struttura del discorso. Contano gli oggetti del ragionamento, non osservazioni sui dati.

---

### `BL-1-4` — che cosa il report non risponde

**Dove**: fascia sotto il diagramma, terzo blocco.

```
Questo report non dice se l'operazione sarà redditizia: il lato dei costi
— licenze, infrastruttura, organico — è fuori dal suo perimetro.

Dice se la mossa sarebbe coerente con ciò che StreamWave già offre, che è
la domanda che viene prima: entrare in un mercato vicino al proprio
catalogo, o in uno estraneo, sono decisioni con costi di partenza molto
diversi.
```

**Che cosa il lettore può concludere**: quale decisione questo report può sostenere e quale no — e perché la domanda a cui risponde ha comunque valore.

**Da dove viene**: `raccomandazione.md` §1 e §6. **È un'applicazione diretta di `N1`**: il limite (non dice se sarà redditizia) sta accanto al permesso (dice se sarebbe coerente, ed è la domanda che viene prima).

---

## Pagina 2 — La risposta

**Spazio riservato**: fascia sotto la visuale del verdetto.

**Che cosa questa pagina deve fare**: portare il verdetto e la regola che lo determina. È la pagina che un lettore ritaglierebbe per una slide, ed è scritta sapendolo.

### `BL-2-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
Sì: l'espansione è coerente con il catalogo attuale
```

**Che cosa il lettore può concludere**: la risposta, prima di qualunque difesa dell'argomento.

**Da dove viene**: `raccomandazione.md` §1, che apre con la stessa affermazione. Il contratto di pagina §5 argomenta perché la risposta viene prima dei suoi limiti: *una pagina sui limiti delle fonti collocata prima del verdetto si legge come una excusatio*.

---

### `BL-2-2` — che cosa la risposta dice

**Dove**: fascia sotto la visuale del verdetto, primo blocco.

```
Le tre condizioni fissate in partenza sono soddisfatte tutte e tre.

Significa che la musica non è un territorio estraneo per StreamWave: il
catalogo attuale contiene già contenuto musicale in misura non
marginale, la musica assomiglia per carattere a ciò che l'azienda già
offre, ed esiste musica insieme molto ascoltata e molto affine a quel
catalogo.
```

**Che cosa il lettore può concludere**: che l'argomento di coerenza regge, e su quali tre gambe poggia.

**Da dove viene**: `raccomandazione.md` §1 e §2. La visuale porta il conteggio e i tre esiti; questo blocco dice che cosa significano.

---

### `BL-2-3` — che cosa la risposta non dice

**Dove**: fascia sotto la visuale del verdetto, secondo blocco.

```
Coerente non significa redditizia. Questo report non ha guardato i costi,
e non dice che l'operazione convenga.

Dice una cosa più stretta e comunque utile: se StreamWave entrasse nella
musica, entrerebbe in un mercato adiacente al proprio catalogo invece che
in uno estraneo — e quella differenza si paga in costi di acquisizione
del pubblico.
```

**Che cosa il lettore può concludere**: che il verdetto sostiene una decisione di posizionamento, non una decisione di investimento — e perché la prima serve comunque.

**Da dove viene**: `raccomandazione.md` §1, *«che cosa questa risposta non dice»*, e il contratto di pagina §17, che riserva questo spazio esattamente a questo. **Applicazione di `N1`**, e di `N1.1`: il permesso sta nel secondo capoverso, cioè nella parte che cadrebbe per ultima.

---

### `BL-2-4` — perché la confidenza è media

**Dove**: fascia sotto la visuale del verdetto, terzo blocco, accanto all'etichetta del verdetto.

```
La confidenza di questa risposta è media, e non è la media delle tre
condizioni.

Una catena non è più solida del suo anello più debole: se una sola delle
condizioni poggia su un dato costruito invece che osservato, l'intera
risposta poggia su quel dato. Trattare la confidenza come una media
lascerebbe che la solidità della prima condizione coprisse quella delle
altre.

Qui l'anello più debole è la seconda condizione, e la pagina che la
tratta dice esattamente quanto è debole.
```

**Che cosa il lettore può concludere**: come leggere l'etichetta di confidenza, e dove andare a cercare il punto fragile invece di doverlo indovinare.

**Da dove viene**: `raccomandazione.md` §2, «La confidenza del verdetto, e perché non è la media delle tre», e il contratto di pagina §1.4. La metafora della catena è nuova: il documento originale argomenta la stessa cosa in forma astratta, e il destinatario di questo report non la riceverebbe.

---

## Pagina 3 — Su che cosa poggia

**Spazio riservato**: **l'intera pagina**, che è di sola prosa.

**Che cosa questa pagina deve fare**: dire che nessun numero del report è una misura fatta su StreamWave. È il limite più importante del deliverable, e ha una pagina propria perché **sopravviva all'estrazione di una schermata**.

**Vincolo di forma** (contratto di pagina §5 e §14): la pagina dà all'occhio **struttura** — l'articolazione fra i cataloghi sostitutivi e quelli che il progetto non ha — non un grafico. Nessuna visuale.

### `BL-3-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
Questi numeri non descrivono StreamWave
```

**Che cosa il lettore può concludere**: il limite più importante del report, nella posizione in cui non può mancarlo.

**Da dove viene**: è **il titolo di `BL-IN-1` della `008b`, ripreso alla lettera**. Il verbale della revisione lo isola come la cosa meglio scritta dell'intero deliverable precedente:

> Cinque parole che portano l'affermazione più importante del deliverable, nella posizione in cui non si può mancarla, senza una sola parola di gergo. Nulla di ciò che segue nella dashboard è scritto altrettanto bene, ed è la riga giusta nel posto giusto.

Riscriverlo per non ripetersi sarebbe buttare via l'unica riga che quella feature ha prodotto e che ha retto una revisione.

---

### `BL-3-2` — la sostituzione, detta per esteso

**Dove**: accanto all'articolazione dei quattro cataloghi, blocco principale.

```
StreamWave non ha ceduto i propri dati a questa analisi. Al posto dei suoi
due cataloghi ne sono stati usati altrettanti, pubblici.

Il catalogo video di Netflix sta al posto del catalogo attuale di
StreamWave. Un estratto pubblico di Spotify sta al posto del catalogo
musicale che StreamWave non ha ancora.
```

**Che cosa il lettore può concludere**: che cosa esattamente è stato guardato, e che non era StreamWave.

**Da dove viene**: `raccomandazione.md` §1, capoverso sui proxy. **La forma è quella che il verbale della `008b` indica come modello**:

> *«il catalogo video di Netflix sta al posto del catalogo attuale di StreamWave»*. Il lettore capisce l'intero impianto dei proxy da una frase, senza che la parola «proxy» compaia. È il modello di come tutti gli altri concetti tecnici andrebbero resi.

---

### `BL-3-3` — che cosa questo compra e che cosa costa

**Dove**: sotto `BL-3-2`.

```
Ciò che i due cataloghi sostitutivi permettono di dire è reale: sono
cataloghi veri, di servizi veri, e ogni misura di questo report li
descrive correttamente.

Ciò che non permettono di dire è che StreamWave sia come loro. Se il
catalogo di StreamWave avesse una composizione molto diversa da quello di
Netflix, ogni numero di questo report resterebbe corretto e smetterebbe
di parlare di StreamWave.
```

**Che cosa il lettore può concludere**: che l'analisi è solida su ciò che ha guardato, e che il salto verso StreamWave è dichiarato invece che nascosto.

**Da dove viene**: `raccomandazione.md` §6, primo trattino — *se non regge, ogni misura di questo progetto resta corretta come descrizione di quei cataloghi e diventa muta su StreamWave*. **Applicazione di `N1`**: il permesso apre il blocco, il limite lo chiude.

---

### `BL-3-4` — il giudizio che spetta al lettore

**Dove**: sotto `BL-3-3`.

```
Questa è l'unica cosa che chi legge può giudicare meglio di chi ha fatto
l'analisi. Valutare una mediana richiede competenza statistica; valutare
se il catalogo di Netflix somigli a quello di StreamWave richiede di
conoscere StreamWave.
```

**Che cosa il lettore può concludere**: che ha un ruolo attivo nel validare il report, e quale.

**Da dove viene**: `raccomandazione.md` §1, ultimo capoverso. È il blocco che trasforma un limite in una consegna al lettore, ed è la forma più forte che `N1` può prendere.

---

### `BL-3-5` — il secondo prestito, e perché è diverso

**Dove**: parte bassa della pagina, distinta dai blocchi precedenti.

```
C'è un secondo prestito, e tocca solo la pagina che stima quanto varrebbe
l'operazione.

Il valore di riferimento economico non descrive né StreamWave né i
cataloghi qui sopra: descrive un altro operatore, su un altro mercato,
alcuni anni prima. Vale per quei numeri e per nessun altro di questo
report.
```

**Che cosa il lettore può concludere**: che il limite economico ha una portata circoscritta, e quale — invece di estenderlo per prudenza a tutto il report.

**Da dove viene**: contratto di pagina §5, che impone che la differenza di portata fra le due assunzioni resti visibile: *`A1` si applica identica a tutti i valori del report; `A6` solo a quelli di `BQ3`. Presentarle come due voci equivalenti di un elenco suggerirebbe che abbiano la stessa portata, e `business_case.md` §6 dichiara che non ce l'hanno.*

**Nota di forma**: «alcuni anni prima» invece dell'anno esatto. L'anno del benchmark compare **solo** a pagina 9 per `N2`, e qui non serve: ciò che questo blocco deve trasmettere è la differenza di portata, non la data.

---

### `BL-3-6` — perché nessuna delle due entra nella scala di confidenza

**Dove**: chiusura della pagina.

```
Nessuno dei due prestiti compare nelle etichette di confidenza che
accompagnano i numeri, e non è una dimenticanza.

Quelle etichette dicono quanto un numero è solido: quanto è osservato
invece che costruito, quanto è riproducibile. I due prestiti riguardano
una domanda diversa — se quel numero parli di StreamWave. Un valore può
essere impeccabile come misura e non dire nulla del soggetto a cui lo si
vuole applicare.

Nessuna confidenza alta li compensa, e nessun miglioramento del metodo li
chiude. Si chiudono in un modo solo: rifacendo l'analisi sui dati reali
dell'azienda.
```

**Che cosa il lettore può concludere**: come leggere le etichette di confidenza su tutte le altre pagine, e che cosa servirebbe per superare questo limite.

**Da dove viene**: `raccomandazione.md` §6, e il contratto di pagina §5 — *le due assunzioni di trasferimento non entrano nella scala di confidenza per costruzione*. L'ultima frase è la chiusura di `N1`: il limite arriva con l'azione che lo risolverebbe.

---

## Pagina 4 — La prima condizione

**Spazio riservato**: fascia sotto la distribuzione.

**Che cosa questa pagina deve fare**: mostrare che nel catalogo video attuale la musica non è una nicchia dimenticata, e tenere distinte due letture che si somigliano — la quota e la posizione.

### `BL-4-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
La musica non è una nicchia nel catalogo attuale
```

**Che cosa il lettore può concludere**: che cosa la pagina afferma, prima di guardare la distribuzione.

**Da dove viene**: `raccomandazione.md` §2, «La prima».

---

### `BL-4-2` — come si legge la distribuzione

**Dove**: fascia sotto la distribuzione, primo blocco.

```
Ogni barra è una categoria del catalogo video, e la sua altezza è il
numero di titoli che contiene. La linea segna la mediana: metà delle
categorie sta sopra, metà sotto.

La categoria musicale, marcata nel grafico, sta nella metà alta. È la
prima condizione, ed è soddisfatta.
```

**Che cosa il lettore può concludere**: perché la condizione è soddisfatta, guardando la posizione invece di doversi fidare di un'asserzione.

**Da dove viene**: contratto di pagina §6 — *è la sola forma che mostra perché la condizione è soddisfatta invece di asserirlo. La condizione è una posizione, e una posizione si vede.* La glossa della mediana è quella di `raccomandazione.md` §3, spostata qui perché è qui che serve per prima.

---

### `BL-4-3` — non residuale non significa grande

**Dove**: fascia sotto la distribuzione, secondo blocco.

```
Non residuale non significa grande. La categoria musicale sta sopra la
mediana e resta comunque una porzione piccola del catalogo: poco più di
quattro titoli su cento.

Le due letture non si contraddicono, perché misurano cose diverse. La
condizione dice che la musica non è marginale rispetto alle altre
categorie, non che il catalogo sia musicale.
```

**Che cosa il lettore può concludere**: che cosa la condizione autorizza a dire e che cosa no — con il numero che rende contestabile l'affermazione invece di doverla accettare.

**Da dove viene**: `raccomandazione.md` §2, «Una precisazione che evita una lettura sbagliata», e il contratto di pagina §6, che la dichiara vincolo di disegno: *la distribuzione lo rende visibile senza dirlo — la categoria musicale sta sopra la mediana e è una barra piccola in valore assoluto*.

**Nota di forma**: «quattro titoli su cento» è la resa divulgativa della quota, che è a schermo come valore ancorato accanto al blocco. Ricade nella **seconda categoria** di `N2.1`: la quota è a schermo come valore ancorato accanto al blocco, e questa frase ne è la lettura in parole. Chi verifica confronta la quota, non la parola.

---

### `BL-4-4` — che cosa questa condizione compra

**Dove**: fascia sotto la distribuzione, terzo blocco.

```
Che cosa se ne ricava: il pubblico che StreamWave ha oggi incontra già
contenuto musicale sul servizio, e non dovrebbe essere educato a un
genere nuovo.

È la condizione più solida delle tre, e l'unica che si legge direttamente
dal dato senza alcuna interpretazione: il catalogo classifica già i propri
titoli, e una delle sue categorie è quella musicale.
```

**Che cosa il lettore può concludere**: la conseguenza pratica della condizione, e che questa è la gamba più forte dell'argomento.

**Da dove viene**: `raccomandazione.md` §2, *«Confidenza: alta. È l'unica delle tre che si legge direttamente dal dato, senza alcuna mappatura interpretativa»*. **Applicazione di `N1`**: è il blocco del permesso, e apre con la conseguenza.

---

## Pagina 5 — La seconda condizione

**Spazio riservato**: fascia sotto la dispersione, la più alta delle pagine con visuale.

**Che cosa questa pagina deve fare**: mostrare che la gran parte del catalogo musicale ricade nella regione di carattere già occupata dal catalogo video — **e mostrare quanto quella misura è debole**, perché è il termine più fragile dell'argomento.

### `BL-5-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
La musica assomiglia, per carattere, a ciò che StreamWave già offre
```

**Che cosa il lettore può concludere**: che cosa la pagina afferma, prima di guardare la dispersione.

**Da dove viene**: `raccomandazione.md` §2, «La seconda».

---

### `BL-5-2` — che cosa significa «carattere»

**Dove**: fascia sotto la dispersione, primo blocco.

```
Ogni contenuto è descritto con tre caratteristiche: quanto è ritmato,
quanto è energico, quanto è positivo di umore.

Il catalogo video occupa una certa regione di questo spazio. La domanda è
quanta parte del catalogo musicale ricada nella stessa regione, e la
risposta è: la gran parte.
```

**Che cosa il lettore può concludere**: che cosa la visuale sta mostrando, senza gergo.

**Da dove viene**: `raccomandazione.md` §2, «La seconda». Le tre caratteristiche sono nominate in italiano corrente e mai con i nomi tecnici degli assi.

---

### `BL-5-3` — perché il rettangolo è più grande della regione reale

**Dove**: fascia sotto la dispersione, secondo blocco.

```
Il rettangolo disegnato non è la forma reale della regione: è la scatola
più piccola che la contiene tutta.

Si costruisce prendendo, per ciascuna caratteristica, il valore minimo e
quello massimo fra le categorie video. Ne risulta un'area che comprende
anche combinazioni che nessuna categoria occupa davvero — il punto in cui
i punti sono radi lo mostra.

La conseguenza è che la sovrapposizione misurata è una stima per eccesso:
quella reale è minore o uguale, e questo report non misura di quanto.
```

**Che cosa il lettore può concludere**: che il valore a schermo è un tetto e non una misura puntuale — e può verificarlo guardando lo spazio vuoto dentro il rettangolo invece di doverlo accettare.

**Da dove viene**: `raccomandazione.md` §2, e il contratto di pagina §7, che fa del vuoto dentro il rettangolo un vincolo di disegno: *il vuoto fra i punti e i bordi è il limite dichiarato della condizione, reso visibile senza doverlo affermare*.

---

### `BL-5-4` — il dato del lato video è costruito

**Dove**: fascia sotto la dispersione, terzo blocco.

```
C'è una seconda ragione per cui questa condizione è la più fragile delle
tre.

Le tre caratteristiche esistono già misurate per ogni brano musicale. Per
il catalogo video non esistono: sono state assegnate categoria per
categoria da chi ha condotto l'analisi. È un dato costruito, non
osservato, e nessuna cura nella costruzione lo sposta di classe.
```

**Che cosa il lettore può concludere**: da dove viene la fragilità di questa condizione, e che non è un difetto di esecuzione ma di materiale disponibile.

**Da dove viene**: `raccomandazione.md` §2, *«C'è una seconda ragione, e riguarda l'origine del dato»*.

---

### `BL-5-5` — che cosa la condizione compra comunque

**Dove**: fascia sotto la dispersione, quarto blocco.

```
Che cosa se ne ricava, malgrado i due limiti: il catalogo musicale non è
fatto di contenuto estraneo al carattere di ciò che StreamWave già
propone. Il grosso di quella musica cade nella stessa regione, non ai
suoi margini.

E la pagina seguente dice quanto questa stima dovrebbe essere sbagliata
perché la conclusione cambi — che è il modo per giudicare se i limiti qui
sopra bastino a rovesciarla.
```

**Che cosa il lettore può concludere**: che cosa la condizione autorizza nonostante sia la più debole, e dove trovare il metro per giudicare quanto la debolezza pesi.

**Da dove viene**: **è la chiusura del rilievo `R19` della `008b`**, che il verbale descrive così: *il blocco ha conservato la parte difficile («come è costruita la regione») perdendo quella utile («di quanto il valore è gonfiato»)*. Qui la parte utile c'è, e rinvia alla pagina che la quantifica. Applicazione di `N1` e di `N1.1`.

---

### `BL-5-6` — l'asse escluso e la versione della tabella

**Dove**: didascalia della dispersione, in prossimità della visuale.

```
Il grafico mostra due delle tre caratteristiche. La terza esiste ed entra
nel calcolo: non è disegnata perché una superficie ne porta due.

Le caratteristiche del lato video sono quelle della versione corrente
della tabella di assegnazione. Se quella tabella venisse rivista, questo
valore andrebbe ricalcolato.
```

**Che cosa il lettore può concludere**: che sta guardando una proiezione e non la cosa intera, e a quali condizioni il valore scadrebbe.

**Da dove viene**: contratto di pagina §7 — obbligo di dichiarare l'asse escluso, e obbligo della terza condizione delle assegnazioni dell'analista (constitution) sulla versione della tabella di mood. Il numero di versione è a schermo come valore ancorato; questo blocco non lo scrive, per `N2`.

---

## Pagina 6 — Quanto dovrebbe sbagliare

**Spazio riservato**: fascia sotto la barra.

**Che cosa questa pagina deve fare**: dire di quanto la stima dovrebbe sovrastimare perché la seconda condizione cada — **e impedire che quel numero venga letto come una stima dell'errore**.

**È il passaggio più forte dell'intero argomento, e nella dashboard precedente non esisteva.**

### `BL-6-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
Quanto dovremmo esserci sbagliati perché la risposta cambi
```

**Che cosa il lettore può concludere**: che la pagina risponde all'obiezione che lui stesso avrebbe fatto dopo la pagina precedente.

**Da dove viene**: `raccomandazione.md` §2, «Quanto la stima dovrebbe sbagliare perché la risposta cambi». **La prima persona plurale è ammessa qui in deroga a `N7`**, e la deroga va dichiarata: la frase mette chi ha fatto l'analisi nella posizione di chi può aver sbagliato, che è precisamente ciò che questa pagina fa. Una formulazione impersonale — «quanto la stima dovrebbe sbagliare» — sposta l'errore su un oggetto e attenua la mossa.

---

### `BL-6-2` — come si legge la barra

**Dove**: fascia sotto la barra, primo blocco.

```
La barra mostra la sovrapposizione misurata sulla scala completa, da zero
a uno. La linea segna la soglia oltre la quale la condizione si considera
soddisfatta: più della metà del catalogo musicale.

La distanza fra le due è il margine, ed è ampia.
```

**Che cosa il lettore può concludere**: che cosa la visuale mostra, e che l'ampiezza che vede non è un effetto dello zoom.

**Da dove viene**: contratto di pagina §8 — *l'asse assoluto è ciò che impedisce alla barra di sembrare più o meno larga a seconda dello zoom*.

---

### `BL-6-3` — che cosa il margine dice

**Dove**: fascia sotto la barra, secondo blocco.

```
Perché la seconda condizione cadesse, la sovrapposizione reale dovrebbe
essere più bassa di quella misurata di oltre il quaranta per cento della
misura stessa.

Detto altrimenti: la stima dovrebbe essere gonfiata di quasi la metà. La
pagina precedente spiega perché è una stima per eccesso; questa dice
quanto grande dovrebbe essere l'eccesso perché cambi qualcosa.
```

**Che cosa il lettore può concludere**: di quanto l'argomento è al riparo, in una forma che può usare per decidere quanto fidarsi.

**Da dove viene**: `raccomandazione.md` §2. I due valori — margine assoluto e relativo — sono a schermo come valori ancorati; il blocco ne dà la lettura.

**Nota di forma**: «oltre il quaranta per cento» e «quasi la metà» ricadono nella **seconda categoria** di `N2.1` — il valore relativo è a schermo, ancorato, su questa pagina.

---

### `BL-6-4` — che cosa il margine non è

**Dove**: fascia sotto la barra, terzo blocco.

```
Questo numero non è una stima dell'errore. Nessuno ha misurato di quanto
la scatola ecceda la regione reale, e questo report non lo afferma.

È una condizione sull'errore: dice quanto grande dovrebbe essere
l'errore perché la conclusione si ribalti, non quanto grande sia.
```

**Che cosa il lettore può concludere**: come usare il numero senza attribuirgli una precisione che non ha.

**Da dove viene**: `raccomandazione.md` §2, *«Due letture sbagliate, che questa frase esiste per impedire»*, e il contratto di pagina §8, che ne fa la ragione d'essere della pagina.

---

### `BL-6-5` — la soglia è una stipulazione

**Dove**: fascia sotto la barra, quarto blocco, accanto alla marcatura della soglia.

```
La soglia — più della metà — non è una misura: è una lettura del termine
«maggioranza» che il criterio usa, fissata prima di guardare il valore.

Chi ritenesse che maggioranza debba significare qualcosa di più severo
troverebbe lo stesso esito con un margine più stretto. La risposta non
cambierebbe con nessuna soglia fino al valore misurato stesso: solo una
soglia più severa di così farebbe cadere la condizione.
```

**Che cosa il lettore può concludere**: che può sostituire il proprio criterio a quello adottato e vedere fin dove l'esito regge — invece di dover accettare la soglia scelta da altri.

**Da dove viene**: `raccomandazione.md` §2, *«Fin dove l'esito regge, detto con precisione perché è l'obiezione più prevedibile a questa analisi»*, e il contratto di pagina §8, che chiede che questa informazione stia sulla pagina e non in una nota. È la seconda etichetta sulla barra, non una seconda visuale.

---

## Pagina 7 — La regione di ingresso

**Spazio riservato**: fascia sotto la dispersione.

**Che cosa questa pagina deve fare**: mostrare che esiste musica insieme molto ascoltata e molto affine al catalogo attuale — e impedire che i segmenti marcati siano letti come «poco richiesti».

### `BL-7-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
Esiste musica insieme molto ascoltata e molto affine
```

**Che cosa il lettore può concludere**: che la terza condizione ha una risposta affermativa, prima di leggere la dispersione.

**Da dove viene**: `raccomandazione.md` §3, «La regione». È anche la terza condizione.

---

### `BL-7-2` — come si legge la dispersione

**Dove**: fascia sotto la dispersione, primo blocco.

```
Ogni punto è un tipo di musica. Più è a destra, più viene ascoltato; più
è in alto, più assomiglia per carattere al catalogo video di StreamWave.

Le due linee segnano le mediane: dividono i tipi di musica a metà su
ciascuna delle due scale. Il riquadro in alto a destra contiene quelli
che stanno nella metà alta su entrambe, ed è la regione da cui converrebbe
entrare.
```

**Che cosa il lettore può concludere**: come leggere la visuale e dove guardare, senza gergo statistico.

**Da dove viene**: `raccomandazione.md` §3, e il contratto di pagina §9. La glossa della mediana è quella già data a pagina 4: qui si ripete perché una pagina deve reggere l'estrazione di una schermata.

**Nota di forma — `N5`**: «viene ascoltato» e non «domanda». Da questa pagina in avanti la parola «domanda» non compare più nel significato di mercato.

---

### `BL-7-3` — che cosa questa condizione compra

**Dove**: fascia sotto la dispersione, secondo blocco.

```
Che cosa se ne ricava: la terza condizione è soddisfatta, e non di misura.
Il riquadro non contiene un caso isolato ma un gruppo consistente di tipi
di musica.

Significa che l'ingresso non dipenderebbe dall'azzeccare un genere solo:
esiste un'area di scelta, e la pagina seguente dice quali tipi la
compongono.
```

**Che cosa il lettore può concludere**: che l'argomento ha una gamba pratica, e che la scelta successiva non è un tiro secco.

**Da dove viene**: `raccomandazione.md` §3, e la decisione `CP-4`, che porta a schermo il conteggio dei membri del riquadro proprio perché *una pagina che porta `C3` senza il numero che la soddisfa lascerebbe l'esito senza il proprio metro*. Il conteggio è a schermo come valore ancorato.

---

### `BL-7-4` — i punti contro il bordo sinistro

**Dove**: fascia sotto la dispersione, terzo blocco, in prossimità della legenda delle marcature.

```
Alcuni punti sono marcati in modo distinto e stanno tutti contro il bordo
sinistro. La loro posizione non significa che quella musica sia poco
ascoltata: significa che la fonte non ha registrato quanto venga
ascoltata.

Sono due situazioni diverse che il dato non distingue, e questo report non
le confonde: quei tipi di musica non entrano in alcuna graduatoria e la
pagina seguente li tiene separati.
```

**Che cosa il lettore può concludere**: come leggere quei punti, e che l'analisi ha preso una posizione esplicita invece di lasciarli scivolare in fondo.

**Da dove viene**: contratto di pagina §9, che ne fa un obbligo di disegno: *nella dispersione cadono tutti contro il bordo sinistro, dove la posizione si legge come «domanda bassa». `kpi_measures.md` §5.3 dice esattamente il contrario, e senza marcatura la visuale affermerebbe con la propria geometria ciò che il documento vieta di affermare a parole.*

**È la chiusura del rilievo `R9` della `008b`**, che il verbale descrive così: *l'apertura «non è basso: è non misurato» si appiattisce in lettura veloce sulla formulazione esclusa*. Qui la frase non oppone due aggettivi ma due **fatti** — la fonte non ha registrato — che non si appiattiscono l'uno sull'altro.

---

### `BL-7-5` — i tipi di musica si sovrappongono

**Dove**: fascia sotto la dispersione, quarto blocco.

```
Un brano appartiene a più tipi di musica insieme. Ne discendono due
conseguenze pratiche.

Le quantità non si sommano: sommare due tipi conta due volte ciò che
appartiene a entrambi, e il totale non corrisponde a nulla.

Contare i brani non misura un mercato. Il numero di brani di un tipo dice
come il catalogo di partenza è stato campionato, non quanta musica di quel
tipo esista o quanto pubblico abbia.
```

**Che cosa il lettore può concludere**: quali operazioni su questi numeri sono lecite e quali no, prima di trovarsi la tabella davanti.

**Da dove viene**: `raccomandazione.md` §3. **La seconda parte è la chiusura di un difetto che il verbale della `008b` segnala come persistente** nel rilievo `R9`: *«la copertura del dato»* è gergo, e qui è resa come *«come il catalogo di partenza è stato campionato»*.

---

## Pagina 8 — Che cosa la regione contiene

**Spazio riservato**: fascia sotto la graduatoria.

**Che cosa questa pagina deve fare**: dare i nomi alla regione — e **impedire che la tabella si legga come una classifica di alternative fra cui scegliere**. È il vincolo più forte del contratto di pagina su qualunque pagina.

### `BL-8-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
Che cosa la regione contiene
```

**Che cosa il lettore può concludere**: che la pagina descrive un'area e non propone una scelta fra alternative.

**Nota di forma**: il titolo non è «Da dove entrare» né «I tipi di musica migliori». Entrambi affermerebbero che la pagina risponde a una domanda che il contratto dichiara mal posta.

---

### `BL-8-2` — la domanda a cui questa pagina non risponde

**Dove**: fascia sotto la graduatoria, **primo blocco, prima di ogni altro**.

```
La raccomandazione non è entrare da un tipo di musica: è entrare da
un'area del catalogo musicale, che questi nomi servono a descrivere.

I tipi di musica non sono alternative fra cui scegliere — un brano
appartiene a più di uno insieme — e trattarli come opzioni concorrenti
direbbe una cosa falsa. La prima riga non è la scelta e le altre non sono
gli scarti.
```

**Che cosa il lettore può concludere**: come usare la tabella — per caratterizzare l'area, non per selezionare una riga.

**Da dove viene**: `raccomandazione.md` §3, citata alla lettera dal contratto di pagina §10.1, che ne fa il vincolo che governa la forma della pagina. Il blocco sta **prima** della tabella nell'ordine di lettura, come `BL-8-2` prima di `BL-8-3`, perché il contratto dichiara che *va detto prima di descrivere la tabella*.

---

### `BL-8-3` — che cosa la posizione dice

**Dove**: fascia sotto la graduatoria, secondo blocco.

```
La posizione dice in quale ordine quanto una musica viene ascoltata e
quanto assomiglia al catalogo attuale si combinano più favorevolmente.
Serve a orientare una scelta di catalogo, non a sostituirla.

Che cosa se ne ricava: i tipi di musica in cima sono quelli su cui le due
grandezze convergono meglio, ed è un punto di partenza ragionevole per
comporre un'offerta — non una lista da seguire dall'alto.
```

**Che cosa il lettore può concludere**: che uso pratico può fare dell'ordine, senza scambiarlo per una prescrizione.

**Da dove viene**: `raccomandazione.md` §3, *«Come si legge questa graduatoria, e come non si legge»*. **Applicazione di `N1`**: il permesso è nella seconda metà, ed è la parte che dice al lettore che cosa fare.

---

### `BL-8-4` — il secondo blocco della tabella

**Dove**: accanto al blocco dei segmenti a domanda non misurata, sotto la tabella principale.

```
I tipi di musica qui sotto non hanno una posizione, e l'assenza è
deliberata.

Per ciascuno di essi una parte rilevante dei brani ha un livello di
ascolto registrato a zero nella fonte. Uno zero può significare che
nessuno ascolta quel brano, oppure che la fonte non ne ha rilevato
l'ascolto: il dato non distingue i due casi, e nessuna misura di questo
report può distinguerli.

Attribuire loro una posizione significherebbe costruire un ordine su
un'assenza di misura. Restano nella pagina con tutti gli altri valori,
perché quelli esistono e vanno letti.
```

**Che cosa il lettore può concludere**: perché quelle righe sono separate, e che i loro altri valori restano utilizzabili.

**Da dove viene**: contratto di pagina §10.2, che sceglie questa forma contro le due alternative ovvie: *una vista che tronca la coda non è parziale: mente per omissione*, e ordinarli insieme agli altri produrrebbe *una posizione costruita su un'assenza di misura, presentata nella stessa colonna e con la stessa forma delle posizioni costruite su una misura*.

**È la chiusura sostanziale del rilievo `R9`.** Il blocco corrispondente della `008b` era quello dichiarato «non tagliabile in nessun caso» e spiegava *con oggetti che il lettore non ha*. Qui non compaiono «le loro righe», «la mediana cade dentro quella metà», «la copertura del dato».

---

### `BL-8-5` — le due colonne che vanno lette insieme

**Dove**: didascalia della tabella, in prossimità delle colonne dell'ascolto e della quota di zeri.

```
La colonna del livello di ascolto e quella accanto vanno lette insieme:
la seconda dice quanta parte di quel tipo di musica ha un ascolto
registrato a zero, cioè quanto la prima sia affidabile.
```

**Che cosa il lettore può concludere**: che le due colonne sono una coppia, e come usarle.

**Da dove viene**: contratto di pagina §10.1, che rende l'adiacenza un obbligo: *sono due misure e non una proprio perché una misura unica renderebbe possibile portarne a schermo una sola*.

---

### `BL-8-6` — i pari merito

**Dove**: didascalia della tabella, sotto `BL-8-5`.

```
Dove due tipi di musica ottengono lo stesso risultato portano la stessa
posizione, e la successiva salta di conseguenza. Non c'è un criterio di
spareggio, perché uno spareggio per nome produrrebbe un ordine
riproducibile e arbitrario.
```

**Che cosa il lettore può concludere**: che i salti di numerazione sono voluti e che cosa significano.

**Da dove viene**: contratto di pagina §10.2, e la regola dei pari merito di `kpi_measures.md` §7.2.

---

## Pagina 9 — Quanto vale

**Spazio riservato**: fascia sotto le due tabelle, la più alta del report.

**Che cosa questa pagina deve fare**: portare gli unici numeri economici del progetto con tutte le qualificazioni che li rendono utilizzabili — e **non lasciare che il valore centrale venga preso da solo**.

### `BL-9-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
Quanto varrebbe, sotto assunzioni dichiarate
```

**Che cosa il lettore può concludere**: che sta per leggere scenari e non previsioni, prima di vedere le cifre.

**Da dove viene**: `raccomandazione.md` §4.

---

### `BL-9-2` — che cosa sono questi numeri

**Dove**: fascia sotto le tabelle, primo blocco.

```
Questi non sono misure: sono scenari, costruiti su un valore di
riferimento esterno e su assunzioni dichiarate. La loro confidenza è
bassa.

Ne discende una regola che vale su tutta la pagina: si leggono come terna,
mai un valore per volta. Prendere quello centrale perché sta meglio in una
slide comunica una certezza che il dato non ha.
```

**Che cosa il lettore può concludere**: come portare via questi numeri senza deformarli.

**Da dove viene**: `raccomandazione.md` §4, e il principio I, che impone il range per la confidenza bassa. Il contratto di pagina §11 lo dichiara *strutturale, non una raccomandazione*.

---

### `BL-9-3` — l'orizzonte e le due unità

**Dove**: fascia sotto le tabelle, secondo blocco.

```
I valori si riferiscono a dodici mesi dal lancio.

Il tasso di adozione è lordo: dice quanti passerebbero all'offerta
musicale, non il saldo fra chi la adotta e chi lascia il servizio. Le
disdette sono fuori dal perimetro di questa analisi.

Il ricavo aggiuntivo è un livello mensile a regime, non un cumulato: è il
valore raggiunto a fine periodo e mantenuto, non la media dei dodici mesi
— nei primi sarebbe minore — e non un totale annuo.
```

**Che cosa il lettore può concludere**: che cosa esattamente misurano le due righe della tabella, in una forma che può usare senza sbagliare l'ordine di grandezza.

**Da dove viene**: `raccomandazione.md` §4. **È la chiusura del rilievo `R7` della `008b`** — *i numeri di BQ3 non sono usabili perché l'orizzonte non è a schermo, ed è definito circolarmente* — e riprende la formulazione che il verbale isola come funzionante: *«Non è un totale cumulato sul periodo e non è un dato annuo: nei primi mesi sarebbe minore.» Concreto, immediatamente utilizzabile, e chiude tre fraintendimenti in una riga.*

**Nota di forma**: «dodici mesi» ricade nella **prima categoria** di `N2.1`. È l'orizzonte dichiarato dalla feature `004`, non un'osservazione sui dati, ed è nella stessa categoria delle soglie.

---

### `BL-9-4` — come si usa il fattore di conversione

**Dove**: fascia sotto le tabelle, terzo blocco, accanto alla seconda tabella.

```
La seconda tabella esprime la stessa terna su un'unità dichiarata: che
cosa quei valori diventano ogni centomila abbonati.

Chi conosce la base di StreamWave la divide per centomila e moltiplica i
tre importi. L'operazione resta sua, e il risultato eredita per intero la
confidenza bassa della terna: va portato avanti come terna, non come
numero.

Questo report non quantifica la base di StreamWave e non offre alcuna
chiave per farlo. Non è un presidio: è una rinuncia, e non impedisce a
valle l'operazione che scoraggia.
```

**Che cosa il lettore può concludere**: come ricavare il valore per la propria azienda, che è l'unica operazione che questi numeri autorizzano.

**Da dove viene**: `raccomandazione.md` §4, e il contratto di pagina §11, che impone la **formulazione stretta** e vieta esplicitamente «l'uplift non è scalabile». **È la chiusura del rilievo `R8` della `008b`**, che segnalava la ricetta della moltiplicazione consegnata *senza il presidio che la qualificava*: qui il presidio è nella stessa frase.

**Nota di forma**: «centomila» in lettere è la lettura dell'unità dichiarata a schermo nell'intestazione della tabella. Ricade nella seconda categoria di `N2.1`.

---

### `BL-9-5` — che cosa di questo numero non si può verificare

**Dove**: fascia sotto le tabelle, quarto blocco.

```
Il valore centrale del tasso di adozione non è una misura di questo
progetto: è un dato pubblicato su un altro operatore, ripreso tale e
quale da un comunicato stampa del 2018.

Quel comunicato non nomina lo studio da cui la cifra proviene e non
dichiara la numerosità del campione. Si può constatare che la cifra sia
stata pubblicata; non si può giudicare come sia stata misurata.

C'è di più, ed è lo scarto di cui si conosce il verso: quella cifra
misurava quanti abbonati si trovavano sul piano più caro a un certo
istante, e qui viene usata per stimare quanti ci passerebbero entro un
anno. Una composizione accumulata negli anni sta strutturalmente sopra il
flusso che le si fa rappresentare, e lo scenario centrale è quindi
probabilmente ottimista.
```

**Che cosa il lettore può concludere**: in quale direzione il numero è probabilmente sbagliato — che è più utile di sapere soltanto che è incerto.

**Da dove viene**: `raccomandazione.md` §4, «Un debito aperto, dichiarato qui perché è qui che pesa», e il contratto di pagina §11, che impone che il debito della `004` sia dichiarato dove i numeri compaiono.

**Il titolo «Un debito aperto» non è usato**, ed è la chiusura del rilievo `R4` della `008b`: *«debito» è gergo di repository, e su una pagina di impatto economico sarà letto come una passività*. Il blocco non ha titolo proprio; se lo strumento ne richiedesse uno, è `Che cosa di questo numero non si può verificare`.

---

### `BL-9-6` — il richiamo del secondo prestito

**Dove**: chiusura della pagina.

```
Il valore di riferimento descrive un altro operatore, su un altro mercato,
alcuni anni prima, in un'offerta in cui il piano caro si distingueva per
numero di schermi e qualità video, non per un tipo di contenuto in più.

Che sia trasferibile a StreamWave è dichiarato e non verificabile con i
dati disponibili. Vale per i numeri di questa pagina e per nessun altro
del report.
```

**Che cosa il lettore può concludere**: la portata circoscritta di questo limite, invece di estenderlo a tutto il report.

**Da dove viene**: `raccomandazione.md` §4, e il contratto di pagina §11, che chiede il richiamo qui perché *`A6` si applica solo ai valori di questa pagina, e una pagina di scenari che non lo ricordasse lascerebbe l'assunzione a tre schermate di distanza dai soli numeri che tocca*.

---

## Pagina 10 — Che cosa lo ribalterebbe

**Spazio riservato**: **l'intera pagina**, che è di sola prosa.

**Che cosa questa pagina deve fare**: dichiarare a quali condizioni la raccomandazione si ribalterebbe, e che cosa non si può concludere — **senza riassumere**. Il contratto di pagina §12 lo dice con precisione: *la ripetizione in coda a un argomento è il punto in cui una raccomandazione si ammorbidisce: si riassume, e riassumendo si perde la qualificazione*.

**Vincolo di forma** (contratto di pagina §12 e §14): l'articolazione **condizione → conseguenza**, una per riga, come struttura visibile. **Nessuna visuale**, e in particolare nessuna barra dei rischi ordinata per gravità.

### `BL-10-1` — il titolo della pagina

**Dove**: intestazione della pagina.

```
A quali condizioni questa risposta cambierebbe
```

**Che cosa il lettore può concludere**: che la pagina gli dà gli strumenti per contestare il verdetto, non una sintesi.

**Da dove viene**: `raccomandazione.md` §5, che apre con *una raccomandazione che non dichiari le condizioni alle quali si ribalterebbe è un'opinione*.

---

### `BL-10-2` — l'apertura

**Dove**: parte alta della pagina, sopra l'articolazione.

```
Una raccomandazione che non dichiari a quali condizioni si ribalterebbe è
un'opinione. Queste sono quelle condizioni, e per ciascuna è scritto che
cosa succederebbe — non soltanto che un rischio esiste.
```

**Che cosa il lettore può concludere**: come leggere le righe che seguono, e che ciascuna porta una conseguenza e non un allarme generico.

**Da dove viene**: `raccomandazione.md` §5, alla lettera. Il contratto di pagina §12 fa della seconda metà un vincolo di disegno: *per ciascuna condizione è scritto che cosa succederebbe, non soltanto che un rischio esiste, e la struttura a due colonne è ciò che rende visibile che la seconda metà c'è sempre*.

---

### `BL-10-3` — le quattro condizioni di ribaltamento

**Dove**: l'articolazione condizione → conseguenza, una per riga. Il testo di ciascuna colonna è quello qui sotto.

**Prima riga:**

```
Se la tabella che assegna il carattere alle categorie video venisse
rivista

→ La seconda condizione andrebbe ricalcolata da capo, e con essa la
risposta. Non è un rischio remoto: è il modo normale in cui quella tabella
evolve, e chiunque la riveda deve rifare quel passaggio prima di citare
questo report.
```

**Seconda riga:**

```
Se la sovrastima fosse maggiore del margine

→ La seconda condizione cadrebbe e l'esito passerebbe da tre condizioni
su tre a due: sostegno parziale, non «argomento non sostenuto».
L'espansione resterebbe difendibile, con la condizione mancante da
indicare come rischio esplicito.
```

**Terza riga:**

```
Se i cataloghi sostitutivi non rappresentassero StreamWave

→ Nessuna delle tre condizioni direbbe più nulla su StreamWave, per quanta
cura sia stata messa nel calcolarle. Non è verificabile con i dati
disponibili: si chiude soltanto rifacendo l'analisi sui dati reali
dell'azienda, ed è la prima cosa da fare se questo report viene preso sul
serio.
```

**Quarta riga:**

```
Se arrivassero dati che il progetto non ha

→ Dati su che cosa gli abbonati guardano davvero sostituirebbero
l'assunzione di rappresentatività con un'osservazione. Dati di costo non
toccherebbero la coerenza ma potrebbero rendere l'operazione
insostenibile. Dati più recenti potrebbero raccontare un'altra storia.
```

**Che cosa il lettore può concludere**: per ciascuna condizione, che cosa accadrebbe alla risposta — e nella terza riga, l'azione concreta che chiuderebbe il limite più importante.

**Da dove viene**: `raccomandazione.md` §5 e il contratto di pagina §12, che fissa le quattro coppie. La seconda riga porta la distinzione che il business case impone fra *sostegno parziale* e *argomento non sostenuto*, e che il contratto dichiara vada mantenuta visibile.

---

### `BL-10-4` — il richiamo dei due prestiti

**Dove**: parte bassa della pagina, blocco proprio.

```
Due limiti valgono su tutto ciò che precede, e vanno ripetuti qui perché
chi arriva da questa pagina li incontri comunque.

I numeri di questo report non descrivono StreamWave. Al posto dei due
cataloghi dell'azienda ne sono stati usati altrettanti, pubblici: il
catalogo video di Netflix e un estratto di Spotify. Che siano
rappresentativi è dichiarato e non verificato.

Il valore di riferimento economico descrive un altro operatore, su un
altro mercato, alcuni anni prima, e tocca soltanto la pagina che stima
quanto varrebbe l'operazione.

Nessuno dei due entra nella scala di confidenza dei numeri: quella
scala dice quanto un numero è solido, non se parli di StreamWave.
```

**Che cosa il lettore può concludere**: i due limiti strutturali, per esteso, anche se ha ritagliato soltanto questa schermata.

**Da dove viene**: contratto di pagina §12, che ne fa un obbligo esplicito e ne spiega la ragione: *un richiamo che dicesse «vedi le assunzioni di pagina 3» lascerebbe chi ritaglia questa schermata senza il limite più importante del report*.

**Perché è un richiamo e non una reintroduzione.** La trattazione è a pagina 3, raggiungibile con un passaggio dalla barra di navigazione. Il contratto §5 argomenta che *ciò che la ripetizione compra nel documento — che il limite raggiunga chi arriva dal fondo — a schermo lo compra la navigazione*, e che il richiamo deve comunque **nominare i due prestiti per esteso** invece di rinviarvi con un'etichetta.

---

### `BL-10-5` — che cosa questo report non è

**Dove**: parte bassa della pagina, elenco strutturato.

```
Non è un business case finanziario. Manca interamente il lato dei costi —
licenze, infrastruttura, organico, marketing — ed è una scelta di
perimetro, non una dimenticanza. I numeri della pagina sull'impatto non
ne sono una versione parziale: sono ricavi potenziali senza il proprio
contraltare.

Non dice che il pubblico attuale vorrebbe la musica. La somiglianza
misurata è fra caratteristiche di contenuto, non fra persone osservate:
dice che la musica assomiglia per carattere al catalogo video, non che
chi guarda quel catalogo ascolterebbe quella musica. Nessun dato sui
comportamenti è entrato in questa analisi.

Non è una previsione. Gli scenari sono costruiti sotto assunzioni
dichiarate, non stime di ciò che accadrà. La banda fra pessimista e
ottimista non dice con quale probabilità il valore vero vi cada, e
nemmeno la sua ampiezza misura quanto siamo incerti: una banda più
stretta non significherebbe più fiducia.
```

**Che cosa il lettore può concludere**: quali domande restano aperte, e quindi quali decisioni questo report non può sostenere da solo.

**Da dove viene**: `raccomandazione.md` §6. La terza voce riprende la formulazione che il verbale della `008b` isola come funzionante — *«Chiedere con quale probabilità il valore vero cada dentro la banda è una domanda a cui questi numeri non rispondono»* — nella forma che parla al lettore invece che del numero.

---

### `BL-10-6` — la copertura temporale

**Dove**: chiusura della pagina.

```
I dati del catalogo video arrivano al 2021. Quelli del catalogo musicale
sono dichiarati al 2022 dalla fonte, che però non espone alcuna data
verificabile: è un'informazione presa dalla documentazione, non osservata
sui dati. Il valore di riferimento economico risale al 2018.

Il mercato del music streaming si è mosso da allora.
```

**Che cosa il lettore può concludere**: quanto è vecchio ciò che ha letto, con la distinzione fra ciò che è stato osservato e ciò che è stato dichiarato.

**Da dove viene**: contratto di pagina §12, che impone la distinzione di statuto: *il catalogo musicale non espone alcun campo di data: il suo anno è un'affermazione presa dalla documentazione della fonte, e il profilo dei dati dichiara esplicitamente di non poterla verificare. È una differenza di statuto fra i due anni, e appiattirla a schermo affermerebbe che entrambi sono osservati.*

**È anche la chiusura del rilievo `R14` della `008b`** — *nessun blocco dice che i dati sono vecchi* — che qui sta nella pagina finale invece che a piè di schermo.

**Nota di forma**: l'anno del catalogo video è a schermo come **valore ancorato**; gli altri due sono nel testo perché non sono ancorabili, e sono le voci dichiarate a `N2`.

---

# Parte III — Le verifiche di questo contratto

Da eseguire **su questo documento**, prima che il testo vada a schermo, e da rieseguire a schermo dopo la costruzione.

## V1 — Zero limiti orfani

Per ciascun limite scritto, cercare sulla stessa pagina il permesso che gli sta accanto. È la tabella di §8, compilata.

## V2 — Nessuna cifra fuori dalla lista chiusa

Scandire i blocchi delimitati e verificare che ogni numerale ricada in `N2` o in `N2b`.

## V3 — Nessuna formulazione esclusa

Cercare le sette voci di `N4` nei blocchi delimitati. **Esito atteso: nessuna occorrenza.**

## V4 — La parola «domanda»

Verificare che dalla pagina 4 in avanti non compaia nel significato di mercato (`N5`).

## V5 — Ogni blocco di prosa finisce con un punto

È il rilievo `R22` della `008b`: *quattro blocchi finiscono senza punto, dentro caselle che scorrono: chi vede un testo finito non sa che è finito.*

**I titoli di pagina sono esclusi**, ed è la lettura letterale del rilievo: il difetto riguardava blocchi di prosa dentro caselle che scorrono, dove il punto finale è il solo segnale che il testo non è troncato. Un titolo non scorre e non porta punto.

## V6 — Nessuna sigla non sciolta

Verificare che `C1`, `C2`, `C3` non compaiano nei blocchi delimitati, e che `BQ1`, `BQ2`, `BQ3` non compaiano affatto (`N3`).

---

## Esito delle verifiche su questo documento

Eseguite sul testo prima che vada a schermo. **Vanno rieseguite a schermo dopo la costruzione**, perché ciò che è stato scritto e ciò che sta a schermo sono due cose diverse, e la seconda è quella che il lettore incontra.

| Verifica | Esito | Note |
|---|---|---|
| `V1` — zero limiti orfani | **verde** | ventotto limiti, ciascuno con il proprio permesso. Due lo hanno in un blocco diverso della stessa pagina, dichiarati in §8 |
| `V2` — nessuna cifra fuori dalle categorie ammesse | **verde** | la terza categoria di `N2.1` — fatto misurato scritto solo in prosa — è **vuota**. Gli anni della lista chiusa compaiono solo dove `N2` li ammette |
| `V3` — nessuna formulazione esclusa | **verde** | nessuna delle sette voci di `N4` compare nei blocchi delimitati |
| `V4` — la parola «domanda» | **verde** | non compare nel significato di mercato dopo la pagina 4. Le pagine 7 e 8 usano il lessico dell'ascolto |
| `V5` — ogni blocco di prosa finisce con un punto | **verde** | i nove blocchi senza punto sono tutti titoli di pagina, esclusi dalla regola |
| `V6` — nessuna sigla non sciolta | **verde** | `C1`, `C2`, `C3` non compaiono nei blocchi; `BQ1`, `BQ2`, `BQ3` non compaiono affatto |

### Il difetto trovato e corretto durante la stesura

**`N2.1` è stato riscritto.** La prima versione vietava ogni numerale in lettere, copiando la regola della `008b`; la verifica `V2` ha trovato che **il testo stesso la violava in una ventina di punti**.

Non era sciatteria di stesura: un report costruito su **tre condizioni** non può nominarle senza contarle. La regola era sbagliata, non il testo. È stata sostituita dalla regola a tre categorie di §2.1, e la sostituzione è dichiarata lì insieme alla ragione per cui la regola della `008b` funzionava per quella dashboard e non per questo report.

**Perché è registrato qui invece di essere corretto in silenzio.** Una regola riscritta perché il testo la violava è esattamente il caso in cui chi scrive potrebbe aver ammorbidito il vincolo per far passare il proprio lavoro. Dichiararlo è ciò che rende la sostituzione contestabile: chi la contesta ha davanti sia la regola vecchia sia la ragione del cambio.

### Che cosa queste verifiche non certificano

**Che il testo sia comprensibile al destinatario.** Nessuna delle sei lo misura: sono verifiche di forma. Contro quel difetto esiste solo la revisione in contesto pulito, ed è la ragione per cui il perimetro della revisione di questa feature include il contratto di narrazione.

**Che il testo entri negli spazi riservati.** Si accerta a schermo, e uno scostamento si dichiara nell'esito della costruzione.
