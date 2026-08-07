# Business Case — Ingresso di StreamWave nel music streaming

> **Cosa è questo documento**: la definizione di *come* valuteremo l'opportunità, non la valutazione. Non contiene risultati, stime calcolate né una raccomandazione sull'espansione. Definisce le domande, le misure con cui rispondere e il grado di fiducia che ciascuna misura potrà sostenere.

## 1. Inquadramento

**StreamWave** è una piattaforma di streaming di intrattenimento video. Il catalogo copre film e serie, distribuiti su un'ampia gamma di generi e mercati.

**La decisione in valutazione**: se aprire un secondo verticale, lo **streaming musicale**, accanto a quello video esistente.

**Il destinatario**: il board di StreamWave. Il documento presuppone competenza di business, non competenza tecnica o statistica. Ogni misura è definita in modo che un membro del board possa contestarla senza sapere come verrà calcolata.

**Perché serve un framework prima dei numeri**: la domanda "conviene entrare nel music streaming?" non è misurabile così com'è. Questo documento la scompone in tre domande che lo sono, associa a ciascuna le misure che le rispondono, e dichiara in anticipo quanta fiducia ciascuna misura potrà reggere. Definire il metro prima di misurare è ciò che impedisce di scegliere, a risultati noti, la misura che dà la risposta desiderata.

## 2. Assunzioni strutturali

Le assunzioni sono ipotesi dichiarate, non fatti osservati. Tutte quelle che seguono sono marcate come tali e nessuna deriva da un dato di StreamWave, che non esiste.

### 📌 A1 — I dati di riferimento sono proxy, non StreamWave

L'analisi poggia su due cataloghi pubblici reali:

- il **catalogo Netflix** rappresenta il catalogo attuale di StreamWave;
- il **catalogo Spotify** rappresenta il mercato musicale accessibile.

È l'assunzione strutturale su cui poggia tutto il resto. Regge il ragionamento — i due cataloghi sono abbastanza rappresentativi dei rispettivi mercati da rendere il confronto informativo — ma nessuna delle conclusioni descrive letteralmente StreamWave. Ogni volta che il documento dice "il nostro catalogo", intende "il catalogo proxy".

### 📌 A2 — Copertura temporale dei dati reali

Il catalogo video è aggiornato al **2021**, quello musicale al **2022**.

**Cosa questo impedisce**: nessuna conclusione su dinamiche di mercato successive a quelle date. Nessuna analisi di tendenza recente, nessuna considerazione sull'evoluzione dei consumi musicali degli ultimi anni. Le misure descrivono una fotografia, non una traiettoria.

### 📌 A3 — Non esistono dati comportamentali

Nessuna delle due fonti contiene visioni, ascolti, sessioni, abbonamenti o ricavi. Tutto ciò che riguarda **engagement e revenue** è generato per simulazione, con assunzioni dichiarate, in una fase successiva del progetto. Nessun numero di comportamento utente in questo progetto è osservato.

### 📌 A4 — Modello di ricavo a due tier

StreamWave adotterebbe una struttura a due livelli di abbonamento:

| Tier | Contenuti | Prezzo mensile assunto |
|---|---|---|
| **Base** | solo video | **8,99 €** |
| **Premium** | video + musica | **12,99 €** |

Differenziale: **4,00 € al mese**.

**Perché questo modello**: è il pattern prevalente quando una piattaforma video aggiunge un verticale adiacente, e rende l'impatto economico misurabile con due sole leve — quanti abbonati passano al premium, e quanto costa in più il premium — invece che con una catena di assunzioni sul comportamento.

**Perché prezzi puntuali e non un intervallo**: un prezzo non è una misura incerta, è una decisione di scenario. L'incertezza di questa analisi vive nel **tasso di adozione** del tier premium, ed è lì che verrà espressa come intervallo. Mettere un intervallo anche sul prezzo moltiplicherebbe le combinazioni senza aggiungere informazione.

**Cosa resta fuori dal modello**: ricavi pubblicitari ed effetti sulla retention. Se emergessero come rilevanti andrebbero trattati come estensione dichiarata del modello, non assorbiti in silenzio nelle stime.

### 📌 A5 — Base utenti e orizzonte

- **Base utenti**: parco abbonati esistente al momento del lancio, assunto stabile per l'orizzonte considerato.
- **Orizzonte**: **12 mesi** dal lancio ipotetico del verticale musicale. Oltre i 12 mesi la fiducia nelle assunzioni degrada al punto da rendere la stima non informativa.
- **Perimetro geografico**: globale, coerentemente con la copertura dei due cataloghi. Nessuna analisi per singolo mercato nazionale.

## 3. North Star metric

> ### 🎯 `BQ1-K1` — Quota di catalogo già musicale
> **Quanta parte del catalogo video attuale è già a contenuto musicale** — musical, documentari musicali, concerti, film sulla musica.
>
> **Confidenza: alta** · valore puntuale

**Perché questa e non un'altra.** Il criterio di successo dell'iniziativa deve essere una misura di **coerenza strategica**: se il pubblico che StreamWave ha già mostra appetito per il contenuto musicale, l'espansione è un'estensione naturale del catalogo; se non lo mostra, è l'ingresso in un mercato estraneo, con tutti i costi di acquisizione che comporta.

Questa misura ha una proprietà che nessuna alternativa possiede: è **osservata direttamente**. Il catalogo video classifica già i propri titoli, e una delle categorie è dedicata al contenuto musicale. Non serve alcuna mappatura interpretativa tra domini, nessuna assunzione, nessun dato simulato. È l'unica misura del framework che può reggere la confidenza alta ed essere presentata come valore puntuale — e una metrica di riferimento che dovesse essere presentata come intervallo sarebbe un oggetto strano da mettere in cima a una dashboard.

**Come si legge**: valore alto significa che l'adiacenza esiste già dentro il catalogo. Non dice che l'espansione sarà redditizia: dice che sarebbe coerente.

### Alternative considerate e scartate

| Alternativa | Perché scartata |
|---|---|
| **Uplift del ricavo medio per utente** (`BQ3-K2`) | Parlerebbe la lingua del board, ma poggia interamente su dati simulati: confidenza bassa, quindi obbligatoriamente un intervallo. Eleggere a criterio ufficiale di successo un numero che non abbiamo osservato significa dare autorevolezza a un'assunzione. |
| **Sovrapposizione dei profili di mood** (`BQ1-K3`) | Concettualmente la misura più ricca di coerenza fra i due cataloghi, ma richiede una tabella di corrispondenza costruita dall'analista: uno strato interpretativo che la porta a confidenza media. Resta nel framework, non come metrica di riferimento. |
| **Indice composito coerenza + impatto** | Sembra la sintesi ideale e sarebbe l'errore peggiore: fonderebbe un dato osservato e una simulazione in una cifra sola, nascondendo al lettore che le due metà non meritano la stessa fiducia. Escluso per principio, non per opportunità. |

## 4. Le tre domande di business

### BQ1 — Posizionamento

**Formulazione originale**: qual è il posizionamento del contenuto musicale rispetto a quello video in termini di caratteristiche "vincenti" (durata, genere, mood)? C'è overlap di audience potenziale?

**Formulazione misurabile**: rispetto al catalogo video attuale, quanto il catalogo musicale accessibile si sovrappone per **durata dei contenuti** (in minuti), **presenza di contenuto già musicale** (quota di titoli) e **profilo di mood** (quota di tracce che ricade nell'intervallo occupato dal catalogo video sugli assi energia, positività e ritmo)? Il confronto è tra profili di contenuto, non tra pubblici osservati.

### BQ2 — Segmento di ingresso

**Formulazione originale**: quale segmento musicale (genere/mood) rappresenterebbe l'opportunità di ingresso più coerente con il catalogo attuale?

**Formulazione misurabile**: ordinando i segmenti musicali per **domanda relativa** (indice di popolarità mediana, scala 0-100) e per **affinità con il catalogo attuale** (distanza sugli assi di mood, scala 0-1), quali segmenti si collocano nel quadrante ad alta domanda e alta affinità? La soglia di ingresso è ordinale: conta la posizione relativa tra segmenti, non un valore assoluto.

### BQ3 — Impatto stimato

**Formulazione originale**: che impatto stimato (simulato, con assunzioni dichiarate) avrebbe l'aggiunta del verticale musicale su engagement/revenue?

**Formulazione misurabile**: nell'orizzonte di 12 mesi e sotto il modello a due tier di A4, quale intervallo di **tasso di adozione del tier premium** (in punti percentuali della base utenti) e quale conseguente intervallo di **variazione del ricavo medio per utente** (in euro/mese) sono compatibili con le assunzioni dichiarate? La risposta è un intervallo best/base/worst, mai un valore singolo.

## 5. Framework KPI

### 5.1 Convenzioni

**Identificativi.** Ogni KPI ha due nomi. La **sigla** `BQn-Km` indica la domanda di business di appartenenza e la progressione al suo interno: serve alla tracciabilità, e a colpo d'occhio dice a quale domanda un numero appartiene. Il **nome semantico** in inglese `snake_case` è quello che diventerà il nome della misura nel modello dati, ed è univoco sull'intero progetto — non solo all'interno della propria domanda.

**Un KPI, una domanda.** Ogni KPI appartiene a esattamente una domanda di business. Dove è utile anche a un'altra, viene citato come riferimento, mai ridefinito.

### 5.2 Nota metodologica sulle granularità

Il catalogo musicale assegna una traccia a più segmenti quando è pertinente a più d'uno. Ne conseguono **due granularità distinte e non intercambiabili**:

| Granularità | Cosa conta | Quando si usa |
|---|---|---|
| **coppia traccia-segmento** | ogni combinazione traccia + segmento | analisi **per segmento**: confronti fra generi, profili di mood |
| **traccia deduplicata** | ogni traccia una volta sola | qualunque **totale di catalogo** |

Un totale calcolato senza deduplicare sovrastima di circa un quinto, perché conta più volte le stesse tracce. Ogni scheda KPI dichiara in quale delle due granularità opera: senza quella dichiarazione due misure apparentemente coerenti darebbero totali diversi, e non ci sarebbe modo di sapere quale è corretta.

*(Le percentuali citate qui e altrove nel documento sono **caratteristiche dei dati di origine**, non risultati dell'analisi — vedi la regola sui numeri in §8.)*

### 5.3 Nota metodologica sugli assi di mood

Il confronto di mood tra i due cataloghi non può poggiare sui nomi dei generi: le due tassonomie classificano lungo dimensioni diverse — quella musicale per stile sonoro, quella video per forma narrativa — e la sovrapposizione lessicale fra le due è trascurabile.

Il confronto avviene quindi su **tre assi comuni definiti a priori**, tutti su scala 0-1:

| Asse | Significato |
|---|---|
| **energia** | intensità e vigore percepiti del contenuto |
| **positività** | tono emotivo, dal cupo al brillante |
| **ritmo** | regolarità e propulsione ritmica |

Sul lato musicale i tre assi sono **misurati direttamente**: il catalogo li espone come attributi di ogni traccia. Sul lato video sono **assegnati** tramite una tabella di corrispondenza che associa ogni genere del catalogo a un profilo atteso sui tre assi. Quella tabella è costruita dall'analista, va versionata insieme al resto ed è contestabile riga per riga: è la ragione per cui ogni KPI che la usa non supera la confidenza media.

### 5.4 Tabella riepilogativa

Indice delle schede. Le definizioni autorevoli sono le schede di §5.5; qui non compaiono le formule.

| Sigla | Nome semantico | Domanda | Fonte | Confidenza | Formato |
|---|---|---|---|---|---|
| `BQ1-K1` 🎯 | `music_adjacent_catalog_share` | BQ1 | Netflix (reale) | alta | valore puntuale |
| `BQ1-K2` | `format_duration_gap` | BQ1 | Derivato (Netflix + Spotify) | alta | valore puntuale |
| `BQ1-K3` | `mood_profile_overlap` | BQ1 | Derivato (Netflix + Spotify) | media | valore puntuale con nota |
| `BQ2-K1` | `segment_demand_index` | BQ2 | Spotify (reale) | media | valore puntuale con nota |
| `BQ2-K2` | `segment_catalog_affinity` | BQ2 | Derivato (Netflix + Spotify) | media | valore puntuale con nota |
| `BQ2-K3` | `segment_entry_priority` | BQ2 | Derivato (`BQ2-K1` + `BQ2-K2`) | media | ordinamento |
| `BQ3-K1` | `premium_tier_adoption_rate` | BQ3 | Sintetico | bassa | range best/base/worst |
| `BQ3-K2` | `arpu_uplift` | BQ3 | Derivato (`BQ3-K1` + prezzi di A4) | bassa | range best/base/worst |

🎯 = North Star metric

### 5.5 Schede

---

#### `BQ1-K1` · `music_adjacent_catalog_share` 🎯

**Domanda di business**: BQ1 — Posizionamento

**Cosa misura**: quanta parte del catalogo video attuale è già a contenuto musicale.

**Formula concettuale**: numero di titoli classificati dalla fonte nella categoria dedicata al contenuto musicale, diviso il numero totale di titoli del catalogo.

**Unità**: percentuale · **Granularità**: titolo · **Direzione**: valore alto = maggiore coerenza dell'espansione

**Fonte**: Netflix (reale) · **Confidenza**: **alta** — la classificazione è assegnata dalla fonte e viene solo letta; nessuna mappatura né assunzione interposta · **Formato**: valore puntuale

**Nota**: un titolo può appartenere a più categorie. Il denominatore è il conteggio dei titoli distinti, non delle assegnazioni di categoria.

---

#### `BQ1-K2` · `format_duration_gap`

**Domanda di business**: BQ1 — Posizionamento

**Cosa misura**: la distanza di formato tra il contenuto video e quello musicale, in termini di durata di una singola unità di fruizione.

**Formula concettuale**: differenza tra la durata mediana di un film del catalogo video e la durata mediana di una traccia del catalogo musicale, entrambe espresse in minuti.

**Unità**: minuti · **Granularità**: film per il lato video, traccia deduplicata per il lato musicale · **Direzione**: nessuna direzione — è un profilo, non un obiettivo

**Fonte**: Derivato (Netflix + Spotify) · **Confidenza**: **alta** — entrambi i termini sono osservati direttamente e il confronto è aritmetico, non interpretativo · **Formato**: valore puntuale

**Nota — esclusione delle serie**: il confronto riguarda i soli **film**. Il catalogo video misura le serie in stagioni, non in minuti, e convertirle richiederebbe un'assunzione su numero e durata degli episodi che i dati non contengono: sarebbe un numero inventato travestito da misura. Le serie sono trattate a parte in §8 come formato a consumo seriale.

---

#### `BQ1-K3` · `mood_profile_overlap`

**Domanda di business**: BQ1 — Posizionamento

**Cosa misura**: quanta parte del catalogo musicale accessibile ricade nella regione di mood già occupata dal catalogo video.

**Formula concettuale**: quota di tracce il cui profilo sui tre assi di mood (§5.3) cade all'interno dell'intervallo occupato dai generi del catalogo video sugli stessi assi.

**Unità**: percentuale · **Granularità**: traccia deduplicata · **Direzione**: valore alto = maggiore sovrapposizione di profilo

**Fonte**: Derivato (Netflix + Spotify) · **Confidenza**: **media** — i dati sono reali su entrambi i lati, ma tra dato e misura si interpone la tabella di corrispondenza di §5.3 · **Formato**: valore puntuale con nota metodologica

**Nota**: è una sovrapposizione tra **caratteristiche di contenuto**, non tra pubblici. Non dice che gli spettatori di un genere video ascolterebbero la musica corrispondente.

---

#### `BQ2-K1` · `segment_demand_index`

**Domanda di business**: BQ2 — Segmento di ingresso

**Cosa misura**: la domanda relativa di un segmento musicale rispetto agli altri segmenti.

**Formula concettuale**: indice di popolarità mediano delle tracce del segmento, calcolato sulle tracce deduplicate del segmento.

**Unità**: indice 0-100 · **Granularità**: coppia traccia-segmento per l'appartenenza, traccia deduplicata per il calcolo · **Direzione**: valore alto = domanda maggiore

**Fonte**: Spotify (reale) · **Confidenza**: **media** — l'indice di popolarità è un dato osservato, ma usarlo come proxy della domanda di mercato è un'assunzione dichiarata · **Formato**: valore puntuale con nota metodologica

**Nota — perché non si contano le tracce**: il catalogo di riferimento contiene **lo stesso numero di tracce per ogni segmento**, per come è stato campionato. Contare le tracce per dimensionare un segmento restituirebbe lo stesso valore ovunque: misurerebbe il campionamento, non il mercato. Il dimensionamento poggia quindi sulla domanda, mai sull'offerta.

**Nota — fragilità dell'indice**: circa una traccia su sette ha indice di popolarità pari a zero, e queste non sono distribuite uniformemente: alcuni segmenti ne concentrano oltre il 60%, il che trascina verso il basso la loro mediana. L'indice misura inoltre la popolarità **sulla piattaforma di origine al momento della rilevazione**, non la domanda di mercato in senso lato. È il miglior proxy disponibile ed è la ragione per cui questo KPI non supera la confidenza media.

---

#### `BQ2-K2` · `segment_catalog_affinity`

**Domanda di business**: BQ2 — Segmento di ingresso

**Cosa misura**: quanto il profilo di mood di un segmento musicale è vicino a quello del catalogo video attuale.

**Formula concettuale**: complemento della distanza tra il profilo di mood mediano del segmento e il profilo di mood mediano del catalogo video, misurata sui tre assi di §5.3 e normalizzata sulla scala 0-1.

**Unità**: indice 0-1 · **Granularità**: coppia traccia-segmento · **Direzione**: valore alto = maggiore affinità

**Fonte**: Derivato (Netflix + Spotify) · **Confidenza**: **media** — dipende dalla tabella di corrispondenza di §5.3 · **Formato**: valore puntuale con nota metodologica

---

#### `BQ2-K3` · `segment_entry_priority`

**Domanda di business**: BQ2 — Segmento di ingresso

**Cosa misura**: l'ordine di priorità dei segmenti musicali come candidati all'ingresso.

**Formula concettuale**: ordinamento dei segmenti secondo la combinazione della loro domanda relativa (`BQ2-K1`) e della loro affinità con il catalogo (`BQ2-K2`), con il peso relativo dei due criteri dichiarato esplicitamente.

**Unità**: posizione in graduatoria · **Granularità**: segmento · **Direzione**: posizione alta = candidato migliore

**Fonte**: Derivato (`BQ2-K1` + `BQ2-K2`) · **Confidenza**: **media** — eredita il livello dei due KPI che compone, entrambi a confidenza media · **Formato**: ordinamento

**Nota**: comporre due misure dello **stesso** livello di confidenza è legittimo, e il risultato eredita quel livello. Ciò che il framework vieta è comporre misure di livelli **diversi**, perché il numero risultante nasconderebbe al lettore che una delle sue metà è meno affidabile dell'altra.

---

#### `BQ3-K1` · `premium_tier_adoption_rate`

**Domanda di business**: BQ3 — Impatto stimato

**Cosa misura**: quanta parte della base abbonati passerebbe al tier premium entro l'orizzonte considerato.

**Formula concettuale**: quota della base utenti che sottoscrive il tier premium entro 12 mesi dal lancio, simulata sotto tre scenari di adozione dichiarati.

**Unità**: percentuale della base utenti · **Granularità**: base utenti · **Direzione**: valore alto = adozione maggiore

**Fonte**: Sintetico · **Confidenza**: **bassa** — nessun dato comportamentale reale esiste; il valore dipende interamente dalle assunzioni di scenario · **Formato**: **range best/base/worst**

**Nota**: è qui che vive l'incertezza dell'intera terza domanda. Le assunzioni che generano i tre scenari saranno dichiarate e versionate insieme allo script che le implementa.

---

#### `BQ3-K2` · `arpu_uplift`

**Domanda di business**: BQ3 — Impatto stimato

**Cosa misura**: la variazione del ricavo medio per utente attribuibile all'introduzione del tier premium.

**Formula concettuale**: prodotto tra il tasso di adozione del tier premium (`BQ3-K1`) e il differenziale di prezzo tra i due tier dichiarato in A4, riferito all'intera base utenti su base mensile.

**Unità**: euro per utente al mese · **Granularità**: base utenti · **Direzione**: valore alto = impatto economico maggiore

**Fonte**: Derivato (`BQ3-K1` sintetico + prezzi assunti in A4) · **Confidenza**: **bassa** — eredita l'incertezza del tasso di adozione, che è la sua unica variabile · **Formato**: **range best/base/worst**

**Nota**: il differenziale di prezzo è fissato per scelta (A4), non stimato. Tutta la variabilità del risultato proviene dal tasso di adozione, il che rende l'intervallo leggibile: la sua ampiezza dice quanto siamo incerti sull'adozione, e nient'altro.

---

## 6. Scala di confidenza

Ogni KPI dichiara quanta fiducia il suo valore può sostenere. Il criterio è **quanti strati interpretativi separano il dato osservato dal numero mostrato**, ed è verificabile leggendo la formula concettuale della scheda: chiunque può applicarlo e arrivare alla stessa classificazione.

| Livello | Criterio di attribuzione | Formato di presentazione ammesso |
|---|---|---|
| **alta** | il valore è osservato direttamente sui dati reali, senza mappature né assunzioni interposte | valore puntuale |
| **media** | il valore poggia su dati reali, ma tra il dato e la misura si interpone almeno una mappatura o un'assunzione dichiarata | valore puntuale, accompagnato da nota metodologica |
| **bassa** | il valore dipende da dati generati o da assunzioni non verificabili con i dati disponibili | **esclusivamente** range best/base/worst |

**La regola non negoziabile**: un KPI a confidenza bassa non può essere presentato come valore singolo. Un numero singolo comunica una certezza che il dato non ha, e in una presentazione al board è la differenza tra informare e persuadere.

La classificazione non è un giudizio sulla qualità del lavoro: è una proprietà della catena che porta dal dato al numero. Che i KPI della terza domanda siano tutti a confidenza bassa non è un difetto dell'analisi, è la conseguenza del fatto che simuliamo un mercato in cui StreamWave non è ancora entrata.

## 7. Impatto economico stimato

L'impatto economico è il **titolo secondario** del documento, non il suo criterio di successo. È misurato da `BQ3-K2` (`arpu_uplift`) e si presenta **sempre come intervallo best/base/worst**, mai come valore singolo.

**Perché è separato dalla North Star.** La metrica di riferimento (§3) è osservata; questa è simulata. Presentarle insieme, o peggio fonderle in un indice unico, darebbe al lettore l'impressione che meritino la stessa fiducia. Il documento le tiene distinte per costruzione: la coerenza strategica dice *se l'espansione ha senso rispetto a ciò che siamo*, l'impatto economico dice *quanto potrebbe valere se le assunzioni reggessero*. Sono due domande diverse e vanno lette separatamente.

**Come si legge un intervallo**: l'ampiezza dell'intervallo è essa stessa informazione. Un intervallo largo non è una risposta debole, è una dichiarazione onesta di quanto l'esito dipenda dall'assunzione di adozione. La decisione del board dovrebbe considerare lo scenario *worst* come il caso da poter sostenere, non lo scenario *best* come il caso da aspettarsi.

## 8. Out of scope

Cosa questo progetto **non** risponderà, e perché.

| Domanda esclusa | Motivazione |
|---|---|
| **Quanto costa costruire il verticale musicale** | Nessun dato su licenze musicali, infrastruttura o organico è disponibile. Senza il lato costi questo è un business case *di opportunità*, non finanziario: chi cercasse qui un ritorno sull'investimento non lo troverà, ed è deliberato. |
| **Se il pubblico attuale vorrebbe la musica** | Non esiste alcun dato comportamentale, di sondaggio o di abbandono. La sovrapposizione che BQ1 misura è tra **caratteristiche di contenuto**, non tra persone osservate. |
| **Quanto è grande il mercato di un segmento musicale** | Il catalogo di riferimento contiene lo stesso numero di tracce per ogni segmento, per costruzione del campione: qualunque dimensionamento basato sull'offerta misurerebbe il campionamento. Si misura la domanda relativa fra segmenti, non la dimensione assoluta di ciascuno. |
| **Come si confronta il formato seriale con la musica** | Il catalogo video misura le serie in stagioni e non in minuti. Convertirle richiederebbe un'assunzione su numero e durata degli episodi che i dati non contengono. Il confronto di durata riguarda i soli film. |
| **Quale sarebbe il prezzo ottimale del tier premium** | I prezzi di A4 sono uno scenario assunto, non il risultato di un'analisi di pricing: senza dati di elasticità della domanda ogni prezzo è un'ipotesi di lavoro. |
| **Cosa è successo al mercato dopo il 2022** | I dati reali si fermano al 2021 (video) e al 2022 (musica). Nessuna conclusione può riguardare dinamiche successive. |

### Inferenze da evitare

- **Che questo framework dimostrerà la convenienza dell'espansione.** È costruito per poter produrre anche una risposta negativa, ed è progettato esplicitamente per non impedirla. Una North Star bassa è un risultato, non un fallimento della misura.
- **Che la somiglianza di mood implichi trasferibilità di pubblico.** È una relazione tra attributi di catalogo. Non descrive il comportamento delle persone, e nessuna misura di questo documento autorizza a parlarne in termini di causa ed effetto.

### Regola sui numeri di questo documento

Questo documento non contiene risultati. Ogni numero che vi compare appartiene a una di due categorie, entrambe **input** e mai esiti:

1. **assunzioni di scenario**, marcate con 📌 nella §2 — i prezzi dei tier, l'orizzonte di 12 mesi;
2. **caratteristiche dichiarate dei dati di origine** — le scale di misura, le proporzioni che descrivono la qualità delle fonti e che motivano una scelta di metodo.

Nessun numero di questo documento risponde a BQ1, BQ2 o BQ3. Le risposte arriveranno dalle feature successive, e porteranno con sé l'etichetta di fonte e confidenza definita qui.
