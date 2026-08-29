# Contratto di documento — `docs/raccomandazione.md`

Che cosa il deliverable deve contenere, sezione per sezione, **prima che venga scritto**. Sul precedente del contratto di pagina della `008a` e del contratto di narrazione della `008b`: l'ordine — contratto prima della stesura — è la parte del loro metodo che ha retto anche quando il resto non ha retto.

**A che cosa serve, in una riga**: impedire che la stesura decida di suo di saltare un vincolo scomodo, e permettere alla revisione di verificare se una sezione **manca** invece di essere solo breve.

---

## 0. Il destinatario, e i due vincoli che ne discendono

**Chi legge**: un membro del board di StreamWave che **non ha letto alcun documento di questo repository** e **non guarda uno schermo**. Ha competenza di business, non competenza tecnica o statistica. Dispone di una stima della base abbonati che questo progetto non ha.

**V-D1 — nessuna sigla non sciolta.** Ogni sigla del progetto — `BQ1`, `C2`, `BQ2-K3`, `is_high_zero_genre`, `A1` — o è sciolta al primo uso o non compare. È il rilievo `R11` della revisione `007b` applicato preventivamente al documento in cui costa di più.

**V-D2 — nessun rimando come sostituto del contenuto.** Un rimando è ammesso per **approfondire**, mai per **completare**: se un'informazione serve a capire la frase in cui compare, sta lì. È il rilievo `R7` della revisione `008b` — i numeri di `BQ3` non erano usabili perché l'orizzonte era altrove.

---

## 1. Sezione «la risposta»

**Deve contenere**: la risposta come **frase**, in apertura, con la cautela già incorporata dal business case.

**Obblighi:**

- **V-1.1** — la prima frase risponde. Non «i dati mostrano che», non «l'analisi suggerisce»: la risposta;
- **V-1.2** — la cautela sta nella stessa sezione, nella formulazione già pubblicata: l'esito **non dice che l'espansione sarà redditizia, dice che sarebbe coerente**. Fonte: `business_case.md` §3;
- **V-1.3** — l'esito è ancorato. Quante condizioni su tre, con ancora; quale delle tre letture del business case si applica;
- **V-1.4** — la sezione regge l'**estrazione**: se qualcuno ne cita la sola prima frase fuori contesto, quella frase non deve attribuire a StreamWave alcuna misura diretta. È il rischio strutturale di questo deliverable (User Story 5).

**Vietato**: presentare il verdetto come una previsione, o come una raccomandazione di investimento.

---

## 2. Sezione «perché»

**Deve contenere**: le tre condizioni, ciascuna con il proprio esito, la propria ancora e la propria confidenza; la confidenza del verdetto con il suo argomento; il margine di robustezza.

**Obblighi:**

- **V-2.1** — le tre condizioni compaiono **tutte e tre**, nella stessa forma. È la chiusura del rilievo `R2` della `008b`, dove `C1` e `C3` nominate senza `C2` facevano comparire la seconda come un buco;
- **V-2.2** — ciascuna è scritta in italiano comprensibile prima che nella sua forma tecnica. «La categoria musicale non è marginale nel catalogo attuale» viene prima di «`C1`: `Music & Musicals` supera la mediana dei conteggi per categoria»;
- **V-2.3** — la confidenza del verdetto è dichiarata **media**, con l'argomento dell'ereditarietà dal termine più debole (decisione `V5`). Non come convenzione: come conseguenza del fatto che una congiunzione non è più affidabile del suo termine più debole;
- **V-2.4** — la sezione dichiara **quale** delle tre è la più debole, e perché: è `C2`, e la ragione è che poggia su una stima per eccesso;
- **V-2.5** — il margine di robustezza compare qui, ancorato, in **entrambe** le forme (`V9`): quanto il valore supera la soglia, e quanto la stima dovrebbe essere gonfiata perché la conclusione cambi.

**Vietato, con la ragione:**

| Formulazione vietata | Perché |
|---|---|
| «il margine mostra che l'errore è piccolo» | il margine è una **condizione sull'errore**, non una stima dell'errore. Nessuno ha misurato l'errore (`V3`) |
| il margine presentato senza la sua dipendenza dalla soglia | il margine cambia di oltre un fattore tre fra le soglie plausibili: presentarlo come proprietà del solo dato sarebbe fuorviante (`V9`) |
| la confidenza del verdetto come media delle tre | farebbe salire il verdetto sopra `C2` grazie a `C1`: la condizione più forte coprirebbe la più debole (`V5`) |

---

## 3. Sezione «con che cosa entrare»

**Deve contenere**: la regione del catalogo da cui entrare, caratterizzata dai segmenti che vi appartengono; il candidato di punta, ancorato; la dichiarazione che i segmenti non sono alternative disgiunte.

**Obblighi:**

- **V-3.1** — si raccomanda una **regione caratterizzata da segmenti**, mai una partizione di alternative fra cui scegliere. I segmenti si sovrappongono per costruzione (`data_model.md` §18);
- **V-3.2** — la numerosità del quadrante e la posizione del primo in graduatoria sono **ancorate**. Un ordinale su un fatto misurato è ammesso solo se ancorato (corollario (a) di `D5`);
- **V-3.3** — la sezione dichiara che le quantità dei segmenti **non si sommano** e che contare le righe misura il campionamento, non il mercato;
- **V-3.4** — nessuna lettura della coda della graduatoria senza l'esclusione dichiarata dei 7 segmenti a domanda non misurata dalla fonte. Se la coda non viene letta, il vincolo è rispettato per omissione — ed è la scelta più semplice;
- **V-3.5** — dove i 7 segmenti vengono nominati, si dice che portano **domanda non misurata dalla fonte**, mai «domanda bassa» (`kpi_measures.md` §5.3).

**Vietato**: «il segmento migliore è X, quindi entrare da X». Tratta i segmenti come una partizione e afferma il falso.

---

## 4. Sezione «quanto vale»

**Deve contenere**: i due KPI di `BQ3` come intervalli, l'orizzonte, le due qualificazioni d'unità, la tabella di sensibilità, il debito aperto sul benchmark.

**Obblighi:**

- **V-4.1** — `BQ3-K1` e `BQ3-K2` compaiono **sempre** come terna pessimista/centrale/ottimista. Mai un valore isolato, in nessuna posizione, nemmeno in una frase di sintesi. La confidenza è bassa e la regola non è negoziabile (`business_case.md` §6);
- **V-4.2** — l'orizzonte di **12 mesi** è scritto **in questa sezione**, non per rimando (rilievo `R7` della `008b`);
- **V-4.3** — il tasso è dichiarato **lordo**: le disdette sono fuori dal perimetro del progetto;
- **V-4.4** — l'uplift è dichiarato **livello mensile a regime**, non cumulato sull'orizzonte;
- **V-4.5** — la tabella di sensibilità porta, per **ciascuna** base di riferimento, tutti e tre gli scenari. Una colonna sola violerebbe `V-4.1`;
- **V-4.6** — le basi di riferimento portano il **marcatore di non-misurato** e sono dichiarate in prosa come illustrazione parametrica, con l'ipotesi attribuita a **chi legge**;
- **V-4.7** — il debito della `004` sulla verificabilità del benchmark è dichiarato **aperto** qui: il valore centrale poggia su un comunicato che non nomina lo studio, e la verifica esterna dipende da un indirizzo che potrebbe smettere di rispondere (`bq3_scenarios.md` §9);
- **V-4.8** — l'assunzione di trasferimento `A6` è nominata dove i numeri di `BQ3` compaiono: il benchmark descrive un altro operatore, su un altro mercato, otto anni prima.

**Vietato, con la ragione:**

| Formulazione vietata | Perché |
|---|---|
| «l'uplift **non è scalabile**» | `bq3_scenarios.md` §8 dichiara che l'affermazione **è falsa**. La formulazione corretta è più stretta: qui nessuna base viene quantificata e l'artefatto non offre alcuna chiave — non è un presidio, è una rinuncia. È l'errore già registrato come issue `#26` |
| il valore centrale citato da solo | «prendere il valore centrale perché sta meglio in una dashboard comunica una certezza che il dato non ha, ed è la violazione più facile da commettere e la più difficile da vedere a valle» (`bq3_scenarios.md` §5) |
| l'uplift moltiplicato per 12 | produrrebbe un cumulato che vale solo sotto l'assunzione di base costante |

**La copia autorevole per questa sezione è `bq3_scenarios.md` §8**, dove esistono più copie di un'affermazione: è la più stretta, ed è quella che le altre tre riprendono in forma abbreviata.

---

## 5. Sezione «che cosa lo farebbe cambiare»

**Deve contenere**: le condizioni che ribalterebbero la risposta, ciascuna con il proprio meccanismo.

**È la sezione che distingue una raccomandazione da un'opinione, e nessun documento del progetto la contiene ancora.** Se il lavoro sfora, **non si comprime**: si riporta lo sforamento.

**Obblighi — deve nominare almeno queste quattro:**

- **V-5.1** — una **revisione della tabella dei mood**: per il contratto di versione di `content_taxonomy_bridge.md` §5, invalida `C2` invece di correggerlo, e con esso il verdetto;
- **V-5.2** — una **sovrastima maggiore del margine**: se il parallelepipedo eccedesse la sovrapposizione reale di più del margine pubblicato, `C2` cadrebbe e l'esito passerebbe a due su tre — che il business case legge come sostegno parziale, non come argomento non sostenuto;
- **V-5.3** — il **fallimento dell'assunzione di trasferimento**: se i cataloghi proxy non rappresentassero StreamWave, nessuna delle tre condizioni direbbe nulla di StreamWave. È `A1`, e non è verificabile con i dati disponibili;
- **V-5.4** — l'**arrivo di dati che il progetto non ha**: dati comportamentali, di costo, o posteriori al 2021-2022.

**Obbligo di forma — V-5.5**: ciascuna dichiara **che cosa succederebbe**, non solo che è un rischio. «Se la tabella dei mood venisse rivista, `C2` andrebbe ricalcolata e il verdetto con essa» è una condizione; «la tabella dei mood è un limite» non lo è.

---

## 6. Sezione «che cosa questa raccomandazione non è»

**Deve contenere**: i limiti, con la stessa cura delle altre sezioni.

**Obblighi:**

- **V-6.1** — **non è un business case finanziario**: manca il lato costi — licenze, infrastruttura, organico — ed è deliberato. Chi cercasse un ritorno sull'investimento non lo troverà;
- **V-6.2** — **non descrive StreamWave**: i cataloghi sono proxy. `A1` e `A6` restano fuori dalla scala di confidenza per costruzione (`business_case.md` §6), e la sezione le nomina entrambe in forma estesa — è il punto in cui devono sopravvivere all'estrazione di una frase;
- **V-6.3** — **non dice che il pubblico attuale vorrebbe la musica**: la sovrapposizione è fra caratteristiche di contenuto, non fra persone osservate;
- **V-6.4** — **non è una previsione**: i numeri di `BQ3` sono scenari sotto assunzioni dichiarate, non stime di ciò che accadrà;
- **V-6.5** — **i dati si fermano al 2021-2022**, e il benchmark al 2018.

---

## 7. Vincoli che valgono su tutto il documento

- **V-7.1** — severità stretta: ogni numerale in posizione di fatto misurato porta l'ancora o il marcatore di non-misurato;
- **V-7.2** — corollario (b) di `D5`: **nessun numerale in lettere per un fatto misurato**. «Tre condizioni su tre» si scrive con l'ancora sulla cifra;
- **V-7.3** — nessun numero scritto a mano che sia derivabile da due valori pubblicati: se è un confronto, una differenza o un rapporto, è un valore e ha un'ancora (`D5`);
- **V-7.4** — nessun lessico causale su risultati correlazionali (principio IV);
- **V-7.5** — il documento dichiara in apertura che cosa è e a chi si rivolge, e dove vivono i documenti che lo sostengono. Un rimando per approfondire, non per completare (`V-D2`).

---

## 8. Che cosa il contratto **non** fissa

- **l'impaginazione, la lunghezza delle sezioni, l'uso di tabelle o elenchi**: sono scelte della stesura;
- **le parole esatte della risposta**: il contratto fissa che la prima frase risponda e con quale cautela, non come sia formulata;
- **la resa a schermo**: appartiene alla `010b`. Questo contratto fissa il **contenuto**, e un contenuto che regge una lettura su carta.

---

## 9. Come si verifica il rispetto di questo contratto

Ogni obbligo numerato è verificabile leggendo il documento finito, e la revisione in contesto pulito è chi lo fa. **Nessuno di questi obblighi è verificabile da uno script**: il controllo di coerenza vede le ancore, non le affermazioni — è il confine della garanzia dichiarato in `convenzioni-marcatura.md` §8.

Gli obblighi che il controllo automatico presidia **in parte** sono `V-7.1` e `V-7.2`, e solo per le quantità che sa riconoscere: frazioni e ordinali in lettere — «la metà», «un quinto» — gli restano invisibili (`convenzioni-marcatura.md` §6). In un documento che parla di **maggioranza** e di **metà superiore**, quella zona è più larga del solito, ed è presidiata a mano.
