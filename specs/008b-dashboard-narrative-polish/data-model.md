# L'inventario degli obblighi, e dove ciascuno atterra a schermo

**Feature**: 008b-dashboard-narrative-polish | **Data**: 2026-08-27

## 1. Che cosa è questo documento, e che cosa non è

La Fase 1 di `/speckit.plan` produce normalmente il modello dei dati della feature. Questa feature **non tocca il modello**: le tabelle restano otto, le relazioni cinque, le misure quattordici, e nessuna colonna cambia. Il modello autorevole resta [`docs/data_model.md`](../../docs/data_model.md) per il disegno e la sezione «Esito della costruzione» di [`../008a-dashboard-model-pages/quickstart.md`](../008a-dashboard-model-pages/quickstart.md) per ciò che esiste.

Al suo posto, questo documento porta ciò che questa feature ha davvero bisogno di strutturare: **l'inventario degli obblighi** che la narrazione deve soddisfare, ciascuno con la fonte che lo impone e la pagina in cui atterra.

**A che cosa serve, operativamente.** Il contratto di narrazione contiene testo; il testo non si conta e non si verifica per esaustività leggendolo. Questo inventario è la lista contro cui il contratto si controlla: **ogni obbligo deve avere almeno un blocco, e ogni blocco deve servire almeno un obbligo.** Un obbligo senza blocco è una dimenticanza; un blocco senza obbligo è testo che qualcuno ha voluto scrivere, che in una feature governata dal principio IV è una categoria diversa e va giustificata.

**Che cosa questo documento non contiene**: il testo. Il testo è del contratto, ed è l'oggetto del terzo punto di fermata.

## 2. Le quattro fasce, e la loro capienza dichiarata

Gli spazi sono quelli riservati dal contratto di pagina della `008a` §8. Nessuno di essi è stato dimensionato sapendo quanto testo avrebbe ospitato — la `008a` ha riservato lo spazio, non lo ha misurato — e la colonna di destra è quindi una **previsione di carico**, non una capienza verificata.

| Pagina | Spazio riservato | Obblighi che vi atterrano | Carico |
|---|---|---|---|
| **Ingresso** | una fascia a piena larghezza sotto la scheda della North Star, più una striscia a piè di pagina | `OB-01`-`OB-04` | quattro obblighi, di cui due brevi. La striscia a piè di pagina è la destinazione naturale della copertura temporale |
| **`BQ1`** | una fascia sotto la fila delle tre schede, con tre aree allineate alle schede | `OB-05`-`OB-12` | otto obblighi su tre aree, cioè da due a tre per area. È la fascia meglio proporzionata delle quattro |
| **`BQ2`** | una fascia sotto la graduatoria | `OB-13`-`OB-23`, `OB-33` | dodici obblighi in una fascia sola, la più carica per numero. Quattro di essi (`OB-20`, `OB-21`, `OB-23`, `OB-33`) riguardano la pagina e non un singolo KPI, e si possono raggruppare |
| **`BQ3`** | una fascia sotto la tabella degli scenari, «la più alta delle quattro» | `OB-24`-`OB-32` | nove obblighi, di cui tre assunzioni strutturali e un debito di governance. È la fascia dichiarata più alta ed è anche la più densa per **peso**, non per numero |

`OB-34` è trasversale e non consuma spazio proprio: vincola la forma di ogni blocco su ogni pagina.

**Dove si concentra il rischio dichiarato da `N4`.** Su `BQ2` per numero e su `BQ3` per peso. Se una fascia non basta, la reazione è tagliare il testo e dichiarare il taglio, mai allargare la fascia — e questa tabella esiste perché quel taglio si decida sapendo che cosa si sta togliendo.

## 3. L'inventario

Colonne: l'identificativo dell'obbligo, che cosa impone, la **fonte** che lo impone — un principio della constitution, una sezione di documento pubblicato, o una issue — la pagina di atterraggio, e il requisito della spec che lo formalizza.

### 3.1 Pagina di ingresso

| ID | Che cosa impone | Fonte | Requisito |
|---|---|---|---|
| `OB-01` | i due cataloghi sono di riferimento e non di StreamWave; nessun valore della dashboard descrive StreamWave | constitution, Vincoli di Dominio e di Dato («DEVE essere dichiarata in ogni artefatto rivolto all'utente finale»); `business_case.md` `A1` | `FR-006` |
| `OB-02` | che cosa la dashboard non risponde: la decisione di entrare, il lato costi, il comportamento degli utenti | principio IV; `business_case.md` §8; `A3` | `FR-007` |
| `OB-03` | la scala di confidenza a tre livelli, e che essa **non** misura la trasferibilità a StreamWave | principio I; `business_case.md` §6 e «Cosa questa scala non misura» | `FR-008` |
| `OB-04` | la copertura temporale dei due cataloghi, con i due statuti distinti | principio IV; `business_case.md` `A2`; `data_model.md` §18 | `FR-007`, `FR-018` |

### 3.2 Pagina `BQ1` — Posizionamento

| ID | Che cosa impone | Fonte | Requisito |
|---|---|---|---|
| `OB-05` | perché `BQ1-K1` è a confidenza alta: si conta quanto del catalogo di riferimento è già musicale, senza mappature interposte | contratto di dashboard `008a` punto 2; `business_case.md` §6 | `FR-009` |
| `OB-06` | la quota **non** dice se `C1` è soddisfatta: sono due letture diverse dello stesso catalogo | `kpi_measures.md` §2.3 | `FR-009` |
| `OB-07` | `C1` è una condizione della regola di decisione del business case, e da sola non decide; la dashboard non pubblica alcun esito complessivo | `008a` `F6`; contratto di dashboard `008a` punto 3; issue `#17` | `FR-019` |
| `OB-08` | perché `BQ1-K2` è a confidenza alta: due durate osservate e una sottrazione | contratto di dashboard `008a` punto 2 | `FR-009` |
| `OB-09` | il confronto è asimmetrico — il lato video sono i soli film, il lato musicale il catalogo intero — e la quota di film accanto al valore dice quanto; la lettura «catalogo video contro catalogo musicale» è **esclusa** | `data_model.md` §18 (categoria *di dominio*) e §19; `kpi_measures.md` §3.4 | `FR-011`, `FR-003` |
| `OB-10` | perché `BQ1-K3` è a confidenza media: dipende dalla tabella dei profili di mood, che l'analista assegna e nessuna fonte osserva | `kpi_operators.md` §11; `data_model.md` §15 | `FR-009` |
| `OB-11` | la sovrapposizione pubblicata è una **stima per eccesso**: la sovrapposizione reale è minore o uguale, e quanto minore il progetto non lo misura | `kpi_operators.md` §4 e §12 (assegnato per nome a questa feature); `kpi_measures.md` §4.3 | `FR-010` |
| `OB-12` | gli intervalli di mood sono ampi per costruzione del criterio di assegnazione, ed è la ragione principale per cui la confidenza resta media | `kpi_measures.md` §4.3 | `FR-009`, `FR-010` |

### 3.3 Pagina `BQ2` — Segmento di ingresso

| ID | Che cosa impone | Fonte | Requisito |
|---|---|---|---|
| `OB-13` | perché `BQ2-K1` è a confidenza media: è un indice di popolarità pubblicato dalla fonte, che non ne dichiara la costruzione, usato come proxy della domanda | `business_case.md` §6; `kpi_operators.md` §11 | `FR-009` |
| `OB-14` | i segmenti marcati portano domanda **non misurata dalla fonte**, non domanda bassa; «domanda bassa» è la formulazione **esclusa** | `kpi_operators.md` §5.1 (`D7`); `kpi_measures.md` §5.3 | `FR-012`, `FR-003` |
| `OB-15` | i segmenti marcati vanno esclusi da qualunque lettura della coda della graduatoria: la loro posizione misura la copertura del dato, non una priorità | `kpi_measures.md` §7.4 | `FR-012` |
| `OB-16` | perché `BQ2-K2` è a confidenza media: confronta un profilo osservato con uno assegnato, su una scala ancorata solo agli estremi | `content_taxonomy_bridge.md` §7; `kpi_operators.md` §11 | `FR-009` |
| `OB-17` | la grandezza assoluta dell'affinità non ha interpretazione indipendente: confronta i segmenti fra loro, non in assoluto | `kpi_operators.md` §6 e §12 (assegnato per nome); `kpi_measures.md` §6.3 | `FR-010` |
| `OB-18` | perché `BQ2-K3` è a confidenza media: eredita il livello dei due valori che compone | `kpi_operators.md` §7 e §11 | `FR-009` |
| `OB-19` | punteggio e quadrante rispondono a domande diverse e non si fondono: un segmento può avere punteggio alto e restare fuori dal quadrante | `kpi_operators.md` §7.2 e §12 (assegnato per nome) | `FR-010` |
| `OB-20` | i segmenti si sovrappongono: le quantità per segmento non si sommano, e la graduatoria non è una partizione del catalogo | `data_model.md` §18 (categoria *sconsigliato*) e §19 | `FR-011` |
| `OB-21` | contare le righe di un segmento misura il campionamento e non il mercato, e non lo dimensiona | `data_model.md` §18 (categoria *sconsigliato*) e §19; `kpi_measures.md` §5.4 | `FR-011` |
| `OB-22` | `C3` è una condizione della regola di decisione, e da sola non decide; la dashboard non pubblica alcun esito complessivo | `008a` `F6`; contratto di dashboard `008a` punto 3 | `FR-019` |
| `OB-23` | dispersione e graduatoria non si filtrano a vicenda, e la graduatoria mostra sempre tutti i segmenti | `008a`, scostamento T028; issue `#21` | `FR-015` |
| `OB-33` | il modello non contiene alcuna entità che rappresenti una persona: «domanda» nomina un indice della fonte, non un comportamento osservato | `data_model.md` §18 (categoria *di dominio*); `business_case.md` `A3` | `FR-011`, `FR-020` |

### 3.4 Pagina `BQ3` — Impatto stimato

| ID | Che cosa impone | Fonte | Requisito |
|---|---|---|---|
| `OB-24` | perché entrambi i KPI sono a confidenza bassa, e perché i tre scenari si leggono insieme: un valore singolo comunicherebbe una certezza che il dato non ha | principio I («Dove la confidenza è bassa, il valore DEVE essere espresso come range»); `business_case.md` §6; `bq3_scenarios.md` §5 | `FR-009`, `FR-013` |
| `OB-25` | il modello di ricavo assunto è a due tier, con un differenziale di prezzo dichiarato e non osservato | `business_case.md` `A4` | `FR-013` |
| `OB-26` | la base utenti è assunta stabile, l'orizzonte è dichiarato, il perimetro è globale | `business_case.md` `A5` | `FR-013` |
| `OB-27` | il parametro centrale viene da un benchmark osservato su un operatore terzo: è un'**assunzione di trasferimento**, e l'ancoraggio non innalza la confidenza | constitution, Vincoli di Dominio e di Dato, condizione 4; `business_case.md` `A6`; `bq3_scenarios.md` §3 | `FR-013` |
| `OB-28` | l'intervallo **non** è un intervallo di confidenza: l'ampiezza non ha interpretazione probabilistica | `bq3_scenarios.md` §8 | `FR-013` |
| `OB-29` | l'uplift è un livello mensile a fine orizzonte e mantenuto: non un cumulato, non un dato annuo | `bq3_scenarios.md` §8 | `FR-013` |
| `OB-30` | il tasso è lordo di disdette, su base assunta costante | `bq3_scenarios.md` §8; `business_case.md` `A5` | `FR-013` |
| `OB-31` | nessuna base utenti è quantificata in questo progetto e la dashboard non fornisce il moltiplicatore; «non è scalabile» è la formulazione **esclusa**, perché è falsa | `bq3_scenarios.md` §8, che dichiara falsa quella formulazione alla lettera | `FR-013`, `FR-003` |
| `OB-32` | il debito sulla verificabilità del benchmark è **aperto**: la fonte è un comunicato di un terzo che non nomina lo studio, congelato nel repository, e la verifica esterna dipende da un indirizzo che potrebbe smettere di rispondere | `bq3_scenarios.md` §9; debito della `004` in `docs/roadmap.md`; contratto di dashboard `008a` punto 6 | `FR-014` |

### 3.5 Obbligo trasversale

| ID | Che cosa impone | Fonte | Requisito |
|---|---|---|---|
| `OB-34` | ogni sigla usata dal testo di questa feature è sciolta sulla stessa pagina in cui compare | criterio di accettazione della constitution (reggere la presentazione a un board reale); la famiglia di difetti delle issue `#16` e `#24`, che questa feature **non** chiude | `FR-021` |

## 4. Le entità che questa feature manipola

- **Blocco di narrazione** — un'unità di testo a schermo. Attributi: pagina, spazio riservato, testo letterale, obblighi serviti, fonti, formulazione esclusa dove esiste. È l'unica entità che questa feature crea.
- **Spazio riservato** — una delle quattro fasce della `008a` §8. Attributi: pagina, posizione, obblighi che vi atterrano. **Non è modificabile**: è il contenitore, e `N4` dichiara che cosa fare se non basta.
- **Formulazione esclusa** — una frase vicina a quella corretta e sbagliata, dichiarata perché chi costruisce non la scelga per comodità. Tre sono obbligatorie (`FR-003`) e vivono su `OB-09`, `OB-14`, `OB-31`.
- **Voce della lista chiusa** — una cifra ammessa in un blocco, con la propria fonte e la ragione per cui non proviene da una misura. Il contratto ne fissa l'elenco definitivo.

**Nessuna entità del modello dati compare in questo elenco**, ed è la conferma del perimetro: questa feature non ha entità di dato.

## 5. La lista chiusa dei numerali, in forma preliminare

Il contratto la fissa; questa sezione dichiara che cosa la spec vi ammette e che cosa no, perché il contratto non la allarghi in silenzio.

| Voce | Perché non può venire da una misura | Fonte |
|---|---|---|
| anno di copertura del catalogo video | il modello non ha dimensione di calendario, quindi nessuna misura può produrlo; è però un fatto **osservato** e ancorato | `data_model.md` §16 e §18; `business_case.md` `A2` |
| anno di copertura del catalogo musicale | come sopra per l'assenza di calendario, ma **non** è un fatto osservato: il catalogo musicale non espone alcun campo di data, e l'anno è preso dalla documentazione della fonte | `data_model.md` §18, che lo dichiara non verificabile; `business_case.md` `A2` |

**Nient'altro.** In particolare **non** sono ammessi in prosa: la quota di titoli film, il conteggio dei segmenti marcati, il conteggio dei segmenti totali, il conteggio dei membri del quadrante, i prezzi dei due tier, il differenziale di prezzo, la durata dell'orizzonte, il valore del benchmark. I primi quattro sono misure o colonne già a schermo, e la narrazione vi rimanda invece di ripeterli; gli ultimi quattro sono valori pubblicati con la propria ancora, che in prosa diventerebbero una seconda copia priva di legame con l'artefatto che li produce.

**La conseguenza sulla formulazione, dichiarata qui perché il contratto non la scopra scrivendo**: le assunzioni `A4`, `A5` e `A6` si dicono **senza i propri numeri**. «Un modello a due livelli di abbonamento, con un differenziale di prezzo assunto e non osservato» dice al lettore ciò che deve sapere — che il numero è una decisione di scenario e non una misura — e non introduce una cifra senza fonte. Il numero, per chi lo vuole, sta nell'artefatto.

## 6. Che cosa resta comunque fuori dallo schermo

Elencato qui perché la selezione sia visibile come decisione e non come dimenticanza. Sono limiti **del metodo**, non del valore: cambiano il giudizio su come un numero è stato costruito, non la lettura del numero stesso.

| Limite | Dove vive | Perché resta fuori |
|---|---|---|
| la convenzione di arrotondamento per unità di misura | `kpi_measures.md` §1.2 | riguarda la presentazione di ogni cifra, non la lettura di alcun valore; chi la deve giudicare apre il documento |
| il contratto di versione sulla tabella dei mood | `content_taxonomy_bridge.md` §5 | vincola chi **ricalcolerà** un valore, non chi lo legge |
| il prodotto cartesiano scelto contro l'inviluppo convesso | `kpi_operators.md` §4 | la sua conseguenza per il lettore è `OB-11`, che è a schermo. La scelta geometrica che la produce non lo è |
| la compensatività della distanza media assoluta | `kpi_operators.md` §6 | come sopra: la conseguenza è `OB-17`, che è a schermo |
| le righe a durata degenere nella mediana di `BQ1-K2` (`D11`) | `kpi_measures.md` §3.3 | entrambe le varianti sono pubblicate e la loro differenza è dichiarata; nessuna lettura a schermo cambia a seconda di quale si adotti |

**La regola che ha guidato la selezione**: va a schermo il limite che cambia **come si legge un numero visibile**; resta nel documento il limite che cambia **come si giudica il metodo con cui quel numero è stato costruito**. Chi deve fare la seconda cosa apre il documento, e questa dashboard gli dice dove.
