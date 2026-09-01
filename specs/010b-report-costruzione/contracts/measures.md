# Contratto delle misure: il DAX che questa feature scrive

**Feature**: `010b-report-costruzione` | **Data**: 2026-08-29 | **Stato**: proposto al punto di fermata 2

**Perché questo documento esiste.** Il `.pbix` non è versionato: una misura che vive solo lì si riperde con il file, e nessun controllo del repository può accorgersene. Il principio V della constitution lo dice esplicitamente — *tutto ciò che è esprimibile come artefatto testuale versionabile DEVE esserlo, invece di vivere solo dentro il file binario del report*.

**Che cosa questo documento è.** Il testo DAX letterale delle sei misure nuove, pronto da incollare, più il testo delle tre misure della `008a` che potrebbero non essere nel file e vanno riscritte se mancano.

**Che cosa non è.** Non è un accertamento: non dichiara che cosa il `.pbix` contenga oggi. Ciò che esiste lo accerta [quickstart.md](../quickstart.md), e **in caso di divergenza quella è la fonte autorevole**.

**Nessun valore di KPI è trascritto qui.** Le ancore di verifica sono identificativi verso `reports/kpi_measures.json`, non cifre. La sola eccezione è la soglia di `M3`, che è una **costante nella formula** e quindi parte del testo DAX: è discussa a §2.3, dove la sua natura di stipulazione è dichiarata.

---

## 1. La regola che governa tutte e sei

> **Nessuna di queste misure calcola un KPI.** Quattro leggono valori che un artefatto versionato già pubblica, una compone un conteggio da tre booleani, una converte una terna su un'unità dichiarata.

**Ne discende il vincolo di verifica**: dove una misura porta un valore già pubblicato, la sua lettura dal motore va confrontata **una volta** con quel valore. Una divergenza è un **ritrovamento** da dichiarare, non un numero da accettare.

**Perché il confronto è una volta e non a ogni apertura.** Un confronto ripetuto senza che nulla sia cambiato non aggiunge informazione; ciò che cambia fra due aperture sono le tre impostazioni dell'issue [`#20`](https://github.com/Valvln/streamwave-bi/issues/20), e quelle si riverificano per conto proprio, **prima** che qualunque valore sia letto.

---

## 2. Le sei misure nuove

### 2.1 `M1` — `verdict_conditions_satisfied`

**Che cosa calcola**: quante delle tre condizioni della regola di decisione sono soddisfatte, come conteggio sul dominio `0-3`.

**Pagina**: 2 · **Ancora di verifica**: `KPI.verdict.conditions_satisfied`

```dax
verdict_conditions_satisfied =
INT ( [c1_music_above_median] )
    + INT ( [c2_overlap_above_threshold] )
    + INT ( [c3_high_high_exists] )
```

**Perché la somma di tre `INT` e non un `SWITCH` o una catena di `IF`.** Le tre condizioni sono una **congiunzione**, e il conteggio è il numero di termini veri: una somma è la forma che dice esattamente questo. Una catena di `IF` enumererebbe otto casi per produrre lo stesso numero, e ogni caso enumerato è un caso che può essere scritto male.

**Che cosa questa misura non è.** Non è il verdetto. Il verdetto è che **tutte e tre** siano soddisfatte, ed è `KPI.verdict.all_satisfied`: la visuale `V1` lo porta come esito e usa `M1` come il numero che lo regge. Sono due valori distinti nell'artefatto e restano due valori distinti a schermo.

---

### 2.2 `M2` — `c2_overlap_above_threshold`

**Che cosa calcola**: la condizione `C2` come booleano.

**Pagine**: 2, 5 · **Ancora di verifica**: `KPI.BQ1K3.c2.satisfied`

```dax
c2_overlap_above_threshold =
[mood_profile_overlap] > [c2_threshold]
```

**L'operatore è stretto (`>`) e non largo (`>=`), e non è una scelta di questa feature.** È la decisione `D12` di [`docs/kpi_operators.md`](../../../docs/kpi_operators.md) §12, fissata dalla `009` per coerenza con `D9.2` e `D4`. Riaprirla sarebbe riaprire un operatore fissato, che è fuori perimetro.

**Perché `M2` esiste, ed è un ritrovamento che il disegno registra.** `C2` è **l'unica delle tre condizioni senza una companion booleana pubblicata**: `C1` ha `c1_music_above_median`, verificata contro il motore; `C3` nasce dalla decisione `CP-1` della `008a`; `C2` esisteva solo come valore continuo più una soglia. Senza `M2` la visuale del verdetto avrebbe due booleani e un numero.

**È un'asimmetria del framework che nessuna feature precedente aveva rilevato**, ed è il contenuto della decisione `CP-2`. Colmarla è una conseguenza del disegno, non il suo scopo.

---

### 2.3 `M3` — `c2_threshold`

**Che cosa calcola**: la soglia di `C2`, esposta come misura invece che digitata dentro una visuale.

**Pagine**: 5, 6 · **Ancora di verifica**: `KPI.BQ1K3.c2.threshold`

```dax
c2_threshold = 0.5
```

**Perché una misura per una costante, che è la domanda ovvia.** Un numero digitato dentro una visuale è un valore la cui **unica fonte è che qualcuno l'ha scritto**, ed è ciò che il principio I vieta. Come misura ha un nome, si legge, e si confronta con la propria ancora. È la stessa ragione per cui la `008a` ha esposto come misure le due soglie del quadrante (`F7`), che vivevano come variabili interne a `segment_entry_priority_quadrant`.

**La soglia è una stipulazione, non una misura sui dati**, e va marcata come tale a schermo (contratto di pagina §8). È la lettura letterale del termine «maggioranza» che il business case usa, **fissata prima di guardare il valore** — ed è quella proprietà, non il valore, a rendere la condizione difendibile.

**Il punto decimale nel testo DAX.** La formula scrive `0.5` con il punto: è sintassi DAX e non una scelta di formato. La **visualizzazione** a schermo segue la convenzione italiana del progetto, ed è la ragione per cui l'ancora porta `display` con la virgola. È lo stesso confine che l'issue [`#11`](https://github.com/Valvln/streamwave-bi/issues/11) ha attraversato in modo doloroso — il punto decimale letto come separatore delle migliaia — e per questo va detto invece che lasciato implicito.

---

### 2.4 `M4` — `c2_margin`

**Che cosa calcola**: la distanza fra il valore misurato della sovrapposizione e la soglia.

**Pagina**: 6 · **Ancora di verifica**: `KPI.BQ1K3.c2.margin`

```dax
c2_margin = [mood_profile_overlap] - [c2_threshold]
```

**Che cosa questo valore non è**, ed è la sola ragione per cui la pagina 6 esiste nella forma che ha: **non è una stima dell'errore**. Nessuno ha misurato di quanto l'inviluppo ecceda la regione reale. È una **condizione sull'errore** — dice quanto grande dovrebbe essere l'errore perché la conclusione si ribalti, non quanto grande sia.

**Ne discende un divieto di forma sulla visuale `V3`**, non una raccomandazione: nessuna barra di errore, nessun intervallo attorno al valore, nessuna banda. Tutte comunicherebbero una dispersione stimata che nessun valore contiene.

---

### 2.5 `M5` — `c2_margin_share_of_value`

**Che cosa calcola**: il margine rapportato al valore misurato.

**Pagina**: 6 · **Ancora di verifica**: `KPI.BQ1K3.c2.margin_share_of_value`

```dax
c2_margin_share_of_value =
DIVIDE ( [c2_margin], [mood_profile_overlap] )
```

**`DIVIDE` e non l'operatore `/`.** `DIVIDE` restituisce vuoto invece di un errore quando il denominatore è zero. Qui il denominatore non può essere zero — `mood_profile_overlap` è una quota su un catalogo non vuoto — ma la convenzione del progetto è `DIVIDE`, ed è quella che tutte le misure pubblicate usano.

**È la forma in cui l'argomento si legge**: quanto la sovrapposizione reale dovrebbe essere più bassa della stima, **in rapporto alla stima stessa**. La barra da sola non la dà, ed è la ragione per cui la pagina 6 porta il valore accanto alla barra invece di una seconda visuale.

---

### 2.6 `M6` — `arpu_uplift_per_100k`

**Che cosa calcola**: la terna dell'uplift espressa per ogni `100.000` abbonati.

**Pagina**: 9 · **Ancora di verifica**: derivata da `BQ3.uplift.worst` / `.base` / `.best`

```dax
arpu_uplift_per_100k =
SUM ( bq3_scenarios[arpu_uplift] ) * 100000
```

**Il fattore è un'unità dichiarata, non una stima della base di StreamWave**, ed è il punto in cui è più facile sbagliare. La misura **converte l'unità** della terna; non stima un totale. Il fattore `100.000` è dichiarato a schermo **come unità**, ed è la stessa categoria delle soglie nella grammatica dei marcatori.

**Il divieto di moltiplicazione resta intero.** Nessuna visuale, nessuna misura, nessuna colonna moltiplica l'uplift per una base utenti di StreamWave. **Nessuna base è quantificata in questo progetto**, e un totale così ottenuto sarebbe un numero che nessuno ha misurato con l'autorevolezza di uno misurato.

**Chi conosce la propria base divide per `100.000` e moltiplica: l'operazione resta sua**, e il risultato eredita per intero la confidenza bassa della terna.

**Perché `SUM` su una tabella disconnessa.** `bq3_scenarios` non ha relazioni con il resto del modello: il contesto di filtro che la raggiunge è solo quello della colonna `scenario` sulla visuale, che seleziona una riga per colonna. `SUM` su una riga sola è quel valore. È il comportamento che la `008a` ha già usato per la terna degli scenari.

**L'alternativa dichiarata equivalente.** Il contratto di pagina §13.1 ammette che, se risultasse più semplice, i tre valori si portino come **colonna calcolata** della tabella disconnessa invece che come misura. È equivalente e **va dichiarato nell'esito**. La misura è la forma preferita perché una colonna calcolata materializza il valore nel modello, e un valore materializzato in un file non versionato è un valore in più che si può riperdere.

---

## 3. Le tre misure della `008a` che vanno trovate o riscritte

**Perché stanno in questo documento.** La `008a` le ha dichiarate come decisioni (`F7` e `CP-1`) ma **nessun artefatto del repository ne registra il testo DAX**. Vivono solo nel `.pbix`, che non è versionato: se il file le avesse perse, non esisterebbe alcun luogo da cui riscriverle.

**È un difetto che questa feature chiude di conseguenza, non uno che si è proposta di chiudere.** Il testo qui sotto è ricostruito dalle variabili interne di `segment_entry_priority_quadrant`, pubblicata a [`docs/kpi_measures.md`](../../../docs/kpi_measures.md) §7.3.

### 3.1 Le due soglie del quadrante — `F7` della `008a`

```dax
quadrant_demand_threshold =
MEDIANX ( ALL ( dim_segment ), [segment_demand_index] )

quadrant_affinity_threshold =
MEDIANX ( ALL ( dim_segment ), [segment_catalog_affinity] )
```

**Ancore di verifica**: `KPI.BQ2K3.threshold.demand` e `KPI.BQ2K3.threshold.affinity`.

**L'`ALL ( dim_segment )` non è decorativo, ed è ciò che rende verificabile la regola di §2.1 del contratto di pagina.** Le soglie non si muovono quando un segmento viene selezionato: è la ragione per cui la selezione incrociata fra le pagine 7 e 8 può essere **evidenziazione e non filtro** senza che alcun valore cambi.

### 3.2 `C3` come booleano — `CP-1` della `008a`

```dax
c3_high_high_exists =
COUNTROWS (
    FILTER ( ALL ( dim_segment ), [segment_entry_priority_quadrant] = TRUE () )
) > 0
```

**Ancora di verifica**: `KPI.BQ2K3.c3_satisfied`.

**`M1` la compone**, e senza di essa il verdetto non si calcola. È la ragione per cui questa misura sta fra quelle da riscrivere se mancano, mentre la quarta estensione della `008a` — la quota di titoli `Movie` — non lo è: quella non la usa nessuna pagina.

### 3.3 Il conteggio dei membri del quadrante — `CP-4`

```dax
quadrant_members_count =
COUNTROWS (
    FILTER ( ALL ( dim_segment ), [segment_entry_priority_quadrant] = TRUE () )
)
```

**Ancora di verifica**: `KPI.BQ2K3.quadrant_members_count`.

**È lo scostamento dichiarato dalla `008a`, ed è la decisione `CP-4`.** Il contratto della `008a` §5.3 dichiarava esplicitamente che nessun conteggio dei membri del quadrante comparisse come valore a sé: là la dispersione lo mostrava e un conteggio sarebbe stato un valore in più da ancorare senza che nulla lo richiedesse.

**Qui lo richiede l'argomento.** `raccomandazione.md` §2 usa quel conteggio come **l'esito della terza condizione**, e una pagina che porta `C3` senza il numero che la soddisfa lascerebbe l'esito senza il proprio metro.

**Non è una correzione del contratto precedente**: è una decisione diversa in un disegno diverso, e i due contratti restano entrambi validi per il proprio artefatto.

---

## 4. Che cosa non si scrive, e perché

| Non si scrive | Perché |
|---|---|
| qualunque riscrittura di una misura pubblicata | sarebbe riaprire un operatore fissato. Il testo DAX pubblicato si incolla **senza modificarlo** |
| un `ALL` aggiunto a `mood_profile_overlap` | è l'issue [`#18`](https://github.com/Valvln/streamwave-bi/issues/18), e **resta aperta**. La formula si chiude solo se una pagina del disegno esponesse un filtro di categoria video — e nessuna lo fa. Il disegno dimostra che il difetto non si manifesta, non che non esista |
| una misura che moltiplica l'uplift per una base | il divieto di moltiplicazione. Nessuna base è quantificata in questo progetto |
| tre misure sui profili di mood per segmento | il contratto di pagina §15 le esclude: la seconda condizione è un'affermazione sull'**intero** catalogo musicale, e portare i segmenti a pagina 5 anticiperebbe la parte «con che cosa entrare» |
| una misura che conta le righe di un segmento come dimensione del punto | misura il **campionamento** e non il mercato (§9.1 del contratto di pagina) |

---

## 5. L'ordine in cui si scrivono

Vincolato dalle dipendenze, non da preferenza:

| # | Misura | Dipende da |
|---|---|---|
| 1 | `c2_threshold` (`M3`) | nulla |
| 2 | le due soglie del quadrante, `c3_high_high_exists` | misure pubblicate, se mancano dal file |
| 3 | `c2_overlap_above_threshold` (`M2`) | `M3` |
| 4 | `c2_margin` (`M4`) | `M3` |
| 5 | `c2_margin_share_of_value` (`M5`) | `M4` |
| 6 | `verdict_conditions_satisfied` (`M1`) | `M2` e `c3_high_high_exists` |
| 7 | `arpu_uplift_per_100k` (`M6`) | la tabella disconnessa |
| 8 | `quadrant_members_count` | `segment_entry_priority_quadrant` |

**Il confronto con le ancore si fa dopo il passo 8**, in un solo passaggio su tutte, e prima che qualunque visuale le consumi. Una visuale costruita su una misura non verificata è una visuale da rifare.
