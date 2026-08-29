# Roadmap — StreamWave BI

**Aggiornata**: 2026-08-28 | **Stato**: `008b` revisionata e **non portata avanti** — la dashboard a quattro pagine è superata. Il progetto ha misurato tutto e non ha mai risposto; la sequenza che resta esiste per rispondere

Questo documento è il piano di lavoro del progetto: cosa resta da fare, in quale ordine, con quale stima e con quali dipendenze. È versionato perché la pianificazione — e soprattutto il suo scostamento dalla realtà — fa parte dell'artefatto da portfolio quanto i risultati.

Non sostituisce le spec: ogni voce di questa tabella diventa una cartella sotto [`specs/`](../specs/) nel momento in cui viene aperta. Qui vive solo l'ordine e il perché.

## L'unità di misura

Il principio III della constitution vincola ogni feature a **una giornata lavorativa**. La prima feature ha reso evidente che l'unità non era definita, e che la lettura a calendario e quella a sforzo davano esiti opposti: la 001 è costata circa 7 ore di lavoro effettivo — dentro il vincolo — distribuite su tre giorni di calendario. Letta a calendario, la feature che inaugurava il principio lo violava.

L'ambiguità è stata chiusa con l'emendamento **v1.0.2** della [constitution](../.specify/memory/constitution.md#iii-incrementalità): una giornata lavorativa è **6-7 ore di lavoro effettivo**, non un giorno di calendario, e il vincolo di repository coerente vale alla fine di **ogni sessione**, non solo a chiusura di feature.

Ne consegue che in questo documento le stime sono in ore e il calendario è una conseguenza della capacità disponibile, non un'unità di pianificazione. Una feature che sfora le ore va scomposta; una feature che occupa più giorni di calendario a parità di ore no.

Capacità dichiarata: **~2 ore al giorno fino al 15 agosto 2026**, giornate piene da lì in avanti.

## Stato

| ID | Feature | Ore | Dipende da | Stato |
|---|---|---|---|---|
| `001` | Business Case & KPI Framework | ~7 (spese) | — | ✅ conclusa, con debito residuo |
| `002` | Data Audit & Profiling | ~4,5 (spese, stimate 4) | 001 | ✅ conclusa, PR #2 mergiata |
| `003` | Data Cleaning & ETL | ~6,5 (spese, stimate 7) | 002 | ✅ conclusa, PR #3 mergiata, con debito residuo |
| `004` | Synthetic Business Metrics | ~3 di sessione (stimate 6) | 001 | ✅ conclusa, PR #4 mergiata, con debito residuo |
| `005` | Data Model Design | ~2,8 di sessione (stimate 5) | 003, *chore ambiente* | ✅ conclusa, con debito residuo |
| `006` | Content Taxonomy Bridge | ~4 di sessione (stimate 6) | 002, 005 | ✅ conclusa, PR #6 mergiata, con debito residuo |
| `007a` | Operatori delle misure | ~2 di sessione (stimate 4) | 005, 006 | ✅ conclusa, con debito residuo |
| `007b` | Misure DAX e documento dei KPI | ~7 di sessione (stimate 5) | 007a, *materializzazione* ✅, *`CF-1`* ✅ | ✅ conclusa, con debito residuo |
| `008a` | Dashboard: modello, pagine, misure a schermo | ~9 di sessione+GUI (stimate 5) | 007b | ✅ conclusa, con debito residuo |
| `008b` | Dashboard: narrazione, limiti esposti, rifiniture | ~6,5 di sessione+GUI (stimate 4) | 008a | 🟥 **chiusa il 2026-08-29 senza raggiungere il proprio obiettivo** |
| `009` | Il verdetto e la raccomandazione | 6 | 007b | ⬜ **apribile**, sblocca le altre |
| `010a` | Il report a 8-12 pagine: disegno e misure | 6 | 009 | ⬜ |
| `010b` | Il report a 8-12 pagine: costruzione e narrazione | 8 | 010a | ⬜ |
| `011` | Case Study & Portfolio Integration | 6 | 010b | ⬜ |
| ~~`009`~~ | ~~Porting Tableau Public~~ | ~~5~~ | — | ❌ **caduta il 2026-08-28**: aggiunge uno strumento, non una risposta |

**Totale residuo**: 26 ore di feature, più ~1,7 ore di debito testuale — **~27,7 ore**. Erano ~11,7 il 25 agosto: lo scarto è il costo della decisione del 2026-08-28, ed è dichiarato qui sotto invece di essere distribuito in silenzio sulle stime.

**La forchetta realistica è più larga della stima**, e va detto: le due feature GUI del progetto hanno sforato di quasi il doppio (`008a`, 5 stimate contro ~9 spese; `008b`, 4 contro ~5 su un perimetro poi abbandonato). Con lo stesso fattore su `010b`, che è la sola feature GUI rimasta e la più grande mai aperta, l'atterraggio sta fra **29 e 38 ore**.

Le stime di `004`, `006`, `007` e `010` includono la **revisione in contesto pulito e la chiusura dei rilievi** — circa un'ora ciascuna. Era il rischio aperto lasciato dalla 002, dove quel costo era stato l'intero scostamento; è chiuso incorporandolo invece che continuando a scoprirlo a consuntivo. La conseguenza è che `007` sale a 8 ore e raggiunge `008` fra le feature che vanno scomposte prima di essere aperte, non dopo.

> **Nota di correzione — 2026-08-18, regia.** L'elenco qui sopra **non contiene la `005`**, e non per una ragione: la sua stima di 5 ore è anteriore alla riga che istituisce la regola, e non è mai stata riallineata quando la regola è stata scritta. La `005` è quindi l'unica feature dopo la `002` ad aver affrontato revisione e chiusura dei rilievi **fuori stima**. La sessione che l'ha eseguita lo ha riportato in forma più larga — «nessuna stima di questo progetto ha mai previsto un costo di chiusura dei rilievi» — che non è esatta: quattro feature su cinque lo prevedevano.
>
> **Il difetto è però doppio, e la seconda metà conta più della prima.** L'ora stanziata è forfettaria e non scala con l'artefatto: `docs/data_model.md` è il documento più lungo del progetto e la sua revisione ha prodotto **22 rilievi e 6 divergenze**, contro i 13-14 delle tre precedenti. Chiuderli è costato il blocco intero. La correzione non è aggiungere una voce mancante, è **legare la voce alla taglia**: da qui in avanti la stima di revisione e chiusura vale ~1 ora per un documento sotto le ~400 righe e **~2 ore sopra**. Ne discende che `007` e `008` — che producono gli artefatti più densi che restano — vanno stimate con 2 ore ciascuna, non 1.
>
> **Fonte verificabile**: `specs/005-data-model-design/review.md`, blocco di chiusura; timestamp git del branch `005-data-model-design`.

> **Nota di correzione — 2026-08-21, regia.** La regola scritta due giorni fa — «~1 ora sotto le ~400 righe, ~2 sopra» — è **contraddetta dal primo caso che l'ha messa alla prova**, e va detto invece di lasciarla in piedi.
>
> `docs/content_taxonomy_bridge.md` è lungo **194 righe**, cioè metà della soglia, e la sua revisione ha prodotto **16 rilievi**, di cui 5 dichiarati bloccanti. `docs/data_model.md` ne è lungo **602** e ne ha prodotti 22. La densità è quindi più che doppia sul documento corto, e la stessa cosa era già visibile prima: `docs/bq3_scenarios.md` è lungo **183 righe** e ha prodotto **14 rilievi**, con il blocco di revisione dichiarato il più costoso della `004`. **Il dato che avrebbe smentito la regola esisteva già nel momento in cui la regola è stata scritta**, ed è stato ignorato perché la nota confrontava la `005` con la media invece che con il caso più simile.
>
> **Che cosa predice davvero il costo.** Non la lunghezza ma la **densità di affermazioni contestabili**: un documento che riporta misure fa poche affermazioni per riga e le fa verificare a un'ancora, un documento che argomenta un metodo ne fa molte e non le fa verificare da nessuno. Il ponte fra tassonomia e mood è quasi interamente della seconda specie, e per questo è corto e caro.
>
> **La correzione operativa.** La stima resta **~2 ore per feature** e smette di dipendere dalla lunghezza: `007` e `008` restano a 2 ore ciascuna, che è dove la nota precedente le aveva già portate, ma per la ragione giusta. Sotto l'ora si scende solo per un documento che pubblica misure e nient'altro, e nessuno dei documenti rimasti lo è.
>
> **Fonte verificabile**: `wc -l` sui tre documenti; conteggi dei rilievi nei blocchi di chiusura di `specs/004-synthetic-business-metrics/review.md`, `specs/005-data-model-design/review.md` e `specs/006-content-taxonomy-bridge/review.md`.

La `003` è la prima feature la cui stima conteneva la revisione, ed è la prima a chiudere **sotto** la stima: ~6,5 ore contro 7, revisione e chiusura di tredici rilievi incluse. Un solo dato non fa una serie, ma la direzione è quella attesa — lo scostamento delle prime due feature non veniva dall'esecuzione, veniva da un costo reale che la stima non conteneva.

`004` non dipende da `002` e `003`: genera dati che non esistono, quindi non ha bisogno che i dati reali siano puliti. È l'unica feature parallelizzabile e va tenuta come riserva per le giornate in cui il contesto sui dati reali non è fresco.

### Nota sulla `004` — ancoraggio a benchmark pubblici

**Decisione del 2026-08-10: accolta, rifilata.** La 004 come originariamente prevista sarebbe stato l'unico artefatto del progetto in cui la fonte di ogni parametro è "l'analista ha deciso così". Formalmente conforme — la constitution ammette i sintetici con assunzioni dichiarate a confidenza bassa — ma incoerente con la tesi del progetto, che è il principio I. I parametri di scenario vanno ancorati a benchmark pubblici di settore, con fonte, data di accesso e citazione puntuale, e legati ai KPI in un file di assunzioni versionato. La [constitution](../.specify/memory/constitution.md) li ammette fra le fonti dati dalla **v1.1.0** del 2026-08-15, a cinque condizioni.

*Correzione del 2026-08-15*: questa nota affermava che «`docs/business_case.md` §7, scheda `BQ3-K1`, prende già questo impegno». Non è esatto e va detto invece di essere riscritto in silenzio. La scheda `BQ3-K1` sta in §5.5, non in §7, e l'impegno che prende è diverso: «le assunzioni che generano i tre scenari saranno dichiarate e versionate insieme allo script che le implementa». È un impegno di **versionamento**, non di **ancoraggio a fonte esterna**, ed è tuttora da onorare. L'ancoraggio è un'aggiunta di questa decisione, non l'esecuzione di una promessa già fatta.

Il perimetro è però molto più stretto di quanto la proposta iniziale prevedesse, perché tre dei valori proposti non hanno un consumatore nel framework:

- **il churn è vietato, non facoltativo**: FR-018 della 001 esclude esplicitamente una riduzione di churn dal modello. Un benchmark di churn finanzierebbe un parametro che il framework proibisce di usare;
- **l'engagement non ha KPI**: BQ3 ha due sole misure, `premium_tier_adoption_rate` e `arpu_uplift`. Nessuna consuma engagement. Generarne un dataset produrrebbe numeri che nessuna misura legge;
- **i prezzi sono già fissati**: A4 e FR-017a li stabiliscono come valori puntuali di scenario e vietano di esprimerli a range. Nessun benchmark di ARPU serve a determinarli.

Resta **un solo benchmark indispensabile**: il tasso di conversione a un tier superiore in servizi di streaming, su cui `BQ3-K1` costruisce best/base/worst. La base utenti **non** va quantificata, per la decisione presa sulla divergenza 9 qui sotto.

**Confidenza dei parametri da benchmark**: si istituisce un'**assunzione di trasferimento** gemella di A1, non un quarto livello della scala. Un benchmark di un operatore terzo è dato osservato su qualcun altro e trasferito a StreamWave: è la stessa natura di A1, che §6 del business case tiene fuori scala per costruzione dopo il rilievo R1. Un quarto livello cambierebbe l'asse su cui tutti e 8 i KPI sono già classificati, obbligando a rivederli uno per uno, per coprire un caso che il pattern esistente copre già.

**Determinismo**: la ricerca produce un file di parametri versionato con fonte e data; uno script con seed fisso genera il dataset a partire da quel file. La pipeline resta rieseguibile da una copia pulita; la ricerca no, ed è congelata. Il precedente è il principio V, che già ammette lavoro non automatizzabile purché versionato come artefatto testuale. Se la ricerca alimentasse la generazione a ogni esecuzione, il principio II sarebbe violato.

> **Nota di correzione — 2026-08-16, feature 004, decisione D1.** La frase qui sopra prescrive che «uno script con **seed fisso** genera il **dataset**». Nessuna delle due cose accade, e la prescrizione è superata dai fatti invece che sbagliata all'origine: è stata scritta il 2026-08-10, **prima** che engagement e quantificazione della base utenti uscissero dal perimetro, cioè prima delle due decisioni che tolgono al seed il proprio oggetto.
>
> Ciò che la 004 produce è una **derivazione deterministica di sei valori** — tre tassi di adozione e i tre uplift corrispondenti — da un parametro e una costante. Non esiste alcun dataset di righe e non esiste alcun seed, e la ragione dirimente non è che il caso sia superfluo ma che sia **impossibile in linea di principio**: una simulazione a livello di individuo richiede una numerosità della popolazione, e la divergenza 9 della revisione 001 ha deciso di non quantificarla. Un seed su uno script che non estrae nulla comunicherebbe al lettore che da qualche parte c'è del caso sotto controllo, ed è falso.
>
> Resta vero tutto il resto del capoverso: il file dei parametri versionato, il congelamento della ricerca, la rieseguibilità da una copia pulita. **Fonte verificabile**: decisione D1 e requisiti FR-013 e FR-024 di [`specs/004-synthetic-business-metrics/spec.md`](../specs/004-synthetic-business-metrics/spec.md).

**Nessun framework di orchestrazione** (LangChain, LangGraph o equivalenti) per questa feature: il passaggio di raccolta produce un valore congelato che nessuno riesegue, e un'orchestrazione a grafo aggiungerebbe una dipendenza, una chiave API e un componente che dopo la prima esecuzione resta inerte. La sede in cui il lavoro con LLM ha senso è la `006` — vedi Decisioni aperte.

**Se nessuna fonte regge le cinque condizioni — decisione della regia, 2026-08-16.** È l'assunzione più esposta della feature e la spec la dichiara non confermata. La decisione è presa in anticipo perché non blocchi l'implementazione a metà: **la feature non si ferma.** Prosegue dichiarando il parametro come **scelta dell'analista**, che è lo stato ammesso prima dell'emendamento a v1.1.0, e registra la ricognizione fallita con le fonti valutate e i motivi del rigetto. Tutto il resto — derivazione, documento, chiusura di R13-BQ3, `A6` e le note sulle schede — è indipendente da dove viene il numero e vale da solo.

La ricognizione fallita **è essa stessa un risultato pubblicabile**: «abbiamo cercato un benchmark citabile per questa metrica e non esiste in forma gratuitamente recuperabile» è un'informazione che il lettore non ha, ed è più onesta di un numero preso da una fonte che non regge il controllo. Resta intatto il divieto di FR-006 nella sostanza — non inventare, non ripiegare in silenzio — e resta obbligatorio il riporto di T013: cambia solo che la risposta è già scritta e non va attesa.

**Stima**: da 5 a 6 ore. L'ancoraggio aggiunge circa un'ora di raccolta e citazione, l'uscita dell'engagement dalla generazione ne restituisce altrettante, la revisione in contesto pulito ne aggiunge una. Resta **una sola feature dentro il limite del principio III**: la scomposizione che la proposta dava per necessaria non serve, perché contava dentro la feature l'emendamento della constitution e le note testuali, che sono chore. Da riverificare in fase di `/speckit.specify`.

### Esito della `003` — chiusa il 2026-08-15

**49 task su 49**, in due sessioni e ~6,5 ore: l'11 agosto spec, piano, task e MVP fino a T026; il 15 agosto il documento, il controllo esteso, le note in loco, la revisione e la chiusura dei suoi rilievi. I 49 task sono uno in più dei 48 pianificati: T049 è stato aggiunto in corsa per chiudere un drift del README che la regia aveva segnalato l'11 agosto e che nessun task copriva.

Lascia quattro artefatti: `scripts/build_datasets.py`, [`reports/cleaning_report.json`](../reports/cleaning_report.json), [`docs/data_cleaning.md`](data_cleaning.md) e [`docs/convenzioni-marcatura.md`](convenzioni-marcatura.md). I quattro dataset di output non sono versionati per il principio II: lo è la pipeline che li rigenera.

**Tre esiti che valgono oltre la feature.**

*La regola D5 diventa metodo di progetto.* Un confronto, una graduatoria o un rapporto costruiti su valori misurati sono essi stessi valori misurati: o hanno un identificativo nell'artefatto, o non si scrivono. La feature l'ha adottata per i propri artefatti e si è fermata prima di scriverla in `CLAUDE.md`, dichiarando che portarla al progetto è atto di governance. È stata portata il 2026-08-15, con le due precisazioni che il rilievo R7 della sua revisione ha reso necessarie.

*La chiave di lettura esce dalle cartelle di lavorazione.* La grammatica di marcatura viveva in due contratti sotto `specs/`, e due documenti pubblicati vi rinviavano. È ora in [`docs/convenzioni-marcatura.md`](convenzioni-marcatura.md), fonte unica, con i due contratti che portano una nota di trasferimento datata e nulla rimosso. La ragione non è il lettore esterno ma la `004`: avrebbe scritto prosa con la stessa grammatica citando la cartella di lavorazione di un'altra feature, e da lì in poi ogni documento avrebbe ereditato il rinvio sbagliato.

*La revisione in contesto pulito ha ripagato il proprio costo.* Tredici rilievi, tutti verificati esatti, nessuno caduto. Il più grave — R1 — mostrava che il meccanismo su cui il documento fonda la propria credibilità falliva **in silenzio** proprio sul numero di testa della prima decisione: una sostituzione automatica aveva rotto cinque ancore, il Markdown reso mostrava `15.844.rows.after-->` al lettore, e il controllo passava. Nessun controllo automatico lo aveva visto perché era il controllo stesso a essere cieco. Diversi rilievi non si chiudevano riscrivendo una frase: hanno richiesto **nuovi valori** nel rendiconto, perché D5 non ammette altra strada — un confronto o ha un identificativo o non si scrive.

**Il ritrovamento del contratto è stato chiuso.** Il disallineamento fra il contratto degli output scritto in fase di piano e ciò che l'implementazione ha prodotto, rinviato a T029 (commit `0e959a7`), è rientrato: `005` e `007b` leggono un contratto che descrive i file reali.

Resta debito, tracciato sotto.

### Esito della `004` — chiusa il 2026-08-17

**46 task su 46**, in due blocchi di sessione: il 16 agosto dalla spec alla Prova 9 del quickstart, il 17 la chiusura dei rilievi della revisione. I timestamp git coprono ~3 ore contro le 6 stimate, e **lo scarto non va letto come un risparmio**: vale la nota sulla misura del tempo speso più sotto, per cui i timestamp misurano una sessione di agent e non ore-uomo. Ciò che si può dire è che la feature è rientrata nel proprio perimetro senza sforare, e che il blocco E — revisione e chiusura dei rilievi — è stato il più costoso, come previsto.

Lascia quattro artefatti: [`data/benchmarks/bq3_tier_upgrade.json`](../data/benchmarks/bq3_tier_upgrade.json), `scripts/build_bq3_scenarios.py`, [`reports/bq3_scenarios.json`](../reports/bq3_scenarios.json) e [`docs/bq3_scenarios.md`](bq3_scenarios.md). Il primo è la prima cartella di `data/` a essere versionata, e per il motivo opposto a quello delle sorelle: le altre non lo sono perché riproducibili, questa lo è perché non lo è.

**Quattro esiti che valgono oltre la feature.**

*Una proprietà dichiarata in una decisione va verificata sull'implementazione.* La decisione D2 prescriveva una banda «simmetrica in termini relativi». L'implementazione l'ha letta come `1 − k` / `1 + k`, che **non lo è**: la simmetria relativa vale se e solo se il prodotto dei due fattori è l'unità. La banda è stata simmetrica in termini assoluti mentre si dichiarava relativa, per tutta la durata della feature, attraverso spec, piano, contratto, implementazione e due punti di stop della regia. Nessun controllo di questo progetto poteva vederlo — non è un numero sbagliato, è una proprietà mancante — e l'ha trovato la revisione in contesto pulito leggendo il solo documento pubblicato.

*Un esito verde può essere prodotto dal fallimento del comando che doveva verificare.* La Prova 9 del quickstart eseguiva `git diff main -- docs/business_case.md | grep "^-"`. Su un clone `main` non esiste come riferimento locale: git esce con `fatal: bad revision`, non produce output, il `grep` non trova corrispondenze e la prova **riporta esito positivo**. È rimasta così finché il quickstart non è stato eseguito per intero su un clone, cosa che le verifiche di fase — che eseguono le prove una alla volta, nel repository di lavoro — non fanno.

*La regola sulle cifre significative non si applica al denaro.* Il principio I vieta di pubblicare un valore sintetico con precisione superiore a quanto la metodologia giustifica. Applicata alla lettera a un importo produce `1,2 €` dove il valore è `1,20 €`, perché il centesimo è l'unità in cui la valuta è denominata e non una cifra di precisione rivendicata. FR-015 distingue ora due famiglie — cifre significative per i tassi, posizioni decimali fisse per gli importi — e la convenzione dichiara che la precisione effettiva resta quella dell'ingresso. **Vale per ogni documento futuro che pubblichi euro**, cioè per `007b` e `008a`.

*Il registro dei rigetti non certifica una superlatività.* Rende ispezionabile perché una fonte è stata scartata, ma è compilato da chi sceglie e contiene solo le fonti incontrate: lo spazio di quelle mai trovate non lascia traccia. La rivendicazione sostenibile è «la migliore fra quelle esaminate, secondo un criterio dichiarato», e il criterio adottato qui — solidità della citazione prima della vicinanza al caso d'uso — ha una conseguenza visibile, perché una fonte più vicina per misura è stata respinta perché la citazione non reggeva.

**La ricognizione ha funzionato, ma per poco.** La fonte adottata soddisfa le cinque condizioni della constitution; il suo scarto di misura è ampio e dichiarato in cinque divergenze, di cui **una sola ha un verso noto**, e spinge il valore verso l'alto. Il terzo punto di fermata previsto — T013, il riporto in entrambi gli esiti — è servito esattamente a ciò per cui era stato messo: non a segnalare un fallimento, ma a portare alla regia una fonte adottata con la propria debolezza, su cui la decisione poteva essere diversa.

### Esito della `005` — chiusa il 2026-08-18

**45 task su 45**, in due blocchi: la notte del 17 dalla spec al MVP del documento, il 18 sera il completamento, la revisione e la chiusura dei rilievi. I timestamp git coprono ~2,8 ore contro le 5 stimate, con la solita avvertenza — misurano una sessione di agent, non ore-uomo. T045 è stato aggiunto in corsa, come T049 sulla `003`.

Lascia **un solo artefatto**, [`docs/data_model.md`](data_model.md), ed è il più lungo del progetto. È la prima feature a non produrre né dati né codice: il suo output è una descrizione, e la constitution lo impone — il principio V vuole schema e mapping dei campi come artefatti testuali invece che come contenuto di un file binario.

**Chiude due voci di debito della `001`** che nessuna feature precedente poteva chiudere: la definizione operativa di «segmento» (R4 / divergenza 1) e la granularità di `BQ2-K2` (R7 / divergenza 7). Entrambe atterrano su `docs/business_case.md` come note in loco, e le due note **non sono dello stesso tipo** — una correzione dove l'affermazione era insufficiente, una nota di adozione dove l'espressione era ambigua e non sbagliata. La distinzione è quella che la prassi di correzione prescrive, ed è la prima volta che viene applicata per intero.

**Tre esiti che valgono oltre la feature.**

*Un documento senza artefatto proprio può stare in severità stretta.* `docs/data_model.md` non genera alcun file sotto `reports/`: le sue 198 ancore risolvono contro gli artefatti delle feature precedenti. Ne discende che la severità stretta non richiede che una feature produca dati — richiede che ogni suo numero venga da qualche parte, il che è cosa diversa e più debole. È ciò che rende il regime applicabile anche a `007a`, `007b` e `010`, che pubblicheranno prosa su misure calcolate altrove.

*Il presidio contro il verde falso è entrato nelle prove.* La Prova 6 del quickstart è l'unica in cui l'assenza di output è l'esito atteso, ed è quindi l'unica esposta al difetto che aveva prodotto un esito positivo sulla `004` — un comando fallito che non stampa nulla. La prova stampa il codice di uscita e distingue `1`, cioè ha cercato e non ha trovato, da `2`, cioè non ha potuto cercare. È la lezione della `004` diventata forma.

*Il blocco di chiusura distingue quattro esiti e non due.* Ai due della `004` — *risolto* e *indebolito* — se ne aggiungono altri due: *respinto*, con la prova a fianco, e *rinviato* fuori perimetro. Tre rilievi sono stati respinti in tutto o in parte, ciascuno con il proprio controllo. È un miglioramento e va tenuto: un verbale in cui nessun rilievo cade non sta dimostrando che il revisore avesse sempre ragione, sta dimostrando che nessuno ha controllato.

**La revisione ha trovato ciò che nessun controllo poteva vedere**, come nelle tre precedenti e con margine più largo: 22 rilievi e 6 divergenze su un documento già riletto da chi lo aveva scritto. Fra questi un fatto misurato dichiarato non-misurato — la categoria che le convenzioni indicano esplicitamente come impresidiabile dallo script — una contraddizione fra due sezioni distanti, e una decisione analitica che tre feature diverse avrebbero potuto ciascuna supporre presa da un'altra.

### Esito della `006` — chiusa il 2026-08-20

**44 task su 44**, in tre blocchi del 19-20 agosto: spec e piano nella notte, criterio-proposta-verifica-congelamento nella mattina, revisione e chiusura dei rilievi in serata. I timestamp git coprono ~4 ore contro le 6 stimate, con un'avvertenza più forte del solito — vedi sotto.

Lascia **quattro artefatti**: [`docs/mood_assignment_criteria.md`](mood_assignment_criteria.md), [`data/curated/dim_category_mood_proposal.json`](../data/curated/dim_category_mood_proposal.json), [`data/curated/dim_category_mood.json`](../data/curated/dim_category_mood.json) e [`docs/content_taxonomy_bridge.md`](content_taxonomy_bridge.md). È la prima feature a produrre valori che **nessuna fonte osserva e nessuna formula calcola**, ed è la ragione per cui ha richiesto l'emendamento **v1.2.0** della constitution prima di poter cominciare.

**Chiude tre voci di debito ereditate**, una per ciascuna delle tre feature che l'avevano rinviata: la governance della tabella (divergenza 10 della `001`), chi si accorge di un cambio di tassonomia (divergenza 5 della `002`), e gli attributi di record negli artefatti versionati (divergenza 5 della `003`, per la parte che questa feature poteva decidere). È il rendimento della regola per cui una decisione si prende dentro la feature che ne ha bisogno: tre divergenze aperte da tre revisioni diverse si sono chiuse nella stessa sessione perché era la prima in cui servivano tutte e tre.

**Tre esiti che valgono oltre la feature.**

*L'ordine dei passi ha retto, e si può dimostrare che ha retto.* Il criterio è stato committato da solo, `0d950e6`, prima che qualunque valore esistesse; la proposta è arrivata dopo, `acf18c1`; la tabella congelata dopo ancora, `57c4781`. Il documento pubblica il comando che ricostruisce quell'ordine, e chiunque può eseguirlo. È il presidio su cui `DA-1` era stata decisa, ed è l'unico del progetto che non poggia su una dichiarazione ma su una cronologia.

*La verifica indipendente ha spostato due celle su 126, e il numero non dice ciò che sembra dire.* Il documento lo pubblica come `MOOD.review.changes_count` e ne dichiara il limite nello stesso punto: un conteggio basso può descrivere una proposta aderente al criterio oppure un criterio che non dà appigli, e da solo non distingue i due casi. La verifica ha però prodotto una seconda categoria di esito che il piano non prevedeva — i **ritrovamenti sul criterio**, `CF-1`, `CF-2`, `CF-3` — che sono difetti del metro e non contestazioni a singole righe. Le celle interessate sono rimaste ferme perché sceglierne una delle due regole in conflitto sarebbe stato decidere sul criterio, non verificare contro il criterio. È la distinzione che rende il registro leggibile, e non esisteva prima di questa feature.

*Un controllo di coerenza verde non esegue i comandi che il documento pubblica.* Il documento proponeva in due punti un `git log --follow` con più percorsi, che git rifiuta — `fatal: --follow requires exactly one pathspec`. Era lì dalla prima stesura, è passato sotto un esito verde, e il revisore non poteva vederlo perché il mandato gli vietava di eseguire comandi. Lo ha trovato la chiusura di `R5`, verificando il comando che il rilievo chiedeva di allineare. **Vale per `007a`, `007b` e `010`**: un blocco di comandi in un documento pubblicato è una promessa al lettore, e nessun controllo di questo progetto la verifica.

**La misura del tempo, qui, non ha funzionato.** Fra il commit del verbale e quello che chiude i sedici rilievi passano nove ore di orologio, e l'ultimo blocco appare nei timestamp come tredici minuti. Non è né l'una né l'altra cosa. Le ~4 ore dichiarate sopra sono la somma dei tre addensamenti di commit e vanno lette come il limite inferiore di ciò che la feature è costata, non come una stima. È il caso che mostra il confine della [nota sulla misura del tempo speso](#nota-sulla-misura-del-tempo-speso): i timestamp misurano una sessione di agent, e quando la sessione si interrompe smettono di misurare qualunque cosa.

### Esito della `007a` — chiusa il 2026-08-21

**19 task su 19**, in un blocco unico di ~2 ore contro le 4 stimate. È la feature più veloce del progetto, e la ragione è dichiarabile: **il lavoro analitico era già stato fatto nella spec.** Le nove decisioni erano argomentate per intero prima del piano, e l'implementazione le ha trasposte in un documento invece di prenderle. Chi legge lo scostamento come efficienza di esecuzione legge male: è lavoro spostato a monte, dove il primo punto di fermata lo ha potuto revisionare.

Lascia **un solo artefatto**, [`docs/kpi_operators.md`](kpi_operators.md), sesto documento sotto controllo di coerenza in severità stretta, 90 marcatori, nessun valore dei KPI.

**Chiude sei voci di debito ereditate da tre revisioni diverse**: `R5`, `R6` e le divergenze 2, 3, 4 della `001` (gli operatori indefiniti, che erano il contenuto principale della feature), la divergenza 8 per la parte sul segno, `R13` per le due parti residue, la divergenza 4 della `002` e la divergenza 1 della `003`. Il debito più vecchio del progetto — aperto dalla prima revisione, il 2026-08-06 — è chiuso.

**Tre esiti che valgono oltre la feature.**

*La revisione al primo punto di fermata ha trovato un buco che nessuno cercava.* La condizione `C1` della regola di decisione della North Star è assegnata da `business_case.md` §3 a `BQ1-K1`, ma **non è calcolabile** da `music_adjacent_catalog_share`: quella è una quota, `C1` chiede una graduatoria di categorie per numero di titoli. La spec dichiarava che le condizioni prive di operatore fossero due, `C2` e `C3`. Erano tre. Trovato leggendo la spec contro il business case, prima del piano — e se fosse arrivato in `007b`, sarebbe arrivato come blocco su un operatore mancante della metrica di riferimento.

*Un'ancora valida può sostenere un ragionamento sbagliato.* Il numeratore della North Star, 375 titoli musicali, è ancorato al profilo del **dato di origine**; nessun identificativo `CL.NF.*` lo conta dopo la trasformazione. Il controllo di coerenza risolveva l'ancora e passava: verifica che il numero venga da qualche parte, non che venga dal posto giusto per l'uso che se ne fa. È la stessa classe della divergenza già aperta dalla `005` sui 114 segmenti, e la `007a` la chiude nell'unico modo che il progetto ammette — scrivendo l'invariante invece di ricontare — ma dichiarandolo **assunzione** e non dimostrazione, dopo che la revisione in contesto pulito ha mostrato che i fatti citati non la dimostravano.

*I rilievi minori diventano issue, non ore di piano.* Due rilievi su sei sono stati **rinviati** e registrati come issue su GitHub (`#7` e `#8`) invece di essere chiusi dentro la feature. È la prima volta che il progetto usa il tracker, ed è una scelta di metodo: un rilievo che non invalida alcun operatore non giustifica di allungare la feature, ma sparisce se resta solo nel verbale. L'issue è il posto in cui una decisione di rinvio resta visibile a chi non legge i verbali.

### Esito della `007b` — chiusa il 2026-08-23

**~7 ore di sessione contro 5 stimate**, e lo scostamento ha una causa dichiarabile riga per riga: la revisione in contesto pulito ha prodotto **14 rilievi**, il numero più alto del progetto dopo `data_model.md`, su un documento che per la prima volta pubblica valori invece di regole. Sei chiusi dentro la feature perché toccavano affermazioni false o valori che non reggevano; otto rinviati come issue (`#12`-`#19`), per la regola del 2026-08-22.

Lascia tre artefatti nuovi — `scripts/build_kpi_measures.py`, [`reports/kpi_measures.json`](../reports/kpi_measures.json), [`docs/kpi_measures.md`](kpi_measures.md) — e uno curato a mano, [`reports/kpi_engine_check.json`](../reports/kpi_engine_check.json): la prima volta che il progetto congela un'osservazione umana sul motore reale invece di un output di script, sul precedente di `data/benchmarks/bq3_tier_upgrade.json`. Settimo documento sotto controllo di coerenza, sesto in severità stretta.

**Il fatto che conta più di ogni rilievo: `E9` ha trovato un difetto reale, e lo ha trovato dove doveva.** La revisione della regia sulla prima versione della spec aveva spostato la verifica contro il motore Power BI da limite dichiarato e permanente a passo eseguito dentro la feature, prima del merge — ed è quel passo che ha trovato che tre colonne di `dim_track` (`energy`, `valence`, `danceability`) erano caricate nel modello con il punto decimale letto come separatore delle migliaia: `0.396` valeva `396`. Tre KPI su otto ne uscivano sbagliati di due ordini di grandezza — `mood_profile_overlap`, `segment_catalog_affinity` e, per composizione, `segment_entry_priority` — sotto un esito verde di ogni controllo automatico del repository, perché il difetto viveva nel `.pbix`, che nessuno script tocca. **Il costo di trovarlo qui è stato di due letture; a valle, dentro `008a`, sarebbe stato il costo di rifare le pagine costruite su numeri sbagliati.**

**Un rischio resta aperto, e non è di questa feature: nessun presidio impedisce che l'errore si ripeta.** Il `.pbix` non è versionato; una nuova materializzazione ripeterebbe la tipizzazione sbagliata senza che alcun controllo di questo repository se ne accorga, perché nessuno di essi legge dentro il modello. È registrato come issue `#11` e come rischio aperto qui sotto — riguarda direttamente `008a`, la prossima feature a toccare il `.pbix`.

### Esito della `008a` — chiusa il 2026-08-25

**Due giornate di calendario, ~9 ore fra sessione e GUI contro le 5 stimate**, e la cifra va letta con più cautela del solito: la parte non scriptabile della feature — costruire quattro pagine, verificare a schermo, correggere due difetti di caricamento — non lascia lo stesso tipo di traccia nei timestamp git di un documento scritto da una sessione, per la stessa ragione già registrata nella [nota sulla misura del tempo speso](#nota-sulla-misura-del-tempo-speso). Lo sforamento è comunque reale: la revisione ha prodotto **25 rilievi**, il numero più alto del progetto, su una feature che per la prima volta produce un artefatto — il `.pbix` — che nessuno script di questo repository può leggere.

**La struttura scelta il 22 agosto ha retto.** Sessione scrive il contratto di pagina, punto di fermata, Valerio costruisce, sessione documenta l'esito — ed è quella struttura ad aver reso possibile trovare due difetti che altrimenti nessuno avrebbe visto: `dim_title` caricava 8.809 righe invece di 8.807 per un `QuoteStyle` sbagliato su due record con un ritorno a capo dentro un campo quotato, e la tabella disconnessa di `BQ3` aveva perso la colonna `scenario`. Nessuno dei due è un errore nei valori pubblicati dalla `007b` — sono difetti di **come il modello li legge**, una terza categoria che il progetto non aveva ancora nominato accanto a *scostamento* (differenza dal contratto) e *ritrovamento* (differenza dal valore pubblicato). La distinzione è stata scritta perché serviva, non prima: `data-model.md` §1.1 l'aveva già prevista in una riga («se il modello caricato ne mostrasse di diversi, è un difetto di caricamento»), ma non le aveva ancora dato un nome proprio nel vocabolario del progetto.

**Il rischio che la `007b` aveva registrato — la tipizzazione delle colonne di mood può ripresentarsi — non solo si è confermato ma si è esteso.** ★1 ha verificato che il difetto specifico non c'era in questa materializzazione, ma la feature ne ha trovati altri due della stessa famiglia: impostazioni che vivono solo dentro un file non versionato, invisibili a ogni controllo automatico, perse una volta e ricostruite a mano. L'issue `#11` non chiude — resta aperta perché un esito positivo oggi non è una garanzia per domani — e viene assorbita da una issue più larga, `#20`, che elenca tutte e tre le impostazioni come punti da riverificare a ogni riapertura del `.pbix`. È un rischio strutturale del deliverable, non un difetto di questa feature: nessun controllo del repository entra nel modello, ed è esattamente il confine che il principio V traccia.

**Tre decisioni prese al terzo punto di fermata, tutte confermate in costruzione.** `CP-1` (due misure companion scritte ex novo) e `CP-2` (tabella disconnessa per `BQ3`) sono state eseguite come proposte, con le rispettive letture coincidenti con i valori pubblicati — nessun ritrovamento. `CP-3` (la North Star ripetuta su due pagine) è stata eseguita come approvata. Le tre erano state sottoposte alla regia prima di aprire Power BI, seguendo esattamente la struttura decisa: il costo di deciderle è stato di una lettura, non di una ricostruzione.

**Un'interazione prevista dal contratto si è rivelata non disponibile nello strumento.** La selezione incrociata fra dispersione e graduatoria di `BQ2` presupponeva l'evidenziazione, che Power BI non offre per quei due tipi di visual; l'alternativa (il filtro) avrebbe fatto sparire gli altri segmenti dalla graduatoria, quindi l'interazione è stata disattivata in entrambe le direzioni. È uno scostamento dal contratto, dichiarato con la propria ragione, non un difetto — e la scelta conservativa (disattivare piuttosto che accettare un filtro che nasconde dati) è la stessa logica di `F2`/`F4`: mai una grana non pubblicata, nemmeno per un clic accidentale. Rinviato come issue `#21`.

**Sul debito ereditato dalla `007b`, entrambe le issue restano aperte per lo stesso motivo — un esito positivo oggi non prova un vincolo per sempre.** `#11` (tipizzazione delle colonne di mood) è verificata assente in questa costruzione, non risolta in generale. `#18` (`ALL` mancante su `mood_profile_overlap`) non si manifesta perché nessuna pagina espone un filtro di categoria — ma la formula resta quella pubblicata, e chi la esporrà in un contesto filtrabile deve chiuderla prima.

### Esito della `008b` — chiusa il 2026-08-29 senza raggiungere il proprio obiettivo

**È la prima feature del progetto che non consegna ciò per cui era stata aperta**, e va registrata come tale invece che ammorbidita. Doveva rendere il `.pbix` pubblicabile; l'ha dichiarato tale il 28 agosto, e la revisione in contesto pulito ha risposto no sul metro che la feature stessa si era data. La dichiarazione è stata **ritirata**.

**~6,5 ore fra sessione e GUI contro le 4 stimate**, di cui ~1,5 per la sola chiusura. Lo sforamento non è il dato interessante: il dato è che le ore sono state spese su un deliverable poi superato — vedi [Il verdetto mancante](#il-verdetto-mancante--decisione-della-regia-2026-08-28), che è la decisione presa in conseguenza di questa revisione.

**Che cosa la feature ha comunque prodotto, e che non va perso.** Trentadue blocchi di testo il cui contenuto letterale vive nel repository, in `contracts/narrative-contract.md`, scritto **prima** che Power BI venisse riaperto — il terzo punto di fermata ha retto anche qui. Il testo non andrà a schermo, ma il lavoro di riduzione di ogni limite tecnico a una forma leggibile è materiale che la `010b` riprende invece di rifare. E soprattutto ha prodotto il verbale che ha fermato il progetto in tempo.

**Il ritiro poggia su un argomento interno al documento ritirato**, ed è la parte che conta per il metodo. La §4 del contratto di pubblicabilità elencava la revisione in contesto pulito come **il primo dei tre presidi** su cui la garanzia poggiava. Quel presidio ha risposto no. Nelle parole del blocco di chiusura: *«un presidio che si nomina come fondamento e poi si ignora quando risponde no non era un presidio: era un ornamento»*. Il criterio `N8` non era sbagliato ed era stato fissato prima di costruire — il revisore lo dice per primo. **È caduta la misura, non il metro.**

**La chiusura ha rispettato la regola del 2026-08-22 nella sua forma più stretta mai applicata**: tre rilievi su venticinque chiusi, ventidue rinviati con numero. Il criterio dichiarato è più preciso di quello generale e vale la pena registrarlo, perché è riusabile: *si chiudono soltanto i rilievi per cui un documento che **resta nel repository** afferma il falso*. I rilievi sul testo a schermo non si chiudono, perché quel testo non andrà più a schermo e la riparazione andrebbe persa insieme al file.

**Un ritrovamento che la revisione non poteva fare.** La frase mal contata di `R18` — «le undici prove manuali», dove le prove eseguite sono dieci — esisteva in **due** copie, e la seconda sta in un documento che il revisore non aveva ricevuto. Non è un rilievo mancato: è una conseguenza del perimetro, e mostra il limite strutturale della revisione su estratti isolati. Vale la pena tenerlo a mente quando si comporrà il perimetro della revisione della `009`.

## Debito della feature 008b

| Voce | Origine | Stato |
|---|---|---|
| `R5a` — la ragione registrata per l'unico taglio in costruzione è contraddetta dalla tabella che la precede | revisione `008b` | ✅ **risolto** con nota in loco, che dichiara le due letture e non sceglie fra loro |
| `R5b`, `R6` — il file è dichiarato pubblicabile mentre lo stesso documento ne registra una riga tronca a schermo | revisione `008b` | ✅ **indeboliti**: ritirata la rivendicazione. La riga tronca si dichiara, non si ripara — il file è superato |
| `R18` caso 4 — le prove manuali eseguite sono dieci, non undici | revisione `008b` | ✅ **risolto** in entrambi i punti in cui la frase compare |
| `R1`, `R2`, `R7`, `R8`, `R14`, `R17`, `R19`, `R21` — il testo dice cosa non concludere e mai cosa si può concludere | revisione `008b` | ⬜ issue [`#28`](https://github.com/Valvln/streamwave-bi/issues/28) — **requisito della `009`** per la sostanza, della `010a` per l'impaginazione |
| `R3`, `R4`, `R9`, `R10`, `R11`, `R12`, `R13`, `R20`, `R22` — difetti localizzati del testo a schermo | revisione `008b` | ⬜ issue [`#29`](https://github.com/Valvln/streamwave-bi/issues/29) — alla `010b`, che riscrive la narrazione da zero |
| `R15`, `R16`, `R18` (casi 1-3), `R23`, `R24`, `R25` — difetti dei documenti di feature | revisione `008b` | ⬜ issue [`#30`](https://github.com/Valvln/streamwave-bi/issues/30) — alla `011`, con l'arretrato del tracker |
| `#26`, `#27` — aperte dalla `008b` durante la costruzione | `008b` | ⬜ aperte |

**Il `.pbix` a quattro pagine resta sul disco di Valerio e non viene toccato.** Non è pubblicabile, non è versionato, e la `010b` lo sostituisce. Le tre impostazioni fragili dell'issue `#20` restano da riverificare a ogni riapertura, `010b` inclusa.

### Il verdetto mancante — decisione della regia, 2026-08-28

La revisione in contesto pulito della `008b` è tornata con **25 rilievi** e un giudizio complessivo negativo sul metro che la feature stessa si era data. La frase che conta non è nessuno dei rilievi:

> Trentadue blocchi dicono al lettore che cosa non concludere; nessuno gli dice che cosa può concludere. […] un decisore che non conclude niente non ha usato la dashboard — l'ha archiviata.

Il difetto non è della `008b`, che è solo la feature in cui è diventato visibile, perché è la prima che ha messo il lavoro davanti a un lettore invece che davanti a un controllo. **Nove feature hanno costruito un apparato di misura impeccabile e non hanno mai risposto alla domanda per cui esiste**: StreamWave può entrare nel music streaming?

**Il ritrovamento che rende la correzione più economica di quanto sembri.** La risposta esiste già, ed è positiva. [`business_case.md`](business_case.md) §3 contiene la regola di decisione — tre condizioni, fissate e pubblicate **prima** di misurare, con la lettura di ciascun esito già scritta. Lo stato reale al 2026-08-28:

| | Condizione | Misurata da | Stato |
|---|---|---|---|
| `C1` | la categoria musicale sta nella metà superiore per numero di titoli | `BQ1-K1` | **soddisfatta**, ancorata a `KPI.BQ1K1.c1.above_median` |
| `C2` | la maggioranza del catalogo musicale ricade nella regione di mood del catalogo video | `BQ1-K3` | il valore è `0,8450` contro una soglia di `0,50`, ma **non esiste** come booleano ancorato — è la issue [`#17`](https://github.com/Valvln/streamwave-bi/issues/17) |
| `C3` | esiste almeno un segmento nella metà superiore per domanda **e** per affinità | `BQ2-K3` | **soddisfatta**, ancorata a `KPI.BQ2K3.c3_satisfied` |

**Tre su tre**, e il business case dichiara già che cosa significa, con la cautela incorporata: *«l'argomento di coerenza è sostenuto: l'espansione è un'estensione del catalogo esistente»*, seguito immediatamente da *«Non dice che l'espansione sarà redditizia: dice che sarebbe coerente.»*

Il progetto non ha mancato un'analisi. Ha eseguito la parte difficile e si è fermato un passo prima della fine, per una soglia mai dichiarata e un'ancora mai scritta.

**Perché sbilanciarsi non viola nulla.** La constitution fissa un solo criterio di accettazione — *reggere la presentazione a un board reale* — e non contiene alcuna norma che imponga l'astensione. La regola D5 sulle affermazioni derivate non vieta il verdetto: **spiega come pubblicarlo**, cioè con un identificativo proprio e un'ancora, come qualunque altro valore. E `N7` della `008b` — *«non conclude, non raccomanda»* — è una decisione di feature poggiata su una lettura contestabile del criterio del board, non un principio: si ribalta senza emendare la constitution e senza toccare un documento pubblicato.

**Che cosa questo dimostra sul metodo, ed è la ragione per cui va scritto qui.** La regola di decisione fu fissata prima dei numeri proprio perché il verdetto non potesse essere spostato dopo. Applicarla adesso è l'unico uso per cui era stata scritta; non applicarla l'avrebbe resa un ornamento. La cautela che ha fermato il progetto un passo prima della fine non era rigore: era il rigore che continua a girare dopo che ha finito il proprio lavoro.

**Un esempio di che cosa significa sbilanciarsi *con* rigore**, perché è il contenuto della `009` e non una figura retorica. `C2` è la più debole delle tre: poggia su una stima che il progetto stesso dichiara per eccesso ([`kpi_measures.md`](kpi_measures.md) §4.3). Ma la distanza dalla soglia è di **34,5 punti** — perché `C2` cada, la sovrastima dovrebbe superare un terzo dell'intero catalogo musicale. Un limite dichiarato diventa così un argomento di robustezza, e il margine è un valore derivato che si ancora come tutti gli altri. Oggi a schermo di tutto questo c'è solo l'inquietudine: è il rilievo `R19` del verbale.

#### Che cosa cambia, e che cosa no

**Niente di ciò che è pubblicato diventa falso**, e non c'è alcuna ritrattazione da fare sui documenti. Restano invariati `data/raw/`, i tre script di costruzione, `data_audit.md`, `data_cleaning.md`, `content_taxonomy_bridge.md`, `mood_assignment_criteria.md`, `dim_category_mood.json`, `bq3_scenarios.md` con artefatto e script, `data_model.md`, `convenzioni-marcatura.md`. **`business_case.md` resta invariato**: contiene già la regola, e va eseguita, non riscritta.

Crescono **in aggiunta**, senza riscritture: `kpi_measures.md` con l'artefatto e lo script che lo alimenta, per l'operatore di `C2`, il booleano, il verdetto congiunto e il margine di robustezza; `kpi_operators.md` con una nota in loco per la soglia di «maggioranza»; il README. Nasce un documento nuovo sotto `docs/` — la raccomandazione, l'unico artefatto che il progetto non ha mai avuto.

Sono superati il `.pbix` a quattro pagine e il contratto di narrazione della `008b`.

#### La sequenza, e perché l'ordine conta più del numero

1. **`009` — il verdetto e la raccomandazione** (~6 h, nessuna GUI). Pubblica `C2`, il verdetto congiunto e il margine; scrive la raccomandazione: la risposta, con quale segmento entrare, quanto vale, sotto quali condizioni cambierebbe.
2. **`010a` — disegno del report a 8-12 pagine** (~6 h) e le misure e visuali nuove che richiede.
3. **`010b` — costruzione e narrazione** (~8 h), con la stessa struttura a tre punti di fermata che ha retto su `008a`.
4. **`011` — case study** (~6 h), che raccoglie anche l'arretrato del tracker.

**La `009` viene prima del disegno, e non è un dettaglio di sequenza.** La dashboard attuale è organizzata per framework di KPI — una pagina per domanda di business — cioè è un inventario. Un report da analista è organizzato per argomento: la domanda, la risposta, perché, che cosa la ribalterebbe, quanto vale, che cosa costa. Le pagine nuove devono essere quella spina, e non si impagina lungo un argomento che non è ancora scritto. È lo stesso errore di ordine che il progetto ha già evitato due volte — il contratto prima della costruzione — applicato un livello più in alto.

**Sulla base utenti.** La revisione della `001` decise di non quantificare alcuna base di abbonati, e il rilievo `R8` della `008b` mostra il prezzo: a schermo resta l'invito a moltiplicare senza il presidio che lo qualificava, davanti a un lettore che una stima di abbonati ce l'ha — *«è la ragione per cui è nella stanza»*. La chiusura non è inventare un numero: è una **tabella di sensibilità in cui il moltiplicatore lo mette chi legge**, dichiarata come illustrazione parametrica. Non è un numero senza fonte, e spetta alla `009`.

**Il porting su Tableau cade.** Era già *stretch, primo a cadere* dal 2026-08-08. Aggiunge uno strumento, non una risposta, e nessuna delle domande di business ne dipende.

#### Che cosa costa e che cosa compra

Costa ~17,5 ore in più e una dashboard costruita in nove ore che viene sostituita. Compra la sola cosa che a questo progetto mancava: un esito. Un repository da portfolio che documenta con questo scrupolo come si misura e non dice mai che cosa ha concluso non dimostra rigore — dimostra di non aver saputo finire, ed è la lettura che ne darebbe chiunque conosca il mestiere.

**Fonte verificabile**: [`specs/008b-dashboard-narrative-polish/review.md`](../specs/008b-dashboard-narrative-polish/review.md), §5; [`business_case.md`](business_case.md) §3; [`kpi_measures.md`](kpi_measures.md) §2.3, §4.1, §7.1.

### La scomposizione di `007` e `008` — decisione della regia, 2026-08-21

Erano 9 ore ciascuna, cioè sopra il limite che ne vieta l'apertura. La scomposizione era una condizione di apertura da tre aggiornamenti e non era mai stata fatta.

**`007` si taglia fra il metro e la misura, non fra un KPI e l'altro.** Il taglio per domanda di business — BQ1 da una parte, BQ2 e BQ3 dall'altra — sembra il più naturale e va scartato: `BQ1-K3` e `BQ2-K2` sono definiti sugli stessi tre assi di mood e condividono l'operatore che nessuno ha ancora scritto, quindi separarli obbligherebbe a decidere due volte la stessa cosa o a decidere una volta e ricordarsene dopo.

Ciò che `007` contiene davvero non sono otto formule: sono **sette decisioni analitiche ereditate e mai prese** — l'intervallo occupato, la metrica di distanza, i pesi e la loro commensurabilità, i quadranti contro la combinazione pesata, il segno della differenza, la precisione del confronto, il trattamento degli zeri. Da lì il taglio:

- **`007a` — Operatori delle misure** (~4 h). Definisce per intero, per ciascuno degli 8 KPI, l'operatore con cui verrà calcolato, **senza calcolare nulla**. Chiude in un solo luogo i rilievi `R5` e `R6` e le divergenze 2, 3, 4 e 8 della `001`, la divergenza 1 della `003` e la divergenza 4 della `002`. Deliverable: `docs/kpi_operators.md`. **Non dipende da alcun chore**: è lavoro di definizione e non tocca il motore;
- **`007b` — Misure DAX e documento dei KPI** (~5 h). Implementa gli 8 KPI contro quegli operatori e pubblica i valori. Dipende dalla materializzazione del modello e da `CF-1`. Deliverable: le misure nel `.pbix` e `docs/kpi_measures.md`.

**È la forma della `006`, applicata dove ha già pagato.** Il metro si scrive e si committa prima che qualunque valore esista, e per la stessa ragione: un operatore sbagliato non produce un valore sbagliato, li produce tutti. La differenza rispetto alla `006` è che qui il metro non ha bisogno di un modello che proponga — le decisioni sono di analisi, non di assegnazione — quindi non serve né la verifica indipendente né la quinta classe di fonte.

**`007a` diventa così l'unica voce apribile oggi**, mentre i chore sono ancora da fare. È il guadagno che questo taglio produce sul calendario: non toglie ore, ma toglie un'attesa.

**`008` si taglia dove la roadmap aveva già previsto**, struttura da una parte e narrazione dall'altra:

- **`008a` — Modello, pagine, misure a schermo** (~5 h): il `.pbix` con il modello caricato, le pagine, le misure esposte e la navigazione. Deliverable: un `.pbix` leggibile;
- **`008b` — Narrazione, limiti esposti, rifiniture** (~4 h): lo storytelling e — obbligo del template di spec che finora nessuna feature ha dovuto onorare — **i limiti dichiarati portati sullo schermo**, dove il lettore della dashboard li incontra invece di doverli cercare nei documenti.

**Sulla numerazione, che non è un dettaglio.** Le quattro feature tengono il suffisso letterale — `007a`, `007b`, `008a`, `008b` — e cartella e branch si chiamano come l'ID, `specs/007a-kpi-operators` e così via. L'alternativa era rinumerare in sequenza fino a `011`, e va scartata: `009` e `010` sono citate da documenti già mergiati e da tre tabelle di debito, e rinumerarle romperebbe riferimenti veri per guadagnare una sequenza pulita che nessuno sta chiedendo. Lo scostamento 1 vincola cartella, branch e ID a coincidere, non a essere interi consecutivi — e il suffisso dice a chi legge da fuori che `007` è stata divisa, cosa che una sequenza continua nasconderebbe.

`008a` anticipa il `.pbix` leggibile di una feature intera. Non serve più alla pubblicazione di prova, che è caduta, ma riduce il rischio della `010`, che di quel file ha bisogno per esistere.

### Lavoro fuori dalle feature

| Chore | Ore | Entro |
|---|---|---|
| ~~Ambiente Power BI: VM Windows 11 x64 e installazione di Power BI Desktop~~ | — | ✅ fatto il 2026-08-18: VMware, Windows 11 x64, primo accesso a Power BI Desktop riuscito |
| ~~Materializzazione del modello dati in Power BI Desktop~~ | ~2 spese | ✅ **conclusa il 2026-08-22**, `R3` inclusa — vedi [il secondo tentativo](#la-materializzazione-secondo-tentativo--2026-08-22) |
| ~~Riscrittura del criterio di mood per `CF-1`, ed eventuale versione 2 della tabella~~ | ~2 | ✅ **fatta il 2026-08-21**, chore `criterio-mood-cf1`: criterio v2, `CF-1` e `CF-2` chiusi, **tabella alla versione 2** |
| ~~Debito testuale della 001: rilievi R9, R10, R12~~ | — | ⬜ **registrato come issue** il 2026-08-21, vedi [la decisione](#il-debito-testuale-della-001-diventa-una-issue--regia-2026-08-21) |
| ~~Debito testuale della 001: allineamento di §3 a R11~~ | ~0,2 | ⬜ **assegnato a `007b`** il 2026-08-21, come task della feature che pubblica il valore |
| Debito testuale della 002: divergenza 3, allineare §5 del documento di audit a citare D3 della 001 e A2/A3 del business case | ~0,5 | ⬜ **spostato a prima di `010`** il 2026-08-21, vedi [la sequenza](#la-sequenza-fino-a-007b--decisione-della-regia-2026-08-21) |
| Debito testuale della 002: portare `docs/data_audit.md` sotto la severità stretta, rimarcandone le quantità | ~1 | ⬜ **spostato a prima di `010`** il 2026-08-21, nella stessa sessione della riga sopra |
| ~~Emendamento della constitution: ammettere i benchmark pubblici di settore fra le fonti dati~~ | — | ✅ fatto il 2026-08-15, **v1.1.0** |
| ~~Emendamento della constitution: ammettere le assegnazioni dell'analista congelate in artefatto versionato~~ | — | ✅ fatto il 2026-08-20, **v1.2.0** — trovato dalla revisione della spec della `006`, vedi sotto |
| Debito testuale per l'ancoraggio: assunzione di trasferimento in §2 di `docs/business_case.md`, richiamo in §6, note datate sulle schede `BQ3-K1` e `BQ3-K2` | ~1 | ✅ chiuso dentro `004` il 2026-08-16, per sole aggiunte |
| ~~Pubblicazione di prova su workspace Power BI Service e cattura schermate~~ | — | ⬜ **dichiarata caduta il 2026-08-21**: l'atterraggio incrocia la scadenza del 26 agosto e la voce non ha più una finestra. Vedi sotto |

**La pubblicazione di prova entro il 18 agosto va decisa ora, non provata il 18.** Presuppone la VM costruita, Power BI Desktop installato e qualcosa da pubblicare: sono ~4 ore per una cattura di schermate su un file vuoto, in giorni in cui `004` e `005` valgono di più. Il deliverable dichiarato è un `.pbix` e Power BI Desktop è gratuito e senza scadenza — è il rischio già chiuso l'8 agosto. La raccomandazione è **lasciarla cadere e dichiararlo**, invece di scoprire il 18 che non è stata fatta.

> **Nota di correzione — 2026-08-17, regia.** La data è sbagliata e la raccomandazione che ne discendeva si ribalta.
>
> **La data.** Non c'è alcuna scadenza il 18 agosto. Non si tratta inoltre di un *trial*: è un **abbonamento Microsoft 365 che include Power BI Pro**. La fatturazione automatica è stata annullata il 2026-08-17 e l'abbonamento **scade da sé il 26 agosto**, senza rischio di rinnovo e senza disdetta anticipata: il Service resta quindi disponibile per tutto il periodo utile. **Fonte verificabile**: verifica di Valerio sul proprio portale di fatturazione, 2026-08-17.
>
> **La raccomandazione.** L'argomento contro era che al 18 agosto non esiste alcun `.pbix` e si pubblicherebbe un file vuoto. Regge per il 18 e cade per il 25: l'atterraggio stimato è il 23-24 e la `008` produce la dashboard prima, quindi entro la scadenza esiste qualcosa di vero da pubblicare. La voce **non si lascia cadere**: si sposta a valle della `008`, che è la sua unica precondizione reale.
>
> **Ciò che resta vero**: la voce continua a non toccare il deliverable dichiarato, che è il `.pbix`. Se la `008` slitta oltre il 26, cade — e cade senza costo, come l'8 agosto aveva già stabilito.
>
> **Quanto è stretta la finestra — aggiornamento del 2026-08-18.** L'atterraggio stimato è ora il **24-25 agosto** e l'abbonamento scade il **26**: fra la `008` e la scadenza restano uno o due giorni, e la voce è l'ultima della catena. Non va quindi pianificata come una coda ma come la **prima cosa da fare appena la `008` produce un `.pbix` leggibile**, anche prima che la feature sia chiusa. È un'ora, e l'unica finestra in cui esiste.
>
> **La finestra si è chiusa — aggiornamento del 2026-08-21, regia.** L'atterraggio stimato è ora il **26-27 agosto**, cioè il giorno della scadenza o quello dopo. La `008` è penultima nella catena e non produrrà un `.pbix` leggibile prima del 25 nella migliore delle ipotesi: la voce non ha più una finestra, ne ha un'eventualità.
>
> *Precisazione della sera del 2026-08-21*: la `007a` ha chiuso in metà stima e l'atterraggio è tornato al **25-26 agosto**, quindi la premessa di questa nota — l'atterraggio oltre la scadenza — non vale più. **La conclusione sì**: la voce dipende da `008a`, che resta due feature più avanti, e un `.pbix` leggibile prima del 25 continua a essere l'ipotesi migliore e non quella attesa. La voce resta caduta, ora per la catena delle dipendenze e non più per la data.
>
> **Va quindi dichiarata caduta ora, non il 26.** È la stessa raccomandazione dell'8 e del 18 agosto, e questa volta senza il difetto che l'aveva resa sbagliata la prima volta: allora poggiava su una data errata, oggi poggia sul residuo di ore confrontato con la capacità dichiarata. Cade **senza costo**, per la ragione già stabilita e mai contestata — il deliverable è un `.pbix`, Power BI Desktop è gratuito e senza scadenza, e il Service non serve a ciò che il progetto consegna.
>
> **Che cosa il progetto perde, detto per intero**: le schermate di un report pubblicato su un workspace, che sarebbero state materiale per la `010`. Non un deliverable, non una verifica, non un numero. **Resta aperta l'eccezione**: se la `008` produce un `.pbix` leggibile il 25 e restano ore quel giorno, l'ora si spende — ma come opportunità colta, non come voce di piano su cui qualcosa poggia.

**La materializzazione del modello — decisione della regia, 2026-08-18.** La `005` ha progettato il modello e non lo ha mai eseguito: nessuna direzione di filtro è stata provata, nessuna cardinalità messa alla prova da un motore. Il buco era noto e rinviato; la `005` chiude e va assegnato. **È un chore, non una feature**, per la stessa ragione del chore ambiente — caricare quattro CSV e tracciare cinque relazioni non risponde a BQ1, BQ2 o BQ3, e il principio V colloca l'interazione con la GUI fuori dall'automazione.

Ha però una **conseguenza analitica che un chore normalmente non ha**, e per questo porta un obbligo di riporto: se il motore contraddice il documento — una cardinalità che si rivela molti-a-molti, una direzione di filtro che non regge — quello non è un intoppo di configurazione, è un difetto di progettazione trovato dall'unica prova che la `005` non poteva eseguire. In quel caso **si chiude con una nota in loco su `docs/data_model.md`**, che è debito della `005`, e non ridisegnando il modello dentro il chore.

Va prima di `007b` perché è la sua precondizione: una misura DAX non si verifica contro un documento. Non produce un deliverable dichiarato — il `.pbix` resta della `008` — e il file che ne esce è materiale di lavoro finché quella feature non lo raccoglie.

**L'emendamento v1.2.0, e come è stato trovato.** La revisione della spec della `006` al primo punto di fermata ha mostrato che l'etichetta `Sintetico` **non copriva** la tabella di corrispondenza generi → mood. L'elenco delle fonti ammesse la definisce come «dati sintetici **generati da script versionati**», e `dim_category_mood` non è generata da alcuno script — né deve esserlo, perché la condizione che rende ammissibile l'intera `DA-1` è che nessuno script chiami mai il modello.

Il progetto aveva già un artefatto curato a mano e mai scritto da uno script, `data/benchmarks/bq3_tier_upgrade.json`, ma quello è ammesso perché la `v1.1.0` gli ha scritto un comma proprio: **la mano curata era ammessa solo quando la fonte è esterna.** Un'assegnazione dell'analista non lo è.

La v1.2.0 aggiunge quindi la quinta fonte con cinque condizioni, più severe di quelle dei benchmark e non più lasche, perché è l'ultimo ripiego e sotto non c'è nulla. **Bump MINOR**, come la `1.1.0`: la formulazione più comoda avrebbe permesso di rivendicare un chiarimento, e scegliere il bump basso per risparmiare è la scorciatoia che questi emendamenti esistono per non prendere.

Due cose vanno dette con precisione, perché la prima indebolisce l'argomento e ometterla sarebbe scorretto. **Il testo precedente non era ostile all'assegnazione dell'analista**: il comma sui benchmark la nominava già come ripiego ammesso — «il parametro torna a essere una scelta dell'analista e va dichiarato come tale, il che è ammesso». Non le poneva però alcuna condizione, e la nominava per il caso in cui alimenta una generazione, cioè dove uno script produce comunque il valore finale. Il caso in cui **il valore assegnato è esso stesso il dato pubblicato** non era regolato. E la seconda: la tabella era già promessa dalla **D1 della `001`** — «una tabella di corrispondenza curata e versionata» — quattordici giorni prima che qualcuno notasse che non era una fonte ammessa. L'emendamento regolarizza una promessa vecchia, non solo una feature che si apre.

Nessuno di questi è una feature e nessuno apre un branch numerato. Il principio VI della constitution richiede che ogni feature sia riconducibile a BQ1, BQ2 o BQ3: predisporre una macchina virtuale non risponde ad alcuna domanda di business. Trattarlo come feature significherebbe o violare il principio VI, o inventargli un aggancio narrativo che non ha. Resta lavoro necessario, tracciato qui e non in una spec.

Il requisito di ambiente va però documentato — il principio II chiede che chiunque cloni il repository possa rieseguire la pipeline, e da `007` in avanti la pipeline include uno strumento che su macOS non esiste. La sede è la sezione Setup del [README](../README.md), non una spec.

## Scostamenti dalla roadmap iniziale

La roadmap costruita a inizio progetto prevedeva 10 voci in 7-10 giornate lavorative. Sei modifiche, tutte con una ragione — la quinta è un errore, non una scelta:

1. **Numerazione allineata ai branch.** La roadmap iniziale numerava da 0, il repository da 001. Ogni riferimento incrociato era sfalsato di uno. Vince la numerazione dei branch, che è quella che compare nella history git.

2. **`002` ridimensionata da una giornata a mezza.** Il profiling è già stato eseguito in [`research.md`](../specs/001-business-case-kpi/research.md) della 001: nulli per campo, 89.741 identificativi distinti su 114.000 righe, campionamento bilanciato a 1.000 tracce per genere, massa di zeri in `popularity`. Quei numeri esistono però solo come prosa, senza uno script che li rigeneri — che è il rilievo R8 della revisione. La feature non riparte da zero: produce lo script mancante e completa ciò che manca.

3. **`006` (Content Taxonomy Bridge) non è più stretch.** Era marcata opzionale. Tre KPI su otto — `BQ1-K3`, `BQ2-K2`, `BQ2-K3` — sono definiti sul profilo di mood e non esistono senza la tabella di corrispondenza generi → mood. Toglierla non alleggerisce il progetto: ne amputa metà del framework. Se serve tagliare, si taglia `009`.

4. **Il debito della 001 è distribuito, non accantonato.** Vedi la sezione seguente.

5. **Le due componenti a LLM della roadmap iniziale sono state cancellate senza dichiararlo.** L'elenco originale prevedeva *Synthetic Business Metrics **(Agent 1)*** e *Content Taxonomy Bridge **(Agent 2)***. La ricalibrazione dell'8 agosto ne ha tenuto i contenuti e lasciato cadere entrambe le parentesi, senza registrare lo scostamento fra i quattro dichiarati qui sopra: nel repository non esisteva un'occorrenza di "agent" o "LLM" fino a questa revisione. È l'errore peggiore fra quelli commessi finora dalla regia, perché una decisione rimossa in silenzio non può nemmeno essere contestata. Per la 004 la cancellazione si conferma corretta nel merito, con le ragioni scritte sopra; per la 006 la decisione è riaperta ed è ora tracciata fra le Decisioni aperte.

6. **La revisione in contesto pulito diventa una prassi, non un'eccezione della 001.** Era registrata fra i rischi aperti come «nessuna verifica indipendente pianificata dopo la 001», con `007` come candidato. La 002 l'ha invece condotta sul proprio documento e ne ha ricavato quattro affermazioni errate che nessun controllo automatico aveva visto. Il costo è di circa mezz'ora più il tempo di chiusura dei rilievi, e va d'ora in poi messo **dentro** la stima di ogni feature che produce un artefatto di lettura — non fuori, come è successo qui.

## Debito della feature 001

La [revisione in contesto pulito](../specs/001-business-case-kpi/review.md) ha prodotto 13 rilievi e 11 divergenze da chiarire. Tre rilievi sono già chiusi (commit `862bdca`). I restanti non diventano una feature dedicata: ciascuno è assegnato alla feature che ha comunque bisogno di quella decisione per procedere. Una decisione presa fuori dal contesto che la richiede è una decisione presa male.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| R4 / div. 1 | definizione operativa di "segmento": genere della fonte o raggruppamento per mood | ✅ chiusa dalla `005`, §2: **un segmento è un genere dichiarato dalla fonte**, il valore di `track_genre`, e ne esistono 114. Il raggruppamento per mood è respinto perché renderebbe circolare `BQ2-K2`, che misura proprio l'affinità di mood. Nota di adozione su §4 del business case: l'espressione ambigua **non** è stata riscritta |
| R7 / div. 7 | granularità di `BQ2-K2` e riformulazione di §5.2 | ✅ chiusa dalla `005`: le nozioni di grana necessarie sono **tre** e non due — quella dell'ingresso, quella su cui si aggrega, quella del risultato — e §5.2 ne dichiarava una sola. Nota di correzione in loco sul business case |
| R8 | provenienza dei numeri sui dati citati nel business case | ✅ chiusa dalla `002`: `reports/data_profile.json` rigenera i valori citati |
| R11 | quali categorie video compongono `BQ1-K1` e se la selezione è una mappatura | ✅ chiusa dalla `002` sul piano osservativo: una sola categoria, nessuna mappatura. Resta la parte testuale, sotto |
| R5, R6 / div. 2, 3, 4 | operatori indefiniti: intervallo occupato, metrica di distanza, pesi e commensurabilità; quadranti contro combinazione pesata | ✅ chiusi dalla `007a`, decisioni `D1`-`D4` di [`docs/kpi_operators.md`](kpi_operators.md): prodotto cartesiano dei tre intervalli scalari; media delle distanze assolute per asse; normalizzazione per divisione e pesi 0,5/0,5 dichiarati; quadrante e punteggio pesato **entrambi**, con ruoli distinti |
| div. 6 | trattamento delle tracce a popolarità zero | ✅ chiusa dalla `003`, D1: incluse e marcate, mai eliminate. **L'obbligo che ne discendeva è ✅ scritto come operatore dalla `007a`, `D7`**, e resta da eseguire alla `007b`: ogni misura sulla popolarità pubblica accanto al proprio valore la quota di zeri del segmento, con un avvertimento testuale dove il segmento porta `is_high_zero_genre` |
| div. 8 | segno della differenza e titoli privi di durata | ✅ **parte dati** chiusa dalla `003`, D2: i 3 titoli privi di durata sono gli stessi 3 con classificazione fuori dominio, riparati per spostamento di campo e non imputati. Il **segno della differenza** di `BQ1-K2` è ✅ chiuso dalla `007a`, `D5`: `format_duration_gap` è musica meno video, e la misura pubblica i minuti **col proprio segno** — non il valore assoluto, non il solo verso |
| div. 9 | dimensione della base utenti | ✅ chiusa per decisione del 2026-08-10: `BQ3-K2` resta **euro per utente al mese e non è scalabile**. Nessuna base utenti viene quantificata. La 004 deve dichiararlo esplicitamente, come la divergenza richiedeva in alternativa |
| div. 10 | governance della tabella generi → mood | ✅ decisa dalla regia il 2026-08-19 insieme a `DA-1` ed **eseguita dalla `006`**: costruisce la sessione sul criterio scritto per primo, approva Valerio sulla revisione in contesto pulito, si contesta citando il criterio, e la tabella porta un **numero di versione** che ogni valore dipendente dichiara. Il contratto di versione vive in §5 di [`docs/content_taxonomy_bridge.md`](content_taxonomy_bridge.md) |
| div. 11 | posizione dell'alternativa "non entrare" | `010` |
| R13 | ambiguità minori sparse | ✅ **chiusa**: parte BQ3 dalla `004` — le disdette sono escluse, tasso lordo su base costante; parte `BQ1-K2` dalla `007a`, `D5`; parte `BQ2-K3` dalla `007a`, `D8` — la posizione 1 della graduatoria è il punteggio più alto, ordinamento decrescente |
| R9, R10, R12 | correzioni terminologiche sul testo del business case | ⬜ **issue aperta** il 2026-08-21: nessuna delle tre invalida un operatore o un valore, e il criterio della `007a` le colloca nel tracker invece che nel piano |
| div. 5 | soglie decisionali | ✅ chiusa dal commit `862bdca` (§3, condizioni C1-C3) |

### Nota su R11 — l'esito cambia il testo, non la North Star

Il rilievo chiedeva se la selezione delle categorie video che compongono `BQ1-K1` sia una mappatura interpretativa, nel qual caso la confidenza scenderebbe a media e la North Star andrebbe ridefinita.

Una ricognizione sulla fonte mostra che esiste **una sola categoria** a contenuto musicale dichiarato, `Music & Musicals`. Non c'è alcuna selezione da compiere fra più categorie, quindi non c'è mappatura e la **confidenza alta regge**: la North Star sopravvive.

Il rilievo si sposta però sul testo. §3 del business case descrive il contenuto misurato come "musical, documentari musicali, concerti, film sulla musica" — quattro tipologie — mentre la misura ne legge una sola etichetta. Concerti e documentari musicali sono catturati solo se la fonte li ha collocati lì, e il documento non può affermarlo. La descrizione va allineata a ciò che la misura fa davvero. Rientra nel debito testuale.

`002` ha formalizzato il tutto con lo script che rigenera il conteggio: il valore esce ora da un artefatto versionato, e il principio II è soddisfatto. La ricognizione è confermata — `Music & Musicals` è l'unica categoria, con 375 titoli distinti — quindi la confidenza alta di `BQ1-K1` regge e la North Star non va ridefinita. La correzione della descrizione di §3 resta debito testuale.

## Debito della feature 002

La [revisione in contesto pulito](../specs/002-data-audit-profiling/review.md) del documento di audit ha prodotto 11 rilievi e 8 divergenze. **I rilievi sono tutti chiusi dentro la 002**, prima del merge: quattro affermazioni errate corrette, e il controllo di coerenza esteso ai numerali scritti in lettere e ai letterali, perché era lì che gli errori erano passati. Restano le divergenze, che sono decisioni e non difetti.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| div. 1 | che cosa il vincolo di tracciabilità debba coprire: ancorare tutto, estendere ancora il controllo, o dichiararne il confine | ✅ chiusa dalla `003`, D5: copre valori numerici, letterali di elenchi e convenzioni versionate, e affermazioni derivate; non copre le affermazioni qualitative prive di contenuto numerico |
| div. 2 | statuto delle **affermazioni derivate** — confronti, graduatorie, rapporti costruiti sui valori. Sono la categoria in cui si concentrano gli errori: vanno calcolate nel profilo o vietate in prosa | ✅ chiusa dalla `003`, D5: entrambe le cose, che sono le due facce della stessa regola. Ora in [`CLAUDE.md`](../CLAUDE.md#le-affermazioni-derivate-sono-esse-stesse-valori) |
| div. 6 | quale delle due letture di «sovrastima di circa un quinto» adottare, prima che si calcoli un totale di catalogo | ✅ chiusa dalla `003`, D3: si adotta `SP.id.inflation`, l'eccesso del totale non deduplicato su quello corretto, perché una sovrastima si misura rispetto al valore giusto. **Sul dato trasformato vale 26,53%**, non più 27,03%: è il valore da citare. Ogni totale di catalogo musicale si calcola sulla grana traccia |
| div. 8 | criterio con cui si seleziona l'insieme dei generi a forte concentrazione di zeri: `country` al 58,70% cade dentro o fuori a seconda di una soglia che nessuno ha ancora fissato | ✅ chiusa dalla `003`, D4: soglia al 50%, `country` cade **dentro**. 7 generi marcati su 114 |
| div. 5 | riverifica del criterio delle categorie musicali se la fonte cambia, e chi se ne accorge | ✅ chiusa dalla `006`, §4: **se ne accorge un controllo che ferma**. `scripts/check_audit_coherence.py` confronta come insiemi le categorie della tabella dei mood e quelle del catalogo video, e su una differenza simmetrica non vuota **fallisce** invece di avvisare. Provato dalla Prova 7 del quickstart. Resta dichiarato ciò che il presidio non fa: non esiste alcun hook di pre-commit né integrazione continua, quindi dipende da chi lancia il controllo |
| div. 4 | se pubblicare numeratore e denominatore accanto alla frase sulla North Star equivalga a pubblicare la misura | ✅ chiusa dalla `007a`, `D9.3`: **no**. La giustapposizione di due valori già ancorati non è la misura; il rapporto è a sua volta un'affermazione derivata e nasce quando `007b` lo calcola e gli dà un'ancora propria |
| div. 3 | `docs/data_audit.md` §5 contiene due decisioni di modellazione — esclusione delle serie da `BQ1-K2`, ricorso a dati simulati per BQ3 — che sono prese altrove (D3 della 001, A2/A3 del business case) e vanno citate, non riformulate | debito testuale, ~0,5 ore |
| div. 7 | prassi di correzione degli artefatti già mergiati: nota in loco o errata separata | ✅ chiusa il 2026-08-10: regola scritta in [`CLAUDE.md`](../CLAUDE.md#correzione-degli-artefatti-già-mergiati) — nota in loco, valore originale mai cancellato, e la scelta dichiarata come tale invece che come constatazione |

### Nota sulla misura del tempo speso

La 002 è costata **~4,5 ore contro le 4 stimate**, distribuite su due sessioni e due giorni di calendario. Lo scostamento è quasi tutto imputabile alla revisione in contesto pulito, che non era nella stima: la roadmap la dava per non pianificata dopo la 001.

Va però registrato un limite di questa misura, perché tocca ogni stima futura. I timestamp git della 002 misurano il tempo di una sessione di agent, non ore-uomo: fra il commit dei task e quello dell'implementazione passano 45 minuti per un lavoro che a mano ne varrebbe molti di più. **Le stime in ore restano stime di sforzo umano** — è ciò che il principio III vincola — ma il metro dei timestamp non le verifica più direttamente. Da qui in avanti lo scostamento va letto come indicativo, non come misura.

## Debito della feature 003

La [revisione in contesto pulito](../specs/003-data-cleaning-etl/review.md) del documento di cleaning ha prodotto 13 rilievi e 8 divergenze. **I rilievi sono tutti chiusi dentro la 003**, prima del merge, come nella 002. Sei divergenze su otto sono chiuse. Restano queste.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| div. 1 | **a quale precisione si confrontano profilo e rendiconto.** Il profilo memorizza a una cifra decimale ciò che il rendiconto memorizza a quattro; il criterio stretto conta perciò 78 generi «cambiati» dove quelli mossi di oltre mezzo punto sono 3 | ✅ chiusa dalla `007a`, `D6`: soglia a **0,5 punti percentuali** in senso stretto, limitata al confronto delle quote di zeri per genere e non estesa ad altre coppie di valori |
| div. 5 | **se gli artefatti versionati possano contenere attributi di record individuali**, o solo aggregati e identificativi. Il caso concreto è chiuso — i nomi dei tre titoli riparati sono registrati — ma la regola generale no | ⬜ **decisa per la `006` e non in generale**, vedi sotto |
| severità stretta | il corollario (c) di D5 vale per `docs/data_cleaning.md` e **non è retroattivo** su `docs/data_audit.md`, che resta sotto il regime ad avvisi | debito testuale, ~1 ora, ⬜ **spostato a prima di `010`** il 2026-08-21 |
| regola D5 in `CLAUDE.md` | portare le affermazioni derivate dal perimetro della feature al metodo del progetto, con le due precisazioni del rilievo R7 | ✅ chiusa dalla regia il 2026-08-15 |

**Sulla divergenza 1, ciò che la feature ha già escluso.** Non c'è un difetto di precisione nel profilo della 002, e questo restringe la decisione. Nel catalogo di origine ogni genere ha esattamente 1.000 righe, quindi la quota di zeri per genere ha una sola cifra decimale **per costruzione**: il profilo la registra esatta. Dopo la deduplicazione i generi non hanno più 1.000 righe e servono quattro cifre. Ciò che resta da decidere è solo se il criterio pubblicato debba essere quello stretto o quello alla precisione minore fra le due, e la risposta cambia due numeri di `docs/data_cleaning.md` §5 e la dimensione del blocco `denominators`. Non è urgente perché il documento pubblica ora i due valori che misurano quanta parte del divario sia apparente — 60 generi tornano identici, 3 si spostano di oltre mezzo punto — quindi nessun lettore è indotto in errore. Va però decisa prima che `007b` citi un denominatore in un artefatto pubblicato, ed è quindi materia di `007a`.

**Sulla divergenza 5, ciò che la `006` ha deciso e ciò che resta aperto.** La feature ha stabilito che **nessuno dei propri artefatti cita un titolo del catalogo** — né nome, né trama, né cast — e lo ha provato con un controllo eseguibile. È la parte generale della divergenza per il perimetro di una feature, non per il progetto.

La regola generale resta aperta, e ora ha **due precedenti che vanno in direzioni opposte**: la `003` registra i nomi dei tre titoli riparati, la `006` vieta di nominarne alcuno. La divergenza fra i due non è un'incoerenza ed è ciò che rende la regola scrivibile: nella `003` il titolo è **l'oggetto di una riparazione da verificare**, e senza il nome nessuno può controllare che la riparazione sia giusta; nella `006` il titolo sarebbe **la prova a sostegno di un giudizio**, e citarlo indurrebbe a leggere un'assegnazione come un'osservazione. Il discrimine è quindi la funzione dell'attributo nell'artefatto, non la sua natura. Scriverlo come regola di progetto è atto di governance e spetta alla regia; non è urgente, perché nessuna feature rimasta produce artefatti a grana record.

**Sulla severità stretta, la decisione della regia.** Non si estende retroattivamente per automatismo, e non resta nemmeno com'è. Il documento della 002 va rimarcato, ma come debito testuale dichiarato e non come lavoro che una feature successiva assorbe di nascosto. La ragione per farlo, contro l'ipotesi di lasciarlo sotto avvisi per sempre: il senso del corollario (c) è che **un controllo che elenca non ferma nessuno**, e decine di avvisi permanenti su un documento pubblicato addestrano chi legge — e chi scrive — a ignorare l'output. La ragione per non farlo ora: `docs/data_audit.md` è già aperto dalla divergenza 3, e le due cose costano meno insieme. Non è una correzione di valori e non tocca quindi la prassi delle note in loco: si aggiungono marcatori, non si riscrive nulla.

## Debito della feature 004

La revisione in contesto pulito del documento degli scenari ha prodotto **14 rilievi**, tutti chiusi dentro la feature prima del merge, come nella 002 e nella 003. Due hanno richiesto decisioni di Valerio perché toccavano scelte già prese: la rimozione di una divergenza e il cambio dei fattori della banda. Resta questo.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| verificabilità del benchmark | il valore è ancorato a un **comunicato stampa** e a nient'altro: nessuna copia archiviata, nessun identificativo permanente, e il comunicato non nomina lo studio né la numerosità campionaria. Se quell'indirizzo smettesse di rispondere, la verifica esterna verrebbe meno e resterebbe solo il valore congelato nel repository | ⬜ aperta — vedi sotto |
| fonte più vicina non citabile | il valore Antenna sui piani in bundle è strutturalmente più vicino al caso di StreamWave ed è del 2026, ma è dietro registrazione e senza data di pubblicazione dichiarata. Se diventasse citabile, la sostituzione va valutata con nota in loco | ⬜ prima di `008a` |
| limite strutturale della banda | nessuna banda moltiplicativa può rappresentare il caso in cui **il trasferimento fallisce**: lo scenario pessimista resta proporzionale al benchmark e non raggiunge lo zero. È dichiarato nel documento e non è correggibile dentro questa forma | ⬜ dichiarato, non chiudibile qui |
| `value` come stringa | l'artefatto della 004 scrive `value` come stringa decimale, dove i due esistenti scrivono un numero JSON. È deliberato — `0,60` e `1,80` non sono esatti in virgola mobile — ma la `007` deve saperlo, ed è nel contratto | `007b`, in lettura |
| sigle con suffisso letterale | `FR-011a` e simili non rientrano nell'esclusione strutturale del controllo di marcatura, che si chiude su un confine di parola dopo le cifre. Si scrivono fra apici inversi; registrato in `docs/convenzioni-marcatura.md` | ✅ chiusa per convenzione |

**Sulla verificabilità del benchmark, che è il debito che conta.** È il punto su cui l'intera terza domanda di business poggia, ed è più fragile di quanto la presenza di una citazione faccia sembrare. Il documento lo dichiara in §9 invece di lasciarlo dedurre, ma dichiararlo non lo chiude. Le strade sono due e nessuna è dentro il perimetro di questa feature: archiviare una copia del comunicato nel repository, che pone una questione di licenza, oppure trovare una fonte primaria che pubblichi la stessa grandezza con metodo ispezionabile — cosa che la ricognizione non ha trovato. **Va deciso prima che `008a` pubblichi quei numeri in una dashboard**, perché è lì che smettono di essere un artefatto tecnico e diventano un'affermazione rivolta a un lettore.

## Debito della feature 005

La [revisione in contesto pulito](../specs/005-data-model-design/review.md) del documento del modello ha prodotto **22 rilievi e 6 divergenze**, il bilancio più pesante del progetto. Tutti chiusi dentro la feature prima del merge, con tre rilievi respinti in tutto o in parte e uno rinviato. Resta questo.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| **materializzazione del modello** | il modello è progettato e mai eseguito: nessuna cardinalità è stata messa alla prova da un motore | ⬜ chore di ~2 ore prima di `007b`, vedi [Lavoro fuori dalle feature](#lavoro-fuori-dalle-feature). Se il motore contraddice il documento, si chiude con nota in loco |
| conteggio dei segmenti letto dal profilo di origine | i 114 segmenti sono ancorati al profilo dei dati **di origine**, e la loro validità sul dato trasformato è argomentata per invariante invece che ricontata | ✅ **decisa dalla regia il 2026-08-18: non si riconta**, vedi sotto |
| graduatoria di `BQ2-K3` a 114 voci | vincolo di presentazione, non di calcolo: una graduatoria di 114 elementi non si legge a colpo d'occhio | `008a`, già registrato in §19 del documento e nella nota sul business case |
| campione musicale non più bilanciato | il catalogo di origine aveva 1.000 righe per segmento; dopo la trasformazione esistono 17 conteggi distinti, il minore a 904. Il rendiconto **non pubblica** il massimo né alcuna misura di dispersione | ⬜ dichiarato, non chiudibile qui — vale per `007a` |

**Sul conteggio dei segmenti, la decisione e la sua ragione.** L'alternativa esisteva: ricontare i 114 segmenti sul dato trasformato e ancorarli lì eliminerebbe l'intera §3.4, cioè un'intera sezione di argomento sostituita da un numero. Costa però rieseguire la pipeline — che richiede `data/raw/`, quindi il download da Kaggle — e aggiungere un'ancora a `reports/cleaning_report.json`, cioè riaprire la `003`. **Non si fa**, per due ragioni: l'invariante è scritto per esteso e verificabile da chi legge, e riaprire una feature mergiata per sostituire un argomento corretto con un numero equivalente è costo senza guadagno. La decisione si riapre solo se `007` ha bisogno di quel conteggio ancorato sul dato trasformato per una misura pubblicata — nel qual caso il costo è già dentro il perimetro di `007b`.

**Sul campione non più bilanciato, ciò che il documento ha fatto bene.** Ha dichiarato il fatto e si è fermato lì, senza dire se lo scostamento sia grande o piccolo, perché nessun artefatto pubblica la dispersione e affermarlo sarebbe stato un numero senza fonte. È l'applicazione corretta della regola sulle affermazioni derivate, in un punto in cui la tentazione di rassicurare il lettore era alta. Chi in `007b` costruirà una misura per segmento eredita il fatto, non una valutazione.

## Debito della feature 006

La [revisione in contesto pulito](../specs/006-content-taxonomy-bridge/review.md) del documento del ponte ha prodotto **16 rilievi**, 5 dichiarati bloccanti, tutti chiusi dentro la feature prima del merge. Il debito che resta non viene però dalla revisione: viene dalla **verifica indipendente della proposta**, che ha trovato tre difetti del criterio contro cui verificava.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| **`CF-1` — il criterio si contraddice** | criterio §2 impone alle etichette generiche, geografiche e linguistiche di restare centrali su tutti gli assi; criterio §5 attribuisce a ogni formato episodico a durata fissa una cadenza più alta. Cinque etichette cadono sotto entrambe le regole | ✅ **chiuso il 2026-08-21** dal chore `criterio-mood-cf1`: criterio v2, nota in loco a §2 e §5, **prevale il tipo che porta segnale**. Le cinque celle salgono da 0,50 a 0,55 sull'asse del ritmo, tabella alla **versione 2** |
| frase ritirata dal documento e conservata dal criterio | criterio §7 dice «questo è l'unico strato interpretativo del progetto», che è l'affermazione che il rilievo `R4.1` ha fatto ritirare da §0 del documento pubblicato | ⬜ **non chiusa** dal chore, che pure doveva prenderla: la frase è ancora in §7 del criterio. Passa al debito testuale, ~0,2 h |
| `CF-2` — nessuna regola per le etichette di pubblico | il criterio non dice come si assegna a `Children & Family Movies` e `Kids' TV`, che ricevono positività molto alta per due vie diverse | ✅ **chiuso il 2026-08-21**, e più largamente di come era registrato: i tipi di §2 non sono esaustivi, e la nota ne aggiunge tre — pubblico, epoca o ricezione, modo di produzione o tema — con la regola di default (centrali per assenza di segnale) e le due eccezioni |
| `CF-3` — griglia implicita a 19 livelli | tutti i 126 valori della proposta sono multipli di 0,05, granularità che il criterio non chiede e non vieta | ⬜ dichiarato, non necessariamente correggibile |
| il criterio è scritto da chi pubblica la tabella | un metro scritto da chi verrà misurato; contestabile e in un file, ma non indipendente | ⬜ dichiarato in §7, non chiudibile dentro il progetto |
| nessuna verifica del merito | che i profili siano *quelli giusti* non è stato testato: servirebbe un secondo giudice indipendente dal criterio, che questo progetto non ha | ⬜ dichiarato, non chiudibile qui |

**Perché `CF-1` va prima di `007b` e non dopo.** Non è una questione di pulizia. Le cinque etichette in conflitto — `TV Shows`, `International TV Shows`, `British TV Shows`, `Korean TV Shows`, `Spanish-Language TV Shows` — hanno un profilo di mood come tutte le altre, e `BQ1-K3`, `BQ2-K2` e `BQ2-K3` lo consumano. Correggere il criterio comporta una **versione 2 della tabella**, e §5 del documento stabilisce che una revisione della tabella **invalida i valori pubblicati che ne dipendono**. Farlo dopo `007b` significherebbe quindi ricalcolare e ripubblicare tre KPI su otto; farlo prima costa una riscrittura del criterio e una riverifica delle celle interessate. È il contratto di versione che funziona come previsto: rende visibile in anticipo un costo che altrimenti si sarebbe scoperto a valle.

**Che cosa la riscrittura non deve fare.** Il criterio è l'artefatto la cui prova sta nell'essere stato committato prima di qualunque valore. Una versione 2 non lo cancella e non lo sovrascrive: la correzione è **in loco**, dichiara la contraddizione trovata, quale delle due regole prevale e perché, e la data. La cronologia `git` deve continuare a mostrare che la versione 1 del criterio precede la versione 1 della tabella — altrimenti si perde il solo presidio che `DA-1` aveva.

**Un ritrovamento di igiene del repository, registrato perché non venga «riparato» dopo.** [`data/curated/dim_category_mood_proposal.json`](../data/curated/dim_category_mood_proposal.json) contiene, dentro il testo del prompt, il percorso assoluto locale della macchina di sviluppo — compare nell'istruzione che vietava al modello di aprire il repository. **Resta come è**, per tre ragioni cumulative: il campo `prompt` è il registro di ciò che è stato realmente inviato, e riscriverlo lo renderebbe una trascrizione ritoccata di un passaggio non riproducibile; il file è sigillato da `source.proposal_sha256` dentro la tabella congelata, quindi qualunque modifica — anche l'aggiunta di una nota — romperebbe l'impronta o costringerebbe a dichiararne una che non è quella del file verificato; e la sostituzione non otterrebbe comunque il proprio scopo, perché la stessa stringa compare in [`specs/005-data-model-design/review.md`](../specs/005-data-model-design/review.md) §1, dove il revisore àncora il file che ha letto, ed **è testo di un verbale, che per prassi non si corregge**. Rimuoverla da un file sigillato per lasciarla in uno intoccabile è costo senza guadagno.

### La ricognizione su `CF-1` — regia, 2026-08-21

Prima di consegnare il chore la regia ha aperto la tabella congelata, e **`CF-1` non ha la forma in cui era stato registrato**. Va detto qui perché cambia che cosa il chore deve produrre, e perché la forma registrata rendeva più cara la voce di quanto sia.

**Come si comportano i valori.** Il secondo segnale di §5 — il formato episodico ha cadenza più alta di quello a durata libera — è applicato dalla proposta su **otto coppie film/serie**: `Dramas` 0,30 contro `TV Dramas` 0,45, `Documentaries` 0,05 contro `Docuseries` 0,20, `Horror Movies` 0,20 contro `TV Horror` 0,35, e altre cinque. Non è applicato su **tre** coppie, e sono le tre in cui il termine film sta già al centro: `Anime Features`, `Movies`, `International Movies`. La verifica indipendente ne ha corrette due — `Anime Series` e `Classic & Cult TV`, le sole due celle che ha mosso — motivando che §2 non copre quelle etichette e che §5 si applica quindi senza conflitto.

**Nessun artefatto contiene una regola di precedenza, ed è questo il punto.** Le cinque etichette in conflitto stanno a 0,50 perché è il valore della proposta, e perché la verifica **si è astenuta deliberatamente**: sceglierne una delle due regole sarebbe stato decidere sul criterio invece che verificare contro il criterio, ed è registrato sopra come esito, non come dimenticanza. La risoluzione economica — dichiarare che §2 prevale, e non muovere nulla — non è quindi «ratificare una regola già applicata»: è **eleggere a regola l'esito di un'astensione**, che è la cosa che la condizione 1 della quinta fonte vieta di fare guardando i valori. Il chore deve perciò decidere la precedenza **senza vedere la tabella**, e confrontare solo dopo. Se l'esito coincide con i valori, la tabella resta alla versione 1 — §5 del documento del ponte incrementa la versione «quando una riga viene corretta», e nessuna lo sarebbe. Se non coincide, si va alla versione 2 e `007b` la dichiara.

**Il difetto di §2 è più largo di `CF-1` e contiene anche `CF-2`.** §2 enumera tre tipi di etichetta — generica, geografica o linguistica, di formato — e li tratta come esclusivi ed esaustivi. Il catalogo ne ha almeno altri tre che nessuna delle tre voci copre: **di pubblico** (`Kids' TV`, `Children & Family Movies`, `Teen TV Shows`), **di epoca o di ricezione** (`Classic Movies`, `Cult Movies`, `Classic & Cult TV`), **di modo di produzione o di tema** (`Independent Movies`, `LGBTQ Movies`). E `Korean TV Shows` mostra che i tipi non sono nemmeno esclusivi: è insieme geografica e di formato. Riscrivere §2 per il solo caso composto lascerebbe in piedi la metà del difetto.

**Un ritrovamento puntuale, dalla stessa ricognizione.** `Teen TV Shows` sta a 0,50 su tutti e tre gli assi. È episodica a durata fissa e non è generica, geografica né linguistica: è **esattamente il caso** in cui la verifica ha mosso `Anime Series` e `Classic & Cult TV`, con la motivazione che ha scritto due volte. Applicando quella stessa motivazione, la cella andava mossa e non lo è stata. È un errore di copertura della verifica, non una decisione — e se il chore lo chiude, `MOOD.review.changes_count` passa da 2 a 3 e la frase che lo commenta in §3 del documento del ponte va rivista con esso.

**Esito, la sera del 2026-08-21.** Il chore ha eseguito i quattro passi. Il subagent isolato ha ricevuto il solo criterio e ha risposto che i tre tipi di §2 non sono né esaustivi né esclusivi; la regola scritta in nota è che **fra un tipo che porta segnale e uno che non ne porta prevale il primo**, perché l'assenza di segnale non ha nulla da opporre a un segnale reale. Le cinque celle di `CF-1` si muovono quindi da 0,50 a 0,55 sull'asse del ritmo, `Teen TV Shows` con esse ma per causa diversa — e il `changelog` della tabella lo tiene fuori dall'elenco di `CF-1` dichiarando perché. La tabella è alla **versione 2**, `MOOD.review.changes_count` a 3, e una seconda verifica isolata ha controllato le sei celle contro il criterio v2 confermandone la direzione e dichiarando che **il criterio autorizza la direzione, non la cifra**: 0,55 resta un'assegnazione dell'analista dentro il verso consentito.

**La previsione della ricognizione era sbagliata sul merito, e va detto.** Avevo scritto che la risoluzione economica — §2 prevale, nulla si muove — era la trappola da cui guardarsi. La decisione presa al buio è andata nella direzione opposta, e sei celle si sono mosse. La cautela procedurale era giusta e l'esito che temeva non si è verificato: è il caso in cui un presidio funziona e non si vede, ed è l'unica forma in cui si possa osservarlo.

### Il debito testuale della 001 diventa una issue — regia, 2026-08-21

Le tre voci non hanno lo stesso statuto, e trattarle insieme era un raggruppamento per origine — vengono dalla stessa revisione — non per natura.

**R9, R10 e R12 vanno nel tracker.** Sono correzioni terminologiche su `docs/business_case.md`: la North Star chiamata «criterio di successo» quando è un criterio di screening; l'esclusione di `BQ3-K2` argomentata anche su una convenzione di presentazione; §7 intitolato «Impatto economico stimato» dove ospita un ricavo lordo. Nessuna invalida un operatore, un valore o una decisione a valle, ed è esattamente il criterio che la `007a` ha stabilito per le issue [`#7`](https://github.com/Valvln/streamwave-bi/issues/7) e [`#8`](https://github.com/Valvln/streamwave-bi/issues/8).

**L'allineamento di §3 a R11 no, e va detto perché.** §3 descrive il contenuto misurato dalla North Star come «musical, documentari musicali, concerti, film sulla musica» — quattro tipologie — mentre la misura legge una sola etichetta. Finché il numero non è pubblicato la descrizione è imprecisa; **nel momento in cui `007b` lo pubblica diventa falsa**, perché il lettore attribuisce al valore un perimetro che il valore non ha. Non è un rilievo che non invalida il deliverable: è un rilievo che il deliverable renderà attivo.

**Va quindi alla `007b` come task**, non come gate esterno né come issue. È la regola che il debito della `001` applica dall'inizio — ogni voce è assegnata alla feature che ha comunque bisogno di quella decisione per procedere — e `007b` è la sola feature che ha in mano insieme il numero e la frase che lo descrive. Costa ~0,2 h dentro una stima da 5.

**Il percorso critico prima di `007b` scende così a `R3`**, e nient'altro — chiusa il 2026-08-22, quindi a nulla.

### I rilievi si rinviano al tracker — decisione del 2026-08-22

Da qui in avanti una feature chiude **solo i rilievi strettamente necessari** delle proprie revisioni e registra gli altri come issue. La regola, il criterio di necessità e l'obbligo di dichiarare ogni rinvio nel blocco di chiusura stanno in [`CLAUDE.md`](../CLAUDE.md#la-revisione-in-contesto-pulito), che è la sede del metodo; qui restano le conseguenze sul piano.

**Le stime non scendono adesso.** La voce di revisione e chiusura resta a ~2 ore per feature. Un solo caso l'ha messa alla prova — la `007a`, chiusa in ~2 ore contro 4 rinviando due rilievi — e ridurre una stima su un punto è ciò che questa roadmap ha già sbagliato una volta con la regola legata alla lunghezza dei documenti. Il guadagno si osserverà come scostamento sotto stima su `007b` e `008a`; se si ripete, allora si riscrive la voce.

**Il rischio va nominato, perché è il rovescio esatto del guadagno.** Un arretrato di issue che nessuna feature raccoglie diventa un elenco di difetti dichiarati e mai chiusi, che su un repository da portfolio è peggio di non averli trovati. Il presidio è la `010`, che legge il repository per intero da fuori: **l'arretrato del tracker si svuota lì**, o si dichiara nel case study come debito residuo con la ragione per cui resta aperto. Non esiste una terza uscita.

### La materializzazione, secondo tentativo — 2026-08-22

Riuscita. Il modello è caricato e `R3` si traccia uno a uno, con la derivazione da lungo a largo di §13.

**Un passaggio in più che la regola non diceva.** Per far collassare il pivot a 42<!--@MOOD.coverage.rows--> righe è stato necessario **eliminare la colonna `Name`**: il blocco `values` dell'artefatto è un oggetto indicizzato per identificativo di ancoraggio, quindi ogni voce arriva al modello portando con sé un valore unico, e un valore unico per riga impedisce a qualunque rotazione di aggregare. Non è un'impostazione della GUI: è una conseguenza della forma del file, e chiunque lo carichi con qualunque strumento la incontra.

**La regola di §13 è quindi incompleta**, non sbagliata: dice quali voci tenere e come ruotarle, non dice che l'identificativo che le indicizza va scartato. Va aggiunto, ed è una riga.

**Va anche detto che la modifica agli artefatti serviva comunque.** L'ipotesi che il solo scarto di `Name` avrebbe risolto senza toccare i documenti non regge: senza la rotazione restano 126<!--#--> righe con `category` ripetuta tre<!--#--> volte per categoria, e `R3` fallisce come prima. Lo scarto di `Name` è un passo **in aggiunta** al pivot, non un'alternativa.

**Chi lo chiude**: la `007b`, come task, insieme al resto del suo drift. Aprire un chore per una riga sarebbe più caro della riga.

### La materializzazione — esito del 2026-08-21

Il modello è stato caricato in Power BI Desktop. Tutto ha retto tranne **`R3`**, `dim_category[category]` → `dim_category_mood[category]`, che il motore rifiuta di tracciare uno a uno: «la colonna selezionata non può essere la colonna chiave perché contiene valori duplicati».

**Il motore non ha contraddetto il documento.** È la prima cosa da stabilire, perché l'obbligo di riporto del chore fa scattare una nota in loco su `docs/data_model.md` solo in quel caso. Sui dati le due colonne hanno **42 valori distinti ciascuna e differenza simmetrica vuota** — è la stessa verifica che `scripts/check_audit_coherence.py` esegue a ogni giro e che continua a passare. `R3` uno a uno, come `data_model.md` §6 la progetta, è quindi corretta: nessuna delle due colonne contiene duplicati **nella forma che il documento prescrive**.

**Il duplicato viene da come una delle due tabelle è arrivata nel modello**, e i candidati sono due:

- `dim_category` caricata dal ponte senza la derivazione di §13 — «i valori distinti di `category` nel ponte» — che senza il passo di deduplicazione porta **19.323 righe** invece di 42;
- `dim_category_mood` caricata dal blocco `values` del JSON, che **non è una tabella a 42 righe**: è un elenco lungo di 129 voci, 126 delle quali sono una coppia categoria-asse e 3 non hanno categoria affatto. Letto così, `category` compare tre volte per categoria.

**Il secondo caso è il più probabile, e sotto di esso c'è un vuoto vero.** Nessun documento dice come si passa dal JSON congelato alla tabella che il modello si aspetta. §10 di `data_model.md` dichiara le colonne e la chiave di `dim_category_mood`; §13 elenca tre derivazioni interne al modello e **questa non c'è**; la `006` ha consegnato un artefatto sagomato per essere ancorato, non per essere caricato. È esattamente la classe di ritrovamento per cui il chore esisteva — una cosa che nessun documento poteva scoprire — e non è un difetto di progettazione: è un passaggio mancante fra due artefatti che nessuno dei due possiede.

**Che cosa non si fa stasera.** Non si apre una nota in loco su `docs/data_model.md`: sarebbe la correzione di un'affermazione errata, e l'affermazione non è errata. La decisione — se il passaggio da lungo a largo sia una quarta derivazione di §13, e quindi debito della `005`, oppure una forma di consegna che spetta alla `006` — si prende domani, insieme all'ispezione delle due tabelle nel modello che dice quale dei due candidati sia il caso reale. Fino ad allora resta **~0,5 h** aperte sul chore.

### La sequenza fino a `007b` — decisione della regia, 2026-08-21

Restano tre voci prima di `007b`, per ~5 ore, di cui ~2 fuori dal percorso critico:

1. ~~**la riscrittura del criterio per `CF-1`** (~2 h), sessione esecutiva~~ — ✅ fatta la sera stessa;
2. ~~**la materializzazione del modello** (~2 h), lavoro alla GUI nella VM, **in parallelo** alla precedente~~ — 🟡 fatta la sera stessa in ~1,5 h, **tranne `R3`**;
3. ~~**il debito testuale della 001** (~1 h) — R9, R10, R12 e l'allineamento di §3 a R11~~ — ⬜ **sciolto il 2026-08-21**: R9, R10 e R12 diventano una issue, l'allineamento di §3 diventa un task della `007b`.

> **Esito della sera del 2026-08-21.** Le due voci sono state eseguite in parallelo come previsto e il parallelismo ha retto: la versione 2 della tabella non ha toccato chiavi né numero di righe, e nessuno dei due lavori ha atteso l'altro. Restano **~1,5 ore** prima di `007b` — la chiusura di `R3` e il debito testuale della `001` — più le due voci di debito che il chore non ha chiuso: la frase di §7 del criterio e la decisione su dove collocare il passaggio da JSON lungo a tabella larga. *Aggiornamento del 2026-08-22: entrambe chiuse, e il debito testuale della `001` è stato sciolto fra tracker e `007b`. Prima di `007b` non resta nulla.*

**Perché 1 e 2 sono davvero parallele.** Una versione 2 della tabella cambierebbe valori di mood, non chiavi né numero di righe: le 42 categorie restano quelle, `R3` resta uno a uno, e il modello caricato non va rifatto ma aggiornato. L'unica ipotesi che romperebbe il parallelismo è che la riscrittura decida di **togliere righe** — escludere le etichette generiche invece di assegnarle — e in quel caso la materializzazione va ricaricata sulla struttura, non aggiornata. È l'unica cosa che chi materializza deve sapere del chore che gira accanto.

**Perché il debito testuale della 001 resta prima di `007b` e quello della 002 no.** `007b` pubblica il valore della North Star, e §3 del business case ne descrive ancora il contenuto misurato come «musical, documentari musicali, concerti, film sulla musica» — quattro tipologie dove la misura legge una sola etichetta. Pubblicare il numero sotto quella descrizione significa pubblicare un numero e una definizione che non corrispondono: è il gate. Le due voci della 002 — la divergenza 3 e la severità stretta su `docs/data_audit.md` — **non toccano nulla che `007b` calcoli o citi**, e stavano prima di `007b` per ordine di scoperta, non per dipendenza.

**Si spostano quindi a prima della `010`**, che è la feature in cui il repository viene letto per intero da fuori, ed è il momento in cui la severità disomogenea fra documenti diventa visibile. Il rischio dello spostamento è dichiarato: una voce senza gate scivola, e per questo prende un gate nominato invece di «quando c'è tempo». Il totale residuo non cambia — le ore restano dentro il piano, cambiano di posizione.

## Debito della feature 007a

La [revisione in contesto pulito](../specs/007a-kpi-operators/review.md) di `docs/kpi_operators.md` ha prodotto **6 rilievi e 1 divergenza**. Quattro rilievi e la divergenza sono chiusi dentro la feature; due sono rinviati come issue.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| **invarianza del numeratore della North Star** | i 375 titoli di `Music & Musicals` sono contati sul dato di **origine**; il documento dichiara l'invarianza sul trasformato come **assunzione**, non come dimostrazione — due totali che coincidono non sono la stessa corrispondenza riga per riga | ✅ chiusa dalla `007b`: il conteggio diretto sul trasformato coincide con 375, l'invarianza passa da assunzione a **fatto verificato** (`docs/kpi_measures.md` §2.4) |
| [`#7`](https://github.com/Valvln/streamwave-bi/issues/7) — convenzione di calcolo della mediana | quale definizione di mediana usano le misure su valori pari; `docs/kpi_operators.md` §12 elenca già l'arrotondamento fra i vincoli aperti, ed è la stessa famiglia | ✅ chiusa dalla `007b`, `D10`: ordinamento e media dei due valori centrali, nessuna eccezione per i pari merito |
| [`#8`](https://github.com/Valvln/streamwave-bi/issues/8) — `D6` attribuita a `BQ2-K1` in §11 | imprecisione di una colonna di tabella, contraddetta dal corpo del testo due sezioni più avanti | ✅ chiusa dalla `007b`, nota in loco su §11 |

**Perché due rilievi sono usciti dalla feature.** Nessuno dei due invalida un operatore, ed è il criterio: un rilievo che non cambia una regola di calcolo non giustifica di allungare la feature oltre la propria stima. Rinviarli **è una decisione**, e la sede in cui una decisione di rinvio resta contestabile non è il verbale — che nessuno rilegge — ma il tracker. Da qui in avanti vale come prassi: i rilievi che non invalidano il deliverable si registrano come issue e si dichiarano nel blocco di chiusura, invece di essere chiusi in fretta o dimenticati.

## Debito della feature 007b

La [revisione in contesto pulito](../specs/007b-kpi-measures/review.md) di `docs/kpi_measures.md` ha prodotto **14 rilievi** — il numero più alto del progetto dopo `data_model.md` — divisi dal revisore stesso in due classi dichiarate: sei che «rendono il documento falso o insostenibile», otto che lo rendono «migliorabile». Tutti e sei della prima classe sono chiusi dentro la feature; tutti e otto della seconda sono rinviati come issue, per la regola del 2026-08-22.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| `R1` — «verificato contro il motore» copriva più di quanto `E9` avesse letto | otto sezioni ripetevano lo stesso bollino di verifica anche dove il valore pubblicato — soglie di `BQ2-K3`, formule companion, `british` non campionato — non era mai passato dal motore | ✅ **risolto**: la frase distingue ora misura verificata da valore verificato, sezione per sezione |
| `R2` — «ogni cifra nasce qui» smentita da §8 due sezioni dopo | `BQ3-K1`/`BQ3-K2` sono citazioni dell'artefatto della `004`, non calcoli di questa feature | ✅ **risolto**, correzione di una parola |
| `R3` — «due ordini di grandezza» per tre misure, mostrato per una sola | un moltiplicatore derivato e non ancorato, quantitativamente impreciso e qualitativamente sbagliato per `mood_profile_overlap` (collasso verso zero, non un multiplo) | ✅ **risolto**: descrizione per misura, nessun moltiplicatore aggregato |
| `R4` — la causa del difetto di tipizzazione, come scritta, prediceva che anche `format_duration_gap` fosse colpita | non lo era: legge `duration_min`, derivazione interna del modello (`data_model.md` §13), non una colonna caricata come testo decimale | ✅ **risolto**, la distinzione aggiunta |
| `R5` — una lettura osservata dal motore (`-253,8667`) priva di ancora, in una pagina a severità stretta | il controesempio più severo possibile: la frase immediatamente precedente rivendicava che i valori del confronto non si scrivono a mano | ✅ **risolto**: la lettura è ora una voce propria di `reports/kpi_engine_check.json` |
| `R6` — due fatti misurati (0,0426 → «4 per cento»; posizione 9/114 → «105 altri») marcati come non-misurati | la sola falsità che nessun controllo automatico può intercettare | ✅ **risolto** per la prima cifra (ancora diretta); ⚠️ **indebolito** per la seconda — sostituita con un'affermazione qualitativa vera invece di costruire l'ancora del ranking coi pari merito |
| [`#12`](https://github.com/Valvln/streamwave-bi/issues/12) — `R7`, pari merito in graduatoria | due segmenti con lo stesso punteggio a due decimali ricevono posizioni diverse; l'ordinamento opera sui valori esatti e il documento non lo dice | ⬜ issue aperta, vincolo di presentazione |
| [`#13`](https://github.com/Valvln/streamwave-bi/issues/13) — `R8`, i pesi 0,5/0,5 non pesano uguale sull'osservato | la domanda muove il punteggio ~2,3 volte più dell'affinità sui valori pubblicati; l'argomento di `D3` è solido, la conseguenza per chi legge la graduatoria non è scritta | ⬜ issue aperta, lettura del composito |
| [`#14`](https://github.com/Valvln/streamwave-bi/issues/14) — `R9`, un «ritrovamento» che potrebbe essere aritmetica | la soglia di `is_high_zero_genre` non è mai dichiarata, e senza di essa il lettore non distingue un fatto da una tautologia | ⬜ issue aperta, chiarezza espositiva |
| [`#15`](https://github.com/Valvln/streamwave-bi/issues/15) — `R10`, un superlativo (904 righe minimo, 1000 massimo) senza colonna in appendice che lo mostri | unica coppia di estremi non verificabile sulla pagina, contro tre analoghe verificate | ⬜ issue aperta, ancoraggio di un'affermazione derivata |
| [`#16`](https://github.com/Valvln/streamwave-bi/issues/16) — `R11`, sigle non introdotte (`E9`, `008a`/`008b`, `is_high_zero_genre`, `NF.cat.music_musicals.titles`) | attrito per il lettore esterno dichiarato come destinatario, nessuna singolarmente falsa | ⬜ issue aperta, glossario |
| [`#17`](https://github.com/Valvln/streamwave-bi/issues/17) — `R12`, il terzo vincolo annunciato di `kpi_operators.md` §12 non compare mai | §3.3/§3.4 dicono «primo» e «secondo» dei tre; il terzo resta scoperto, e lo stesso vale per `C2` accanto a `C1`/`C3` | ⬜ issue aperta, verificare contro `kpi_operators.md` |
| [`#18`](https://github.com/Valvln/streamwave-bi/issues/18) — `R13`, `mood_profile_overlap` senza `ALL` su un filtro di categoria | l'omissione è argomentata per il filtro di segmento (§6.2) ma non per quello di categoria, a cui `dim_category_mood` è raggiungibile; il valore attuale non è sbagliato (nessun filtro nel confronto di `E9`), è un rischio per l'uso futuro in dashboard | ⬜ issue aperta, rischio per `008a` |
| [`#19`](https://github.com/Valvln/streamwave-bi/issues/19) — `R14`, la riproducibilità byte-per-byte è l'unica verifica non ancorata come esito booleano | trattamento disomogeneo rispetto a `E7` e `E9`, che ricevono entrambe un identificativo | ⬜ issue aperta, coerenza di forma |

**Perché sei rilievi erano necessari e otto no.** Il revisore stesso li ha divisi in due classi prima ancora che la feature decidesse — «rendono il documento falso o insostenibile» contro «migliorabile» — e la soglia di `CLAUDE.md` ricalca esattamente quella linea: `R1`-`R6` facevano affermare alla pagina qualcosa che i propri dati non sostenevano (uno stato di verifica più ampio di quanto verificato, un moltiplicatore sbagliato, due fatti misurati marcati come non misurati); `R7`-`R14` sono lacune di esposizione o di robustezza futura, nessuna delle quali rende falso un valore oggi pubblicato.

**`#18` ha riguardato direttamente la `008a`, come previsto qui, ed è stata rispettata invece che chiusa.** La feature ha letto la issue prima di costruire e ha scelto — decisione `F2` del proprio piano — di non esporre mai `BQ1-K3` accanto a un filtro di categoria: nessuna pagina costruita ne offre uno. Il rischio non si manifesta nelle pagine esistenti, ma la formula resta quella pubblicata, senza l'`ALL`. **`#18` resta aperta**: chiunque, in `008b` o dopo, voglia esporre `BQ1-K3` in un contesto filtrabile per categoria deve chiuderla prima, non aggirarla come ha fatto la `008a`.

## Debito della feature 008a

La [revisione in contesto pulito](../specs/008a-dashboard-model-pages/review.md) del contratto di pagina e dell'esito della costruzione ha prodotto **25 rilievi** — il numero più alto del progetto. Otto chiusi dentro la feature perché il documento affermava il falso o si contraddiceva; diciassette rinviati, raggruppati in quattro issue per evitare un arretrato di diciassette voci separate che nessuno rilegge.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| `R1`, `R3`, `R4`, `R8`, `R13`, `R15`, `R21`, `R22` | otto contraddizioni interne o affermazioni non più vere — fra cui l'esito che poggiava sulla verifica sbagliata (`007b` invece del confronto diretto `T023`) e una tabella delle grane che dichiarava un filtro dove nessuna pagina ne offre uno | ✅ **risolti**, nessuno indebolito: sette aggiungono ciò che mancava, uno sostituisce un'ancora debole con una più forte già disponibile |
| [`#22`](https://github.com/Valvln/streamwave-bi/issues/22) — `R2`, `R5`, `R6`, `R24`, `R25` | obblighi del contratto di pagina che l'esito non riporta come verificati | ⬜ issue aperta, si chiude con una passata di verifica a schermo |
| [`#23`](https://github.com/Valvln/streamwave-bi/issues/23) — `R7`, `R9`, `R11` | affermazioni date come accertate senza dire come e da chi — inclusa quella per cui Power BI non offrirebbe l'evidenziazione, vera per quanto constatato ma non per una fonte citabile | ⬜ issue aperta |
| [`#24`](https://github.com/Valvln/streamwave-bi/issues/24) — `R12`, `R14`, `R16`, `R19`, `R23` | leggibilità per il lettore esterno: sigle mai sciolte, due numerazioni delle verifiche, nomi di file incoerenti | ⬜ issue aperta, la stessa famiglia della `#16` della `007b` |
| [`#25`](https://github.com/Valvln/streamwave-bi/issues/25) — `R10`, `R17`, `R18`, `R20` | completezza della mappa, dei formati e del DAX trascritto | ⬜ issue aperta |
| [`#20`](https://github.com/Valvln/streamwave-bi/issues/20) — fragilità del `.pbix` non versionato | tre impostazioni vivono solo nel file e nessun controllo del repository le vede: tipizzazione delle colonne di mood (`#11`), `QuoteStyle` sull'origine di `dim_title`, colonna `scenario` di `bq3_scenarios`. Le prime tre si sono già perse una volta ciascuna | ⬜ issue aperta, nota di ricostruzione da tenere aggiornata a ogni riapertura |
| [`#21`](https://github.com/Valvln/streamwave-bi/issues/21) — selezione incrociata su `BQ2` disattivata | Power BI non offre l'evidenziazione per dispersione o tabella; il filtro avrebbe nascosto segmenti dalla graduatoria, quindi l'interazione è spenta in entrambe le direzioni | ⬜ issue aperta, comodità di lettura persa, non una garanzia |

**Perché due difetti di caricamento non sono in questa tabella.** `dim_title` a 8.809 righe invece di 8.807, e `bq3_scenarios` senza la colonna `scenario`, sono stati **trovati e corretti dentro la feature**, prima ancora della revisione: non sono debito, sono lavoro già chiuso. Restano visibili nell'issue `#20` come promemoria di ciò che può riperdersi, non come voci aperte.

**Perché diciassette rilievi in quattro issue e non diciassette issue.** È un'estensione della prassi della `007b`, non una nuova regola: raggruppare per tema fa sì che una singola passata di lavoro chiuda più rilievi insieme, e ogni rilievo resta nominato dentro la propria issue — nessuno sparisce senza numero, che è la garanzia che conta.

## Decisioni aperte

Decisioni consapevolmente rinviate. Non sono debito — il debito è lavoro noto da fare, queste sono scelte non ancora prese — e stanno qui perché una decisione rinviata senza un punto in cui va presa è una decisione che si perde. È già successo una volta, ed è lo scostamento 5 qui sopra.

**Una decisione risolta resta in questa sezione, con la propria risoluzione sotto al testo che la teneva aperta.** Non si sposta altrove e non si cancella: la ragione per cui era stata rinviata è parte di come è stata poi decisa, e separarle renderebbe la seconda illeggibile. Oggi **non ci sono decisioni aperte**: `DA-1` è l'unica voce, ed è chiusa.

### DA-1 — Uso di un LLM per la tabella di corrispondenza generi → mood (`006`)

**Stato**: rinviata il 2026-08-10. **Va presa**: prima di invocare `/speckit.specify` sulla `006`, e il prompt di consegna di quella feature non è consegnabile se non la riporta risolta.

La roadmap iniziale prevedeva questa componente come *Agent 2*. Le due strade sono: un LLM che **propone** le 42 righe della tabella, con revisione riga per riga e versionamento di prompt, modello e data; oppure una tabella curata interamente a mano.

Quello che va deciso non è solo quale strada, ma se la prima sia compatibile con la **D1 della 001**, che ha respinto a verbale l'approccio a modello con la motivazione che introduce «un modello non spiegabile a un board». La distinzione esiste e regge — D1 respingeva l'estrazione del tono dal campo `description`, il cui output è opaco, mentre una tabella di 42 righe revisionata è ispezionabile — ma **va scritta, non sottintesa**: riaprire una decisione documentata senza dichiarare perché è esattamente il modo in cui una constitution si aggira in silenzio.

Ricadute: la scelta chiude anche la divergenza 10 della 001, la governance di quella tabella. E determina se il progetto conserva la componente di lavoro con LLM che la roadmap iniziale prevedeva, o se la perde — nel qual caso la perdita va dichiarata, non subita.

#### Risolta il 2026-08-19 — un LLM propone, con il criterio scritto prima

**La compatibilità con D1 si chiude, e la ragione va scritta perché è ciò che distingue una decisione riaperta da una aggirata.** D1 respinse l'estrazione del tono dal campo `description` per due motivi: un modello non spiegabile a un board, e lo sfondamento del vincolo di giornata. Il primo non si applica qui, per tre differenze che non sono di grado:

- **la scala.** Là erano 8.807 titoli, un output che nessuno verifica riga per riga. Qui sono 42 categorie per tre assi, cioè 126 numeri, che una persona controlla in una seduta;
- **la posizione del modello.** Là il modello sarebbe stato *dentro la pipeline*, e rieseguire l'analisi avrebbe significato rieseguirlo. Qui produce una **prima stesura**, l'esito si congela in una tabella versionata, e **nessuno script chiama mai il modello**. È la forma del benchmark della `004`: un passaggio non riproducibile il cui esito è congelato, con la derivazione a valle deterministica. Il principio V la ammette già;
- **che cosa arriva al lettore.** Una tabella contestabile riga per riga. Da dove vengono i numeri è una questione di provenienza, non di opacità.

Il secondo motivo di D1 non decide in nessuna direzione: costruire 126 valori a mano e revisionarne 126 proposti sono costi dello stesso ordine, e nessuna delle due strade è stata scelta per rapidità.

**L'obiezione che regge non è l'opacità, è l'ancoraggio.** La tabella è l'unico strato interpretativo del progetto e porta tre KPI su otto. Se un modello propone i valori, il lavoro del revisore scivola da autore a **ratificatore**, e chi rilegge 126 numeri plausibili si ancora a quelli che ha davanti. È lo stesso meccanismo per cui nella `002` tre affermazioni derivate erano passate sotto un controllo verde: nessuno le aveva ricalcolate perché sembravano giuste.

**Il presidio è l'ordine dei passi, ed è già in uso nel progetto.** Il criterio di assegnazione si scrive e **si committa da solo, prima che qualunque valore esista**. È la forma di `FR-011a` della `004` — i fattori della banda fissati e committati prima che la ricognizione cominciasse, perché «fissato prima» fosse distinguibile da «riempito dopo» — e vale qui identica. Ne discende un **terzo punto di fermata** per la `006`, dopo il commit del criterio e prima che il modello proponga alcunché: è il punto di massima leva della feature, perché un criterio sbagliato non produce un valore sbagliato, li produce tutti.

Ne discende anche una misura che oggi non esiste: **quante righe la revisione ha spostato rispetto alla proposta**. Va registrata. Se ne sposta zero, non è un successo — è un ritrovamento, e va dichiarato come tale.

**Che cosa la feature deve produrre, in ordine**: il criterio, committato da solo; poi la proposta del modello, con prompt, modello e data versionati; poi la revisione riga per riga contro il criterio, con il conteggio degli spostamenti; poi la tabella congelata in un artefatto versionato, che nessuno script rigenera.

#### La governance della tabella — divergenza 10 della `001`, chiusa qui

Quattro domande, quattro risposte.

**Chi la costruisce**: la sessione della `006`, sul criterio che ha scritto per primo. **Chi la approva**: Valerio, sull'esito della revisione in contesto pulito, che riceve la sola tabella più il criterio e nient'altro. **Con quale criterio si contesta una riga**: quello scritto al primo passo — una contestazione è legittima se lo cita, e altrimenti è un'opinione sul mood di un genere, che non è contestabile perché non è verificabile.

**Se le revisioni invalidino i valori già pubblicati**: sì, e il presidio deve essere meccanico e non di buon senso. La tabella porta un **numero di versione**, e ogni valore pubblicato che ne dipende — `BQ1-K3`, `BQ2-K2`, `BQ2-K3` — dichiara su quale versione è stato calcolato. Senza quel legame si ricade nella classe di difetto del totale a ~65 ore corretto il 2026-08-17: un numero giusto quando è stato scritto e mai più riverificato, che nessuno può distinguere da uno ancora valido.

**Il progetto conserva quindi la componente di lavoro con LLM** che la roadmap iniziale prevedeva come *Agent 2*, in una sola delle due sedi originarie: la `004` l'ha lasciata cadere con le ragioni scritte più sopra, la `006` la tiene. Lo scostamento 5 è chiuso in entrambe le direzioni.

#### Come è andata — eseguita dalla `006` il 2026-08-20

I quattro passi sono stati eseguiti nell'ordine prescritto e la cronologia `git` lo dimostra: criterio `0d950e6`, proposta `acf18c1`, tabella congelata `57c4781`. La misura richiesta esiste e vale **2 celle su 126**, pubblicata come `MOOD.review.changes_count`.

**Due cose sono andate diversamente da come questa decisione le aveva previste, ed entrambe migliorano il disegno.**

La prima: la decisione dava per scontato che la verifica producesse **contestazioni a singole righe**, e basta. Ne ha prodotta una seconda specie — i difetti del **criterio**, che una contestazione di riga non può contenere perché non riguarda una cella ma il metro. La tabella ha quindi un campo che il piano non prevedeva, `criterion_findings`, e il conteggio degli spostamenti va letto insieme a quello: le celle che `CF-1` tocca sono rimaste ferme **proprio perché** il criterio si contraddice su di esse, e muoverle sarebbe stato decidere invece di verificare.

La seconda: «se ne sposta zero non è un successo, è un ritrovamento». Il valore è 2, non 0, quindi il caso previsto non si è dato — ma la ragione per cui era stato previsto si è data lo stesso, e il documento la dichiara nel punto giusto: un conteggio basso non distingue una proposta aderente al criterio da un criterio che non dà appigli. La cautela era ben riposta e non dipendeva dallo zero.

**Ciò che la decisione aveva sottovalutato**: che il criterio potesse essere difettoso. Tutto il presidio è costruito sull'ordine — il metro scritto prima dei valori — e nessuna parte di esso chiede chi verifichi il metro. La risposta pratica è stata la verifica indipendente stessa, che ha trovato tre difetti applicandolo; è un esito fortunato, non un presidio, e va scritto come tale.

## Calendario previsto

| Finestra | Capacità | Contenuto atteso |
|---|---|---|
| 8 → 9 agosto | ~4,5 h spese | `002` ✅ conclusa e mergiata |
| 11 agosto | ~4 h spese | `003`: spec, piano, 48 task e **MVP completo** (T001-T026) |
| 12 → 14 agosto | **non pianificata** | nulla, come previsto. Vedi sotto |
| 15 agosto | ~2,5 h spese | `003` ✅ conclusa e mergiata (T027-T049), revisione inclusa |
| 16 agosto | ~2,5 h di sessione | `004`: spec, piano, 46 task, e implementazione fino alla Prova 9 |
| 17 agosto | ~0,5 h di sessione | `004` ✅ conclusa e mergiata (PR #4), revisione e verbale inclusi |
| 18 agosto | ~2,8 h di sessione | chore ambiente ✅ eseguito; `005` ✅ conclusa, revisione e verbale inclusi |
| 19 → 20 agosto | ~4 h di sessione | `006` ✅ conclusa, revisione e verbale inclusi |
| 21 agosto | ~2 h di sessione | `007a` ✅ conclusa, revisione e verbale inclusi |
| 21 agosto, sera | ~2 h di sessione + ~1,5 h alla GUI | chore `CF-1` ✅ concluso, tabella dei mood alla versione 2; materializzazione 🟡 riuscita tranne `R3` |
| 22 → 23 agosto | ~6,5 h di sessione + ~3 h alla GUI (`E9`, esclusa dalla stima) | `007b` ✅ conclusa, revisione (14 rilievi) e verbale inclusi; il confronto con Power BI ha trovato e chiuso il difetto di tipizzazione sulle colonne di mood |
| 24 → 25 agosto | ~9 h fra sessione e GUI (stimate 5) | `008a` ✅ conclusa, revisione (25 rilievi, il numero più alto del progetto) e verbale inclusi; due difetti di caricamento trovati e corretti in costruzione |
| 26 → 29 agosto | ~6,5 h fra sessione e GUI (stimate 4) | `008b` 🟥 costruita, revisionata (25 rilievi) e **chiusa senza raggiungere il proprio obiettivo**; la dichiarazione di pubblicabilità è stata ritirata |
| **dal 29 agosto** | giornate piene, ~6 h/giorno | `009`, `010a`, `010b`, `011`, più ~1,7 h di debito testuale |

> **Riapertura dell'atterraggio — 2026-08-28.** Le cinque righe qui sotto raccontano la stima come si è mossa fino al 25 agosto e **restano**: erano vere quando sono state scritte, e la loro sequenza è essa stessa un dato sulla qualità delle previsioni di questa roadmap. Non descrivono più il piano. La decisione del 28 agosto aggiunge ~17,5 ore e riporta l'atterraggio a **1-3 settembre** nella stima, **fino al 5** con il fattore di sforamento che le due feature GUI hanno mostrato. La differenza fra le due date è quasi tutta `010b`.
>
> Un giorno del ritardo non è nuovo lavoro: è la `008b` costruita e poi abbandonata. Va contato come speso, perché lo è, ed è ciò che ha reso visibile il difetto.

Atterraggio stimato al 25 agosto: **27-28 agosto**, con `009` escluso. Era 21-22 prima dell'ancoraggio a benchmark della `004`, poi 24-25 con la finestra non pianificata del 12-14 agosto, poi 23-24 dopo le chiusure sotto stima di `003` e `004`, poi di nuovo 24-25 con la materializzazione del modello, poi 26-27 il mattino del 21 agosto, poi 25-26 la sera stessa con la `007a` sotto stima. Restano **~11,7 ore**, cioè meno di due giorni pieni. Lo sforamento della `008a` — ~4 ore, il secondo del progetto dopo la `007b` — sposta l'atterraggio di un altro giorno, oltre la scadenza dell'abbonamento del 26: la pubblicazione di prova, già dichiarata caduta per la catena delle dipendenze e poi per il margine, ora cade anche perché la finestra si è chiusa.

**Il `.pbix` leggibile esiste da ieri, e la scadenza dell'abbonamento è oggi.** È la stessa eccezione dichiarata il 21 agosto — «se la `008` produce un `.pbix` leggibile e restano ore quel giorno, l'ora si spende come opportunità colta» — ma il giorno in cui valeva era il 25, non il 26, e il 25 si è chiuso con la revisione e il merge, non con ore libere per una pubblicazione di prova. Se l'abbonamento risultasse ancora attivo oggi, la decisione di spenderne un'ora resta di Valerio: non è nel piano, non ha un costo se non si fa.

**Il movimento del 21 agosto, in due tempi.** Al mattino la data era scivolata a 26-27 per la ragione scritta qui sotto; in giornata la `007a` ha chiuso in ~2 ore contro 4 e ha riportato l'atterraggio a **25-26**, dentro la scadenza dell'abbonamento. Non basta a riaprire la pubblicazione di prova, che resta caduta: quella dipende da `008a`, che è ancora due feature più avanti.

**Il movimento del mattino non veniva da uno sforamento: veniva dal calendario.** La `006` ha chiuso sotto stima come le tre precedenti — ~4 ore contro 6 — e l'unica voce nuova che entra, la riscrittura del criterio per `CF-1`, vale ~1,5 ore. Il residuo è quindi sceso di ~5,5 ore — la feature che esce, la riscrittura che entra, la pubblicazione che cade — ma la finestra a giornate piene si è aperta il 19 agosto e ha prodotto ~4 ore di lavoro registrato in due giorni. La roadmap non può dire se la differenza sia capacità non spesa o lavoro che i timestamp non vedono — la [nota sulla misura del tempo speso](#nota-sulla-misura-del-tempo-speso) lo vieta, e l'esito della `006` mostra il caso in cui quel metro cede del tutto. Può dire l'unica cosa che serviva a decidere: **al mattino del 21 restavano ~30 ore.**

**La conseguenza operativa è una sola, e cade sulla voce più fragile.** L'atterraggio incrocia ora la scadenza dell'abbonamento — vedi sotto.

**Il chore dell'ambiente Power BI non è stato fatto**, e la finestra a bassa capacità che doveva ospitarlo è chiusa. Va ora incastrato fra `004` e `005`, che è il suo termine ultimo: è l'unica voce del piano che consuma tempo di calendario senza consumare attenzione, e collocarla in una giornata piena è lo spreco che si era cercato di evitare. Se una sessione si apre stanca, è quella da fare.

> **Aggiornamento — 2026-08-18.** Eseguito nel suo termine ultimo, come previsto. La stima era ~3 ore e non è stata misurata separatamente: è stato installato mentre la sessione lavorava ad altro, il che è precisamente la ragione per cui era stato classificato come voce interrompibile.

### Il 18 agosto, in ordine

**Prima il chore, poi la feature**, e non il contrario. La `005` disegna il modello dati per lo strumento che lo ospiterà, e conviene averlo visto funzionare prima di decidere granularità e relazioni: una decisione di modello presa senza aver mai aperto Power BI è una decisione presa su un manuale. Il chore è inoltre l'unica voce interrompibile in qualunque punto del piano residuo — attese di download e di installazione — quindi collocarlo per primo protegge la parte fragile della giornata.

1. **Chore ambiente** (~3 h): VM Windows 11 x64, Power BI Desktop, prima apertura. Non apre branch e non ha spec, per il principio VI. L'esito va scritto nella sezione `Setup` del [README](../README.md), che il principio II richiede: da `007` in avanti la catena include uno strumento che su macOS non esiste.
2. **`005` Data Model Design** (5 h, di cui ~2 il 18): la regia scrive il prompt di consegna la mattina, a partire da questa roadmap. Il debito da dichiarare nel prompt è già mappato — R4 e R7 della revisione `001` (definizione operativa di «segmento», granularità di `BQ2-K2`), il contratto degli output della `003`, e la divergenza 1 della `003` sulla precisione, che `005` incontra ma **non** chiude.

**Ciò che il 18 agosto non fa**: la `006` e la sua decisione aperta `DA-1`. Va risolta prima di `/speckit.specify` sulla `006`, non prima della `005`.

**Com'è andata.** Entrambe le voci sono state eseguite nell'ordine previsto: VM, Windows 11 x64 e primo accesso a Power BI Desktop riuscito, poi la `005`, conclusa in giornata con revisione e verbale. L'ordine ha retto ed è servito — ma va detto con precisione che cosa ha dato, perché la ragione scritta sopra era più forte del vero. **Aprire lo strumento non ha cambiato alcuna decisione di modello**: le grane, le relazioni e le direzioni di filtro sono state decise sugli artefatti della `003` e sulle schede dei KPI, come sarebbero state decise comunque. Ciò che l'ordine ha davvero prodotto è più modesto e più utile: ha reso visibile che il modello **non era stato eseguito**, che è il ritrovamento principale della feature. Averlo scoperto con lo strumento installato lo rende un chore di due ore; scoprirlo dentro la `007` sarebbe stato un blocco.

**Decisione che scade il 18 agosto — la pubblicazione di prova su Power BI Service.** È l'ultimo giorno del trial Pro. La raccomandazione della regia è **lasciarla cadere e dichiararlo**: presuppone la VM appena costruita e qualcosa da pubblicare, e non esiste ancora alcun `.pbix`. Sarebbe un'ora spesa per schermate di un file vuoto, nel giorno in cui il chore e l'apertura della `005` valgono di più. Il rischio era già stato chiuso l'8 agosto — il deliverable è un `.pbix` e Power BI Desktop è gratuito e senza scadenza. **Se Valerio non decide diversamente entro il 18, la voce si considera caduta** e va spostata fra i rischi chiusi con la ragione.

> **Nota di correzione — 2026-08-17, regia.** Nessuna decisione scade il 18 agosto: la scadenza è il **25**, e non è un trial. La voce non cade e non va decisa qui — si sposta a valle della `008`. Motivazione estesa nella nota in coda a [Lavoro fuori dalle feature](#lavoro-fuori-dalle-feature). **Il 18 agosto resta quindi il chore ambiente e l'apertura della `005`**, senza altre decisioni pendenti.

### La finestra non pianificata del 12-14 agosto — com'è andata

Tre giorni in cui il lavoro poteva essere nullo oppure breve, e non è stato deciso in anticipo di proposito. La pianificazione non ha provato a indovinarlo: **nessun lavoro è stato collocato in quella finestra, e nessuna attività l'ha attraversata a metà.** Il calendario è stato costruito assumendo capacità zero, così che qualunque ora effettivamente spesa fosse guadagno e non recupero.

**Esito: capacità zero, come l'ipotesi peggiore prevedeva, e nessun costo.** Il 15 agosto la sessione ha ripreso dalla Phase 4 su un repository coerente, senza dover ricostruire nulla.

Il confine di pausa era stato scelto a **T011**, per una ragione strutturale: i task da T003 a T011 non scrivono alcun file di output — il primo atterra in `data/processed/` a T012 — quindi l'intero tratto era interrompibile senza lasciare dati parziali che invecchiano. L'11 agosto la specifica è costata molto meno del previsto e la sessione è andata **oltre** quel confine fino a T026, cioè fino al MVP: un punto di sosta ancora migliore, perché ciò che restava era tutto lavoro di documento e di verifica, che non dipende da uno stato intermedio dei dati.

Ne esce una regola, non un aneddoto: **il confine di pausa si sceglie dove il lavoro smette di produrre stato intermedio**, non dove il piano ha messo un punto di stop. Le due cose coincidono raramente.

La stima iniziale di 7-10 giornate lavorative **non regge più**: ~65 ore complessive sono 10-11 giornate piene. Lo sforamento non viene dall'esecuzione, che è stata sostanzialmente in linea, ma da due cose che la stima iniziale non conteneva — la revisione indipendente, diventata prassi perché produce valore, e l'ancoraggio dei parametri sintetici a benchmark citati. Sono entrambe scelte di qualità prese consapevolmente. Il modo onesto di registrarlo è questo, non ricalibrare all'indietro la stima di partenza per farla sembrare azzeccata.

> **Nota di correzione — 2026-08-17, regia.** Il capoverso qui sopra contiene un valore errato e, di conseguenza, un'affermazione che non si sostiene. Restano entrambi perché sono la traccia di ciò che la regia aveva concluso.
>
> **Il valore.** «~65 ore complessive» era il totale precedente e includeva la `009`. Sommando le ore spese dalla tabella di Stato — ~7 + ~4,5 + ~6,5 + ~3 = ~21 — e il residuo dichiarato nella riga dei totali — ~39,5, dove la `009` è esclusa — il progetto vale **~60,5 ore**. Lo scarto di ~5 ore è esattamente la stima della `009`: il totale la contava mentre il testo dichiarava di escluderla.
>
> **L'affermazione.** «La stima iniziale non regge più» non discende da quel valore né da quello corretto: ~60,5 ore stanno **dentro** l'intervallo di 49-70 ore, e anche ~65 vi stava. Il confronto reggeva solo scegliendo implicitamente quante ore vale una giornata — a 6 il conto esce dall'intervallo, a 7 vi rientra — e la constitution ammette entrambe le letture. Era un'affermazione derivata priva di ancora in posizione di fatto misurato, cioè la categoria che il §7 di [`convenzioni-marcatura.md`](convenzioni-marcatura.md) vieta. **Causa della divergenza**: il totale non è stato ricalcolato quando la `003` e la `004` hanno chiuso sotto stima e la riga dei totali è stata aggiornata; l'affermazione che vi poggiava non è stata riverificata.
>
> **Che cosa resta vero, e va detto così.** Non il superamento, ma la **sostituzione**: dentro lo stesso involucro di ore sono entrate due attività che la stima iniziale non conteneva — la revisione in contesto pulito e l'ancoraggio a benchmark citati — ed è uscita la `009`. Il perimetro non è cresciuto oltre la previsione: a parità di ore, **compra meno**. È un esito più scomodo di quello che il capoverso dichiarava, non più comodo.
>
> **Fonte verificabile**: tabella di Stato e riga dei totali di questo stesso documento.

## Rischi aperti

**Densità di `007` e `008`.** Nove ore ciascuna **superano** il limite del principio III, che non è più questione di margine: una feature stimata sopra le 6-7 ore non va avviata, va scomposta prima. La scomposizione smette quindi di essere raccomandata e diventa una condizione di apertura. Per `008` il taglio presumibile resta struttura e pagine da una parte, storytelling e rifiniture dall'altra; per `007` va deciso in fase di prompt, non davanti allo schermo. **Fatto il 2026-08-21**, e per `008` il taglio è quello previsto qui.

**Concentrazione del rischio dopo il 18 agosto.** Quattro feature su quattro, incluse le due più dense, più ~5,5 ore di chore e debito, cadono tutte nella finestra a giornate piene. La finestra a bassa capacità si è chiusa senza lasciare arretrato — è la buona notizia — ma anche senza lasciare margine: da qui in avanti ogni sforamento si trasferisce intero sul giorno successivo, perché non esiste più una seconda finestra che lo assorba. Il primo scostamento va quindi letto subito, non a fine feature.

> **Aggiornamento — 2026-08-21.** La `006` e la `007a` sono uscite, entrambe sotto stima, quindi restano **quattro feature** — `007b`, `008a`, `008b`, `010` — più ~6 ore di chore e debito. Il rischio non si è però ridotto in proporzione, perché **le due feature più dense sono entrambe ancora dentro**, e sono le uniche mai state stimate sopra il limite del principio III. Il margine di cui il capoverso lamentava l'assenza non è ricomparso: la prima cosa che il 21 agosto ha consumato è la voce che l'avrebbe usato, la pubblicazione di prova.
>
> **Aggiornamento — 2026-08-23.** La `007b` è uscita, **sopra** stima per la prima volta (~7 ore contro 5). Restano **tre feature** — `008a`, `008b`, `010` — nessuna delle quali era mai stata fra le due dense originarie: quel rischio specifico si chiude qui. Ne resta uno strutturalmente diverso e più concreto, aperto dalla `007b` stessa — vedi «Il `.pbix` non versionato è un rischio ricorrente», sotto.
>
> **Aggiornamento — 2026-08-25.** La `008a` è uscita, sopra stima per la seconda volta di fila (~9 ore contro 5). Restano **due feature** — `008b`, `010`. Il rischio di densità resta chiuso: nessuna delle due ha mai superato il limite del principio III. Il rischio che ne ha preso il posto — due sforamenti consecutivi sulla stessa causa strutturale — è quello descritto sotto, e riguarda ora direttamente `008b`.

**La scomposizione di `007` e `008` è stata fatta il 2026-08-21**, prima di qualunque prompt, ed è descritta in [La scomposizione di `007` e `008`](#la-scomposizione-di-007-e-008--decisione-della-regia-2026-08-21). Nessuna delle quattro feature che ne escono supera il limite del principio III, e il totale non cambia: 4 + 5 e 5 + 4 contro 9 e 9. Una scomposizione che aggiungesse ore sarebbe un ripensamento del perimetro travestito da conformità.

**Il prompt non dice chi revisiona al punto di stop 1.** Sulla `003` la sessione esecutiva si è fermata dopo `/speckit.specify` e ha riportato spec, esito della checklist e sei decisioni da contestare, proseguendo solo dopo l'approvazione — il punto di stop ha quindi tenuto. A revisionare è stato però l'autore e non la regia, che la spec non l'ha letta: il controllo è arrivato a valle sui soli task, con esito positivo su decisioni ereditate, denominatori, note in loco ed esclusioni di perimetro, ma resta un'assicurazione parziale su un artefatto già congelato in 48 task. Non è una violazione: [`CLAUDE.md`](../CLAUDE.md#punti-di-stop-del-flusso) prescrive che la spec torni in revisione e non da chi, e l'autore ha più contesto di chiunque. È un'ambiguità del prompt, e i prompti successivi devono nominare il revisore invece di lasciarlo implicito.

> **Chiuso il 2026-08-21.** I prompt di `004`, `005` e `006` nominano la regia come revisore al primo punto di fermata, e la regia ha effettivamente revisionato tutte e tre le spec prima del piano. Sulla `006` quella revisione ha prodotto il ritrovamento più caro della feature — che l'etichetta `Sintetico` non copriva la tabella — con l'emendamento **v1.2.0** della constitution come conseguenza. È l'argomento per cui il punto di stop 1 è dichiarato il punto di massima leva: un errore di perimetro trovato lì è costato un emendamento, trovato a valle sarebbe costato la feature.

**Il perimetro complessivo ha superato la stima iniziale.** Non è più un rischio, è un fatto: ~65 ore contro le 7-10 giornate (49-70 ore) previste all'inizio, con `009` già escluso e nulla di ulteriore da tagliare che non amputi il framework. Da qui in avanti ogni estensione di perimetro va compensata da un taglio dichiarato, non assorbita.

> **Nota di correzione — 2026-08-17, regia.** Il superamento non è avvenuto: ~60,5 ore contro un intervallo previsto di 49-70 stanno dentro, non oltre. Il valore ~65 includeva la `009` che la frase dichiara esclusa. Motivazione estesa nella nota in coda alla sezione [Calendario previsto](#la-finestra-non-pianificata-del-12-14-agosto--comè-andata).
>
> **La voce non esce però dai rischi aperti**, e il rischio va riformulato invece che ritirato: non «abbiamo sforato», ma **«non abbiamo più margine»**. Il residuo occupa quasi per intero ciò che resta dell'intervallo iniziale, la `009` è già stata spesa come cuscinetto, e non esiste un secondo taglio disponibile che non amputi il framework. La conseguenza operativa è identica a quella dichiarata sopra e resta valida: ogni estensione di perimetro va compensata da un taglio dichiarato, non assorbita.
>
> *Precisazione del 2026-08-21*: il totale aggiornato è **~55,8 ore** — ~29,8 spese dalla tabella di Stato più ~26 di residuo — e resta dentro l'intervallo di 49-70 come il valore che questa nota correggeva. La riformulazione regge intatta, e il 21 agosto ne ha dato il primo caso concreto: l'estensione di perimetro prodotta da `CF-1`, ~1,5 ore, è stata compensata da un taglio dichiarato, la pubblicazione di prova. Non è stata assorbita.
>
> *Precisazione del 2026-08-23*: il totale aggiornato è **~53,5 ore** — ~36,8 spese più ~16,7 di residuo. La `007b` ha sforato di ~2 ore (7 contro 5 stimate), il primo sforamento dopo cinque feature consecutive chiuse sotto stima, ed **è compensato dall'esito, non assorbito in silenzio**: la revisione più densa del progetto dopo `data_model.md` ha prodotto un ritrovamento reale — la tipizzazione sbagliata delle colonne di mood — che altrimenti sarebbe atterrato su `008a` a un costo più alto delle due ore che è costato trovarlo qui. Il totale resta dentro 49-70, e il margine si è ristretto di quanto lo sforamento vale, non di più: nessuna delle otto issue rinviate porta ore di piano.
>
> *Precisazione del 2026-08-25*: il totale aggiornato è **~57,5 ore** — ~45,8 spese più ~11,7 di residuo. La `008a` ha sforato di ~4 ore (9 contro 5 stimate), il secondo sforamento consecutivo dopo la `007b`. **Compensato allo stesso modo**: la parte non scriptabile della feature ha trovato due difetti di caricamento che nessun controllo del repository avrebbe mai potuto vedere — è la stessa dinamica di `E9`, sullo stesso tipo di superficie cieca, il `.pbix` non versionato. Il totale resta dentro 49-70 per un margine che si sta però restringendo più in fretta di quanto le prime sette feature avessero fatto prevedere: due sforamenti su due feature consecutive, entrambi sulla stessa causa strutturale, meritano di essere letti come un pattern e non come due eventi isolati — vedi il rischio qui sotto.

**Il `.pbix` non versionato è un rischio ricorrente, non un incidente isolato: due feature di fila lo hanno confermato.** `E9` della `007b` ha trovato che tre colonne di `dim_track` erano caricate col punto decimale letto come separatore delle migliaia. La `008a` ha trovato altri due difetti della stessa famiglia — il `QuoteStyle` sull'origine di `dim_title`, la colonna `scenario` perduta sulla tabella disconnessa di `BQ3` — durante la propria costruzione, non durante una verifica dedicata come `E9`: sono comparsi da soli. **Tre impostazioni diverse, perse in tre momenti diversi, tutte per la stessa ragione**: `scripts/check_audit_coherence.py` confronta documenti e artefatti versionati, e il `.pbix` non è né l'uno né l'altro — nessun controllo di questo repository entra mai nel modello. Le tre sono ora raccolte in una sola issue, [`#20`](https://github.com/Valvln/streamwave-bi/issues/20), che sostituisce la `#11` come registro delle impostazioni da riverificare a ogni riapertura — `#11` resta aperta e citata dentro `#20`, non chiusa per assorbimento.

**La conseguenza operativa per `008b`**: quella feature non ricostruisce il modello da zero, ma tocca lo stesso `.pbix` per aggiungere narrazione e rifiniture. Se lo riapre, la prima cosa da fare è la stessa di `008a` — verificare le tre impostazioni di `#20` — prima di costruire qualunque cosa sopra.

**La conseguenza operativa per chi apre `008a`**: la prima cosa da fare dopo aver caricato il modello, prima di costruire una sola pagina, è verificare a occhio che `energy`, `valence` e `danceability` di `dim_track` mostrino valori fra 0 e 1 e non nell'ordine delle centinaia. Costa una lettura, come è costato a `E9`. Non è un lavoro da automatizzare — sarebbe di nuovo pilotare la GUI, principio V — è un passo da nominare esplicitamente nel prompt di consegna della `008a`, perché senza `E9` a valle nessuno lo farebbe da sé.

## Rischi chiusi

**Il terzo punto di fermata della `004`** *(chiuso il 2026-08-16)*. Fra la ricerca e la derivazione, a T013, la feature aveva un riporto obbligatorio in entrambi gli esiti — discendeva da FR-006 e FR-006a. Era l'unico punto del progetto in cui una feature si poteva fermare per una ragione **esterna**, cioè l'assenza di una fonte pubblica che reggesse le cinque condizioni. Non è accaduto: una fonte regge, e il riporto è servito a ciò per cui era stato messo, cioè a portare alla regia **una fonte adottata con la propria debolezza** invece di un fallimento. La lezione da tenere: un punto di fermata vale anche quando l'esito è positivo, perché il rischio non è il fallimento rumoroso ma l'adozione silenziosa.

**Ambiente Power BI** *(chiuso il 2026-08-08)*. Power BI Desktop non esiste per macOS. La macchina di sviluppo è però un Mac **Intel x86_64** con 16 GB di RAM e oltre 250 GB liberi: una VM Windows 11 x64 esegue Power BI Desktop in modo nativo, senza l'emulazione x64 che sarebbe stata necessaria su Apple Silicon. Il rischio si riduce al chore di predisposizione. Tableau Public resta il piano di riserva, non il percorso principale.

**Scadenza del trial Power BI Pro** *(chiuso il 2026-08-08)*. Impatto basso: il deliverable è un file `.pbix` e Power BI Desktop è gratuito e senza scadenza. Il trial abilita il Service — workspace, pubblicazione, condivisione — che non serve al deliverable dichiarato. Resta la sola azione opportunistica di pubblicare una versione di prova entro il 18, tracciata fra i chore.

> **Nota di correzione — 2026-08-17, regia.** Non è un trial ma un **abbonamento Microsoft 365** che include Power BI Pro, e la data è il **25 agosto**, non il 18. La chiusura del rischio regge intatta — è anzi ciò che permette all'azione opportunistica di essere rinviata senza costo — e resta valido che il Service non serve al deliverable dichiarato.
>
> *Precisazione del 2026-08-18*: la data corretta è il **26 agosto**, non il 25. Il 25 è l'ultimo giorno coperto; l'abbonamento cessa il giorno dopo.
