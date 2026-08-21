# Research: Operatori delle misure

**Feature**: 007a-kpi-operators | **Data**: 2026-08-21

## Perché questo documento è corto

Il Technical Context di [plan.md](./plan.md) non contiene alcun `NEEDS CLARIFICATION`: le nove decisioni che altrove sarebbero "ignoti tecnici da chiarire" sono già state prese, argomentate e verificate dalla regia dentro [spec.md](./spec.md) (sezione "Decisioni"), perché per una feature di analisi pura la decisione **è** il lavoro, non una premessa a cui arrivare prima di scrivere codice. Questo file non riapre le nove decisioni: le consolida nel formato Decisione/Motivazione/Alternative richiesto dalla Fase 0, con puntatore alla sezione di spec che le argomenta per esteso, così che chi legge il piano non debba tornare a spec.md per sapere cosa è stato scelto e perché.

Nessun ritrovamento nuovo emerge in questa fase: i tre ritrovamenti che la feature avrebbe potuto generare (mood non definitivo per `CF-1`, campione musicale sbilanciato, 114 segmenti non ricontati sul dato trasformato) erano già noti all'apertura della spec e sono trattati come vincoli ereditati, non come scoperte di questa fase — la differenza con la `006`, che nominava `F3`/`F5` come ritrovamenti prodotti *durante* la costruzione dell'artefatto, è che qui non c'è alcun artefatto dati da costruire in cui un ritrovamento possa emergere in corso d'opera.

## Le nove decisioni, in formato Fase 0

### D1 — Intervallo occupato (`BQ1-K3`)

- **Decisione**: prodotto cartesiano dei tre intervalli scalari indipendenti (energia, positività, ritmo), non un inviluppo convesso congiunto.
- **Motivazione**: `docs/data_model.md` §11 fissa l'aggregazione come min/max non ponderato per asse sulle 42 righe di `dim_category_mood` — tre intervalli scalari separati, non una struttura a punti (x,y,z). Costruire un inviluppo convesso richiederebbe un elenco di 42 terne che nessun artefatto pubblica; il prodotto cartesiano è l'unica lettura che non introduce un dato non ancorato.
- **Alternative scartate**: inviluppo convesso sui tre assi (richiede dati non disponibili); un'unica soglia scalare aggregata sui tre assi (perde l'indipendenza per-asse che §11 fissa).
- **Riferimento**: spec.md, D1; divergenza 2 della revisione 001.

### D2 — Metrica di distanza (`BQ2-K2`)

- **Decisione**: distanza city-block (Manhattan) sui tre assi normalizzati 0-1, complementata a 1 per ottenere l'affinità.
- **Motivazione**: coerente con l'ancoraggio solo agli estremi di `docs/content_taxonomy_bridge.md` §7 — nessun valore osservato calibra il centro della scala, quindi una metrica euclidea (che pesa le differenze al quadrato) implicherebbe un'interpretazione geometrica del centro che il modello non sostiene. La city-block resta interpretabile come somma di scostamenti indipendenti per asse, coerente con l'indipendenza già assunta in D1.
- **Alternative scartate**: euclidea (introduce un'interpretazione geometrica congiunta che §7 non sostiene); Chebyshev/max-per-asse (getta via informazione sugli altri due assi).
- **Riferimento**: spec.md, D2; divergenza 3 della revisione 001; vincolo ereditato da content_taxonomy_bridge.md §7.

### D3 — Pesi e commensurabilità (`BQ2-K3`)

- **Decisione**: `BQ2-K1` (0-100) si normalizza a 0-1 dividendo per 100 prima di comporre; peso 0,5/0,5 fra domanda e affinità, dichiarato come punto di partenza simmetrico, non come stima calibrata.
- **Motivazione**: nessun artefatto pubblica un criterio per pesare domanda più di affinità o viceversa; un peso arbitrario diverso da 0,5 introdurrebbe un giudizio di valore non tracciabile a una fonte. Il 50/50 è l'unica scelta che non richiede una giustificazione empirica che il progetto non possiede.
- **Alternative scartate**: peso calibrato su dati esterni (nessuna fonte ammessa dalla constitution lo sosterrebbe); normalizzare `BQ2-K2` a 0-100 invece di `BQ2-K1` a 0-1 (equivalente in sostanza, scelto 0-1 per coerenza con l'affinità che è già in quella scala).
- **Riferimento**: spec.md, D3; divergenza 4 della revisione 001 (parte 1).

### D4 — Quadranti contro combinazione pesata (`BQ2-K3`)

- **Decisione**: entrambi gli strumenti, con ruoli distinti — il quadrante (soglie ordinali, mediana come spartiacque, condizione stretta `>`) risponde a C3 della North Star; la combinazione pesata di D3 produce l'ordinamento continuo che la scheda di `BQ2-K3` descrive per il ranking dei segmenti.
- **Motivazione**: `business_case.md` §4 e la scheda di `BQ2-K3` (§5.5) descrivono due domande leggermente diverse — "quali segmenti sono contemporaneamente sopra soglia su entrambi gli assi" (decisione binaria, serve alla North Star) e "come si ordinano i segmenti" (ranking, serve all'esplorazione) — e nessuna delle due assorbe l'altra senza perdita.
- **Alternative scartate**: solo quadranti (perde l'ordinamento continuo che la scheda richiede esplicitamente); solo combinazione pesata (non risponde a C3, che chiede una soglia binaria, non un ranking).
- **Riferimento**: spec.md, D4; divergenza 4 della revisione 001 (parte 2).

### D5 — Segno della differenza (`BQ1-K2`)

- **Decisione**: video meno musica; il segno si pubblica insieme al valore assoluto.
- **Motivazione**: la scheda non fissa un verso, ma la narrazione del business case è sempre "il video rispetto a un ingresso in musica" (non il contrario), quindi il verso video-meno-musica è quello coerente con la direzione in cui le altre misure del framework leggono il confronto.
- **Alternative scartate**: musica meno video (verso opposto, meno coerente con la narrazione); solo valore assoluto (perde informazione direzionale che la scheda implicitamente presuppone quando parla di "gap").
- **Riferimento**: spec.md, D5; divergenza 8 della revisione 001 (parte residua).

### D6 — Precisione del confronto

- **Decisione**: una cifra decimale (la precisione del profilo di origine, `reports/data_profile.json`) come soglia di "cambiato", non le quattro cifre del rendiconto di cleaning; la soglia resta esplicitamente limitata al confronto delle quote di zeri per genere, non generalizzata a ogni confronto fra i due artefatti (FR-010, corretto dalla revisione della regia).
- **Motivazione**: confrontare a quattro cifre quando una delle due fonti ne pubblica solo una crea "cambiamenti" che sono artefatti di arrotondamento, non differenze reali — il criterio a una cifra allinea il confronto alla precisione della fonte meno precisa, la convenzione minima che non sovra-interpreta il dato.
- **Alternative scartate**: confronto a quattro cifre (78 generi "cambiati", in gran parte rumore di arrotondamento); generalizzare la soglia a ogni confronto profilo/cleaning (la soglia in punti percentuali non ha senso su conteggi o medie, dichiarato esplicitamente come limite).
- **Riferimento**: spec.md, D6; divergenza 1 della revisione 003, ereditata da data_model.md §19.

### D7 — Trattamento degli zeri

- **Decisione**: ogni misura che tocca la popolarità (in particolare `BQ2-K1`) pubblica accanto al proprio valore la quota di tracce a popolarità zero del segmento, letta da `is_popularity_zero`/`is_high_zero_genre` su `fact_track_segment`/`dim_segment`.
- **Motivazione**: la feature 003 (D1) ha già deciso di non eliminare le tracce a popolarità zero; l'operatore mancante è l'obbligo di pubblicazione, non una nuova decisione sui dati — senza questo obbligo un consumatore della misura non saprebbe quanto del segnale è comprimibile a zero.
- **Alternative scartate**: nessuna — è la traduzione diretta in operatore di una decisione sui dati già chiusa, non una scelta fra opzioni.
- **Riferimento**: spec.md, D7; divergenza 6 della revisione 001, dati chiusi da feature 003 D1, modello dati da data_model.md §14.

### D8 — Direzione della graduatoria (voce minore, `R13`)

- **Decisione**: la direzione residua non-BQ3 di `R13` si chiude dichiarando esplicitamente il verso di ordinamento (crescente/decrescente) per ciascun KPI a cui `R13` si applica ancora, con lo stesso criterio di stretta disuguaglianza già usato in D3/D4.
- **Motivazione**: `R13` lascia ambiguo solo il verso, non la sostanza della misura; fissarlo con la stessa convenzione già adottata altrove evita di introdurre una seconda regola di direzione nel documento.
- **Alternative scartate**: nessuna — ambiguità di forma, non di sostanza.
- **Riferimento**: spec.md, D8; R13 della revisione 001, parte residua non-BQ3 (la parte BQ3 è già chiusa dalla feature 004).

### D9 — `BQ1-K1`: l'operatore di C1, il rapporto della North Star, e l'invariante sul dato trasformato

- **Decisione** (tre parti, si chiudono insieme perché sono lo stesso passaggio su `BQ1-K1`):
  - **D9.1**: l'invariante che rende valido il numeratore 375 (letto solo in `reports/data_profile.json`, sul dato di origine) anche sul dato trasformato, argomentato via `NF.shape.rows` = `CL.NF.titles.rows.after` (8.807 = 8.807) e la natura non distruttiva dei tre soli record riparati (`CL.NF.duration.repaired.rows`, riparazione per field-shift, non imputazione/eliminazione).
  - **D9.2**: l'operatore di C1 — graduatoria delle 42 categorie per conteggio titoli, contato per riga di `bridge_title_category` raggruppata per categoria (non sul totale di 8.807 titoli distinti, non sul totale di 19.323 assegnazioni), C1 soddisfatta se `Music & Musicals` supera la mediana delle 42 categorie, condizione stretta.
  - **D9.3**: il rapporto 375/8.807 resta non pubblicato accanto alla frase sulla North Star finché non viene esplicitamente calcolato e ancorato con un identificativo proprio — pubblicare numeratore e denominatore fianco a fianco non equivale a pubblicare il rapporto (regola D5 del progetto).
- **Motivazione**: la revisione della regia (rilievi B1/B2) ha trovato che la spec dichiarava C1 come condizione della North Star senza mai definirne l'operatore, e che l'unico numero disponibile (375) esiste solo sul dato di origine — le tre parti si chiudono insieme perché sono la stessa lacuna vista da tre angoli dello stesso KPI.
- **Alternative scartate**: ricontare `Music & Musicals` sul dato trasformato invece di argomentare l'invariante (violerebbe il precedente FR-032 della 002 sui conteggi ancorati all'origine); pubblicare il rapporto come implicito nella giustapposizione (esplicitamente vietato da D5/CLAUDE.md).
- **Riferimento**: spec.md, D9 (D9.1-D9.3); divergenza 4 della revisione 002; C1 della North Star, business_case.md §3; correzioni B1/B2/B3 della revisione della regia sulla spec di questa feature.

## Esito

Nessun `NEEDS CLARIFICATION` residuo. La Fase 1 procede direttamente sulla base di queste nove decisioni.
