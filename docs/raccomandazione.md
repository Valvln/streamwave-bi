# La raccomandazione

**Data**: 2026-08-29 · **Feature**: `009` · **Destinatario**: il board di StreamWave

---

## Che cosa è questo documento

È la risposta alla domanda per cui l'analisi è stata commissionata: **StreamWave può entrare nel music streaming?**

È scritto per essere letto **da solo**. Non richiede di aver letto alcun altro documento del progetto, non rimanda altrove per informazioni che servono a capire le frasi che contiene, e non presuppone competenza tecnica o statistica. Dove indica un altro documento lo fa per chi voglia **approfondire** un passaggio — mai per completare una frase lasciata a metà.

I documenti che lo sostengono vivono nella cartella `docs/` di questo repository: il [business case](business_case.md) fissa le domande e il criterio di decisione, [gli operatori](kpi_operators.md) le regole di calcolo, [le misure](kpi_measures.md) i valori con la loro provenienza, [gli scenari](bq3_scenarios.md) le stime economiche. Ogni numero di questa pagina è legato all'artefatto che lo produce da un riferimento invisibile, verificabile con un comando: nessuna cifra qui è stata digitata a mano.

---

## 1. La risposta

**Sì: l'espansione nel music streaming è coerente con il catalogo che StreamWave ha già.**

Il criterio con cui questa risposta si dà è stato fissato e pubblicato **prima** che i numeri esistessero: tre<!--#--> condizioni, e l'argomento si considera sostenuto solo se valgono tutte e tre<!--#-->. Sono soddisfatte 3<!--@KPI.verdict.conditions_satisfied--> condizioni su tre<!--#-->, ed è l'esito che il business case legge così: *l'argomento di coerenza è sostenuto, l'espansione è un'estensione del catalogo esistente*.

**Che cosa questa risposta non dice.** Non dice che l'espansione sarà redditizia: dice che sarebbe **coerente**. È la formulazione che il progetto ha adottato prima di misurare, e va presa alla lettera. La coerenza strategica dice che StreamWave entrerebbe in un mercato adiacente al proprio catalogo invece che in un mercato estraneo, con i costi di acquisizione che il secondo comporterebbe. Non dice nulla su ricavi, costi, tempi o vantaggio competitivo.

**Su che cosa poggia, in una riga.** Su due<!--#--> cataloghi pubblici usati come sostituti — un catalogo video e un catalogo musicale — perché StreamWave non ha ceduto i propri dati a questa analisi. Che quei cataloghi rappresentino StreamWave è un'assunzione dichiarata e non verificata, ed è il limite più importante di questo documento: la sezione [«che cosa questa raccomandazione non è»](#6-che-cosa-questa-raccomandazione-non-è) lo tratta per esteso. **Nessun numero di questa pagina è una misura fatta su StreamWave.**

---

## 2. Perché

L'argomento poggia su tre<!--#--> condizioni. Ciascuna è stata scritta prima di conoscere il proprio esito, e ciascuna è verificabile risalendo al valore che la determina.

### La prima: il contenuto musicale non è residuale nel catalogo attuale

In italiano: nel catalogo video che StreamWave offre oggi, la musica **non è una nicchia dimenticata**. Sta nella metà più popolata delle categorie.

In forma tecnica, è la condizione `C1`: il numero di titoli della categoria `Music & Musicals`<!--@catalogs.netflix_categories_musical--> supera la mediana dei conteggi delle 42<!--@CL.NF.category.distinct--> categorie del catalogo. Quel conteggio vale 375<!--@KPI.BQ1K1.c1.category_count.music_musicals--> titoli contro una mediana di 248,00<!--@KPI.BQ1K1.c1.median_of_42-->, e la condizione è quindi soddisfatta: sì<!--@KPI.BQ1K1.c1.above_median-->.

**Confidenza: alta.** È l'unica delle tre<!--#--> che si legge direttamente dal dato, senza alcuna mappatura interpretativa: il catalogo classifica già i propri titoli, e una delle sue categorie è quella musicale.

**Una precisazione che evita una lettura sbagliata.** «Non residuale» non significa «grande». La quota della categoria musicale sull'intero catalogo vale 0,0426<!--@KPI.BQ1K1.share-->, cioè una frazione piccola. Le due<!--#--> letture non si contraddicono, perché misurano cose diverse: una categoria può stare sopra la mediana delle 42<!--@CL.NF.category.distinct--> categorie e restare comunque una porzione minima del catalogo, ed è esattamente ciò che accade qui. La prima condizione dice che la musica non è marginale **fra le categorie**, non che il catalogo sia musicale.

### La seconda: la musica assomiglia, per carattere, a ciò che StreamWave già offre

In italiano: se si descrive ogni contenuto con tre<!--#--> caratteristiche di carattere — quanto è ballabile, quanto è energico, quanto è positivo di umore — allora **la gran parte del catalogo musicale ricade nella stessa regione** che il catalogo video occupa già.

In forma tecnica, è la condizione `C2`: la quota di tracce il cui profilo cade dentro l'intervallo occupato dal catalogo video su tutti e tre<!--#--> gli assi vale 0,8450<!--@KPI.BQ1K3.overlap_share-->, contro una soglia di maggioranza semplice fissata a 0,5000<!--@KPI.BQ1K3.c2.threshold-->. La condizione è soddisfatta: sì<!--@KPI.BQ1K3.c2.satisfied-->.

**Confidenza: media**, e la ragione sta nel come quel valore è costruito — la prossima sottosezione la tratta.

### La terza: esiste almeno un punto d'ingresso concreto

In italiano: non basta che la musica assomigli in generale al catalogo. Serve che **esista almeno un tipo di musica** che sia insieme molto richiesto e molto affine a ciò che StreamWave offre. Esiste.

In forma tecnica, è la condizione `C3`: almeno un segmento musicale si colloca contemporaneamente nella metà superiore per domanda e nella metà superiore per affinità con il catalogo video. Ne esistono 33<!--@KPI.BQ2K3.quadrant_members_count-->, e la condizione è soddisfatta: sì<!--@KPI.BQ2K3.c3_satisfied-->. Quali siano, e come vadano letti, è la sezione [«con che cosa entrare»](#3-con-che-cosa-entrare).

**Confidenza: media.** Poggia sulla stessa mappatura interpretativa della seconda condizione.

### La confidenza del verdetto, e perché non è la media delle tre

**Il verdetto ha confidenza media**, non alta.

Non è una convenzione: è una conseguenza. Una congiunzione di condizioni **non è più affidabile del suo termine meno affidabile**. Se una sola delle tre<!--#--> poggia su un dato costruito invece che osservato, l'esito complessivo poggia su quel dato — e trattare la confidenza come una media lascerebbe che l'affidabilità alta della prima condizione coprisse quella media delle altre due<!--#-->, producendo un verdetto che si presenta come più solido dei suoi stessi ingredienti.

**Il termine più debole è la seconda condizione**, e la ragione è precisa. La regione di carattere occupata dal catalogo video è descritta prendendo, per ciascuno dei tre<!--#--> assi, l'estremo minimo e l'estremo massimo, e considerando dentro tutto ciò che vi ricade su tutti e tre<!--#-->. È una scatola che **contiene** la regione reale ma è più grande di essa: qualunque combinazione degli estremi vi rientra, anche una che nel catalogo video non compare mai. Ne discende che il valore pubblicato è una **stima per eccesso**: la sovrapposizione reale è minore o uguale a 0,8450<!--@KPI.BQ1K3.overlap_share-->, e **quanto minore questo progetto non lo misura**.

C'è una seconda ragione, e riguarda l'origine del dato. Le tre<!--#--> caratteristiche di carattere esistono già, misurate, per ogni traccia musicale; per il catalogo video **non esistono**, e sono state assegnate categoria per categoria da chi ha condotto l'analisi. È un dato costruito, non osservato, e nessuna cura nella costruzione lo sposta di classe.

### Quanto la stima dovrebbe sbagliare perché la risposta cambi

Da «stima per eccesso» discende una domanda che il progetto non aveva mai posto: **di quanto dovrebbe sovrastimare, perché la seconda condizione cada?**

La distanza fra il valore misurato e la soglia vale 0,3450<!--@KPI.BQ1K3.c2.margin-->, che è 0,4083<!--@KPI.BQ1K3.c2.margin_share_of_value--> del valore stesso. In parole: la sovrapposizione reale dovrebbe essere inferiore alla stima di **più di 0,4083<!--@KPI.BQ1K3.c2.margin_share_of_value--> della stima stessa** perché scenda sotto la maggioranza semplice e la condizione cada.

**Due<!--#--> letture sbagliate, che questa frase esiste per impedire.**

La prima: questo margine **non è una stima dell'errore**. Nessuno ha misurato di quanto la scatola ecceda la regione reale, e questo documento non lo afferma. È una **condizione sull'errore**: dice quanto grande dovrebbe essere l'errore perché la conclusione si ribalti, non quanto grande sia.

La seconda: il margine **dipende dalla soglia**, e non è una proprietà del solo dato. Con una soglia di due<!--#--> terzi invece della maggioranza semplice varrebbe meno della metà. La soglia adottata — più della metà del catalogo musicale — è la lettura letterale del termine che il business case usa, «maggioranza», ed è stata fissata senza guardare al valore; ma chi ritenesse che «maggioranza» debba significare qualcosa di più severo troverebbe un margine più stretto, pur trovando la stessa risposta. **Sull'esito la soglia è ininfluente su questi dati; sul margine no.**

---

## 3. Con che cosa entrare

**La raccomandazione non è entrare da un genere.** È entrare da una **regione del catalogo musicale**, che i segmenti qui sotto servono a caratterizzare — non a delimitare.

La distinzione non è una sfumatura ed è la ragione per cui questa sezione non contiene una classifica da leggere dall'alto. I segmenti musicali **si sovrappongono per costruzione**: una stessa traccia appartiene a più segmenti insieme, e ogni traccia partecipa a ciascuno di quelli a cui è assegnata. Ne discendono due<!--#--> conseguenze pratiche.

**Le quantità dei segmenti non si sommano.** Sommare due<!--#--> segmenti conta due<!--#--> volte ciò che appartiene a entrambi, e il totale che ne esce non corrisponde a nulla.

**Contare le righe non dimensiona un mercato.** Il numero di tracce di un segmento misura come il catalogo di origine è stato **campionato**, non quanta musica di quel tipo esista o quanto pubblico abbia. È una proprietà della fonte, non del mondo.

### La regione

Dei 114<!--@SP.genre.count--> segmenti che l'analisi ordina, 33<!--@KPI.BQ2K3.quadrant_members_count--> si collocano contemporaneamente sopra la mediana per domanda e sopra la mediana per affinità con il catalogo video. Sono la regione da cui entrare: musica che il pubblico cerca **e** che assomiglia per carattere a ciò che StreamWave già offre.

Il candidato di punta è il segmento `pop`<!--@catalogs.kpi_segments-->, che occupa la posizione 1<!--@KPI.BQ2K3.pop.rank--> della graduatoria costruita combinando domanda e affinità con peso uguale.

**Come si legge questa posizione, e come non si legge.** Dice che, fra i segmenti considerati, quello è il punto in cui domanda e affinità sono insieme più alte. **Non** dice che sia il solo da cui entrare, né che gli altri della regione siano alternative da scartare: non sono insiemi disgiunti fra cui scegliere, e trattarli come tali affermerebbe il falso. Una scelta di catalogo si costruisce sulla regione, e la posizione in graduatoria serve a orientarla, non a sostituirla.

### Un'esclusione che va dichiarata

7<!--@KPI.BQ2K1.high_zero_segments_count--> dei segmenti ordinati portano una marcatura particolare: una parte rilevante delle loro tracce ha popolarità registrata a zero<!--#--> nella fonte. Sono `country`<!--@catalogs.kpi_high_zero_segments-->, `iranian`<!--@catalogs.kpi_high_zero_segments-->, `jazz`<!--@catalogs.kpi_high_zero_segments-->, `latin`<!--@catalogs.kpi_high_zero_segments-->, `rock`<!--@catalogs.kpi_high_zero_segments-->, `romance`<!--@catalogs.kpi_high_zero_segments--> e `soul`<!--@catalogs.kpi_high_zero_segments-->.

Per questi segmenti la misura di domanda dice una cosa più stretta di quanto sembri: **la domanda non è misurata dalla fonte**, il che è diverso da «la domanda è bassa». Uno zero<!--#--> registrato può significare che nessuno ascolta quella traccia, oppure che la fonte non ne ha rilevato l'ascolto; il dato non distingue i due<!--#--> casi, e nessuna misura di questo progetto può distinguerli.

Ne discende un vincolo di lettura, e questo documento vi si attiene: **la coda della graduatoria non si legge**. Dire «questi generi sono i meno promettenti» attribuirebbe una domanda bassa a segmenti la cui domanda semplicemente non è stata osservata — cioè trasformerebbe un'assenza di misura in una misura sfavorevole. Dove quei 7<!--@KPI.BQ2K1.high_zero_segments_count--> compaiono, compaiono con questa qualificazione e non altrimenti.

---

## 4. Quanto vale

Questa sezione porta gli unici numeri economici del progetto, e sono di natura diversa da tutti i precedenti: **non sono misure, sono scenari** costruiti su un valore di riferimento esterno e su assunzioni dichiarate. La loro confidenza è **bassa**, e ne discende una regola che vale su tutta la sezione e non è negoziabile: **si presentano sempre come terna, mai come valore isolato**, nemmeno in una frase di sintesi. Prendere il valore centrale perché sta meglio in una slide comunica una certezza che il dato non ha.

**L'orizzonte è di 12<!--#--> mesi.** I valori qui sotto sono ciò che si otterrebbe entro quell'orizzonte, e la grandezza a cui si riferiscono è dichiarata riga per riga.

| | Pessimista | Centrale | Ottimista |
|---|---|---|---|
| **Quota della base che adotterebbe l'offerta musicale** | 15<!--@BQ3.adoption.worst-->% | 30<!--@BQ3.adoption.base-->% | 60<!--@BQ3.adoption.best-->% |
| **Ricavo aggiuntivo per utente al mese** | 0,60<!--@BQ3.uplift.worst--> € | 1,20<!--@BQ3.uplift.base--> € | 2,40<!--@BQ3.uplift.best--> € |

**Due<!--#--> qualificazioni d'unità, senza le quali i numeri sono inutilizzabili.**

**Il tasso di adozione è lordo.** Le disdette sono fuori dal perimetro di questa analisi: il numero descrive chi adotterebbe l'offerta, non il saldo fra chi la adotta e chi abbandona il servizio. È una scelta di perimetro dichiarata, non una proprietà del mercato.

**Il ricavo aggiuntivo è un livello mensile a regime, non un cumulato.** È il valore raggiunto a fine orizzonte e mantenuto, non la media del periodo — nei primi mesi sarebbe minore — e **non** un totale annuo. Moltiplicarlo per dodici<!--#--> produrrebbe un cumulato che vale solo sotto l'assunzione che la base resti costante, assunzione che questo progetto fa per il calcolo ma non per il mondo.

### Che cosa quei numeri diventano su una base di abbonati

I valori qui sopra sono per utente. Chiunque disponga di una stima della base abbonati può moltiplicarli, ed è un'operazione che si fa in pochi secondi.

**Questo progetto non quantifica la base di StreamWave**, e la tabella che segue non è una stima di quella base: le cifre nella prima colonna sono **ipotesi che mette chi legge**, scelte solo per rendere leggibile l'aritmetica. Non provengono da alcun dato di questo progetto, e chi conosca la base reale sostituisca la propria.

| Base ipotizzata da chi legge | Pessimista | Centrale | Ottimista |
|---|---|---|---|
| 500.000<!--#--> abbonati | 300.000<!--#--> € / mese | 600.000<!--#--> € / mese | 1.200.000<!--#--> € / mese |
| 1.000.000<!--#--> abbonati | 600.000<!--#--> € / mese | 1.200.000<!--#--> € / mese | 2.400.000<!--#--> € / mese |
| 2.000.000<!--#--> abbonati | 1.200.000<!--#--> € / mese | 2.400.000<!--#--> € / mese | 4.800.000<!--#--> € / mese |

**Come va letta questa tabella, ed è il punto in cui è più facile sbagliare.** Non dice che l'offerta musicale varrebbe uno di quegli importi. Dice che **se** la base fosse quella ipotizzata nella riga, **allora** l'aritmetica darebbe quei valori — e la riga giusta questo progetto non sa quale sia. Ogni cella eredita per intero la confidenza bassa della terna da cui discende: moltiplicare per una base nota non rende più solido il numero che si moltiplica.

**Una formulazione che questo documento evita, e la ragione.** Sarebbe comodo dire che il ricavo per utente «non è scalabile», e sarebbe falso: è perfettamente scalabile, ed è ciò che la tabella qui sopra fa. Ciò che è vero è più stretto — **qui nessuna base viene quantificata e nessun artefatto del progetto offre una chiave per farlo**. Non è un presidio: è una rinuncia, e non impedisce a valle l'operazione che scoraggia. Un totale di ricavo costruito su questi numeri e presentato senza la propria banda sarebbe un numero che nessuno ha misurato, con l'autorevolezza di uno misurato.

### Un debito aperto, dichiarato qui perché è qui che pesa

Il valore centrale della terna di adozione poggia su un **benchmark esterno**: una cifra pubblicata da un altro operatore, in un comunicato che questo progetto cita.

Quel comunicato **non nomina lo studio** da cui la cifra proviene. Si può constatare che un comunicato la riporti; non si può giudicare come sia stata misurata. Non esiste copia archiviata né identificativo permanente: se quell'indirizzo smettesse di rispondere, la verifica esterna verrebbe meno e resterebbe solo il valore congelato nel repository. **È un debito aperto**, non chiuso da questa raccomandazione né da alcuna feature precedente.

**Vi si aggiunge un'assunzione di trasferimento.** Il benchmark descrive **un altro operatore, su un altro mercato, otto<!--#--> anni prima**. Che quella cifra sia trasferibile a StreamWave è un'assunzione dichiarata e non verificabile con i dati disponibili. Non entra nella scala di confidenza dei numeri — la sezione seguente spiega perché — e resta valida o non valida indipendentemente da quanto il calcolo che la usa sia accurato.

---

## 5. Che cosa lo farebbe cambiare

Una raccomandazione che non dichiari le condizioni alle quali si ribalterebbe è un'opinione. Queste sono quelle condizioni, e per ciascuna è scritto **che cosa succederebbe**, non soltanto che esiste un rischio.

**Se la tabella che assegna il carattere alle categorie video venisse rivista.** Le tre<!--#--> caratteristiche di carattere del catalogo video non sono osservate: sono assegnate categoria per categoria da chi ha condotto l'analisi, e la versione usata qui è la `2`<!--@conventions.kpi_mood_table_version-->. Per il contratto che governa quella tabella, una revisione **invalida** i valori che ne dipendono invece di correggerli: la seconda condizione andrebbe ricalcolata da capo, e con essa il verdetto. Non è un rischio remoto — è il modo normale in cui quella tabella evolve — e chiunque riveda la tabella deve rifare questo passaggio prima di citare questa pagina.

**Se la sovrastima fosse maggiore del margine.** La seconda condizione poggia su una stima per eccesso, e il margine dice quanto quella stima dovrebbe essere gonfiata perché la condizione cada: più di 0,4083<!--@KPI.BQ1K3.c2.margin_share_of_value--> del proprio valore. Se lo fosse, la seconda condizione cadrebbe e l'esito passerebbe da tre<!--#--> condizioni su tre<!--#--> a due<!--#--> — che il business case legge come **sostegno parziale**: l'espansione resterebbe difendibile, ma la condizione mancante andrebbe indicata come rischio esplicito. Non passerebbe a «argomento non sostenuto».

**Se i cataloghi sostitutivi non rappresentassero StreamWave.** Tutta l'analisi poggia su due<!--#--> cataloghi pubblici usati al posto dei dati di StreamWave, che il progetto non ha. Se quei cataloghi non fossero rappresentativi — un catalogo video con una composizione diversa, un pubblico con gusti diversi — **nessuna delle tre<!--#--> condizioni direbbe più nulla su StreamWave**, indipendentemente da quanto ciascuna sia stata calcolata con cura. Non è una condizione che si possa verificare con i dati disponibili: si chiude soltanto ripetendo l'analisi sui dati reali dell'azienda, ed è la prima cosa da fare se questa raccomandazione viene presa sul serio.

**Se arrivassero dati che il progetto non ha.** Tre<!--#--> categorie li ribalterebbero in modi diversi. **Dati comportamentali** — che cosa gli abbonati di StreamWave guardano e cercano davvero — sostituirebbero l'assunzione di rappresentatività con un'osservazione, e potrebbero confermarla o smentirla. **Dati di costo** — licenze musicali, infrastruttura, organico — non toccherebbero la coerenza strategica ma potrebbero rendere l'operazione insostenibile lo stesso: questa raccomandazione non li considera. **Dati più recenti**: quelli usati qui si fermano al 2021-2022<!--#-->, e il benchmark economico al 2018<!--#-->; il mercato del music streaming si è mosso da allora, e un catalogo o un livello di adozione misurati oggi potrebbero raccontare un'altra storia.

---

## 6. Che cosa questa raccomandazione non è

**Non è un business case finanziario.** Manca interamente il lato dei costi — licenze, infrastruttura, organico, marketing — ed è una scelta deliberata di perimetro, non una dimenticanza. Chi cercasse qui un ritorno sull'investimento non lo troverà, e i numeri della sezione [«quanto vale»](#4-quanto-vale) non ne sono una versione parziale: sono ricavi potenziali senza il proprio contraltare.

**Non descrive StreamWave.** È il limite più importante e va detto due<!--#--> volte. StreamWave non ha ceduto dati a questa analisi: al posto del suo catalogo video e del suo catalogo musicale sono stati usati due<!--#--> cataloghi pubblici come **sostituti**. Ne discendono due<!--#--> assunzioni di trasferimento, e nessuna delle due<!--#--> rientra nella scala di confidenza dei numeri:

- **che i cataloghi sostitutivi rappresentino StreamWave.** Non è verificabile con i dati disponibili. Se non regge, ogni misura di questo progetto resta corretta come descrizione di quei cataloghi e diventa muta su StreamWave;
- **che il benchmark economico sia trasferibile.** Descrive un altro operatore, su un altro mercato, otto<!--#--> anni prima.

Restano fuori dalla scala **per costruzione**, e la ragione è che la scala misura quanto un numero sia solido — quanto sia osservato invece che costruito, quanto sia riproducibile — mentre queste due<!--#--> assunzioni riguardano se quel numero parli **di StreamWave**. Sono domande diverse: un valore può essere impeccabile come misura e non dire nulla del soggetto a cui lo si vuole applicare. Nessuna confidenza alta le compensa, e nessun miglioramento del metodo le chiude.

**Non dice che il pubblico attuale di StreamWave vorrebbe la musica.** La sovrapposizione della seconda condizione è fra **caratteristiche di contenuto**, non fra persone osservate: dice che la musica assomiglia per carattere al catalogo video, non che chi guarda quel catalogo ascolterebbe quella musica. Nessun dato comportamentale è entrato in questa analisi, e la domanda «lo vorrebbero?» resta senza risposta.

**Non è una previsione.** I numeri della sezione [«quanto vale»](#4-quanto-vale) sono scenari costruiti sotto assunzioni dichiarate, non stime di ciò che accadrà. La banda fra pessimista e ottimista non è un intervallo di confidenza: non c'è alcuna probabilità dentro quei numeri, e chiedere con che probabilità il valore vero vi cada è una domanda a cui questo documento non risponde.

I dati si fermano al **2021-2022**<!--#-->, e il benchmark economico al **2018**<!--#-->.

---

## Come si verifica ogni numero di questa pagina

```bash
python3 scripts/build_kpi_measures.py    # rigenera i valori delle condizioni e il verdetto
python3 scripts/check_audit_coherence.py # verifica che nessun numero di questa pagina diverga dall'artefatto che lo produce
```

Il controllo scandisce questa pagina in **severità stretta**: una quantità priva di ancora o di dichiarazione esplicita di non-misurato è un errore, non un avviso.

**Che cosa un esito verde certifica, e che cosa no.** Certifica che ogni numero ancorato coincida con il valore dell'artefatto che lo produce, e che nessun riferimento sia irrisolvibile. **Non** certifica che le affermazioni siano vere, che un'affermazione che avrebbe dovuto essere ancorata lo sia, né che le assunzioni di trasferimento reggano. Nessun controllo automatico legge un'argomentazione: contro quel difetto esiste la revisione in contesto pulito, il cui verbale vive in [`specs/009-verdetto-raccomandazione/review.md`](../specs/009-verdetto-raccomandazione/review.md).
