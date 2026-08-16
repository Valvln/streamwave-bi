# Fase 0 — Ricognizione tecnica

**Feature**: 004 Synthetic Business Metrics · **Data**: 2026-08-16 · **Spec**: [spec.md](./spec.md)

Nessun `NEEDS CLARIFICATION` era rimasto aperto dalla spec. Questa fase serve quindi a due cose: scegliere dove vivono gli artefatti e con quale aritmetica si calcolano i sei valori, e **ispezionare gli strumenti che la feature eredita** dalla 002 e dalla 003 prima di estenderli. La seconda parte ha prodotto quattro ritrovamenti, e due di essi avrebbero causato un difetto silenzioso.

---

## Ritrovamenti

### F1 — `data/external/` è già ignorato da git

È la cartella che il nome suggerisce per un valore preso da una fonte esterna, ed è una trappola: [`.gitignore`](../../.gitignore) contiene `data/external/*`. Un file dei parametri collocato lì **non sarebbe versionato**, e la condizione 2 della constitution — il valore congelato in un artefatto del repository — sarebbe violata senza che nulla lo segnali. Il file sparirebbe al primo clone e la derivazione fallirebbe su una copia pulita, cioè esattamente nel caso che SC-002 verifica.

Conseguenza: T1 sceglie una cartella nuova e la verifica di committabilità entra fra i task, invece di essere data per scontata.

### F2 — Lo spazio dei nomi di `conventions` è piatto, e una chiave utile è già occupata

Il controllo unisce le mappe `values`, `catalogs` e `conventions` di tutti gli artefatti e **fallisce sulle collisioni**. I `values` sono protetti da prefissi disgiunti — oggi `NF.`, `SP.`, `CL.`, `X.` — ma `conventions` no: le sue chiavi sono nomi piatti come `rounding_decimals`, `missing`, `dispersion`.

`rounding_decimals` **esiste già**. La regola di arrotondamento che FR-015 impone di dichiarare fra le convenzioni avrebbe preso quel nome per la via più naturale, con contenuto diverso, e il controllo sarebbe fallito — nel caso migliore. Nel caso peggiore l'avrebbe preso con contenuto *identico*, la collisione non sarebbe scattata, e due feature avrebbero condiviso una convenzione che nessuna delle due ha inteso condividere.

Conseguenza: **T4**, tutte le chiavi di convenzione della feature portano il prefisso `bq3_`.

### F3 — La trappola di determinismo sta nella banda, non nel prodotto per 4,00 €

Il sospetto naturale cadeva sul prodotto: moltiplicare un tasso per un prezzo in virgola mobile. La verifica lo assolve e accusa l'altro passaggio.

```
0,11 × 4,00  →  0.44                    esatto
0,29 × 4,00  →  1.16                    esatto
0,07 × 1,5   →  0.10500000000000001     ← la banda
0,29 × 1,5   →  0.43499999999999994     ← la banda
```

Il secondo caso è il peggiore possibile: il valore vero è `0,435`, cioè esattamente il punto di mezzo che l'arrotondamento a due cifre deve decidere, e la rappresentazione binaria lo colloca **sotto**. `round(0.435, 2)` restituisce `0,43` dove la regola dichiarata direbbe `0,44`. Il difetto non si manifesterebbe come errore ma come una cifra sbagliata in un artefatto verde, su un valore di confine, dipendente dal benchmark che non conosciamo ancora — cioè scopribile solo dopo aver scelto la fonte, quando riaprire l'aritmetica costa di più.

È l'analogo strutturale del ritrovamento F6 della 003 sulla conversione di `date_added`: una funzione che sulla macchina di sviluppo dà il risultato giusto per caso.

Conseguenza: **T5**, tutta l'aritmetica in `decimal.Decimal`, mai in virgola mobile, e la modalità di arrotondamento dichiarata invece che ereditata.

### F4 — `docs/business_case.md` non è sotto controllo, e ora è confermato

`DOCUMENTS` in `scripts/check_audit_coherence.py` contiene due voci: `docs/data_audit.md` e `docs/data_cleaning.md`. Il business case non c'è. È la premessa di fatto su cui poggiano FR-025a e FR-027a — un numero scritto nella sua prosa non ha ancora e nessuno lo verifica — ed è ora verificata invece che assunta.

**Ciò che questa feature non fa, e va detto**: non aggiunge il business case a `DOCUMENTS`. Marcarlo significherebbe ancorare i numeri di un artefatto già mergiato scritto prima che la grammatica esistesse, che è lavoro di rimarcatura dello stesso tipo già tracciato in roadmap per `docs/data_audit.md`. La feature lo **evita alla radice** non scrivendovi numeri nuovi.

---

## Decisioni tecniche

### T1 — Il file dei parametri vive in `data/benchmarks/`, ed è versionato

**Le opzioni**: `data/external/` (naturale per nome, ma ignorato — F1); `reports/` (versionata, ma è la cartella degli artefatti *generati*, e questo è curato a mano); `specs/004-.../` (versionata, ma `CLAUDE.md` esclude che un artefatto pubblicato deleghi a una cartella di lavorazione); una cartella nuova sotto `data/`.

**La decisione**: **`data/benchmarks/bq3_tier_upgrade.json`**, versionato, in sola lettura per ogni script.

**La ragione, che è un'inversione dichiarata della regola di `data/`**: le altre cartelle di `data/` non sono versionate **perché sono riproducibili** — `scripts/download_data.sh` ricostruisce `raw/`, la pipeline della 003 ricostruisce `processed/`. Questa lo è **perché non lo è**: la raccolta del benchmark è un passaggio umano che nessuno rieseguirà, ed è precisamente la ragione per cui la condizione 3 della constitution impone di congelarne l'esito. La regola non viene violata, viene applicata al proprio criterio invece che alla propria lettera.

La cosa va scritta in [`data/README.md`](../../data/README.md), che oggi dichiara «i dataset raw non sono versionati» e un layout a tre cartelle: chi legge quella pagina deve trovare la quarta e capire perché si comporta al contrario.

### T2 — JSON, sola libreria standard

Coerente con i due artefatti esistenti e con la scelta T1 della 003. Nessuna dipendenza nuova per leggere un file di poche decine di righe. La citazione contiene prosa — titolo, assunzione di trasferimento, scarto di misura — e JSON la ospita senza problemi; la scomodità di scrivere prosa dentro JSON è reale ma si paga una volta sola, su un file che nasce a mano e non viene più riscritto.

**Escluso YAML/TOML**: introdurrebbero una dipendenza (`pyyaml`) o un modulo disponibile solo da 3.11 (`tomllib`) per un guadagno di leggibilità su un file che si apre due volte in tutto il progetto.

### T3 — L'artefatto dei valori è `reports/bq3_scenarios.json`, con prefisso `BQ3.`

Sta in `reports/` perché è generato, come `data_profile.json` e `cleaning_report.json`, ed è versionato per FR-018a. Espone `values`, `conventions`, `sources` e `schema_version`, nella forma che `load_artifacts()` già sa unire.

Il prefisso degli identificativi è **`BQ3.`**, disgiunto dai quattro esistenti (`NF.`, `SP.`, `CL.`, `X.`) — verificato, non assunto. La disgiunzione non viene comunque data per buona: la verifica di collisione del controllo resta attiva e si estende al terzo artefatto senza modifiche, perché è già scritta in forma generica su una lista di artefatti.

### T4 — Le chiavi di `conventions` portano il prefisso `bq3_`

Conseguenza diretta di F2. `bq3_band_factor_low`, `bq3_band_factor_high`, `bq3_rounding`, `bq3_price_delta_eur`. Il prefisso è brutto e necessario: lo spazio è piatto, condiviso fra tutti gli artefatti, e una collisione silenziosa vi è possibile in un modo che nei `values` non è.

### T5 — Tutta l'aritmetica in `decimal.Decimal`

Conseguenza diretta di F3. I valori si leggono dal file dei parametri **come stringhe** e si convertono in `Decimal`, mai passando per `float`. L'arrotondamento usa `ROUND_HALF_UP` dichiarato esplicitamente e non la modalità predefinita: `Decimal` usa `ROUND_HALF_EVEN`, che su `0,435` darebbe `0,44` e su `0,445` darebbe `0,44` — corretto ma controintuitivo per chi verifica a mano, ed è chi verifica a mano il destinatario di questo progetto.

La modalità scelta entra fra le convenzioni dell'artefatto (`bq3_rounding`), così che il lettore possa rifare il conto sapendo quale regola applicare.

### T6 — La banda è moltiplicativa relativa, con fattore 0,50

**La forma**: `worst = base × (1 − k)`, `best = base × (1 + k)`. È la lettura letterale di «simmetrici in termini relativi» di D2.

**Il valore**: **k = 0,50**. Worst è metà del benchmark, best è una volta e mezzo.

**Perché un numero tondo, quando D4 della 003 ha respinto il 60% proprio perché tondo.** L'obiezione va affrontata, non evitata, perché i due casi sembrano identici e non lo sono. Il 60% della 003 era una **soglia su una grandezza osservata**, dove esiste un criterio migliore di un numero tondo — e infatti la 003 lo ha trovato, nella proprietà della mediana. Qui la grandezza non è osservata da nessuno: k è per costruzione una **stipulazione** sulla fiducia nel trasferimento, e non esiste alcun criterio che la derivi da qualcosa. In questa condizione la rotondità non è l'assenza di una ragione, **è la ragione**: un k = 0,37 comunicherebbe a chi legge che il numero viene da un calcolo, e non ne viene. Una stipulazione grossolana deve avere l'aspetto di una stipulazione grossolana.

**Che cosa dichiara k = 0,50**: che l'analista considera il trasferimento incerto entro un fattore 3 fra i due estremi, e che lo scenario *worst* è «metà di quanto ha fatto chi il verticale ce l'ha già». È l'affermazione più grossolana che sia ancora informativa, ed è coerente con §7 del business case, che chiede al board di considerare *worst* come il caso da poter sostenere.

**Il vincolo di FR-011a vale su questo numero**: k è fissato **qui**, in fase di piano, prima che la ricognizione sul benchmark abbia inizio. Vedi T7.

### T7 — L'ordine di esecuzione è imposto, e il commit lo testimonia

FR-011a richiede che i fattori precedano il benchmark e che la precedenza sia dichiarata. Il piano la rende verificabile invece che asserita:

1. il file dei parametri nasce con i **soli** fattori, la loro ragione e il differenziale di A4 — nessun campo del benchmark, nemmeno vuoto o segnaposto;
2. commit;
3. solo dopo comincia la ricognizione, che aggiunge valore, citazione, scarto di misura e assunzione di trasferimento;
4. commit separato.

Chi dubita apre `git log` sul file e guarda i due commit. Un campo segnaposto lasciato pronto al passo 1 vanificherebbe la garanzia, perché renderebbe indistinguibile «fissato prima» da «riempito dopo»: per questo il passo 1 dice *nemmeno vuoto*.

### T8 — Il documento è `docs/bq3_scenarios.md`, in severità stretta

Nome in inglese come gli altri file (convenzione della constitution), prosa in italiano. Entra in `DOCUMENTS` con `strict=True`.

Tre modifiche discendono su [`docs/convenzioni-marcatura.md`](../../docs/convenzioni-marcatura.md), che è la fonte unica e non può descrivere uno stato superato: §3 dice «oggi `reports/data_profile.json` e `reports/cleaning_report.json`» e da qui in avanti sono tre; la tabella di §5 elenca due documenti con la propria severità e ne avrà tre; la tabella di provenienza in coda registra data e feature.

### T9 — Nessun framework di test: verifica per esecuzione

Come la 002 e la 003. I comportamenti verificabili sono meno di dieci e si verificano da riga di comando secondo [quickstart.md](./quickstart.md). Introdurre `pytest` per una derivazione senza rami costerebbe più della verifica che sostituisce.

La prova che conta è comunque una sola e non è unitaria: **doppia esecuzione, diff vuoto, su una copia priva di `data/raw/` e senza rete**.

---

## Alternative valutate e scartate

| Alternativa | Perché scartata |
|---|---|
| Generazione stocastica con seed fisso | decisione D1 della spec: nessun consumatore di righe, nessuna informazione aggiunta, e **nessun N** da cui estrarre, perché la base utenti non è quantificata |
| `data/external/` per il file dei parametri | ignorato da git (F1): il valore non sarebbe congelato |
| Convenzioni senza prefisso | collisione silenziosa possibile nello spazio piatto di `conventions` (F2) |
| Aritmetica in virgola mobile | produce `0,43499999999999994` sul confine di arrotondamento (F3) |
| `pandas` o `numpy` | sei valori scalari. La 003 aveva già escluso i dataframe per 122.807 righe |
| Un framework di orchestrazione a LLM per la raccolta | escluso dalla roadmap e dal prompt di consegna: il passaggio produce un valore congelato che nessuno riesegue, e l'orchestrazione resterebbe inerte dopo la prima esecuzione, al prezzo di una dipendenza e di una chiave API |
| Marcare `docs/business_case.md` e aggiungerlo a `DOCUMENTS` | è rimarcatura di un artefatto già mergiato, dello stesso tipo già tracciato in roadmap per `docs/data_audit.md`. La feature evita il problema non scrivendovi numeri nuovi (FR-025a, FR-027a) |
