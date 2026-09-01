# Che cosa il modello riceve

**Feature**: `010b-report-costruzione` | **Data**: 2026-08-29

Che cosa questa feature aggiunge al modello dati, e che cosa vi trova già. Consuma [`specs/010a-report-disegno/data-model.md`](../010a-report-disegno/data-model.md) §2 e §3 invece di riprodurlo: là ciascuna voce ha la propria motivazione per esteso.

**Questo documento non descrive il `.pbix`.** Dichiara che cosa deve esistere nel modello quando questa feature chiude; ciò che esiste lo accerta la sezione «Esito della costruzione» di [quickstart.md](quickstart.md), e **in caso di divergenza quella è la fonte autorevole**.

---

## 1. Le tabelle: nessuna cambia

Il modello della `008a` porta sette tabelle e cinque relazioni, più la tabella disconnessa degli scenari. **Questa feature non ne aggiunge, non ne toglie e non cambia alcuna relazione.**

**Perché va detto invece di lasciarlo implicito.** Il report nuovo porta dieci pagine invece di quattro e sei misure nuove: è la situazione in cui è naturale supporre che serva anche una tabella nuova. Non serve. Le sei misure leggono tutte da tabelle esistenti o da costanti ancorate, e la ragione è che **nessuna calcola un KPI**.

| Tabella | Che cosa questa feature ne legge | Pagine |
|---|---|---|
| `dim_category_mood` | i profili di mood delle `42` categorie video, e gli estremi degli assi | 5 |
| `dim_track` | le tracce dentro l'inviluppo, via `mood_profile_overlap` | 2, 5, 6 |
| `dim_segment` | i `114` segmenti, la marcatura `is_high_zero_genre` | 7, 8 |
| `fact_track_segment` | le righe su cui la domanda è mediana | 7, 8 |
| `dim_title`, `dim_category`, il ponte titolo-categoria | i conteggi per categoria di `C1` | 4 |
| `bq3_scenarios` *(disconnessa)* | i sei valori di scenario | 9 |

**La tabella degli scenari resta disconnessa, ed è un vincolo e non una constatazione.** Il contratto di pagina §11.1 vieta la selezione incrociata col resto del report: *una relazione renderebbe possibile filtrarli per segmento o per categoria, producendo scenari che nessuno ha stimato*. `FR-029` chiede di accertare che sia così.

---

## 2. Le misure: che cosa esiste e che cosa questa feature scrive

### 2.1 Esistono e non si toccano — pubblicate da `docs/kpi_measures.md`

Il testo DAX è quello pubblicato. **Si incolla senza modificarlo**, e riscriverne una sarebbe riaprire un operatore fissato (`FR-037`).

| Misura | Pagine | Stato |
|---|---|---|
| `music_adjacent_catalog_share` | 4 | pubblicata §2.2, verificata contro il motore |
| `c1_music_above_median` | 2, 4 | companion pubblicata, verificata contro il motore |
| `mood_profile_overlap` | 2, 5, 6 | pubblicata §4.2, verificata contro il motore |
| `segment_demand_index` | 7, 8 | pubblicata §5.2, verificata contro il motore |
| `segment_zero_share` | 7, 8 | companion obbligatoria di `D7`, verificata |
| `segment_catalog_affinity` | 7, 8 | pubblicata §6.2, verificata contro il motore |
| `segment_entry_priority_score` | 8 | pubblicata §7.3, verificata contro il motore |
| `segment_entry_priority_quadrant` | 2, 7, 8 | pubblicata §7.3, verificata contro il motore |
| `segment_entry_priority_rank` | 8 | pubblicata §7.3, verificata contro il motore |

**`format_duration_gap` esiste e questo report non la usa.** È `BQ1-K2`, ed è la decisione `CP-1`. La misura resta nel modello — toglierla sarebbe una modifica al modello che nessuno ha chiesto — e semplicemente nessuna pagina la porta a schermo.

### 2.2 Esistono per decisione della `008a`, e vanno **trovate o riscritte**

Le quattro estensioni che il contratto della `008a` ha dichiarato. **Questa feature non può assumere che siano nel `.pbix`**: il file non è versionato, e nessun artefatto del repository ne registra il testo DAX.

| Misura | Che cosa legge | Pagine | Se manca |
|---|---|---|---|
| soglia di domanda del quadrante | la mediana delle domande dei `114` segmenti | 7 | si riscrive dalla variabile interna di `segment_entry_priority_quadrant` |
| soglia di affinità del quadrante | la mediana delle affinità dei `114` segmenti | 7 | come sopra |
| quota di titoli `Movie` | l'asimmetria di `BQ1-K2` | — | **non usata**, e non si riscrive |
| `C3` come booleano | esiste almeno un segmento nel quadrante | 2, 7 | si riscrive: `M1` la compone, e senza di essa il verdetto non si calcola |

**Il testo delle tre che servono sta in [contracts/measures.md](contracts/measures.md) §3**, perché il principio II lo chiede: se una misura si può riperdere con il file, il suo testo deve vivere nel repository.

### 2.3 Nuove — le scrive questa feature

Sei misure. **Nessuna calcola un KPI**: quattro leggono valori già pubblicati, una compone un conteggio, una converte una terna su un'unità dichiarata.

| # | Nome | Che cosa calcola | Legge da | Pagine | Ancora di verifica |
|---|---|---|---|---|---|
| `M1` | `verdict_conditions_satisfied` | quante delle tre condizioni sono soddisfatte, `0-3` | `c1_music_above_median`, `M2`, `C3` | 2 | `KPI.verdict.conditions_satisfied` |
| `M2` | `c2_overlap_above_threshold` | `C2` come booleano | `mood_profile_overlap` contro `M3` | 2, 5 | `KPI.BQ1K3.c2.satisfied` |
| `M3` | `c2_threshold` | la soglia di `C2`, esposta come misura | costante ancorata | 5, 6 | `KPI.BQ1K3.c2.threshold` |
| `M4` | `c2_margin` | la distanza dal valore alla soglia | `mood_profile_overlap` meno `M3` | 6 | `KPI.BQ1K3.c2.margin` |
| `M5` | `c2_margin_share_of_value` | il margine rapportato al valore | `M4` diviso `mood_profile_overlap` | 6 | `KPI.BQ1K3.c2.margin_share_of_value` |
| `M6` | `arpu_uplift_per_100k` | la terna dell'uplift per `100.000` abbonati | la tabella disconnessa | 9 | derivata da `BQ3.uplift.*` |

**Il conteggio finale.** Il modello porta **venti** misure alla chiusura di questa feature: nove pubblicate usate dal report, `format_duration_gap` pubblicata e non usata, due soglie di `F7`, due companion di `CP-1` della `008a`, sei nuove. È ciò che `CP-2` dichiara.

### 2.4 Il vincolo di verifica su `M1`, `M4` e `M5`

Portano valori che `reports/kpi_measures.json` **già pubblica**. La lettura dal motore va confrontata **una volta** con il valore pubblicato.

| Misura | Valore pubblicato (`display`) |
|---|---|
| `M1` | `3` |
| `M4` | `0,3450` |
| `M5` | `0,4083` |

**Una divergenza è un ritrovamento, non un numero da accettare.** È il presidio che sulla `007b` ha trovato tre KPI sbagliati di due ordini di grandezza sotto un esito verde di ogni controllo del repository.

**`M2` e `M3` portano anch'esse valori pubblicati** — `sì` e `0,5000` — e si verificano allo stesso modo. Il contratto nomina esplicitamente solo `M1`, `M4` e `M5`; estendere il confronto alle altre due costa nulla, e questa feature lo fa.

---

## 3. Le visuali

### 3.1 Nuove

| # | Visuale | Tipo | Pagina | Che cosa la alimenta |
|---|---|---|---|---|
| `V1` | il verdetto congiunto | stato a tre elementi dentro un esito unico | 2 | `c1_music_above_median`, `M2`, `C3`, `M1` |
| `V2` | i due cataloghi sugli assi di mood | dispersione delle `42` categorie con inviluppo | 5 | `dim_category_mood`, `KPI.BQ1K3.bound.*` |
| `V3` | il margine di `C2` | barra orizzontale su asse `0-1` assoluto | 6 | `mood_profile_overlap`, `M3`, `M4`, `M5` |
| `V4` | il fattore di conversione | tabella a tre colonne, unità in intestazione | 9 | `bq3_scenarios` via `M6` |

**Una quinta è nuova come forma e non come dato**: la distribuzione delle `42` categorie video per numero di titoli, a pagina 4. Legge gli stessi valori che la `008a` portava come scheda.

**Su `V2`, la scelta della coppia di assi.** [research.md](research.md) `R-5` ha accertato che gli estremi pubblicati sono **identici sui tre assi**: `0,0500` come minimo e `0,9500` come massimo su energia, positività e ritmo. L'inviluppo è quindi un cubo, e qualunque coppia produce lo stesso rettangolo. La scelta si fa su ciò che distingue meglio i punti delle categorie, davanti allo schermo, e **l'asse escluso va dichiarato** (`FR-016`).

### 3.2 Riusate, invariate

| Visuale | Pagina | Origine |
|---|---|---|
| dispersione dei `114` segmenti | 7 | contratto `008a` §5.1 |
| graduatoria completa | 8 | contratto `008a` §5.2 |
| terna degli scenari | 9 | contratto `008a` §6 |
| scheda della North Star | 4 | contratto `008a` §3 |

**Cambiano pagina, non forma** (`FR-015`). La revisione della `008b` non aveva trovato difetti in quelle due di `BQ2`: aveva trovato che stavano in un inventario.

### 3.3 La visuale che resta non costruita

Le `89.741` tracce come nube sui tre assi con l'inviluppo sovrapposto. **Non si costruisce** (`FR-014`), e la ragione sta a §15 del contratto: nessun artefatto pubblica quella nube, la sua grana è la traccia, e nessun KPI è pubblicato a quella grana.

**Se sembrasse facile farla comunque, è il segnale che si sta per pubblicare un numero senza fonte.**

---

## 4. Le tre impostazioni da riverificare — issue [`#20`](https://github.com/Valvln/streamwave-bi/issues/20)

Lette dall'issue, non da una copia. Sono in [research.md](research.md) `R-2`:

| # | Impostazione | Che cosa produce se è riperduta |
|---|---|---|
| `S-1` | tipizzazione di `energy`, `valence`, `danceability` nel dominio `0-1` | tre KPI sbagliati di **due ordini di grandezza**, senza errore a schermo |
| `S-2` | `QuoteStyle.Csv` sull'origine di `dim_title` | due record si spezzano in quattro |
| `S-3` | colonna `scenario` di `bq3_scenarios` | l'intervallo di `BQ3` perde le etichette |

**Si verificano prima di leggere qualunque valore.** L'issue **non si chiude**: un esito positivo oggi non prova un vincolo per sempre.

---

## 5. Il filtro di categoria e l'issue [`#18`](https://github.com/Valvln/streamwave-bi/issues/18)

`mood_profile_overlap` legge gli estremi degli assi con `MINX`/`MAXX` su `dim_category_mood` **senza `ALL`**. Un filtro di categoria video restringerebbe silenziosamente l'inviluppo.

**Nessuna pagina del disegno espone quel filtro**, ed è dichiarato pagina per pagina nel contratto: §6.1 lo vieta a pagina 4, §7.1 a pagina 5 dove il difetto sarebbe *visibile e ingannevole insieme* — il rettangolo si stringerebbe e sembrerebbe corretto.

**La verifica è di questa feature** (`FR-030`): se una pagina lo esponesse, la formula va chiusa prima. L'issue resta aperta perché il disegno dimostra che il difetto non si manifesta, non che non esista.
