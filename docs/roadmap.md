# Roadmap — StreamWave BI

**Aggiornata**: 2026-08-17 | **Stato**: feature 004 conclusa e mergiata (PR #4); chore ambiente e 005 il 18 agosto

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
| `005` | Data Model Design | 5 | 003, *chore ambiente* | ⬜ |
| `006` | Content Taxonomy Bridge | 6 | 002, 005 | ⬜ decisione aperta DA-1 |
| `007` | Misure DAX & KPI | 8 | 004, 005, 006 | ⬜ da scomporre in due |
| `008` | Dashboard Build — Power BI | 8 | 007 | ⬜ da scomporre in due |
| `009` | Porting Tableau Public | 5 | 007 | ⬜ *stretch, primo a cadere* |
| `010` | Case Study & Portfolio Integration | 6 | 008 | ⬜ |

**Totale residuo escluso `009`**: ~33 ore di feature, più ~2,5 ore di debito testuale e ~4 ore di altri chore. Erano ~39 e ~3,5 prima della chiusura della `004`, che ha assorbito anche l'ora di debito testuale sull'ancoraggio.

Le stime di `004`, `006`, `007` e `010` includono la **revisione in contesto pulito e la chiusura dei rilievi** — circa un'ora ciascuna. Era il rischio aperto lasciato dalla 002, dove quel costo era stato l'intero scostamento; è chiuso incorporandolo invece che continuando a scoprirlo a consuntivo. La conseguenza è che `007` sale a 8 ore e raggiunge `008` fra le feature che vanno scomposte prima di essere aperte, non dopo.

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

**Il ritrovamento del contratto è stato chiuso.** Il disallineamento fra il contratto degli output scritto in fase di piano e ciò che l'implementazione ha prodotto, rinviato a T029 (commit `0e959a7`), è rientrato: `005` e `007` leggono un contratto che descrive i file reali.

Resta debito, tracciato sotto.

### Esito della `004` — chiusa il 2026-08-17

**46 task su 46**, in due blocchi di sessione: il 16 agosto dalla spec alla Prova 9 del quickstart, il 17 la chiusura dei rilievi della revisione. I timestamp git coprono ~3 ore contro le 6 stimate, e **lo scarto non va letto come un risparmio**: vale la nota sulla misura del tempo speso più sotto, per cui i timestamp misurano una sessione di agent e non ore-uomo. Ciò che si può dire è che la feature è rientrata nel proprio perimetro senza sforare, e che il blocco E — revisione e chiusura dei rilievi — è stato il più costoso, come previsto.

Lascia quattro artefatti: [`data/benchmarks/bq3_tier_upgrade.json`](../data/benchmarks/bq3_tier_upgrade.json), `scripts/build_bq3_scenarios.py`, [`reports/bq3_scenarios.json`](../reports/bq3_scenarios.json) e [`docs/bq3_scenarios.md`](bq3_scenarios.md). Il primo è la prima cartella di `data/` a essere versionata, e per il motivo opposto a quello delle sorelle: le altre non lo sono perché riproducibili, questa lo è perché non lo è.

**Quattro esiti che valgono oltre la feature.**

*Una proprietà dichiarata in una decisione va verificata sull'implementazione.* La decisione D2 prescriveva una banda «simmetrica in termini relativi». L'implementazione l'ha letta come `1 − k` / `1 + k`, che **non lo è**: la simmetria relativa vale se e solo se il prodotto dei due fattori è l'unità. La banda è stata simmetrica in termini assoluti mentre si dichiarava relativa, per tutta la durata della feature, attraverso spec, piano, contratto, implementazione e due punti di stop della regia. Nessun controllo di questo progetto poteva vederlo — non è un numero sbagliato, è una proprietà mancante — e l'ha trovato la revisione in contesto pulito leggendo il solo documento pubblicato.

*Un esito verde può essere prodotto dal fallimento del comando che doveva verificare.* La Prova 9 del quickstart eseguiva `git diff main -- docs/business_case.md | grep "^-"`. Su un clone `main` non esiste come riferimento locale: git esce con `fatal: bad revision`, non produce output, il `grep` non trova corrispondenze e la prova **riporta esito positivo**. È rimasta così finché il quickstart non è stato eseguito per intero su un clone, cosa che le verifiche di fase — che eseguono le prove una alla volta, nel repository di lavoro — non fanno.

*La regola sulle cifre significative non si applica al denaro.* Il principio I vieta di pubblicare un valore sintetico con precisione superiore a quanto la metodologia giustifica. Applicata alla lettera a un importo produce `1,2 €` dove il valore è `1,20 €`, perché il centesimo è l'unità in cui la valuta è denominata e non una cifra di precisione rivendicata. FR-015 distingue ora due famiglie — cifre significative per i tassi, posizioni decimali fisse per gli importi — e la convenzione dichiara che la precisione effettiva resta quella dell'ingresso. **Vale per ogni documento futuro che pubblichi euro**, cioè per `007` e `008`.

*Il registro dei rigetti non certifica una superlatività.* Rende ispezionabile perché una fonte è stata scartata, ma è compilato da chi sceglie e contiene solo le fonti incontrate: lo spazio di quelle mai trovate non lascia traccia. La rivendicazione sostenibile è «la migliore fra quelle esaminate, secondo un criterio dichiarato», e il criterio adottato qui — solidità della citazione prima della vicinanza al caso d'uso — ha una conseguenza visibile, perché una fonte più vicina per misura è stata respinta perché la citazione non reggeva.

**La ricognizione ha funzionato, ma per poco.** La fonte adottata soddisfa le cinque condizioni della constitution; il suo scarto di misura è ampio e dichiarato in cinque divergenze, di cui **una sola ha un verso noto**, e spinge il valore verso l'alto. Il terzo punto di fermata previsto — T013, il riporto in entrambi gli esiti — è servito esattamente a ciò per cui era stato messo: non a segnalare un fallimento, ma a portare alla regia una fonte adottata con la propria debolezza, su cui la decisione poteva essere diversa.

### Lavoro fuori dalle feature

| Chore | Ore | Entro |
|---|---|---|
| Ambiente Power BI: VM Windows 11 x64 e installazione di Power BI Desktop | ~3 | prima di `005` |
| Debito testuale della 001: rilievi R9, R10, R12 e allineamento di §3 a R11 | ~1 | prima di `007` |
| Debito testuale della 002: divergenza 3, allineare §5 del documento di audit a citare D3 della 001 e A2/A3 del business case | ~0,5 | prima di `007` |
| Debito testuale della 002: portare `docs/data_audit.md` sotto la severità stretta, rimarcandone le quantità | ~1 | prima di `007`, nella stessa sessione della riga sopra |
| ~~Emendamento della constitution: ammettere i benchmark pubblici di settore fra le fonti dati~~ | — | ✅ fatto il 2026-08-15, **v1.1.0** |
| Debito testuale per l'ancoraggio: assunzione di trasferimento in §2 di `docs/business_case.md`, richiamo in §6, note datate sulle schede `BQ3-K1` e `BQ3-K2` | ~1 | ✅ chiuso dentro `004` il 2026-08-16, per sole aggiunte |
| Pubblicazione di prova su workspace Power BI Service e cattura schermate | ~1 | 18 agosto (scadenza trial Pro) — **a rischio**, vedi sotto |

**La pubblicazione di prova entro il 18 agosto va decisa ora, non provata il 18.** Presuppone la VM costruita, Power BI Desktop installato e qualcosa da pubblicare: sono ~4 ore per una cattura di schermate su un file vuoto, in giorni in cui `004` e `005` valgono di più. Il deliverable dichiarato è un `.pbix` e Power BI Desktop è gratuito e senza scadenza — è il rischio già chiuso l'8 agosto. La raccomandazione è **lasciarla cadere e dichiararlo**, invece di scoprire il 18 che non è stata fatta.

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
| R4 / div. 1 | definizione operativa di "segmento": genere della fonte o raggruppamento per mood | `005` |
| R7 / div. 7 | granularità di `BQ2-K2` e riformulazione di §5.2 | `005` |
| R8 | provenienza dei numeri sui dati citati nel business case | ✅ chiusa dalla `002`: `reports/data_profile.json` rigenera i valori citati |
| R11 | quali categorie video compongono `BQ1-K1` e se la selezione è una mappatura | ✅ chiusa dalla `002` sul piano osservativo: una sola categoria, nessuna mappatura. Resta la parte testuale, sotto |
| R5, R6 / div. 2, 3, 4 | operatori indefiniti: intervallo occupato, metrica di distanza, pesi e commensurabilità; quadranti contro combinazione pesata | `007` |
| div. 6 | trattamento delle tracce a popolarità zero | ✅ chiusa dalla `003`, D1: incluse e marcate, mai eliminate. **Ne discende un obbligo per `007`**: ogni misura calcolata sulla popolarità pubblica accanto al proprio valore la quota di zeri del segmento, in particolare `BQ2-K1` |
| div. 8 | segno della differenza e titoli privi di durata | ✅ **parte dati** chiusa dalla `003`, D2: i 3 titoli privi di durata sono gli stessi 3 con classificazione fuori dominio, riparati per spostamento di campo e non imputati. Il **segno della differenza** di `BQ1-K2` resta a `007` |
| div. 9 | dimensione della base utenti | ✅ chiusa per decisione del 2026-08-10: `BQ3-K2` resta **euro per utente al mese e non è scalabile**. Nessuna base utenti viene quantificata. La 004 deve dichiararlo esplicitamente, come la divergenza richiedeva in alternativa |
| div. 10 | governance della tabella generi → mood | `006` |
| div. 11 | posizione dell'alternativa "non entrare" | `010` |
| R13 | ambiguità minori sparse | parte BQ3 ✅ chiusa dalla `004` — le disdette sono escluse, tasso lordo su base costante; il resto resta a `007` |
| R9, R10, R12 | correzioni terminologiche sul testo del business case | debito testuale, ~1 ora, da chiudere prima di `007` |
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
| div. 5 | riverifica del criterio delle categorie musicali se la fonte cambia, e chi se ne accorge | `006` |
| div. 4 | se pubblicare numeratore e denominatore accanto alla frase sulla North Star equivalga a pubblicare la misura | `007` |
| div. 3 | `docs/data_audit.md` §5 contiene due decisioni di modellazione — esclusione delle serie da `BQ1-K2`, ricorso a dati simulati per BQ3 — che sono prese altrove (D3 della 001, A2/A3 del business case) e vanno citate, non riformulate | debito testuale, ~0,5 ore |
| div. 7 | prassi di correzione degli artefatti già mergiati: nota in loco o errata separata | ✅ chiusa il 2026-08-10: regola scritta in [`CLAUDE.md`](../CLAUDE.md#correzione-degli-artefatti-già-mergiati) — nota in loco, valore originale mai cancellato, e la scelta dichiarata come tale invece che come constatazione |

### Nota sulla misura del tempo speso

La 002 è costata **~4,5 ore contro le 4 stimate**, distribuite su due sessioni e due giorni di calendario. Lo scostamento è quasi tutto imputabile alla revisione in contesto pulito, che non era nella stima: la roadmap la dava per non pianificata dopo la 001.

Va però registrato un limite di questa misura, perché tocca ogni stima futura. I timestamp git della 002 misurano il tempo di una sessione di agent, non ore-uomo: fra il commit dei task e quello dell'implementazione passano 45 minuti per un lavoro che a mano ne varrebbe molti di più. **Le stime in ore restano stime di sforzo umano** — è ciò che il principio III vincola — ma il metro dei timestamp non le verifica più direttamente. Da qui in avanti lo scostamento va letto come indicativo, non come misura.

## Debito della feature 003

La [revisione in contesto pulito](../specs/003-data-cleaning-etl/review.md) del documento di cleaning ha prodotto 13 rilievi e 8 divergenze. **I rilievi sono tutti chiusi dentro la 003**, prima del merge, come nella 002. Sei divergenze su otto sono chiuse. Restano queste.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| div. 1 | **a quale precisione si confrontano profilo e rendiconto.** Il profilo memorizza a una cifra decimale ciò che il rendiconto memorizza a quattro; il criterio stretto conta perciò 78 generi «cambiati» dove quelli mossi di oltre mezzo punto sono 3 | `007` |
| div. 5 | **se gli artefatti versionati possano contenere attributi di record individuali**, o solo aggregati e identificativi. Il caso concreto è chiuso — i nomi dei tre titoli riparati sono registrati — ma la regola generale no | `006` |
| severità stretta | il corollario (c) di D5 vale per `docs/data_cleaning.md` e **non è retroattivo** su `docs/data_audit.md`, che resta sotto il regime ad avvisi | debito testuale, ~1 ora, prima di `007` |
| regola D5 in `CLAUDE.md` | portare le affermazioni derivate dal perimetro della feature al metodo del progetto, con le due precisazioni del rilievo R7 | ✅ chiusa dalla regia il 2026-08-15 |

**Sulla divergenza 1, ciò che la feature ha già escluso.** Non c'è un difetto di precisione nel profilo della 002, e questo restringe la decisione. Nel catalogo di origine ogni genere ha esattamente 1.000 righe, quindi la quota di zeri per genere ha una sola cifra decimale **per costruzione**: il profilo la registra esatta. Dopo la deduplicazione i generi non hanno più 1.000 righe e servono quattro cifre. Ciò che resta da decidere è solo se il criterio pubblicato debba essere quello stretto o quello alla precisione minore fra le due, e la risposta cambia due numeri di `docs/data_cleaning.md` §5 e la dimensione del blocco `denominators`. Non è urgente perché il documento pubblica ora i due valori che misurano quanta parte del divario sia apparente — 60 generi tornano identici, 3 si spostano di oltre mezzo punto — quindi nessun lettore è indotto in errore. Va però decisa prima che `007` citi un denominatore in un artefatto pubblicato.

**Sulla severità stretta, la decisione della regia.** Non si estende retroattivamente per automatismo, e non resta nemmeno com'è. Il documento della 002 va rimarcato, ma come debito testuale dichiarato e non come lavoro che una feature successiva assorbe di nascosto. La ragione per farlo, contro l'ipotesi di lasciarlo sotto avvisi per sempre: il senso del corollario (c) è che **un controllo che elenca non ferma nessuno**, e decine di avvisi permanenti su un documento pubblicato addestrano chi legge — e chi scrive — a ignorare l'output. La ragione per non farlo ora: `docs/data_audit.md` è già aperto dalla divergenza 3, e le due cose costano meno insieme. Non è una correzione di valori e non tocca quindi la prassi delle note in loco: si aggiungono marcatori, non si riscrive nulla.

## Debito della feature 004

La revisione in contesto pulito del documento degli scenari ha prodotto **14 rilievi**, tutti chiusi dentro la feature prima del merge, come nella 002 e nella 003. Due hanno richiesto decisioni di Valerio perché toccavano scelte già prese: la rimozione di una divergenza e il cambio dei fattori della banda. Resta questo.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| verificabilità del benchmark | il valore è ancorato a un **comunicato stampa** e a nient'altro: nessuna copia archiviata, nessun identificativo permanente, e il comunicato non nomina lo studio né la numerosità campionaria. Se quell'indirizzo smettesse di rispondere, la verifica esterna verrebbe meno e resterebbe solo il valore congelato nel repository | ⬜ aperta — vedi sotto |
| fonte più vicina non citabile | il valore Antenna sui piani in bundle è strutturalmente più vicino al caso di StreamWave ed è del 2026, ma è dietro registrazione e senza data di pubblicazione dichiarata. Se diventasse citabile, la sostituzione va valutata con nota in loco | ⬜ prima di `008` |
| limite strutturale della banda | nessuna banda moltiplicativa può rappresentare il caso in cui **il trasferimento fallisce**: lo scenario pessimista resta proporzionale al benchmark e non raggiunge lo zero. È dichiarato nel documento e non è correggibile dentro questa forma | ⬜ dichiarato, non chiudibile qui |
| `value` come stringa | l'artefatto della 004 scrive `value` come stringa decimale, dove i due esistenti scrivono un numero JSON. È deliberato — `0,60` e `1,80` non sono esatti in virgola mobile — ma la `007` deve saperlo, ed è nel contratto | `007`, in lettura |
| sigle con suffisso letterale | `FR-011a` e simili non rientrano nell'esclusione strutturale del controllo di marcatura, che si chiude su un confine di parola dopo le cifre. Si scrivono fra apici inversi; registrato in `docs/convenzioni-marcatura.md` | ✅ chiusa per convenzione |

**Sulla verificabilità del benchmark, che è il debito che conta.** È il punto su cui l'intera terza domanda di business poggia, ed è più fragile di quanto la presenza di una citazione faccia sembrare. Il documento lo dichiara in §9 invece di lasciarlo dedurre, ma dichiararlo non lo chiude. Le strade sono due e nessuna è dentro il perimetro di questa feature: archiviare una copia del comunicato nel repository, che pone una questione di licenza, oppure trovare una fonte primaria che pubblichi la stessa grandezza con metodo ispezionabile — cosa che la ricognizione non ha trovato. **Va deciso prima che `008` pubblichi quei numeri in una dashboard**, perché è lì che smettono di essere un artefatto tecnico e diventano un'affermazione rivolta a un lettore.

## Decisioni aperte

Decisioni consapevolmente rinviate. Non sono debito — il debito è lavoro noto da fare, queste sono scelte non ancora prese — e stanno qui perché una decisione rinviata senza un punto in cui va presa è una decisione che si perde. È già successo una volta, ed è lo scostamento 5 qui sopra.

### DA-1 — Uso di un LLM per la tabella di corrispondenza generi → mood (`006`)

**Stato**: rinviata il 2026-08-10. **Va presa**: prima di invocare `/speckit.specify` sulla `006`, e il prompt di consegna di quella feature non è consegnabile se non la riporta risolta.

La roadmap iniziale prevedeva questa componente come *Agent 2*. Le due strade sono: un LLM che **propone** le 42 righe della tabella, con revisione riga per riga e versionamento di prompt, modello e data; oppure una tabella curata interamente a mano.

Quello che va deciso non è solo quale strada, ma se la prima sia compatibile con la **D1 della 001**, che ha respinto a verbale l'approccio a modello con la motivazione che introduce «un modello non spiegabile a un board». La distinzione esiste e regge — D1 respingeva l'estrazione del tono dal campo `description`, il cui output è opaco, mentre una tabella di 42 righe revisionata è ispezionabile — ma **va scritta, non sottintesa**: riaprire una decisione documentata senza dichiarare perché è esattamente il modo in cui una constitution si aggira in silenzio.

Ricadute: la scelta chiude anche la divergenza 10 della 001, la governance di quella tabella. E determina se il progetto conserva la componente di lavoro con LLM che la roadmap iniziale prevedeva, o se la perde — nel qual caso la perdita va dichiarata, non subita.

## Calendario previsto

| Finestra | Capacità | Contenuto atteso |
|---|---|---|
| 8 → 9 agosto | ~4,5 h spese | `002` ✅ conclusa e mergiata |
| 11 agosto | ~4 h spese | `003`: spec, piano, 48 task e **MVP completo** (T001-T026) |
| 12 → 14 agosto | **non pianificata** | nulla, come previsto. Vedi sotto |
| 15 agosto | ~2,5 h spese | `003` ✅ conclusa e mergiata (T027-T049), revisione inclusa |
| 16 agosto | ~2,5 h di sessione | `004`: spec, piano, 46 task, e implementazione fino alla Prova 9 |
| 17 agosto | ~0,5 h di sessione | `004` ✅ conclusa e mergiata (PR #4), revisione e verbale inclusi |
| **18 agosto** | ~6 h | **chore ambiente Power BI (~3 h), poi apertura della `005`.** Vedi sotto |
| dal 19 agosto | giornate piene, ~6 h/giorno | `005`, `006`, `007`, `008`, `010`, più ~6,5 h di chore e debito |

Atterraggio stimato: **23-24 agosto**, con `009` escluso. Era 21-22 prima dell'ancoraggio a benchmark della `004` e dell'inclusione del costo di revisione nelle stime, poi 24-25 con la finestra non pianificata del 12-14 agosto. Le ore in più dell'11 agosto lo avevano riportato a 23-24, e le chiusure di `003` e `004` sotto stima lo confermano: restano ~39,5 ore su giornate da ~6, cioè poco meno di sette giorni pieni a partire dal 18 agosto.

**Il chore dell'ambiente Power BI non è stato fatto**, e la finestra a bassa capacità che doveva ospitarlo è chiusa. Va ora incastrato fra `004` e `005`, che è il suo termine ultimo: è l'unica voce del piano che consuma tempo di calendario senza consumare attenzione, e collocarla in una giornata piena è lo spreco che si era cercato di evitare. Se una sessione si apre stanca, è quella da fare.

### Il 18 agosto, in ordine

**Prima il chore, poi la feature**, e non il contrario. La `005` disegna il modello dati per lo strumento che lo ospiterà, e conviene averlo visto funzionare prima di decidere granularità e relazioni: una decisione di modello presa senza aver mai aperto Power BI è una decisione presa su un manuale. Il chore è inoltre l'unica voce interrompibile in qualunque punto del piano residuo — attese di download e di installazione — quindi collocarlo per primo protegge la parte fragile della giornata.

1. **Chore ambiente** (~3 h): VM Windows 11 x64, Power BI Desktop, prima apertura. Non apre branch e non ha spec, per il principio VI. L'esito va scritto nella sezione `Setup` del [README](../README.md), che il principio II richiede: da `007` in avanti la catena include uno strumento che su macOS non esiste.
2. **`005` Data Model Design** (5 h, di cui ~2 il 18): la regia scrive il prompt di consegna la mattina, a partire da questa roadmap. Il debito da dichiarare nel prompt è già mappato — R4 e R7 della revisione `001` (definizione operativa di «segmento», granularità di `BQ2-K2`), il contratto degli output della `003`, e la divergenza 1 della `003` sulla precisione, che `005` incontra ma **non** chiude.

**Ciò che il 18 agosto non fa**: la `006` e la sua decisione aperta `DA-1`. Va risolta prima di `/speckit.specify` sulla `006`, non prima della `005`.

**Decisione che scade il 18 agosto — la pubblicazione di prova su Power BI Service.** È l'ultimo giorno del trial Pro. La raccomandazione della regia è **lasciarla cadere e dichiararlo**: presuppone la VM appena costruita e qualcosa da pubblicare, e non esiste ancora alcun `.pbix`. Sarebbe un'ora spesa per schermate di un file vuoto, nel giorno in cui il chore e l'apertura della `005` valgono di più. Il rischio era già stato chiuso l'8 agosto — il deliverable è un `.pbix` e Power BI Desktop è gratuito e senza scadenza. **Se Valerio non decide diversamente entro il 18, la voce si considera caduta** e va spostata fra i rischi chiusi con la ragione.

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

**Densità di `008`.** Otto ore per una sola feature sono il limite superiore del principio III, e la voce più esposta a scoprirsi più grande di così davanti allo schermo. Va scomposta in fase di `/speckit.specify` — presumibilmente struttura e pagine da una parte, storytelling e rifiniture dall'altra — non dopo averla aperta.

**Concentrazione del rischio dopo il 17 agosto.** Cinque feature su cinque, incluse le tre più dense, più ~6,5 ore di chore e debito, cadono tutte nella finestra a giornate piene. La finestra a bassa capacità si è chiusa senza lasciare arretrato — è la buona notizia — ma anche senza lasciare margine: da qui in avanti ogni sforamento si trasferisce intero sul giorno successivo, perché non esiste più una seconda finestra che lo assorba. Il primo scostamento va quindi letto subito, non a fine feature.

**Il prompt non dice chi revisiona al punto di stop 1.** Sulla `003` la sessione esecutiva si è fermata dopo `/speckit.specify` e ha riportato spec, esito della checklist e sei decisioni da contestare, proseguendo solo dopo l'approvazione — il punto di stop ha quindi tenuto. A revisionare è stato però l'autore e non la regia, che la spec non l'ha letta: il controllo è arrivato a valle sui soli task, con esito positivo su decisioni ereditate, denominatori, note in loco ed esclusioni di perimetro, ma resta un'assicurazione parziale su un artefatto già congelato in 48 task. Non è una violazione: [`CLAUDE.md`](../CLAUDE.md#punti-di-stop-del-flusso) prescrive che la spec torni in revisione e non da chi, e l'autore ha più contesto di chiunque. È un'ambiguità del prompt, e i prompti successivi devono nominare il revisore invece di lasciarlo implicito.

**Il perimetro complessivo ha superato la stima iniziale.** Non è più un rischio, è un fatto: ~65 ore contro le 7-10 giornate (49-70 ore) previste all'inizio, con `009` già escluso e nulla di ulteriore da tagliare che non amputi il framework. Da qui in avanti ogni estensione di perimetro va compensata da un taglio dichiarato, non assorbita.

> **Nota di correzione — 2026-08-17, regia.** Il superamento non è avvenuto: ~60,5 ore contro un intervallo previsto di 49-70 stanno dentro, non oltre. Il valore ~65 includeva la `009` che la frase dichiara esclusa. Motivazione estesa nella nota in coda alla sezione [Calendario previsto](#la-finestra-non-pianificata-del-12-14-agosto--comè-andata).
>
> **La voce non esce però dai rischi aperti**, e il rischio va riformulato invece che ritirato: non «abbiamo sforato», ma **«non abbiamo più margine»**. Il residuo occupa quasi per intero ciò che resta dell'intervallo iniziale, la `009` è già stata spesa come cuscinetto, e non esiste un secondo taglio disponibile che non amputi il framework. La conseguenza operativa è identica a quella dichiarata sopra e resta valida: ogni estensione di perimetro va compensata da un taglio dichiarato, non assorbita.

## Rischi chiusi

**Il terzo punto di fermata della `004`** *(chiuso il 2026-08-16)*. Fra la ricerca e la derivazione, a T013, la feature aveva un riporto obbligatorio in entrambi gli esiti — discendeva da FR-006 e FR-006a. Era l'unico punto del progetto in cui una feature si poteva fermare per una ragione **esterna**, cioè l'assenza di una fonte pubblica che reggesse le cinque condizioni. Non è accaduto: una fonte regge, e il riporto è servito a ciò per cui era stato messo, cioè a portare alla regia **una fonte adottata con la propria debolezza** invece di un fallimento. La lezione da tenere: un punto di fermata vale anche quando l'esito è positivo, perché il rischio non è il fallimento rumoroso ma l'adozione silenziosa.

**Ambiente Power BI** *(chiuso il 2026-08-08)*. Power BI Desktop non esiste per macOS. La macchina di sviluppo è però un Mac **Intel x86_64** con 16 GB di RAM e oltre 250 GB liberi: una VM Windows 11 x64 esegue Power BI Desktop in modo nativo, senza l'emulazione x64 che sarebbe stata necessaria su Apple Silicon. Il rischio si riduce al chore di predisposizione. Tableau Public resta il piano di riserva, non il percorso principale.

**Scadenza del trial Power BI Pro** *(chiuso il 2026-08-08)*. Impatto basso: il deliverable è un file `.pbix` e Power BI Desktop è gratuito e senza scadenza. Il trial abilita il Service — workspace, pubblicazione, condivisione — che non serve al deliverable dichiarato. Resta la sola azione opportunistica di pubblicare una versione di prova entro il 18, tracciata fra i chore.
