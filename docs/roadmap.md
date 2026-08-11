# Roadmap — StreamWave BI

**Aggiornata**: 2026-08-10 | **Stato**: feature 002 conclusa e mergiata, 003 da aprire

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
| `003` | Data Cleaning & ETL | 7 | 002 | 🔄 in corso — spec, piano e 48 task chiusi; implementazione avviata |
| `004` | Synthetic Business Metrics | 6 | 001 | ⬜ ancorata a benchmark, vedi sotto |
| `005` | Data Model Design | 5 | 003, *chore ambiente* | ⬜ |
| `006` | Content Taxonomy Bridge | 6 | 002, 005 | ⬜ decisione aperta DA-1 |
| `007` | Misure DAX & KPI | 8 | 004, 005, 006 | ⬜ da scomporre in due |
| `008` | Dashboard Build — Power BI | 8 | 007 | ⬜ da scomporre in due |
| `009` | Porting Tableau Public | 5 | 007 | ⬜ *stretch, primo a cadere* |
| `010` | Case Study & Portfolio Integration | 6 | 008 | ⬜ |

**Totale residuo escluso `009`**: ~46 ore di feature, più ~2,5 ore di debito testuale e ~5 ore di altri chore.

Le stime di `003`, `006`, `007` e `010` includono da ora la **revisione in contesto pulito e la chiusura dei rilievi** — circa un'ora ciascuna. Era il rischio aperto lasciato dalla 002, dove quel costo era stato l'intero scostamento; è chiuso incorporandolo invece che continuando a scoprirlo a consuntivo. La conseguenza è che `007` sale a 8 ore e raggiunge `008` fra le feature che vanno scomposte prima di essere aperte, non dopo.

`004` non dipende da `002` e `003`: genera dati che non esistono, quindi non ha bisogno che i dati reali siano puliti. È l'unica feature parallelizzabile e va tenuta come riserva per le giornate in cui il contesto sui dati reali non è fresco.

### Nota sulla `004` — ancoraggio a benchmark pubblici

**Decisione del 2026-08-10: accolta, rifilata.** La 004 come originariamente prevista sarebbe stato l'unico artefatto del progetto in cui la fonte di ogni parametro è "l'analista ha deciso così". Formalmente conforme — la constitution ammette i sintetici con assunzioni dichiarate a confidenza bassa — ma incoerente con la tesi del progetto, che è il principio I. I parametri di scenario vanno ancorati a benchmark pubblici di settore, con fonte, data di accesso e citazione puntuale, e legati ai KPI in un file di assunzioni versionato. Il documento `docs/business_case.md` §7, scheda `BQ3-K1`, prende già questo impegno e non lo ha ancora onorato.

Il perimetro è però molto più stretto di quanto la proposta iniziale prevedesse, perché tre dei valori proposti non hanno un consumatore nel framework:

- **il churn è vietato, non facoltativo**: FR-018 della 001 esclude esplicitamente una riduzione di churn dal modello. Un benchmark di churn finanzierebbe un parametro che il framework proibisce di usare;
- **l'engagement non ha KPI**: BQ3 ha due sole misure, `premium_tier_adoption_rate` e `arpu_uplift`. Nessuna consuma engagement. Generarne un dataset produrrebbe numeri che nessuna misura legge;
- **i prezzi sono già fissati**: A4 e FR-017a li stabiliscono come valori puntuali di scenario e vietano di esprimerli a range. Nessun benchmark di ARPU serve a determinarli.

Resta **un solo benchmark indispensabile**: il tasso di conversione a un tier superiore in servizi di streaming, su cui `BQ3-K1` costruisce best/base/worst. La base utenti **non** va quantificata, per la decisione presa sulla divergenza 9 qui sotto.

**Confidenza dei parametri da benchmark**: si istituisce un'**assunzione di trasferimento** gemella di A1, non un quarto livello della scala. Un benchmark di un operatore terzo è dato osservato su qualcun altro e trasferito a StreamWave: è la stessa natura di A1, che §6 del business case tiene fuori scala per costruzione dopo il rilievo R1. Un quarto livello cambierebbe l'asse su cui tutti e 8 i KPI sono già classificati, obbligando a rivederli uno per uno, per coprire un caso che il pattern esistente copre già.

**Determinismo**: la ricerca produce un file di parametri versionato con fonte e data; uno script con seed fisso genera il dataset a partire da quel file. La pipeline resta rieseguibile da una copia pulita; la ricerca no, ed è congelata. Il precedente è il principio V, che già ammette lavoro non automatizzabile purché versionato come artefatto testuale. Se la ricerca alimentasse la generazione a ogni esecuzione, il principio II sarebbe violato.

**Nessun framework di orchestrazione** (LangChain, LangGraph o equivalenti) per questa feature: il passaggio di raccolta produce un valore congelato che nessuno riesegue, e un'orchestrazione a grafo aggiungerebbe una dipendenza, una chiave API e un componente che dopo la prima esecuzione resta inerte. La sede in cui il lavoro con LLM ha senso è la `006` — vedi Decisioni aperte.

**Stima**: da 5 a 6 ore. L'ancoraggio aggiunge circa un'ora di raccolta e citazione, l'uscita dell'engagement dalla generazione ne restituisce altrettante, la revisione in contesto pulito ne aggiunge una. Resta **una sola feature dentro il limite del principio III**: la scomposizione che la proposta dava per necessaria non serve, perché contava dentro la feature l'emendamento della constitution e le note testuali, che sono chore. Da riverificare in fase di `/speckit.specify`.

### Lavoro fuori dalle feature

| Chore | Ore | Entro |
|---|---|---|
| Ambiente Power BI: VM Windows 11 x64 e installazione di Power BI Desktop | ~3 | prima di `005` |
| Debito testuale della 001: rilievi R9, R10, R12 e allineamento di §3 a R11 | ~1 | prima di `007` |
| Debito testuale della 002: divergenza 3, allineare §5 del documento di audit a citare D3 della 001 e A2/A3 del business case | ~0,5 | prima di `007` |
| Emendamento della constitution: ammettere i benchmark pubblici di settore fra le fonti dati, con Sync Impact Report e bump di versione | ~1 | prima di `004` |
| Debito testuale per l'ancoraggio: assunzione di trasferimento in §2 di `docs/business_case.md`, richiamo in §6, note datate sulle schede `BQ3-K1` e `BQ3-K2` | ~1 | dentro `004` o subito prima |
| Pubblicazione di prova su workspace Power BI Service e cattura schermate | ~1 | 18 agosto (scadenza trial Pro) |

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
| div. 6 | trattamento delle tracce a popolarità zero | `003` |
| div. 8 | segno della differenza e titoli privi di durata | `003` (dati) + `007` (segno) |
| div. 9 | dimensione della base utenti | ✅ chiusa per decisione del 2026-08-10: `BQ3-K2` resta **euro per utente al mese e non è scalabile**. Nessuna base utenti viene quantificata. La 004 deve dichiararlo esplicitamente, come la divergenza richiedeva in alternativa |
| div. 10 | governance della tabella generi → mood | `006` |
| div. 11 | posizione dell'alternativa "non entrare" | `010` |
| R13 | ambiguità minori sparse | `004`, `007` |
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
| div. 1 | che cosa il vincolo di tracciabilità debba coprire: ancorare tutto, estendere ancora il controllo, o dichiararne il confine | `003` |
| div. 2 | statuto delle **affermazioni derivate** — confronti, graduatorie, rapporti costruiti sui valori. Sono la categoria in cui si concentrano gli errori: vanno calcolate nel profilo o vietate in prosa | `003` |
| div. 6 | quale delle due letture di «sovrastima di circa un quinto» adottare, prima che si calcoli un totale di catalogo | `003` |
| div. 8 | criterio con cui si seleziona l'insieme dei generi a forte concentrazione di zeri: `country` al 58,70% cade dentro o fuori a seconda di una soglia che nessuno ha ancora fissato | `003` |
| div. 5 | riverifica del criterio delle categorie musicali se la fonte cambia, e chi se ne accorge | `006` |
| div. 4 | se pubblicare numeratore e denominatore accanto alla frase sulla North Star equivalga a pubblicare la misura | `007` |
| div. 3 | `docs/data_audit.md` §5 contiene due decisioni di modellazione — esclusione delle serie da `BQ1-K2`, ricorso a dati simulati per BQ3 — che sono prese altrove (D3 della 001, A2/A3 del business case) e vanno citate, non riformulate | debito testuale, ~0,5 ore |
| div. 7 | prassi di correzione degli artefatti già mergiati: nota in loco o errata separata | ✅ chiusa il 2026-08-10: regola scritta in [`CLAUDE.md`](../CLAUDE.md#correzione-degli-artefatti-già-mergiati) — nota in loco, valore originale mai cancellato, e la scelta dichiarata come tale invece che come constatazione |

### Nota sulla misura del tempo speso

La 002 è costata **~4,5 ore contro le 4 stimate**, distribuite su due sessioni e due giorni di calendario. Lo scostamento è quasi tutto imputabile alla revisione in contesto pulito, che non era nella stima: la roadmap la dava per non pianificata dopo la 001.

Va però registrato un limite di questa misura, perché tocca ogni stima futura. I timestamp git della 002 misurano il tempo di una sessione di agent, non ore-uomo: fra il commit dei task e quello dell'implementazione passano 45 minuti per un lavoro che a mano ne varrebbe molti di più. **Le stime in ore restano stime di sforzo umano** — è ciò che il principio III vincola — ma il metro dei timestamp non le verifica più direttamente. Da qui in avanti lo scostamento va letto come indicativo, non come misura.

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
| 11 agosto | 2-3,5 h | spec, piano e 48 task della `003`; poi implementazione fino a **T011** |
| 12 → 14 agosto | **non pianificata** | nulla. Vedi sotto |
| 15 agosto | ~2 h | `003` da T012, o chore ambiente |
| dal 16 agosto | giornate piene, ~6 h/giorno | `004`, `005`, `006`, `007`, `008`, `010` |

Atterraggio stimato: **24-25 agosto**, con `009` escluso. Era 21-22 prima dell'ancoraggio a benchmark della `004` e dell'inclusione del costo di revisione nelle stime; la finestra non pianificata del 12-14 agosto ne sposta uno.

### La finestra non pianificata del 12-14 agosto

Tre giorni in cui il lavoro può essere nullo oppure breve, e non è deciso in anticipo di proposito. La pianificazione non prova a indovinarlo: **nessun lavoro è collocato in quella finestra, e nessuna attività la attraversa a metà.** Il calendario qui sopra è costruito assumendo capacità zero, così che qualunque ora effettivamente spesa sia guadagno e non recupero.

Il principio III chiede il repository coerente alla fine di ogni sessione; con tre giorni di distanza quel vincolo smette di essere una formalità, perché ciò che resta aperto non perde solo continuità ma il contesto di chi lo aveva aperto.

L'11 agosto la fase di specifica è costata molto meno del previsto, e l'implementazione è partita lo stesso giorno. Il confine scelto non è più il punto di stop 2 ma **T011**, per una ragione strutturale: i task da T003 a T011 non scrivono alcun file di output — il primo atterra in `data/processed/` a T012. L'intero tratto è quindi interrompibile senza lasciare dati parziali che invecchiano, e coincide con la parte del lavoro che dipende dal contratto invece che dal quadro d'insieme. È il confine di pausa migliore disponibile dentro questa feature.

Se la finestra ospiterà qualcosa, il candidato naturale è il **chore dell'ambiente Power BI**: download e installazioni, nessun contesto da ricostruire, interrompibile in qualunque punto e senza conseguenze se non viene toccato.

La stima iniziale di 7-10 giornate lavorative **non regge più**: ~65 ore complessive sono 10-11 giornate piene. Lo sforamento non viene dall'esecuzione, che è stata sostanzialmente in linea, ma da due cose che la stima iniziale non conteneva — la revisione indipendente, diventata prassi perché produce valore, e l'ancoraggio dei parametri sintetici a benchmark citati. Sono entrambe scelte di qualità prese consapevolmente. Il modo onesto di registrarlo è questo, non ricalibrare all'indietro la stima di partenza per farla sembrare azzeccata.

Il chore dell'ambiente è collocato nella finestra a bassa capacità di proposito: è lavoro a bassa intensità cognitiva — attese di download e di installazione — e sarebbe uno spreco consumarci una giornata piena. Va però completato entro il 15, perché `005` disegna il modello dati per lo strumento che lo ospiterà e conviene averlo visto funzionare prima.

## Rischi aperti

**Densità di `008`.** Otto ore per una sola feature sono il limite superiore del principio III, e la voce più esposta a scoprirsi più grande di così davanti allo schermo. Va scomposta in fase di `/speckit.specify` — presumibilmente struttura e pagine da una parte, storytelling e rifiniture dall'altra — non dopo averla aperta.

**Concentrazione del rischio dopo il 16 agosto.** Sei feature su otto cadono nella finestra a giornate piene, incluse le tre più dense. La finestra a bassa capacità non ha margine di recupero: se `003` sfora, lo scostamento si trasferisce intero sulla seconda finestra invece di essere assorbito. La `002` ha sforato di mezz'ora e la finestra l'ha assorbita, ma era la più piccola delle due.

**Il prompt non dice chi revisiona al punto di stop 1.** Sulla `003` la sessione esecutiva si è fermata dopo `/speckit.specify` e ha riportato spec, esito della checklist e sei decisioni da contestare, proseguendo solo dopo l'approvazione — il punto di stop ha quindi tenuto. A revisionare è stato però l'autore e non la regia, che la spec non l'ha letta: il controllo è arrivato a valle sui soli task, con esito positivo su decisioni ereditate, denominatori, note in loco ed esclusioni di perimetro, ma resta un'assicurazione parziale su un artefatto già congelato in 48 task. Non è una violazione: [`CLAUDE.md`](../CLAUDE.md#punti-di-stop-del-flusso) prescrive che la spec torni in revisione e non da chi, e l'autore ha più contesto di chiunque. È un'ambiguità del prompt, e i prompti successivi devono nominare il revisore invece di lasciarlo implicito.

**Il perimetro complessivo ha superato la stima iniziale.** Non è più un rischio, è un fatto: ~65 ore contro le 7-10 giornate (49-70 ore) previste all'inizio, con `009` già escluso e nulla di ulteriore da tagliare che non amputi il framework. Da qui in avanti ogni estensione di perimetro va compensata da un taglio dichiarato, non assorbita.

## Rischi chiusi

**Ambiente Power BI** *(chiuso il 2026-08-08)*. Power BI Desktop non esiste per macOS. La macchina di sviluppo è però un Mac **Intel x86_64** con 16 GB di RAM e oltre 250 GB liberi: una VM Windows 11 x64 esegue Power BI Desktop in modo nativo, senza l'emulazione x64 che sarebbe stata necessaria su Apple Silicon. Il rischio si riduce al chore di predisposizione. Tableau Public resta il piano di riserva, non il percorso principale.

**Scadenza del trial Power BI Pro** *(chiuso il 2026-08-08)*. Impatto basso: il deliverable è un file `.pbix` e Power BI Desktop è gratuito e senza scadenza. Il trial abilita il Service — workspace, pubblicazione, condivisione — che non serve al deliverable dichiarato. Resta la sola azione opportunistica di pubblicare una versione di prova entro il 18, tracciata fra i chore.
