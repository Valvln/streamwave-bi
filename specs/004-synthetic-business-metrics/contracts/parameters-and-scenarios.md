# Contratto — Parametri e valori di scenario di BQ3

**Feature**: 004 Synthetic Business Metrics · **Data**: 2026-08-16

Che cosa la `007` — e chiunque legga i valori di BQ3 — **può assumere**, e che cosa **non deve** assumere. Il contratto lega la feature che produce a quelle che consumano; dove diverge dall'implementazione, la 003 ha insegnato che è il contratto a dover essere corretto, non il lettore a doverlo indovinare.

La grammatica di marcatura non è definita qui: la fonte unica è [`docs/convenzioni-marcatura.md`](../../../docs/convenzioni-marcatura.md).

---

## 1. I due file

| File | Chi lo scrive | Versionato | Rigenerabile |
|---|---|---|---|
| `data/benchmarks/bq3_tier_upgrade.json` | **una persona**, a mano | sì | **no, mai** — è il congelamento della condizione 3 della constitution |
| `reports/bq3_scenarios.json` | `scripts/build_bq3_scenarios.py` | sì | sì, da copia pulita senza rete e senza `data/raw/` |

**La riga che conta è la seconda colonna della quarta**: il file dei parametri non si rigenera perché a monte c'è una persona con un browser. Uno script che lo riscrivesse violerebbe la condizione 3, e questa è la ragione per cui il contratto lo dichiara in sola lettura invece di lasciarlo al buon senso.

`data/benchmarks/` è versionata **al contrario** delle altre cartelle di `data/`, che non lo sono perché riproducibili. Questa lo è perché non lo è.

## 2. Che cosa la `007` può assumere

1. **I sei valori esistono già calcolati.** `reports/bq3_scenarios.json` contiene tasso e uplift per i tre scenari, arrotondati secondo la regola dichiarata in `conventions.bq3_rounding`. La `007` **legge**, non ricalcola.
2. **Gli identificativi sono stabili.** `BQ3.adoption.{worst,base,best}`, `BQ3.uplift.{worst,base,best}`, `BQ3.band.spread_pp`, `BQ3.band.ratio`. Un identificativo pubblicato non cambia nome senza una nota in loco.
3. **Il prefisso `BQ3.` è disgiunto** dagli altri quattro dello spazio dei nomi unito. Verificato, e la verifica di collisione del controllo resta attiva.
4. **`adoption.base` è il valore del benchmark**, senza trasformazioni. Gli altri due ne discendono per i fattori dichiarati.
5. **L'unità di `uplift` è euro per utente al mese**, e quella di `adoption` sono punti percentuali della base.

## 3. Che cosa la `007` NON deve assumere — i cinque divieti

Questa sezione è il cuore del contratto. Ognuno dei cinque punti chiude una strada per cui un errore già commesso altrove nel progetto potrebbe rientrare.

1. **Non moltiplicare `uplift` per una base utenti.** `BQ3-K2` è euro per utente al mese e **non è scalabile**: la divergenza 9 della revisione 001, chiusa il 2026-08-10, ha deciso di non quantificare la base. L'artefatto non offre alcuna chiave con cui farlo, ed è deliberato. Un totale di ricavo costruito su questi numeri sarebbe un numero che nessuno ha misurato.
2. **Non presentare un valore singolo.** `BQ3-K1` e `BQ3-K2` sono a confidenza `bassa` e vanno **sempre** come range best/base/worst (FR-021, principio I, §6 del business case). Prendere `base` da solo perché sta meglio in una dashboard è la violazione più facile da commettere e la più difficile da vedere a valle.
3. **Non trattare il range come intervallo di confidenza.** L'ampiezza dichiara la fiducia dell'analista nel trasferimento del benchmark, non una probabilità. Non c'è alcun «95%» dentro questi tre numeri. `conventions.bq3_band_meaning` lo dice nell'artefatto, così che il divieto viaggi con i dati e non solo con questo file.
4. **Non innalzare la confidenza perché il valore è ancorato.** L'ancoraggio rende il parametro **verificabile**, non **vero per StreamWave**. È la distinzione che il principio I chiama assunzione di trasferimento ed è il contenuto di `A6`.
5. **Non leggere il tasso come netto da disdette.** È **lordo su base costante**: le disdette sono escluse per FR-018 della 001 e A5. Ne discende che `uplift` è a regime e **non** un ricavo cumulato sui 12 mesi — le due grandezze coincidono solo se nessuno disdice.

## 4. La forma delle voci

Ogni voce di `values` porta almeno `display`, `value`, `label`, `unit`; le voci di scenario portano anche `scenario`. È la struttura dei due artefatti esistenti, ed è ciò che consente al controllo di risolvere le ancore senza sapere quale feature ha prodotto il valore.

Le chiavi di `conventions` portano **tutte** il prefisso `bq3_`. Non è cosmesi: lo spazio dei nomi di `conventions` è piatto e condiviso fra artefatti, e `rounding_decimals` è già occupato con contenuto diverso (ritrovamento F2). Chi aggiunge una convenzione a questo artefatto senza prefisso la fa collidere.

## 5. Che cosa il controllo garantisce, e che cosa no

`scripts/check_audit_coherence.py` verifica che ogni cifra marcata in `docs/bq3_scenarios.md` corrisponda al valore dell'artefatto, in **severità stretta**: una quantità priva di marcatore è un errore, non un avviso.

Non garantisce, e va detto qui come lo dice §8 della fonte unica:

- che il valore del benchmark sia **quello giusto**. Il controllo confronta documento e artefatto, non artefatto e mondo;
- che l'**assunzione di trasferimento** regga. Nessun controllo può verificarla: è un'assunzione;
- che un fatto misurato non sia stato marcato come **non-misurato**. Contro la dichiarazione falsa esiste solo la revisione in contesto pulito.

`docs/business_case.md` **non è** sotto controllo, e non viene aggiunto. È la ragione per cui FR-025a e FR-027a vietano di scrivervi il valore del benchmark o le sei cifre derivate: là un numero non avrebbe ancora e nessuno lo verificherebbe — che è il rilievo R8 della 001, chiuso dalla 002 e da non riaprire.

## 6. Se il benchmark cambia

Un benchmark migliore che emerga dopo il merge **non si sovrascrive in silenzio**. Vale la prassi di [`CLAUDE.md`](../../../CLAUDE.md) sugli artefatti già mergiati: il valore originale resta, la nota in loco dichiara data, feature, valore precedente, valore corretto, causa della divergenza e fonte.

I sei valori derivati si rigenerano invece per esecuzione, perché nessuno di essi è scritto a mano (FR-014): è il motivo per cui la catena ha una sola sorgente.

**I due fattori della banda sono il caso speciale.** Sono fissati prima della ricognizione (FR-011a) proprio perché non seguano il benchmark. Cambiarli dopo aver visto un valore nuovo è ammesso, ma è la mossa che la garanzia di FR-011a esiste per rendere visibile: va dichiarata con la propria ragione, e chi la fa deve sapere che sta spostando l'unico numero libero della feature.
