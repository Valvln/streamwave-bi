# Fase 1 — che cosa il disegno richiede al modello

**Feature**: `010a-report-disegno` | **Data**: 2026-08-29

Che cosa il report nuovo chiede al modello dati, alle misure e alle visuali. È l'input diretto della `010b`: la stima di quella feature poggia su questo documento, e ciò che qui è vago là diventa un'ora davanti allo schermo.

**Questo documento non descrive il `.pbix`.** Il file non è versionato e questa sessione non lo apre. Dichiara ciò che deve esistere; ciò che esiste lo accerterà la `010b`.

---

## 1. La mappa delle pagine

Dieci pagine, iniziale compresa, nessuna pagina finale separata (`G3`). L'ordine è quello dell'argomento (`G2`); la corrispondenza con le sezioni di [`docs/raccomandazione.md`](../../docs/raccomandazione.md) è molti-a-uno (`G1`).

| # | Pagina | Parte dell'argomento | Sezione servita |
|---|---|---|---|
| 1 | La domanda | perché l'analisi esiste, e a quali condizioni si risponde | §«Che cosa è questo documento» |
| 2 | La risposta | il verdetto e la regola di decisione fissata prima dei valori | §1 |
| 3 | Su che cosa poggia | i due cataloghi sostitutivi, e che nessun numero è misurato su StreamWave | §1, capoverso sui proxy |
| 4 | La prima condizione | la musica non è residuale nel catalogo attuale | §2, «La prima» |
| 5 | La seconda condizione | il catalogo musicale ricade nella regione di carattere del video | §2, «La seconda» |
| 6 | Quanto dovrebbe sbagliare | il margine di `C2`, e che è una condizione sull'errore e non una stima | §2, «Quanto la stima dovrebbe sbagliare» |
| 7 | La regione di ingresso | esiste una regione ad alta domanda e alta affinità | §3, «La regione» |
| 8 | Che cosa la regione contiene | la graduatoria completa e l'esclusione dei segmenti a domanda non misurata | §3, «La regione» + «Un'esclusione che va dichiarata» |
| 9 | Quanto vale | la terna degli scenari e il fattore di conversione | §4 |
| 10 | Che cosa lo ribalterebbe, e che cosa non si conclude | le condizioni di ribaltamento e i limiti dichiarati | §5 e §6 |

**Le tre condizioni non hanno una pagina ciascuna, ed è deliberato.** La terza — esiste almeno un punto d'ingresso — **è** la regione di `BQ2`, e la pagina 7 la porta. Darle una pagina propria fra la 5 e la 6 la separerebbe dai segmenti che la rendono vera, cioè dall'unica cosa che la rende utile a chi deve decidere.

**Due pagine servono due sezioni ciascuna, ed è l'unica eccezione a `G1`.** La pagina 8 tiene insieme la regione e la sua esclusione perché l'esclusione è una qualificazione della graduatoria che sta sulla stessa schermata: separarle produrrebbe una graduatoria leggibile senza il suo avvertimento, che è il difetto che `kpi_measures.md` §7.4 chiede di prevenire. La pagina 10 tiene insieme §5 e §6 perché entrambe dicono che cosa l'analisi non stabilisce, e la distinzione fra «lo ribalterebbe» e «non lo conclude» è una distinzione di prosa, non di visuale.

**Perché la pagina 3 esiste.** È la collocazione delle assunzioni `A1` e `A6` richiesta da `FR-018`. `docs/raccomandazione.md` le tratta in una sezione propria perché sopravvivano all'estrazione di una frase; una nota a piè di schermo su ogni pagina perde quella proprietà, e una pagina intera subito dopo la risposta la conserva. La pagina 10 le richiama, non le introduce.

---

## 2. Le misure: quelle che esistono e quelle nuove

### 2.1 Esistono già, pubblicate da `docs/kpi_measures.md`

Nessuna di queste va riscritta. Il testo DAX è quello pubblicato, e si incolla senza modificarlo.

| Misura | Pagina che la usa | Stato |
|---|---|---|
| `music_adjacent_catalog_share` | 4 | pubblicata §2.2, verificata contro il motore |
| `c1_music_above_median` | 2, 4 | companion pubblicata, verificata contro il motore |
| `format_duration_gap` | — | **non usata dal disegno**, vedi §2.4 |
| `mood_profile_overlap` | 2, 5, 6 | pubblicata §4.2, verificata contro il motore |
| `segment_demand_index` | 7, 8 | pubblicata §5.2, verificata contro il motore |
| `segment_zero_share` | 7, 8 | companion obbligatoria di `D7`, verificata |
| `segment_catalog_affinity` | 7, 8 | pubblicata §6.2, verificata contro il motore |
| `segment_entry_priority_score` | 8 | pubblicata §7.3, verificata contro il motore |
| `segment_entry_priority_quadrant` | 2, 7, 8 | pubblicata §7.3, verificata contro il motore |
| `segment_entry_priority_rank` | 8 | pubblicata §7.3, verificata contro il motore |

### 2.2 Esistono per decisione della `008a`, mai verificate contro il motore

Le quattro estensioni che il contratto della `008a` ha dichiarato. **Questa sessione non può accertare se siano nel `.pbix`**: il file non è versionato. Chi costruisce le trova o le scrive.

| Misura | Che cosa legge | Pagina | Origine |
|---|---|---|---|
| soglia di domanda del quadrante | la mediana delle domande dei 114 segmenti | 7 | `F7` della `008a`, esposta come misura invece che digitata |
| soglia di affinità del quadrante | la mediana delle affinità dei 114 segmenti | 7 | `F7` della `008a` |
| quota di titoli `Movie` sul catalogo video | dichiara l'asimmetria di `BQ1-K2` | — | `CP-1` della `008a`; **non usata**, vedi §2.4 |
| `C3` come booleano | esiste almeno un segmento nel quadrante | 2, 7 | `CP-1` della `008a` |

### 2.3 Nuove — le scrive la `010b`

**Sei misure.** Nessuna calcola un KPI: quattro leggono valori già pubblicati, una compone un conteggio, una converte una terna già pubblicata su un'unità dichiarata.

| # | Nome proposto | Che cosa calcola | Da quali tabelle | Pagina | Perché serve |
|---|---|---|---|---|---|
| `M1` | `verdict_conditions_satisfied` | quante delle tre condizioni sono soddisfatte, come conteggio `0-3` | compone `c1_music_above_median`, `C3` e la condizione `C2` | 2 | `G5`: il verdetto congiunto è una visuale, e il conteggio è il valore che la regge. È ancorato a `KPI.verdict.conditions_satisfied` e va confrontato una volta con quel valore |
| `M2` | `c2_overlap_above_threshold` | la condizione `C2` come booleano: la sovrapposizione supera la soglia di maggioranza | `mood_profile_overlap` contro la soglia pubblicata | 2, 5 | è l'unica delle tre condizioni **senza una companion booleana pubblicata**. `C1` ha `c1_music_above_median`, `C3` nasce da `CP-1`, `C2` no: oggi esiste solo come valore continuo e una soglia. Senza `M2` la visuale del verdetto avrebbe due booleani e un numero |
| `M3` | `c2_threshold` | la soglia di `C2`, esposta come misura invece che digitata | costante ancorata a `KPI.BQ1K3.c2.threshold` | 5, 6 | stessa ragione di `F7` per le soglie del quadrante: un numero digitato in una visuale è un valore la cui unica fonte è che qualcuno l'ha scritto |
| `M4` | `c2_margin` | la distanza fra il valore misurato e la soglia | `mood_profile_overlap` meno `M3` | 6 | è il valore che la pagina 6 esiste per mostrare. Ancorato a `KPI.BQ1K3.c2.margin` |
| `M5` | `c2_margin_share_of_value` | il margine rapportato al valore misurato | `M4` diviso `mood_profile_overlap` | 6 | è la forma in cui l'argomento si legge — «oltre il 40% della stima stessa» — ed è ancorato a `KPI.BQ1K3.c2.margin_share_of_value` |
| `M6` | `arpu_uplift_per_100k` | la terna dell'uplift espressa per ogni 100.000 abbonati | la tabella disconnessa degli scenari, per un fattore dichiarato | 9 | `G9`. **Non è una moltiplicazione per una base di StreamWave**: nessuna base viene quantificata, ed è la stessa terna su un'unità dichiarata. Il divieto di `FR-014` della `008a` resta intero |

**Su `M6`, il punto in cui è più facile sbagliare.** La misura converte l'unità, non stima un totale. Ciò che la distingue da una violazione del divieto di moltiplicazione è che il fattore — 100.000 — è **dichiarato a schermo come unità** e non è una stima della base di StreamWave: chi legge deve dividere la propria base per 100.000, e l'operazione resta sua. Se la `010b` trovasse più semplice portare quei tre valori come colonne della tabella disconnessa invece che come misura, è equivalente e va dichiarato nell'esito.

**Su `M1`, `M4` e `M5`, un vincolo di verifica.** Sono valori che `reports/kpi_measures.json` già pubblica. La loro lettura dal motore va confrontata **una volta** con il valore pubblicato, sul modello di `★3` della `008a`: una divergenza è un ritrovamento, non un numero da accettare.

### 2.4 Le due misure che il disegno non usa, dichiarate perché l'assenza si nota

`format_duration_gap` (`BQ1-K2`) e la quota di titoli `Movie` che la accompagna **non compaiono su alcuna pagina**.

**La ragione**: `BQ1-K2` non è una delle tre condizioni della regola di decisione, e `docs/raccomandazione.md` non lo cita mai. È un KPI del framework che descrive una distanza di formato fra i due cataloghi — informativo, e fuori dall'argomento che questo report porta. Includerlo richiederebbe una pagina che nessuna sezione della raccomandazione serve, cioè una violazione di `G1`.

**Che cosa questo comporta, dichiarato invece di taciuto**: il report porta **sette KPI su otto**. La dashboard vecchia li portava tutti e otto, ed era un inventario: la completezza rispetto al framework era la sua proprietà organizzatrice, ed è precisamente ciò che la revisione ha respinto. È un ritrovamento per la regia, non una decisione che questa feature prende da sola — vedi §5.

---

## 3. Le visuali

### 3.1 Nuove rispetto alla dashboard a quattro pagine

| # | Visuale | Tipo | Assi / contenuto | Pagina | Dati che la sostengono |
|---|---|---|---|---|---|
| `V1` | il verdetto congiunto | stato a tre elementi dentro un esito unico | le tre condizioni come booleani, il conteggio `M1` al centro | 2 | `c1_music_above_median`, `M2`, `C3`, `M1` — tutti ancorati |
| `V2` | i due cataloghi sui tre assi | dispersione delle 42 categorie video con inviluppo disegnato | ascissa e ordinata: due dei tre assi di mood; l'inviluppo dagli estremi ancorati | 5 | `data/curated/dim_category_mood.json`, 126 valori; `KPI.BQ1K3.bound.*` |
| `V3` | il margine di `C2` | barra orizzontale su asse `0-1` | il valore misurato, la soglia `M3`, la distanza `M4` etichettata | 6 | `mood_profile_overlap`, `M3`, `M4`, `M5` |
| `V4` | il fattore di conversione | tabella a tre colonne, unità dichiarata in intestazione | la terna di `M6` per ogni 100.000 abbonati | 9 | `reports/bq3_scenarios.json` via `M6` |

**Su `V2`, quale coppia di assi.** Il disegno non la fissa: i tre assi sono energia, positività e ritmo, e una dispersione ne porta due. La scelta è di chi costruisce, con un vincolo — **l'asse escluso va dichiarato a schermo**, perché una scatola disegnata su due assi di tre è una proiezione, e una proiezione non dichiarata si legge come la cosa intera. È la stessa asimmetria che rende `BQ1-K3` una stima per eccesso, e mostrarla senza dirlo la nasconderebbe due volte.

### 3.2 Riusano materiale già costruito

| Visuale | Tipo | Pagina | Origine |
|---|---|---|---|
| dispersione dei 114 segmenti | dispersione con due linee di riferimento e tre marcature | 7 | §5.1 del contratto della `008a`, invariata |
| graduatoria completa | tabella, 114 righe, quota di zeri adiacente alla domanda | 8 | §5.2 del contratto della `008a`, invariata |
| terna degli scenari | tabella a tre colonne più unità | 9 | §6 del contratto della `008a`, invariata |
| scheda della North Star | scheda con etichette di fonte e confidenza | 4 | §3 del contratto della `008a` |

**Le due visuali di `BQ2` cambiano pagina ma non forma.** È deliberato: la revisione della `008b` non ha trovato difetti in quelle due visuali — ha trovato che stavano in un inventario. Ridisegnarle avrebbe rimesso in discussione scelte già verificate a schermo per un guadagno che nessuno sta chiedendo.

### 3.3 Le pagine di sola prosa

| Pagina | Perché nessun valore | Che cosa dà all'occhio |
|---|---|---|
| 3 — su che cosa poggia | le due assunzioni di trasferimento **non entrano nella scala di confidenza** per costruzione: non c'è un numero che le misuri, ed è precisamente la loro proprietà | l'articolazione fra i due cataloghi sostitutivi e i due cataloghi reali che non esistono nel progetto |
| 10 — che cosa lo ribalterebbe | tre delle quattro condizioni di ribaltamento non portano valori; la quarta ha la propria pagina (`G4`) | l'articolazione fra condizione e conseguenza, una per riga |

**Nessuna delle due riceve grafica.** Un grafico costruito per riempirle affermerebbe con la geometria ciò che il testo non afferma — e il caso concreto, prevedibile e vietato è una barra dei rischi ordinata per gravità: nessun valore ordina quei rischi, e disegnarli ordinati sarebbe una graduatoria senza fonte.

### 3.4 La visuale che i dati non sostengono

**Le 89.741 tracce come nube sui tre assi, con l'inviluppo sovrapposto.** Sarebbe la forma migliore per la pagina 5: renderebbe visibile quanta parte della scatola è vuota, che è ciò che «stima per eccesso» significa.

**Non entra nel contratto.** Nessun artefatto pubblica quella nube; la sua grana è la traccia e nessun KPI è pubblicato a quella grana; portarla a schermo significherebbe pubblicare valori che nessun documento del progetto pubblica. `V2` la sostituisce con le 42 categorie, che sono ancorate.

È dichiarata qui perché chi costruisce non la reinventi credendo che sia stata dimenticata.

---

## 4. Le etichette di fonte e confidenza

Invariate rispetto a `business_case.md` §5.4 e al contratto della `008a` §1.1. Questa feature non le ridefinisce e non le trascrive di nuovo: il contratto di pagina rinvia a quella tabella.

**Una sola etichetta è nuova**, e riguarda il verdetto congiunto di `V1`: `Fonte: Derivato (C1 + C2 + C3) · Confidenza: media`. La confidenza è media e **non** la media delle tre, per la ragione che `docs/raccomandazione.md` §2 argomenta: una congiunzione non è più affidabile del suo termine più debole. È il motivo per cui `V1` porta una sola etichetta invece di tre.

---

## 5. I ritrovamenti di questa fase

Nessuno dei tre richiede una nota in loco: nessuno è una divergenza fra un valore pubblicato e il suo artefatto.

1. **Nessun profilo di mood per segmento musicale è pubblicato come valore ancorato.** `reports/kpi_measures.json` porta affinità e distanza per segmento, non le tre coordinate. Non è un difetto — nessun documento afferma il contrario — ma va saputo: un confronto di profili segmento per segmento richiederebbe tre misure nuove, e questo disegno non le chiede.
2. **`C2` è l'unica delle tre condizioni senza una companion booleana pubblicata.** `C1` ha `c1_music_above_median` verificata contro il motore, `C3` nasce da `CP-1` della `008a`, `C2` esiste solo come valore continuo più una soglia. È la ragione di `M2`, ed è un'asimmetria del framework che nessuna feature aveva rilevato.
3. **Il report porta sette KPI su otto.** `BQ1-K2` resta fuori perché l'argomento non lo usa. È una conseguenza diretta dell'ordinare il report come argomento invece che come framework, ed è la decisione più contestabile di questo disegno: va portata alla regia al secondo punto di fermata, non assorbita qui.
