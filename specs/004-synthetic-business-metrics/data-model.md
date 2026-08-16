# Fase 1 — Modello dei dati

**Feature**: 004 Synthetic Business Metrics · **Data**: 2026-08-16 · **Piano**: [plan.md](./plan.md)

Questa feature non ha un modello dati nel senso della `005`: non produce tabelle, relazioni o granularità. Ha **due file e una catena**. Questo documento ne fissa la forma; il [contratto](./contracts/parameters-and-scenarios.md) fissa ciò che la `007` può assumere.

---

## Le due entità

### 1. File dei parametri — `data/benchmarks/bq3_tier_upgrade.json`

Curato a mano, versionato, **mai riscritto da uno script**. È il congelamento della condizione 2 della constitution.

| Blocco | Contenuto | Quando nasce |
|---|---|---|
| `band` | i due fattori, la loro ragione, la dichiarazione che non misurano nulla | **blocco A** — prima della ricognizione (FR-011a, T7) |
| `price` | il differenziale di 4,00 €, con rimando ad A4 | blocco A |
| `benchmark` | valore adottato, i cinque elementi della citazione, che cosa la fonte misura, scarto di misura, assunzione di trasferimento | **blocco B** — dopo la ricognizione |
| `rejected` | fonti valutate e respinte, con il motivo (FR-005) | blocco B |
| `schema_version` | intero | blocco A |

**Il vincolo di ordine è parte della forma, non solo della procedura.** Al termine del blocco A il file **non contiene** la chiave `benchmark`, nemmeno vuota o con un segnaposto. Un campo pronto da riempire renderebbe indistinguibile «fissato prima» da «riempito dopo», e distruggerebbe la garanzia che FR-011a esiste per dare.

**I numeri si scrivono come stringhe.** `"0.50"`, non `0.50`. È la condizione per T5: il valore entra in `Decimal` senza mai passare per un `float`, e il file dichiara letteralmente la cifra che l'analista ha scelto invece di quella che il parser JSON gli assegna.

### 2. Artefatto dei valori — `reports/bq3_scenarios.json`

Generato da `scripts/build_bq3_scenarios.py`, versionato (FR-018a), nella forma che `load_artifacts()` del controllo già sa unire.

| Chiave | Contenuto |
|---|---|
| `values` | i sei valori più le due affermazioni derivate, con prefisso `BQ3.` (T3) |
| `conventions` | i fattori, la regola di arrotondamento, il differenziale — tutti con prefisso `bq3_` (T4, F2) |
| `sources` | rimando al file dei parametri con la sua impronta, così che l'artefatto dichiari da quale versione dell'ingresso discende |
| `schema_version` | intero |

Ogni voce di `values` ha la struttura degli artefatti esistenti: `display`, `value`, `label`, `unit`, più `scenario` dove pertinente.

---

## Gli identificativi

Prefisso `BQ3.`, verificato disgiunto da `NF.`, `SP.`, `CL.`, `X.` (T3). La verifica di collisione del controllo resta comunque attiva: la disgiunzione è dimostrata oggi, non garantita domani.

| Identificativo | Che cosa contiene | Unità |
|---|---|---|
| `BQ3.adoption.worst` | tasso di adozione, scenario pessimista | punti percentuali della base |
| `BQ3.adoption.base` | tasso di adozione, scenario centrale — **è il valore del benchmark** | punti percentuali della base |
| `BQ3.adoption.best` | tasso di adozione, scenario ottimista | punti percentuali della base |
| `BQ3.uplift.worst` | variazione del ricavo medio per utente, scenario pessimista | euro per utente al mese |
| `BQ3.uplift.base` | come sopra, scenario centrale | euro per utente al mese |
| `BQ3.uplift.best` | come sopra, scenario ottimista | euro per utente al mese |

**Due valori in più, che esistono per la regola D5.** Un confronto costruito su valori misurati è esso stesso un valore misurato: o ha un identificativo, o non si scrive (FR-031). Il documento avrà bisogno di dire quanto è larga la banda e quante volte lo scenario ottimista supera il pessimista, e nessuna delle due frasi è scrivibile senza ancora.

| Identificativo | Che cosa contiene |
|---|---|
| `BQ3.band.spread_pp` | ampiezza della banda di adozione, in punti percentuali: `best − worst` |
| `BQ3.band.ratio` | rapporto fra scenario ottimista e pessimista: `best ÷ worst` |

`BQ3.band.ratio` **non dipende dal benchmark**: con banda moltiplicativa vale `(1+k)/(1−k)`, cioè 3 per k = 0,50, qualunque sia il valore adottato. È una proprietà della stipulazione, e il documento può dirlo — con l'ancora, non a mente.

## Le convenzioni

| Chiave | Valore | Che cosa dichiara |
|---|---|---|
| `bq3_band_factor_low` | `0.50` | moltiplicatore dello scenario pessimista, `1 − k` |
| `bq3_band_factor_high` | `1.50` | moltiplicatore dello scenario ottimista, `1 + k` |
| `bq3_band_meaning` | prosa | che l'ampiezza **non misura nulla**: è fiducia nel trasferimento, non varianza osservata (FR-011) |
| `bq3_band_fixed_before` | prosa, **senza alcun hash** | che i fattori precedono la ricognizione, e come verificarlo (FR-011a) |
| `bq3_rounding` | `ROUND_HALF_UP`; cifre significative per i tassi, due decimali fissi per gli importi | la regola di arrotondamento, dichiarata e non ereditata, **con la precisione effettiva degli importi** (T5, FR-015) |
| `bq3_price_delta_eur` | `4.00` | il differenziale di A4, letto e non scritto nel codice (FR-012) |

**Perché `bq3_band_fixed_before` non contiene un riferimento al commit.** Sembrava la forma più forte e non è scrivibile in nessuna delle due direzioni. Nel file dei parametri il campo dovrebbe portare l'hash del commit che lo introduce, che **non esiste ancora** nel momento in cui il file si scrive. Nell'artefatto generato, ricavarlo obbligherebbe lo script a interrogare `git`, cioè a dipendere dalla presenza della history — e la Prova 3 del quickstart gira su una copia pulita che potrebbe non averla, oltre a introdurre in una derivazione deterministica una lettura di stato esterno.

La prova di precedenza **è già la history**, prodotta dal commit isolato della Fase 2. La convenzione dichiara quindi il fatto in prosa e indica come verificarlo — `git log --follow data/benchmarks/bq3_tier_upgrade.json`, che è la Prova 1 del [quickstart](./quickstart.md) — senza incorporare nulla che debba essere tenuto allineato a mano.

Il prefisso `bq3_` è obbligatorio e brutto per la ragione di F2: lo spazio dei nomi di `conventions` è piatto e condiviso fra artefatti, e `rounding_decimals` è già occupato da un'altra feature con contenuto diverso.

---

## La catena di derivazione

```
adoption.base   = benchmark
adoption.worst  = benchmark × bq3_band_factor_low
adoption.best   = benchmark × bq3_band_factor_high

uplift.<s>      = adoption.<s> × bq3_price_delta_eur / 100

band.spread_pp  = adoption.best − adoption.worst
band.ratio      = adoption.best ÷ adoption.worst
```

Tre proprietà, tutte verificabili per ispezione dello script:

- **nessun ramo.** Nessuna condizione, nessun caso speciale. L'unica uscita anomala è l'arresto di FR-016 se un tasso cade fuori da 0-100;
- **nessuna sorgente di variabilità.** Nessun `random`, nessun seed, nessuna lettura dell'orologio, nessuna chiamata di rete (FR-013, FR-008);
- **nessun valore scritto a mano.** Tutti e otto discendono dai tre ingressi. Cambiare il benchmark e rieseguire li muove tutti (FR-014).

### Regole di arrotondamento e di presentazione

Aritmetica in `decimal.Decimal`, mai in virgola mobile (T5, F3). L'arrotondamento è `ROUND_HALF_UP` **dichiarato**, non la modalità predefinita di `Decimal`, che è `ROUND_HALF_EVEN`: la differenza si vede su `0,435`, dove la predefinita darebbe `0,44` e su `0,445` darebbe di nuovo `0,44`. Corretto, e controintuitivo per chi rifà il conto a mano — che è il destinatario dichiarato di questo progetto.

La precisione è **quella del benchmark, e mai più di due cifre significative** (FR-015, D3), e si applica in due modi a seconda della famiglia:

| Famiglia | Identificativi | Come si pubblica |
|---|---|---|
| tassi, in punti percentuali | `BQ3.adoption.*`, `BQ3.band.spread_pp` | a **cifre significative** del benchmark, al più due |
| importi, in euro | `BQ3.uplift.*` | a **due posizioni decimali fisse** — convenzione della valuta, non pretesa di precisione |
| rapporto puro | `BQ3.band.ratio` | **esatto**: non discende dal benchmark, vale `(1+k)/(1−k)` per costruzione |

**Perché gli importi non seguono le cifre significative.** Con il benchmark adottato `uplift.base` vale 1,20 € e `uplift.best` vale 1,80 €: applicando le cifre significative si pubblicherebbero `1,2 €` e `1,8 €`. Sarebbe conforme alla lettera e sbagliato — la seconda cifra decimale di un importo è il centesimo, l'unità in cui la valuta è denominata, e toglierla non rende il numero più prudente, lo rende malformato. `bq3_rounding` dichiara perciò **entrambe** le famiglie e dichiara che la precisione effettiva degli importi resta di due cifre significative, così che nessuno legga `1,20 €` come una conoscenza a tre.

Il campo `display` porta il separatore decimale italiano, la virgola, prodotto per formattazione esplicita e mai da una funzione dipendente dal locale — vincolo ereditato da F6 della 003.

---

## Ciò che questo modello non contiene, e perché

- **nessuna riga, nessun utente, nessun mese.** Decisione D1: non esiste consumatore di righe, un'estrazione casuale non aggiungerebbe informazione, e soprattutto **non esiste alcun N** — la base utenti non è quantificata (divergenza 9);
- **nessun totale di ricavo.** `uplift` è euro per utente al mese e non è scalabile (FR-023). Il modello non offre alcuna chiave con cui moltiplicarlo, ed è deliberato;
- **nessun valore di churn, engagement o prezzo alternativo.** Fuori perimetro per FR-018 della 001, per assenza di KPI e per A4/FR-017a;
- **nessun identificativo dei KPI.** `BQ3-K1` e `BQ3-K2` sono nomi di misure e appartengono alla `007`. Questo artefatto ne produce i **parametri**, e gli identificativi lo dicono: `BQ3.adoption.*`, non `BQ3-K1`.
