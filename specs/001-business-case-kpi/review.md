# Verbale di revisione indipendente — `docs/business_case.md`

**Data**: 2026-08-07
**Oggetto**: business case "Ingresso di StreamWave nel music streaming"
**Natura della revisione**: contesto pulito. Il revisore non ha scritto il documento e non ne conosce la storia. È stato letto **esclusivamente** `docs/business_case.md`. Non sono stati aperti spec, plan, research, data-model, quickstart, tasks, README, constitution; non è stato consultato il log git; non sono stati ispezionati i dataset. La Prova 2 è stata eseguita per prima, su un estratto delle sole righe di formula, e le otto interpretazioni cieche sono state fissate per iscritto **prima** di aprire il documento.

**Esito complessivo**: **le tre prove sono superate**. Il documento si regge da solo: un lettore che non abbia altro in mano capisce quale decisione supporta, per chi, con quali misure e con quanta fiducia, e non ne ricava alcuna raccomandazione sull'espansione. La tenuta non è però uniforme. Le formule sono leggibili in isolamento nella loro aritmetica, ma tre di esse contengono un operatore centrale che il documento non definisce da nessuna parte, e l'unità di analisi dell'intera seconda domanda di business — il "segmento" — non è mai definita. Il rilievo più serio non riguarda la chiarezza ma l'architettura del giudizio: la scala di confidenza misura la distanza fra dato e numero ma ignora l'assunzione A1, che è la sola su cui poggia il fatto che questi numeri riguardino StreamWave. Il documento è sopra la media per disciplina metodologica e per onestà dichiarativa; i suoi punti deboli sono concentrati nel passaggio da definizione a calcolo, cioè esattamente dove la feature successiva dovrà lavorare.

---

## Prova 2 — Leggibilità delle formule in isolamento

**Esito: SUPERATA (8 formule su 8 coincidono, 100% contro una soglia dell'80%)**

### Metodo

Estrazione delle sole righe `**Formula concettuale**` via grep, senza aprire il file. Per ciascuna riga sono stati scritti calcolo descritto, granularità presunta e ambiguità residue. Solo dopo il documento è stato letto integralmente e ogni interpretazione confrontata con la scheda di appartenenza.

### Esiti per formula

| Sigla | Esito | In cosa diverge / cosa la scheda ha dovuto aggiungere |
|---|---|---|
| `BQ1-K1` | **coincide** | Nessuna divergenza su calcolo e granularità. La scheda risolve il denominatore (titoli distinti, non assegnazioni di categoria), che dalla sola formula era ambiguo; resta non risolto se il numeratore conti i titoli con la categoria musicale come primaria o come una qualunque delle sue categorie. |
| `BQ1-K2` | **coincide** | Ho letto correttamente l'esclusione delle serie e ho segnalato come ambiguo il trattamento dei duplicati sul lato musicale: la scheda lo chiude con "traccia deduplicata". Restano impliciti il segno della differenza e il trattamento dei film privi di durata. |
| `BQ1-K3` | **coincide** | Calcolo e granularità (traccia deduplicata) come previsto. Le due ambiguità che avevo sollevato — cosa sia l'"intervallo occupato" (min-max? percentili?) e se la condizione valga per asse o congiuntamente sui tre — **non sono risolte né dalla scheda né da §5.3**. La formula resta non calcolabile senza una decisione ulteriore. |
| `BQ2-K1` | **coincide, con riserva sulla nomenclatura** | Il calcolo (mediana dell'indice di popolarità sulle tracce del segmento, duplicati rimossi) coincide. La scheda dichiara però "coppia traccia-segmento per l'appartenenza, traccia deduplicata per il calcolo": una granularità ibrida che non è nessuna delle due di §5.2, dove la deduplicazione è riservata ai "totali di catalogo" e una mediana per segmento non lo è. Vedi R7. |
| `BQ2-K2` | **coincide** | Complemento a 1 della distanza, segmento contro un profilo mediano unico del catalogo video: previsto correttamente. Le ambiguità che avevo sollevato — quale metrica di distanza, su quale massimo si normalizza, come si ottiene un profilo di mood del catalogo video — **non sono risolte in nessun punto del documento**. |
| `BQ2-K3` | **coincide** | Combinazione pesata di K1 e K2 con pesi esterni alla formula, output ordinale: previsto. Non risolta la mia obiezione sulla eterogeneità delle scale (0-100 contro 0-1) e sulla trasformazione necessaria prima di pesare. Emerge inoltre un conflitto con §4 (vedi R5) che dalla sola formula non era visibile. |
| `BQ3-K1` | **coincide** | Avevo letto la misura come input di scenario e non come stima, e avevo segnalato come ambiguo se la base utenti sia quella al lancio o una media: A5 la fissa al parco abbonati al lancio, assunto stabile. Il churn resta fuori dal modello senza menzione esplicita. |
| `BQ3-K2` | **coincide** | Avevo segnalato che il prodotto di due soli fattori non produce un valore monetario totale e che serviva un terzo fattore, oppure una lettura per-utente: la riga `Unità` ("euro per utente al mese") chiude l'ambiguità nel secondo senso. È il caso in cui la **formula da sola era genuinamente bivalente** e a disambiguarla è un campo diverso della scheda. |

### Lettura dell'esito

La soglia è ampiamente superata e questo è un risultato reale: otto formule su otto sono state ricostruite correttamente da un lettore che non aveva visto né la scheda né il resto del documento, il che significa che il testo delle formule è denso ma non ellittico e che le sigle richiamate (`BQ2-K1`, `A4`, `§5.3`) sono sufficienti a orientare senza spiegazione.

L'esito va però letto per quello che è. "Coincide" qui significa che l'interpretazione cieca e la scheda dicono la stessa cosa; **non** significa che la formula sia eseguibile. Su `BQ1-K3`, `BQ2-K2` e `BQ2-K3` le ambiguità che avevo annotato in cieco sono sopravvissute alla lettura integrale: il documento e io concordiamo sul fatto che la misura sia una quota dentro un intervallo, un complemento di distanza e una combinazione pesata, e concordiamo anche nel non sapere quale intervallo, quale distanza e quale combinazione. Tre KPI su otto sono quindi definiti fino al livello del concetto e non oltre. Per un documento che dichiara di definire il metro prima di misurare, questo è il confine esatto di ciò che ha effettivamente definito.

---

## Prova 1 — Comprensione dell'inquadramento

**Esito: SUPERATA**

Le risposte che seguono sono state formulate dopo una sola lettura integrale, senza consultare altro e senza aver avuto bisogno di porre domande di chiarimento.

**Decisione supportata e destinatario.** Il documento deve supportare la decisione se aprire un secondo verticale di business, lo streaming musicale, accanto a quello video esistente (§1). Il destinatario è il board di StreamWave, di cui il documento presuppone competenza di business ma non competenza tecnica o statistica; il vincolo dichiarato è che ogni misura sia contestabile da un membro del board senza che sappia come verrà calcolata. Il documento è esplicito nel non essere la valutazione ma la definizione di come si valuterà: non contiene risultati né raccomandazione.

**North Star metric.** È `BQ1-K1` `music_adjacent_catalog_share`, la quota di catalogo video già a contenuto musicale. La motivazione dichiarata è duplice. Sul piano del merito, il criterio di successo deve essere una misura di coerenza strategica: se il pubblico esistente mostra già appetito per il contenuto musicale l'espansione è un'estensione del catalogo, altrimenti è l'ingresso in un mercato estraneo. Sul piano metodologico, è l'unica misura del framework osservata direttamente, senza mappature interpretative né dati simulati, e quindi l'unica che può reggere confidenza alta e presentarsi come valore puntuale. Le alternative sono scartate con motivazioni distinte: `BQ3-K2` (uplift dell'ARPU) parlerebbe la lingua del board ma poggia su dati simulati, e eleggere a criterio ufficiale un numero non osservato darebbe autorevolezza a un'assunzione; `BQ1-K3` (sovrapposizione dei mood) è concettualmente più ricca ma richiede una tabella di corrispondenza costruita dall'analista, che la ferma a confidenza media; un indice composito coerenza + impatto è escluso per principio, perché fonderebbe un dato osservato e una simulazione in una cifra sola nascondendo che le due metà non meritano la stessa fiducia.

**Cosa il progetto non risponderà.** Il documento ne elenca sei in §8; le più rilevanti sono: (a) **quanto costa costruire il verticale musicale**, perché non esiste alcun dato su licenze, infrastruttura o organico, il che rende questo un business case di opportunità e non finanziario — chi vi cercasse un ritorno sull'investimento non lo troverà; (b) **se il pubblico attuale vorrebbe la musica**, perché non esiste alcun dato comportamentale o di sondaggio e la sovrapposizione misurata da BQ1 è tra caratteristiche di contenuto, non tra persone. Si aggiungono: la dimensione assoluta del mercato di un segmento (il campione ha lo stesso numero di tracce per segmento, quindi qualunque dimensionamento dal lato offerta misurerebbe il campionamento), il confronto fra formato seriale e musica, il prezzo ottimale del tier premium, e qualunque dinamica di mercato successiva al 2022.

**Cosa è rimasto oscuro.** La prova è superata, ma tre cose restano non ricostruibili dal documento e le segnalo perché sono esattamente il tipo di informazione che serve:

1. **Cosa sia un "segmento"**. §4 lo scrive come "segmento musicale (genere/mood)", con una barra che lascia aperte due letture incompatibili: un genere del catalogo di origine, oppure un raggruppamento derivato per profilo di mood. Tre KPI su otto (`BQ2-K1`, `BQ2-K2`, `BQ2-K3`) e un'intera domanda di business poggiano su questa unità di analisi, che non viene mai definita. §5.2 la usa come primitiva ("il catalogo musicale assegna una traccia a più segmenti"), il che suggerisce la prima lettura, ma non lo dichiara.
2. **Quale valore della North Star conta come basso**. Il documento afferma che il framework è costruito per poter produrre anche una risposta negativa e che una North Star bassa è un risultato e non un fallimento, ma non fissa alcuna soglia, alcun intervallo di riferimento e alcun benchmark. Fissare il metro senza fissare il punto di rottura lascia in piedi metà del problema che §1 dichiara di voler risolvere.
3. **La dimensione della base utenti**. A5 la assume stabile ma non la quantifica, il che è coerente con A3 ma implica che `BQ3-K2` resti leggibile solo in euro per utente al mese e non sia convertibile in un impatto aggregato. Il documento non lo dice.

---

## Prova 3 — Tenuta del perimetro

**Esito: SUPERATA**

**Risposta alla domanda posta**: il documento **non contiene alcuna raccomandazione** sull'espansione nel music streaming e non consente di derivarne una. Non dice se StreamWave debba entrare nel mercato musicale, e non contiene alcun elemento — numero, stima, tendenza, giudizio — da cui una risposta possa essere estratta, nemmeno implicitamente.

Il perimetro è difeso in quattro punti indipendenti, il che è più di quanto serva e va riconosciuto come una scelta deliberata:

- il cappello introduttivo dichiara che il documento definisce *come* si valuterà, non la valutazione, e che non contiene risultati, stime calcolate né una raccomandazione;
- §8 "Inferenze da evitare" anticipa esplicitamente l'errore: "che questo framework dimostrerà la convenienza dell'espansione. È costruito per poter produrre anche una risposta negativa, ed è progettato esplicitamente per non impedirla";
- la "Regola sui numeri di questo documento" classifica ogni numero presente come assunzione di scenario o caratteristica dichiarata dei dati di origine, entrambe input e mai esiti, e chiude con "nessun numero di questo documento risponde a BQ1, BQ2 o BQ3";
- la direzione della North Star è dichiarata in modo simmetrico ("valore alto = maggiore coerenza dell'espansione") e §3 esplicita entrambi i rami, incluso quello negativo: "se non lo mostra, è l'ingresso in un mercato estraneo, con tutti i costi di acquisizione che comporta".

Ho cercato attivamente inclinazioni implicite e ne segnalo tre, nessuna delle quali arriva a costituire una raccomandazione, ma due delle quali meritano di essere viste:

- **§2 A4** motiva il modello a due tier con "è il pattern prevalente quando una piattaforma video aggiunge un verticale adiacente". L'aggettivo "adiacente" è qui usato come dato di fatto, mentre l'adiacenza è precisamente ciò che la North Star deve accertare. È una petizione di principio locale, contenuta e non decisiva, ma è nel testo.
- **BQ2 presuppone l'ingresso.** La domanda "quale segmento rappresenterebbe l'opportunità di ingresso più coerente" ha senso solo se si entra; il condizionale la tiene formalmente aperta, ma tre KPI su otto sono dedicati a *come* entrare e nessuno all'alternativa di non entrare o a un controfattuale (per esempio: lo stesso investimento sul verticale video). Questo non produce una conclusione, ma restringe lo spazio delle risposte che il framework può articolare: il documento può dire "l'adiacenza è debole" e può dire "il segmento X è il migliore", ma non ha alcuna misura che dica "meglio non entrare".
- **§7** contiene l'unica frase normativa del documento: "la decisione del board dovrebbe considerare lo scenario *worst* come il caso da poter sostenere, non lo scenario *best* come il caso da aspettarsi". È una prescrizione su come leggere un intervallo, non sull'esito, ed è semmai conservativa; non la considero una violazione del perimetro, ma è una raccomandazione di metodo decisionale rivolta al board, e come tale va notata in un documento che dichiara di non raccomandare nulla.

---

## Rilievi

In ordine di gravità decrescente.

### R1 — La scala di confidenza non valuta A1, che è l'assunzione su cui poggia tutto

**Riferimento**: §2 A1 (righe 19-26), §6 (righe 286-298), scheda `BQ1-K1` (riga 168).

§6 definisce la confidenza come "quanti strati interpretativi separano il dato osservato dal numero mostrato". Applicata così, `BQ1-K1` prende confidenza alta perché "la classificazione è assegnata dalla fonte e viene solo letta; nessuna mappatura né assunzione interposta". Ma fra il dato e la decisione del board c'è A1, che è un'assunzione interposta e non è né piccola né verificabile: il catalogo Netflix *rappresenta* il catalogo di StreamWave. La quota di titoli musicali è quindi misurata con confidenza alta **su Netflix** e con confidenza indeterminata **su StreamWave**, che è l'unico soggetto della decisione. Il documento è consapevole del problema e lo dichiara con onestà a riga 26 ("nessuna delle conclusioni descrive letteralmente StreamWave"), ma la dichiarazione vive in §2 e non entra mai nella scala che governa come i numeri saranno presentati. L'effetto pratico è che l'unica metrica autorizzata a comparire come valore puntuale in cima a una dashboard è quella la cui validità dipende interamente da un'assunzione che la scala non pesa. A1 è per costruzione irrefutabile con i dati disponibili, il che secondo il criterio della riga 294 la collocherebbe fra le assunzioni da confidenza bassa.

### R2 — Nessuna soglia decisionale è dichiarata ex ante, per nessun KPI

**Riferimento**: §1 (riga 13), §3 (righe 63-72), §8 "Inferenze da evitare" (riga 323).

§1 fonda l'intero documento su un principio: "definire il metro prima di misurare è ciò che impedisce di scegliere, a risultati noti, la misura che dà la risposta desiderata". Il principio è rispettato per metà. Il metro è fissato — quali misure, con quale formula, con quanta fiducia — ma il punto di rottura no: non esiste un valore di `BQ1-K1` sotto il quale l'adiacenza si consideri assente, non esiste un livello di `BQ3-K2` nello scenario worst sotto il quale l'iniziativa non regga, non esiste un criterio che dica quanti segmenti del quadrante alto/alto siano abbastanza. §8 afferma che "una North Star bassa è un risultato, non un fallimento della misura", ma senza una soglia la parola "bassa" non ha referente. La conseguenza è che la scelta di cosa conti come esito negativo resta disponibile *dopo* aver visto i numeri, che è esattamente il rischio che §1 dichiara di voler chiudere. È il rilievo che raccomando di sanare per primo, perché è a costo quasi nullo: basta una riga per KPI, scritta ora.

### R3 — §6 dichiara la classificazione riproducibile dalla formula, e `BQ2-K1` lo smentisce

**Riferimento**: §6 (riga 288) contro scheda `BQ2-K1` (righe 212 e 216).

§6 afferma che il criterio "è verificabile leggendo la formula concettuale della scheda: chiunque può applicarlo e arrivare alla stessa classificazione". Ho verificato l'affermazione nelle condizioni ideali, cioè leggendo le formule in isolamento prima di tutto il resto. Su `BQ2-K1` il test fallisce: la formula dice "indice di popolarità mediano delle tracce del segmento, calcolato sulle tracce deduplicate del segmento", che è una lettura diretta di un attributo osservato senza alcuna mappatura, e applicando il criterio di riga 292 un lettore la classificherebbe **alta**. La scheda la classifica media, e la ragione — "usarlo come proxy della domanda di mercato è un'assunzione dichiarata" — non compare nella formula ma solo nel campo Confidenza. L'assunzione è nel salto fra il nome della misura (`segment_demand_index`) e ciò che la formula calcola (una mediana di popolarità), cioè in un punto che la formula per costruzione non mostra. Il rilievo non è sulla classificazione, che è corretta e prudente: è sulla promessa di riproducibilità, che è più forte di quanto il framework possa mantenere e che andrebbe riformulata ("verificabile leggendo la scheda" anziché "la formula").

### R4 — "Segmento" non è mai definito

**Riferimento**: §4 BQ2 (riga 92), §5.2 (riga 112), schede `BQ2-K1`, `BQ2-K2`, `BQ2-K3`.

L'unica occorrenza definitoria è "segmento musicale (genere/mood)": una barra fra due nozioni che non coincidono. Se il segmento è un genere dichiarato dalla fonte, allora è un dato osservato e `BQ2-K1` eredita confidenza dalla fonte; se è un raggruppamento derivato per profilo di mood, allora è costruito dall'analista, dipende dalla tabella di §5.3 e trascina `BQ2-K1` allo stesso strato interpretativo di `BQ2-K2`, rendendo per giunta parzialmente circolare l'affinità (si misurerebbe la distanza di mood di un raggruppamento definito per mood). Le due letture producono due framework diversi. Il documento chiede al board di contestare le misure senza sapere come si calcolano: qui il board non può, perché non sa cosa viene ordinato.

### R5 — Due regole di selezione incompatibili per BQ2

**Riferimento**: §4 BQ2 (riga 94) contro scheda `BQ2-K3` (riga 244).

§4 formula la domanda in termini di quadranti: "quali segmenti si collocano nel quadrante ad alta domanda e alta affinità", una selezione congiuntiva in cui un segmento eccellente su un asse e pessimo sull'altro viene escluso. `BQ2-K3` la implementa come "combinazione della loro domanda relativa e della loro affinità con il catalogo, con il peso relativo dei due criteri dichiarato esplicitamente", cioè uno scalare pesato in cui un asse compensa l'altro. Le due regole ordinano diversamente lo stesso insieme di segmenti e possono selezionare candidati differenti. Va scelta una delle due, o dichiarato che il quadrante è il filtro e la combinazione pesata l'ordinamento interno al filtro.

### R6 — Tre formule lasciano indefinito il proprio operatore centrale

**Riferimento**: `BQ1-K3` (riga 196), `BQ2-K2` (riga 230), `BQ2-K3` (riga 244).

"Intervallo occupato dai generi del catalogo video" non dice se sia il min-max, un intervallo interquartile o un'altra copertura, né se la condizione di appartenenza valga asse per asse o come regione congiunta nello spazio a tre dimensioni: le due letture producono quote molto diverse, e la lettura min-max congiunta tende meccanicamente a valori alti su un catalogo video eterogeneo, gonfiando la misura. "Distanza normalizzata sulla scala 0-1" non dice quale metrica né su quale massimo si normalizza, e non dice come si ottiene un "profilo di mood mediano del catalogo video" — mediana sui generi, o sui titoli, e con quale ponderazione. "Combinazione con il peso relativo dichiarato" non dice come si rendono commensurabili un indice 0-100 e un indice 0-1 prima di pesarli: senza dichiarare anche la trasformazione di scala, il peso da solo non determina il risultato. Sono scelte legittimamente rinviabili alla fase di implementazione, ma solo se il documento dichiara di rinviarle; oggi le omette in silenzio, e su tre KPI questo significa che la definizione non è ancora sufficiente a rendere il calcolo riproducibile da un secondo analista.

### R7 — `BQ2-K1` usa una granularità che §5.2 non prevede

**Riferimento**: §5.2 (righe 112-119) contro scheda `BQ2-K1` (riga 214).

§5.2 presenta due granularità "distinte e non intercambiabili" e assegna la traccia deduplicata a "qualunque **totale di catalogo**". La scheda di `BQ2-K1` dichiara invece "coppia traccia-segmento per l'appartenenza, traccia deduplicata per il calcolo", che è una terza modalità: deduplicazione *interna al segmento*, con la stessa traccia legittimamente conteggiata nella mediana di più segmenti. È probabilmente ciò che serve, ma non è ciò che §5.2 descrive, e §5.2 chiude affermando che "ogni scheda KPI dichiara in quale delle due granularità opera". Qui ne dichiara una che non è fra le due. Da correggere in §5.2, non nella scheda.

### R8 — Numeri sui dati presentati come input, ma prodotti da un'analisi

**Riferimento**: §5.2 (riga 119 e nota di riga 121), `BQ2-K1` note (righe 218 e 220), §8 (righe 328-331).

Il documento dichiara di non contenere risultati e classifica ogni numero come assunzione di scenario o caratteristica dichiarata dei dati di origine. Alcuni numeri stanno però al confine: "un totale calcolato senza deduplicare sovrastima di circa un quinto", "circa una traccia su sette ha indice di popolarità pari a zero", "alcuni segmenti ne concentrano oltre il 60%". Non sono caratteristiche documentate di una fonte come lo sono una scala 0-100 o una data di aggiornamento: sono esiti di un calcolo eseguito sui dati. La distinzione regge sul piano dell'uso — motivano una scelta di metodo, non rispondono a BQ1/BQ2/BQ3 — ma il lettore deve prenderli sulla fiducia, senza riferimento a come sono stati ottenuti né possibilità di replicarli. Lo stesso vale per l'affermazione strutturale "il catalogo di riferimento contiene lo stesso numero di tracce per ogni segmento, per come è stato campionato", che sorregge da sola una voce di out of scope. Una nota di provenienza per questi valori chiuderebbe il rilievo.

### R9 — La North Star è una proprietà statica del catalogo, non un criterio che l'iniziativa muove

**Riferimento**: §3 (righe 68, 72), tabella alternative (riga 79), §7 (riga 302).

Il documento chiama `BQ1-K1` alternativamente "criterio di successo dell'iniziativa" (riga 68), "metrica di riferimento" (righe 70, 79) e "North Star metric" (§3, §7), come se fossero sinonimi. Non lo sono. `BQ1-K1` misura una caratteristica del catalogo video *attuale*: non cambia se il verticale musicale viene lanciato, non cambia nei dodici mesi dell'orizzonte, e non può in alcun senso essere raggiunta o mancata. È un criterio di **screening**, cioè una condizione di coerenza da verificare prima di decidere, e come tale è una scelta difendibile; ma chiamarlo criterio di successo di un'iniziativa suggerisce al board che l'iniziativa verrà giudicata su di esso, cosa che non può accadere. Riga 72 corregge parzialmente il tiro ("non dice che l'espansione sarà redditizia: dice che sarebbe coerente"), il che rende il problema terminologico più che sostanziale, ma su un documento indirizzato a un board la terminologia è sostanza.

### R10 — L'esclusione di `BQ3-K2` dalla North Star è argomentata anche su basi presentazionali

**Riferimento**: §3 (riga 70).

L'argomento metodologico contro `arpu_uplift` come metrica di riferimento è solido e sufficiente: è simulato, quindi confidenza bassa, quindi obbligatoriamente un intervallo, quindi eleggerlo a criterio ufficiale darebbe autorevolezza a un'assunzione. La frase che chiude il paragrafo aggiunge però un argomento di natura diversa: "una metrica di riferimento che dovesse essere presentata come intervallo sarebbe un oggetto strano da mettere in cima a una dashboard". Qui il vincolo che la North Star sia un valore puntuale è asserito per convenzione di presentazione, non derivato. È un dettaglio, ma indebolisce un passaggio che stava reggendo da solo, e un lettore ostile lo userebbe per sostenere che il documento ha scelto la metrica che stava bene in dashboard.

### R11 — `BQ1-K1`: la pretesa "nessuna mappatura" è più forte di quanto la scheda mostri

**Riferimento**: §3 (riga 64) contro scheda `BQ1-K1` (riga 168).

§3 descrive il contenuto misurato come "musical, documentari musicali, concerti, film sulla musica" — quattro tipologie — mentre §3 riga 70 e la scheda riga 168 sostengono che si legge una singola categoria assegnata dalla fonte, senza alcuna mappatura interposta. Le due cose stanno insieme solo se la fonte ha effettivamente un'unica categoria che le comprende tutte e quattro; se invece i concerti o i documentari musicali vivono in categorie diverse, allora la selezione delle categorie da includere **è** una mappatura, esattamente il tipo di strato interpretativo che §6 fa scendere a confidenza media. Il documento non nomina la categoria e non dichiara quante ne siano coinvolte, quindi il lettore non può verificare l'affermazione su cui poggia la confidenza alta della North Star.

### R12 — `arpu_uplift` è un ricavo lordo, e §7 si intitola "Impatto economico stimato"

**Riferimento**: §7 (righe 300-302) contro §8 (riga 314).

`BQ3-K2` è il prodotto fra tasso di adozione e differenziale di prezzo: è ricavo incrementale lordo per utente, senza alcun costo dedotto, e i costi del verticale musicale — licenze in primis, che in questo settore sono la voce dominante e sono per gran parte variabili con l'ascolto — sono dichiarati fuori scope. §8 lo dice con chiarezza esemplare ("chi cercasse qui un ritorno sull'investimento non lo troverà, ed è deliberato"), ma la sezione che ospita la misura si intitola "Impatto economico stimato" e la sua direzione è "valore alto = impatto economico maggiore". Un lettore che leggesse §7 senza arrivare a §8 concluderebbe di avere davanti una stima di valore creato. Titolare la sezione "Ricavo incrementale lordo" costerebbe nulla e chiuderebbe l'equivoco.

### R13 — Ambiguità minori non risolte

**Riferimento**: `BQ2-K3` (riga 246), `BQ1-K2` (riga 180), `BQ3-K1` (riga 260), A5 (riga 57).

La direzione di `BQ2-K3` è "posizione alta = candidato migliore", che con una graduatoria è bidirezionale: non è detto se il candidato migliore sia la posizione 1 o la posizione con il punteggio maggiore. `BQ1-K2` non dichiara il segno della differenza né come trattare i film privi di durata. `BQ3-K1` misura una quota entro dodici mesi su una base assunta stabile: le disdette non sono menzionate né come incluse né come escluse, e la stabilità della base è affermata in A5 senza discussione. Nessuna di queste è grave, tutte costano una riga.

---

## Divergenze da chiarire nella feature successiva

Non sono difetti del documento: sono punti su cui va presa una decisione, dichiarata e versionata prima di calcolare qualsiasi cosa.

1. **Definizione operativa di "segmento"**: genere dichiarato dalla fonte oppure raggruppamento derivato per mood. La scelta cambia la confidenza di `BQ2-K1` e, nella seconda lettura, introduce circolarità in `BQ2-K2`.
2. **`BQ1-K3`, definizione di "intervallo occupato"**: min-max, intervallo interquartile o altra copertura; e appartenenza verificata asse per asse oppure come regione congiunta sui tre assi. Va dichiarato anche l'effetto atteso della scelta sulla grandezza del risultato.
3. **`BQ2-K2`, metrica e normalizzazione**: quale distanza (euclidea, Manhattan, coseno), su quale massimo si normalizza, e se il lato video sia un unico centroide o un profilo per genere poi aggregato — e in quest'ultimo caso con quale ponderazione (per numero di titoli o per genere).
4. **`BQ2-K3`, commensurabilità e pesi**: quale trasformazione porta `BQ2-K1` e `BQ2-K2` su una scala comune, quali sono i pesi, chi li fissa, e se prevale la lettura a quadranti di §4 o quella pesata della scheda.
5. **Soglie decisionali**: per la North Star e, dove ha senso, per gli altri KPI. Vanno fissate ora, prima di vedere i numeri, coerentemente con il principio dichiarato in §1.
6. **`BQ2-K1`, trattamento delle tracce a popolarità zero**: incluse, escluse, o riportate come misura di fragilità accanto alla mediana. La nota di riga 220 riconosce che alcuni segmenti ne concentrano oltre il 60% ma non decide.
7. **Granularità di `BQ2-K2`**: la scheda dichiara coppia traccia-segmento, la formula lavora su un profilo mediano di segmento. Va allineata, insieme alla riformulazione di §5.2 richiesta da R7.
8. **`BQ1-K2`, convenzioni di calcolo**: segno della differenza e trattamento dei titoli privi di durata.
9. **Dimensione della base utenti**: se si vuole affiancare a `BQ3-K2` un impatto aggregato in euro, serve una cifra dichiarata come assunzione in A5. Se non si vuole, va detto esplicitamente che il KPI resta per-utente e non è scalabile.
10. **Governance della tabella di corrispondenza generi → mood** (§5.3): chi la costruisce, chi la approva, con quale criterio si valuta una contestazione riga per riga, e se le sue revisioni invalidino i valori già pubblicati di `BQ1-K3`, `BQ2-K2` e `BQ2-K3`.
11. **Posizione dell'alternativa "non entrare"**: se il framework debba includere un controfattuale o almeno una regola di stop, oppure se si accetti esplicitamente che BQ2 presupponga l'ingresso e che il "no" possa venire solo da BQ1.
