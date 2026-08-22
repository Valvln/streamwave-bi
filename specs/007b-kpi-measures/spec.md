# Feature Specification: Misure DAX e documento dei KPI

**Feature Branch**: `007b-kpi-measures`

**Created**: 2026-08-22

**Status**: Draft

**Input**: User description: "Implementare le 8 misure DAX del framework KPI di StreamWave BI contro gli operatori già fissati da `docs/kpi_operators.md` (feature `007a`), e pubblicare i valori calcolati in `docs/kpi_measures.md`. Sei debiti ereditati con riferimento puntuale (invarianza del numeratore della North Star, contratto di versione della tabella dei mood, D7 sugli zeri di popolarità, i tre vincoli aperti di `kpi_operators.md` §12, le issue GitHub `#7`/`#8`, l'allineamento di `business_case.md` §3). Perimetro: nessuna pagina, narrazione, Tableau, `roadmap.md`, `data/raw/`, nessuna riapertura delle decisioni della `007a`."

*(Il prompt di consegna integrale è più esteso di questa sintesi. Ogni vincolo che conteneva compare qui sotto come decisione, requisito, criterio di successo o limite dichiarato: questa spec è il testo autorevole, non il prompt.)*

---

## La domanda a cui questa spec risponde per prima

`docs/kpi_operators.md` fissa la regola; questa feature calcola il numero e lo rende difendibile. La domanda che precede ogni riga di codice non è "quanto vale il KPI" ma "come si calcola un valore quando lo strumento che dovrebbe calcolarlo — Power BI Desktop — non è raggiungibile dall'automazione". Il `.pbix` non è versionato (`data/processed/` è materiale di lavoro, principio II) e le misure DAX si scrivono in una GUI, fuori dal confine dell'automazione dichiarato dal principio V. Questa feature non aggira il vincolo: lo dichiara e sceglie la conseguenza — un artefatto riproducibile che chiunque cloni il repository può rigenerare, sullo stesso schema di `reports/data_profile.json`, `reports/cleaning_report.json` e `reports/bq3_scenarios.json`, con il testo DAX trascritto accanto come la formula da incollare nel modello quando qualcuno lo apre in Power BI Desktop.

Questa non è una scorciatoia rispetto al deliverable dichiarato in `docs/roadmap.md` — «le misure nel `.pbix` e `docs/kpi_measures.md`» — è la sola strada compatibile con un repository che chiunque possa clonare e verificare senza una licenza di Power BI e senza una VM: se Valerio verificherà poi il testo DAX contro il motore reale e un valore non torna, è un ritrovamento da dichiarare con nota in loco, non un esito che invalida silenziosamente questo documento.

---

## Le decisioni che questa feature prende

Cinque decisioni nuove, più la chiusura verificata di un'assunzione lasciata aperta dalla `007a`. Ciascuna riporta il debito che l'ha sollevata, le opzioni sul tavolo, la scelta, la ragione.

### E1 — Come si calcola un valore senza aprire Power BI: script deterministico, non simulazione

**Il contesto**: il `.pbix` materializzato esiste solo sulla macchina di Valerio (`docs/roadmap.md`, «La materializzazione, secondo tentativo»); questa sessione non vi ha accesso, e non potrebbe comunque scriverci dentro senza violare il principio V.

**Le opzioni**: (a) scrivere solo il testo DAX e lasciare che sia Valerio a eseguirlo ed a riportare i numeri; (b) scrivere uno script Python deterministico che applica esattamente le regole già fissate da `docs/data_model.md` e `docs/kpi_operators.md` sugli stessi dati che il modello consuma (`data/processed/*.csv`, `data/curated/dim_category_mood.json`), pubblicare il suo output come artefatto ancorato, e trascrivere comunque il DAX come la formula da inserire nel modello; (c) rinviare l'intera feature finché non esiste un accesso automatizzabile al motore.

**La decisione**: **(b)**. `scripts/build_kpi_measures.py`, sullo schema di `scripts/build_bq3_scenarios.py` — aritmetica in `decimal.Decimal`, mai `float`; nessuna lettura dell'orologio; due esecuzioni consecutive producono file identici — legge `data/processed/netflix_titles.csv`, `data/processed/netflix_title_category.csv`, `data/processed/spotify_tracks.csv`, `data/processed/spotify_track_genre.csv` e `data/curated/dim_category_mood.json`, e scrive `reports/kpi_measures.json` con lo stesso schema `values`/`catalogs`/`conventions`/`sources` degli altri artefatti.

**La ragione**: (a) non è riproducibile da chi clona il repository — dipende da un'esecuzione manuale su una macchina specifica, e un valore che nessuno script rigenera è un debito per principio I; (c) contraddirebbe la sequenza già decisa dalla regia, che dichiara `007b` apribile ora. (b) è l'unica opzione compatibile con un repository verificabile da fuori: il numero che il documento pubblica è quello che chiunque, eseguendo lo stesso comando sugli stessi file versionati, ottiene di nuovo.

**Il limite che la scelta introduce, dichiarato e non nascosto**: lo script applica gli operatori a `data/processed/*.csv`, che sono gli stessi file da cui il modello Power BI legge — non è un ricalcolo su dati diversi. Ma lo script **non è** il motore DAX: una differenza di comportamento fra come Power BI valuta una misura (contesto di filtro, propagazione delle relazioni) e come questo script itera sulle stesse righe è un rischio residuo che nessuna delle due parti elimina da sola. Finché quel rischio resta solo dichiarato, ogni valore di questo documento porta «calcolato da `scripts/build_kpi_measures.py`, non ancora verificato contro il motore Power BI reale» accanto alla propria ancora — ma questa feature non si ferma alla dichiarazione: **E9** chiude il rischio eseguendo il confronto, non limitandosi a scriverlo come limite permanente.

---

### E2 — La convenzione di mediana (issue `#7`): ordinamento e media dei due valori centrali, nessuna eccezione per i pari merito

**Il contesto**: issue GitHub `#7`, rilievo R5 della revisione `007a` — la mediana compare in quattro operatori (`BQ1-K1`/C1 su 42 conteggi, `BQ2-K1` sulla popolarità per segmento, `BQ2-K2` sui tre assi, `BQ2-K3` su 114 segmenti) senza che `docs/kpi_operators.md` dichiari mai la convenzione per un conteggio pari di osservazioni. Era rinviata perché nessun operatore ne dipendeva in modo bloccante; `BQ1-K2` è una differenza di due mediane e la rende necessaria ora.

**Le opzioni**: (a) media aritmetica dei due valori centrali su un conteggio pari, nessun trattamento speciale dei valori ripetuti — la convenzione da manuale di statistica; (b) valore basso dei due centrali (mediana "inferiore"); (c) valore alto dei due centrali (mediana "superiore").

**La decisione**: **(a)**. Si ordinano le osservazioni; su un conteggio dispari la mediana è il valore centrale; su un conteggio pari è la media aritmetica dei due valori centrali. Nessuna regola distinta per i valori ripetuti al centro: sono trattati come qualunque altro valore nell'ordinamento.

**La ragione**: è la definizione che qualunque lettore già conosce senza dover consultare questo documento, e nessuno dei quattro operatori ha un motivo per scostarsene — non c'è un'asimmetria dichiarata nella distribuzione di alcuna delle quattro grandezze che giustificherebbe (b) o (c). Introdurre una convenzione non standard qui sposterebbe silenziosamente ogni valore che dipende da una mediana su un conteggio pari (42 categorie, 114 segmenti sono entrambi pari) senza un guadagno dichiarabile.

**Dove si chiude**: questa decisione è scritta come **D10** in `docs/kpi_operators.md` §10 (tabella delle decisioni) e §12 (limiti dichiarati, che elimina questa voce dall'elenco dei vincoli aperti), e chiude l'issue `#7` quando il documento è aggiornato.

---

### E3 — Le righe a durata degenere entrano nella mediana di `BQ1-K2`, e la scelta si verifica per confronto

**Il contesto**: `docs/kpi_operators.md` §12, primo vincolo aperto — se la riga con `is_duration_zero = vero` (1 riga su 89.741 tracce) entri nella mediana di durata del lato musicale.

**Le opzioni**: (a) includerla, coerentemente con la decisione già presa per gli zeri di popolarità (D7: marcare e includere, mai scartare in silenzio una riga che la trasformazione ha scelto di conservare); (b) escluderla dal calcolo della mediana, dichiarando la marcatura come criterio di filtro.

**La decisione**: **(a), inclusione**. Lo script calcola comunque **entrambe** le varianti — mediana su tutte le tracce e mediana escludendo la riga marcata — e pubblica la differenza fra le due come valore ancorato accanto al risultato principale, invece di scegliere e nascondere l'alternativa scartata.

**La ragione**: è la stessa disciplina già applicata a `is_popularity_zero` (`docs/kpi_operators.md` §5.1, D7) — la trasformazione ha deciso di **conservare e marcare**, non di eliminare, e una misura scritta a valle non ha titolo a ribaltare quella decisione senza una ragione nuova che qui non esiste. Calcolare comunque la variante esclusa costa una riga di codice e rende la scelta verificabile invece che dichiarata a parole: se la differenza fra le due mediane risultasse rilevante, chi legge lo vede da un numero ancorato, non da un aggettivo.

**Dove si chiude**: `docs/kpi_operators.md` §3, sotto forma di nota che referenzia questa decisione (D11), e §12.

---

### E4 — L'asimmetria di `BQ1-K2` si dichiara con la quota di film sul catalogo video

**Il contesto**: `docs/kpi_operators.md` §12, secondo vincolo aperto — il lato video di `BQ1-K2` usa solo i film, il lato musicale l'intero catalogo, e l'asimmetria va dichiarata accanto al valore.

**La decisione**: `docs/kpi_measures.md` pubblica, accanto a `format_duration_gap`, la quota di titoli di tipo `Movie` sul totale dei titoli distinti del catalogo video (`dim_title`), calcolata dallo stesso script.

**La ragione**: è un conteggio già alla portata dello script (stessa tabella, stessa passata) e rende leggibile quanto piccola o grande sia la porzione di catalogo video effettivamente confrontata — senza introdurre alcun giudizio su quanto l'asimmetria sia "grande", che nessun operatore ha mai chiesto di produrre.

**Dove si chiude**: `docs/kpi_operators.md` §12 registra la chiusura con un riferimento a `docs/kpi_measures.md`; il valore stesso vive solo nel documento delle misure, mai negli operatori (§1 di `kpi_operators.md`: nessun valore dei KPI in quel documento).

---

### E5 — Arrotondamento e precisione di presentazione: una regola per unità di misura, non per KPI

**Il contesto**: `docs/kpi_operators.md` §12, terzo vincolo aperto — nessuna regola di arrotondamento è mai stata dichiarata per nessuna delle otto misure.

**La decisione**: `decimal.Decimal` con `ROUND_HALF_UP` esplicito (mai la modalità predefinita `ROUND_HALF_EVEN`), stessa disciplina di `scripts/build_bq3_scenarios.py`. La precisione di presentazione dipende dall'unità, non dal singolo KPI:

| Unità | Cifre pubblicate | KPI |
|---|---|---|
| quota / proporzione (`0-1`) | 4 cifre decimali | `BQ1-K1` (quota), `BQ1-K3`, quote di popolarità zero, quota di film |
| minuti | 2 cifre decimali | `BQ1-K2` |
| indice `0-100` | 1 cifra decimale | mediane di popolarità di `BQ2-K1` |
| affinità (`0-1`) | 4 cifre decimali | `BQ2-K2` |
| punteggio composito (`0-1`) | 4 cifre decimali | `BQ2-K3` |
| conteggio | intero, nessun decimale | titoli per categoria, righe |

**La ragione**: una precisione dichiarata per unità, e non scelta caso per caso, è contestabile con lo stesso argomento di `docs/data_model.md` §9 sulle colonne — una regola si discute una volta sola, un giudizio per singolo valore si discute ogni volta. Quattro cifre per le quote riflette che gli assi di mood e le distanze vivono già su una scala `0-1` con due cifre di risoluzione propria (`docs/content_taxonomy_bridge.md`, `mood_rounding`); due cifre per i minuti è la convenzione con cui si legge un orologio, non una pretesa di precisione superiore a quella della sorgente (`duration_ms` è già un numero esatto, la conversione a minuti non arrotonda per §13 di `data_model.md` — l'arrotondamento avviene solo in presentazione, dopo il calcolo della mediana su valori esatti).

**Dove si chiude**: `docs/kpi_operators.md` §12 registra la chiusura con riferimento a questa decisione (E5) e a `scripts/build_kpi_measures.py`.

---

### E6 — Issue `#8`: la riga di `D6`/`BQ2-K1` in `docs/kpi_operators.md` §11 è una nota in loco, non una riscrittura

**Il contesto**: issue GitHub `#8`, rilievo R6 della revisione `007a` — la tabella §11 di `docs/kpi_operators.md` attribuisce `D6` a `BQ2-K1` come «operatore fissato da», mentre il corpo di §5.3 dichiara esplicitamente che `D6` «non entra nella formula del KPI».

**La decisione**: `docs/kpi_operators.md` è già mergiato, quindi la correzione segue la regola di `CLAUDE.md` sugli artefatti già mergiati — nota in loco accanto alla cella, non riscrittura silenziosa. La cella riporta il valore precedente («D7, D6»), la nota dichiara data, feature `007b`, causa (contraddizione con §5.3, rilievo R6) e valore corretto («D7» soltanto, con `D6` spostata a un riferimento di inquadramento separato dalla colonna «operatore fissato da»).

**Dove si chiude**: `docs/kpi_operators.md` §11, e chiude l'issue `#8` quando il documento è aggiornato.

---

### E7 (verifica, non decisione) — L'invarianza del numeratore della North Star si esegue, non si assume più

**Il contesto**: rilievo R1 della revisione `007a`, `docs/kpi_operators.md` §2.1 (`D9.1`) — l'invarianza del conteggio di `Music & Musicals` fra dato di origine (375, `NF.cat.music_musicals.titles`) e dato trasformato è dichiarata come **assunzione**, sostenuta da fatti che non riguardano l'assegnazione di categoria riga per riga. Il documento stesso indica la chiusura: eseguire l'operatore di §2.2 (conteggio titoli per categoria sul ponte trasformato) fa uscire il confronto «quasi gratis».

**Che cosa questa feature fa**: lo script conta direttamente, su `data/processed/netflix_title_category.csv`, i titoli distinti assegnati a `Music & Musicals` e lo confronta con `375`. Non è una nuova decisione analitica — l'operatore è già scritto dalla `007a` — è l'esecuzione che l'operatore stesso prevede.

**I due esiti possibili, entrambi dichiarati in anticipo**: se il conteggio coincide con 375, l'invarianza passa da assunzione dichiarata a **fatto verificato**, e `docs/kpi_measures.md` lo dichiara con il nuovo conteggio ancorato sul dato trasformato accanto al valore di origine. Se non coincide, è un **ritrovamento**: si dichiara la divergenza con entrambi i numeri ancorati, si usa il conteggio sul dato trasformato per calcolare `music_adjacent_catalog_share` — perché è quello su cui il modello opera — e si registra la divergenza come nota in loco su `docs/kpi_operators.md` §2.1, non si nasconde scegliendo in silenzio quale dei due numeri citare.

---

### E8 (verifica, non decisione) — Il contratto di versione della tabella dei mood è già rispettato

**Il contesto**: il prompt di consegna elenca come debito l'allineamento di tre passaggi di `docs/kpi_operators.md` che citerebbero ancora la versione 1 della tabella dei mood come corrente, da correggere allineandoli alla versione 2 stabilita dal chore `criterio-mood-cf1` (2026-08-21/22).

**Che cosa questa feature ha trovato**: i tre passaggi (§4, §6, §7 di `docs/kpi_operators.md`) citano già `oggi la 2<!--@MOOD.table.version-->` — un'ancora, non un numero scritto a mano — e risolvono correttamente alla versione corrente perché il chore `criterio-mood-cf1` li aveva già corretti con nota in loco prima dell'apertura di questo branch. **Questo debito è quindi già chiuso**, e questa feature non tocca quei tre passaggi: rieseguire una correzione già fatta introdurrebbe un secondo diff sullo stesso testo senza alcun valore aggiunto. La spec lo dichiara come ritrovamento invece di eseguire un lavoro superfluo.

---

### E9 — Verifica contro il motore reale, eseguita da Valerio prima del merge

**Il contesto**: revisione della regia sulla prima versione di questa spec, 2026-08-22. La prima versione relegava il confronto fra il DAX trascritto e il motore Power BI reale a un limite dichiarato e permanente — «questa feature non ha accesso a quel motore» — e ne assegnava l'eventuale verifica alla `008a`. La regia corregge: il `.pbix` è già aperto, le misure sono otto, e il confronto costa incollare il DAX e leggere un numero. Rinviarlo significa scoprire alla `008a` un difetto che questa feature poteva trovare da sé, nel momento in cui trovarlo costa meno.

**Nota di perimetro, dalla stessa revisione**: eseguire il DAX nella GUI di Power BI Desktop non viola il principio V. Il principio colloca **l'interazione con la GUI fuori dall'automazione** — nessuno script di questa feature apre Power BI o vi scrive dentro — non fuori dal perimetro del progetto. È la stessa distinzione già applicata alla materializzazione del modello (`docs/roadmap.md`): un chore fatto a mano da Valerio, dentro il progetto, mai da uno script.

**Il passo**: Valerio, nel `.pbix` già materializzato, incolla il testo DAX trascritto in `docs/kpi_measures.md` per ciascuna delle otto misure, legge i valori che il motore restituisce, e li confronta con quelli pubblicati in `reports/kpi_measures.json`.

**I due esiti, entrambi dichiarati in anticipo**:

- **Coincidono**: il documento non pubblica più «valori calcolati da uno script, non ancora verificati contro il motore» — pubblica **valori verificati contro il motore reale**, che è una categoria diversa e più forte. Il limite dichiarato in E1 («una differenza di comportamento fra script e motore è un rischio residuo») si chiude per tutte e otto le misure, e il documento lo dichiara esplicitamente invece di lasciare il limite scritto come se fosse ancora aperto.
- **Non coincidono, su almeno una misura**: è il ritrovamento più importante che questa feature possa produrre — una differenza fra la regola scritta (`docs/kpi_operators.md`) e il comportamento del motore che la esegue davvero, o un errore nello script che nessuna lettura del codice aveva colto. Si dichiara con nota in loco sul valore in `docs/kpi_measures.md` (numero dello script, numero del motore, causa se identificabile) e si registra nel blocco di chiusura riportato prima del merge. Non si sceglie in silenzio quale dei due numeri pubblicare.

**Perché questo passo non è automatizzabile e resta comunque dentro questa feature**: nessuno script di questo repository può aprire Power BI Desktop, incollare del testo in una GUI o leggere un valore a schermo — è esattamente il confine del principio V. Ma il passo stesso — Valerio che lo esegue a mano, una volta, su otto misure già scritte — è lavoro della `007b`, non della `008a`: la `008a` costruisce pagine e navigazione sul `.pbix`, non verifica se i numeri del `.pbix` sono corretti.

**Dove vive l'esito**: `docs/kpi_measures.md` dichiara, per ciascuna misura, se il valore è «verificato contro il motore» o, in caso di divergenza non ancora risolta, «calcolato da script, verifica contro il motore in corso» — mai il secondo stato in silenzio quando il primo è già disponibile. Il riporto finale di questa feature (prima del merge) include l'esito del confronto misura per misura.

---

## Rapporto con le feature vicine

**Questa feature eredita senza riaprire**: le nove decisioni di `docs/kpi_operators.md` (D1-D9) restano quelle della `007a` — nessun operatore viene ridiscusso, solo eseguito. Le quattro derivazioni interne di `docs/data_model.md` §13 (incluso il passaggio da lungo a largo di `dim_category_mood`, con lo scarto dell'identificativo di riga che indicizza il blocco `values`, senza il quale il pivot non collassa a 42 righe) sono applicate dallo script esattamente come descritte, non ridiscusse.

**Questa feature non tocca**: `docs/roadmap.md` (regia), `data/raw/` (sola lettura, principio II), Tableau (`009`), pagine/layout/navigazione (`008a`), narrazione e limiti a schermo (`008b`).

**Questa feature include, e non lascia a valle**: la verifica del testo DAX contro un'esecuzione reale in Power BI Desktop, eseguita a mano da Valerio nel `.pbix` già materializzato, prima del merge (E9). Non è un'interazione automatizzata con la GUI — nessuno script la esegue — quindi resta dentro il confine del principio V, ed è dentro il perimetro di questa feature perché il costo di trovare ora una divergenza fra script e motore è più basso di scoprirla alla `008a`.

**Questa feature lascia a valle**: la presentazione dei 114 valori per segmento in una forma leggibile a colpo d'occhio (`docs/kpi_operators.md` §7.3 lo dichiara già «un problema della dashboard, non di questo operatore»).

---

## Perimetro

| Fuori perimetro | Ragione | A chi spetta |
|---|---|---|
| **Costruire pagine, layout, navigazione nel `.pbix`** | è presentazione, non calcolo del valore | `008a` |
| **Portare narrazione o limiti a schermo** | `docs/kpi_operators.md` §12 li assegna già a chi costruisce la narrazione | `008b` |
| **Toccare Tableau** | stretch goal dichiarato fuori sequenza | `009` |
| **Modificare `docs/roadmap.md`** | appartiene alla regia, per qualunque ragione | regia |
| **Toccare `data/raw/`** | sola lettura per principio II, non versionata | nessuno, mai da script |
| **Riaprire le nove decisioni di `docs/kpi_operators.md` (D1-D9)** | già chiuse e revisionate dalla `007a` | `007a`, conclusa |
| **Automatizzare l'apertura di Power BI Desktop o la scrittura nel `.pbix`** | interazione con la GUI, fuori dal confine dell'automazione (principio V) — la verifica manuale di E9 resta invece dentro perimetro | nessuno, mai da script |

---

## User Scenarios & Testing *(mandatory)*

Gli attori sono due: **chi scrive** questo documento e lo script (la sessione della `007b`) e **chi lo eredita** — Valerio, che incolla il DAX trascritto nel `.pbix` già materializzato e verifica i numeri contro il motore reale prima del merge (E9), e chiunque cloni il repository e voglia rigenerare ogni valore senza una licenza Power BI.

### User Story 1 — La pipeline intera, non solo lo script, rigenera tutti gli 8 valori in modo riproducibile (Priority: P1)

`data/processed/` non è versionato (`.gitignore`, fuori dal principio II): chi verifica la riproducibilità non può fermarsi a rieseguire `scripts/build_kpi_measures.py` da solo, perché il suo input non è nel repository. La prova che conta parte da `data/raw/` — ottenuto con `scripts/download_data.sh` e un token Kaggle, come dichiarato in `CLAUDE.md` — e attraversa `scripts/build_datasets.py` (già verificato deterministico: nessuna lettura dell'orologio, nessun generatore casuale) prima di arrivare a `scripts/build_kpi_measures.py`.

**Why this priority**: è la proprietà che rende questa feature compatibile con un repository da portfolio letto da esterni — un numero che dipende da un'esecuzione manuale non riproducibile è un debito verso il principio I fin dal primo giorno. Rivendicare la riproducibilità e verificarla solo su metà della catena (lo script nuovo, non la rigenerazione del suo input) sarebbe la stessa classe di scorciatoia che questa feature esiste per non prendere.

**Independent Test**: si rigenera `data/processed/` da `data/raw/` con `python3 scripts/build_datasets.py`, poi si esegue `python3 scripts/build_kpi_measures.py`; l'artefatto prodotto coincide con quello committato. Ripetere l'intera catena una seconda volta produce lo stesso risultato.

**Acceptance Scenarios**:

1. **Given** `data/raw/` presente (scaricato una volta con token Kaggle), **When** si esegue `python3 scripts/build_datasets.py` seguito da `python3 scripts/build_kpi_measures.py`, **Then** entrambi terminano con successo e `reports/kpi_measures.json` viene prodotto.
2. **Given** l'artefatto prodotto dalla catena completa, **When** lo si confronta con quello committato, **Then** coincide byte per byte.

---

### User Story 2 — L'invarianza del numeratore della North Star si legge come verificata o come ritrovamento, mai come assunzione taciuta (Priority: P1)

Chi legge `docs/kpi_measures.md` trova, per `BQ1-K1`, il conteggio di `Music & Musicals` calcolato sul dato trasformato e il confronto esplicito con il conteggio di origine (375), con l'esito dichiarato in entrambi i casi possibili.

**Why this priority**: è il rilievo bloccante più esposto ereditato dalla `007a` (R1), e l'unico dei sei debiti che cambia lo stato epistemico di un valore pubblicato — da assunzione a fatto verificato, o da assunzione a divergenza dichiarata.

**Independent Test**: si legge la sezione `BQ1-K1` di `docs/kpi_measures.md`; il conteggio sul trasformato è ancorato a un valore di `reports/kpi_measures.json`, non scritto a mano.

**Acceptance Scenarios**:

1. **Given** il conteggio calcolato sul dato trasformato coincide con 375, **When** si legge il documento, **Then** dichiara esplicitamente che l'invarianza è ora verificata, con entrambi i numeri ancorati.
2. **Given** il conteggio calcolato non coincidesse con 375, **When** si legge il documento, **Then** dichiara la divergenza come ritrovamento, con entrambi i numeri ancorati e nessuna scelta silenziosa fra i due.

---

### User Story 3 — Ogni misura sulla popolarità porta accanto la propria quota di zeri, con avvertimento dove dovuto (Priority: P1)

Chi legge `BQ2-K1` trova, per ciascuno dei 114 segmenti, la mediana di popolarità e la quota di righe a popolarità zero dello stesso segmento; dove il segmento porta `is_high_zero_genre = vero`, un avvertimento testuale esplicito accompagna il valore.

**Why this priority**: è D7 di `docs/kpi_operators.md` §5.1, un obbligo non negoziabile, non un'opzione di presentazione.

**Independent Test**: si cercano nel documento i 7 segmenti con `is_high_zero_genre = vero`; ciascuno porta l'avvertimento testuale accanto al proprio valore di mediana.

**Acceptance Scenarios**:

1. **Given** un segmento con `is_high_zero_genre = vero`, **When** si legge il suo valore di `segment_demand_index`, **Then** l'avvertimento testuale è presente, indipendentemente da quanto la mediana sia alta.
2. **Given** un segmento senza quella marcatura, **When** si legge il suo valore, **Then** la quota di zeri è comunque pubblicata accanto al valore, senza l'avvertimento.

---

### User Story 4 — I tre vincoli di `docs/kpi_operators.md` §12 e le issue `#7`/`#8` si chiudono con dichiarazione esplicita di dove (Priority: P2)

Chi legge `docs/kpi_operators.md` dopo questa feature trova §12 senza vincoli aperti relativi alla mediana, alla durata degenere, all'asimmetria e all'arrotondamento — ciascuno chiuso con un riferimento a dove la chiusura vive (una decisione D10/D11 nel documento stesso, o un valore in `docs/kpi_measures.md`).

**Why this priority**: è l'applicazione diretta della regola scritta in `CLAUDE.md` il 2026-08-22 — chiudere solo i rilievi necessari, ma dichiarare sempre come. Questi quattro non sono rilievi di revisione: sono vincoli che `docs/kpi_operators.md` stesso ha dichiarato di non chiudere e assegnato esplicitamente a chi verrà dopo.

**Independent Test**: si apre `docs/kpi_operators.md` §12 dopo la feature; nessuno dei tre vincoli compare più come aperto senza un riferimento a dove è stato chiuso. Si aprono le issue `#7` e `#8` su GitHub; entrambe sono chiuse con un commento che punta al commit che le ha chiuse.

**Acceptance Scenarios**:

1. **Given** §12 di `docs/kpi_operators.md`, **When** lo si legge dopo la feature, **Then** dichiara la convenzione di mediana (E2/D10), la decisione sulla durata degenere (E3/D11) e la regola di arrotondamento (E5), ciascuna con riferimento a dove vive il dettaglio operativo.
2. **Given** l'issue `#7`, **When** la si controlla su GitHub, **Then** è chiusa con riferimento a `docs/kpi_operators.md` §10/§12.
3. **Given** l'issue `#8`, **When** la si controlla su GitHub, **Then** è chiusa con riferimento alla nota in loco di `docs/kpi_operators.md` §11.

---

### User Story 5 — Il documento e l'artefatto sono verificabili meccanicamente (Priority: P2)

Chi esegue `python3 scripts/check_audit_coherence.py` dopo questa feature trova `docs/kpi_measures.md` come settimo documento verificato — sesto in severità stretta, dato che `docs/data_audit.md` resta ad avvisi — e `reports/kpi_measures.json` come quinto artefatto nello spazio dei nomi unito, ed entrambi i controlli passano.

**Why this priority**: è il presidio meccanico che rende il documento coerente con il resto del progetto, ed è la condizione esplicita di successo dichiarata dal prompt di consegna.

**Independent Test**: si esegue il controllo dopo l'implementazione; esce con stato 0, e continua a farlo sui sei documenti già verificati.

**Acceptance Scenarios**:

1. **Given** `docs/kpi_measures.md` completo, **When** il controllo lo scandisce, **Then** ogni numerale in posizione di fatto misurato porta un'ancora verso `reports/kpi_measures.json` o un altro artefatto già versionato, o il marcatore esplicito di non-misurato.
2. **Given** la tupla `ARTIFACTS` e `DOCUMENTS` dello script, **When** le si ispeziona, **Then** contengono rispettivamente `reports/kpi_measures.json` e `docs/kpi_measures.md` (severità stretta).

---

### User Story 6 — La nota in loco su `business_case.md` §3 rende vera la descrizione della North Star nel momento in cui il suo valore viene pubblicato (Priority: P2)

Chi legge `business_case.md` §3 mentre `docs/kpi_measures.md` pubblica per la prima volta il valore della North Star trova, accanto al testo originale («musical, documentari musicali, concerti, film sulla musica»), una nota che dichiara che la misura legge una sola etichetta (`Music & Musicals`).

**Why this priority**: rilievo R11 della revisione `001`, assegnato a questa feature dalla decisione di regia del 2026-08-21 in `docs/roadmap.md`. Il testo era impreciso da quando esiste; nel momento in cui il numero della North Star viene pubblicato sotto quella descrizione, l'imprecisione diventa un'affermazione falsa sul deliverable che la accompagna.

**Independent Test**: si legge `business_case.md` §3; il testo originale è intatto, la nota è accanto e dichiara data, feature, causa, valore corretto.

**Acceptance Scenarios**:

1. **Given** `business_case.md` §3, **When** lo si legge dopo questa feature, **Then** il testo originale non è stato cancellato né riscritto, e la nota in loco è immediatamente accanto al passaggio che corregge.

---

### User Story 7 — Ogni valore pubblicato dichiara se è stato verificato contro il motore reale, non solo calcolato da script (Priority: P1)

Prima del merge, Valerio incolla il DAX trascritto per ciascuna delle otto misure nel `.pbix` già materializzato, legge i valori restituiti dal motore, e li confronta con `reports/kpi_measures.json` (E9). `docs/kpi_measures.md` dichiara l'esito per ciascuna misura.

**Why this priority**: è la correzione più importante della revisione di regia sulla prima versione di questa spec — un valore verificato contro il motore reale è una categoria diversa, e più forte, di un valore calcolato da uno script che replica le stesse regole. Rinviare questo confronto alla `008a` sposterebbe a valle il ritrovamento più rilevante che questa feature possa produrre, nel momento in cui costerebbe di più risolverlo.

**Independent Test**: si apre `docs/kpi_measures.md` dopo il merge; ciascuna delle otto misure dichiara esplicitamente «verificato contro il motore» oppure, in caso di divergenza, la nota in loco con i due numeri e la causa se identificabile.

**Acceptance Scenarios**:

1. **Given** una misura il cui valore letto dal motore coincide con `reports/kpi_measures.json`, **When** si legge la sua sezione in `docs/kpi_measures.md`, **Then** dichiara che il valore è verificato contro il motore reale, non solo calcolato da script.
2. **Given** una misura il cui valore letto dal motore non coincide, **When** si legge la sua sezione, **Then** porta una nota in loco con entrambi i numeri, dichiarata come il ritrovamento più rilevante della feature, e il blocco di chiusura riportato prima del merge la cita esplicitamente.
3. **Given** l'intero documento, **When** lo si legge prima che Valerio esegua il confronto, **Then** nessuna misura dichiara di essere «verificata contro il motore» senza che il confronto sia realmente avvenuto — lo stato di default resta «calcolato da script».

---

### Edge Cases

- **Il conteggio trasformato di `Music & Musicals` non coincide con 375.** È il caso E7: si dichiara come ritrovamento con entrambi i numeri ancorati, si usa il valore sul trasformato per il calcolo, e si aggiunge una nota in loco su `docs/kpi_operators.md` §2.1. Non è un fallimento della feature: è esattamente il tipo di scoperta che l'esecuzione dell'operatore di §2.2 esiste per rendere possibile.
- **Un segmento ha un numero pari di righe e la mediana di popolarità cade fra due interi diversi** (es. popolarità 40 e 41). La convenzione E2/D10 pubblica la media (40,5), non uno dei due arrotondato — l'arrotondamento a una cifra decimale di E5 lo rappresenta correttamente senza perdita.
- **La riga a durata degenere (`is_duration_zero`) coincide per caso con uno dei due valori centrali della mediana di 89.741 tracce.** Impossibile per costruzione: il valore è il minimo assoluto della distribuzione (zero), e la posizione centrale di un campione di quella dimensione non può coincidere con l'estremo inferiore a meno che l'intera distribuzione non sia degenere, il che i dati esclusi da questa feature (`docs/data_cleaning.md`) escludono.
- **Un segmento appare vuoto dopo il filtro per `track_genre`** (0 righe). Non è un caso atteso — ogni segmento ha almeno 904 righe (`CL.SP.recalc.genre.rows_min`) — ma se si verificasse lo script si ferma con un errore esplicito invece di produrre una mediana indefinita silenziosamente, sullo stesso principio di `scripts/build_bq3_scenarios.py` (FR-016 della `004`: meglio nessun file che un file parziale).
- **Il verbale di revisione trova un rilievo che invaliderebbe un valore pubblicato ma non un operatore** (per esempio, un errore aritmetico nello script). È per definizione "strettamente necessario" secondo `CLAUDE.md`: il documento, senza quella correzione, pubblicherebbe un valore che non regge. Si chiude dentro questa feature, non si rinvia.

---

## Requirements *(mandatory)*

### Lo script e l'artefatto (E1)

- **FR-001**: La feature MUST produrre `scripts/build_kpi_measures.py`, deterministico (nessuna lettura dell'orologio, nessun generatore casuale, aritmetica in `decimal.Decimal`), che legge solo file già versionati (`data/processed/*.csv`, `data/curated/dim_category_mood.json`, `reports/data_profile.json`, `reports/bq3_scenarios.json`) e produce `reports/kpi_measures.json`.
- **FR-002**: `reports/kpi_measures.json` MUST seguire lo schema `values`/`catalogs`/`conventions`/`sources` già in uso da `reports/bq3_scenarios.json`, con un'impronta (`sha256`) di ciascun file di ingresso letto.
- **FR-003**: Due esecuzioni consecutive dello script su input invariati MUST produrre un file identico byte per byte.
- **FR-004**: Lo script MUST fermarsi con un errore esplicito, senza scrivere alcun file, se un'aggregazione per segmento o per categoria opera su un insieme vuoto o su un identificativo assente dai cataloghi previsti (`catalogs.mood_categories`, l'elenco dei 42 nomi di categoria).

### Le otto misure

- **FR-005**: Lo script MUST calcolare `music_adjacent_catalog_share` (`BQ1-K1`) come il numero di titoli distinti in `Music & Musicals` sul ponte titolo-categoria trasformato, diviso il numero di titoli distinti di `dim_title`, e MUST pubblicare anche l'operatore della condizione C1 (§2.2 di `docs/kpi_operators.md`): il conteggio di titoli per ciascuna delle 42 categorie e la posizione di `Music & Musicals` rispetto alla mediana dei 42 conteggi (convenzione E2/D10).
- **FR-006**: Lo script MUST calcolare `format_duration_gap` (`BQ1-K2`) come mediana della durata in minuti delle tracce musicali deduplicate meno mediana della durata in minuti dei soli film del catalogo video, con il proprio segno, e MUST pubblicare accanto: (a) entrambe le varianti della mediana musicale — con e senza la riga a durata degenere (E3/D11) — e la loro differenza; (b) la quota di titoli di tipo `Movie` sul totale del catalogo video (E4).
- **FR-007**: Lo script MUST calcolare `mood_profile_overlap` (`BQ1-K3`) come quota di tracce musicali deduplicate il cui profilo (`energy`, `valence`, `danceability`) cade, su tutti e tre gli assi contemporaneamente, dentro gli intervalli chiusi `[min, max]` calcolati sulle 42 righe di `dim_category_mood` — il prodotto cartesiano di D1 di `docs/kpi_operators.md`, non un inviluppo convesso.
- **FR-008**: Lo script MUST calcolare, per ciascuno dei 114 segmenti, `segment_demand_index` (`BQ2-K1`) come mediana di popolarità delle coppie traccia-segmento di quel segmento, e MUST pubblicare accanto la quota di righe a popolarità zero dello stesso segmento; dove il segmento porta `is_high_zero_genre = vero`, il valore MUST portare un avvertimento testuale esplicito (D7 di `docs/kpi_operators.md`).
- **FR-009**: Lo script MUST calcolare, per ciascuno dei 114 segmenti, `segment_catalog_affinity` (`BQ2-K2`) come `1 − d`, con `d` media delle tre distanze assolute per asse fra il profilo mediano del segmento (sulle coppie traccia-segmento) e il profilo del catalogo video (mediana ponderata sulle 19.323 assegnazioni titolo-categoria, ciascuna con il profilo della propria categoria) — D2 di `docs/kpi_operators.md`.
- **FR-010**: Lo script MUST calcolare, per ciascuno dei 114 segmenti, `segment_entry_priority` (`BQ2-K3`): la domanda normalizzata (`segment_demand_index / 100`), il punteggio pesato (`0,5 × domanda_normalizzata + 0,5 × affinità`), l'appartenenza al quadrante alta-domanda/alta-affinità (soglia mediana su entrambi gli assi, condizione stretta), e la graduatoria ordinata per punteggio decrescente — D3/D4/D8 di `docs/kpi_operators.md`.
- **FR-011**: Il documento MUST citare i valori di `premium_tier_adoption_rate` (`BQ3-K1`) e `arpu_uplift` (`BQ3-K2`) direttamente da `reports/bq3_scenarios.json`, senza alcun nuovo calcolo, dichiarando esplicitamente che l'operatore e il valore sono già chiusi dalla `004`.

### La verifica dell'invarianza (E7) e il contratto di versione (E8)

- **FR-012**: Lo script MUST contare i titoli distinti assegnati a `Music & Musicals` su `data/processed/netflix_title_category.csv` e confrontare il risultato con `375` (`NF.cat.music_musicals.titles`), pubblicando entrambi i numeri come valori ancorati distinti nell'artefatto.
- **FR-013**: `docs/kpi_measures.md` MUST dichiarare esplicitamente l'esito del confronto di FR-012 — invarianza verificata, o divergenza dichiarata come ritrovamento con nota in loco su `docs/kpi_operators.md` §2.1 — e MUST usare il conteggio sul dato trasformato, non il 375 di origine, per calcolare `music_adjacent_catalog_share`.
- **FR-014**: La feature MUST verificare che i tre passaggi di `docs/kpi_operators.md` che citano la versione della tabella dei mood risolvano correttamente alla versione corrente (`MOOD.table.version`); se già corretti (come trovato in E8), la feature MUST dichiararlo come ritrovamento invece di modificare quei passaggi.

### Chiusura dei vincoli di §12 e delle issue (E2-E6)

- **FR-015**: `docs/kpi_operators.md` MUST guadagnare una decisione **D10** che dichiara la convenzione di mediana (E2), riportata in §10 e §12, e la feature MUST chiudere l'issue GitHub `#7` con riferimento a quella decisione.
- **FR-016**: `docs/kpi_operators.md` MUST guadagnare una decisione **D11** che dichiara se le righe a durata degenere entrano nella mediana di `BQ1-K2` (E3), con riferimento al valore comparativo pubblicato in `docs/kpi_measures.md`.
- **FR-017**: `docs/kpi_operators.md` §12 MUST registrare la chiusura del vincolo sull'asimmetria di `BQ1-K2` (E4) con un riferimento a dove il valore vive (`docs/kpi_measures.md`), e la chiusura del vincolo di arrotondamento (E5) con la tabella delle cifre per unità di misura.
- **FR-018**: `docs/kpi_operators.md` §11 MUST portare una nota in loco che corregge l'attribuzione di `D6` a `BQ2-K1` (E6), con data, feature, causa e valore corretto, senza cancellare il testo precedente; la feature MUST chiudere l'issue GitHub `#8` con riferimento a quella nota.

### `business_case.md` §3 (User Story 6)

- **FR-019**: `business_case.md` §3 MUST portare una nota in loco, accanto al passaggio che descrive il contenuto della North Star come «musical, documentari musicali, concerti, film sulla musica», che dichiara: la misura legge la sola etichetta `Music & Musicals`; data; feature `007b`; causa (rilievo R11 della revisione `001`, assegnato dalla decisione di regia del 2026-08-21). Il testo originale non MUST essere cancellato.

### Documento pubblicato e controllo di coerenza

- **FR-020**: La feature MUST produrre `docs/kpi_measures.md` con, per ciascuno degli otto KPI: domanda di business, formula (prosa e testo DAX trascritto), provenienza nel modello dati, valore pubblicato con ancora verso `reports/kpi_measures.json`, confidenza dichiarata, limiti specifici del KPI.
- **FR-021**: `docs/kpi_measures.md` MUST entrare in `DOCUMENTS` di `scripts/check_audit_coherence.py` sotto **severità stretta**, come settimo documento verificato.
- **FR-022**: `reports/kpi_measures.json` MUST entrare in `ARTIFACTS` di `scripts/check_audit_coherence.py`, come quinto artefatto nello spazio dei nomi unito, verificando l'assenza di collisioni di prefisso con gli altri quattro.
- **FR-023**: Ogni numerale scritto in `docs/kpi_measures.md` in posizione di fatto misurato MUST portare un'ancora verso un artefatto già versionato o il marcatore esplicito di non-misurato, secondo `docs/convenzioni-marcatura.md`; ogni affermazione derivata (confronto, graduatoria, rapporto — regola D5 di `docs/convenzioni-marcatura.md` §7) MUST avere un identificativo proprio nell'artefatto.
- **FR-024**: `docs/convenzioni-marcatura.md` MUST registrare `docs/kpi_measures.md` nella propria tabella di severità e nella tabella di provenienza, con data e feature.

### Obblighi che nessun automatismo esegue

- **FR-025**: La feature MUST aggiornare `README.md`: riga nella tabella di stato con link a `specs/007b-kpi-measures/review.md`, deliverable elencato, la frase sui documenti che pubblicano misure estesa all'ottavo documento, `Setup` e `Struttura` allineati, il conteggio dei documenti sotto controllo di coerenza aggiornato da sei a sette.
- **FR-026**: La feature MUST produrre `specs/007b-kpi-measures/review.md` secondo i quattro obblighi di `CLAUDE.md`: committato prima di correggere l'artefatto; dichiara in apertura che cosa ha letto e che cosa no; ancora commit e impronta del contenuto letto; non si corregge, con un blocco di chiusura che distingue risolto/indebolito/rinviato per ciascun rilievo, e nomina il numero dell'issue per ogni rinvio.
- **FR-027**: Nessun commit MUST essere eseguito di iniziativa dalla sessione esecutiva. Messaggio e contenuto si propongono; decide Valerio. Vale per `add`, `push`, apertura di PR, merge, e per la chiusura delle issue `#7` e `#8` su GitHub.
- **FR-028**: `docs/roadmap.md` NON DEVE essere modificato da questa feature: appartiene alla regia.

### La verifica contro il motore reale (E9)

- **FR-029**: Prima del merge, Valerio MUST incollare il testo DAX trascritto di ciascuna delle otto misure nel `.pbix` già materializzato, leggere i valori restituiti dal motore e confrontarli con `reports/kpi_measures.json`. Questo passo non MUST essere automatizzato da alcuno script (principio V), ed è comunque dentro il perimetro di questa feature, non della `008a`.
- **FR-030**: `docs/kpi_measures.md` MUST dichiarare, per ciascuna delle otto misure, l'esito del confronto di FR-029: «verificato contro il motore reale» se i valori coincidono, oppure una nota in loco con entrambi i numeri e la causa (se identificabile) se divergono. Nessuna misura MUST dichiararsi verificata prima che il confronto sia realmente avvenuto.
- **FR-031**: Una divergenza trovata da FR-029 su almeno una misura MUST essere riportata nel blocco di chiusura della feature, prima del merge, come il ritrovamento di priorità più alta — non assorbita in silenzio né rinviata alla `008a`.

### Key Entities

- **`scripts/build_kpi_measures.py`**: lo script deterministico che calcola le otto misure applicando gli operatori di `docs/kpi_operators.md` sui dati versionati.
- **`reports/kpi_measures.json`**: l'artefatto prodotto, schema `values`/`catalogs`/`conventions`/`sources`, quinto nello spazio dei nomi unito del controllo di coerenza.
- **`docs/kpi_measures.md`**: il documento pubblicato, un valore per ciascuno degli otto KPI (114 righe per segmento per `BQ2-K1`/`BQ2-K2`/`BQ2-K3`, riportate per intero o riassunte con rimando esplicito all'artefatto completo), settimo documento verificato — sesto in severità stretta.
- **`D10`, `D11`**: le due nuove decisioni aggiunte a `docs/kpi_operators.md` (convenzione di mediana, trattamento della durata degenere).
- **Verifica contro il motore (E9)**: il confronto, eseguito a mano da Valerio, fra il valore letto dal `.pbix` materializzato per ciascuna misura e il valore corrispondente in `reports/kpi_measures.json`. Cambia lo statuto epistemico del valore pubblicato, da «calcolato da script» a «verificato contro il motore reale», o rivela un ritrovamento.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Tutti e otto i KPI hanno un valore pubblicato in `docs/kpi_measures.md`, ciascuno con ancora verso `reports/kpi_measures.json` o, per `BQ3-K1`/`BQ3-K2`, verso `reports/bq3_scenarios.json`.
- **SC-002**: `python3 scripts/build_kpi_measures.py` eseguito due volte produce un artefatto identico byte per byte.
- **SC-003**: `python3 scripts/check_audit_coherence.py` esce con stato 0, verificando tutti e sette i documenti (i sei esistenti più `docs/kpi_measures.md`) e i cinque artefatti.
- **SC-004**: L'invarianza del numeratore della North Star è dichiarata come verificata (con il conteggio sul trasformato ancorato e coincidente con 375) oppure come divergenza esplicita con nota in loco — non resta un'assunzione taciuta.
- **SC-005**: I tre vincoli di `docs/kpi_operators.md` §12 e le issue `#7`/`#8` sono chiusi, ciascuno con un riferimento verificabile a dove la chiusura vive.
- **SC-006**: `specs/007b-kpi-measures/review.md` esiste, è committato prima di qualunque correzione a `docs/kpi_measures.md`, e il suo blocco di chiusura distingue risolto/indebolito/rinviato per ogni rilievo.
- **SC-007**: `README.md` non presenta alcun disallineamento con lo stato della feature (tabella di stato, deliverable, conteggio documenti, `Setup`, `Struttura`).
- **SC-008**: Ciascuna delle otto misure dichiara in `docs/kpi_measures.md` l'esito del confronto con il motore reale (E9) prima del merge — verificata, o divergente con nota in loco e ritrovamento riportato.

Otto criteri, verificabili sul prodotto da chi riceve il repository senza sapere come è stato costruito. La stima di 5 ore, revisione inclusa, è un vincolo di processo del principio III e non compare fra loro.

---

## Stima e scomposizione

**5 ore** di sessione esecutiva, dichiarate nel prompt di consegna, revisione e chiusura dei rilievi incluse. Il tempo che Valerio spende sul passo manuale di E9 — incollare otto misure DAX in un `.pbix` già aperto e leggere i valori — è lavoro alla GUI, non della sessione, sullo stesso trattamento riservato alla materializzazione del modello: non entra nella stima di 5 ore e non la fa slittare.

Se dopo `/speckit.tasks` la scomposizione dei task rivela un lavoro sostanzialmente più grande — in particolare se il confronto di E7 rivela una divergenza che richiede di riaprire l'operatore di `BQ1-K1` invece di limitarsi a dichiararla, o se E9 rivela una divergenza fra script e motore che richiede di correggere lo script — la sessione esecutiva si ferma al secondo punto di stop e lo riporta, invece di comprimere la verifica per restare dentro la stima.

Questa spec non propone una scomposizione in più feature: le otto misure condividono lo stesso script e lo stesso documento, e separarle moltiplicherebbe la revisione senza ridurre il lavoro — la `007a` aveva già osservato lo stesso argomento per le nove decisioni interdipendenti.

---

## Assumptions

- **`data/processed/*.csv` è il dato che il modello Power BI materializzato legge**, verificato per coincidenza di conteggio riga con gli anchor di `reports/cleaning_report.json` (8.807 titoli, 19.323 assegnazioni, 89.741 tracce deduplicate, 113.550 coppie traccia-genere). Se il `.pbix` reale leggesse da una copia divergente di questi file, il confronto di E9 fra script e motore lo rivelerebbe.
- **Il testo DAX trascritto in `docs/kpi_measures.md` è equivalente, non necessariamente identico nella meccanica di valutazione, al comportamento del motore Power BI Desktop reale.** Questa feature non lo assume più senza verifica: E9 esegue il confronto a mano, dentro questa stessa feature e prima del merge, non alla `008a`. Una divergenza trovata è un ritrovamento da registrare con nota in loco su questo documento (FR-030), non un difetto del processo che l'ha trovata.
- **I sei debiti ereditati non richiedono di riaprire alcuna decisione di `docs/kpi_operators.md` (D1-D9).** Se l'esecuzione di E7 rivelasse una divergenza che invalida l'operatore stesso di `BQ1-K1` (non solo il numero di origine), sarebbe un ritrovamento più ampio della stima di questa feature, e la sessione si fermerebbe a dichiararlo invece di decidere autonomamente come correggerlo.
- **Il verbale di revisione della `007b` riceve solo `docs/kpi_measures.md`**, non lo script né l'artefatto JSON: è il documento pubblicato, non il codice che lo produce, l'oggetto della revisione in contesto pulito — coerente con il precedente della `007a`, che ha revisionato `docs/kpi_operators.md` e non gli artefatti a monte.

---

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: **BQ1 — Posizionamento**, **BQ2 — Segmento di ingresso**, **BQ3 — Impatto stimato**. Le tre insieme: questa feature pubblica il valore di tutti e otto i KPI del framework, incluse le tre condizioni della regola di decisione della North Star (`business_case.md` §3).
- **Contributo**: è la prima feature del progetto che pubblica un numero per ciascuno degli otto KPI. Senza questi valori, l'argomento di coerenza strategica della North Star resta una regola scritta ma mai applicata — nessuno dei tre criteri C1/C2/C3 ha un esito, e nessuna delle tre domande di business ha una risposta verificabile, solo un metodo dichiarato per produrla.

---

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

Questa feature non introduce alcuna nuova fonte dati: eredita per intero la classificazione già fissata da `docs/business_case.md` §5.4 e ripetuta da `docs/kpi_operators.md` §11, e la tabella seguente la riporta senza modificarla.

| KPI | Nome semantico | Fonte | Confidenza | Formato di presentazione | Calcolato da |
|---|---|---|---|---|---|
| `BQ1-K1` | `music_adjacent_catalog_share` | Netflix (reale) | alta | valore puntuale | `scripts/build_kpi_measures.py`, su `netflix_title_category.csv` e `netflix_titles.csv` |
| `BQ1-K2` | `format_duration_gap` | Derivato (Netflix + Spotify) | alta | valore puntuale con segno | `scripts/build_kpi_measures.py`, su `spotify_tracks.csv` e `netflix_titles.csv` |
| `BQ1-K3` | `mood_profile_overlap` | Derivato (Netflix + Spotify) | **media**, non negoziabile (`data_model.md` §15) | valore puntuale con nota | `scripts/build_kpi_measures.py`, su `spotify_tracks.csv` e `dim_category_mood.json` |
| `BQ2-K1` | `segment_demand_index` | Spotify (reale) | media | un valore per segmento, con nota | `scripts/build_kpi_measures.py`, su `spotify_track_genre.csv` |
| `BQ2-K2` | `segment_catalog_affinity` | Derivato (Netflix + Spotify) | **media**, non negoziabile (`data_model.md` §15) | un valore per segmento, con nota | `scripts/build_kpi_measures.py`, su tutte e quattro le fonti |
| `BQ2-K3` | `segment_entry_priority` | Derivato (`BQ2-K1` + `BQ2-K2`) | **media**, non negoziabile (`data_model.md` §15) | quadrante booleano + punteggio + graduatoria, per segmento | `scripts/build_kpi_measures.py`, componendo i due KPI precedenti |
| `BQ3-K1` | `premium_tier_adoption_rate` | Benchmark (esterno) + Sintetico | bassa | range best/base/worst | già calcolato dalla `004`, citato senza ricalcolo |
| `BQ3-K2` | `arpu_uplift` | Derivato (`BQ3-K1` + prezzi assunti) | bassa | range best/base/worst | già calcolato dalla `004`, citato senza ricalcolo |

**Assunzioni dietro i dati**, dichiarate per iscritto: nessuna nuova rispetto a quelle già dichiarate da `docs/kpi_operators.md` §11 (indipendenza per asse, equipeso, soglia mediana). Questa feature ne aggiunge una propria, dichiarata in E1: che `data/processed/*.csv` rappresenti fedelmente il dato che il modello Power BI materializzato consuma.

**Nessuna promozione di confidenza**: nessun valore calcolato da questa feature sposta la confidenza di alcun KPI oltre quella già fissata dal business case e dal modello dati.

---

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Non risponde a, fino al passo E9**: se il testo DAX trascritto produca esattamente lo stesso numero quando eseguito dal motore reale di Power BI Desktop. Questa feature esegue quel confronto a mano, dentro il proprio perimetro e prima del merge (FR-029) — non lo lascia indefinito: la domanda resta aperta solo nella finestra fra l'implementazione dello script e l'esecuzione manuale di Valerio, non oltre il merge.
- **Non risponde a**: se le nove decisioni di `docs/kpi_operators.md` (D1-D9) o le due nuove di questa feature (D10-D11) siano le uniche difendibili — eredita quel limite dalla `007a` senza aggiungerne di analoghi propri, tranne dove questa feature stessa argomenta una scelta nuova (E2-E5), per cui vale la stessa riserva.
- **Inferenza da evitare — un valore calcolato da questa feature non è, di per sé, un valore verificato contro il motore reale.** Riduce l'arbitrarietà residua che restava dopo `docs/kpi_operators.md` (una formula ben definita eseguita male produce comunque un numero sbagliato), ma il salto di categoria — da «calcolato da script» a «verificato contro il motore» — avviene solo con E9, non per il solo fatto che lo script applichi correttamente le regole.
- **Inferenza da evitare — `mood_profile_overlap` resta una stima per eccesso della sovrapposizione reale** (D1 della `007a`, ereditato senza modifiche): il valore pubblicato sovrastima quanto un inviluppo convesso stimerebbe, per la ragione già dichiarata in `docs/kpi_operators.md` §4.
- **Inferenza da evitare — la grandezza assoluta di `segment_catalog_affinity` non è confrontabile con una distanza osservata altrove** (D2 della `007a`, ereditato): ha senso solo relativamente ad altri segmenti calcolati con la stessa formula.
- **Copertura del dato**: eredita per intero i limiti già dichiarati da `docs/business_case.md` (A1-A6), `docs/data_model.md` §18 e `docs/kpi_operators.md` §12 — cataloghi proxy, non StreamWave; copertura ferma al 2021 (video) e al 2022 (musica, non verificabile); nessun dato comportamentale; nessuna dimensione temporale nel modello. Questa feature non ne introduce di nuovi, perché non tocca alcun dato oltre a quello già modellato.
- **Dove è esposto a chi legge la dashboard**: da nessuna parte. Come `docs/kpi_operators.md` §12 dichiara già, i limiti di questo framework devono essere ereditati e ripresentati in forma comprensibile da chi costruirà la narrazione (`008b`), dove il lettore della dashboard li incontra.
