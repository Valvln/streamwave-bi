# Research: Misure DAX e documento dei KPI

**Feature**: 007b-kpi-measures | **Data**: 2026-08-22

## Perché questo documento è corto, e diverso da quello della `007a`

Il Technical Context di [plan.md](./plan.md) non contiene alcun `NEEDS CLARIFICATION`: le nove decisioni/verifiche (E1-E9) sono già argomentate per intero in [spec.md](./spec.md), inclusa quella — E9 — che la revisione della regia ha corretto rispetto alla prima stesura. Questo file le consolida nel formato Decisione/Motivazione/Alternative richiesto dalla Fase 0, con puntatore alla sezione di spec che le argomenta per esteso.

**La differenza con la `007a` non è di formato, è di natura.** Le nove decisioni della `007a` erano tutte scelte fra letture alternative di una formula non ancora scritta in nessun documento. Qui, sei delle nove (E1-E6) sono scelte di *come tradurre* una formula già fissata in un artefatto verificabile, e tre (E7, E8, E9) non sono scelte affatto: sono esecuzioni di un confronto che un documento precedente aveva già dichiarato come il modo in cui un'assunzione si chiude. Nessun ritrovamento nuovo di questa fase: gli esiti di E7/E8/E9 non sono ancora noti a questo punto del piano — dipendono dall'esecuzione dello script (E7) e dal confronto manuale di Valerio (E9) — ma l'esistenza dei due possibili esiti, e cosa fare in ciascun caso, è già dichiarata per intero in spec.

## Le nove decisioni/verifiche, in formato Fase 0

### E1 — Script deterministico, non simulazione

- **Decisione**: `scripts/build_kpi_measures.py`, sullo schema di `scripts/build_bq3_scenarios.py` — `Decimal`, mai `float`, nessuna lettura dell'orologio, due esecuzioni identiche — legge `data/processed/*.csv` e `data/curated/dim_category_mood.json`, scrive `reports/kpi_measures.json`.
- **Motivazione**: è l'unica opzione compatibile con un repository verificabile da chi lo clona senza una licenza Power BI; lasciare che sia Valerio a eseguire il DAX a mano e riportare i numeri non sarebbe riproducibile da nessun altro.
- **Alternative scartate**: solo testo DAX senza calcolo (non riproducibile da chi clona); rinvio dell'intera feature (contraddirebbe la sequenza già decisa dalla regia).
- **Il limite che introduce e come si chiude**: una differenza di comportamento fra motore e script è un rischio residuo — E9 lo chiude eseguendo il confronto, non lasciandolo come limite permanente.
- **Riferimento**: spec.md, E1.

### E2 — Convenzione di mediana (issue `#7`)

- **Decisione**: ordinamento, media aritmetica dei due valori centrali su conteggio pari, nessun trattamento speciale dei pari merito.
- **Motivazione**: è la definizione da manuale di statistica; nessuno dei quattro operatori che usano la mediana (`BQ1-K1`/C1, `BQ2-K1`, `BQ2-K2`, `BQ2-K3`) ha un'asimmetria dichiarata che giustificherebbe una mediana "inferiore" o "superiore".
- **Alternative scartate**: mediana inferiore; mediana superiore — entrambe introdurrebbero una convenzione non standard senza un guadagno dichiarabile.
- **Dove si chiude**: `docs/kpi_operators.md` come nuova decisione **D10** (§10, §12); chiude l'issue `#7`.
- **Riferimento**: spec.md, E2.

### E3 — Le righe a durata degenere entrano nella mediana di `BQ1-K2`

- **Decisione**: inclusione, con calcolo di entrambe le varianti (con e senza la riga marcata `is_duration_zero`) e pubblicazione della differenza.
- **Motivazione**: stessa disciplina già applicata a `is_popularity_zero` (D7) — la trasformazione ha scelto di conservare e marcare, non di eliminare; calcolare comunque la variante esclusa rende la scelta verificabile invece che dichiarata a parole.
- **Alternative scartate**: esclusione dal calcolo della mediana, con la marcatura come criterio di filtro — romperebbe la coerenza con D7 senza una ragione nuova.
- **Dove si chiude**: `docs/kpi_operators.md` come nuova decisione **D11** (§3, §12).
- **Riferimento**: spec.md, E3.

### E4 — L'asimmetria di `BQ1-K2` si dichiara con la quota di film

- **Decisione**: pubblicare, accanto a `format_duration_gap`, la quota di titoli `Movie` sul totale dei titoli distinti del catalogo video.
- **Motivazione**: conteggio già alla portata dello stesso script, sulla stessa tabella; rende leggibile l'asimmetria senza introdurre un giudizio su quanto sia grande.
- **Alternative scartate**: nessuna — è la traduzione diretta in operatore del vincolo già dichiarato da `kpi_operators.md` §12, non una scelta fra opzioni.
- **Dove si chiude**: `docs/kpi_operators.md` §12, con riferimento a `docs/kpi_measures.md` dove il valore vive.
- **Riferimento**: spec.md, E4.

### E5 — Arrotondamento e precisione per unità di misura

- **Decisione**: `Decimal` con `ROUND_HALF_UP` esplicito; cifre pubblicate per unità (quote 4 cifre, minuti 2 cifre, indice di popolarità 1 cifra, affinità/punteggio 4 cifre, conteggi interi).
- **Motivazione**: una regola dichiarata per unità si discute una volta sola; un giudizio per singolo valore si discuterebbe ogni volta — lo stesso argomento già usato da `data_model.md` §9 per le colonne.
- **Alternative scartate**: arrotondamento deciso caso per caso, KPI per KPI — introdurrebbe otto regole invece di una.
- **Dove si chiude**: `docs/kpi_operators.md` §12, con riferimento a questa decisione e allo script.
- **Riferimento**: spec.md, E5.

### E6 — Issue `#8`: nota in loco su `kpi_operators.md` §11

- **Decisione**: correggere con nota in loco la riga che attribuisce erroneamente `D6` a `BQ2-K1` come «operatore fissato da» (contraddetta da §5.3), senza riscrivere la cella.
- **Motivazione**: `kpi_operators.md` è già mergiato; la regola di CLAUDE.md sugli artefatti mergiati impone nota in loco, non riscrittura silenziosa.
- **Alternative scartate**: correggere silenziosamente la cella — perderebbe la traccia dell'errore originale, che è essa stessa un dato per chi legge la history del documento.
- **Dove si chiude**: `docs/kpi_operators.md` §11; chiude l'issue `#8`.
- **Riferimento**: spec.md, E6.

### E7 (verifica) — L'invarianza del numeratore della North Star

- **Che cosa si esegue**: conteggio diretto dei titoli distinti in `Music & Musicals` su `data/processed/netflix_title_category.csv`, confrontato con `375` (`NF.cat.music_musicals.titles`).
- **Motivazione**: `kpi_operators.md` §2.1 (D9.1) dichiara questo confronto come il modo in cui l'assunzione di invarianza si chiude, e nota che l'operatore di §2.2 lo fa uscire "quasi gratis" — non è una nuova decisione analitica, è l'esecuzione di un operatore già scritto.
- **Esiti possibili, entrambi dichiarati in anticipo**: coincidenza → invarianza verificata, dichiarata come fatto con il nuovo conteggio ancorato; divergenza → ritrovamento dichiarato con nota in loco su `kpi_operators.md` §2.1, usando comunque il conteggio sul trasformato per il calcolo.
- **Riferimento**: spec.md, E7.

### E8 (verifica) — Il contratto di versione della tabella dei mood

- **Che cosa si è trovato**: i tre passaggi di `kpi_operators.md` (§4, §6, §7) che citano la versione della tabella dei mood usano già l'ancora `oggi la 2<!--@MOOD.table.version-->`, corretta dal chore `criterio-mood-cf1` prima dell'apertura di questo branch.
- **Motivazione per non intervenire**: rieseguire una correzione già fatta produrrebbe un secondo diff sullo stesso testo senza alcun valore aggiunto; la spec dichiara questo debito come già chiuso, non lo riesegue.
- **Riferimento**: spec.md, E8.

### E9 — Verifica contro il motore reale, prima del merge

- **Decisione**: Valerio, nel `.pbix` già materializzato, incolla il DAX trascritto di ciascuna delle otto misure, legge i valori del motore, li confronta con `reports/kpi_measures.json`, prima del merge — non rinviato alla `008a`.
- **Motivazione**: correzione della revisione di regia sulla prima stesura della spec — il `.pbix` è già aperto, il costo è incollare otto misure e leggere un numero; rinviarlo sposterebbe a valle il ritrovamento più rilevante che questa feature possa produrre.
- **Perimetro**: eseguire DAX nella GUI di Power BI Desktop a mano non viola il principio V, che esclude l'automazione della GUI, non l'uso manuale del progetto — nessuno script di questa feature apre o scrive nel `.pbix`.
- **Alternative scartate**: rinvio alla `008a` (prima stesura della spec, corretta dalla regia) — sposterebbe il costo di trovare una divergenza al momento in cui costerebbe di più.
- **Esiti possibili, entrambi dichiarati in anticipo**: coincidenza su tutte e otto → il documento dichiara "verificato contro il motore reale" per ciascuna; divergenza su almeno una → nota in loco con entrambi i numeri e la causa se identificabile, dichiarata come il ritrovamento di priorità più alta nel blocco di chiusura.
- **Riferimento**: spec.md, E9.

## Esito

Nessun `NEEDS CLARIFICATION` residuo. La Fase 1 procede direttamente sullo schema dell'artefatto (`data-model.md`) e sul contratto di lettura per le feature a valle (`contracts/kpi-measures-contract.md`). Gli esiti di E7 e di E9 non sono determinabili in questa fase — dipendono rispettivamente dall'esecuzione dello script e dal confronto manuale di Valerio — e questo è dichiarato come proprietà della fase, non come lacuna: nessun documento precedente a questo punto del piano può anticiparli senza calcolarli o eseguirli per davvero.
