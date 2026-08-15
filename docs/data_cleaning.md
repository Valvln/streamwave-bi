# Trasformazioni dei dati — feature 003

**Data**: 2026-08-11 | **Feature**: 003 Data Cleaning & ETL | **Pipeline**: [`scripts/build_datasets.py`](../scripts/build_datasets.py)

## 1. Perché questo documento esiste

I dataset che questa feature produce **non sono nel repository**. `data/processed/` è escluso da git, e lo è per scelta: gli output non si versionano, si versiona la pipeline che li produce. Chiunque abbia i dati di origine può rigenerarli identici; chi non li ha non può nemmeno aprirli.

Ne discende il compito di questo documento. Non racconta cosa c'è nei file: **dichiara ogni decisione presa sui dati**, con la ragione che la motiva, l'effetto che produce misurato in righe o valori, e il riferimento all'osservazione del profilo su cui poggia. È, insieme alla pipeline e a [`reports/cleaning_report.json`](../reports/cleaning_report.json), l'unico modo in cui una decisione di trattamento diventa contestabile da chi non possiede i dati.

Il documento **cita** i numeri, non li possiede. Ogni valore che segue vive in uno dei due<!--#--> artefatti versionati — il profilo della feature 002 e il rendiconto di questa — e un comando eseguibile verifica che il testo e gli artefatti non siano divergenti.

## 2. Come si legge, e che cosa il controllo garantisce

Ogni numero di questo documento porta un marcatore invisibile nel Markdown reso e leggibile nel sorgente. Ne esistono quattro<!--#--> forme, dichiarate in [`specs/003-data-cleaning-etl/contracts/output-datasets.md`](../specs/003-data-cleaning-etl/contracts/output-datasets.md) §3:

| Forma | Che cosa dichiara |
|---|---|
| ancora a un identificativo | il numero è un valore di uno dei due<!--#--> artefatti, e il controllo lo confronta carattere per carattere |
| numerale in lettere ancorato | come sopra, per i numeri che in prosa si scrivono a parole |
| letterale fra apici inversi | il testo è membro di un elenco registrato negli artefatti |
| marcatore di non-misurato | il numero **non è un valore di questi artefatti**, e chi scrive lo dichiara |

`python3 scripts/check_audit_coherence.py` risolve ogni ancora, confronta, e **fallisce** se trova una divergenza, un riferimento inesistente o una quantità priva di entrambi i marcatori. Non richiede `data/raw/`: confronta artefatti tutti versionati.

**Che cosa il controllo copre.** Ogni cifra e ogni numerale del documento. Nessuna quantità può comparire senza che chi scrive abbia dichiarato se sia un valore misurato o no: è la differenza rispetto al documento della feature 002, dove le quantità non marcate producevano un avviso e tre<!--#--> affermazioni errate sono passate proprio da lì.

**Che cosa il controllo non copre**, e va detto perché estendere la copertura sposta il confine invece di eliminarlo:

- **una dichiarazione falsa di non-misurato.** Nessun meccanismo impedisce di marcare come non misurato un numero che invece lo è. Contro questo esiste la revisione in contesto pulito, non il controllo;
- **le affermazioni qualitative senza contenuto numerico.** «La deduplicazione è priva di perdita» è verificata dalla pipeline come invariante, non da questo controllo;
- **i numeri che sono fatti dichiarati altrove.** La copertura temporale dei due<!--#--> cataloghi — 2021<!--#--> e 2022<!--#--> — è stabilita dalla constitution fra le fonti dati ammesse, non è un valore di questi artefatti, e porta il marcatore di non-misurato con la fonte citata in prosa;
- **le soglie.** Una soglia scelta da questa feature è una stipulazione, non un fatto sui dati. Dove è possibile la si ancora al proprio valore registrato fra le convenzioni del rendiconto; dove ricorre in prosa porta il marcatore di non-misurato.

## 3. Le cinque decisioni ereditate

Cinque<!--#--> decisioni arrivavano dalle revisioni in contesto pulito delle feature 001 e 002. Nessuna poteva essere rinviata: stanno tutte a monte di calcoli che le feature successive faranno. Sono chiuse qui, con la ragione.

### D1 — Le tracce a popolarità zero sono incluse e marcate

*Divergenza 6 della revisione 001.* Le opzioni erano tre<!--#-->: escluderle, includerle, o riportarle come misura di fragilità accanto alla mediana.

**La decisione**: la pipeline non elimina alcuna riga per il valore di popolarità. Aggiunge un indicatore esplicito e pubblica la quota di zeri per genere insieme ai dati.

**La ragione**: zero<!--#--> è un valore ammissibile di un indice definito su 0-100<!--#-->, non un valore mancante. Nulla nei dati distingue una traccia genuinamente non popolare da una non misurata, e non esiste alcun criterio osservabile per farlo. Escluderle significherebbe scegliere per conto di una misura che questa feature non possiede. La forma adottata è anche la sola che non pregiudica le altre due<!--#-->: l'indicatore consente a valle sia di includere sia di escludere, mentre l'eliminazione in pipeline sarebbe irreversibile.

**L'effetto**: 15.844<!--@CL.SP.zero.rows.after--> righe marcate, il 13,95%<!--@CL.SP.zero.pct.after--> del totale alla grana coppia traccia-genere. Nessuna riga e' rimossa per il valore di popolarita': e' verificato come invariante a ogni esecuzione.

**L'obbligo che ne discende**: qualunque misura del framework calcolata sulla popolarità **deve pubblicare accanto al proprio valore la quota di zeri del segmento su cui è calcolata**. Vale in particolare per `BQ2-K1`. La feature 007 eredita l'obbligo, non la scelta.

### D2 — I titoli privi di durata sono riparati, non eliminati e non imputati

*Divergenza 8 della revisione 001, parte dati.*

**Il fatto su cui la decisione poggia.** Il profilo registra 3<!--@NF.duration.missing--> titoli privi di durata e 3<!--@NF.rating.out_of_domain.rows--> titoli con classificazione per età fuori dal dominio dichiarato, i cui valori sono `66 min`<!--@catalogs.netflix_rating_out_of_domain-->, `74 min`<!--@catalogs.netflix_rating_out_of_domain--> e `84 min`<!--@catalogs.netflix_rating_out_of_domain-->. Una verifica sui dati di origine mostra che si tratta **degli stessi titoli**: `s5542`<!--@catalogs.netflix_repaired_titles-->, `s5795`<!--@catalogs.netflix_repaired_titles--> e `s5814`<!--@catalogs.netflix_repaired_titles-->. La corrispondenza è totale in entrambe le direzioni — non esiste una riga senza durata con classificazione valida, né una riga con classificazione a forma di durata che abbia una durata.

Sono tre<!--#--> special di stand-up dello stesso artista. Non è un caso sparso: è la firma di un errore di caricamento su un lotto omogeneo, e rende l'ipotesi dello scivolamento di colonna più solida della sola coincidenza numerica.

**La decisione**, in tre<!--#--> movimenti:

1. il valore che si trova nel campo di classificazione e soddisfa la forma di una durata in minuti, su una riga il cui campo durata è vuoto, viene **spostato** nel campo durata;
2. il campo di classificazione di quelle righe è posto a **mancante**, perché il valore corretto è andato perso nella fonte e inventarlo sarebbe l'unica cosa peggiore che perderlo;
3. le righe restano nel dataset e portano un indicatore che le distingue.

**La ragione, e perché i due<!--#--> movimenti restano distinti.** Porre a mancante un valore fuori da un dominio già dichiarato e versionato è un controllo di dominio: meccanico, verificabile, ripetibile da chiunque. Spostare il valore nel campo durata è ammissibile solo perché la regola che lo autorizza è altrettanto meccanica — forma sintattica riconosciuta sul campo di partenza, campo di destinazione vuoto — e perché la sua area di applicazione è verificabile a priori. Non è una congettura sull'intenzione della fonte: è l'unica lettura che rende conto simultaneamente di due<!--#--> anomalie che coincidono riga per riga.

Nel codice le due<!--#--> operazioni sono due<!--#--> funzioni separate, e non per pulizia formale: è su quella distinzione che l'intera decisione si difende, e collassarle l'avrebbe resa invisibile.

**Il vincolo che rende la riparazione difendibile.** La regola dichiara in anticipo quante righe si aspetta di toccare, e la pipeline **si ferma con errore** se ne tocca un numero diverso. Una regola di riparazione senza un limite dichiarato al proprio raggio d'azione è una regola che, su una versione diversa della fonte, riscrive dati senza che nessuno se ne accorga.

**L'effetto**: 3<!--@CL.NF.duration.repaired.rows--> righe riparate. Il controllo di dominio, applicato dopo, non trova alcun residuo: 0<!--@CL.NF.rating.out_of_domain.blanked--> valori ulteriori posti a mancante. Nessuna riga e' eliminata, e la pipeline lo verifica confrontando il conteggio con il profilo.

**La regola generale che resta in piedi**: fuori da questo caso, nessuna durata mancante viene imputata e nessuna riga viene eliminata perché priva di durata. Un titolo senza durata resta un titolo del catalogo: eliminarlo cambierebbe il denominatore della North Star `BQ1-K1`. L'esclusione dai calcoli spetta alla misura, che deve dichiarare il proprio denominatore.

**Cosa resta fuori**: il segno della differenza di `BQ1-K2` è della feature 007 e questo documento non lo tocca.

### D3 — I totali di catalogo si calcolano sulla grana traccia

*Divergenza 6 della revisione 002.* La nota di correzione in §5.2 di [`docs/business_case.md`](business_case.md) lascia aperte due<!--#--> letture aritmetiche dell'espressione «sovrastima di circa un quinto»: 21,28%<!--@SP.id.duplicate_share--> come quota di righe che ripetono una traccia già presente, 27,03%<!--@SP.id.inflation--> come eccesso del totale non deduplicato su quello corretto.

**La decisione**: si adotta la seconda lettura, `SP.id.inflation`, come misura dell'errore che si commette calcolando un totale di catalogo senza deduplicare.

**La ragione**: le due<!--#--> quote rispondono a domande diverse e solo una delle due<!--#--> è una sovrastima. La prima è una proprietà del file — quanta parte delle sue righe è ridondante — e ha per denominatore le righe, cioè la grandezza sbagliata. Una sovrastima si misura invece rispetto al valore giusto: quanto il totale errato eccede quello corretto. Il denominatore è il totale sulle tracce distinte, ed è la seconda lettura. Che sia anche quella che la parola *sovrastima* suggerisce più naturalmente lo aveva già osservato la nota di §5.2.

**La conseguenza sul testo**: «circa un quinto» descrive correttamente la prima lettura e non la seconda. La nota in loco che dichiara la lettura adottata va apposta in §5.2 del business case, ed è debito di questa feature.

**L'effetto**: sul dato trasformato l'errore vale 26,53%<!--@CL.SP.track.inflation.after-->, non più 27,03%<!--@SP.id.inflation-->, perché la deduplicazione di coppia ha spostato il numeratore. È il valore da citare d'ora in avanti.

**L'obbligo che ne discende**: ogni totale di catalogo musicale si calcola su `spotify_tracks.csv`. Le due<!--#--> grane restano entrambe disponibili, ma la loro intercambiabilità è chiusa: nessuna misura può scegliere in silenzio.

### D4 — I generi a forte concentrazione di zeri sono quelli oltre metà delle righe

*Divergenza 8 della revisione 002.* Nessuna soglia era fissata. Il profilo conta 4<!--@SP.pop.zero.genres_over_60--> generi oltre il 60%<!--#-->, ma quella soglia è un'etichetta di un conteggio, non un criterio adottato, e `country` — al 58,70%<!--@SP.pop.zero.by_genre.country--> — cadeva dentro o fuori a seconda di dove la si metteva.

**La decisione**: il criterio è una quota di righe a popolarità zero<!--#--> superiore a `50.0`<!--@conventions.zero_share_threshold_pct-->%.

**La ragione**: il 60%<!--#--> è un numero tondo, cioè nessuna ragione. La soglia adottata è invece quella oltre la quale un genere smette di essere descrivibile dalla propria mediana di popolarità: se più della metà delle righe di un genere vale zero<!--#-->, il valore centrale di quel genere è zero<!--#-->, qualunque cosa facciano le altre. Non è una proprietà stimata, è una proprietà della definizione di mediana. La soglia non nasce da un giudizio sull'ampiezza accettabile di una massa di zeri, ma dalla misura che a valle la consumerà.

**Perché non le mediane, che sarebbero il criterio più diretto.** Una mediana di popolarità per genere è a un passo da `BQ2-K1`, e «segmento» non è ancora definito — è la feature 005. La quota di zeri è l'osservazione equivalente che resta dentro il perimetro di questa feature. La scelta costa chiarezza espositiva e la si paga volentieri.

**L'effetto**: 7<!--@CL.SP.zero.high_genres.count--> generi marcati su 114<!--@SP.genre.count-->, elencati e commentati in §7. `country` cade **dentro**.

### D5 — Le affermazioni derivate sono esse stesse valori

*Divergenze 1 e 2 della revisione 002.* La revisione aveva trovato tre<!--#--> affermazioni errate nel documento di audit, e tutte e tre<!--#--> erano confronti o rapporti costruiti sui valori del profilo — «il secondo campo più incompleto», «tre<!--#--> delle sei<!--#--> corrispondenze», «un dominio quattro<!--#--> volte più ricco». Nessun valore del profilo le conteneva e nessun controllo le verificava.

**La decisione — la regola**, adottata per gli artefatti di questa feature e proposta come regola generale del progetto:

> Un confronto, una graduatoria, un rapporto o una differenza costruiti su valori misurati **sono essi stessi valori misurati**. O esistono nell'artefatto con un identificativo proprio e vengono ancorati come qualunque altro numero, o non si scrivono. Non esiste la categoria intermedia dell'affermazione che «si ricava dai numeri già pubblicati e quindi non ha bisogno di fonte».
>
> Tre<!--#--> corollari operativi:
> **(a)** superlativi, ordinali e moltiplicatori riferiti a fatti misurati sono ammessi solo se ancorati a un valore che li sostiene;
> **(b)** i numerali scritti in lettere sono vietati per qualunque fatto misurato;
> **(c)** il controllo di coerenza **fallisce** — non avvisa — su un numerale non ancorato in posizione di fatto misurato.

**La ragione**: delle tre<!--#--> strade che la revisione indicava — vietare in prosa, calcolare nell'artefatto, restringere l'enunciato della garanzia — le prime due<!--#--> non sono alternative ma le due<!--#--> facce della stessa regola, e la terza da sola non impedisce il ripetersi dell'errore. Un divieto senza il canale del calcolo obbligherebbe a scrivere documenti che non possono dire nulla di comparativo; il calcolo senza divieto lascerebbe aperta la scorciatoia. Insieme funzionano perché spostano il costo dove serve: chi vuole scrivere «il campo più incompleto» deve prima farlo calcolare, e quel passaggio è esattamente ciò che nella 002 non è stato pagato.

**Come il corollario (c) è realizzato.** Non facendo indovinare al controllo se un numerale sia «in posizione di fatto misurato» — sarebbe l'euristica sulla prosa italiana che la 002 aveva giustamente vietato — ma **spostando l'onere su chi scrive**, con il marcatore di non-misurato di §2. L'autore sa in un istante ciò che nessuna regola posizionale distingue. Il costo è una scrittura in più per ogni numerale; il ricavo è un controllo che ferma invece di elencare.

**Il perimetro del vincolo di tracciabilità**, che è la divergenza 1: copre i valori numerici, i valori letterali degli elenchi e delle convenzioni versionate, e le affermazioni derivate. Non copre le affermazioni qualitative prive di contenuto numerico. Il confine è dichiarato in §2 e non altrove.

**Che cosa resta da fare a chi legge questa regola.** Vale per gli artefatti di questa feature. Portarla in `CLAUDE.md` perché valga per ogni documento successivo è atto di governance e non appartiene a questa feature.

## 4. Le nove decisioni di trattamento

Nove<!--#--> decisioni sono applicate ai dati. Cinque<!--#--> sono quelle ereditate di §3; quattro<!--#--> sono emerse dalla ricognizione sui dati reali condotta prima di scrivere la pipeline. Ciascuna è dichiarata qui con il proprio effetto misurato.

| # | Decisione | Origine | Effetto | Marcatura sui dati |
|---|---|---|---|---|
| 1<!--#--> | popolarità zero<!--#--> conservata e marcata | D1 | 15.844<!--@CL.SP.zero<!--#-->.rows.after--> righe | `is_popularity_zero` |
| 2<!--#--> | riparazione dello scivolamento di colonna | D2 | 3<!--@CL.NF.duration.repaired.rows--> righe | `is_repaired_duration` |
| 3<!--#--> | classificazione fuori dominio posta a mancante | D2 | 0<!--@CL.NF.rating.out_of_domain.blanked--> valori residui | — |
| 4<!--#--> | totali di catalogo sulla grana traccia | D3 | 26,53%<!--@CL.SP.track.inflation.after--> di errore evitato | — |
| 5<!--#--> | soglia dei generi a forte concentrazione di zeri | D4 | 7<!--@CL.SP.zero.high_genres.count--> generi | `is_high_zero_genre` |
| 6<!--#--> | deduplicazione della grana coppia | ricognizione | 450<!--@CL.SP.pair.removed_rows--> righe rimosse | — |
| 7<!--#--> | scelta della popolarità fra repliche discordi | ricognizione | 720<!--@CL.SP.track.popularity_conflict.tracks--> tracce | `has_conflicting_popularity` |
| 8<!--#--> | conversione delle date in forma ISO 8601 | ricognizione | 8.797<!--@CL.NF.date_added.converted--> valori | — |
| 9<!--#--> | normalizzazione del solo campo delle categorie | ricognizione | 1<!--@CL.NF.multivalue.fields_normalized--> campo su 4<!--#--> | — |

Le quattro<!--#--> emerse dalla ricognizione meritano la loro ragione per esteso.

### 6 — La grana coppia traccia-genere non era unica

L'audit della 002 aveva stabilito che la riga della fonte non è la traccia: 114.000<!--@SP.shape.rows--> righe per 89.741<!--@SP.id.distinct--> identificativi distinti. Ne concludeva che esistono due<!--#--> grane non intercambiabili. La ricognizione mostra che **la seconda di quelle due<!--#--> non è unica nemmeno lei**: 444<!--@CL.SP.pair.duplicate_pairs--> coppie traccia-genere compaiono più di una volta, per 450<!--@CL.SP.pair.removed_rows--> righe eccedenti. È un fatto che né la 001 né la 002 registrano.

La deduplicazione è quindi obbligatoria, perché la pipeline verifica la grana di ogni output come invariante e su questa la verifica sarebbe fallita. Ed è **priva di perdita**: le repliche di una stessa coppia sono identiche su ogni attributo. Non lo si assume — la pipeline lo verifica prima di scartare, e si ferma se trovasse repliche discordi, perché in quel caso scartarle butterebbe via informazione.

**L'effetto**: da 114.000<!--@SP.shape.rows--> a 113.550<!--@CL.SP.pair.rows.after--> righe.

### 7 — La deduplicazione a traccia non è priva di perdita

Vedi §6 del documento per la quantificazione. La regola è: dove le repliche di una traccia discordano, la grana deduplicata conserva il **massimo osservato**.

### 8 — Le date erano una trappola di determinismo

Il campo delle date di aggiunta contiene forme testuali inglesi, e 88<!--@CL.NF.date_added.trimmed--> valori portano uno spazio iniziale. Il problema non è lo spazio, che è banale da normalizzare: è che la conversione ovvia — la funzione di libreria che interpreta il nome del mese — **dipende dal locale del sistema**. Funziona sotto locale inglese e fallisce sotto locale italiano.

Una pipeline che la usasse produrrebbe risultati diversi su macchine diverse, cioè violerebbe il determinismo in un modo che **non si manifesta sulla macchina di chi la scrive** e si manifesta su quella di chi la riesegue. È il caso peggiore, perché rompe esattamente la promessa che la feature esiste per mantenere. La conversione usa una mappa dei mesi esplicita, registrata fra le convenzioni del rendiconto.

**L'effetto**: 8.797<!--@CL.NF.date_added.converted--> valori convertiti, 10<!--@CL.NF.date_added.missing--> lasciati vuoti e non imputati.

### 9 — Si normalizza un campo multi-valore su quattro

Il campo delle categorie del catalogo video è multi-valore, e produce una tabella propria: 19.323<!--@CL.NF.category.assignments--> assegnazioni su 42<!--@CL.NF.category.distinct--> categorie. Ma sono multi-valore anche `country`<!--@catalogs.netflix_multivalue_not_normalized-->, `cast`<!--@catalogs.netflix_multivalue_not_normalized--> e `director`<!--@catalogs.netflix_multivalue_not_normalized-->, che restano stringhe di sorgente.

La ragione è che la normalizzazione ha un consumatore dichiarato solo nel primo caso: `BQ1-K1` conta titoli per categoria, ed è il caso in cui i conteggi non sono sommabili. Gli altri 3<!--@CL.NF.multivalue.fields_not_normalized--> campi non alimentano alcuna misura del framework, e normalizzarli produrrebbe tre<!--#--> tabelle senza lettore.

**Va detto come limite, non come dettaglio**: chi in futuro volesse contare titoli per paese incontrerà lo stesso problema di sommabilità, non risolto.

## 5. I valori che cambiano

È la sezione che protegge dal citare un numero del profilo credendo che descriva il dato trasformato.

Il profilo della 002 contiene 1.030<!--@CL.meta.profile_values.total--> valori. Dopo la trasformazione 421<!--@CL.meta.profile_values.changed--> **non valgono più**. Ogni singolo caso è registrato nel blocco `denominators` del rendiconto, con l'identificativo del profilo che non vale più, quello che lo sostituisce, e la ragione della differenza.

La completezza non è una promessa di chi scrive: la pipeline **ricalcola** i valori del profilo sul dato trasformato e li confronta uno per uno. Ciò che coincide non entra fra i denominatori; ciò che differisce ci entra da solo. Il ricalcolo riusa le funzioni del profiler della 002 invece di riscriverle, così una differenza segnalata è una differenza nei dati e mai nell'aritmetica di chi la calcola.

Il conto dei valori del profilo torna per intero, ed è verificato come invariante a ogni esecuzione:

| Categoria | Valori |
|---|---:|
| riconfrontati sul dato trasformato | 1.002<!--@CL.meta.profile_values.compared--> |
| senza controparte — descrivono la colonna indice esclusa | 22<!--@CL.meta.profile_values.without_counterpart--> |
| fuori perimetro — la trasformazione non può toccarli | 6<!--@CL.meta.profile_values.out_of_scope--> |
| **totale** | 1.030<!--@CL.meta.profile_values.total--> |

Senza quell'invariante l'affermazione sarebbe vera soltanto per i valori che qualcuno si fosse ricordato di confrontare, e nessuno potrebbe accorgersi dei dimenticati. Alla prima esecuzione ne ha fermati sei<!--#-->.

### I cambiamenti che chi legge deve conoscere

| Valore del profilo | Prima | Dopo | Perché |
|---|---:|---:|---|
| film con durata valorizzata | 6.128<!--@NF.num.movie_duration_min.count--> | 6.131<!--@CL.NF.duration.movie.count.after--> | la riparazione di D2 |
| titoli privi di durata | 3<!--@NF.duration.missing--> | 0<!--@CL.NF.recalc.duration.missing--> | la riparazione di D2 |
| classificazioni mancanti | 4<!--@NF.miss.rating.count--> | 7<!--@CL.NF.rating.missing.after--> | la riparazione di D2 svuota tre<!--#--> valori |
| valori distinti di classificazione | 17<!--@NF.card.rating--> | 14<!--@CL.NF.recalc.card.rating--> | i tre<!--#--> fuori dominio non compaiono più |
| date distinte | 1.767<!--@NF.card.date_added--> | 1.714<!--@CL.NF.recalc.card.date_added--> | vedi sotto |
| righe del catalogo musicale | 114.000<!--@SP.shape.rows--> | 113.550<!--@CL.SP.recalc.shape.rows--> | la deduplicazione di coppia |
| quota di righe ripetute | 21,28%<!--@SP.id.duplicate_share--> | 20,97%<!--@CL.SP.recalc.id.duplicate_share--> | la deduplicazione di coppia |
| eccesso del totale non deduplicato | 27,03%<!--@SP.id.inflation--> | 26,53%<!--@CL.SP.recalc.id.inflation--> | la deduplicazione di coppia |
| righe a popolarità zero<!--#--> | 16.020<!--@SP.pop.zero<!--#-->.count--> | 15.844<!--@CL.SP.recalc.pop.zero<!--#-->.count--> | la deduplicazione di coppia |
| quota di righe a popolarità zero<!--#--> | 14,05%<!--@SP.pop.zero<!--#-->.pct--> | 13,95%<!--@CL.SP.recalc.pop.zero<!--#-->.pct--> | la deduplicazione di coppia |

**Le date distinte meritano una spiegazione, perché il caso è istruttivo.** Il profilo ne conta 1.767<!--@NF.card.date_added-->; dopo la normalizzazione sono 1.714<!--@CL.NF.recalc.card.date_added-->. Il profilo non sbaglia: descrive correttamente il dato grezzo, dove una data con spazio iniziale e la stessa data senza **sono due<!--#--> stringhe diverse**. Ma chi legga quel numero come «quante date distinte esistono nel catalogo» sovrastima. Non è un errore del profilo, è un'ambiguità che solo la trasformazione rende visibile.

**Le quote di zeri per genere cambiano su 78<!--#--> generi su 114<!--@SP.genre.count-->**, e qui va segnalata una distinzione che il lettore incontrerà. Il confronto avviene sul valore, non sulla forma con cui lo si scrive: dei 78<!--#--> generi che cambiano, solo su 48<!--#--> la differenza è visibile anche alla seconda cifra decimale. Sugli altri il valore si sposta oltre. Chi confrontasse le tabelle stampate ne conterebbe 48<!--#-->; il blocco dei denominatori ne registra 78<!--#-->, perché usa il criterio stretto.

## 6. La perdita della deduplicazione

La deduplicazione alla grana traccia **non è priva di perdita**, a differenza di quella di coppia, e dichiararlo senza quantificarlo non sarebbe dichiararlo.

Su 89.741<!--@CL.SP.track.rows.after--> tracce distinte, 720<!--@CL.SP.track.popularity_conflict.tracks--> hanno repliche che discordano — e discordano **soltanto** sull'indice di popolarità. Ogni altro attributo, incluse tutte le audio feature, coincide fra le repliche di una stessa traccia. Anche questo è verificato come invariante: se il disaccordo toccasse altri attributi la regola dichiarata non li coprirebbe, e la pipeline si ferma invece di scegliere in silenzio.

**La regola**: si conserva il **massimo osservato**. È un valore effettivamente presente nella fonte; media e mediana ne produrrebbero uno che nessuna riga contiene. Fra i candidati che conservano un valore osservato — massimo, minimo, prima occorrenza — la prima occorrenza è deterministica ma arbitraria, perché dipende dall'ordine di esportazione della fonte, cioè da nulla di interpretabile. Il massimo è invece leggibile come enunciato: *la popolarità più alta che quella traccia ha registrato nel dataset*.

**L'entità della perdita.** Lo scarto fra le repliche discordi è quasi sempre trascurabile e ha una coda: 13<!--@CL.SP.track.popularity_conflict.spread_over_10--> tracce superano i dieci<!--#--> punti di scarto, e il massimo osservato è 44<!--@CL.SP.track.popularity_conflict.spread_max--> punti.

**La distorsione va dichiarata, non solo la regola.** Conservare il massimo introduce una distorsione **verso l'alto**, sistematica per costruzione ancorché minima. Chi cita un totale o una distribuzione sulla grana traccia cita anche questa regola. Le righe interessate portano un indicatore, così che una misura possa escluderle se la scelta la disturba.

**Perché non si è misurata la dispersione con una mediana.** Sarebbe stata la strada ovvia, ed è esclusa per non introdurre in questo artefatto una misura di posizione che il perimetro della feature tiene fuori. Il massimo e il conteggio della coda descrivono la stessa cosa senza aprire quella porta.

## 7. La soglia dei generi a forte concentrazione di zeri, e la sua sensibilità

I 7<!--@CL.SP.zero.high_genres.count--> generi selezionati dal criterio di D4 sono `country`<!--@catalogs.spotify_high_zero_genres-->, `iranian`<!--@catalogs.spotify_high_zero_genres-->, `jazz`<!--@catalogs.spotify_high_zero_genres-->, `latin`<!--@catalogs.spotify_high_zero_genres-->, `rock`<!--@catalogs.spotify_high_zero_genres-->, `romance`<!--@catalogs.spotify_high_zero_genres--> e `soul`<!--@catalogs.spotify_high_zero_genres-->.

**Questa lista è l'esito di un taglio, non una proprietà naturale dei dati.** La distinzione conta: una lista prodotta da un criterio si legge diversamente da una classifica, e chi la cita a valle deve sapere quale delle due<!--#--> ha in mano.

**La sensibilità della soglia.** Il genere più vicino da sotto — escluso — è al 48,45%<!--@CL.SP.zero.high_genres.nearest_below-->; il più vicino da sopra — incluso — è al 52,50%<!--@CL.SP.zero.high_genres.nearest_above-->. Nessun genere sta a un decimo di punto dal confine: attorno alla soglia c'è un margine di alcuni punti in entrambe le direzioni.

**Una constatazione, non la ragione della scelta.** La soglia scartata del 60%<!--#--> sarebbe stata più esposta: con quella, un genere sarebbe rimasto fuori per meno di un punto e mezzo. Che la soglia scelta per una ragione risulti anche la più stabile delle due<!--#--> è una circostanza favorevole verificata a posteriori, e va letta come tale — non come l'argomento che l'ha motivata, che è quello di D4.

**Le quote sono ricalcolate, non riprese dal profilo.** La deduplicazione ha spostato i denominatori, e usare le quote del profilo avrebbe selezionato l'insieme su dati che non esistono più. L'insieme selezionato risulta comunque **identico** prima e dopo la trasformazione: è una constatazione sulla robustezza del criterio, non una giustificazione della soglia.

## 8. Che cosa esce dagli output, e che cosa vi resta

Nessun campo dei due<!--#--> dataset di origine sparisce in silenzio.

**Il catalogo video** conserva tutti i suoi campi. Due<!--#--> sono riscritti — la durata è separata in due<!--#--> campi tipizzati e distinti, la classificazione per età è ripulita — e uno è convertito in forma ISO 8601. Il campo delle categorie resta come stringa di sorgente **accanto** alla tabella normalizzata: rimuoverlo obbligherebbe chi legge il solo dataset alla grana titolo a fare una giunzione per sapere di che cosa parla un titolo.

**Il catalogo musicale** perde un campo: `(colonna priva di nome)`<!--@catalogs.spotify_excluded_fields-->, che è l'indice di riga dell'esportazione della fonte e non un dato. Trasportarlo produrrebbe una colonna che invita a essere usata come chiave e che non lo è — dopo la deduplicazione non sarebbe nemmeno più contigua. I 22<!--@CL.meta.profile_values.without_counterpart--> valori del profilo che descrivono quella colonna non hanno quindi controparte, e sono elencati nel rendiconto.

**I quattro<!--#--> output.**

| File | Grana — cosa è una riga | Righe |
|---|---|---:|
| `netflix_titles.csv` | un titolo | 8.807<!--@CL.NF.titles.rows.after--> |
| `netflix_title_category.csv` | l'assegnazione di una categoria a un titolo | 19.323<!--@CL.NF.category.assignments--> |
| `spotify_track_genre.csv` | l'appartenenza di una traccia a un genere | 113.550<!--@CL.SP.pair.rows.after--> |
| `spotify_tracks.csv` | una traccia | 89.741<!--@CL.SP.track.rows.after--> |

**Regola di lettura, non negoziabile.** I due<!--#--> dataset musicali non sono intercambiabili, e nemmeno i due<!--#--> video. Sommare i conteggi per categoria **non** restituisce il numero di titoli: 19.323<!--@CL.NF.category.assignments--> assegnazioni su 8.807<!--@CL.NF.titles.rows.after--> titoli, perché un titolo appartiene a più categorie. Sommare i conteggi per genere non restituisce il numero di tracce, perché una traccia appartiene fino a 9<!--@SP.id.max_multiplicity--> generi.

Gli output **non sono versionati**. Chi possiede i dati di origine li rigenera identici e verifica di averlo fatto confrontando le impronte registrate nel rendiconto. Chi non li possiede non può aprirli: per lui esistono la pipeline, il rendiconto e questo documento.

## 9. Provenienza e confidenza

Questa feature **non introduce numeri nuovi sul mondo**. Ogni valore che produce è o un valore osservato sui dati reali, o la misura dell'effetto di una propria trasformazione.

| Famiglia di valori | Fonte | Confidenza | Criterio di attribuzione |
|---|---|---|---|
| Conteggi e quote ricalcolati sui dataset trasformati | Netflix (reale), Spotify (reale) | alta | conteggio diretto sull'output di una trasformazione dichiarata e rieseguibile |
| Effetto quantificato di una decisione di trattamento | Derivato (dati reali + regola dichiarata) | alta | la regola è meccanica, versionata, e il suo raggio d'azione è verificato dalla pipeline |
| Perdita della deduplicazione | Spotify (reale) | alta | confronto diretto fra le repliche di uno stesso identificativo |
| Insieme dei generi a forte concentrazione di zeri | Derivato (Spotify + soglia dichiarata) | **media** | il valore osservato è la quota di zeri, a confidenza alta; l'**appartenenza all'insieme** dipende da una soglia scelta da questa feature |
| Durate recuperate dalla riparazione dello scivolamento | Derivato (Netflix + regola dichiarata) | **media** | il valore è osservato nella fonte, ma la sua **attribuzione al campo durata** è un'inferenza — meccanica, verificabile e circoscritta a un raggio d'azione dichiarato, ma pur sempre un'inferenza |

**Nessun dato sintetico** viene generato in questa feature.

**Perché due<!--#--> righe a confidenza media.** Il resto della feature osserva o conta. In questi due<!--#--> casi no: fra il dato e il valore pubblicato si interpone una regola scelta qui — una soglia, un'attribuzione di campo. Sono scelte dichiarate, motivate e verificabili, e restano scelte. Marcarle come alte le renderebbe indistinguibili dai conteggi diretti, che è esattamente la confusione che il principio di provenienza esiste per impedire. Nessuna delle due<!--#--> è a confidenza bassa: entrambe poggiano su valori osservati e su regole meccaniche, e il formato a range non aggiungerebbe informazione.

**Cosa questa scala non misura.** La confidenza qualifica la solidità di un numero **rispetto al dataset da cui è calcolato**, non la sua trasferibilità a StreamWave. Fra le due<!--#--> si interpone l'assunzione che il catalogo Netflix rappresenti il catalogo di StreamWave e il dataset Spotify il mercato musicale accessibile — assunzione che resta fuori scala per costruzione, perché si applica identica a tutti i valori. Un dataset trasformato correttamente resta un dataset pubblico di terzi.

## 10. Limiti dichiarati

**Pulizia non è correttezza semantica.** La pipeline verifica forme, domini e coerenze dichiarate. Non ha modo di sapere se una durata dichiarata sia quella reale, se un genere sia attribuito correttamente, se un regista sia quello giusto. Il caso esemplare è dentro questa feature: 3<!--@NF.duration.missing--> durate finite nel campo della classificazione per età, in un campo che nessuna misura di completezza segnalava come problematico perché i valori erano **presenti**. Che quel caso sia stato trovato non autorizza a concludere che casi analoghi non esistano: autorizza a concludere il contrario.

**Copertura del dato.** Catalogo video fermo al 2021<!--#-->, catalogo musicale fermo al 2022<!--#--> — come dichiarato dalla constitution fra le fonti dati ammesse. La trasformazione non estende la copertura di un giorno. Nessuna osservazione sui dataset trasformati dice qualcosa su dinamiche successive.

**Gli output non sono ispezionabili da chi non può rigenerarli.** Non essendo versionati, non esistono per chi clona il repository senza token Kaggle. La verifica passa interamente dalla pipeline, dal rendiconto e da questo documento. Chi ha i dati confronta le impronte; chi non li ha si affida a tre<!--#--> artefatti leggibili invece che a un file che non può aprire. È un compromesso, e va dichiarato invece che attenuato.

**Non risponde a**: nessuna delle tre<!--#--> domande di business. Non contiene KPI, stime né raccomandazioni.

**Non risponde a**: quale sia il modello dati. La normalizzazione dei campi multi-valore è trasformazione sintattica, non disegno di tabelle dei fatti e di dimensioni. Chi leggesse gli output come uno schema li leggerebbe male: è la feature 005.

**Non risponde a**: quale delle due<!--#--> grane del catalogo musicale una misura debba usare, salvo il vincolo posto da D3 sui totali di catalogo.

**Non risponde a**: che cosa sia un «segmento». La marcatura dei generi di D4 è una marcatura di generi, non di segmenti: che il segmento coincida con il genere è una decisione della feature 005 che questa feature non anticipa.

**Inferenza da evitare — un dataset pulito non è un dataset rappresentativo.** La pipeline rimuove ambiguità di forma, non distorsioni di campionamento. Il catalogo musicale resta bilanciato per costruzione, e contare righe per dimensionare un segmento resta sbagliato prima di essere calcolato, esattamente come lo era prima della trasformazione.

**Inferenza da evitare — la deduplicazione non è priva di perdita.** Vedi §6. Il valore conservato è osservato; la scelta di quale conservare no.

**Inferenza da evitare — la marcatura di uno zero<!--#--> non è un giudizio sulla traccia.** L'indicatore dice che l'indice di popolarità di quella riga vale zero<!--#-->, non che la traccia sia irrilevante. Nulla nei dati distingue una traccia non popolare da una non misurata.

**Inferenza da evitare — l'insieme dei generi di §7 è l'esito di un taglio.** La soglia è scelta e motivata, e la lista che ne esce va letta come tale.
