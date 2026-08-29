# Fase 0 — le decisioni di disegno

**Feature**: `010a-report-disegno` | **Data**: 2026-08-29

Le decisioni che il contratto di pagina presuppone. Non sono ricerche bibliografiche: sono scelte di disegno, e stanno qui perché il contratto le usi senza doverle riargomentare pagina per pagina. Numerate `G1`-`G9` — la lettera è nuova, come `E` per la `007b` e `F` per la `008a`, e va estesa nell'esclusione strutturale del controllo di coerenza se un documento pubblicato le citerà (non accade in questa feature: il contratto vive sotto `specs/`, che il controllo non legge).

Il vincolo che le governa tutte è dichiarato una volta sola, `G1`, e le altre otto vi si appoggiano.

---

## `G1` — La corrispondenza pagina→sezione è molti-a-uno, e la direzione conta

**Decisione**: **una pagina serve esattamente una sezione** di [`docs/raccomandazione.md`](../../docs/raccomandazione.md); **una sezione può ricevere più pagine**. La corrispondenza non è biunivoca e non deve esserlo.

**Motivazione, che è il cuore di questa feature.** L'argomento ha sei sezioni numerate e il report ne ha fra 8 e 12 pagine: la corrispondenza uno-a-uno è aritmeticamente impossibile, e va risolta in una direzione o nell'altra prima di disegnare, non a metà. Le due direzioni non sono simmetriche:

- **una pagina che serve più sezioni** riporta l'inventario dalla porta di servizio. È esattamente la dashboard a quattro pagine — dove ciascuna pagina copriva una domanda di business intera, cioè più mosse dell'argomento affastellate — ed è il difetto per cui questa feature esiste;
- **più pagine che servono una sezione** è invece la forma normale di un argomento lungo: una sezione che cambia mossa al proprio interno chiede due schermate, non due paragrafi sulla stessa.

**Il criterio con cui si divide una sezione**, ed è il presidio contro la divisione arbitraria: **si divide quando l'argomento cambia mossa** — dall'affermazione all'obiezione, dalla regione all'esclusione, dalla stima alla sua qualificazione — **non quando la sezione ha troppi numeri per una pagina sola**. La seconda ragione produrrebbe pagine divise per capienza, che è di nuovo un inventario, solo con più fogli.

**Alternative scartate**: forzare sei pagine, una per sezione. Rispetterebbe la corrispondenza puntuale al prezzo di comprimere §2 e §3, che sono le due sezioni in cui l'argomento fa più mosse; e violerebbe la forchetta 8-12 dichiarata dalla regia. Il contratto dichiara comunque, per ciascuna pagina, la sezione servita: `FR-006` chiede la corrispondenza puntuale, e molti-a-uno resta puntuale.

---

## `G2` — L'ordine è quello dell'argomento, e le tre domande di business si sciolgono

**Decisione**: le pagine non portano i titoli `BQ1`, `BQ2`, `BQ3` e non sono ordinate per essi. Ogni KPI compare dove l'argomento lo usa. La sigla resta leggibile nelle etichette di provenienza, non nell'intestazione della pagina.

**Motivazione.** L'ordine `BQ1`→`BQ2`→`BQ3` è l'ordine in cui le domande sono state **poste**, ed è l'ordine giusto per il business case, che le pone. Non è l'ordine in cui si **risponde**: una risposta comincia dalla conclusione e poi la difende, mentre il framework comincia dal posizionamento e arriva all'impatto. Il documento della `009` è già ordinato come risposta, e questa feature ne eredita l'ordine invece di reinventarlo.

**Conseguenza concreta, e va dichiarata perché è visibile.** `BQ1-K1`, `BQ1-K3` e `BQ2-K3` compaiono tutti e tre sulla pagina delle tre condizioni: sono le tre condizioni, e provengono da due domande di business diverse. Nella dashboard vecchia stavano su due pagine distinte, e la loro congiunzione — che è **il verdetto** — non stava da nessuna parte.

**Alternative scartate**: tenere l'ordine del framework e aggiungere una pagina di sintesi in testa. È il disegno peggiore dei due, perché lascia intatto l'inventario e vi antepone un riassunto: chi scorre trova la risposta a pagina 1 e poi otto pagine che non la difendono nell'ordine in cui l'ha ricevuta.

---

## `G3` — La pagina iniziale è compresa nel conteggio; non esiste una pagina finale

**Decisione**: il report ha **10 pagine**, pagina iniziale **compresa** nel conteggio. Non esiste una pagina conclusiva separata: l'ultima pagina dell'argomento è l'ultima pagina del report.

**Motivazione.** La forchetta 8-12 della regia ammette entrambe le convenzioni purché dichiarate, e questa è la dichiarazione. La pagina iniziale è compresa perché **porta un pezzo dell'argomento** — la domanda per cui l'analisi esiste, e a quali condizioni si risponderà — e non è un frontespizio: contarla fuori suggerirebbe che sia decorazione.

**Perché nessuna pagina finale.** Una pagina conclusiva ripeterebbe la risposta già data alla pagina 2, e la ripetizione in coda a un argomento è il posto in cui una raccomandazione si ammorbidisce: si riassume, e riassumendo si perde la qualificazione. `docs/raccomandazione.md` non ha una conclusione per la stessa ragione, e chiude su «che cosa questa raccomandazione non è» — che è la posizione più scomoda e la più onesta.

---

## `G4` — Le pagine di sola prosa: quali sono, e perché non si decorano

**Decisione**: **due** pagine del disegno non portano alcun valore misurato — quella sulla revisione della tabella di mood e quella sui dati mancanti. Restano di sola prosa e non ricevono grafica.

**Motivazione.** Il vincolo della regia è che ogni pagina dia all'occhio qualcosa da guardare, e la stessa regia ammette le pagine di sola prosa dove il passaggio dell'argomento non porta numeri. Le due sono compatibili: ciò che una pagina di sola prosa deve dare all'occhio è **struttura** — un'articolazione visibile fra condizione e conseguenza — non un grafico.

**Che cosa questo esclude, esplicitamente.** Un grafico costruito per riempire una pagina di prosa è peggio di un vuoto: afferma con la propria geometria qualcosa che il testo non afferma. Il caso concreto e prevedibile è la sezione «che cosa lo farebbe cambiare», dove sarebbe facile disegnare una barra dei rischi con un'altezza inventata. Non esiste alcun valore che ordini quei rischi per gravità, e disegnarli ordinati sarebbe una graduatoria senza fonte — cioè ciò che il principio I vieta.

**Perché sono due e non tre.** La sezione «che cosa lo farebbe cambiare» ha quattro condizioni, e **una di esse porta un numero ancorato**: il margine di `C2`, che dice quanto la stima dovrebbe sbagliare perché la conclusione si ribalti. Quella condizione va quindi su una pagina propria con la propria visuale (`G7`), e le altre tre restano insieme sulla pagina di prosa. Dividere per la presenza del numero non è dividere per capienza: è la mossa dell'argomento che cambia — da «quanto siamo lontani dalla soglia», che è misurato, a «che cosa non abbiamo osservato», che non lo è.

---

## `G5` — Il verdetto congiunto è una visuale, non tre schede

**Decisione**: la pagina della risposta porta le tre condizioni come **un'unica visuale di stato a tre elementi**, con il conteggio congiunto letto da un'ancora, e non come tre schede booleane affiancate.

**Motivazione.** Le tre condizioni non sono tre misure indipendenti: sono una **congiunzione**, e la regola di decisione — pubblicata prima dei valori — dice che l'argomento regge solo se valgono tutte e tre. Tre schede affiancate mostrano tre fatti e lasciano la congiunzione all'occhio di chi guarda; una visuale che porta le tre condizioni **dentro** l'esito congiunto mostra la regola.

**La conseguenza sulla confidenza, che è il motivo per cui la forma conta.** `docs/raccomandazione.md` §2 argomenta che la confidenza del verdetto è **media e non la media delle tre**: una congiunzione non è più affidabile del suo termine più debole. Tre schede con tre etichette di confidenza — alta, media, media — invitano esattamente alla lettura che quel passaggio esiste per impedire. La visuale unica porta **una** etichetta di confidenza, quella del verdetto, e le tre condizioni portano la propria dentro.

**Alternative scartate**: una scheda sola col conteggio «3 su 3». Nasconde quali condizioni siano soddisfatte e quale sia la più debole, cioè tutto ciò che rende il verdetto discutibile — e un verdetto che non si può discutere non si può nemmeno verificare.

---

## `G6` — La regione di `BQ2` prende due pagine, e l'issue `#21` si chiude

**Decisione**: la parte «con che cosa entrare» prende **due pagine** — la regione (dispersione) e la graduatoria (tabella) — e le due **si evidenziano a vicenda**, chiudendo l'issue `#21`. La selezione incrociata attraversa le due pagine tramite un filtro di report sincronizzato sul segmento selezionato, non tramite due visuali sulla stessa schermata.

**Motivazione della divisione.** Nella dashboard vecchia dispersione e tabella stavano sulla stessa pagina, e la pagina era piena: 114 punti e 114 righe su una schermata sola. La divisione non è per capienza — sarebbe la ragione che `G1` vieta — ma perché **le due visuali fanno due mosse diverse dell'argomento**: la dispersione dice *esiste una regione*, la tabella dice *ecco che cosa contiene, e in quale ordine*. Sono le due metà che `docs/raccomandazione.md` §3 tiene distinte, la regione e l'estratto, e su cui insiste che la seconda non sostituisce la prima.

**Perché l'issue `#21` si chiude invece di essere riproposta.** Il difetto originale è che la selezione di un punto nella dispersione non evidenziava la riga corrispondente nella tabella. Su due pagine il problema cambia natura: non è più un'interazione mancante fra visuali vicine, è una continuità di lettura fra due schermate. Il presidio è la sincronizzazione della selezione, che Power BI offre come filtro di report sincronizzato — e va **verificata a schermo** dalla `010b`, perché questa sessione non può accertarla.

**Il vincolo che non cambia**: la selezione resta **evidenziazione e non filtro**. Le soglie e le posizioni portano `ALL ( dim_segment )` nelle formule pubblicate e non si muovono; è la proprietà che rende la coppia di pagine interattiva senza renderla bugiarda, e la `010b` la riverifica.

---

## `G7` — Il margine di `C2` merita una visuale, e la visuale dice una cosa sola

**Decisione**: il margine di `C2` — quanto la stima dovrebbe sbagliare perché la conclusione si ribalti — va su una pagina propria, con **una visuale a barra orizzontale su un asse `0-1`** che porta tre riferimenti: il valore misurato, la soglia adottata, e la distanza fra i due.

**Motivazione.** È il passaggio più forte dell'intero argomento e nella dashboard vecchia non esisteva: la `009` lo ha prodotto rispondendo a una domanda che il progetto non aveva mai posto. È anche l'unica parte della sezione «che cosa lo farebbe cambiare» che porta valori ancorati, ed è la ragione per cui è una pagina e non un capoverso (`G4`).

**Che cosa la visuale deve dire, e che cosa deve impedire.** Deve mostrare che la distanza dalla soglia è ampia. Non deve suggerire che sia una **stima dell'errore**: nessuno ha misurato di quanto l'inviluppo ecceda la regione reale. È una **condizione sull'errore**, e la differenza è la sola cosa che quella pagina esiste per comunicare. La forma a barra su asse assoluto la sostiene; una barra di errore o un intervallo attorno al valore la contraddirebbe, perché entrambe le forme comunicano una dispersione stimata.

**Il secondo riferimento che la visuale porta**, ed è un ritrovamento di questo disegno: `docs/raccomandazione.md` §2 dichiara che la risposta non cambierebbe con **nessuna soglia fino al valore misurato stesso**. Sulla stessa barra è la distanza fra la soglia e il valore, cioè ciò che la visuale già disegna: la forma non va cambiata per portare quel secondo fatto, va solo etichettata perché si legga.

---

## `G8` — I due cataloghi sui tre assi: una visuale che i dati sostengono, una che no

**Decisione**: la pagina della seconda condizione porta un **confronto dei due cataloghi sui tre assi di mood**, costruito su valori ancorati che esistono. Non porta una dispersione delle tracce sugli assi.

**Che cosa esiste, verificato negli artefatti**:

- i **profili di mood delle 42 categorie video** vivono in `data/curated/dim_category_mood.json`, tre assi per categoria, 126 valori ancorati;
- il **profilo mediano del catalogo video** sui tre assi vive in `reports/kpi_measures.json` (`KPI.BQ2K2.video_profile.*`);
- gli **estremi dell'inviluppo** su ciascun asse vivono nello stesso artefatto (`KPI.BQ1K3.bound.*`);
- la **quota di tracce dentro l'inviluppo** e il loro conteggio sono ancorati.

**Che cosa non esiste, ed è il ritrovamento di questa fase**: **nessun profilo di mood per segmento musicale è pubblicato come valore ancorato**. `reports/kpi_measures.json` porta per ciascun segmento affinità e distanza, non le tre coordinate. Un confronto dei profili segmento per segmento richiederebbe quindi tre misure DAX nuove sui tre assi — leggibili da `dim_track`, che porta le colonne — e questo disegno **non le chiede**: la seconda condizione è un'affermazione sull'**intero** catalogo musicale, non sui segmenti, e portare i segmenti su quella pagina anticiperebbe la parte «con che cosa entrare» che viene dopo.

**La forma scelta**: le 42 categorie video come punti su un piano a due assi, con l'inviluppo disegnato e la quota di tracce musicali che vi ricade dichiarata come valore ancorato accanto. Mostra la scatola e mostra che la scatola è larga — che è il limite dichiarato di quella condizione — usando solo valori che esistono.

**La visuale che sarebbe stata migliore e che i dati non sostengono**: le 89.741 tracce come nube sui tre assi, con l'inviluppo sovrapposto. Renderebbe visibile quanta parte della scatola sia vuota, che è precisamente ciò che «stima per eccesso» significa. Non entra nel contratto: nessun artefatto pubblica quella nube, la sua grana è la traccia e nessun KPI è pubblicato a quella grana, e disegnarla richiederebbe di portare a schermo un valore che nessun documento del progetto pubblica. È dichiarata qui perché chi costruisce non la reinventi credendo che sia stata dimenticata.

---

## `G9` — `BQ3` prende due pagine, e la terna non si scompone

**Decisione**: la parte «quanto vale» prende **due pagine** — gli scenari, e il fattore di conversione con il debito aperto. Su entrambe i valori compaiono come **terna**.

**Motivazione della divisione.** Anche qui la mossa cambia: la prima pagina dice *quanto varrebbe per utente*, la seconda dice *che cosa quel numero diventa su una base, e perché il progetto non la quantifica*. La seconda è la pagina in cui l'argomento si difende dall'uso sbagliato più prevedibile — moltiplicare il centrale per una base e stampare un totale — e in `docs/raccomandazione.md` §4 occupa quasi metà della sezione.

**La forma della terna**, ereditata dal contratto della `008a` e non ridiscussa: una tabella a tre colonne, mai una scheda singola, mai una barra. Il divieto di scheda singola è strutturale per la confidenza bassa, ed è l'unico punto in cui un principio non negoziabile prescrive direttamente una forma di visuale.

**Che cosa cambia rispetto alla `008a`, ed è l'unica cosa.** La pagina degli scenari riceve una visuale che la dashboard vecchia non aveva: il **fattore di conversione per ogni 100.000 abbonati**, che `docs/raccomandazione.md` §4 pubblica come riga aggiuntiva. Non è una moltiplicazione dell'uplift per una base — il divieto resta intero, e nessuna base di StreamWave viene quantificata — è la stessa terna espressa su un'unità dichiarata, che è ciò che rende l'operazione ripetibile da chi conosce la propria base senza che il progetto la esegua.

**La formulazione sull'uplift**, e chiude l'issue `#26` per questo contratto: si usa quella stretta — *qui nessuna base viene quantificata e nessun artefatto offre una chiave per farlo* — e mai «non è scalabile», che `bq3_scenarios.md` §8 dichiara falsa. L'issue resta aperta sui due documenti che la portano ancora (`kpi_operators.md` §9 e il contratto della `008a` §8): questa feature non li corregge.

---

## Che cosa questa fase non ha deciso

**I colori, i caratteri, le dimensioni.** Sono di chi costruisce, con l'eccezione ereditata dalla `008a`: le marcature che portano informazione — appartenenza al quadrante, segmenti a domanda non misurata, resto — devono restare distinguibili fra loro.

**Se una visuale regge davanti allo schermo.** È l'unica cosa che un disegno a tavolino non può verificare. Gli scostamenti sono previsti: si annotano mentre accadono e si elencano nell'esito della `010b`, con la propria ragione.

**In quale forma il `.pbix` porta oggi i sei valori di scenario.** Il file non è versionato e questa sessione non lo apre. La decisione `CP-2` della `008a` resta il vincolo dichiarato; accertarla è della `010b`.
