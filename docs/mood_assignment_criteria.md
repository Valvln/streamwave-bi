# Criterio di assegnazione del profilo di mood alle categorie video

Questo documento dichiara **che cosa significa** ciascun valore dei tre<!--#--> assi di mood quando è assegnato a una categoria del catalogo video, e **su quale base** si assegna. È il metro contro cui ogni riga di `dim_category_mood` può essere contestata, ed è l'unico ammesso.

---

## Nota di provenienza — questo documento precede ogni valore

Scritto il **2026-08-20**, nella feature `006-content-taxonomy-bridge`, come **passo 1 dei quattro** che la decisione D1 della sua [spec](../specs/006-content-taxonomy-bridge/spec.md) impone in quest'ordine: criterio, proposta di un modello, verifica indipendente, congelamento. L'ordine è esso stesso il presidio, e vale solo se è verificabile: il commit che introduce questo file **non contiene alcun valore della tabella, nemmeno di prova**, e precede in history git sia `data/curated/dim_category_mood_proposal.json` sia `data/curated/dim_category_mood.json`.

La ragione per cui l'ordine conta più di quanto sembri: un criterio scritto dopo che i valori esistono è indistinguibile, a lettura, da un criterio scritto prima — salvo che nella history. Chi vuole verificare che questo documento non sia stato adattato ai numeri che giustifica ha un solo modo, e non è leggerlo:

```
git log --follow --oneline docs/mood_assignment_criteria.md data/curated/dim_category_mood.json
```

Il piano che colloca questo passo è [`specs/006-content-taxonomy-bridge/plan.md`](../specs/006-content-taxonomy-bridge/plan.md); la decisione di processo che lo rende obbligatorio — `DA-1`, presa dalla regia il 2026-08-19 — è trascritta qui sotto.

**Sulla marcatura.** Questo documento non è fra quelli che `scripts/check_audit_coherence.py` verifica, e la ragione è nel piano (T7 della ricerca): al momento del suo commit la tabella che dovrebbe ancorare non esiste ancora, per costruzione. Usa comunque la grammatica di [`convenzioni-marcatura.md`](convenzioni-marcatura.md) sui sei identificativi di ancoraggio e sui nomi di categoria, perché sono esattamente i punti che chi verifica deve poter risolvere contro un artefatto invece di doverli accettare sulla parola.

---

## La decisione di processo — `DA-1`, 2026-08-19

*Presa dalla regia prima che la `006` fosse aperta, e trascritta qui il 2026-08-29 perché è la fonte della regola che questo documento esegue. Era rimasta fino a quel giorno nel piano di lavoro, che non è un artefatto pubblicato.*

**La questione.** Il piano iniziale prevedeva un componente che costruisse la tabella di corrispondenza generi → mood con un modello linguistico. Due strade: un LLM che **propone** le 42<!--#--> righe, con revisione riga per riga e versionamento di prompt, modello e data; oppure una tabella curata interamente a mano. Da decidere non era solo quale strada, ma se la prima fosse compatibile con la **decisione D1 della `001`**, che aveva respinto a verbale l'approccio a modello perché introduce «un modello non spiegabile a un board».

**La risoluzione: un LLM propone, con il criterio scritto prima.** La compatibilità con `D1` si chiude, e la ragione va scritta perché è ciò che distingue una decisione riaperta da una aggirata. `D1` respingeva l'estrazione del tono dal campo `description` per due motivi — un modello non spiegabile a un board, e lo sfondamento del vincolo di giornata. Il primo non si applica qui, per tre<!--#--> differenze che non sono di grado:

- **la scala.** Là erano 8.807<!--#--> titoli, un output che nessuno verifica riga per riga. Qui sono 42<!--#--> categorie per tre<!--#--> assi, cioè 126<!--#--> numeri, che una persona controlla in una seduta;
- **la posizione del modello.** Là il modello sarebbe stato *dentro la pipeline*, e rieseguire l'analisi avrebbe significato rieseguirlo. Qui produce una **prima stesura**, l'esito si congela in una tabella versionata, e **nessuno script chiama mai il modello**. È la forma del benchmark della `004`: un passaggio non riproducibile il cui esito è congelato, con la derivazione a valle deterministica. Il principio V la ammette già;
- **che cosa arriva al lettore.** Una tabella contestabile riga per riga. Da dove vengono i numeri è una questione di provenienza, non di opacità.

Il secondo motivo di `D1` non decide in nessuna direzione: costruire 126<!--#--> valori a mano e revisionarne 126<!--#--> proposti sono costi dello stesso ordine, e nessuna delle due strade è stata scelta per rapidità.

**L'obiezione che regge non è l'opacità, è l'ancoraggio.** La tabella è l'unico strato interpretativo del progetto e porta tre<!--#--> KPI su otto<!--#-->. Se un modello propone i valori, il lavoro del revisore scivola da autore a **ratificatore**, e chi rilegge 126<!--#--> numeri plausibili si ancora a quelli che ha davanti. È lo stesso meccanismo per cui nella `002` tre<!--#--> affermazioni derivate erano passate sotto un controllo verde: nessuno le aveva ricalcolate perché sembravano giuste.

**Il presidio è l'ordine dei passi.** Il criterio di assegnazione si scrive e **si committa da solo, prima che qualunque valore esista** — è ciò che la nota di provenienza qui sopra dichiara e che la history git rende verificabile. Ne discende una misura che altrimenti non esisterebbe: **quante righe la revisione ha spostato rispetto alla proposta**. Se ne sposta zero non è un successo, è un ritrovamento, e va dichiarato come tale.

**Che cosa la feature doveva produrre, in ordine**: il criterio, committato da solo; poi la proposta del modello, con prompt, modello e data versionati; poi la revisione riga per riga contro il criterio, con il conteggio degli spostamenti; poi la tabella congelata in un artefatto versionato, che nessuno script rigenera.

### La governance della tabella

Quattro<!--#--> domande, quattro<!--#--> risposte, decise insieme a `DA-1`.

**Chi la costruisce**: la sessione della `006`, sul criterio che ha scritto per primo. **Chi la approva**: Valerio, sull'esito della revisione in contesto pulito, che riceve la sola tabella più il criterio e nient'altro. **Con quale criterio si contesta una riga**: quello scritto al primo passo — una contestazione è legittima se lo cita, e altrimenti è un'opinione sul mood di un genere, che non è contestabile perché non è verificabile. È la regola che §7 di questo documento applica.

**Se le revisioni invalidino i valori già pubblicati**: sì, e il presidio è meccanico e non di buon senso. La tabella porta un **numero di versione**, e ogni valore pubblicato che ne dipende — `BQ1-K3`, `BQ2-K2`, `BQ2-K3` — dichiara su quale versione è stato calcolato. Il contratto di versione vive in §5 di [`content_taxonomy_bridge.md`](content_taxonomy_bridge.md).

### Come è andata — eseguita dalla `006` il 2026-08-20

I quattro<!--#--> passi sono stati eseguiti nell'ordine prescritto e la cronologia `git` lo dimostra: criterio `0d950e6`, proposta `acf18c1`, tabella congelata `57c4781`. La misura richiesta esiste e vale **2<!--#--> celle su 126<!--#-->** al congelamento, pubblicata come `MOOD.review.changes_count` — poi 3<!--#-->, dopo il chore del 2026-08-21 descritto nelle note in loco a §2 e §5.

**Due cose sono andate diversamente da come la decisione le aveva previste, ed entrambe migliorano il disegno.**

La prima: `DA-1` dava per scontato che la verifica producesse **contestazioni a singole righe**, e basta. Ne ha prodotta una seconda specie — i difetti del **criterio**, che una contestazione di riga non può contenere perché non riguarda una cella ma il metro. La tabella ha quindi un campo che il piano non prevedeva, `criterion_findings`.

La seconda: «se ne sposta zero non è un successo, è un ritrovamento». Il valore è 2<!--#-->, non 0<!--#-->, quindi il caso previsto non si è dato — ma la ragione per cui era stato previsto si è data lo stesso: un conteggio basso non distingue una proposta aderente al criterio da un criterio che non dà appigli.

**Ciò che la decisione aveva sottovalutato**: che il criterio potesse essere difettoso. Tutto il presidio è costruito sull'ordine — il metro scritto prima dei valori — e nessuna parte di esso chiede chi verifichi il metro. La risposta pratica è stata la verifica indipendente stessa, che ha trovato tre<!--#--> difetti applicandolo; è un esito fortunato, non un presidio, e va scritto come tale. I tre<!--#--> difetti sono `CF-1`, `CF-2` e `CF-3`, e il loro esito sta in §3 di [`content_taxonomy_bridge.md`](content_taxonomy_bridge.md).

---

## Che cosa questo documento non contiene, e perché

**Nessun valore assegnato a una categoria.** Non perché sia scomodo scriverli qui, ma perché un criterio che contenesse anche una sola riga di esempio — «`Horror Movies` sta intorno a *tale* valore di positività» — smetterebbe di essere il metro e diventerebbe la prima riga della tabella, scritta prima che il processo che deve produrla sia cominciato. La legenda della scala che segue descrive **regioni**, non assegnazioni: dice che cosa significa stare in basso su un asse, non chi ci sta.

**Nessun titolo del catalogo video.** Né nome, né trama, né cast, né alcun altro attributo specifico di una riga di `dim_title` (D7 della spec, che chiude la parte generale della divergenza 5 della revisione `003`). Gli ancoraggi qui sotto si esprimono a livello di **categoria** o di **genere musicale come archetipo**. Non è un vincolo che tolga qualcosa: l'assegnazione avviene a grana categoria, e nessun passo del processo ha bisogno di guardare un titolo per decidere il mood di una categoria. Citarne uno renderebbe però più facile leggere l'assegnazione come «osservata su quegli esempi» invece che come ciò che è — un giudizio dell'analista.

---

## 1. La scala è ereditata, non decisa qui

§11 di [`data_model.md`](data_model.md) fissa che sul lato musicale i tre<!--#--> assi sono `energy`, `valence`, `danceability`, letti dalla fonte **senza alcuna normalizzazione, trasformazione o riscalamento**, sul dominio decimale `0-1`.

I tre campi del lato video vivono sulla **stessa scala e con lo stesso significato di estremo**:

| Asse | Campo lato video | Campo lato musicale | Dominio |
|---|---|---|---|
| energia | `mood_energy` | `energy` | `0-1` |
| positività | `mood_valence` | `valence` | `0-1` |
| ritmo | `mood_danceability` | `danceability` | `0-1` |

**Questo è l'obbligo che conta di più, e la ragione è che un suo errore non produce alcun sintomo.** Se il lato video fosse assegnato su una scala qualitativa a cinque livelli e poi rinormalizzato a `0-1`, oppure se `0,5` significasse «medio rispetto alle altre categorie video» invece di «ciò che `0,5` significa sul lato musicale», la distanza fra i due profili che `BQ2-K2` calcola non misurerebbe più nulla — e il numero uscirebbe comunque, dell'ordine di grandezza atteso, senza che alcun controllo di questo progetto lo intercetti. È il difetto che solo la verifica indipendente della proposta può trovare, ed è per questo che il paragrafo seguente esiste.

### Gli ancoraggi osservati sul lato musicale

Perché «stessa scala del lato musicale» sia verificabile e non un'affermazione, gli estremi si ancorano a ciò che sul lato musicale è **già misurato e già pubblicato**: la distribuzione dei tre campi sull'intero insieme delle tracce, in `reports/data_profile.json`.

| Asse | Minimo osservato | Massimo osservato |
|---|---|---|
| `energy` | 0,0000<!--@SP.num.energy.min--> | 1,0000<!--@SP.num.energy.max--> |
| `valence` | 0,0000<!--@SP.num.valence.min--> | 0,9950<!--@SP.num.valence.max--> |
| `danceability` | 0,0000<!--@SP.num.danceability.min--> | 0,9850<!--@SP.num.danceability.max--> |

Chi verifica una riga contro questo criterio risolve questi sei identificativi contro l'artefatto e confronta: è un numero pubblicato, non un giudizio a occhio.

**Due letture di questa tabella vanno tenute distinte**, perché confonderle porta a un errore di scala.

La prima: il **dominio** dei tre assi è `0-1` su entrambi i lati, ed è ciò che §11 fissa e che questo criterio eredita. Su `valence` e `danceability` il massimo *osservato* sta poco sotto il limite superiore del dominio — nessuna traccia dell'insieme tocca `1` su quei due assi — ma questo non restringe il dominio: descrive la distribuzione, non la scala.

La seconda: l'estremo alto di un asse sul lato video significa ciò che significa un valore **prossimo al massimo osservato** sul lato musicale per lo stesso asse. Assegnare `1,00` a una categoria video su `valence` è quindi ammesso dal dominio ma dichiara qualcosa di più forte di quanto qualunque traccia del catalogo musicale esprima, e va fatto solo se è ciò che si intende dire.

*(Il ritrovamento che i due massimi non sono `1,0000` è di questa feature: la fase di ricerca aveva trascritto tutti e sei gli estremi come `0` e `1`, generalizzando da `energy`. La correzione è annotata in loco in [`research.md`](../specs/006-content-taxonomy-bridge/research.md), ritrovamento F3.)*

---

## 2. Su che cosa si assegna: la categoria come etichetta, non i titoli che contiene

Una categoria del catalogo video è un'**etichetta editoriale**: dichiara la promessa che il catalogo fa a chi sceglie cosa guardare. Il profilo di mood di una categoria è il registro affettivo **che quella promessa evoca**, non la media dei titoli che vi ricadono.

La distinzione non è sottile, e determina l'assegnazione in ogni caso ambiguo:

- una categoria **eterogenea** — `Movies`<!--@catalogs.netflix_categories_normalized-->, `TV Shows`<!--@catalogs.netflix_categories_normalized--> — non riceve la media dei suoi contenuti, che sarebbe un valore calcolato su un insieme di titoli che nessuno ha misurato. Riceve il profilo che la sua etichetta comunica, che per un'etichetta generica è **centrale su tutti e tre gli assi, per assenza di segnale, non per equilibrio misurato**;
- una categoria **geografica o linguistica** — `International Movies`<!--@catalogs.netflix_categories_normalized-->, `Korean TV Shows`<!--@catalogs.netflix_categories_normalized-->, `Spanish-Language TV Shows`<!--@catalogs.netflix_categories_normalized--> — non porta un registro affettivo proprio: l'etichetta dichiara una provenienza, non un tono. Vale la stessa regola dell'etichetta generica, ed è la ragione per cui su queste categorie l'assegnazione deve restare centrale invece di inseguire uno stereotipo culturale;
- una categoria **di formato** — `Docuseries`<!--@catalogs.netflix_categories_normalized-->, `Stand-Up Comedy`<!--@catalogs.netflix_categories_normalized--> — porta il registro del formato, che è un segnale reale: un formato comico dichiara positività alta come parte della propria promessa.

**Il criterio di scelta, in una riga:** se per assegnare un valore serve immaginare quali titoli stiano nella categoria, l'assegnazione sta uscendo dal criterio.

---

### Nota in loco — 2026-08-21, chore `criterio-mood-cf1`

La verifica indipendente della proposta (`006-content-taxonomy-bridge`) ha trovato che i tre tipi sopra non sono né esaustivi né esclusivi, e che la loro combinazione con il secondo segnale di §5 li fa contraddire. Il ritrovamento è registrato come `CF-1` e `CF-2` in §3 di [`content_taxonomy_bridge.md`](content_taxonomy_bridge.md), con la ricognizione della regia del 2026-08-21 che ne ha corretto la forma.

**La contraddizione (`CF-1`).** Un'etichetta generica, geografica o linguistica riceve qui il profilo centrale «per assenza di segnale»; un'etichetta di formato episodico a durata fissa riceve da §5 una cadenza più alta. `TV Shows`, `International TV Shows`, `British TV Shows`, `Korean TV Shows` e `Spanish-Language TV Shows` sono insieme geografiche o generiche **e** episodiche a durata fissa: le due regole prescrivono valori diversi sullo stesso asse per la stessa etichetta, e nessun testo di questo documento diceva quale prevale.

**La regola che prevale, e perché.** Fra un tipo che non porta segnale (generica, geografica o linguistica, e — vedi sotto — di pubblico, di epoca o ricezione, di modo di produzione o tema quando non nominata come archetipo altrove) e un tipo che lo porta (di formato, o l'assegnazione diretta di §3-§5), **prevale il tipo che porta segnale**: l'assenza di segnale non ha nulla da opporre a un segnale reale. È la stessa lettura con cui la verifica indipendente aveva già mosso `Anime Series` e `Classic & Cult TV`, motivando che §2 non le copre e che §5 si applica quindi senza conflitto. Sulle cinque etichette sopra, la cadenza episodica di §5 prevale sulla centralità di §2.

**Il vuoto più largo (`CF-2`).** I tre tipi elencati non coprono almeno tre casi reali del catalogo: le etichette **di pubblico** (`Kids' TV`, `Children & Family Movies`, `Teen TV Shows`), **di epoca o ricezione** (`Classic Movies`, `Cult Movies`, `Classic & Cult TV`), **di modo di produzione o tema** (`Independent Movies`, `LGBTQ Movies`). Non sono un quarto, quinto e sesto tipo con una regola propria: seguono di default la stessa regola delle etichette generiche — centrali per assenza di segnale — a meno che un'etichetta della stessa famiglia non sia già nominata come archetipo diretto in §3-§5 (`Children & Family Movies` lo è, in §4) o non porti anche il segnale di formato di cui sopra, nel qual caso vale la regola di prevalenza appena dichiarata.

**Che cosa non cambia.** §3-§5 restano gli unici punti in cui un'etichetta riceve un segnale diretto per nome; questa nota non ne aggiunge. `CF-3` — che i 126 valori della proposta siano tutti multipli di 0,05, una griglia più grossolana delle due cifre decimali che §6 fissa — resta dichiarata e non corretta: questa riscrittura non introduce alcun vincolo di granularità, quindi non la rende una conseguenza.

---

## 3. Asse energia — `mood_energy`

**Che cosa misura sul lato musicale.** `energy` è l'intensità percepita di un brano: densità sonora, aggressività, spinta. Un valore basso è quiete, un valore alto è pressione continua.

**Che cosa significa assegnato a una categoria video.** Il **livello di attivazione** che l'etichetta promette a chi sceglie: quanto ci si aspetta di stare tesi, sollecitati, mossi dall'azione — indipendentemente dal fatto che l'attivazione sia piacevole o sgradevole. Un thriller e una commedia scatenata possono condividere l'energia e stare agli antipodi sulla positività: sono assi diversi e non vanno collassati.

**Su quale base si assegna.** Sul ritmo narrativo e sulla densità di eventi che l'etichetta dichiara — non sulla qualità emotiva, che è l'asse successivo.

**Ancoraggio all'estremo basso** (prossimo a `SP.num.energy.min`, 0,0000<!--@SP.num.energy.min-->): l'archetipo musicale è la musica d'ambiente — drone, ambient, campo sonoro senza percussione né sviluppo dinamico. Sul lato video l'equivalente è una categoria che promette contemplazione e non sollecitazione: `Faith & Spirituality`<!--@catalogs.netflix_categories_normalized--> è l'archetipo dell'estremo basso su questo asse.

**Ancoraggio all'estremo alto** (prossimo a `SP.num.energy.max`, 1,0000<!--@SP.num.energy.max-->): l'archetipo musicale è il metal estremo o l'EDM da picco di serata — massima densità, nessuna pausa dinamica. Sul lato video l'equivalente è una categoria la cui promessa è l'attivazione continua: `Action & Adventure`<!--@catalogs.netflix_categories_normalized--> è l'archetipo dell'estremo alto.

---

## 4. Asse positività — `mood_valence`

**Che cosa misura sul lato musicale.** `valence` è la valenza affettiva percepita: quanto un brano suona lieto o cupo, a prescindere da quanto sia intenso.

**Che cosa significa assegnato a una categoria video.** Il **tono affettivo** che l'etichetta promette: quanto ci si aspetta di uscirne sollevati o turbati. È l'asse su cui l'indipendenza dall'energia va tenuta con più cura, perché è quello su cui l'intuizione tende a confonderli.

**Su quale base si assegna.** Sull'esito emotivo che l'etichetta prefigura, non sull'intensità con cui lo prefigura.

**Ancoraggio all'estremo basso** (prossimo a `SP.num.valence.min`, 0,0000<!--@SP.num.valence.min-->): l'archetipo musicale è il funeral doom o il dark ambient — registro di lutto, nessuna risoluzione. Sul lato video l'equivalente è una categoria la cui promessa è il disagio: `Horror Movies`<!--@catalogs.netflix_categories_normalized--> è l'archetipo dell'estremo basso su questo asse, e vi sta con **energia alta**, che è precisamente il caso che dimostra l'indipendenza dei due assi.

**Ancoraggio all'estremo alto** (prossimo a `SP.num.valence.max`, 0,9950<!--@SP.num.valence.max-->): l'archetipo musicale è il pop solare o il reggae in maggiore — lietezza esplicita e senza ironia. Sul lato video l'equivalente è una categoria che promette leggerezza come proprio contenuto: `Children & Family Movies`<!--@catalogs.netflix_categories_normalized--> è l'archetipo dell'estremo alto.

---

## 5. Asse ritmo — `mood_danceability`

**Che cosa misura sul lato musicale.** `danceability` è la regolarità e la propulsione ritmica: quanto un brano ha un battito stabile e riconoscibile. Non è la velocità — §11 di [`data_model.md`](data_model.md) spiega perché l'asse non è `tempo` — ma la **prevedibilità della pulsazione**.

**Che cosa significa assegnato a una categoria video.** La **regolarità della cadenza** che l'etichetta promette: quanto la fruizione ha un passo riconoscibile e ripetuto, contro quanto procede per durate irregolari e stacchi imprevedibili. È l'asse meno intuitivo dei tre nella trasposizione, ed è quello su cui il criterio deve essere più esplicito.

**Su quale base si assegna.** Su due segnali dell'etichetta, in quest'ordine: la presenza di musica ritmica come parte dichiarata del contenuto, e la regolarità del formato — un formato episodico a durata fissa ha una cadenza più alta di un formato a durata libera.

**Ancoraggio all'estremo basso** (prossimo a `SP.num.danceability.min`, 0,0000<!--@SP.num.danceability.min-->): l'archetipo musicale è il free jazz o la musica classica a tempo libero — nessuna pulsazione stabile a cui agganciarsi. Sul lato video l'equivalente è una categoria che procede per durate e ritmi non prevedibili, senza alcuna componente ritmica dichiarata: `Documentaries`<!--@catalogs.netflix_categories_normalized--> è l'archetipo dell'estremo basso.

**Ancoraggio all'estremo alto** (prossimo a `SP.num.danceability.max`, 0,9850<!--@SP.num.danceability.max-->): l'archetipo musicale è il funk, la disco, la house — battito stabile e propulsivo come tratto costitutivo. Sul lato video l'equivalente è la sola categoria in cui la musica ritmica **è** il contenuto dichiarato: `Music & Musicals`<!--@catalogs.netflix_categories_normalized--> è l'archetipo dell'estremo alto.

### Nota in loco — 2026-08-21, chore `criterio-mood-cf1`

Il secondo segnale qui sopra — formato episodico a durata fissa → cadenza più alta — è il segnale che prevale nella regola di precedenza aggiunta in nota a §2, sulle etichette che sono insieme generiche, geografiche o linguistiche **ed** episodiche. Vedi quella nota per l'elenco delle etichette interessate e la motivazione.

---

## 6. Come si legge un valore che non sta a un estremo

Gli ancoraggi fissano i capi della scala. Fra i due, la legenda è questa — e descrive **regioni**, non assegnazioni:

| Regione | Che cosa dichiara chi assegna |
|---|---|
| prossima all'estremo basso | l'etichetta promette il polo basso dell'asse come proprio tratto **costitutivo**: toglierlo cambierebbe la categoria |
| bassa | il polo basso è il registro prevalente, ma non è ciò che definisce l'etichetta |
| centrale | l'etichetta **non porta segnale** su questo asse — è il caso delle categorie generiche, geografiche e linguistiche di §2. Non significa «equilibrio misurato fra contenuti opposti» |
| alta | il polo alto è il registro prevalente, ma non è ciò che definisce l'etichetta |
| prossima all'estremo alto | l'etichetta promette il polo alto come proprio tratto **costitutivo** |

**Due vincoli sulla forma del valore**, entrambi conseguenza di ciò che il valore è.

Il primo: si scrive con **due cifre decimali**, arrotondate `ROUND_HALF_UP`. Non è un limite tecnico — è la granularità con cui questo criterio distingue i casi. Pubblicare più cifre per un valore assegnato, non misurato, dichiarerebbe una precisione che la costruzione non ha.

Il secondo: i tre assi sono **indipendenti**. Nessuna regola lega il valore di un asse a quello di un altro sulla stessa categoria, e una coppia che sembra contraddittoria — energia alta e positività bassa — non è un errore da correggere ma spesso l'assegnazione giusta.

---

## 7. Come si contesta una riga

Una contestazione è **legittima solo se cita un punto specifico di questo documento**: un ancoraggio di §3-§5, una regola di §2, la legenda di §6, o l'obbligo di scala di §1. Una contestazione della forma «a me quella categoria sembra più cupa» non è ammessa come tale, e chi verifica la registra come non ammessa invece di agire su di essa.

Il motivo non è formale. Questo è l'unico strato interpretativo del progetto: se il metro di contestazione fosse l'opinione di chi verifica, la verifica indipendente diventerebbe una seconda assegnazione sovrapposta alla prima, e la tabella finale non avrebbe più alcun criterio dichiarato dietro di sé — avrebbe due giudizi non dichiarati, il secondo dei quali ha vinto perché è arrivato dopo.

**Che cosa il verificatore può leggere è un'altra questione, e la risposta è: tutto.** Il criterio è il **metro** con cui si contesta, non un perimetro di lettura. In particolare, chi verifica deve poter aprire `reports/data_profile.json` per risolvere i sei identificativi di §1: senza di essi l'obbligo di scala — quello che questo documento chiama l'obbligo che conta di più — non è verificabile affatto.

---

## 8. I limiti di questo criterio

**Non rende l'assegnazione riproducibile.** Due persone che applicassero questo documento alle stesse 42<!--@CL.NF.category.distinct--> categorie non otterrebbero le stesse righe. Il criterio riduce la dispersione e rende ogni scostamento **discutibile contro un testo**; non lo elimina, e non pretende di farlo.

**Non copre il caso in cui la tassonomia della fonte cambi.** Se una categoria comparisse o sparisse dal catalogo, questo documento resterebbe valido come metro ma la tabella non coprirebbe più l'insieme. Il presidio contro quel caso non è nel criterio: è il controllo meccanico che confronta le categorie della tabella congelata con quelle del catalogo e **fallisce** se divergono.

**Non autorizza a leggere il profilo di una categoria come una proprietà dei suoi titoli.** È una proprietà dell'**etichetta**, assegnata da una persona secondo questo documento. Un titolo che vi ricade non eredita quel profilo, e nessuna conclusione su un singolo contenuto discende da qui.

**Non fa salire la confidenza di nulla.** I tre KPI che leggono la tabella — `BQ1-K3`, `BQ2-K2` e, attraverso quest'ultimo, `BQ2-K3` — restano a confidenza **media** per obbligo di §15 di [`data_model.md`](data_model.md), qualunque sia la cura con cui questo criterio è stato scritto e applicato.
