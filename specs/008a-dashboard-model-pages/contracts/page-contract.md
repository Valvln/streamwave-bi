# Contratto di pagina: che cosa la dashboard espone, e con quale forma

**Feature**: 008a-dashboard-model-pages | **Data**: 2026-08-24 | **Stato**: **da approvare** (punto di fermata 3)

Questo documento è il disegno delle pagine, scritto **prima** che Power BI Desktop venga aperto (`FR-001`). Non è un resoconto di ciò che esiste: nel momento in cui viene proposto, non esiste nulla. Ciò che esiste sarà descritto dalla sezione «Esito della costruzione» di [quickstart.md](../quickstart.md), e in caso di divergenza **quella** è la fonte autorevole, non questa (`F9`).

**Che cosa questo documento non contiene, deliberatamente**: nessun valore di KPI trascritto (`FR-003`). Le misure si citano per nome e i valori si rinviano alla sezione di [`docs/kpi_measures.md`](../../../docs/kpi_measures.md) che li pubblica. Una seconda copia di un valore è una copia che può divergere dall'originale senza che nulla lo segnali, ed è il difetto che questo progetto ha già incontrato altrove.

**Che cosa non decide**: la prosa, i limiti in forma divulgativa, il tono. Sono della `008b`, e la sezione 8 dichiara dove andranno a stare perché quella feature non debba ridisegnare le pagine per farvi entrare il proprio testo.

---

## 1. La mappa: quale KPI vive su quale pagina, e a quale grana

Quattro pagine. Otto KPI, ciascuno su esattamente una pagina di domanda; la North Star compare una seconda volta sulla pagina di ingresso, ed è l'unica ripetizione ammessa (sezione 3).

| Pagina | KPI esposti | Misure lette | Grana pubblicata ([data-model.md](../data-model.md) §1.4) |
|---|---|---|---|
| **Ingresso** | `BQ1-K1` 🎯 | `music_adjacent_catalog_share` | catalogo intero |
| **BQ1 — Posizionamento** | `BQ1-K1` 🎯, `BQ1-K2`, `BQ1-K3` | `music_adjacent_catalog_share`, `c1_music_above_median`, `format_duration_gap`, `mood_profile_overlap` | catalogo intero |
| **BQ2 — Segmento di ingresso** | `BQ2-K1`, `BQ2-K2`, `BQ2-K3` | `segment_demand_index`, `segment_zero_share`, `segment_catalog_affinity`, `segment_entry_priority_score`, `segment_entry_priority_quadrant`, `segment_entry_priority_rank` | segmento |
| **BQ3 — Impatto stimato** | `BQ3-K1`, `BQ3-K2` | nessuna misura: sei valori di scenario (sezione 6) | scenario |

**Le pagine sono quattro e non tre**, e la ragione non è estetica: la pagina di ingresso è l'unica che porta la navigazione senza essere sotto la giurisdizione di una domanda di business. Fondere l'ingresso con `BQ1` costringerebbe la North Star a convivere sulla stessa pagina con i due KPI che non la compongono, e la vicinanza suggerirebbe una composizione che non esiste.

**Ogni KPI su una pagina sola** discende da `business_case.md` §5.1: un KPI appartiene a esattamente una domanda di business, e dove serve a un'altra si cita, non si ridefinisce. La dashboard rispetta il framework invece di reinventarlo.

### 1.1 Le etichette di fonte e confidenza

Ogni KPI a schermo porta accanto le due etichette, nella forma di `business_case.md` §5.4 (`F5`, `FR-012`). Sono **etichette, non valori**: si trascrivono qui perché sono attributi fissi del KPI, non numeri misurati.

| KPI | Etichetta a schermo |
|---|---|
| `BQ1-K1` | `Fonte: Netflix (reale) · Confidenza: alta` |
| `BQ1-K2` | `Fonte: Derivato (Netflix + Spotify) · Confidenza: alta` |
| `BQ1-K3` | `Fonte: Derivato (Netflix + Spotify) · Confidenza: media` |
| `BQ2-K1` | `Fonte: Spotify (reale) · Confidenza: media` |
| `BQ2-K2` | `Fonte: Derivato (Netflix + Spotify) · Confidenza: media` |
| `BQ2-K3` | `Fonte: Derivato (BQ2-K1 + BQ2-K2) · Confidenza: media` |
| `BQ3-K1` | `Fonte: Sintetico · Confidenza: bassa` |
| `BQ3-K2` | `Fonte: Derivato (BQ3-K1 + prezzi di A4) · Confidenza: bassa` |

**Il *perché* di ciascuna confidenza non compare**: è narrazione, ed è della `008b`. Qui compare il fatto che una confidenza esiste e quale sia, che il principio I dichiara non negoziabile.

### 1.2 I formati numerici, che sono parte del contratto e non una rifinitura

Un formato può cambiare come un valore si legge senza cambiare il valore, ed è una delle poche cose che questa feature può sbagliare senza che alcuno script se ne accorga.

| KPI | Formato a schermo | Vincolo |
|---|---|---|
| `BQ1-K1` | quota sul dominio `0-1`, con le cifre decimali di `kpi_measures.md` §2.1 | se si adotta il formato percentuale, l'etichetta lo dichiara e le cifre significative restano quelle pubblicate |
| `BQ1-K2` | numero **con segno**, unità `minuti` | mai in valore assoluto: il segno porta l'informazione su quale formato sia più lungo (`kpi_measures.md` §3) |
| `BQ1-K3` | quota sul dominio `0-1`, cifre di §4.1 | come `BQ1-K1` |
| `BQ2-K1` | scala `0-100` | mai riscalata sui valori osservati: è un indice delimitato per definizione (`D3`) |
| `BQ2-K2` | dominio `0-1`, cifre di §6.1 | — |
| `BQ2-K3` | punteggio sul dominio `0-1`; posizione come intero | — |
| `BQ3-K1` | unità `punti percentuali della base` | — |
| `BQ3-K2` | unità `€ per utente al mese` | — |

---

## 2. La regola che governa ogni pagina

Enunciata qui una volta sola. Le sezioni per pagina la citano, non la ripetono.

> **Regola di invarianza a schermo (`F2`).** Un valore a schermo deve essere un valore pubblicato da [`docs/kpi_measures.md`](../../../docs/kpi_measures.md), **alla grana a cui quel documento lo pubblica**. Nessuna pagina offre un'interazione che produca un valore di KPI a una grana diversa.

Le grane pubblicate sono tre, e non ne esiste una quarta:

| Grana | KPI | Che cosa una selezione può legittimamente restringere |
|---|---|---|
| catalogo intero | `BQ1-K1`, `BQ1-K2`, `BQ1-K3` | **nulla** |
| segmento | `BQ2-K1`, `BQ2-K2`, `BQ2-K3` | il segmento, per tutti e 114 |
| scenario | `BQ3-K1`, `BQ3-K2` | lo scenario, per tutti e tre — mai riducendo a uno solo |

**Perché la regola sta qui e non dentro le formule.** L'issue `#18` osserva che `mood_profile_overlap` legge gli estremi degli assi di mood senza un `ALL` sulla categoria: un filtro di categoria video restringerebbe silenziosamente l'inviluppo e produrrebbe un valore diverso da quello pubblicato, senza alcun segnale. La correzione della formula chiuderebbe quel caso; la regola chiude **la classe** di cui quel caso è un membro, al costo di una riga di contratto e senza toccare un artefatto già verificato contro il motore. L'issue resta aperta: questa feature dimostra che il difetto non si manifesta nelle pagine costruite, non che non esista (`F2`).

**Il presidio non è la buona volontà di chi costruisce.** Ogni sezione di pagina porta la voce «interazioni non offerte, e perché» (`FR-004`), e la Fase 6 dei task verifica sul costruito, filtro per filtro, che la grana risultante sia una delle tre.

### 2.1 Un corollario che vale su tutte e quattro le pagine

**La selezione incrociata è ammessa; il filtro non lo è.** Selezionare un punto o una riga per evidenziare il corrispondente altrove non cambia alcun valore. Un filtro ricalcola, e ricalcolare è il modo in cui nasce una quarta grana.

Su `BQ2` la distinzione regge per una ragione verificabile e non per convenzione: `segment_entry_priority_quadrant` e `segment_entry_priority_rank` portano `ALL ( dim_segment )` dentro la formula (`kpi_measures.md` §7.3), quindi soglie e posizioni **non si muovono** quando un segmento viene selezionato. È la proprietà che rende la pagina interattiva senza renderla bugiarda, e va riverificata a schermo (prova 9).

---

## 3. Pagina di ingresso

**Che cosa risponde**: nulla, da sola. Porta la North Star e la porta alle tre domande.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| `BQ1-K1` 🎯 | **scheda** (card) singola, con le due etichette di §1.1 sotto il valore | è un valore unico sul catalogo intero, privo di qualunque dimensione di scomposizione. Una barra o una linea avrebbero bisogno di un asse che non esiste, e disegnarlo significherebbe inventare una dimensione. La scheda è l'unica forma che non insinua una distribuzione |
| navigazione | tre elementi cliccabili verso `BQ1`, `BQ2`, `BQ3` | — |

**Le etichette dei tre elementi di navigazione sono le intestazioni di `business_case.md` §4 alla lettera** — `BQ1 — Posizionamento`, `BQ2 — Segmento di ingresso`, `BQ3 — Impatto stimato` — e non prosa nuova. Il confine è netto: riportare il titolo di una sezione esistente non è narrazione; spiegare che cosa quella sezione contiene lo è, ed è della `008b`.

**`C1` non compare su questa pagina**, benché `FR-017` lo consentirebbe. La ragione è che sulla pagina di ingresso la North Star sta da sola: accostarle una condizione soddisfatta, in assenza delle altre due, produrrebbe la lettura di un verdetto parziale — che è precisamente ciò che `F6` esiste per impedire. Su `BQ1` la condizione ha accanto lo spazio in cui `kpi_measures.md` §2.3 la distingue dalla quota, e lì il rischio non c'è.

**Nessuna prosa su questa pagina.** Lo spazio per essa è riservato ed è dichiarato nella sezione 8.

### 3.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| qualunque filtro o slicer | `BQ1-K1` è pubblicato a grana catalogo intero e non ha varianti; ogni restrizione produce una quarta grana (sezione 2) |
| selezione incrociata | c'è una sola visuale di dato: non esiste nulla da incrociare |
| drill-through, drill-down, tooltip che calcolano | un tooltip è una visuale, e una visuale può calcolare a una grana qualunque. Nessun tooltip di questa dashboard espone una misura |

---

## 4. Pagina `BQ1` — Posizionamento

**Che cosa risponde**: quanto il catalogo musicale accessibile si sovrapponga a quello video per presenza di contenuto già musicale, durata e profilo di mood (`business_case.md` §4, BQ1).

**La forma del dato detta la forma della pagina**: tre valori unici sul catalogo intero, nessuno dei tre scomponibile per alcuna dimensione. Sono tre scalari, e tre scalari si presentano come tre schede affiancate. **È anche la ragione per cui la scheda regge qui e non regge su `BQ2`** (`FR-002`): là ogni KPI ha 114 valori, e una scheda dovrebbe sceglierne uno o aggregarli, cioè decidere al posto di chi legge.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| `BQ1-K1` 🎯 con `C1` accanto | scheda, con sotto un indicatore booleano che legge `c1_music_above_median` | `C1` è un booleano, e un booleano non ha altra forma che sé stesso. Sta accanto alla quota perché `kpi_measures.md` §2.3 avverte che **non è calcolabile dalla quota**: sono due letture diverse dello stesso catalogo, e separarle le farebbe leggere come due misure indipendenti |
| `BQ1-K2` | scheda, valore **con segno**, unità `minuti`, con accanto la quota di titoli `Movie` sul catalogo video | il segno è parte del valore (`kpi_measures.md` §3): un formato in valore assoluto perderebbe l'informazione su quale dei due formati sia più lungo, che è ciò che il KPI misura. La quota di film sta accanto perché il confronto è **asimmetrico per costruzione** — il lato video contribuisce con i soli film — e §3.4 pubblica quel numero proprio per rendere leggibile l'asimmetria |
| `BQ1-K3` | scheda | valore unico sul catalogo intero, come `BQ1-K1` |

**L'indicatore di `C1` porta la sua etichetta e non il suo significato**: `C1 — la categoria musicale è sopra la mediana delle categorie: sì/no`. Perché quella condizione conti, e che cosa non significhi, è testo della `008b`.

**La quota di titoli `Movie` non è un KPI** e non porta etichette di fonte e confidenza: è il numero che dichiara l'asimmetria del confronto, e va etichettato come tale (`quota del catalogo video costituita da film`). Come entra nel modello è la decisione `CP-1` della sezione 9.

### 4.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| **qualunque filtro di categoria video** | è il caso noto dell'issue `#18`: `mood_profile_overlap` legge gli estremi degli assi da `dim_category_mood` senza `ALL`, e un filtro di categoria restringerebbe l'inviluppo cambiando il valore di `BQ1-K3` senza alcun segnale (`FR-020`). Lo stesso filtro cambierebbe anche `music_adjacent_catalog_share` e `c1_music_above_median`, che contano titoli per categoria |
| filtro sul tipo di titolo (`Movie` / `TV Show`) | `BQ1-K2` è già definito sui soli film, e `BQ1-K1` sull'intero catalogo: un filtro produrrebbe due valori nessuno dei quali è pubblicato |
| filtro di anno | non esiste alcun KPI pubblicato per anno; l'asse temporale è una delle tre letture prive di significato di `data_model.md` §18 (`FR-018`) |
| selezione incrociata fra le tre schede | sono tre scalari indipendenti: non c'è nulla che una selezione possa restringere, e l'unico effetto possibile sarebbe azzerare gli altri due |
| drill-down sulle categorie o sui segmenti | porterebbe a grana categoria, che non è una delle tre |
| gli estremi degli assi di mood come visuale | sono pubblicati (`kpi_measures.md` §4.1) ma appartengono alla spiegazione del limite di `BQ1-K3`, non al valore: sono materiale della `008b` |

---

## 5. Pagina `BQ2` — Segmento di ingresso

**Che cosa risponde**: quali segmenti si collocano nel quadrante ad alta domanda e alta affinità, e in quale ordine di priorità (`business_case.md` §4, BQ2).

**Il vincolo che questa pagina esiste per risolvere.** Ciascuno dei tre KPI ha 114 valori, uno per segmento — `dim_segment` ha 114 righe ([data-model.md](../data-model.md) §1.1). `kpi_operators.md` §7.3, `data_model.md` §19 e la nota di adozione di `business_case.md` §4 lo chiamano tutti e tre **un problema della dashboard** e lo assegnano qui. La risposta è **due visuali sulla stessa pagina**, e nessuna delle due basta da sola.

### 5.1 La dispersione, visuale primaria

| Aspetto | Scelta |
|---|---|
| assi | ascissa `segment_demand_index` (scala `0-100`), ordinata `segment_catalog_affinity` (dominio `0-1`) |
| un punto | un segmento |
| linee di riferimento | le due misure di soglia di `F7`, esposte come misure e non digitate |
| distinzione | i segmenti con `segment_entry_priority_quadrant` vero sono visivamente distinti dagli altri |
| avvertimento | i segmenti con `dim_segment[is_high_zero_genre]` vero portano una marcatura propria, distinta da entrambe le precedenti |

**Ragione, contro la forma del dato.** `BQ2` è formulata da `business_case.md` §4 letteralmente come una domanda sul quadrante: due misure continue alla stessa grana, e la domanda chiede dove i segmenti si collocano rispetto a entrambe. Una dispersione con due linee di riferimento è la forma in cui quella domanda si legge su 114 unità senza ordinarle. L'appartenenza al quadrante, inoltre, **è un booleano già pubblicato per ogni segmento**: la visuale mostra ciò che l'artefatto contiene, non una classificazione costruita a schermo.

**Perché i segmenti `is_high_zero_genre` devono essere marcati anche nella dispersione**, e non solo nella tabella. La loro domanda mediana è nulla: nella dispersione cadono tutti contro il bordo sinistro, dove la posizione si legge come «domanda bassa». `kpi_measures.md` §5.3 dice esattamente il contrario — il valore misura la copertura della fonte, non la domanda — e senza marcatura la visuale affermerebbe con la propria geometria ciò che il documento vieta di affermare a parole. Sono `country`, `iranian`, `jazz`, `latin`, `rock`, `romance`, `soul`.

**Perché le linee di riferimento sono misure e non costanti** (`F7`, `FR-010`): due numeri digitati a mano in una visuale sono valori la cui unica fonte è che qualcuno li ha scritti, che è ciò che il principio I vieta. Le espressioni esistono già come variabili interne a `segment_entry_priority_quadrant`; esporle come misure proprie costa nulla e permette per la prima volta di **leggerle**, chiudendo — o aprendo — l'esclusione dichiarata in `kpi_measures.md` §11.1, dove quelle due soglie risultano non lette dal motore come valori a sé stanti (★3).

### 5.2 La graduatoria completa, visuale di dettaglio

Tabella sulla stessa pagina, **tutte le 114 righe**, ordinata per punteggio decrescente.

| Colonna | Misura o campo |
|---|---|
| posizione | `segment_entry_priority_rank` |
| segmento | `dim_segment[segment]`, con l'avvertimento accanto al nome dove `is_high_zero_genre` è vero |
| domanda | `segment_demand_index` |
| quota di zeri | `segment_zero_share`, **nella colonna immediatamente adiacente alla domanda** |
| affinità | `segment_catalog_affinity` |
| punteggio | `segment_entry_priority_score` |
| quadrante | `segment_entry_priority_quadrant` |

**Ragione, contro la forma del dato.** La dispersione mostra i punti e non i nomi: su 114 unità nessuna etichetta è leggibile, e la domanda «da quale segmento entrare» chiede un nome. La tabella lo dà, e dà la posizione esatta che la dispersione non può dare.

**Perché non una cima di graduatoria** (`F3`), che è l'alternativa scartata con la ragione più netta: i segmenti a mediana nulla stanno tutti nella coda profonda (`kpi_measures.md` §5.3), e una vista alle prime posizioni li escluderebbe **insieme all'avvertimento che li accompagna**. Il lettore vedrebbe una classifica pulita e non saprebbe che una parte della coda non misura la priorità ma la copertura della fonte. Una vista che tronca la coda non è una vista parziale: è una vista che mente per omissione, ed è esattamente il difetto che `kpi_measures.md` §7.4 chiede di prevenire.

**Perché non la sola tabella con ricerca**: risponde alla domanda «dov'è il segmento X», che nessuno ha posto, e non risponde a `BQ2`, che chiede un quadrante. Le due visuali non sono ridondanti — sono le due metà della stessa risposta.

**La quota di zeri è adiacente alla domanda per obbligo, non per comodità** (`D7`, `FR-015`): sono due misure e non una proprio perché una misura unica renderebbe possibile portarne a schermo una sola (`kpi_measures.md` §5.2). Separarle in due colonne distanti, o renderne una nascondibile dall'utente, ricrea il difetto che la separazione esisteva per impedire.

**L'avvertimento accanto al nome** riporta la lettura che `kpi_measures.md` §5.3 prescrive: `⚠ domanda non misurata dalla fonte`. È una marcatura, non una spiegazione — il perché è della `008b`.

**I pari merito**: due segmenti con lo stesso punteggio portano la stessa posizione e la successiva salta di altrettante unità. È il comportamento di `RANKX ( …, Skip )` già nella formula pubblicata; la tabella non deve reintrodurre un ordinamento secondario che spareggi, perché uno spareggio per nome produrrebbe un ordine riproducibile ma arbitrario presentato con l'autorevolezza di un risultato (`kpi_measures.md` §7.2).

### 5.3 `C3`

`C3` compare accanto a `BQ2-K3` come indicatore booleano: `C3 — esiste almeno un segmento nel quadrante: sì/no`. Come entra nel modello è la decisione `CP-1` della sezione 9.

Non compare alcun conteggio dei membri del quadrante come valore a sé: la dispersione lo mostra, e un conteggio a schermo sarebbe un valore in più da ancorare senza che nulla lo richieda.

### 5.4 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| filtro su qualunque attributo di `dim_track` o riga di `fact_track_segment` | `segment_demand_index` è una mediana sulle righe del fatto **senza `ALL`**: filtrare le tracce sposterebbe la mediana e produrrebbe un indice di domanda che nessun artefatto pubblica. È la forma più insidiosa della quarta grana, perché la visuale continuerebbe a chiamarsi «domanda» |
| filtro «prime N posizioni» sulla tabella | tronca la coda, cioè §5.2 |
| filtro di popolarità, di anno, di durata | come sopra: cambiano la mediana o introducono un asse temporale (`FR-018`) |
| riga di totale, somma o media su più segmenti | è la seconda delle tre letture prive di significato di `data_model.md` §18: i segmenti si sovrappongono, una traccia appartiene a più segmenti, e un totale conterebbe più volte le stesse tracce (`FR-018`) |
| conteggio delle righe di un segmento | è la prima delle tre: misura il campionamento e non il mercato (`kpi_measures.md` §5.4), e a schermo si leggerebbe come una dimensione del segmento |
| possibilità di nascondere la colonna della quota di zeri | ricrea il difetto che `D7` impedisce |
| drill-through al livello traccia | porta a una grana che non è pubblicata |

**Ammessa**: la selezione incrociata fra dispersione e tabella, in entrambe le direzioni, come evidenziazione. Non muove le soglie né le posizioni, che portano `ALL ( dim_segment )` (sezione 2.1), e non ricalcola alcun valore.

---

## 6. Pagina `BQ3` — Impatto stimato

**Che cosa risponde**: quale intervallo di adozione del tier premium e di variazione del ricavo medio per utente sia compatibile con le assunzioni dichiarate (`business_case.md` §4, BQ3).

**La forma del dato qui è diversa da tutte le altre**, e la pagina lo riflette: non ci sono misure da scrivere, ci sono sei valori di scenario congelati da un'altra feature in [`reports/bq3_scenarios.json`](../../../reports/bq3_scenarios.json) (`kpi_measures.md` §8). Non c'è aggregazione, non c'è dimensione di calcolo, non c'è relazione con il resto del modello.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| `BQ3-K1` e `BQ3-K2` | **una tabella**, due righe (un KPI ciascuna) e tre colonne (`Pessimista`, `Centrale`, `Ottimista`), più una colonna di unità | i tre valori non sono una serie né una distribuzione: sono tre ipotesi alternative, e nessuna è più probabile delle altre. Una tabella li affianca senza ordinarli e senza attribuire loro una magnitudine visiva. Una barra suggerirebbe un confronto quantitativo fra scenari, che è una lettura che le assunzioni non sostengono |

**Il divieto di scheda singola è strutturale, non una raccomandazione** (`F4`, `FR-013`). Il principio I lo impone per la confidenza bassa: un valore singolo comunica una certezza che il dato non ha. È l'unico punto in cui un principio non negoziabile prescrive direttamente una forma di visuale, e non prescriverlo qui significherebbe lasciarlo scoprire davanti allo schermo, dove la scheda singola è il comportamento predefinito di qualunque strumento.

**Il divieto di moltiplicazione** (`FR-014`): nessuna visuale, nessuna misura e nessuna colonna calcolata moltiplica `arpu_uplift` per una base utenti, per una durata o per qualunque altro fattore. Nessuna base utenti è quantificata in questo progetto, e un totale così ottenuto sarebbe un numero che nessuno ha misurato presentato con l'autorevolezza di uno misurato (`kpi_measures.md` §8).

**Il debito della `004` resta aperto mentre questi numeri vanno a schermo.** La verificabilità del benchmark su cui gli scenari poggiano è registrata come debito in `docs/roadmap.md` e la sua risoluzione è una decisione di governance che questa feature non prende. Il fatto va dichiarato nell'esito (`FR-025` per le issue, e qui per il debito), e la spiegazione a schermo è della `008b` insieme alle assunzioni `A4`, `A5` e `A6`.

Come i sei valori entrano nel modello è la decisione `CP-2` della sezione 9.

### 6.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| slicer di scenario che riduce a uno | è il divieto di `F4` per un'altra via: un intervallo ridotto a un valore è un valore singolo, e il fatto che l'utente lo abbia scelto non lo rende misurato |
| qualunque altro filtro | i sei valori non hanno dimensioni |
| selezione incrociata con il resto del modello | i valori di scenario non hanno relazione con le tabelle del catalogo, e non devono averne: una relazione renderebbe possibile filtrarli per segmento o per categoria, producendo scenari che nessuno ha stimato |
| misure o colonne derivate dai sei valori | sezione 6, divieto di moltiplicazione |

---

## 7. Navigazione

Una barra di navigazione **persistente su tutte e quattro le pagine**, con quattro elementi — `Ingresso`, `BQ1`, `BQ2`, `BQ3` — e l'elemento della pagina corrente marcato come tale.

Da ciascuna pagina si raggiunge ogni altra con un solo passaggio, tramite elementi interni al report (`FR-021`). **Il riquadro delle schede di Power BI non è navigazione**: è un'affordance dello strumento, non del report, e chi guarda il file in modalità di lettura o in un contenitore incorporato può non averlo. Un report che dipende da esso ha una navigazione che funziona solo sulla macchina di chi lo ha costruito.

La barra non porta prosa. Le etichette sono le quattro qui sopra.

---

## 8. Dove la `008b` scriverà

Lo spazio elencato qui è **riservato, non vuoto**. La differenza è operativa: una pagina disegnata senza questo spazio costringerebbe la feature successiva a ridisegnare le pagine per farvi entrare il proprio testo, e ridisegnare significa rimettere in discussione scelte già approvate e già verificate a schermo.

| Pagina | Spazio riservato | Che cosa ci andrà |
|---|---|---|
| **Ingresso** | una fascia a piena larghezza sotto la scheda della North Star, più una striscia a piè di pagina | che cosa la dashboard risponde e che cosa non risponde; l'assunzione `A1` — i dati sono proxy e non StreamWave — che la constitution impone in ogni artefatto rivolto all'utente finale |
| **`BQ1`** | una fascia sotto la fila delle tre schede, con tre aree allineate alle schede | per `BQ1-K2`, l'asimmetria del confronto; per `BQ1-K3`, la stima per eccesso e l'ampiezza degli intervalli di mood; per `BQ1-K1`, la distinzione fra quota e condizione `C1` |
| **`BQ2`** | una fascia sotto la graduatoria | la lettura di `D7` e dei segmenti `is_high_zero_genre`; il limite del campione; perché il punteggio e il quadrante non si fondono |
| **`BQ3`** | una fascia sotto la tabella degli scenari, la più alta delle quattro | le assunzioni `A4`, `A5`, `A6`; la non scalabilità dell'uplift; il tasso lordo; il debito della `004` sulla verificabilità del benchmark |

**Nessuna di queste fasce contiene testo alla chiusura di questa feature.** È la deviazione consapevole registrata nel Complexity Tracking di [plan.md](../plan.md): il principio IV non è soddisfatto nella sua metà «nella dashboard» finché la `008b` non chiude, e la conseguenza dichiarata è che il `.pbix` alla chiusura della `008a` è **leggibile, non pubblicabile**.

---

## 9. Le tre decisioni su cui questo contratto chiede una conferma

Sono i punti in cui il disegno **estende** ciò che [data-model.md](../data-model.md) fissava, e per questo tornano a Valerio invece di essere dati per acquisiti.

### `CP-1` — Due misure companion che oggi non esistono

Due valori richiesti dalle pagine sono pubblicati da `kpi_measures.md` ma **non hanno una formula DAX pubblicata**: la quota di titoli `Movie` sul catalogo video (§3.4), che dichiara l'asimmetria di `BQ1-K2`, e `C3` (§7.1), che compare accanto a `BQ2-K3`.

**Decisione proposta**: esistono nel modello come **misure companion**, scritte qui per la prima volta, sul modello di `c1_music_above_median` — che è la companion già pubblicata e già verificata contro il motore. La loro lettura si confronta **una volta** con il valore pubblicato, esattamente come le due soglie di `F7` (★3); una divergenza è un ritrovamento.

**Alternativa scartata**: portarle a schermo come testo digitato. Sarebbero due valori la cui unica fonte è che qualcuno li ha scritti — ciò che il principio I vieta e che `F7` ha già rifiutato per le soglie.

**Che cosa comporta**: le misure nel modello diventano quattordici invece delle dieci di [data-model.md](../data-model.md) §1.3 — dieci pubblicate, due soglie di `F7`, due companion di `CP-1`. Nessuna delle quattro aggiunte calcola un KPI: tre leggono valori già pubblicati e una compone un booleano da una misura pubblicata.

### `CP-2` — Come i sei valori di `BQ3` entrano nel modello

`kpi_measures.md` §8 dice che non c'è una misura da scrivere; `data_model.md` §19 assegna il vincolo «alle misure o alla dashboard» senza sceglierne una. La `007b` li ha portati nel modello e `E9` li ha letti dal motore in modo esaustivo, quindi **nel `.pbix` materializzato esistono già in qualche forma**, che questa sessione non può ispezionare.

**Decisione proposta**: i sei valori raggiungono il modello da [`reports/bq3_scenarios.json`](../../../reports/bq3_scenarios.json), come una tabella disconnessa — nessuna relazione con le altre sette — con colonne `kpi`, `scenario`, `valore`, `unità`. È l'unica forma in cui restano legati alla propria ancora invece di essere costanti digitate.

**Che cosa chiede**: che T013 accerti in quale forma il `.pbix` li porta oggi. Se sono digitati, il passaggio alla lettura dell'artefatto è un miglioramento e va registrato come tale; se già provengono dall'artefatto, non c'è nulla da fare.

**Che cosa comporta**: una **ottava tabella** rispetto alle sette di [data-model.md](../data-model.md) §1.1, priva di relazioni. La sua assenza di relazioni non è un difetto di modellazione: è ciò che impedisce di filtrare gli scenari per segmento o per categoria, producendo stime che nessuno ha fatto.

### `CP-3` — La North Star su due pagine

`BQ1-K1` compare sulla pagina di ingresso e sulla pagina `BQ1`. È l'unica ripetizione del disegno.

**Decisione proposta**: si mantiene. È la stessa misura alla stessa grana, quindi non può divergere; sull'ingresso porta le etichette e nient'altro, su `BQ1` porta `C1` accanto. L'alternativa — un ingresso di sola navigazione — lascerebbe la North Star senza il rilievo che la parola *North Star* implica, e renderebbe la prima pagina un indice.

**Che cosa chiede**: che la ripetizione sia voluta e non letta come una svista da chi revisiona.

---

## 10. Che cosa questo contratto non decide

**I colori, i caratteri, le dimensioni esatte.** Sono scelte di chi costruisce e non hanno conseguenze sulla correttezza, con **una eccezione**: le tre marcature della dispersione di §5.1 — quadrante, `is_high_zero_genre`, resto — devono restare distinguibili fra loro, perché la distinzione porta informazione e non decorazione.

**L'ordine in cui le pagine vengono costruite.** È fissato dai task, non da qui.

**Che cosa accade se una visuale non regge davanti allo schermo.** È l'unica cosa che questo disegno non poteva verificare a tavolino (`research.md`, sezione finale), ed è la ragione per cui gli scostamenti sono previsti dal disegno invece di essere trattati come difetti. Uno scostamento si annota **mentre accade** e si elenca nell'esito con la propria ragione (`F9`, `FR-023`); non si ricostruisce a memoria alla fine.
