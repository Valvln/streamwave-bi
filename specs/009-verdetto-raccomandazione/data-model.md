# Modello dati — le voci che questa feature aggiunge

Che cosa `scripts/build_kpi_measures.py` calcola in più, con quale chiave lo pubblica, e da quali valori esistenti lo deriva. **Nessuna tabella nuova, nessun file nuovo, nessuna lettura di dati che lo script non faccia già.**

---

## 1. Il principio che governa questo modello

Le sei voci nuove sono tutte **derivate da valori che lo script ha già in memoria** quando arriva a calcolarle. Nessuna richiede una passata sui dati, nessuna apre un file che lo script non legga già. È la ragione per cui la funzione nuova sta in fondo alla catena, dopo che le tre misure che la alimentano sono state calcolate.

Ne discende un vincolo di implementazione che vale la pena scrivere prima del codice: **la funzione non ricalcola nulla**. Riceve i valori esatti — non quelli arrotondati per la pubblicazione — e li confronta. Arrotondare prima di un confronto di soglia è precisamente ciò che la convenzione `kpi_rounding` vieta, e qui il confronto *è* la misura.

---

## 2. Le voci nuove

### 2.1 La condizione `C2`

| Chiave | Unità | Valore | Formula |
|---|---|---|---|
| `KPI.BQ1K3.c2.threshold` | quota, `0-1` | soglia di maggioranza semplice | stipulazione: `0,50` (decisione `D12`) |
| `KPI.BQ1K3.c2.satisfied` | esito booleano | `C2` è soddisfatta | `mood_profile_overlap > soglia`, confronto **stretto** |
| `KPI.BQ1K3.c2.margin` | quota, `0-1` | margine assoluto | `mood_profile_overlap − soglia` |
| `KPI.BQ1K3.c2.margin_share_of_value` | quota, `0-1` | sovrastima richiesta, come quota del valore | `margine ÷ mood_profile_overlap` |

**Cifre di presentazione**: quattro decimali per tutte e quattro, secondo la regola per unità già in vigore (`kpi_rounding`: quote e indici sul dominio `0-1` a 4 cifre). L'esito booleano non si arrotonda, essendo esatto per costruzione.

**Sulla soglia, che è una voce dell'artefatto pur non essendo una misura.** È lo stesso statuto delle soglie del quadrante di `BQ2-K3`, che vivono nell'artefatto come `KPI.BQ2K3.threshold.demand` e `.affinity`. La ragione è dichiarata in `convenzioni-marcatura.md` §2: «dove una soglia ha un valore registrato fra le convenzioni di un artefatto la si **ancora** invece di marcarla: ancorare è sempre più forte che dichiarare». Una soglia scritta a mano nel documento sarebbe una costante digitata, cioè un numero senza fonte.

**Sulle due voci del margine, e perché sono due** — è la decisione `V9` del piano. Il margine assoluto risponde a «di quanto il valore supera la soglia»; la quota risponde a «di quanto la stima dovrebbe essere gonfiata perché la conclusione cambi», che è la domanda che il limite di `kpi_measures.md` §4.3 pone. **Entrambe dipendono dalla soglia**, e nessuna delle due va pubblicata senza quella dipendenza dichiarata: con una soglia più severa il margine si restringe.

### 2.2 Il verdetto congiunto

| Chiave | Unità | Valore | Formula |
|---|---|---|---|
| `KPI.verdict.conditions_satisfied` | conteggio | quante delle tre condizioni sono soddisfatte | somma dei tre booleani `C1`, `C2`, `C3` |
| `KPI.verdict.all_satisfied` | esito booleano | l'argomento di coerenza è sostenuto | `C1 ∧ C2 ∧ C3` |

**Perché entrambe e non una sola.** Rispondono a domande diverse, ed è la stessa distinzione che `D4` ha già imposto al quadrante e al punteggio di `BQ2-K3`. Il conteggio è ciò che seleziona **quale delle tre letture** di `business_case.md` §3 si applica — tre su tre, due su tre, una o zero — e resta informativo anche in un esito parziale; la congiunzione è l'esito che il business case chiama «argomento sostenuto», e risponde per sì o per no. Pubblicare solo la seconda perderebbe l'informazione che serve a scegliere la lettura; pubblicare solo il primo obbligherebbe chi legge a ricavare la congiunzione, che è un calcolo a mente su valori misurati — vietato da `D5`.

**Il denominatore è una costante di struttura, non una misura**: le condizioni sono tre perché la regola di decisione ne ha tre. Nel documento il numerale «tre» in questa posizione porta il marcatore di non-misurato, non un'ancora.

### 2.3 La dipendenza di versione, che non è una voce nuova

Il verdetto poggia su `C2`, che poggia su `BQ1-K3`, che poggia su `dim_category_mood`. La versione della tabella è **già** nell'artefatto come convenzione `kpi_mood_table_version`, scritta dalla `007b` proprio perché «chi apre solo questo artefatto deve poter leggere su quale versione della tabella dei mood i tre KPI che ne dipendono sono stati calcolati, senza aprirne un secondo».

**Nessuna voce nuova serve**: la convenzione esiste e copre già il caso. Ciò che questa feature aggiunge è l'obbligo, in prosa, che **il verdetto dichiari la dipendenza dove viene pubblicato** — è la condizione 3 delle assegnazioni dell'analista nella constitution, e il contratto di versione di `content_taxonomy_bridge.md` §5: una revisione della tabella **invalida** il valore invece di correggerlo.

---

## 3. I valori esistenti che la feature legge e non ricalcola

Elencati perché la distinzione fra *letto* e *ricalcolato* è la stessa che la `007b` ha dovuto dichiarare per `BQ3`: ricalcolare produrrebbe una seconda copia capace di divergere dall'originale senza che nulla lo segnali.

| Valore | Ancora | Da dove viene | Ruolo qui |
|---|---|---|---|
| `mood_profile_overlap` | `KPI.BQ1K3.overlap_share` | calcolato dallo script stesso, poco sopra | il termine sinistro del confronto di `C2` |
| `C1` | `KPI.BQ1K1.c1.above_median` | calcolato dallo script stesso | primo termine della congiunzione |
| `C3` | `KPI.BQ2K3.c3_satisfied` | calcolato dallo script stesso | terzo termine della congiunzione |
| posizione di `pop` in graduatoria | `KPI.BQ2K3.pop.rank` | `007b` | l'ordinale della sezione «con che cosa entrare» |
| numerosità del quadrante | `KPI.BQ2K3.quadrant_members_count` | `007b` | l'insieme dei candidati |
| i sei valori di scenario di `BQ3` | `BQ3.adoption.*`, `BQ3.uplift.*` | `004`, via `reports/bq3_scenarios.json` | la sezione «quanto vale» |
| versione della tabella dei mood | `conventions.kpi_mood_table_version`, `MOOD.table.version` | `006` | il contratto di versione |

**Nessuno di questi valori viene modificato.** Se una rigenerazione ne producesse uno diverso da quello pubblicato, è un **ritrovamento** da dichiarare con nota in loco — mai un aggiornamento silenzioso (FR-010).

---

## 4. Dove la funzione si innesta nello script

`build_kpi_measures.py` ha oggi questa sequenza in `main()`:

```
build_bq1k1(...)          → fra le altre cose, KPI.BQ1K1.c1.above_median
build_bq1k2(...)
build_bq1k3(...)          → KPI.BQ1K3.overlap_share
build_segment_measures(...) → fra le altre cose, KPI.BQ2K3.c3_satisfied
```

La funzione nuova — `build_decision_rule(values)` — si innesta **dopo tutte e quattro**, perché ha bisogno dei valori delle tre condizioni. Riceve il dizionario `values` già popolato e vi aggiunge le sei voci.

**Un vincolo di implementazione che nasce da come lo script è fatto.** Le voci di `values` portano il valore come **stringa** (`{"display": ..., "value": ..., "label": ..., "unit": ...}`): i numeri escono come stringhe, come entrano. La funzione nuova deve quindi ricostruire i `Decimal` dai valori esatti che ha calcolato la funzione precedente, **non** rileggere `value` dalla voce già arrotondata per la pubblicazione. La forma più sicura è che `build_bq1k3` restituisca la quota esatta e `main()` la passi, sullo schema già usato da `build_segment_measures`, che restituisce due liste ai chiamanti invece di farle rileggere dall'artefatto.

**Una convenzione nuova nell'artefatto.** Come le sei già presenti (`kpi_median_rule`, `kpi_quadrant_rule`, …), la regola di decisione ne prende una: `kpi_decision_rule`, che dichiara la soglia, la strettezza del confronto, la provenienza della regola (`business_case.md` §3, fissata prima dei numeri), l'ereditarietà della confidenza dal termine più debole e la dipendenza dalla versione della tabella dei mood. È il posto in cui un lettore che apre **solo** l'artefatto trova che cosa quei sei numeri significano.

---

## 5. Le guardie

Lo script ha già una guardia sulle cardinalità (`guard_cardinalities`, FR-004 della `007b`) che si ferma con un errore esplicito invece di scrivere un file. La funzione nuova ne eredita lo spirito con due controlli:

1. **le tre condizioni devono esistere** in `values` prima che il verdetto si calcoli. Se una mancasse — per un errore di ordine nelle chiamate — lo script si ferma invece di pubblicare un verdetto costruito su due condizioni;
2. **il conteggio e la congiunzione devono essere coerenti fra loro**: `all_satisfied` è vero se e solo se `conditions_satisfied` vale tre. È una tautologia nel codice corretto, ed è esattamente per questo che vale la pena verificarla — è la sola forma di incoerenza che nessun lettore noterebbe leggendo l'artefatto.

Entrambe usano `halt()`, la funzione già presente: nessun file scritto, messaggio esplicito, uscita con stato non nullo.
