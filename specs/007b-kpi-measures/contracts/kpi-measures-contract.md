# Contratto: cosa `008a`/`008b` possono presupporre leggendo `docs/kpi_measures.md` e `reports/kpi_measures.json`

**Feature**: 007b-kpi-measures | **Data**: 2026-08-22

Come il contratto della `007a`, non è un'interfaccia software: è il contratto di lettura fra questa feature e le due che la seguono nella sequenza dichiarata da `docs/roadmap.md` — `008a` (pagine e navigazione nel `.pbix`) e `008b` (narrazione e limiti a schermo). Dichiara cosa possono dare per garantito senza riaprire questa feature o la sua revisione, e cosa resta invece a loro carico.

## Cosa questi due artefatti garantiscono

1. **Un valore per ciascuno degli otto KPI**, con ancora verso `reports/kpi_measures.json` (sei KPI) o `reports/bq3_scenarios.json` (`BQ3-K1`, `BQ3-K2`, citati senza ricalcolo) — nessuno dei due mancante, nessun placeholder (SC-001).
2. **Ogni valore per-segmento esiste per tutti e 114 i segmenti**, senza eccezioni silenziose: `BQ2-K1`, `BQ2-K2`, `BQ2-K3` pubblicano una riga per segmento, e la guardia di FR-004 impedisce che lo script abbia mai scritto un artefatto con un segmento mancante o un'aggregazione vuota.
3. **La quota di popolarità zero e l'avvertimento sui 7 segmenti `is_high_zero_genre`** accompagnano ogni valore di `BQ2-K1`, mai come nota separata che chi disegna una pagina potrebbe staccare dal valore (D7, FR-008).
4. **L'invarianza del numeratore della North Star è dichiarata come fatto verificato o come divergenza esplicita**, mai come assunzione taciuta (E7, FR-013) — `008b`, che scrive la narrazione della North Star, eredita un'affermazione già chiusa in un senso o nell'altro, non un'assunzione che deve controllare da sé.
5. **Lo stato di verifica contro il motore reale è dichiarato per ciascuna misura, ancorato a `reports/kpi_engine_check.json`** (E9, FR-030, FR-029a): «verificato contro il motore reale» è una categoria diversa e più forte di «calcolato da script», e nessuna delle due compare senza che il confronto corrispondente sia realmente avvenuto.
6. **I limiti strutturali già noti sono dichiarati** — la stima per eccesso di `BQ1-K3` (D1, ereditata), la non comparabilità assoluta di `BQ2-K2` (D2, ereditata) — `008b` non li scopre a schermo già costruito.
7. **La convenzione di arrotondamento (E5) è unica e dichiarata per unità di misura**: chi legge un valore in una pagina sa già a quale precisione fidarsi, senza dover indovinare KPI per KPI.

## Cosa questi due artefatti non garantiscono, e resta a carico di `008a`/`008b`

1. **Che 114 righe per segmento siano presentabili a schermo in una forma leggibile.** `kpi_operators.md` §7.3 lo dichiara già «un problema della dashboard, non di questo operatore»; questa feature eredita e non risolve quel problema — pubblica il valore completo, non una sintesi per la presentazione.
2. **Che un valore "calcolato da script" al momento della pubblicazione resti tale per sempre.** Se E9 rivelasse, dopo la stesura di questo contratto, una divergenza non ancora chiusa quando `008a` inizia a leggere, `008a` deve verificare lo stato corrente in `docs/kpi_measures.md`, non assumere l'esito dichiarato in questo documento come immutabile.
3. **Che i limiti tecnici di questo documento siano già comprensibili a un lettore non tecnico.** `kpi_operators.md` §12 lo assegna esplicitamente a chi costruisce la narrazione (`008b`): questa feature dichiara i limiti in forma verificabile, non in forma divulgativa.
4. **Che la versione 2 di `dim_category_mood` (o una versione successiva) non richieda un ricalcolo.** Il contratto di versione di `content_taxonomy_bridge.md` §5 resta in vigore: ogni valore che dipende dalla tabella dei mood dichiara su quale versione è stato calcolato, e una revisione della tabella invalida — non corregge automaticamente — i valori già pubblicati.
5. **Che il testo DAX trascritto sia la forma definitiva della misura nel modello finale.** `008a` può adattarlo (nomi di misura, organizzazione in cartelle DAX) purché il valore che produce resti quello verificato da E9; un adattamento che cambia il valore è un ritrovamento della `008a`, non una libertà implicita.

## Come si verifica che il contratto è rispettato

Che `007b` abbia scritto un artefatto e un documento completi si verifica con [quickstart.md](../quickstart.md). Che `008a`/`008b` li abbiano letti correttamente si verificherà quando quelle feature apriranno la propria spec e dichiareranno, KPI per KPI o pagina per pagina, quale valore di `docs/kpi_measures.md` stanno presentando — non è verificabile da questa feature, che si ferma alla pubblicazione del documento e all'esito di E9.
