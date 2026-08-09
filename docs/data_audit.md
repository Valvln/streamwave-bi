# Data Audit — profilo dei due dataset reali

> **Cosa è questo documento**: la descrizione di com'è fatto il dato su cui poggerà tutto il resto del progetto. Descrive, non corregge e non giudica. Non contiene KPI, non risponde a nessuna delle tre domande di business, e non dice se i dati siano buoni: dice cosa contengono, dove sono incompleti e cosa questo vincola per le feature successive.

## 1. Inquadramento

Il progetto usa due cataloghi pubblici reali: un **catalogo video**, proxy del catalogo attuale di StreamWave, e un **catalogo musicale**, proxy del mercato musicale accessibile. È l'assunzione A1 del [business case](business_case.md#-a1--i-dati-di-riferimento-sono-proxy-non-streamwave), e vale per ogni riga di questo documento.

**Perché questo documento esiste.** La feature precedente ha citato numerosi fatti su questi dati — completezza dei campi, identificativi distinti, struttura del campionamento, concentrazione degli zeri — che esistevano soltanto come prosa: nessuno script li rigenerava. Il lettore doveva prenderli sulla fiducia. Era il rilievo R8 della [revisione in contesto pulito](../specs/001-business-case-kpi/review.md), e finché restava aperto il principio II della constitution non era soddisfatto per quei valori.

**Come si legge.** Ogni numero di questo documento è prodotto da [`scripts/profile_data.py`](../scripts/profile_data.py) e vive in [`reports/data_profile.json`](../reports/data_profile.json), che ne è l'**unica fonte di verità**. Il documento li cita, non li possiede. Ogni valore ripreso dal profilo porta con sé un riferimento invisibile all'identificativo che lo contiene, e un comando eseguibile verifica che i due non siano divergenti:

```bash
python3 scripts/profile_data.py          # rigenera il profilo (richiede data/raw/)
python3 scripts/check_audit_coherence.py # verifica documento ↔ profilo (non lo richiede)
```

Il secondo comando funziona anche su una copia del repository **priva** dei dati di origine, che non sono versionati e richiedono un token Kaggle: è il motivo per cui l'artefatto del profilo è versionato insieme al documento.

### Una nota per chi legge le due feature in sequenza

Il [business case](business_case.md) dichiara di non contenere risultati e classifica ogni numero che vi compare come input. Questo documento è quasi soltanto numeri. Non è una contraddizione: quel divieto era **locale a quel documento**, che definiva il metro e non poteva quindi contenere misure. Non è un principio generale del progetto. Ciò che vale sempre è il principio I — ogni numero dichiara fonte e confidenza — ed è applicato qui in §7.

## 2. Il catalogo video

### 2.1 Forma

Il catalogo contiene 8.807<!--@NF.shape.rows--> titoli descritti da 12<!--@NF.shape.fields--> campi, di cui 6.131<!--@NF.type.movie--> film e 2.676<!--@NF.type.tvshow--> serie. Gli identificativi di titolo distinti sono 8.807<!--@NF.shape.distinct_ids-->: **nessun titolo è duplicato**, a differenza di quanto accade sul lato musicale.

### 2.2 Completezza

| Campo | Valori mancanti | Quota |
|---|---|---|
| `director` | 2.634<!--@NF.miss.director.count--> | 29,91%<!--@NF.miss.director.pct--> |
| `country` | 831<!--@NF.miss.country.count--> | 9,44%<!--@NF.miss.country.pct--> |
| `cast` | 825<!--@NF.miss.cast.count--> | 9,37%<!--@NF.miss.cast.pct--> |
| `date_added` | 10<!--@NF.miss.date_added.count--> | 0,11%<!--@NF.miss.date_added.pct--> |
| `rating` | 4<!--@NF.miss.rating.count--> | 0,05%<!--@NF.miss.rating.pct--> |
| `duration` | 3<!--@NF.miss.duration.count--> | 0,03%<!--@NF.miss.duration.pct--> |
| `show_id`, `type`, `title`, `release_year`, `listed_in`, `description` | 0<!--@NF.miss.title.count--> | 0,00%<!--@NF.miss.title.pct--> |

Il profilo copre **tutti e dodici** i campi. La ricerca della feature precedente ne documentava nove: `show_id`, `title` e `cast` non vi comparivano, e il terzo dei tre è il secondo campo più incompleto del catalogo dopo il regista.

### 2.3 Le categorie

Le categorie distinte sono 42<!--@NF.cat.count-->, e il campo è **multi-valore**: un titolo ne porta più d'una. Le assegnazioni titolo-categoria sono 19.323<!--@NF.cat.assignments-->, cioè 2,19<!--@NF.cat.per_title.mean--> categorie per titolo in media.

**Ne discende che i conteggi per categoria non sono sommabili.** Sommare i titoli delle 42<!--@NF.cat.count--> categorie darebbe 19.323<!--@NF.cat.assignments-->, non 8.807<!--@NF.shape.rows-->: si conterebbe più volte lo stesso titolo. È la stessa trappola che sul lato musicale produce la doppia granularità di §3.3, e va dichiarata ogni volta che un conteggio per categoria compare accanto a un totale di catalogo.

### 2.4 Quante categorie hanno contenuto musicale dichiarato

È la domanda del rilievo **R11** della revisione, e non è una curiosità: da essa dipende la confidenza della North Star del progetto. Se le categorie a contenuto musicale fossero più d'una, sceglierle sarebbe una **mappatura interpretativa**, e `BQ1-K1` non potrebbe più reggere la confidenza alta che il business case le attribuisce.

**Il criterio applicato**, registrato nel profilo sotto `conventions.music_terms`: una categoria ha contenuto musicale dichiarato se il suo nome contiene uno fra `music`, `musical`, `concert`, `song`, `sing`, `opera`, `sound`. Il criterio è deliberatamente più largo del necessario: se avesse selezionato più categorie, lo avremmo saputo.

**L'esito**: le categorie a contenuto musicale dichiarato sono 1<!--@NF.cat.music.count-->, e sono `Music & Musicals`, con 375<!--@NF.cat.music_musicals.titles--> titoli distinti. Nessuna delle altre 41<!--@NF.cat.non_music.count--> etichette contiene un riferimento a musica, concerti, canto o suono.

**La conseguenza**: `BQ1-K1` non compie alcuna selezione fra categorie. Non c'è mappatura, non c'è strato interpretativo, e la **confidenza alta regge**. La North Star sopravvive al rilievo.

Resta un disallineamento **di testo**, non di misura: §3 del business case descrive il contenuto misurato come "musical, documentari musicali, concerti, film sulla musica" — quattro tipologie — mentre la misura legge una sola etichetta. Concerti e documentari musicali entrano nel conteggio soltanto se la fonte li ha collocati lì, e il profilo non permette di affermarlo. La correzione della descrizione non appartiene a questa feature: è debito testuale, assegnato dalla [roadmap](roadmap.md#debito-della-feature-001) a un momento precedente alla feature 007. Qui è registrato e basta.

### 2.5 Un campo valorizzato e sbagliato

Il campo della classificazione per età contiene 17<!--@NF.card.rating--> valori distinti. Di questi, 14<!--@NF.rating.in_domain.values--> sono classificazioni per età vere e proprie; gli altri 3<!--@NF.rating.out_of_domain.values--> sono **durate** — `66 min`, `74 min`, `84 min` — una per titolo, per un totale di 3<!--@NF.rating.out_of_domain.rows--> titoli interessati. È un evidente scivolamento di campo nella fonte.

Il caso merita attenzione oltre la sua dimensione: quei tre campi sono **valorizzati al 100%** e contengono un dato sbagliato. Nessuna misura di completezza li segnalerebbe. È l'esempio concreto del limite dichiarato in §8: completezza non è correttezza.

### 2.6 Durate

Il campo della durata ha **formato misto**: minuti per i film, numero di stagioni per le serie. I titoli privi di durata sono 3<!--@NF.duration.missing-->, e le durate in un formato non riconosciuto sono 0<!--@NF.duration.malformed-->.

| Misura | Film (minuti) | Serie (stagioni) |
|---|---|---|
| titoli con valore | 6.128<!--@NF.num.movie_duration_min.count--> | 2.676<!--@NF.num.tvshow_seasons.count--> |
| minimo | 3,0<!--@NF.num.movie_duration_min.min--> | 1,0<!--@NF.num.tvshow_seasons.min--> |
| primo quartile | 87,0<!--@NF.num.movie_duration_min.q1--> | 1,0<!--@NF.num.tvshow_seasons.q1--> |
| mediana | 98,0<!--@NF.num.movie_duration_min.median--> | 1,0<!--@NF.num.tvshow_seasons.median--> |
| terzo quartile | 114,0<!--@NF.num.movie_duration_min.q3--> | 2,0<!--@NF.num.tvshow_seasons.q3--> |
| massimo | 312,0<!--@NF.num.movie_duration_min.max--> | 17,0<!--@NF.num.tvshow_seasons.max--> |

Le due colonne **non sono confrontabili fra loro** né con una durata musicale: convertire stagioni in minuti richiederebbe un'assunzione su numero e durata degli episodi che i dati non contengono.

### 2.7 Copertura temporale

Gli anni di uscita vanno dal 1925<!--@NF.num.release_year.min--> al 2021<!--@NF.num.release_year.max-->, con mediana 2017<!--@NF.num.release_year.median--> e primo quartile 2013<!--@NF.num.release_year.q1-->: il catalogo è **fortemente concentrato sull'ultimo decennio** della sua copertura. Nessuna osservazione di questo documento riguarda ciò che è accaduto dopo l'anno più recente.

## 3. Il catalogo musicale

### 3.1 Forma

Il catalogo contiene 114.000<!--@SP.shape.rows--> righe descritte da 21<!--@SP.shape.fields--> campi.

Il **primo campo è privo di nome**: è l'indice di riga della fonte, sopravvissuto all'esportazione. Ha 114.000<!--@SP.card.unnamed--> valori distinti e 0,00%<!--@SP.miss.unnamed.pct--> di valori mancanti, cioè è una numerazione progressiva integra. Non porta informazione e non va confuso con l'identificativo di traccia. Il profilo lo documenta invece di ignorarlo, perché un campo che nessuno ha guardato è un campo che qualcuno userà per sbaglio.

### 3.2 Completezza

I campi mancanti sono concentrati in una sola riga: 1<!--@SP.miss.artists.count--> valore mancante per `artists`, 1<!--@SP.miss.album_name.count--> per `album_name`, 1<!--@SP.miss.track_name.count--> per `track_name`. Tutti gli altri campi, incluse tutte le audio feature, sono completi.

### 3.3 La riga non è la traccia

È il ritrovamento con le conseguenze più estese sull'intero progetto.

Le righe sono 114.000<!--@SP.shape.rows-->, ma gli identificativi di traccia distinti sono 89.741<!--@SP.id.distinct-->. Gli identificativi che compaiono più di una volta sono 16.641<!--@SP.id.repeated-->, con una molteplicità massima di 9<!--@SP.id.max_multiplicity-->: la stessa traccia è assegnata a più generi, e ogni assegnazione è una riga.

Le righe eccedenti gli identificativi distinti sono 24.259<!--@SP.id.duplicate_rows-->. La stessa quantità si legge in **due modi diversi**, ed è importante non confonderli:

| Lettura | Valore |
|---|---|
| quota di righe che sono ripetizioni di una traccia già presente | 21,28%<!--@SP.id.duplicate_share--> |
| di quanto un totale non deduplicato eccede il totale sulle tracce distinte | 27,03%<!--@SP.id.inflation--> |

**Conseguenza**: esistono due granularità distinte e non intercambiabili. La **coppia traccia-genere**, che conta 114.000<!--@SP.shape.rows--> unità, serve alle analisi per genere; la **traccia deduplicata**, che ne conta 89.741<!--@SP.id.distinct-->, serve a qualunque totale di catalogo. Ogni misura deve dichiarare in quale delle due opera. È la nota metodologica §5.2 del business case, qui verificata sul dato.

### 3.4 Il campione è bilanciato per costruzione

I generi distinti sono 114<!--@SP.genre.count-->. Il numero di righe per genere assume 1<!--@SP.genre.row_counts_distinct--> solo valore: il minimo è 1.000<!--@SP.genre.rows_min--> e il massimo è 1.000<!--@SP.genre.rows_max-->.

**Conseguenza**: la distribuzione dei generi in questo catalogo è un **artefatto del campionamento**, non un fatto di mercato. Qualunque misura che dimensioni un segmento contando righe restituirebbe lo stesso valore per ogni genere. Il dimensionamento deve poggiare su una variabile che varia.

### 3.5 L'indice di popolarità e la sua massa di zeri

| Misura | Valore |
|---|---|
| primo quartile | 17,0<!--@SP.num.popularity.q1--> |
| mediana | 35,0<!--@SP.num.popularity.median--> |
| media | 33,2<!--@SP.num.popularity.mean--> |
| terzo quartile | 50,0<!--@SP.num.popularity.q3--> |
| massimo | 100,0<!--@SP.num.popularity.max--> |

Le righe con indice pari a zero sono 16.020<!--@SP.pop.zero.count-->, il 14,05%<!--@SP.pop.zero.pct--> del totale. Non sono distribuite uniformemente: i generi con oltre il 60% di righe a zero sono 4<!--@SP.pop.zero.genres_over_60-->.

| Genere | Quota a zero |
|---|---|
| `jazz` | 68,10%<!--@SP.pop.zero.by_genre.jazz--> |
| `iranian` | 65,60%<!--@SP.pop.zero.by_genre.iranian--> |
| `romance` | 63,60%<!--@SP.pop.zero.by_genre.romance--> |
| `soul` | 61,10%<!--@SP.pop.zero.by_genre.soul--> |
| `latin` | 58,80%<!--@SP.pop.zero.by_genre.latin--> |

I generi interamente a zero sono 0<!--@SP.pop.zero.genres_fully_zero-->: nessun genere è privo di segnale, ma in quattro casi la maggioranza delle righe lo è.

**Conseguenza**: una mediana per genere è trascinata verso il basso proprio nei generi più penalizzati. Questo documento **non decide** se quelle righe vadano incluse, escluse o riportate a parte: è la divergenza 6 della revisione, assegnata alla feature 003. Le conta e le localizza.

### 3.6 Durata e assi di mood

La durata mediana di una riga è 212,9<!--@SP.duration.median_s--> secondi. Esiste 1<!--@SP.duration.zero--> riga con durata dichiarata pari a zero: è un valore degenere, contato e non corretto.

I tre assi di mood su cui il framework costruisce il confronto fra i due cataloghi sono **completi**: `energy` ha 0<!--@SP.mood.energy.missing--> valori mancanti, `valence` 0<!--@SP.mood.valence.missing-->, `danceability` 0<!--@SP.mood.danceability.missing-->. Le loro mediane sono rispettivamente 0,6850<!--@SP.num.energy.median-->, 0,4640<!--@SP.num.valence.median--> e 0,5800<!--@SP.num.danceability.median-->.

## 4. Le due tassonomie non si agganciano per nome

I generi musicali il cui nome ricorre in almeno una categoria video sono 6<!--@X.genre_lexical.count-->, il 5,26%<!--@X.genre_lexical.share--> dei generi: `anime`, `british`, `children`, `comedy`, `kids`, `spanish`.

**La regola di confronto**, registrata nel profilo sotto `conventions.lexical_rule`: il nome del genere musicale, normalizzato in minuscolo, compare come sottostringa nel nome di almeno una categoria video. Il valore **non esiste senza la sua regola**: una regola per token esatti ne troverebbe quattro invece di sei, perché `kids` e `spanish` vivono dentro `Kids' TV` e `Spanish-Language TV Shows`, dove apostrofo e trattino spezzano il token.

**Cosa questo valore non dice.** Descrive i **vocabolari di etichette** dei due cataloghi, non la corrispondenza dei loro contenuti. Tre delle sei corrispondenze sono peraltro coincidenze di lingua o di pubblico di destinazione, non di contenuto. La feature precedente ha già escluso il matching lessicale come piano di confronto fra i due cataloghi (decisione D1): questo numero lo documenta, non lo riabilita.

## 5. Cosa i dati permettono di costruire

Per ciascuna delle otto misure del framework, se i campi che la alimentano esistono e con quale completezza. **È una constatazione sui campi, non un giudizio sulla misura**: dire che un campo esiste ed è completo non è dire che la misura che vi poggia sia buona.

| Misura | I campi che la alimentano | Stato |
|---|---|---|
| `BQ1-K1` `music_adjacent_catalog_share` | categorie del catalogo video, identificativo di titolo | **presenti e completi**. Una sola categoria musicale (§2.4), nessuna selezione da compiere |
| `BQ1-K2` `format_duration_gap` | durata dei film in minuti, durata delle tracce | **presenti**, con 3<!--@NF.duration.missing--> titoli privi di durata e 1<!--@SP.duration.zero--> riga a durata zero. Il lato serie resta fuori per incompatibilità di unità (§2.6) |
| `BQ1-K3` `mood_profile_overlap` | tre assi di mood sul lato musicale; profilo di mood sul lato video | **presenti solo su un lato**. Le audio feature sono complete; il lato video **non ha alcun campo di mood**, e la tabella di corrispondenza che lo supplisce non è nei dati: è la feature 006 |
| `BQ2-K1` `segment_demand_index` | indice di popolarità, genere | **presenti e completi**, con la fragilità di §3.5 |
| `BQ2-K2` `segment_catalog_affinity` | come `BQ1-K3` | **presenti solo su un lato**, stessa dipendenza dalla tabella di corrispondenza |
| `BQ2-K3` `segment_entry_priority` | deriva da `BQ2-K1` e `BQ2-K2` | eredita lo stato dei due |
| `BQ3-K1` `premium_tier_adoption_rate` | comportamento di abbonamento | **assente**. Il censimento dei campi non trova visioni, ascolti, sessioni o abbonamenti |
| `BQ3-K2` `arpu_uplift` | ricavi, prezzi | **assente**. Nessun campo economico esiste in nessuno dei due cataloghi |

L'ultima riga chiude una questione per constatazione anziché per assunzione: che l'intera terza domanda debba poggiare su dati simulati non è una scelta di comodo, è la conseguenza del fatto che nessuno dei 12<!--@NF.shape.fields--> campi del catalogo video né dei 21<!--@SP.shape.fields--> del catalogo musicale contiene un comportamento o un ricavo.

## 6. Divergenze rispetto alla feature 001

Il profilo confronta automaticamente ogni valore rigenerato con l'affermazione corrispondente della feature precedente. Su quattordici affermazioni verificate, dodici coincidono. Le due che non coincidono sono registrate qui, e gli artefatti della 001 hanno ricevuto una nota di correzione: lasciare un numero sbagliato in un documento già mergiato è peggio che modificarlo.

### D1 — «18 valori» per la classificazione per età

**Dove**: [`specs/001-business-case-kpi/research.md`](../specs/001-business-case-kpi/research.md), tabella di completezza del catalogo video.

**Affermato**: 18 valori distinti. **Rigenerato**: 17<!--@NF.card.rating-->.

**Causa**: la differenza è la definizione di valore mancante. Il profilo conta i valori distinti **non mancanti** secondo la convenzione dichiarata; il conteggio della 001 includeva anche il valore vuoto, che non è una classificazione ma la sua assenza. Nessuno dei due è sbagliato in aritmetica: uno dei due è sbagliato come descrizione di un dominio.

**Perché conta più della cifra**: dei 17<!--@NF.card.rating--> valori, solo 14<!--@NF.rating.in_domain.values--> sono classificazioni per età (§2.5). Descrivere il campo come avente 18 valori suggerisce un dominio quattro volte più ricco di quanto sia.

### D2 — «Sovrastima di circa un quinto»

**Dove**: [`docs/business_case.md`](business_case.md#52-nota-metodologica-sulle-granularità) §5.2.

**Stato**: **ambiguo**, non divergente. L'enunciato ammette due letture aritmetiche e non dichiara quale adotti.

Come quota di righe che sono ripetizioni vale 21,28%<!--@SP.id.duplicate_share-->, e "circa un quinto" è corretto. Come eccesso del totale non deduplicato sul totale corretto vale 27,03%<!--@SP.id.inflation-->, e "circa un quinto" non lo è — la seconda è però la lettura che la parola *sovrastima* suggerisce più naturalmente, perché si sovrastima rispetto al valore giusto.

**Perché non è stato risolto in un senso**: scegliere quale delle due la 001 intendesse significherebbe deciderlo al posto suo. La nota applicata al business case riporta entrambi i valori e la distinzione, senza riscrivere l'affermazione.

## 7. Provenienza e confidenza

Ogni valore di questo documento è **osservato direttamente sui dati reali**, senza mappature né assunzioni interposte: confidenza **alta** secondo il criterio della scala definita in [`docs/business_case.md`](business_case.md#6-scala-di-confidenza) §6, e formato a valore puntuale.

| Famiglia di valori | Fonte | Confidenza |
|---|---|---|
| dimensioni e completezza dei campi | catalogo video, catalogo musicale (reali) | alta |
| cardinalità e frequenze dei campi categorici | catalogo video, catalogo musicale (reali) | alta |
| duplicazione degli identificativi | catalogo musicale (reale) | alta |
| struttura del campionamento | catalogo musicale (reale) | alta |
| distribuzioni delle variabili numeriche | catalogo video, catalogo musicale (reali) | alta |
| valori sentinella e degeneri | catalogo video, catalogo musicale (reali) | alta |
| censimento delle categorie video | catalogo video (reale) | alta |
| corrispondenza lessicale fra i nomi (§4) | derivato dai due cataloghi | alta, con nota: la regola di confronto è dichiarata e meccanica, ma il valore descrive i vocabolari di etichette e non i contenuti |

### Cosa questa scala non misura

Vale integralmente la distinzione che il business case introduce in [§6](business_case.md#cosa-questa-scala-non-misura): la confidenza qualifica la solidità di un numero **rispetto al dataset da cui è calcolato**, non la sua trasferibilità a StreamWave.

Fra le due si interpone A1 — il catalogo video rappresenta il catalogo di StreamWave, quello musicale il mercato musicale accessibile — che resta fuori dalla scala per costruzione, perché si applica identica a ogni valore. **Un profilo a confidenza alta è alta sul dataset**: che il dataset descriva StreamWave dipende interamente da un'assunzione che con i dati disponibili non è verificabile.

## 8. Limiti dichiarati

**Copertura temporale.** Il catalogo video è fermo al 2021<!--@NF.num.release_year.max-->, e questo il profilo lo verifica: l'anno di uscita è un campo del dataset. Il catalogo musicale è fermo al 2022 secondo l'assunzione A2 della feature precedente, e questo il profilo **non** lo verifica: il dataset non espone alcun campo di data, quindi la sua copertura temporale resta un'affermazione presa dalla documentazione della fonte e non un fatto osservato. Il profilo è una fotografia a quelle date; nessuna sua osservazione dice qualcosa su dinamiche successive.

**Il profilo descrive i dataset, non i mercati che rappresentano.** Ogni numero qui riguarda due cataloghi pubblici specifici. Che rappresentino il mercato video e il mercato musicale è l'assunzione A1, che resta indimostrata.

**Non risponde a** nessuna delle tre domande di business. Non contiene KPI, stime né raccomandazioni: il rapporto fra i titoli musicali e il totale del catalogo, che è la formula della North Star, non compare né in questo documento né nel profilo. Il numeratore e il denominatore ci sono entrambi; il rapporto è della feature che calcolerà le misure.

**Non risponde a** come i dati vadano puliti, deduplicati o trasformati. È la feature 003.

**Non risponde a** se le righe a popolarità zero vadano incluse, escluse o riportate a parte. Le conta e le localizza; la decisione è della feature 003.

**Non risponde a** se i dati siano idonei allo scopo del progetto, oltre a quanto la feature precedente ha già stabilito. Descrivere un dataset non è approvarlo.

**Inferenza da evitare — la distribuzione del campione non è la distribuzione del mercato.** Ogni genere musicale ha esattamente 1.000<!--@SP.genre.rows_max--> righe perché così è stato campionato (§3.4). Contare le righe di un genere misura il campionamento, non l'importanza di quel genere sul mercato. Qualunque dimensionamento costruito sui conteggi è sbagliato prima di essere calcolato.

**Inferenza da evitare — completezza non è correttezza.** Un campo valorizzato al 100% è un campo senza valori mancanti, non un campo con valori giusti. I 3<!--@NF.rating.out_of_domain.rows--> titoli con una durata nel campo della classificazione per età (§2.5) sono valorizzati e sbagliati: nessuna misura di completezza li segnala.

**Inferenza da evitare — la corrispondenza lessicale non è corrispondenza di contenuto.** §4 conta quante etichette coincidono come stringhe sotto una regola dichiarata. Non dice che i contenuti corrispondano, e non riabilita un piano di confronto che la feature precedente ha già scartato.
