# Research — Feature 001: Business Case e Framework KPI

**Data**: 2026-08-07 | **Fase**: 0 (Outline & Research) | **Spec**: [spec.md](./spec.md)

Questa fase non produce numeri di risultato (FR-016). Ispeziona i dataset reali per stabilire **quali KPI sono effettivamente costruibili**, così che il documento non proponga misure che si riveleranno impossibili in fase di implementazione — l'edge case "un KPI si rivela non calcolabile" della spec.

## Inventario dei dati reali

### Netflix — `data/raw/netflix_titles.csv`

8.807 titoli: 6.131 film e 2.676 serie TV. Campi utilizzabili e loro completezza:

| Campo | Nulli | Note |
|---|---|---|
| `type` | 0% | Movie / TV Show |
| `duration` | 0,03% | **formato misto**: minuti per i film, numero di stagioni per le serie |
| `listed_in` | 0% | 42 generi distinti, multi-valore per titolo |
| `rating` | 0,05% | 18 valori (classificazione per età) |
| `release_year` | 0% | |
| `date_added` | 0,1% | |
| `country` | 9,4% | |
| `director` | 29,9% | inutilizzabile per analisi sistematiche |
| `description` | 0% | testo libero, unica fonte di segnale sul tono |

Nessun campo di audience, visione o ricavo. Nessun campo di mood.

### Spotify — `data/raw/spotify_tracks_dataset.csv`

114.000 righe, 114 generi. Audio feature reali e complete: `valence`, `energy`, `danceability`, `acousticness`, `instrumentalness`, `speechiness`, `liveness`, `tempo`, `loudness`. Più `popularity` (0-100) e `duration_ms` (mediana 213 s).

## Ritrovamenti che vincolano il framework

### R1 — Il campione è bilanciato per costruzione: i conteggi non misurano il mercato

Ogni genere ha **esattamente 1.000 tracce**. La distribuzione dei generi nel dataset è un artefatto di campionamento, non un fatto di mercato.

**Conseguenza**: qualunque KPI che dimensioni un segmento contando tracce è privo di significato — restituirebbe 1.000 per ogni genere. Il dimensionamento deve poggiare su `popularity`, che varia, non sulla numerosità.

### R2 — Il 21% delle righe sono tracce ripetute

89.741 `track_id` distinti su 114.000 righe: 16.641 identificativi compaiono più volte, perché una traccia è assegnata a più generi.

**Conseguenza**: due granularità diverse e non intercambiabili. Le analisi **per genere** lavorano sulle coppie traccia-genere (114.000); qualunque **totale di catalogo** deve deduplicare su `track_id` (89.741). Ogni KPI deve dichiarare in quale delle due vive, altrimenti i totali gonfiano del 21%.

### R3 — Le durate non sono direttamente confrontabili

Netflix misura i film in minuti (6.128 titoli, mediana 98 min, range 3-312) e le serie in stagioni (2.676 titoli). Spotify misura in millisecondi.

**Conseguenza**: il confronto di durata è legittimo solo tra **film Netflix e tracce Spotify**, entrambi riconducibili a minuti. Le serie TV escono dal KPI di durata e vanno trattate a parte come formato a consumo seriale — cosa che il documento deve dichiarare, non silenziare.

### R4 — I generi dei due domini non si agganciano per nome

Solo **6 generi Spotify su 114** hanno una corrispondenza lessicale con i 42 generi Netflix (`anime`, `british`, `children`, `comedy`, `kids`, `spanish`), e tre di queste sono coincidenze di lingua o target, non di contenuto.

**Conseguenza**: l'overlap di BQ1 non può essere costruito sui nomi dei generi. Serve un piano di confronto diverso, che è la decisione D1.

### R5 — `popularity` ha una massa di zeri concentrata

14,1% delle tracce ha `popularity = 0`, distribuita in modo non uniforme: `jazz` 68%, `iranian` 66%, `romance` 64%, `soul` 61%, `latin` 59%. Nessun genere è però interamente a zero.

**Conseguenza**: la mediana per genere è trascinata verso il basso proprio nei generi più penalizzati, e `popularity` misura la popolarità **su Spotify al momento dell'estrazione**, non la domanda di mercato. Resta il miglior proxy disponibile, ma la sua fragilità va dichiarata e il KPI che lo usa non può salire sopra confidenza media.

## Decisioni

### D1 — L'overlap si costruisce sul profilo di mood, non sui generi

**Decisione**: BQ1 confronta i due cataloghi attraverso una **tabella di corrispondenza curata e versionata** che associa ogni genere Netflix a un profilo di mood atteso (assi: energia, positività, ritmo). Il lato Spotify usa le audio feature reali (`energy`, `valence`, `danceability`); il lato Netflix usa la mappatura dichiarata. L'overlap è la sovrapposizione tra le due distribuzioni su quegli assi.

**Rationale**: è l'unico piano di confronto che esiste davvero nei dati. Le audio feature sono misurate; la mappatura dei generi video è interpretativa, e proprio per questo va resa esplicita in una tabella che il lettore può contestare riga per riga, invece di restare implicita in un calcolo.

**Alternative scartate**: matching lessicale dei generi (R4: copre 6 casi su 114); estrazione del tono dal campo `description` con tecniche NLP (introduce un modello non spiegabile a un board e sfonda il vincolo di una giornata del principio III).

### D2 — Il segmento si dimensiona sulla domanda, non sull'offerta

**Decisione**: i KPI di BQ2 usano `popularity` aggregata per genere come proxy di domanda relativa, su tracce deduplicate. **Nessun KPI conta tracce per dimensionare un segmento.**

**Rationale**: R1 rende i conteggi privi di informazione. `popularity` è l'unica variabile che porta segnale di domanda, per quanto imperfetta.

**Alternative scartate**: conteggio di tracce per genere (misura il campionamento, non il mercato); dati di mercato esterni (violerebbe il perimetro delle fonti ammesse dalla constitution).

**Impatto sulla spec**: la tabella di provenienza della spec prevede una famiglia "Dimensionamento del segmento (BQ2)" a confidenza **media** con criterio "il dataset è un campione del mercato, non il mercato". R1 e R5 sono più severi di così. Il criterio va riscritto e la confidenza confermata media solo perché `popularity` è un dato osservato — mai alta. Vedi la nota di impatto in fondo.

### D3 — Il confronto di durata esclude le serie TV

**Decisione**: il KPI di durata confronta film Netflix (minuti) e tracce Spotify (minuti). Le serie TV sono escluse dal confronto e trattate in una nota separata sul formato seriale.

**Rationale**: R3. Convertire stagioni in minuti richiederebbe un'assunzione sul numero e la durata degli episodi che i dati non contengono: sarebbe un numero inventato travestito da misura.

**Alternative scartate**: stima della durata delle serie via numero medio di episodi (dato assente); esclusione totale del confronto di durata (perderebbe il confronto di formato, che è il cuore di BQ1).

### D4 — Ogni KPI dichiara la propria granularità

**Decisione**: la scheda di ogni KPI riporta se opera su coppie traccia-genere o su tracce deduplicate. Il documento definisce le due granularità una volta sola, in una nota metodologica, e le schede vi rimandano.

**Rationale**: R2. Senza questa dichiarazione due KPI apparentemente coerenti darebbero totali diversi del 21%, e non ci sarebbe modo di sapere quale è giusto.

### D5 — Criteri operativi della scala di confidenza

**Decisione**: FR-009 è soddisfatto da questi tre criteri, applicabili da un terzo senza giudizio soggettivo:

| Livello | Criterio |
|---|---|
| **alto** | il valore è osservato direttamente su dati reali, senza mappature né assunzioni interposte |
| **medio** | il valore poggia su dati reali, ma tra dato e KPI c'è almeno una mappatura o assunzione dichiarata (es. la tabella di corrispondenza di D1, o l'uso di `popularity` come proxy di domanda) |
| **basso** | il valore dipende da dati generati o da assunzioni non verificabili con i dati disponibili |

**Rationale**: il criterio discriminante è *quanti strati interpretativi separano il dato osservato dal numero mostrato*, che è ispezionabile leggendo la formula concettuale. Le alternative basate su intervalli di confidenza statistici non si applicano: la maggior parte di questi KPI sono descrittivi, non stimatori.

### D6 — Nessun artefatto `contracts/`

**Decisione**: la fase 1 non produce una cartella `contracts/`.

**Rationale**: il contratto che questa feature espone alle feature successive **è il documento stesso** — le schede KPI con identificativo, formula e granularità. Duplicarne lo schema in un file separato creerebbe due definizioni della stessa cosa destinate a divergere, che è precisamente ciò che FR-005b vieta all'interno del documento. Il vincolo vale a maggior ragione tra file diversi.

## Nota di impatto sulla spec

R1, R2 e R5 sono emersi dopo la scrittura della spec e ne toccano un punto: la famiglia di KPI "Dimensionamento del segmento (BQ2)" della tabella di provenienza ha un criterio di attribuzione ora incompleto. Non è una contraddizione — la confidenza resta media — ma il criterio andrebbe riscritto per citare il campionamento bilanciato e la massa di zeri di `popularity` invece del generico "il dataset è un campione del mercato". **Modifica proposta, non applicata**: tocca la spec, che è già approvata.
