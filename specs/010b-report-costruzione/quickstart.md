# Le prove, e l'esito della costruzione

**Feature**: `010b-report-costruzione` | **Data**: 2026-08-29

Questo documento porta due cose distinte, e la distinzione va tenuta:

1. **le prove** — che cosa va verificato perché la feature possa dirsi conclusa. Scritte **prima** di costruire;
2. **l'esito della costruzione** — che cosa è stato effettivamente costruito, con gli scostamenti e i ritrovamenti. Scritto **mentre** si costruisce, e completato alla fine.

**La seconda sezione è la fonte autorevole su ciò che esiste a schermo.** Il contratto di pagina della `010a` lo stabilisce esplicitamente (§7 del suo preambolo): *ciò che esisterà lo accerterà la `010b`, nella sezione di esito del proprio `quickstart.md`, e in caso di divergenza quella è la fonte autorevole, non questa*.

---

## Prerequisiti

- Power BI Desktop, con il `.pbix` della `008` sul disco;
- il repository clonato, per gli artefatti di verifica;
- `python3` per il controllo di coerenza.

**Il `.pbix` non è versionato.** Se non fosse disponibile, è un blocco da riportare e non da aggirare: ricostruire il modello da zero è un lavoro che nessuna stima di questa feature copre.

---

## Le prove

Nessun test automatico può leggere il `.pbix`. Tutte le prove che toccano il report sono **manuali, eseguibili da una persona**, come il principio V impone.

### 1 — Le tre impostazioni del modello *(manuale, ★ — prima di ogni altra cosa)*

Leggere l'issue [`#20`](https://github.com/Valvln/streamwave-bi/issues/20) e verificare le tre impostazioni che vi sono registrate.

**Esito atteso**: tutte e tre in ordine, oppure ripristinate prima che qualunque valore venga letto.

**Perché è la prima prova.** Un'impostazione riperduta **non produce un errore**: produce un valore diverso senza segnale. Sulla `007b` è costata tre KPI sbagliati di due ordini di grandezza sotto un esito verde di ogni controllo del repository.

**L'issue non si chiude.** Un esito positivo oggi non prova un vincolo per sempre.

### 2 — Le sei misure nuove esistono e portano i valori pubblicati *(manuale)*

Per ciascuna misura di [contracts/measures.md](contracts/measures.md), leggerne il valore dal motore e confrontarlo **una volta** con il `display` della propria ancora in `reports/kpi_measures.json`.

| Misura | Ancora |
|---|---|
| `M1` | `KPI.verdict.conditions_satisfied` |
| `M2` | `KPI.BQ1K3.c2.satisfied` |
| `M3` | `KPI.BQ1K3.c2.threshold` |
| `M4` | `KPI.BQ1K3.c2.margin` |
| `M5` | `KPI.BQ1K3.c2.margin_share_of_value` |
| `M6` | derivata da `BQ3.uplift.*` |

**Esito atteso**: coincidenza su tutte. **Una divergenza è un ritrovamento**, da dichiarare nella sezione di esito, non un numero da accettare.

### 3 — Le tre misure della `008a` esistono *(manuale)*

Verificare che le due soglie del quadrante, `c3_high_high_exists` e `quadrant_members_count` siano nel modello. Se mancano, riscriverle dal testo di [contracts/measures.md](contracts/measures.md) §3.

**Esito atteso**: presenti, e coincidenti con `KPI.BQ2K3.threshold.demand`, `KPI.BQ2K3.threshold.affinity`, `KPI.BQ2K3.c3_satisfied`, `KPI.BQ2K3.quadrant_members_count`.

### 4 — La tabella degli scenari è disconnessa *(manuale, `FR-029`)*

Verificare che `bq3_scenarios` porti i sei valori da `reports/bq3_scenarios.json` **senza alcuna relazione** con il resto del modello.

**Esito atteso**: nessuna relazione. Una relazione renderebbe possibile filtrare gli scenari per segmento o per categoria, producendo scenari che nessuno ha stimato.

### 5 — La sincronizzazione fra le pagine 7 e 8 — `CP-3` *(manuale, ★ — presto)*

Verificare se la selezione di un segmento sulla pagina 7 resti selezionata sulla pagina 8 e viceversa, **come evidenziazione e senza ricalcolare alcun valore**.

**Esito atteso**: non predeterminato. L'issue [`#21`](https://github.com/Valvln/streamwave-bi/issues/21) registra un accertamento precedente e **contrario**, ottenuto dalla `008a` sullo stesso strumento: *Power BI non offre l'evidenziazione come modalità di risposta per una dispersione né per una tabella*.

**Le due strade**:

- **se ottenibile** — l'issue `#21` si chiude, e va risposta l'issue [`#33`](https://github.com/Valvln/streamwave-bi/issues/33): la riga corrispondente viene **evidenziata lasciandola dov'è**, oppure **evidenziata e portata in vista**? Un'evidenziazione che il lettore non può vedere non è una continuità di lettura, che è il termine con cui §10.3 definisce il difetto;
- **se non ottenibile** — l'issue `#21` **resta aperta** e diventa un ritrovamento. Le pagine 7 e 8 si costruiscono comunque: nessun valore dipende da quella sincronizzazione.

**Perché va fatta presto.** È l'unica prova il cui esito cambia ciò che si dichiara, non ciò che si costruisce.

### 6 — Le dieci pagine esistono, con le visuali dichiarate *(manuale, `SC-004`)*

Per ciascuna pagina, verificare che porti gli elementi che il contratto di pagina le assegna, con le visuali del tipo dichiarato.

**Esito atteso**: dieci pagine, nell'ordine e con i titoli della mappa di §1.

### 7 — Ogni valore a schermo coincide con la propria ancora *(manuale, `SC-003`)*

Per ciascun valore a schermo, confrontarlo con il `display` dell'ancora che il contratto di pagina gli assegna.

**Esito atteso**: coincidenza. Ogni divergenza è un ritrovamento da dichiarare con nota in loco.

### 8 — Nessun numero è digitato in una visuale *(manuale, `FR-003`)*

Verificare che le linee di riferimento siano **misure lette dal modello** e non costanti digitate: la mediana di pagina 4, la soglia di pagina 6, le due soglie di pagina 7, i bordi dell'inviluppo di pagina 5.

**Esito atteso**: nessuna costante digitata. Un numero digitato in una visuale è un valore la cui unica fonte è che qualcuno l'ha scritto.

### 9 — Le etichette di fonte e confidenza *(manuale, `FR-012`)*

Verificare che ogni valore a schermo porti le due etichette, su ogni pagina.

**Esito atteso**: nessuna eccezione. **La pagina 2 porta una sola etichetta**, quella del verdetto: tre etichette inviterebbero alla lettura che la confidenza del verdetto sia la media delle tre.

### 10 — Nessuna interazione produce una grana non pubblicata *(manuale, `SC-007`)*

Per ciascuna pagina, verificare che le interazioni elencate come non offerte siano effettivamente disattivate.

**Esito atteso**: nessun filtro che ricalcoli un valore a una grana diversa dalle tre pubblicate. **In particolare, nessun filtro di categoria video su alcuna pagina** — è l'issue [`#18`](https://github.com/Valvln/streamwave-bi/issues/18), e a pagina 5 il difetto sarebbe *visibile e ingannevole insieme*.

### 11 — Le pagine 3 e 10 non hanno ricevuto grafica *(manuale, `FR-013`)*

**Esito atteso**: nessuna visuale. In particolare, **nessuna barra dei rischi ordinata per gravità** a pagina 10: nessun valore ordina quei rischi.

### 12 — La visuale di §15 non è stata costruita *(manuale, `FR-014`)*

**Esito atteso**: la nube delle tracce sui tre assi non esiste in alcuna pagina.

### 13 — La navigazione *(manuale, `SC-004`)*

Da ciascuna delle dieci pagine, raggiungere ogni altra pagina con **un solo passaggio**, tramite elementi interni al report.

**Esito atteso**: dieci pagine raggiungibili da ciascuna. **Il riquadro delle schede di Power BI non conta**: è un'affordance dello strumento, non del report.

### 14 — Il testo a schermo coincide con il contratto di narrazione *(manuale, `SC-005`)*

**Esito atteso**: coincidenza letterale. Dove diverge, prevale ciò che è a schermo e **lo scostamento si dichiara**.

### 15 — Zero limiti orfani *(manuale, `SC-002`, issue `#28`)*

Per ciascun limite scritto a schermo, cercare sulla stessa pagina l'affermazione positiva che gli sta accanto.

**Esito atteso**: **zero limiti orfani**. È il difetto che ha fermato la `008b` — *trentadue blocchi dicono al lettore che cosa non concludere; nessuno gli dice che cosa può concludere* — e questa prova è il suo presidio.

### 16 — Il controllo di coerenza *(eseguibile)*

```bash
python3 scripts/check_audit_coherence.py
```

**Esito atteso**: verde sui documenti che questa feature pubblica o modifica.

---

## Esito della costruzione

> **Da compilare mentre si costruisce, non alla fine.** Uno scostamento ricostruito a posteriori è una razionalizzazione — è §19 del contratto di pagina, ed è la disciplina che la `008a` ha dimostrato valere.

### Le pagine che esistono

*(da compilare)*

### Gli scostamenti dal contratto di pagina

*(da compilare — ciascuno con la propria ragione)*

### I ritrovamenti

*(da compilare — in particolare ogni divergenza fra un valore letto dal motore e il valore pubblicato)*

### L'esito delle quattro decisioni di §18

*(da compilare — `CP-3` in particolare)*

### Lo stato delle issue

*(da compilare — quali si chiudono, quali restano, e perché)*

### L'esito delle sedici prove

*(da compilare)*

### Le issue aperte da questa feature

*(da compilare)*
