# Contratto di narrazione: che cosa la dashboard dice, alla lettera

**Feature**: 008b-dashboard-narrative-polish | **Data**: 2026-08-27 | **Stato**: **in attesa di approvazione** — punto di fermata 3

## A chi questo testo è rivolto

**Un decisore che non ha letto alcun documento di questo repository.** Non sa che cosa sia un segmento, non sa che cosa distingua una confidenza alta da una media, non ha modo di aprire `docs/` e non aprirebbe una nota a piè di pagina. Legge quattro pagine e se ne va.

È il destinatario dichiarato perché è quello che il criterio di accettazione della constitution nomina — *reggere la presentazione a un board reale* — ed è anche il metro contro cui la revisione in contesto pulito valuterà questo documento (`T035`): **un blocco esatto e incomprensibile è un difetto**, e nessun altro presidio di questa feature può vederlo.

Ne discendono tre conseguenze sulla forma di ogni testo qui sotto: niente gergo non sciolto, niente rimandi a documenti che il lettore non ha, e nessuna frase che abbia bisogno di una seconda frase altrove per non essere fraintesa.

## Che cosa questo documento è

**È il deliverable, non la sua descrizione.** Il contratto di pagina della `008a` disegnava una struttura, e una struttura si descrive; qui il deliverable **è prosa**, e una prosa descritta non è una prosa (`N1`). Ciò che segue è il testo che finirà a schermo, pronto da incollare.

Ogni blocco porta quattro cose, sempre nello stesso ordine (`FR-002`):

1. **dove va** — pagina e spazio riservato dalla `008a` §8;
2. **che cosa dice** — il testo letterale, dentro un blocco delimitato;
3. **quale obbligo lo richiede** — l'identificativo dell'inventario di [data-model.md](../data-model.md) §3, con il requisito di spec che lo formalizza;
4. **da dove viene** — la sezione di documento pubblicato, il principio della constitution o la issue da cui l'affermazione discende.

Dove esiste una **formulazione vicina e sbagliata**, il blocco la dichiara come esclusa. Non è una raffinatezza: sono le frasi che chi costruisce sceglierebbe per comodità, e tre di esse sono obbligatorie per `FR-003`.

## Che cosa questo documento non è

**Non è un manuale di clic.** Dove un testo va è dichiarato in termini di pagina e di spazio riservato; **come** si crea una casella di testo, quale carattere, quale corpo, quale allineamento, quale colore appartiene a chi costruisce, e prescriverlo sarebbe pilotare la GUI per interposta prosa (principio V, `FR-004`).

**Non è la fonte autorevole su ciò che esiste a schermo.** Questo documento dichiara che cosa si è deciso di scrivere; ciò che è stato scritto lo dirà la sezione «Esito della costruzione» di [quickstart.md](../quickstart.md), e dove i due divergono **quella** prevale (`F9` della `008a`, ereditata invariata).

**Non pubblica alcun valore.** Nessun numero di KPI è trascritto qui, per la stessa ragione per cui il contratto della `008a` non ne trascriveva: una seconda copia di un valore è una copia che può divergere dall'originale senza che nulla lo segnali.

---

# Parte I — I vincoli

Questa parte precede i blocchi e li governa tutti. È scritta per prima perché un blocco scritto prima che il proprio vincolo esista è un blocco scritto senza di esso, e riscriverlo dopo non è la stessa cosa.

## 1. La lista chiusa dei numerali (`N2`, `FR-016`)

**Nessun blocco di narrazione contiene una cifra**, salvo le voci di questa lista. La lista è chiusa: aggiungervi una voce è una modifica di questo contratto, da riapprovare, non una scelta di chi costruisce.

| Voce | Dove compare | Perché non può venire da una misura | Fonte |
|---|---|---|---|
| **2021** — copertura del catalogo video | `BL-IN-4`, e in nessun altro blocco | il modello non ha dimensione di calendario, quindi nessuna misura può produrlo. È però un fatto **osservato**: è il massimo del campo `release_year` di `dim_title` | `data_model.md` §16 e §18; `business_case.md` `A2` |
| **2022** — copertura del catalogo musicale | `BL-IN-4`, e in nessun altro blocco | come sopra per l'assenza di calendario, ma **non** è un fatto osservato: il catalogo musicale non espone alcun campo di data, e l'anno è preso dalla documentazione della fonte | `data_model.md` §18, che lo dichiara non verificabile; `business_case.md` `A2` |

**L'obbligo che la lista si porta dietro** (`FR-018`): i due anni **non hanno lo stesso statuto**, e il testo che li porta a schermo deve distinguerli. Pubblicare come osservata una cosa che nessuno ha osservato è la sola categoria di errore contro cui, per `convenzioni-marcatura.md` §8, non esiste presidio automatico. `BL-IN-4` è l'unico blocco autorizzato a nominarli, ed è costruito su questa distinzione.

### 1.1 Che cosa in questo contratto conta come cifra, e che cosa no

Una precisazione che `T022` (prova 6) ha bisogno di avere prima di eseguirsi, o la verifica diventa una questione di interpretazione.

- **Conta come cifra** qualunque numerale in posizione di quantità, in cifre o in lettere. Il divieto del corollario (b) di `convenzioni-marcatura.md` §7 vale a schermo esattamente come su una pagina, e qui è applicato in forma **più severa**: nessun blocco scrive «due», «tre», «sette», nemmeno riferito a cose che non sono misure, e nemmeno nella forma dei pronomi che contano al posto del numerale — «i due», «entrambi». Dove il testo dovrebbe contare, **enumera** (`alta, media o bassa`) o **rimanda alla marcatura che il lettore ha davanti** (`i segmenti che portano l'avvertimento in graduatoria`), che è la regola operativa di `N2` e l'oggetto di `FR-017`.

L'articolo indeterminativo — «una tabella», «un livello» — non è un numerale e non è toccato dalla regola: introduce un oggetto, non ne dichiara la quantità.
- **Non conta come cifra** un identificativo: `C1`, `C3` sono nomi, non quantità. Sono governati da un obbligo diverso — `OB-34`, che impone di scioglierli sulla stessa pagina in cui compaiono — e ciascuno dei blocchi che li usa lo fa.

**Perché la regola più severa e non quella minima.** Perché la regola minima obbligherebbe chi verifica a decidere, numerale per numerale, se sia in posizione di fatto misurato; la regola severa si verifica leggendo. È lo stesso spostamento dell'onere che il corollario (c) fa sul controllo automatico, applicato qui a una verifica che nessuno script eseguirà mai.

## 2. I tre divieti sul registro (`N7`, `FR-020`)

La narrazione ha tre registri ammessi, e nessun altro: **che cosa il valore misura**, **che cosa il valore non permette di concludere**, **quale assunzione lo regge**. Nessun blocco formula una raccomandazione, un verdetto o una previsione.

| Divieto | Che cosa esclude | Da dove viene |
|---|---|---|
| **nessun lessico causale** | qualunque frase che presenti una relazione fra attributi di catalogo come causa o effetto — «il mood simile attira il pubblico», «la vicinanza dei profili spiega» | principio IV; `business_case.md` §8: *«la somiglianza di mood non descrive il comportamento delle persone»*; `content_taxonomy_bridge.md` §7 |
| **nessun superlativo né ordinale** riferito a un fatto misurato che il lettore non veda a schermo | «il segmento più promettente», «il secondo per affinità», «quattro volte più ricco» | `convenzioni-marcatura.md` §7, corollario (a) |
| **nessuna affermazione sul pubblico** | qualunque frase che attribuisca a delle persone un comportamento, un desiderio o una preferenza | `data_model.md` §18: il modello non contiene alcuna entità che rappresenti una persona |

**Il caso da cercare per primo è la parola «domanda»**, che è a schermo dalla `008a` come nome di un indicatore e che una prosa distratta trasforma in un comportamento osservato. Il blocco `BL-Q2-10` esiste apposta per dichiarare che cosa quella parola nomini davvero.

## 3. Il divieto di comporre la regola di decisione (`N6`, `FR-019`)

`C1` compare sulla pagina `BQ1`, `C3` sulla pagina `BQ2`, **ciascuna da sola**. Nessun blocco, su nessuna pagina:

- **conta** le condizioni, né scrive «due su tre», «tre su tre», o qualunque frazione o ordinale riferito ad esse;
- **nomina `C2`**, che non esiste come valore ancorato in alcun artefatto (issue `#17`);
- **pubblica un esito complessivo** della regola di decisione, in alcuna forma.

**Che cosa questo contratto scrive al posto del silenzio.** La `008a` poteva tacere perché non aveva prosa; un documento che scrive prosa e tace lascia in piedi l'inferenza che la geometria della pagina suggerisce — un segno verde accanto a `C1` *invita* a concludere che l'argomento sia sostenuto. Ciascuno dei due blocchi dichiara quindi, con la stessa formulazione, che **quella condizione da sola non decide** e che questa dashboard non pubblica alcun esito complessivo. È l'unica formulazione che nega l'inferenza senza costruire l'affermazione che la nega: dire che una condizione da sola non decide non richiede di sapere quante siano.

**La formulazione dei due blocchi è deliberatamente identica** nell'attacco e nella chiusa. Non è pigrizia: due formulazioni diverse inviterebbero a cercare la differenza, e la differenza non c'è.

## 4. Le formulazioni escluse

Una formulazione esclusa è una frase **vicina a quella corretta e sbagliata**, dichiarata perché chi costruisce non la scelga per comodità davanti allo schermo. Tre sono obbligatorie (`FR-003`) e vivono nei blocchi che le nominano.

| # | Formulazione esclusa | Dove sarebbe comoda | Perché è sbagliata | Blocco che la esclude |
|---|---|---|---|---|
| 1 | «differenza fra la durata del catalogo video e quella del catalogo musicale», e ogni variante che sottintenda i cataloghi interi | è la lettura naturale di un numero che è una differenza di durate | il lato video sono i **soli film**; `data_model.md` §18 la dichiara alla lettera *«una lettura sbagliata di quel numero»*, e aggiunge che nulla nel modello la smentisce | `BL-Q1-5` |
| 2 | «domanda bassa» riferita ai segmenti marcati | è più corta e sembra dire la stessa cosa | il valore misura la **copertura della fonte**, non la domanda; `kpi_measures.md` §5.3 prescrive esplicitamente di presentarli come *«non misurati dalla fonte», non come «a domanda bassa»* | `BL-Q2-2` |
| 3 | «l'uplift non è scalabile», e ogni variante che presenti come impossibile un'operazione che è soltanto non fornita | è la sintesi comoda di una frase lunga | `bq3_scenarios.md` §8 dichiara quella versione **falsa** alla lettera: *«il valore **è** scalabile, chiunque disponga di una stima di abbonati lo moltiplica in pochi secondi»*. Ciò che è vero è che qui nessuna base utenti viene quantificata | `BL-Q3-8` |

**Una quarta formulazione è esclusa da tutta la pagina `BQ2`**, e non è fra le obbligatorie: «i segmenti in fondo alla graduatoria sono i meno interessanti». Compone il divieto 2 con un ordinale, ed è il modo in cui la lettura sbagliata rientrerebbe dalla porta di servizio.

---

# Parte II — I blocchi

Trentadue blocchi. Il testo dentro i riquadri è **letterale**: è ciò che va a schermo, e `T021` (prova 5) verifica la coincidenza alla lettera.

Ogni blocco ha un **titolo** e un **testo**. Il titolo è la riga che il lettore incontra per prima e serve a fargli decidere se leggere il resto; a schermo sarà distinguibile dal testo, ma **come** distinguerlo — grassetto, corpo maggiore, colore — è di chi costruisce.

## 5. Pagina di ingresso

**Spazio**: una fascia a piena larghezza sotto la scheda della North Star (`BL-IN-1`, `BL-IN-2`, `BL-IN-3`), più la striscia a piè di pagina (`BL-IN-4`).

**Perché quest'ordine.** L'assunzione dei proxy va per prima perché è la sola che, se non letta, rende tutto il resto frainteso. La copertura temporale sta a piè di pagina perché è l'unico blocco che vale identico su tutte le pagine e che il lettore ritrova dove si aspetta una nota di edizione.

---

### `BL-IN-1` — L'assunzione strutturale dei proxy

**Obblighi**: `OB-01` · **Requisito**: `FR-006`
**Fonte**: constitution, *Vincoli di Dominio e di Dato* — l'assunzione «DEVE essere dichiarata in ogni artefatto rivolto all'utente finale»; `business_case.md` `A1`

> **Titolo**
>
> ```text
> Questi numeri non descrivono StreamWave
> ```
>
> **Testo**
>
> ```text
> Sono calcolati su cataloghi pubblici reali, usati come riferimento: il catalogo video di
> Netflix sta al posto del catalogo attuale di StreamWave, il catalogo musicale di Spotify
> sta al posto del mercato musicale accessibile. È un'ipotesi dichiarata, e nessun dato di
> StreamWave esiste in questo progetto. Ogni volta che qui si legge «il nostro catalogo», si
> intende il catalogo di riferimento.
> ```

**Perché sta sulla pagina di ingresso e non altrove**: è l'unica affermazione il cui mancato incontro rende sbagliata la lettura di ogni pagina successiva. È anche la sola che la constitution impone **per estensione**, indipendentemente da quale numero il lettore guardi.

---

### `BL-IN-2` — Che cosa questa dashboard non risponde

**Obblighi**: `OB-02` · **Requisito**: `FR-007`
**Fonte**: principio IV; `business_case.md` §8 (*Out of scope*) e `A3`

> **Titolo**
>
> ```text
> A cosa questa dashboard non risponde
> ```
>
> **Testo**
>
> ```text
> Non dice se convenga entrare nel mercato musicale.
> Non contiene il lato costi — licenze, infrastruttura, organico — e senza quello non c'è
> alcun ritorno sull'investimento da leggere qui.
> Non osserva le persone: nessuna delle fonti di questo progetto contiene visioni, ascolti,
> abbonamenti o ricavi.
> ```

**Perché è formulata per negazioni successive e non come un capoverso unico**: le tre esclusioni sono indipendenti, e un lettore che si ferma alla prima ha comunque letto una cosa vera e completa.

---

### `BL-IN-3` — La scala di confidenza, e ciò che non misura

**Obblighi**: `OB-03` · **Requisito**: `FR-008`
**Fonte**: principio I; `business_case.md` §6 e la sua sottosezione *Cosa questa scala non misura*

> **Titolo**
>
> ```text
> Come leggere l'etichetta di confidenza
> ```
>
> **Testo**
>
> ```text
> Accanto a ogni indicatore compare un livello: alta, media o bassa. Misura quanti passaggi
> interpretativi separano il dato osservato dal numero mostrato.
> Alta: il numero si legge direttamente sul dato reale, senza corrispondenze costruite né
> ipotesi interposte.
> Media: fra il dato e il numero si interpone almeno una corrispondenza costruita
> dall'analista o un'ipotesi dichiarata.
> Bassa: il numero dipende da ipotesi che i dati disponibili non permettono di verificare.
> Questa etichetta non dice quanto il numero descriva StreamWave. Un indicatore a confidenza
> alta è alto rispetto al catalogo di riferimento, non rispetto a StreamWave.
> ```

**Perché la chiusa è la parte più importante del blocco** (`N5`): la scala misura la solidità del calcolo, non la trasferibilità. Senza di essa, un'etichetta «alta» accanto alla metrica di riferimento si legge come una garanzia su StreamWave — che è precisamente ciò che `business_case.md` §6 dichiara che nessun livello autorizza.

**Che cosa il blocco non ripete, e dove sta invece.** Che un valore a confidenza bassa si presenti obbligatoriamente come intervallo è detto su `BQ3` da `BL-Q3-1`, cioè sulla pagina in cui il lettore ha quell'intervallo davanti. Qui la scala definisce i livelli e non prescrive formati.

---

### `BL-IN-4` — La copertura temporale, con i due statuti distinti

**Obblighi**: `OB-04` · **Requisiti**: `FR-007`, `FR-018`
**Fonte**: principio IV; `business_case.md` `A2`; `data_model.md` §18 — *«I due anni non hanno lo stesso statuto, ed è la parte che conta»*
**Unico blocco autorizzato a portare una cifra** (lista chiusa, §1)

> **Titolo**
>
> ```text
> Fin dove arrivano i dati
> ```
>
> **Testo**
>
> ```text
> Il catalogo video si ferma al 2021: è l'anno di uscita più recente presente nel dato. Per il
> catalogo musicale la documentazione della fonte indica il 2022. Sono fotografie di momenti
> diversi. Nessuna conclusione presentata qui riguarda ciò che è accaduto dopo.
> ```

**Come la distinzione è realizzata**: non con un'etichetta accanto a ciascun anno, che il lettore salterebbe, ma con il verbo — *«presente nel dato»* contro *«la documentazione della fonte indica»*. Il primo anno è dichiarato osservato, il secondo è attribuito a chi lo afferma.

> **Che cosa questa formulazione dichiara in meno, dichiarato qui perché non passi in silenzio.** `FR-018` chiede che i due anni siano distinti per statuto — *osservato* sul lato video, *dichiarato dalla fonte e non verificabile* sul lato musicale. La distinzione fra osservato e dichiarato è realizzata; la **non verificabilità** non è più detta a schermo, e con essa la sua ragione — che il catalogo musicale non porta alcun campo di data, per cui nessuno in questo progetto potrebbe verificare quell'anno nemmeno volendo (`data_model.md` §18).
>
> Il requisito è quindi **indebolito, non soddisfatto**, ed è registrato come tale in §13. È una scelta di brevità legittima: il blocco resta vero, e un lettore che si ferma qui non conclude nulla di falso. Ciò che perde è la ragione per cui i due anni non sono intercambiabili.

---

## 6. Pagina `BQ1` — Posizionamento

**Spazio**: la fascia sotto la fila delle tre schede, con tre aree allineate alle schede. `BL-Q1-1`, `BL-Q1-1b`, `BL-Q1-2` e `BL-Q1-3` stanno nell'area della metrica di riferimento; `BL-Q1-4` e `BL-Q1-5` in quella della differenza di durata; `BL-Q1-6`, `BL-Q1-7` e `BL-Q1-8` in quella della sovrapposizione dei profili.

---

### `BL-Q1-1` — Perché la confidenza della metrica di riferimento è alta

**Obblighi**: `OB-05` · **Requisito**: `FR-009`
**Fonte**: contratto di dashboard `008a`, punto 2; `business_case.md` §6; `kpi_operators.md` §11

> **Titolo**
>
> ```text
> Perché la confidenza è alta
> ```
>
> **Testo**
>
> ```text
> Questo valore conta quanta parte del catalogo di riferimento è già a contenuto musicale,
> leggendo la classificazione che il catalogo porta con sé. Fra il dato e il numero non si
> interpone alcuna corrispondenza costruita né alcuna ipotesi.
> ```

---

### `BL-Q1-1b` — Che cosa il conteggio legge davvero

**Obblighi**: `OB-35` · **Requisito**: `FR-009`
**Fonte**: `business_case.md` §3, nota in loco della `007b` (rilievo `R11` della revisione `001`)
**Sta in coda a `BL-Q1-1`**, nella stessa area della fascia

> **Testo**
>
> ```text
> Il conteggio legge una sola etichetta del catalogo: la categoria dedicata al contenuto
> musicale. Un titolo musicale classificato altrove non vi entra.
> ```

**Perché esiste**: la nota in loco della `007b` corregge la descrizione della metrica di riferimento — il business case la descriveva enumerando tipologie di contenuto, mentre la misura legge **una sola etichetta**. È un limite di lettura di un valore visibile, cioè la classe che la regola di selezione di [data-model.md](../data-model.md) §6 manda a schermo.

**Perché non ha un titolo proprio**: sta sotto il titolo di `BL-Q1-1` e ne continua il discorso. Separarlo con un titolo suggerirebbe che sia un limite di natura diversa dalla confidenza, mentre è la ragione per cui quella confidenza alta vale su un perimetro stretto.

---

### `BL-Q1-2` — La quota non è la condizione

**Obblighi**: `OB-06` · **Requisito**: `FR-009`
**Fonte**: `kpi_measures.md` §2.3, *«`C1` — la condizione della North Star, che non è la quota»*

> **Titolo**
>
> ```text
> Questa quota non dice se C1 sia soddisfatta
> ```
>
> **Testo**
>
> ```text
> La quota e la condizione C1 sono letture diverse dello stesso catalogo. La quota è una
> proporzione sull'intero catalogo; C1 chiede invece se la categoria musicale si collochi
> nella metà superiore delle categorie per numero di titoli. Una categoria può stare nella
> metà superiore e restare al tempo stesso una frazione piccola del totale: le letture non si
> contraddicono, misurano cose diverse.
> ```

**Nota su una cifra che non compare**: la quota e la mediana delle categorie sono entrambe pubblicate e ancorate in `kpi_measures.md` §2.1 e §2.3. Qui non si trascrivono: la quota è la scheda che il lettore ha davanti, e la mediana è un valore intermedio che a schermo non serve a nulla se non a introdurre una cifra senza fonte.

---

### `BL-Q1-3` — `C1` da sola non decide

**Obblighi**: `OB-07`, e `OB-34` per lo scioglimento della sigla · **Requisiti**: `FR-019`, `FR-021`
**Fonte**: `008a` `F6`; contratto di dashboard `008a`, punto 3; `business_case.md` §3; issue `#17`

> **Titolo**
>
> ```text
> Che cos'è C1, e che cosa non decide
> ```
>
> **Testo**
>
> ```text
> C1 è il nome che il business case dà a una condizione della propria regola di decisione: il
> contenuto musicale non è residuale nel catalogo attuale. Da sola, questa condizione non
> decide nulla. Questa dashboard non pubblica alcun esito complessivo della regola di
> decisione.
> ```

**Formulazione gemella**: `BL-Q2-8`, identica nell'attacco e nella chiusa. Vedi Parte I §3.

---

### `BL-Q1-4` — Perché la confidenza della differenza di durata è alta

**Obblighi**: `OB-08` · **Requisito**: `FR-009`
**Fonte**: contratto di dashboard `008a`, punto 2; `kpi_operators.md` §11

> **Titolo**
>
> ```text
> Perché la confidenza è alta
> ```
>
> **Testo**
>
> ```text
> Il valore è la differenza fra una durata mediana osservata sul lato video e una durata
> mediana osservata sul lato musicale: nessuna corrispondenza costruita, nessuna ipotesi
> interposta.
> ```

---

### `BL-Q1-5` — L'asimmetria del confronto

**Obblighi**: `OB-09` · **Requisiti**: `FR-011`, `FR-003`
**Fonte**: `data_model.md` §18 (categoria *di dominio*) e §19; `kpi_measures.md` §3.4; `business_case.md` §8
**Formulazione esclusa**: «differenza fra la durata del catalogo video e quella del catalogo musicale», e ogni variante che sottintenda i cataloghi interi

> **Titolo**
>
> ```text
> Che cosa si sta confrontando
> ```
>
> **Testo**
>
> ```text
> Sul lato video entrano i soli film. Le serie misurano la propria durata in stagioni. Sul
> lato musicale entra invece il catalogo intero. Il confronto è quindi asimmetrico per
> costruzione, e la quota di film accanto al valore dice quanta parte del catalogo video vi
> partecipi.
> ```

**Perché la formulazione esclusa è pericolosa e non solo imprecisa**: `data_model.md` §18 la nomina come *«una lettura sbagliata di quel numero»* e aggiunge che **nulla nel modello la smentisce**. È un limite della categoria *sconsigliato*: l'operazione riesce, il risultato è privo del significato che chi lo legge gli attribuisce, e questo blocco è l'unico presidio esistente.

**Rimando invece di ripetizione** (`FR-017`): il testo dice *«la quota di film accanto al valore»* e non ripete la quota. La quota è a schermo come misura dalla `008a` (`CP-1`), e si aggiorna con essa.

---

### `BL-Q1-6` — Perché la confidenza della sovrapposizione è media

**Obblighi**: `OB-10` · **Requisito**: `FR-009`
**Fonte**: `kpi_operators.md` §11; `data_model.md` §15; `content_taxonomy_bridge.md` §7

> **Titolo**
>
> ```text
> Perché la confidenza è media
> ```
>
> **Testo**
>
> ```text
> Questo valore poggia su una tabella che assegna a ciascuna categoria video un profilo di
> energia, positività e ritmo. Quel profilo è deciso secondo un criterio scritto e pubblico, e
> non è osservato da alcuna fonte.
> ```

---

### `BL-Q1-7` — La sovrapposizione è una stima per eccesso

**Obblighi**: `OB-11` · **Requisito**: `FR-010`
**Fonte**: `kpi_operators.md` §4 e §12 — assegnato **per nome** a questa feature: *«I limiti di §4, §6 e §7.2 devono essere ereditati e ripresentati in forma comprensibile da chi costruirà la narrazione»*; `kpi_measures.md` §4.3

> **Titolo**
>
> ```text
> Questa sovrapposizione è una stima per eccesso
> ```
>
> **Testo**
>
> ```text
> La regione con cui il catalogo musicale viene confrontato è costruita prendendo, asse per
> asse, il valore minimo e quello massimo dei profili video. Include quindi combinazioni di
> energia, positività e ritmo che nessuna categoria video occupa davvero: un'energia pari a
> quella della categoria più energica insieme a una positività pari a quella della categoria
> più cupa, per esempio, anche se nessuna categoria è insieme l'una e l'altra.
> ```

**Sui superlativi che compaiono nel testo**: *«la categoria più energica»* e *«la più cupa»* non sono affermazioni su un fatto misurato — non nominano alcuna categoria e non pubblicano alcun valore. Sono l'esempio che rende concreta la costruzione geometrica, ed è preso alla lettera da `kpi_measures.md` §4.3. Il divieto del corollario (a) riguarda i superlativi **riferiti a un fatto misurato**; questo non lo è, e la distinzione è dichiarata qui perché `T024` (prova 8) la incontrerà.

> **Che cosa questa formulazione dichiara in meno.** `OB-11` impone due cose: che la sovrapposizione sia una stima per eccesso, e che **la sovrapposizione reale sia minore o uguale a quella mostrata, quanto minore il progetto non lo misura**. Il titolo del blocco porta la prima e il testo ne spiega il meccanismo; la seconda non è più a schermo.
>
> `FR-010` è quindi **indebolito** su questo obbligo, ed è il caso più oneroso dei tre di questa pagina: `kpi_operators.md` §12 assegna il limite di §4 **per nome** a questa feature, e ciò che cade è precisamente la parte che dichiara di non sapere quanto grande sia lo scarto. Un lettore che si ferma al titolo sa che il numero è gonfiato; non sa che di quanto nessuno lo ha misurato.
>
> Registrato in §13. Il blocco resta vero e non afferma nulla di falso.

---

### `BL-Q1-8` — Perché il valore è alto quasi per costruzione

**Obblighi**: `OB-12` · **Requisiti**: `FR-009`, `FR-010`
**Fonte**: `kpi_measures.md` §4.3, *«Un secondo limite, più facile da perdere»*

> **Titolo**
>
> ```text
> Perché questo valore è alto per costruzione
> ```
>
> **Testo**
>
> ```text
> Gli estremi di ciascun asse provengono dalla scala a passi regolari con cui sono stati
> assegnati i profili, non dal catalogo video in sé: sono una proprietà del criterio prima che
> del catalogo. L'intervallo che ne risulta è ampio su ogni asse.
> ```

> **Che cosa questa formulazione dichiara in meno.** `OB-12` chiede che l'ampiezza degli intervalli sia dichiarata **come la ragione principale per cui la confidenza resta media**. Il blocco dichiara l'ampiezza e la sua provenienza; il legame con la confidenza non è più scritto, e nemmeno il passaggio che lo rendeva leggibile — *un intervallo ampio è facile da coprire*.
>
> Il titolo afferma che il valore è alto per costruzione, e il testo ne dà la causa geometrica; che questo sia anche il motivo dell'etichetta «media» accanto al numero, il lettore lo deve dedurre. `FR-009` è **indebolito** su questo obbligo, `FR-010` resta soddisfatto: l'ampiezza è dichiarata come proprietà del criterio, che è ciò che `kpi_measures.md` §4.3 chiama il limite «più facile da perdere».
>
> Registrato in §13.

---

## 7. Pagina `BQ2` — Segmento di ingresso

**Spazio**: la fascia sotto la graduatoria. È **la fascia più carica per numero di obblighi** ([data-model.md](../data-model.md) §2), e i blocchi sono ordinati per rendere il taglio governabile se non basta: prima i limiti che riguardano la lettura di un valore visibile, poi quelli che riguardano la pagina nel suo insieme.

**Se la fascia non basta** (`N4`): si taglia il testo, non si allarga la fascia a spese della graduatoria. L'ordine di taglio proposto è dal fondo — `BL-Q2-9` per primo, poi `BL-Q2-5` — e ogni taglio va annotato con l'obbligo che ha ridotto o scoperto. **`BL-Q2-3` non si taglia prima di `BL-Q2-4`**, che dopo la revisione dei testi ne porta la ragione. **`BL-Q2-2` e `BL-Q2-10` non si tagliano in nessun caso**: il primo è l'unico presidio contro una lettura che `kpi_measures.md` §5.3 vieta alla lettera, il secondo è l'unico blocco della pagina che dichiara che cosa la parola «domanda» nomini.

---

### `BL-Q2-1` — Perché la confidenza dell'indice di domanda è media

**Obblighi**: `OB-13` · **Requisito**: `FR-009`
**Fonte**: `business_case.md` §6 (che nomina questo KPI come esempio della scala); `kpi_operators.md` §11

> **Titolo**
>
> ```text
> Perché la confidenza è media
> ```
>
> **Testo**
>
> ```text
> L'indice di domanda aggrega per segmento un indicatore di popolarità pubblicato dalla fonte
> musicale. La fonte non dichiara come quell'indicatore sia costruito, e questo progetto lo
> usa come approssimazione della domanda di mercato
> ```

---

### `BL-Q2-2` — I segmenti che portano l'avvertimento

**Obblighi**: `OB-14`, `OB-15` · **Requisiti**: `FR-012`, `FR-003`
**Fonte**: `kpi_operators.md` §5.1 (`D7`); `kpi_measures.md` §5.3 e §7.4
**Formulazione esclusa**: «domanda bassa» riferita a questi segmenti
**Non tagliabile**

> **Titolo**
>
> ```text
> I segmenti che portano l'avvertimento in graduatoria
> ```
>
> **Testo**
>
> ```text
> Per questi segmenti l'indice di domanda non è basso: è non misurato dalla fonte. Più della
> metà delle loro righe porta popolarità nulla, la mediana cade dentro quella metà, e il
> valore che ne esce misura la copertura del dato invece della domanda. La loro posizione in
> fondo alla graduatoria misura quindi l'assenza di segnale, non una priorità bassa
> ```

**Rimando invece di ripetizione** (`FR-017`): il testo dice *«i segmenti che portano l'avvertimento in graduatoria»* e non ne scrive il numero. L'avvertimento viene da `segment_display`, cioè da una colonna del modello, e si aggiorna con essa; un numero digitato qui sopravvivrebbe a un ricalcolo che lo cambiasse.

**Perché questo blocco non si taglia**: `kpi_measures.md` §5.3 prescrive testualmente la presentazione da adottare e quella da evitare. Senza questo blocco la coda della graduatoria si legge come una classifica di preferenza quando è in parte una classifica di copertura del dato — ed è l'unico punto della pagina in cui una lettura sbagliata è anche la più naturale.

> **Che cosa questa formulazione dichiara in meno.** `OB-14` è servito per intero: la formulazione esclusa è negata alla lettera nella prima riga. `OB-15` no. Il blocco dice che cosa quella posizione misura — l'assenza di segnale — ma non dice più che i segmenti marcati **vanno esclusi da qualunque lettura della coda della graduatoria**, che è la prescrizione testuale di `kpi_measures.md` §7.4.
>
> `FR-012` è quindi **indebolito** sulla metà `OB-15`: resta la constatazione, cade l'istruzione. Registrato in §13.1.

---

### `BL-Q2-3` — Perché la confidenza dell'affinità è media

**Obblighi**: `OB-16` · **Requisito**: `FR-009`
**Fonte**: `content_taxonomy_bridge.md` §7; `kpi_operators.md` §11

> **Titolo**
>
> ```text
> Perché la confidenza è media
> ```
>
> **Testo**
>
> ```text
> L'affinità confronta un profilo osservato sul lato musicale con un profilo assegnato sul
> lato video. La scala su cui questi profili si incontrano è ancorata solo agli estremi:
> nessun valore osservato ne calibra il centro.
> ```

---

### `BL-Q2-4` — Che cosa l'affinità permette di dire

**Obblighi**: `OB-17` · **Requisito**: `FR-010`
**Fonte**: `kpi_operators.md` §6 e §12 (assegnato **per nome** a questa feature); `kpi_measures.md` §6.3, *«Il limite specifico, che è severo»*

> **Titolo**
>
> ```text
> Che cosa questo numero permette di dire
> ```
>
> **Testo**
>
> ```text
> Permette di confrontare i segmenti fra loro. Non permette di leggerne la grandezza in
> assoluto: dire quanto un segmento sia affine, in sé, non ha significato
> ```

**`OB-17` resta servito per intero**, ma la sua **ragione** non vive più in questo blocco: che il centro della scala non sia ancorato a nulla di osservato lo dice `BL-Q2-3`, poco sopra nella stessa fascia. Ne discende un vincolo per la costruzione: **`BL-Q2-3` non si taglia prima di `BL-Q2-4`**, o questo blocco resta un divieto senza motivo.

---

### `BL-Q2-5` — Perché la confidenza del punteggio è media

**Obblighi**: `OB-18` · **Requisito**: `FR-009`
**Fonte**: `kpi_operators.md` §7 e §11

> **Titolo**
>
> ```text
> Perché la confidenza è media
> ```
>
> **Testo**
>
> ```text
> Il punteggio di priorità compone la domanda e l'affinità, ed eredita il livello dei valori
> da cui nasce: non può essere più solido di essi.
> ```

---

### `BL-Q2-6` — Punteggio e quadrante non si fondono

**Obblighi**: `OB-19` · **Requisito**: `FR-010`
**Fonte**: `kpi_operators.md` §7.2 e §12 (assegnato **per nome** a questa feature)

> **Titolo**
>
> ```text
> Punteggio e quadrante rispondono a domande diverse
> ```
>
> **Testo**
>
> ```text
> Il quadrante dice se un segmento supera insieme la soglia di domanda e quella di affinità:
> è una risposta per sì o per no, e non cambia a seconda di quanto sopra la soglia il
> segmento si trovi. Il punteggio dice invece quanto un segmento sia preferibile a un altro,
> anche fra segmenti che stanno tutti dentro o tutti fuori dal quadrante
> ```

> **Che cosa questa formulazione dichiara in meno.** Il blocco distingue le due letture; cade il caso concreto che le rende non intercambiabili — **un segmento può avere punteggio alto e restare fuori dal quadrante**, con affinità alta e domanda appena sotto la soglia.
>
> È il caso che `kpi_operators.md` §7.2 nomina come quello che la fusione *«nasconderebbe»*, e la fusione è ciò che `OB-19` esiste per impedire: senza di esso il blocco dice che le due letture rispondono a domande diverse, ma non mostra dove il lettore sbaglierebbe. `FR-010` è **indebolito** su questo obbligo, ed è il secondo dei tre limiti che `kpi_operators.md` §12 assegna **per nome** a questa feature a subire un taglio. Registrato in §13.1.

---

### `BL-Q2-7` — Che cosa non si può fare con questa graduatoria

**Obblighi**: `OB-20`, `OB-21` · **Requisito**: `FR-011`
**Fonte**: `data_model.md` §18 (entrambi in categoria *sconsigliato*) e §19; `kpi_measures.md` §5.4; `business_case.md` §8

> **Titolo**
>
> ```text
> Che cosa non si può fare con questa graduatoria
> ```
>
> **Testo**
>
> ```text
> I segmenti si sovrappongono: una stessa traccia appartiene a più segmenti. Sommare una
> quantità su più segmenti non ricostruisce il catalogo, lo eccede.
> Contare le righe di un segmento, poi, non lo dimensiona: il catalogo musicale di
> riferimento è campionato, e un conteggio di righe misura il campionamento invece del
> mercato.
> ```

**Perché entrambi in un blocco solo**: appartengono alla stessa categoria di `data_model.md` §18 — *sconsigliato*, cioè «il calcolo riesce, e il risultato è privo di significato» — e sono le **uniche due operazioni** che un lettore compie spontaneamente davanti a una graduatoria. Separarli su due blocchi distanti li renderebbe leggibili uno senza l'altro.

**Perché il testo non quantifica lo sbilanciamento del campione**: `data_model.md` §18 dichiara deliberatamente di non pubblicare né il conteggio massimo né alcuna misura di dispersione, e affermare che lo scostamento sia grande — o rassicurare che sia piccolo — sarebbe un numero senza fonte travestito da valutazione.

> **Che cosa questa formulazione dichiara in meno.** `OB-21` è servito per intero. `OB-20` a metà: resta che sommare eccede il catalogo, cade che **la graduatoria non è un elenco di alternative che si escludono a vicenda**.
>
> È la metà che `data_model.md` §18 dichiara più insidiosa delle due — *«la rappresentazione corretta di una sovrapposizione assomiglia in tutto a quella di una partizione, e la differenza non compare in nessun numero pubblicato»* — e la graduatoria è precisamente la visuale che la fa assomigliare a un elenco di alternative. `FR-011` è **indebolito** su questo obbligo, e registrato in §13.1.

---

### `BL-Q2-8` — `C3` da sola non decide

**Obblighi**: `OB-22`, e `OB-34` per lo scioglimento della sigla · **Requisiti**: `FR-019`, `FR-021`
**Fonte**: `008a` `F6`; contratto di dashboard `008a`, punto 3; `business_case.md` §3; `kpi_operators.md` §7.2; issue `#17`

> **Titolo**
>
> ```text
> Che cos'è C3, e che cosa non decide
> ```
>
> **Testo**
>
> ```text
> C3 è il nome che il business case dà a una condizione della propria regola di decisione:
> esiste almeno un segmento musicale che si colloca insieme nella metà superiore per domanda
> e nella metà superiore per affinità. Da sola, questa condizione non decide nulla. Questa
> dashboard non pubblica alcun esito complessivo della regola di decisione.
> ```

**Formulazione gemella**: `BL-Q1-3`, identica nell'attacco e nella chiusa. Vedi Parte I §3.

---

### `BL-Q2-9` — Le due visuali non si filtrano a vicenda

**Obblighi**: `OB-23` · **Requisito**: `FR-015`
**Fonte**: `008a`, scostamento registrato in `T028` dell'esito di costruzione; issue `#21`
**Primo blocco della fascia da tagliare, se la fascia non basta**

> **Titolo**
>
> ```text
> Le visuali di questa pagina non si filtrano a vicenda
> ```
>
> **Testo**
>
> ```text
> Selezionare un punto nella dispersione non riduce la graduatoria, che mostra sempre tutti i
> segmenti.
> ```

**Che cosa questo blocco non fa**: non riapre l'issue `#21`. Dichiara lo stato costruito, che è vero indipendentemente da come e se quell'issue verrà chiusa.

---

### `BL-Q2-10` — Che cosa significa qui la parola «domanda»

**Obblighi**: `OB-33` · **Requisiti**: `FR-011`, `FR-020`
**Fonte**: `data_model.md` §18 (categoria *di dominio*), *«Non contiene alcuna entità che rappresenti una persona»*; `business_case.md` `A3` e §8
**Non tagliabile**

> **Titolo**
>
> ```text
> Che cosa significa qui la parola «domanda»
> ```
>
> **Testo**
>
> ```text
> Nomina un indice di popolarità pubblicato dalla fonte musicale, non un comportamento
> osservato. In questo progetto non esiste alcun dato che rappresenti una persona: nessuna
> visione, nessun ascolto, nessun abbonamento. Nulla di ciò che si legge in questa pagina
> descrive che cosa il pubblico farebbe.
> ```

**Perché è a schermo e non nel documento**: la parola «domanda» compare nel nome dell'indicatore, cioè in un punto che il lettore incontra prima di qualunque testo. `data_model.md` §18 dichiara che il modello **qualcosa sui pubblici lo dice** — ciò che manca è il livello — e questo blocco è il solo posto in cui quella precisazione raggiunge chi legge la pagina.

---

## 8. Pagina `BQ3` — Impatto stimato

**Spazio**: la fascia sotto la tabella degli scenari, dichiarata dalla `008a` §8 come *«la più alta delle quattro»*. È la fascia più densa **per peso**, non per numero: porta tre assunzioni strutturali, quattro limiti di lettura e un debito di governance.

**Ordine di taglio, se non basta** (`N4`): dal fondo, e **`BL-Q3-9` non si taglia in nessun caso** (`FR-014`). È l'unico blocco dell'intera dashboard che dichiara un debito aperto invece di un limite, ed è ciò che rende il file pubblicabile invece di impedirlo.

---

### `BL-Q3-1` — Perché la confidenza è bassa, e perché gli scenari si leggono insieme

**Obblighi**: `OB-24` · **Requisiti**: `FR-009`, `FR-013`
**Fonte**: principio I — *«Dove la confidenza è bassa, il valore DEVE essere espresso come range»*; `business_case.md` §6; `bq3_scenarios.md` §5

> **Titolo**
>
> ```text
> Perché la confidenza è bassa, e perché gli scenari si leggono insieme
> ```
>
> **Testo**
>
> ```text
> I valori di questa pagina non sono osservati: discendono da ipotesi che i dati di questo
> progetto non permettono di verificare. Per questa ragione sono presentati come intervallo e
> vanno letti insieme.
> ```

**Copre entrambi gli indicatori della pagina**: il tasso di adozione e l'uplift condividono il livello e la ragione, e ripeterla due volte occuperebbe lo spazio dei limiti.

> **Che cosa questa formulazione dichiara in meno.** Resta che gli scenari si leggono insieme; cade **perché**: *un valore singolo comunicherebbe una certezza che il dato non ha*. È la ragione che `business_case.md` §6 dà alla propria regola non negoziabile, e senza di essa la lettura congiunta è prescritta e non motivata. `FR-013` è **indebolito** su `OB-24`, e registrato in §13.1.

---

### `BL-Q3-2` — L'ipotesi di ricavo, senza i suoi numeri

**Obblighi**: `OB-25` · **Requisito**: `FR-013`
**Fonte**: `business_case.md` `A4`

> **Titolo**
>
> ```text
> L'ipotesi sul modello di ricavo
> ```
>
> **Testo**
>
> ```text
> Lo scenario assume un abbonamento a livelli — un livello con il solo video e un livello con
> video e musica — e un differenziale di prezzo fra loro assunto, non osservato. Un prezzo qui
> non è una misura incerta: è una decisione di scenario, e nessuna analisi di elasticità della
> domanda la sostiene.
> ```

**Perché senza i numeri** ([data-model.md](../data-model.md) §5): i prezzi e il differenziale sono valori pubblicati con la propria ancora in `business_case.md` `A4`. In prosa diventerebbero una seconda copia priva di legame con l'artefatto che li produce. Ciò che il lettore deve sapere — che sono decisioni e non misure — è detto per intero senza scriverli.

---

### `BL-Q3-3` — L'ipotesi sulla base di abbonati e sull'orizzonte

**Obblighi**: `OB-26` · **Requisito**: `FR-013`
**Fonte**: `business_case.md` `A5`

> **Titolo**
>
> ```text
> L'ipotesi sulla base di abbonati e sull'orizzonte
> ```
>
> **Testo**
>
> ```text
> La base di abbonati è assunta stabile per tutto l'orizzonte considerato. L'orizzonte è
> quello dichiarato nel business case, oltre il quale la fiducia nelle ipotesi degrada al
> punto da rendere la stima non informativa. Il perimetro è globale: nessuna di queste stime
> riguarda un singolo mercato nazionale.
> ```

---

### `BL-Q3-4` — Da dove viene il valore centrale

**Obblighi**: `OB-27` · **Requisito**: `FR-013`
**Fonte**: constitution, *Vincoli di Dominio e di Dato*, condizione 4; `business_case.md` `A6`; `bq3_scenarios.md` §3

> **Titolo**
>
> ```text
> Da dove viene il valore centrale
> ```
>
> **Testo**
>
> ```text
> Non è osservato su StreamWave. Viene da un benchmark pubblico: un valore osservato e
> pubblicato da terzi su un operatore che non è StreamWave. La fonte è citabile, e il valore
> verificabile: ciò non innalza la confidenza.
> ```

> **Che cosa questa formulazione dichiara in meno, ed è il caso più delicato del contratto.** Resta la provenienza — un operatore terzo — e resta che l'ancoraggio non innalza la confidenza. Cadono due cose:
>
> - che assumere quel valore per StreamWave sia **un'ipotesi di trasferimento**. `A6` prescrive che vada *«dichiarata accanto al valore ogni volta che il valore compare»*, e il *«non è osservato su StreamWave»* dell'attacco la implica senza nominarla;
> - che *verificabile* e *vero per StreamWave* siano **proprietà diverse, e che la seconda non discenda dalla prima**. Il testo accosta ora la citabilità della fonte alla confidenza che non sale, e lascia al lettore il passaggio che le separa.
>
> `FR-013` è **indebolito** su `OB-27`. È il caso più delicato perché la fonte dell'obbligo non è un documento del progetto ma la constitution, *Vincoli di Dominio e di Dato*, condizione 4 — ed è anche il blocco che regge `BL-Q3-9`, che dello stesso benchmark dichiara il debito. Registrato in §13.1.

---

### `BL-Q3-5` — L'intervallo non è un intervallo di confidenza

**Obblighi**: `OB-28` · **Requisito**: `FR-013`
**Fonte**: `bq3_scenarios.md` §8

> **Titolo**
>
> ```text
> Questo intervallo non è un intervallo di confidenza
> ```
>
> **Testo**
>
> ```text
> La sua ampiezza non ha alcuna interpretazione probabilistica. Chiedere con quale
> probabilità il valore vero cada dentro la banda è una domanda a cui questi numeri non
> rispondono.
> ```

---

### `BL-Q3-6` — Che grandezza è l'uplift

**Obblighi**: `OB-29` · **Requisito**: `FR-013`
**Fonte**: `bq3_scenarios.md` §8, *«Quale grandezza temporale sia il tasso, dichiarata una volta per tutte»* e *«L'uplift non è un ricavo cumulato»*

> **Titolo**
>
> ```text
> Che grandezza è questo valore
> ```
>
> **Testo**
>
> ```text
> È un livello mensile, raggiunto a fine orizzonte e poi mantenuto. Non è un totale cumulato
> sul periodo e non è un dato annuo: nei primi mesi sarebbe minore.
> ```

---

### `BL-Q3-7` — Il tasso è lordo di disdette

**Obblighi**: `OB-30` · **Requisito**: `FR-013`
**Fonte**: `bq3_scenarios.md` §8, *«Le disdette sono escluse»*; `business_case.md` `A5`

> **Titolo**
>
> ```text
> Il tasso è al lordo delle disdette
> ```
>
> **Testo**
>
> ```text
> È calcolato su una base assunta costante, senza sottrarre chi abbandona. È una scelta di
> perimetro dichiarata, non una proprietà del mercato.
> ```

---

### `BL-Q3-8` — Perché qui non c'è un totale di ricavo

**Obblighi**: `OB-31` · **Requisiti**: `FR-013`, `FR-003`
**Fonte**: `bq3_scenarios.md` §8, che dichiara **falsa alla lettera** la formulazione esclusa
**Formulazione esclusa**: «l'uplift non è scalabile», e ogni variante che presenti come impossibile un'operazione che è soltanto non fornita

> **Titolo**
>
> ```text
> Perché qui non c'è un totale di ricavo
> ```
>
> **Testo**
>
> ```text
> Questo valore è per utente al mese, e questo progetto non quantifica alcuna base di
> abbonati: la dashboard non fornisce quindi la chiave per passare all'aggregato. Chiunque
> disponga di una stima di abbonati può moltiplicare, ma il totale sarebbe un numero che
> nessuno ha misurato.
> ```

**Perché la formulazione comoda è vietata e non solo sconsigliata**: `bq3_scenarios.md` §8 dichiara che *«la versione più comoda — "non è scalabile" — direbbe una cosa falsa»*, e prosegue: non è un presidio, è una rinuncia, e non impedisce a valle l'operazione che scoraggia. Questo blocco dice che l'operazione è possibile e che cosa produrrebbe, che è l'unica cosa vera dicibile qui.

---

### `BL-Q3-9` — Il debito aperto sulla verificabilità del benchmark

**Obblighi**: `OB-32` · **Requisito**: `FR-014`
**Fonte**: `bq3_scenarios.md` §9; debito della `004` registrato in `docs/roadmap.md`; contratto di dashboard `008a`, punto 6
**Non tagliabile in nessun caso**

> **Titolo**
>
> ```text
> Un debito aperto
> ```
>
> **Testo**
>
> ```text
> Il valore centrale poggia su un comunicato pubblicato da un terzo, che non nomina lo studio
> da cui la cifra proviene: se ne constata che un comunicato la riporta, non che sia stata
> misurata in un modo che si possa giudicare.
> ```

**Perché non si taglia**: è il blocco che la consegna nomina esplicitamente — *il debito della `004` resta aperto e dichiarato, non risolto: `BQ3` va a schermo con quella provenienza e la narrazione lo dice invece di nasconderlo.* Un file che espone una stima poggiata su un benchmark non verificabile senza dirlo non è meno pubblicabile: è pubblicabile a un prezzo che qualcun altro paga.

> **Che cosa questa formulazione dichiara in meno.** Che il debito sia **aperto** è ora affidato al solo titolo, ed è sufficiente. Della ragione resta la metà più forte — il comunicato non nomina lo studio, quindi la cifra non è giudicabile. Cade la metà che riguarda la **fragilità nel tempo**: che il valore sia congelato in un file del progetto, che del comunicato non esista copia archiviata né identificativo permanente, e che la verifica esterna dipenda da un indirizzo che potrebbe smettere di rispondere.
>
> `FR-014` elenca quella fragilità per esteso fra ciò che la pagina deve dichiarare, quindi è **indebolito**. La conseguenza pratica è che il blocco dice perché il benchmark non è giudicabile **oggi**, e non più che potrebbe non essere nemmeno consultabile domani. Registrato in §13.1.

---

# Parte III — Che cosa questa feature può e non può toccare nel file

Il contratto della `008a` chiude la struttura. Questa parte dichiara il confine fra ciò che resta legittimo e ciò che, se necessario, è un **ritrovamento da dichiarare** e non una libertà di chi costruisce.

## 9. Le rifiniture ammesse

Una rifinitura è una modifica che **non cambia che cosa una visuale calcola né quali dati mostra**:

- il titolo di una visuale o di una pagina;
- l'allineamento, la spaziatura, la posizione di un elemento **dentro** il proprio spazio;
- il colore, purché resti leggibile e non codifichi un'informazione nuova;
- l'etichetta di un asse;
- un formato numerico **già dichiarato** dal contratto di pagina della `008a` §1.2 — non un formato nuovo, che cambierebbe come un valore si legge senza cambiarne il valore.

Le rifiniture sono l'unica parte di questa feature che nessun obbligo richiede. Se il tempo stringe, **cedono per prime**.

## 10. I divieti

| Divieto | Requisito | Perché |
|---|---|---|
| **nessuna pagina-tooltip** | `FR-023`, `N3` | è una **pagina**, quindi sarebbe la quinta in un report chiuso a quattro, e ospita visuali, quindi può calcolare a una grana qualunque — vietato già dalla `008a` §3.1 in termini di misure |
| **nessun segnalibro, nessun pannello a scomparsa, nessun pulsante che scopra o nasconda un blocco** | `FR-023`, `N3` | un limite raggiungibile con un clic si legge solo se qualcuno sospetta che esista. È l'argomento con cui la `008a` §5.4 vieta di rendere nascondibile la colonna della quota di zeri |
| **nessuna visuale legata a un campo, nessun filtro, nessuno slicer, nessuna interazione incrociata** | `FR-024` | questa feature aggiunge caselle di testo e forme. Ogni altra cosa cambia che cosa la pagina calcola |
| **nessuna modifica a una misura, a una relazione, a una colonna del modello, né al numero di pagine** | `FR-024` | il modello è chiuso dalla `008a`; una modifica necessaria è un ritrovamento da dichiarare |
| **su qualunque visuale di segmenti si usa `segment_display`, mai `segment`** | `FR-025` | è la colonna che porta l'avvertimento dentro il nome. Con `segment` l'avvertimento sparisce dalla graduatoria, e `BL-Q2-2` resta a parlare di una marcatura che il lettore non vede più (contratto di dashboard `008a`, punto 11) |
| **nessuna pagina che espone la sovrapposizione dei profili acquisisce un filtro di categoria video** | `FR-026` | l'issue `#18` è aperta: la formula di `mood_profile_overlap` è priva dell'`ALL` sul filtro di categoria, e il difetto si manifesterebbe. Non si può presupporre che la misura regga il filtro solo perché nessuna pagina attuale lo offre |

**Il tooltip statico d'intestazione resta ammesso** per una funzione sola: chiarire un termine tecnico già a schermo, dove la fascia porta già il limite e il tooltip porta la definizione. **Non è un posto in cui un limite possa abitare**, e nessun blocco di questo contratto vi va a stare.

**Una precisazione sul confine.** I divieti su `segment_display` e sul filtro di categoria sono, alla lettera, già impliciti in `FR-024`: una feature che non aggiunge alcuna visuale legata a un campo non può nemmeno sbagliare campo. Restano dichiarati come vincoli autonomi perché sopravvivano a `FR-024` — se una rifinitura futura riaprisse quella porta, questi due divieti dicono che cosa non va fatto entrando.

## 11. Prima di ogni altra cosa nel file

All'apertura del `.pbix`, **prima che venga scritto un solo blocco**, vanno verificate le tre impostazioni dell'issue `#20` (`FR-027`, `T010`): il dominio dei valori di mood su `dim_track`, il conteggio di riga di `dim_title`, la presenza della colonna di scenario su `bq3_scenarios`.

Se una è persa, la narrazione si ferma, la correzione precede, e se tocca un valore a schermo gli otto valori vanno riconfrontati con `docs/kpi_measures.md` (`FR-028`). **È il costo di una lettura contro il costo di scrivere «questo valore misura X» sotto un numero che non misura più X.**

---

# Parte IV — La verifica di questo contratto

## 12. L'esaustività, verificata in entrambe le direzioni

Eseguita su questo documento contro l'inventario di [data-model.md](../data-model.md) §3, prima della proposta di approvazione (`T008`).

**Da obbligo a blocco** — ogni `OB` ha almeno un blocco:

| Obblighi | Blocco |
|---|---|
| `OB-01` · `OB-02` · `OB-03` · `OB-04` | `BL-IN-1` · `BL-IN-2` · `BL-IN-3` · `BL-IN-4` |
| `OB-05` · `OB-35` | `BL-Q1-1` · `BL-Q1-1b` |
| `OB-06` · `OB-07` · `OB-08` | `BL-Q1-2` · `BL-Q1-3` · `BL-Q1-4` |
| `OB-09` · `OB-10` · `OB-11` · `OB-12` | `BL-Q1-5` · `BL-Q1-6` · `BL-Q1-7` · `BL-Q1-8` |
| `OB-13` | `BL-Q2-1` |
| `OB-14` · `OB-15` | `BL-Q2-2` |
| `OB-16` · `OB-17` · `OB-18` · `OB-19` | `BL-Q2-3` · `BL-Q2-4` · `BL-Q2-5` · `BL-Q2-6` |
| `OB-20` · `OB-21` | `BL-Q2-7` |
| `OB-22` · `OB-23` · `OB-33` | `BL-Q2-8` · `BL-Q2-9` · `BL-Q2-10` |
| `OB-24` … `OB-32` | `BL-Q3-1` … `BL-Q3-9`, nell'ordine |
| `OB-34` | nessun blocco proprio: è soddisfatto dagli scioglimenti dentro `BL-Q1-3` e `BL-Q2-8`, che sono gli unici blocchi a usare una sigla |

**Da blocco a obbligo** — ogni blocco serve almeno un `OB`: verificato riga per riga sulla stessa tabella. **Nessun blocco di questo contratto è privo di obbligo**, con l'unica eccezione dichiarata in §14, che è proposta e non scritta.

## 13. I vincoli della Parte I, verificati sui blocchi

| Vincolo | Esito |
|---|---|
| nessuna cifra fuori dalla lista chiusa (§1) | **rispettato**. `2021` e `2022` compaiono solo in `BL-IN-4`; nessun altro blocco porta una cifra |
| nessun numerale in lettere, in alcuna posizione (§1.1) | **rispettato**. Dove il testo dovrebbe contare, enumera o rimanda alla marcatura: `BL-IN-3` enumera i livelli, `BL-Q2-2` rimanda all'avvertimento, `BL-Q1-5` rimanda alla quota a schermo |
| i due anni distinti per statuto (`FR-018`) | **indebolito** — vedi §13.1 |
| nessuna composizione della regola di decisione (§3) | **rispettato**. `C1` in `BL-Q1-3`, `C3` in `BL-Q2-8`, nessun conteggio, nessuna menzione di `C2`, nessun esito complessivo |
| nessuna conclusione, raccomandazione o previsione (§2) | **rispettato**. Ogni blocco sta in uno dei tre registri ammessi |
| nessun lessico causale | **rispettato** |
| nessun superlativo o ordinale riferito a un fatto misurato | **rispettato**, con l'eccezione dichiarata e argomentata in `BL-Q1-7`, dove i superlativi non nominano alcuna categoria né pubblicano alcun valore |
| nessuna affermazione sul pubblico | **rispettato**, e `BL-Q2-10` esiste per dichiararlo al lettore |
| ogni sigla sciolta sulla stessa pagina (`OB-34`) | **rispettato**. Le uniche sigle a schermo sono `C1` e `C3`, e ciascuna è sciolta nel blocco che la introduce |

### 13.1 Gli obblighi che il testo approvato soddisfa in parte

I testi di questo contratto sono stati accorciati in revisione, e l'accorciamento ha un prezzo su tre obblighi. **Nessuno dei tre blocchi afferma il falso**: ciascuno dice meno di ciò che il proprio obbligo prescrive.

Sono elencati qui e non nascosti dentro il commento del blocco perché la distinzione fra *risolto* e *indebolito* è una regola di questo progetto, e vale per gli obblighi esattamente come per i rilievi di revisione: se un indebolimento non è dichiarato, chi legge non può distinguere un obbligo soddisfatto da una pretesa ritirata.

| Obbligo | Blocco | Che cosa è a schermo | Che cosa non lo è più |
|---|---|---|---|
| `OB-04` (`FR-018`) | `BL-IN-4` | la distinzione fra anno osservato e anno dichiarato dalla fonte, portata dal verbo | che l'anno musicale sia **non verificabile**, e la ragione: il catalogo musicale non porta alcun campo di data |
| `OB-11` (`FR-010`) | `BL-Q1-7` | che la sovrapposizione sia una stima per eccesso, con il meccanismo geometrico che la produce | che la sovrapposizione reale sia **minore o uguale** a quella mostrata, e che **quanto minore il progetto non lo misuri** |
| `OB-12` (`FR-009`) | `BL-Q1-8` | che gli intervalli siano ampi e che l'ampiezza venga dal criterio e non dal catalogo | che sia **la ragione principale per cui la confidenza resta media**, e il passaggio che lo rendeva leggibile — un intervallo ampio è facile da coprire |
| `OB-15` (`FR-012`) | `BL-Q2-2` | che la posizione in fondo alla graduatoria misuri l'assenza di segnale e non una priorità bassa | che quei segmenti **vadano esclusi da qualunque lettura della coda** — la prescrizione testuale di `kpi_measures.md` §7.4 |
| `OB-19` (`FR-010`) | `BL-Q2-6` | che punteggio e quadrante rispondano a domande diverse, ciascuna con la propria | il caso concreto che le rende non intercambiabili: **punteggio alto e fuori dal quadrante** |
| `OB-20` (`FR-011`) | `BL-Q2-7` | che le quantità per segmento non si sommino, perché i segmenti si sovrappongono | che **la graduatoria non sia un elenco di alternative che si escludono a vicenda** |
| `OB-24` (`FR-013`) | `BL-Q3-1` | che gli scenari siano presentati come intervallo e vadano letti insieme | **perché**: che un valore singolo comunicherebbe una certezza che il dato non ha |
| `OB-27` (`FR-013`) | `BL-Q3-4` | che il valore venga da un operatore terzo e che l'ancoraggio non innalzi la confidenza | che sia **un'ipotesi di trasferimento**, e che *verificabile* e *vero per StreamWave* siano proprietà diverse |
| `OB-32` (`FR-014`) | `BL-Q3-9` | che il debito sia aperto (dal titolo), e che il comunicato non nomini lo studio | la **fragilità nel tempo**: nessuna copia archiviata, nessun identificativo permanente, la verifica esterna appesa a un indirizzo |

**I due più onerosi fra gli obblighi tecnici sono `OB-11` e `OB-19`**, perché sono limiti che `kpi_operators.md` §12 assegna **per nome** a questa feature — su tre assegnati, due sono stati accorciati. Il terzo, `OB-17`, resta intero.

**Il più delicato in assoluto è `OB-27`**, perché la sua fonte non è un documento del progetto ma la constitution, *Vincoli di Dominio e di Dato*, condizione 4, ripresa da `A6` con la parola *«ogni volta che il valore compare»*.

**Una regolarità che vale la pena nominare**, perché non è un caso e chi legge questa tabella la vedrà da sé: in otto casi su nove ciò che cade è **la seconda metà del blocco** — quella che dice al lettore che cosa non fare con il numero, o perché la prima metà sia vera. È la parte più lunga, la più prescrittiva, e la prima a sembrare superflua a chi il dato lo conosce già.

**Che cosa questo comporta per la dichiarazione di pubblicabilità.** La condizione 3 di `N8` chiede che i limiti assegnati esplicitamente a questa feature siano a schermo **in forma leggibile da un non tecnico**. Dopo questi accorciamenti la condizione è verificabile solo insieme a questa tabella: sono tutti a schermo, non tutti per intero. Il contratto di pubblicabilità del blocco D dovrà dirlo così, o dichiarerebbe una condizione soddisfatta al posto di una soddisfatta in parte.

**Che cosa questo comporta per la revisione in contesto pulito.** Sono tre punti su cui il revisore va lasciato libero di arrivare per conto proprio: se li trova senza aver letto questa tabella, l'indebolimento è visibile a chi legge lo schermo, e la decisione va rivista. Se non li trova, la brevità ha comprato più di quanto è costata.

## 14. Le due decisioni prese al punto di fermata

**`OB-35` è adottato.** La glossa sul numeratore della metrica di riferimento va a schermo come `BL-Q1-1b`, e l'obbligo entra nell'inventario di [data-model.md](../data-model.md) §3.2 con la propria fonte. Il testo approvato è più corto di quello proposto: la chiusa *«e questo progetto non ha modo di accorgersene»* è caduta. Il blocco dice che cosa il conteggio legge e che cosa resta fuori, e non aggiunge la dichiarazione di cecità — che è vera, sta nella nota in loco della `007b`, e a schermo aggiungeva una frase senza cambiare che cosa il lettore deve fare con il numero.

**Il ritrovamento sul contratto di pagina della `008a` non riceve una nota in loco.** Il contratto della `008a` §8 descrive la fascia di `BQ3` includendo *«la non scalabilità dell'uplift»*, che è la formulazione dichiarata falsa alla lettera da `bq3_scenarios.md` §8 e che questo contratto esclude (§4, riga 3). Il documento della `008a` **non è toccato**: la regola di correzione in loco di `CLAUDE.md` nasce per gli artefatti pubblicati, e quello è un contratto di disegno di una feature chiusa. Il ritrovamento è registrato sul tracker come issue `#26`, e resta contestabile lì.

---

## 16. Come si verifica che questo contratto sia stato rispettato

Non da uno script. `scripts/check_audit_coherence.py` non legge i file sotto `specs/` e non entra in alcun caso in un `.pbix`: **il deliverable di questa feature è la sola cosa del repository che nessun controllo automatico può leggere, per costruzione.**

Si verifica con le prove 4-11 di [quickstart.md](../quickstart.md), tutte manuali, tutte di lettura, e con la revisione in contesto pulito che riceverà questo documento insieme alla sezione di esito. Il metro di quella revisione non è la conformità agli obblighi — che le prove coprono — ma la **leggibilità per il destinatario dichiarato in apertura**.
