# Fase 0 — Ricognizione tecnica

**Feature**: 006 Content Taxonomy Bridge · **Data**: 2026-08-20 · **Spec**: [spec.md](./spec.md)

Nessun `NEEDS CLARIFICATION` è rimasto aperto dalla spec: le nove decisioni la chiudono. Questa fase serve quindi a tre cose: verificare che gli strumenti ereditati (`check_audit_coherence.py`, lo spazio dei nomi degli artefatti, `data/`) reggano l'estensione senza trappole silenziose, come nella 004; trovare la forma dei tre artefatti nuovi; e cercare, prima di scriverla, se il criterio del passo 1 di D1 possa ancorarsi a qualcosa che esiste già.

L'ultima ricerca ha trovato più di quanto cercasse.

---

## Ritrovamenti

### F1 — `data/curated/` non è ignorata da git, a differenza della trappola della 004

La 004 aveva trovato `data/external/*` in `.gitignore`: la cartella che il nome suggeriva per un valore esterno non lo avrebbe versionato. Verificato qui lo stesso rischio sul nome che l'Assumption della spec propone:

```
git check-ignore -v data/curated/test.json   → nessun output, non ignorata
```

`.gitignore` copre solo `raw/*`, `interim/*`, `processed/*`, `external/*`. `curated/` non compare. Nessuna trappola: il percorso proposto nella spec è committabile come scritto, e non serve una cartella diversa da quella che l'Assumption suggeriva.

### F2 — Lo spazio dei nomi di `conventions` è ancora piatto

Stesso fatto della F2 della 004, verificato di nuovo perché nulla garantisce che due feature lo trovino nello stesso stato: `conventions` in `load_artifacts()` è un dizionario piatto condiviso da tutti gli artefatti uniti, senza prefissi per artefatto. Le chiavi che la 006 introdurrà devono quindi portare un prefisso proprio, come `bq3_` per la 004.

Conseguenza: **T2**, prefisso `mood_`.

### F3 — Gli estremi degli assi sul lato musicale sono già misurati e già ancorati

Questo è il ritrovamento che conta. D2 impone che il criterio ancori gli estremi di ciascun asse a "osservazioni reali disponibili sul lato musicale", e D7 vieta di farlo citando un titolo o una traccia individuale. Le due condizioni insieme sembravano lasciare poco spazio: un ancoraggio che non sia un titolo e non sia un'affermazione a mente.

`reports/data_profile.json` — prodotto dalla 002, già versionato, già dentro `ARTIFACTS` — contiene per ciascuno dei tre campi (`energy`, `valence`, `danceability`) minimo, massimo, mediana e quartili sull'intero insieme delle 114.000<!--#--> tracce:

```
SP.num.energy.min       → 0,0000     SP.num.energy.max       → 1,0000
SP.num.valence.min      → 0,0000     SP.num.valence.max      → 1,0000
SP.num.danceability.min → 0,0000     SP.num.danceability.max → 1,0000
```

I tre assi occupano **per intero** l'intervallo `0-1` sul dato osservato — non è un'assunzione della `006`, è un fatto già misurato e già anchorabile con identificativi esistenti. Il criterio può quindi ancorare i propri estremi non a un titolo (vietato da D7) né a un'affermazione qualitativa (che D2 non accetterebbe come verifica), ma alla **distribuzione aggregata già pubblica**: "l'estremo basso dell'asse energia corrisponde a ciò che un brano con `energy` vicino al minimo osservato (`SP.num.energy.min`) rappresenta: assenza quasi totale di intensità percepita", eccetera. È un'osservazione aggregata sul lato musicale, esattamente la categoria che D7 ammette, e arriva già marcata secondo la grammatica di `docs/convenzioni-marcatura.md`.

**Conseguenza**: il criterio (`docs/mood_assignment_criteria.md`) può e deve citare questi sei identificativi come proprio ancoraggio di scala, invece di descriverli in prosa libera. Non chiude da sola la verifica indipendente di D9.1 — quella resta un giudizio su 126 righe — ma le dà un metro concreto sul punto che D2 chiama "l'obbligo che conta di più": chi verifica può confrontare l'estremo dichiarato dal criterio con un numero già pubblicato, invece di doverlo giudicare a occhio.

### F4 — Le 42 categorie non collidono sotto normalizzazione a slug

L'identificativo per cella (T3) richiede di trasformare ogni nome di categoria in una chiave valida. Verificato su `catalogs.netflix_categories_normalized` (`reports/cleaning_report.json`) con la normalizzazione più semplice possibile — minuscolo, ogni carattere non alfanumerico a `_`, tagli ai bordi:

```
42 categorie → 42 slug distinti, nessuna collisione
```

`TV Action & Adventure` → `tv_action_adventure`, `Action & Adventure` → `action_adventure`: restano distinti perché il prefisso `tv_` non si perde. Nessuna coppia di categorie collide. Non serve uno schema di normalizzazione più elaborato, né una tabella di eccezioni.

### F5 — Questa feature non produce un secondo artefatto generato, e questo cambia la forma di `ARTIFACTS`

Nella 004 il file curato a mano (`data/benchmarks/bq3_tier_upgrade.json`) e l'artefatto che entra in `ARTIFACTS` (`reports/bq3_scenarios.json`) sono **due file distinti**: uno stipulato, uno derivato da uno script deterministico. Qui non esiste un passo di derivazione — D1 lo esclude esplicitamente, "nessuno script chiama mai il modello" **e** nessuno script rigenera la tabella verificata (FR-012). L'unico artefatto di numeri che la feature produce è `data/curated/dim_category_mood.json` stesso, ed è quello che FR-023 chiede di entrare in `ARTIFACTS` come quarto membro.

**Conseguenza**: `dim_category_mood.json` deve portare la forma che `load_artifacts()` sa unire — chiavi `values`, `catalogs`, `conventions`, `schema_version` — **oltre** a essere il congelamento non riscrivibile che D1 richiede. Non è un'incompatibilità: nessuno dei due obblighi impone che il file sia generato, impone solo la sua forma e la sua immutabilità dopo il congelamento. Ma è la ragione per cui il modello dati di questa feature (T3) non replica la coppia file-parametri/file-artefatto della 004.

---

## Decisioni tecniche

### T1 — `data/curated/`, versionata, confermata da F1

Nessuna cartella nuova da inventare: il percorso che l'Assumption della spec proponeva è committabile. La motivazione per esteso è già scritta in [`data/README.md`](../../data/README.md) in questa stessa fase, come la spec richiede.

### T2 — Prefisso `mood_` per le chiavi di `conventions`

Conseguenza diretta di F2. `mood_scale_anchor`, `mood_rounding`.

### T3 — Un solo artefatto, e il suo spazio `values` **è** la tabella, non una sua copia

Conseguenza di F5. `data/curated/dim_category_mood.json` porta:

- **`values`**: 126 identificativi `MOOD.category.<slug>.<asse>`, uno per cella — è la forma canonica della tabella, non un doppione da tenere allineato a mano; più tre identificativi aggregati (`MOOD.coverage.rows`, `MOOD.table.version`, `MOOD.review.changes_count`) che il documento pubblicato userà per i propri numerali (FR-024, regola D5 della 003 sulle affermazioni derivate — un conteggio è esso stesso un valore misurato, non un fatto libero).
- **`catalogs.mood_categories`**: le 42 chiavi `category`, la stessa lista che D6/FR-019 confronta con `catalogs.netflix_categories_normalized`, e che raddoppia come forma letterale per citare una categoria in prosa (`` `Horror Movies`<!--@catalogs.mood_categories--> ``).
- **`conventions`**: `mood_scale_anchor` (rimanda ai sei identificativi di F3), `mood_rounding`.
- **`version`**, **`verification`** (registro di D9.1: `changes_count`, l'elenco delle righe spostate con il punto del criterio citato, la dichiarazione esplicita quando il conteggio è zero): campi propri, fuori dai tre spazi che `load_artifacts()` unisce — la stessa posizione di `sources`/`denominators`/`outputs` negli artefatti esistenti, che il merge ignora senza doverli conoscere.

**Perché non un campo `rows` separato.** Un `rows` accanto a `values` con lo stesso contenuto in due forme sarebbe una seconda fonte di verità dentro lo stesso file: nulla la riscriverebbe automaticamente allineata, perché il file non è mai rigenerato da uno script (FR-012). Un'unica rappresentazione — `values`, filtrabile per prefisso `MOOD.category.` — è l'unica forma che non può divergere da se stessa. Il [contratto per la `007`](./contracts/dim-category-mood-contract.md) descrive come ricostruire una riga.

**Perché tutte e 126 le celle, e non solo le aggregate.** Costano poco — sono voci JSON minime — e tolgono a chi scriverà il documento pubblicato la scelta caso per caso di quali esempi marcare: qualunque categoria citata come esempio (D7 lo ammette a livello di categoria) ha già il proprio ancoraggio pronto, senza bisogno di tornare su questo file per aggiungerlo a metà stesura del documento.

### T4 — Valori come stringhe decimali, mai `float`

Stessa ragione della T5 della 004 (F3 di quella fase): un valore letto da JSON come `float` e riscritto da uno script introduce artefatti di rappresentazione binaria. Qui nessuno script scrive il file dopo il congelamento, quindi il rischio è più piccolo — ma la lettura (`check_audit_coherence.py`, e la 007 a valle) confronta `display` carattere per carattere, e un valore scritto come `0.70` invece di `"0.70"` cambia come `json.dumps` lo pretty-printerebbe in un'eventuale rigenerazione futura del solo scopo di ispezione. La convenzione dell'intero progetto (002-004) scrive i decimali come stringhe; questa feature non introduce un'eccezione.

### T5 — Arrotondamento a due decimali, dichiarato in `mood_rounding`

I tre assi sul lato musicale (§11 di `docs/data_model.md`) non dichiarano una precisione oltre "decimale `0-1`"; lo stesso vale qui per costruzione (D2). Due decimali è la precisione con cui `energy`/`valence`/`danceability` compaiono già nei valori esposti da `reports/data_profile.json` (`0,6414`, quattro decimali in realtà — ma il criterio non richiede quella granularità per un giudizio dell'analista, e pubblicare più di due cifre significative per un valore assegnato, non misurato, implicherebbe una precisione che la costruzione non ha, violando il principio I). `mood_rounding` dichiara la regola e la ragione, sul modello di `bq3_rounding`.

### T6 — Nessun framework di test: verifica per esecuzione e per ispezione

Come nella 002, 003, 004. I comportamenti verificabili di questa feature sono più procedurali che aritmetici — precedenza in history, indipendenza dichiarata, copertura, fallimento meccanico — e si verificano da riga di comando o per lettura, secondo [quickstart.md](./quickstart.md).

### T7 — Il criterio e il documento pubblicato non condividono la severità di marcatura

Solo `docs/content_taxonomy_bridge.md` entra in `DOCUMENTS` (FR-023). `docs/mood_assignment_criteria.md` **non** vi entra: la spec non lo richiede, e forzarlo aggiungerebbe una severità che nessun requisito impone a un documento che precede l'esistenza di ogni valore per costruzione (D1, passo 1) — marcarlo meccanicamente presupporrebbe un artefatto di numeri che al momento del suo commit non esiste ancora. Il vincolo di ancoraggio del criterio (FR-004) resta comunque verificabile a occhio, come per ogni sezione di spec che cita identificativi già pubblicati.

### T8 — Estensione di `check_audit_coherence.py`: quarto artefatto, quinto documento, guardia di copertura separata dal ciclo dei marcatori

Tre modifiche distinte, non una:

1. `ARTIFACTS` guadagna un quarto percorso, `MOOD = REPO / "data" / "curated" / "dim_category_mood.json"`. `load_artifacts()` non cambia: il ciclo su `("values", "catalogs", "conventions")` è già generico.
2. `DOCUMENTS` guadagna `(REPO / "docs" / "content_taxonomy_bridge.md", True, "feature 006")`, in severità stretta fin dalla nascita — non c'è un periodo di avviso da onorare, perché non esiste un documento precedente scritto prima che la regola stretta esistesse.
3. Una funzione nuova, chiamata da `main()` **prima** del ciclo sui documenti e indipendente da esso: confronta l'insieme `catalogs.mood_categories` dell'artefatto unito con `catalogs.netflix_categories_normalized` come insiemi, e se divergono aggiunge l'esito a `failed` con la differenza simmetrica esplicita — quali categorie mancano da una parte, quali dall'altra. È il meccanismo di D6/FR-019: non è un marcatore nella prosa, è un controllo sui dati dell'artefatto stesso, e per questo vive fuori dal ciclo `check_markers`, che opera sul testo di un documento.

### T9 — La verifica indipendente di D9.1 non produce un file a parte

Il registro (`verification` dentro `dim_category_mood.json`, T3) è già l'esito di D9.1. Non serve un secondo artefatto per "la verifica": il campo dedicato che FR-010 richiede vive dentro la tabella congelata stessa, perché la verifica e il congelamento sono lo stesso commit (passo 3 e passo 4 di D1 restano distinti come lavorazione, ma l'esito della verifica è ciò che rende la tabella congelabile, non un documento separato che la precede).

---

## Alternative valutate e scartate

| Alternativa | Perché scartata |
|---|---|
| Due file, sul modello esatto della 004 (parametri curati + artefatto generato) | non esiste un passo di derivazione: D1 esclude ogni script che tocchi il valore dopo il congelamento (FR-012). Un secondo file sarebbe una copia senza una regola che lo produca |
| Campo `rows` accanto a `values`, con lo stesso contenuto in due forme | seconda fonte di verità nello stesso file, senza uno script che le tenga allineate — il rischio di drift esiste proprio perché nessuno script riscrive mai il file |
| Ancoraggio del criterio a titoli o trame specifiche | vietato da D7/FR-003: attributi di record individuali negli artefatti versionati |
| Marcatura meccanica anche di `docs/mood_assignment_criteria.md` | nessun requisito la chiede; il documento precede per costruzione ogni valore che potrebbe marcare |
| Valori JSON come numeri invece che stringhe | rischio di rappresentazione binaria imprecisa alla prima rilettura/riscrittura da script, e scostamento dalla convenzione già in uso nel progetto (002-004) |
| Normalizzazione degli slug con tabella di eccezioni manuali | non necessaria: la normalizzazione più semplice non produce collisioni sulle 42 categorie (F4) |
