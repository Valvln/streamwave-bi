# Contratto — `data/curated/dim_category_mood.json` per chi legge, in particolare la `007`

**Feature**: 006 Content Taxonomy Bridge · **Data**: 2026-08-20

Questo file esiste perché la `007`, che pubblicherà `BQ1-K3`, `BQ2-K2` e `BQ2-K3`, deve poter leggere questo artefatto senza riaprire la `006` per capirne le regole. Ciò che segue è ciò su cui la `007` può contare; ciò che non è scritto qui non è garantito.

---

## 1. Il file non viene mai rigenerato

`data/curated/dim_category_mood.json` è congelato a mano (FR-012). Nessuno script del repository lo scrive. Se il suo contenuto cambia, cambia perché una persona lo ha corretto dopo aver trovato un errore — mai come effetto collaterale di una pipeline.

## 2. Ogni valore che dipende da questa tabella dichiara la versione

Campo di primo livello `version` (intero, da `1`), incrementato a ogni correzione post-congelamento (FR-015, D5). **La `007` MUST leggere `version` e riportarlo accanto a ogni valore pubblicato che dipende da questa tabella** — in dashboard, nel proprio documento, ovunque `BQ1-K3`/`BQ2-K2`/`BQ2-K3` compaiano. Senza questo legame, una correzione della `006` lascerebbe a valle numeri "giusti quando sono stati scritti", indistinguibili da quelli ancora validi (precedente: il totale a ~65 ore corretto il 2026-08-17, citato dalla roadmap).

## 3. Come ricostruire una riga

Non esiste un campo `rows`. La tabella vive dentro `values`, filtrando per prefisso e raggruppando per categoria:

```python
import json, re

data = json.loads(open("data/curated/dim_category_mood.json").read())
rows: dict[str, dict[str, str]] = {}
for vid, payload in data["values"].items():
    if not vid.startswith("MOOD.category."):
        continue
    rows.setdefault(payload["category"], {})[payload["axis"]] = payload["value"]

# rows["Action & Adventure"] == {"mood_energy": "0.95", "mood_valence": "0.65", "mood_danceability": "0.35"}
```

> **Corretto il 2026-08-20, in fase di implementazione (T042).** Il commento qui sopra riportava `0.70` / `0.55` / `0.60`: erano i valori dell'esempio di forma scritto in fase di piano, quando nessun valore esisteva ancora, e dopo il congelamento erano diventati **falsi**. Chi avesse eseguito il frammento per verificare il contratto avrebbe visto l'asserzione fallire e non avrebbe saputo se a sbagliare fosse il file o il contratto. Sono ora i valori realmente congelati, verificabili eseguendo il codice sopra. Vale la regola della `003`: dove contratto e implementazione divergono, è il contratto a doversi correggere.

`catalogs.mood_categories` elenca le chiavi attese; se `rows` ne contiene di meno, la copertura è parziale ed è dichiarata altrove nel file (§5).

## 4. La scala è quella del lato musicale, senza eccezioni

I tre valori di ogni cella sono decimali `0-1`, sullo stesso significato di estremo di `energy`/`valence`/`danceability` sul lato musicale (D2, FR-013). **La `007` non deve normalizzare, riscalare o reinterpretare questi valori** prima di usarli nelle due regole di aggregazione già fissate in §11 di `docs/data_model.md` — minimo/massimo non ponderati per `BQ1-K3`, mediana ponderata sul ponte per `BQ2-K2`. Se un valore cade fuori da `0-1`, il file non dovrebbe essere stato congelato (Edge case della spec) — la `007` che lo trovasse fuori scala deve fermarsi e segnalarlo, non correggerlo silenziosamente.

## 5. La copertura può essere parziale, e se lo è va letta da `catalogs.mood_categories` contro `catalogs.netflix_categories_normalized`

Copertura attesa: 42 righe (FR-014). Se `MOOD.coverage.rows` è inferiore a 42, alcune categorie non hanno profilo. Il documento pubblicato (`docs/content_taxonomy_bridge.md`) dichiara quali e perché; **la `007` deve applicare lo stesso comportamento sulle categorie mancanti che quel documento dichiara** — non inventarne uno proprio (per esempio non deve assumere silenziosamente un valore neutro).

## 6. La confidenza non sale mai

`BQ1-K3`, `BQ2-K2`, `BQ2-K3` restano a confidenza `media` in ogni artefatto che li pubblica, indipendentemente da quanto accurata sia stata la costruzione di questa tabella (D4, FR-017). **La `007` non deve promuoverli a confidenza alta** in nessuna circostanza: è un vincolo di §15 di `docs/data_model.md`, non una scelta che questa feature o la successiva possano rinegoziare.

## 7. La fonte è `Sintetico`, mai `Benchmark (esterno)`

D3, FR-018. Non esiste un operatore terzo da citare: la tabella è un'assegnazione dell'analista su proposta di un LLM, verificata e congelata secondo la quinta fonte della constitution v1.2.0.

## 8. Nessun attributo di record individuale

Il file non contiene, e non deve mai contenere, titoli, trame, cast o altri attributi specifici di una riga di `dim_title` (D7, FR-020). Se la `007` avesse bisogno di collegare un profilo di mood a titoli specifici, lo fa attraverso `bridge_title_category` e `dim_category` del modello dati — non attraverso questo file, che resta a grana categoria.

## 9. Il registro di verifica non è un secondo artefatto da consumare

Il campo `verification` (D9.1) documenta come la tabella è stata costruita. Non è pensato per essere letto da una pipeline: è pensato per essere letto da una persona che vuole sapere quanto la revisione ha corretto. La `007` non ha bisogno di leggerlo per calcolare un KPI.

**Aggiunta del 2026-08-20 (T042): il registro contiene un campo che il piano non aveva previsto, `criterion_findings`.** Sono difetti del **criterio** trovati dalla verifica e non contestazioni a singole celle — la categoria che `changes` non poteva contenere. Uno di essi, `CF-1`, è una contraddizione fra due regole del criterio che tocca più celle di quante la verifica ne abbia spostate: quelle celle sono rimaste ferme perché sceglierne una delle due regole sarebbe stato decidere sul criterio, non verificare contro il criterio.

Che cosa questo significa per la `007`: **la versione `1` di questa tabella porta un difetto noto e dichiarato**, e la sua risoluzione comporterà un incremento di `version` con celle spostate. È il caso concreto per cui §2 esiste. La `007` non deve leggere `criterion_findings` per calcolare, ma chi pubblica un valore a valle senza dichiararne la versione lo renderà indistinguibile dai valori ancora validi nel momento in cui quella correzione arriverà.
