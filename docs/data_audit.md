# Data Audit — profilo dei due dataset reali

> **Cosa è questo documento**: la descrizione di com'è fatto il dato su cui poggerà tutto il resto del progetto. Descrive, non corregge e non giudica. Non contiene KPI, non risponde a nessuna delle tre domande di business, e non dice se i dati siano buoni: dice cosa contengono, dove sono incompleti e cosa questo vincola per le feature successive.

## 1. Inquadramento

Il progetto usa due cataloghi pubblici reali: il **catalogo video** `netflix_titles.csv`, proxy del catalogo attuale di StreamWave, e il **catalogo musicale** `spotify_tracks_dataset.csv`, proxy del mercato musicale accessibile. È l'assunzione A1 del [business case](business_case.md#-a1--i-dati-di-riferimento-sono-proxy-non-streamwave), e vale per ogni riga di questo documento.

I due file non sono versionati e vanno ricostruiti con `scripts/download_data.sh`. Il blocco `sources` del profilo ne registra nome, dimensione in byte e impronta `sha256`: è lì che si verifica di stare guardando gli stessi dati, e non in questo documento.

**Perché questo documento esiste.** La feature precedente ha citato numerosi fatti su questi dati — completezza dei campi, identificativi distinti, struttura del campionamento, concentrazione degli zeri — che esistevano soltanto come prosa: nessuno script li rigenerava. Il lettore doveva prenderli sulla fiducia. Era il rilievo R8 della [revisione in contesto pulito](../specs/001-business-case-kpi/review.md), e finché restava aperto il principio II della constitution non era soddisfatto per quei valori.

**Come si legge.** I valori misurati di questo documento sono prodotti da [`scripts/profile_data.py`](../scripts/profile_data.py) e vivono in [`reports/data_profile.json`](../reports/data_profile.json), che ne è l'**unica fonte di verità**. Il documento li cita, non li possiede. Ogni valore citato porta accanto a sé un'ancora — un commento HTML nella forma `<!--@identificativo-->`, invisibile nel testo reso e leggibile aprendo il sorgente del file — e un comando eseguibile verifica che testo e profilo non siano divergenti:

```bash
python3 scripts/profile_data.py          # rigenera il profilo (richiede data/raw/)
python3 scripts/check_audit_coherence.py # verifica documento ↔ profilo (non lo richiede)
```

Il secondo comando funziona anche su una copia del repository **priva** dei dati di origine, che non sono versionati e richiedono un token Kaggle: è il motivo per cui l'artefatto del profilo è versionato insieme al documento.

**Che cosa il controllo copre, e che cosa no.** Copre tre forme: i valori scritti in cifre, confrontati carattere per carattere con la forma di visualizzazione registrata nel profilo; i numerali scritti in lettere, confrontati con il valore numerico; i letterali fra apici inversi — nomi di categoria, di genere, valori fuori dominio — verificati come membri dell'elenco corrispondente. **Non copre** ciò che non è ancorato, e per costruzione non può accorgersi di un'affermazione che *avrebbe dovuto* esserlo: segnala come avviso ogni quantità non marcata, ma la decisione se marcarla resta di chi scrive. Un esito verde certifica le ancore, non l'intero documento — e questa distinzione è nata da una revisione indipendente che, sfruttando esattamente quella zona d'ombra, ha trovato tre affermazioni errate mentre il comando dichiarava tutto coerente.

### Una nota per chi legge le due feature in sequenza

Il [business case](business_case.md) dichiara di non contenere risultati e classifica ogni numero che vi compare come input. Questo documento è quasi soltanto numeri. Non è una contraddizione: quel divieto era **locale a quel documento**, che definiva il metro e non poteva quindi contenere misure. Non è un principio generale del progetto. Ciò che vale sempre è il principio I — ogni numero dichiara fonte e confidenza — ed è applicato qui in §7.

## 2. Il catalogo video

### 2.1 Forma

Il catalogo contiene 8.807<!--@NF.shape.rows--> titoli descritti da 12<!--@NF.shape.fields--> campi, di cui 6.131<!--@NF.type.movie--> film e 2.676<!--@NF.type.tvshow--> serie. Gli identificativi di titolo distinti sono 8.807<!--@NF.shape.distinct_ids-->, tanti quanti le righe: nessun identificativo compare due volte.

### 2.2 Completezza

| Campo | Valori mancanti | Quota |
|---|---|---|
| `director` | 2.634<!--@NF.miss.director.count--> | 29,91%<!--@NF.miss.director.pct--> |
| `country` | 831<!--@NF.miss.country.count--> | 9,44%<!--@NF.miss.country.pct--> |
| `cast` | 825<!--@NF.miss.cast.count--> | 9,37%<!--@NF.miss.cast.pct--> |
| `date_added` | 10<!--@NF.miss.date_added.count--> | 0,11%<!--@NF.miss.date_added.pct--> |
| `rating` | 4<!--@NF.miss.rating.count--> | 0,05%<!--@NF.miss.rating.pct--> |
| `duration` | 3<!--@NF.miss.duration.count--> | 0,03%<!--@NF.miss.duration.pct--> |
| `show_id` | 0<!--@NF.miss.show_id.count--> | 0,00%<!--@NF.miss.show_id.pct--> |
| `type` | 0<!--@NF.miss.type.count--> | 0,00%<!--@NF.miss.type.pct--> |
| `title` | 0<!--@NF.miss.title.count--> | 0,00%<!--@NF.miss.title.pct--> |
| `release_year` | 0<!--@NF.miss.release_year.count--> | 0,00%<!--@NF.miss.release_year.pct--> |
| `listed_in` | 0<!--@NF.miss.listed_in.count--> | 0,00%<!--@NF.miss.listed_in.pct--> |
| `description` | 0<!--@NF.miss.description.count--> | 0,00%<!--@NF.miss.description.pct--> |

I campi senza alcun valore mancante sono sei<!--@NF.miss.complete_fields-->, e il profilo copre tutti e dodici<!--@NF.shape.fields--> i campi. La ricerca della feature precedente ne documentava nove: `show_id`, `title` e `cast` non vi comparivano. Fra i tre, `cast` è quello con più valori mancanti — 825<!--@NF.miss.cast.count-->, che ne fanno il **terzo** campo più incompleto del catalogo, dopo `director` e `country`.

### 2.3 Le categorie

Le categorie distinte sono 42<!--@NF.cat.count-->, e il campo è **multi-valore**: un titolo ne porta più d'una. Le assegnazioni titolo-categoria sono 19.323<!--@NF.cat.assignments-->, cioè 2,19<!--@NF.cat.per_title.mean--> categorie per titolo in media.

**Ne discende che i conteggi per categoria non sono sommabili.** Sommare i titoli delle 42<!--@NF.cat.count--> categorie darebbe 19.323<!--@NF.cat.assignments-->, non 8.807<!--@NF.shape.rows-->: si conterebbe più volte lo stesso titolo. È la stessa trappola che sul lato musicale produce la doppia granularità di §3.3, e va dichiarata ogni volta che un conteggio per categoria compare accanto a un totale di catalogo.

### 2.4 Quante categorie hanno contenuto musicale dichiarato

È la domanda del rilievo **R11** della revisione, e non è una curiosità: da essa dipende la confidenza della North Star del progetto. Se le categorie a contenuto musicale fossero più d'una, sceglierle sarebbe una **mappatura interpretativa**, e `BQ1-K1` non potrebbe più reggere la confidenza alta che il business case le attribuisce.

**Il criterio applicato**, registrato nel profilo sotto `conventions.music_terms`: una categoria ha contenuto musicale dichiarato se il suo nome contiene uno fra `music`<!--@conventions.music_terms-->, `musical`<!--@conventions.music_terms-->, `concert`<!--@conventions.music_terms-->, `song`<!--@conventions.music_terms-->, `sing`<!--@conventions.music_terms-->, `opera`<!--@conventions.music_terms--> e `sound`<!--@conventions.music_terms-->. Il criterio è deliberatamente più largo del necessario: se avesse selezionato più categorie, lo avremmo saputo.

**L'esito**: le categorie a contenuto musicale dichiarato sono 1<!--@NF.cat.music.count-->, ed è `Music & Musicals`<!--@catalogs.netflix_categories_musical-->, con 375<!--@NF.cat.music_musicals.titles--> titoli distinti. Nessuna delle altre 41<!--@NF.cat.non_music.count--> etichette contiene un riferimento a musica, concerti, canto o suono.

**La conseguenza, e da chi viene.** Il fatto osservato si ferma alla riga precedente: le categorie che soddisfano il criterio dichiarato sono una sola. Ciò che ne segue non è una descrizione del dato ma una valutazione della misura, e questo documento la riporta soltanto perché la propria specifica gliela chiede — il rilievo R11 andava chiuso qui o da nessuna parte. La riporto quindi marcandola per quello che è: **poiché non c'è alcuna selezione da compiere fra categorie, non si interpone mappatura né strato interpretativo fra la fonte e la misura, e il presupposto su cui `BQ1-K1` fonda la propria confidenza alta risulta verificato.** Il giudizio finale sulla confidenza appartiene a chi possiede la misura, non a chi profila i dati.

Resta un disallineamento **di testo**, non di misura: §3 del business case descrive il contenuto misurato come "musical, documentari musicali, concerti, film sulla musica" — quattro tipologie — mentre la misura legge una sola etichetta. Concerti e documentari musicali entrano nel conteggio soltanto se la fonte li ha collocati lì, e il profilo non permette di affermarlo. La correzione della descrizione non appartiene a questa feature: è debito testuale, assegnato dalla [roadmap](roadmap.md#debito-della-feature-001) a un momento precedente alla feature 007. Qui è registrato e basta.

### 2.5 Un campo valorizzato e sbagliato

Il campo della classificazione per età contiene 17<!--@NF.card.rating--> valori distinti. Di questi, 14<!--@NF.rating.in_domain.values--> sono classificazioni per età vere e proprie; gli altri 3<!--@NF.rating.out_of_domain.values--> sono **durate** — `66 min`<!--@catalogs.netflix_rating_out_of_domain-->, `74 min`<!--@catalogs.netflix_rating_out_of_domain--> e `84 min`<!--@catalogs.netflix_rating_out_of_domain--> — una per titolo, per un totale di 3<!--@NF.rating.out_of_domain.rows--> titoli interessati. È uno scivolamento di campo nella fonte.

Il campo interessato è **uno**, e le righe sono tre<!--@NF.rating.out_of_domain.rows-->: quei tre valori non sono mancanti, sono presenti e fuori dominio. Nessuna misura di completezza li segnala — il campo risulta anzi fra i più completi del catalogo, con appena 4<!--@NF.miss.rating.count--> valori mancanti su 8.807<!--@NF.shape.rows-->. È l'esempio concreto del limite dichiarato in §8: completezza non è correttezza.

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

Gli anni di uscita vanno dal 1925<!--@NF.num.release_year.min--> al 2021<!--@NF.num.release_year.max-->, con mediana 2017<!--@NF.num.release_year.median--> e primo quartile 2013<!--@NF.num.release_year.q1-->: metà dei titoli è uscita dal 2017<!--@NF.num.release_year.median--> in poi e tre quarti dal 2013<!--@NF.num.release_year.q1--> in poi. Nessuna osservazione di questo documento riguarda ciò che è accaduto dopo l'anno più recente.

## 3. Il catalogo musicale

### 3.1 Forma

Il catalogo contiene 114.000<!--@SP.shape.rows--> righe descritte da 21<!--@SP.shape.fields--> campi.

Il **primo campo è privo di nome**: è l'indice di riga della fonte, sopravvissuto all'esportazione. Ha 114.000<!--@SP.card.unnamed--> valori distinti e 0,00%<!--@SP.miss.unnamed.pct--> di valori mancanti, cioè è una numerazione progressiva integra. Non porta informazione e non va confuso con l'identificativo di traccia. Il profilo lo documenta invece di ignorarlo: FR-019 vieta di escludere un campo in silenzio, e un campo non profilato resta indistinguibile da un campo dimenticato.

### 3.2 Completezza

I campi mancanti sono concentrati in una sola riga: 1<!--@SP.miss.artists.count--> valore mancante per `artists`, 1<!--@SP.miss.album_name.count--> per `album_name`, 1<!--@SP.miss.track_name.count--> per `track_name`. Tutti gli altri campi, incluse tutte le audio feature, sono completi.

### 3.3 La riga non è la traccia

È il ritrovamento che vincola il maggior numero di misure a valle, fra quelle elencate in §5.

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
| minimo | 0,0<!--@SP.num.popularity.min--> |
| primo quartile | 17,0<!--@SP.num.popularity.q1--> |
| mediana | 35,0<!--@SP.num.popularity.median--> |
| media | 33,2<!--@SP.num.popularity.mean--> |
| terzo quartile | 50,0<!--@SP.num.popularity.q3--> |
| massimo | 100,0<!--@SP.num.popularity.max--> |

Le righe con indice pari a zero sono 16.020<!--@SP.pop.zero.count-->, il 14,05%<!--@SP.pop.zero.pct--> del totale. Non sono distribuite uniformemente: i generi con oltre il 60% di righe a zero sono 4<!--@SP.pop.zero.genres_over_60-->.

La tabella che segue riporta i **sei generi con la quota più alta**, non i generi sopra una soglia: il criterio è dichiarato perché due dei sei stanno sotto il 60% e senza la regola il taglio sarebbe arbitrario. Il profilo contiene la quota di tutti e 114<!--@SP.genre.count--> i generi.

| Genere | Quota a zero | Sopra il 60% |
|---|---|---|
| `jazz` | 68,10%<!--@SP.pop.zero.by_genre.jazz--> | sì |
| `iranian` | 65,60%<!--@SP.pop.zero.by_genre.iranian--> | sì |
| `romance` | 63,60%<!--@SP.pop.zero.by_genre.romance--> | sì |
| `soul` | 61,10%<!--@SP.pop.zero.by_genre.soul--> | sì |
| `latin` | 58,80%<!--@SP.pop.zero.by_genre.latin--> | no |
| `country` | 58,70%<!--@SP.pop.zero.by_genre.country--> | no |

Gli ultimi due mancano la soglia per poco più di un punto, e distano fra loro un decimo di punto: qualunque decisione a valle che tratti diversamente il quarto e il quinto genere di questa lista poggia su una differenza che il dato non sostiene.

I generi interamente a zero sono 0<!--@SP.pop.zero.genres_fully_zero-->: nessun genere è privo di segnale, ma in quattro<!--@SP.pop.zero.genres_over_60--> casi la maggioranza delle righe lo è.

**Conseguenza**: una mediana per genere è trascinata verso il basso proprio nei generi più penalizzati. Questo documento **non decide** se quelle righe vadano incluse, escluse o riportate a parte: è la divergenza 6 della revisione, assegnata alla feature 003. Le conta e le localizza.

> **⚠️ Nota di adozione — 2026-08-11, feature 003.** La divergenza 8 della revisione di questo documento chiedeva con quale criterio si selezioni l'insieme dei generi «a forte concentrazione di zeri», osservando che nessuna soglia era fissata e che `country` cadeva dentro o fuori a seconda di dove la si mettesse. La feature 003 ha fissato il criterio, e l'esito **non coincide con questa tabella**.
>
> **Il criterio adottato**: quota di righe a popolarità zero superiore al `50.0`<!--@conventions.zero_share_threshold_pct-->%, non al 60%. La ragione non è di comodo ed è quella per cui la soglia è difendibile: oltre metà delle righe a zero, la mediana di popolarità di quel genere è zero qualunque cosa facciano le altre righe. Non è una proprietà stimata, è una proprietà della definizione di mediana — e lega la soglia alla misura che a valle la consumerà invece che a un numero tondo.
>
> **L'insieme che ne esce sono 7<!--@CL.SP.zero.high_genres.count--> generi**: `country`<!--@catalogs.spotify_high_zero_genres-->, `iranian`<!--@catalogs.spotify_high_zero_genres-->, `jazz`<!--@catalogs.spotify_high_zero_genres-->, `latin`<!--@catalogs.spotify_high_zero_genres-->, `rock`<!--@catalogs.spotify_high_zero_genres-->, `romance`<!--@catalogs.spotify_high_zero_genres--> e `soul`<!--@catalogs.spotify_high_zero_genres-->. `country` cade **dentro**, e con esso `latin` e `rock`, che questa tabella escludeva o non elencava. Il conteggio di 4<!--@SP.pop.zero.genres_over_60--> generi qui sopra resta corretto **per la soglia del 60%**, che non è più il criterio adottato.
>
> **Le quote vanno ricalcolate, non riprese da qui.** La trasformazione ha rimosso 450<!--@CL.SP.pair.removed_rows--> righe ridondanti dalla grana coppia traccia-genere, e le quote di zeri cambiano su 78<!--@CL.SP.zero.by_genre.changed--> dei 114<!--@SP.genre.count--> generi — su 48<!--@CL.SP.zero.by_genre.changed_visible--> la differenza è visibile anche alla seconda cifra decimale. Le quote di questa tabella restano vere sui dati di origine e non descrivono più `data/processed/`.
>
> **Sulla frase «distano fra loro un decimo di punto»**: resta vera sui dati di origine, ma non vale più come argomento sulla fragilità del taglio, perché il taglio non passa più fra quei due generi. Sulla soglia adottata il genere più vicino da sotto è al 48,45%<!--@CL.SP.zero.high_genres.nearest_below-->, cioè a diversi punti dal confine. Fonti: [`reports/cleaning_report.json`](../reports/cleaning_report.json), identificativi `CL.SP.zero.high_genres.count`, `CL.SP.zero.high_genres.nearest_below` e `catalogs.spotify_high_zero_genres`; decisione e ragione per esteso in [`docs/data_cleaning.md`](data_cleaning.md) §3, D4, e §7.

### 3.6 Durata e assi di mood

La durata mediana di una riga è 212,9<!--@SP.duration.median_s--> secondi. Esiste 1<!--@SP.duration.zero--> riga con durata dichiarata pari a zero: è un valore degenere, contato e non corretto.

I tre assi di mood su cui il framework costruisce il confronto fra i due cataloghi sono **completi**: `energy` ha 0<!--@SP.mood.energy.missing--> valori mancanti, `valence` 0<!--@SP.mood.valence.missing-->, `danceability` 0<!--@SP.mood.danceability.missing-->. Le loro mediane sono rispettivamente 0,6850<!--@SP.num.energy.median-->, 0,4640<!--@SP.num.valence.median--> e 0,5800<!--@SP.num.danceability.median-->.

## 4. Le due tassonomie non si agganciano per nome

I generi musicali il cui nome ricorre in almeno una categoria video sono 6<!--@X.genre_lexical.count-->, il 5,26%<!--@X.genre_lexical.share--> dei generi: `anime`<!--@catalogs.genre_lexical_matches-->, `british`<!--@catalogs.genre_lexical_matches-->, `children`<!--@catalogs.genre_lexical_matches-->, `comedy`<!--@catalogs.genre_lexical_matches-->, `kids`<!--@catalogs.genre_lexical_matches--> e `spanish`<!--@catalogs.genre_lexical_matches-->.

**La regola di confronto**, registrata nel profilo sotto `conventions.lexical_rule`: il nome del genere musicale, normalizzato in minuscolo, compare come sottostringa nel nome di almeno una categoria video. Il valore **non esiste senza la sua regola**: una regola per token esatti ne troverebbe quattro invece di sei, perché `kids` e `spanish` vivono dentro `Kids' TV` e `Spanish-Language TV Shows`, dove apostrofo e trattino spezzano il token.

**Cosa questo valore non dice.** Descrive i **vocabolari di etichette** dei due cataloghi, non la corrispondenza dei loro contenuti. La feature precedente osservava che alcune delle corrispondenze sono coincidenze di lingua o di pubblico di destinazione anziché di contenuto — è un giudizio interpretativo sulle etichette, non un valore misurato, e questo profilo non lo rigenera né lo quantifica: chi volesse usarlo deve rifarlo con un criterio dichiarato. La stessa feature ha già escluso il matching lessicale come piano di confronto fra i due cataloghi (decisione D1): questo numero lo documenta, non lo riabilita.

## 5. Cosa i dati permettono di costruire

Per ciascuna delle otto misure del framework, se i campi che la alimentano esistono e con quale completezza. **È una constatazione sui campi, non un giudizio sulla misura**: dire che un campo esiste ed è completo non è dire che la misura che vi poggia sia buona.

| Misura | I campi che la alimentano | Stato |
|---|---|---|
| `BQ1-K1` `music_adjacent_catalog_share` | categorie del catalogo video, identificativo di titolo | **presenti e completi**. Una sola categoria musicale (§2.4), nessuna selezione da compiere |
| `BQ1-K2` `format_duration_gap` | durata dei film in minuti, durata delle tracce | **presenti**, con 3<!--@NF.duration.missing--> titoli privi di durata e 1<!--@SP.duration.zero--> riga a durata zero. Il lato serie resta fuori per incompatibilità di unità (§2.6) |
| `BQ1-K3` `mood_profile_overlap` | tre assi di mood sul lato musicale; profilo di mood sul lato video | **presenti solo su un lato**. Le audio feature sono complete; il lato video **non ha alcun campo di mood**, e la tabella di corrispondenza che lo supplisce non è nei dati: è la feature 006 |
| `BQ2-K1` `segment_demand_index` | indice di popolarità, genere | **presenti e completi**; la concentrazione di zeri descritta in §3.5 riguarda i valori del campo, non la sua presenza |
| `BQ2-K2` `segment_catalog_affinity` | come `BQ1-K3` | **presenti solo su un lato**, stessa dipendenza dalla tabella di corrispondenza |
| `BQ2-K3` `segment_entry_priority` | deriva da `BQ2-K1` e `BQ2-K2` | eredita lo stato dei due |
| `BQ3-K1` `premium_tier_adoption_rate` | comportamento di abbonamento | **assente**. Il censimento dei campi non trova visioni, ascolti, sessioni o abbonamenti |
| `BQ3-K2` `arpu_uplift` | ricavi, prezzi | **assente**. Nessun campo economico esiste in nessuno dei due cataloghi |

L'ultima riga chiude una questione per constatazione anziché per assunzione: che l'intera terza domanda debba poggiare su dati simulati non è una scelta di comodo, è la conseguenza del fatto che nessuno dei 12<!--@NF.shape.fields--> campi del catalogo video né dei 21<!--@SP.shape.fields--> del catalogo musicale contiene un comportamento o un ricavo.

## 6. Divergenze rispetto alla feature 001

Il profilo confronta automaticamente ogni valore rigenerato con l'affermazione corrispondente della feature precedente. Le affermazioni sottoposte a confronto sono quattordici<!--@X.claims_001.total-->: dodici<!--@X.claims_001.coincide--> coincidono, una<!--@X.claims_001.diverge--> diverge e una<!--@X.claims_001.ambiguo--> è sotto-determinata, cioè non confrontabile finché non si dichiara quale lettura adotti. Le ultime due sono registrate qui, e gli artefatti della 001 hanno ricevuto una nota di correzione che affianca il testo originale senza sostituirlo.

### D1 — «18 valori» per la classificazione per età

**Dove**: [`specs/001-business-case-kpi/research.md`](../specs/001-business-case-kpi/research.md), tabella di completezza del catalogo video.

**Affermato**: 18 valori distinti. **Rigenerato**: 17<!--@NF.card.rating-->.

**Causa**: la differenza è la definizione di valore mancante. Il profilo conta i valori distinti **non mancanti** secondo la convenzione dichiarata; il conteggio della 001 includeva anche il valore vuoto, che non è una classificazione ma la sua assenza. Nessuno dei due è sbagliato in aritmetica: uno dei due è sbagliato come descrizione di un dominio.

**Perché conta più della cifra**: dei 17<!--@NF.card.rating--> valori, solo 14<!--@NF.rating.in_domain.values--> sono classificazioni per età (§2.5). Descrivere il campo come avente 18 valori attribuisce al dominio quattro valori che non ha.

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

**Inferenza da evitare — la distribuzione del campione non è la distribuzione del mercato.** Ogni genere musicale ha esattamente 1.000<!--@SP.genre.rows_max--> righe perché così è stato campionato (§3.4). Contare le righe di un genere misura il campionamento, non l'importanza di quel genere sul mercato. Un dimensionamento costruito sui conteggi restituirebbe lo stesso valore per ogni genere, qualunque sia il genere.

**Inferenza da evitare — completezza non è correttezza.** Un campo valorizzato al 100% è un campo senza valori mancanti, non un campo con valori giusti. I 3<!--@NF.rating.out_of_domain.rows--> titoli con una durata nel campo della classificazione per età (§2.5) sono valorizzati e sbagliati: nessuna misura di completezza li segnala.

**Inferenza da evitare — la corrispondenza lessicale non è corrispondenza di contenuto.** §4 conta quante etichette coincidono come stringhe sotto una regola dichiarata. Non dice che i contenuti corrispondano, e non riabilita un piano di confronto che la feature precedente ha già scartato.
