# Roadmap — StreamWave BI

**Aggiornata**: 2026-08-08 | **Stato**: feature 001 conclusa, 002 da aprire

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
| `002` | Data Audit & Profiling | 4 | 001 | ⬜ prossima |
| `003` | Data Cleaning & ETL | 6 | 002 | ⬜ |
| `004` | Synthetic Business Metrics | 5 | 001 | ⬜ |
| `005` | Data Model Design | 5 | 003, *chore ambiente* | ⬜ |
| `006` | Content Taxonomy Bridge | 5 | 002, 005 | ⬜ |
| `007` | Misure DAX & KPI | 7 | 004, 005, 006 | ⬜ |
| `008` | Dashboard Build — Power BI | 8 | 007 | ⬜ da scomporre in due |
| `009` | Porting Tableau Public | 5 | 007 | ⬜ *stretch, primo a cadere* |
| `010` | Case Study & Portfolio Integration | 5 | 008 | ⬜ |

**Totale residuo escluso `009`**: ~45 ore, più ~1 ora di debito testuale sulla 001 e ~3 ore di chore.

`004` non dipende da `002` e `003`: genera dati che non esistono, quindi non ha bisogno che i dati reali siano puliti. È l'unica feature parallelizzabile e va tenuta come riserva per le giornate in cui il contesto sui dati reali non è fresco.

### Lavoro fuori dalle feature

| Chore | Ore | Entro |
|---|---|---|
| Ambiente Power BI: VM Windows 11 x64 e installazione di Power BI Desktop | ~3 | prima di `005` |
| Debito testuale della 001: rilievi R9, R10, R12 e allineamento di §3 a R11 | ~1 | prima di `007` |
| Pubblicazione di prova su workspace Power BI Service e cattura schermate | ~1 | 18 agosto (scadenza trial Pro) |

Nessuno dei tre è una feature e nessuno apre un branch numerato. Il principio VI della constitution richiede che ogni feature sia riconducibile a BQ1, BQ2 o BQ3: predisporre una macchina virtuale non risponde ad alcuna domanda di business. Trattarlo come feature significherebbe o violare il principio VI, o inventargli un aggancio narrativo che non ha. Resta lavoro necessario, tracciato qui e non in una spec.

Il requisito di ambiente va però documentato — il principio II chiede che chiunque cloni il repository possa rieseguire la pipeline, e da `007` in avanti la pipeline include uno strumento che su macOS non esiste. La sede è la sezione Setup del [README](../README.md), non una spec.

## Scostamenti dalla roadmap iniziale

La roadmap costruita a inizio progetto prevedeva 10 voci in 7-10 giornate lavorative. Quattro modifiche, tutte con una ragione:

1. **Numerazione allineata ai branch.** La roadmap iniziale numerava da 0, il repository da 001. Ogni riferimento incrociato era sfalsato di uno. Vince la numerazione dei branch, che è quella che compare nella history git.

2. **`002` ridimensionata da una giornata a mezza.** Il profiling è già stato eseguito in [`research.md`](../specs/001-business-case-kpi/research.md) della 001: nulli per campo, 89.741 identificativi distinti su 114.000 righe, campionamento bilanciato a 1.000 tracce per genere, massa di zeri in `popularity`. Quei numeri esistono però solo come prosa, senza uno script che li rigeneri — che è il rilievo R8 della revisione. La feature non riparte da zero: produce lo script mancante e completa ciò che manca.

3. **`006` (Content Taxonomy Bridge) non è più stretch.** Era marcata opzionale. Tre KPI su otto — `BQ1-K3`, `BQ2-K2`, `BQ2-K3` — sono definiti sul profilo di mood e non esistono senza la tabella di corrispondenza generi → mood. Toglierla non alleggerisce il progetto: ne amputa metà del framework. Se serve tagliare, si taglia `009`.

4. **Il debito della 001 è distribuito, non accantonato.** Vedi la sezione seguente.

## Debito della feature 001

La [revisione in contesto pulito](../specs/001-business-case-kpi/review.md) ha prodotto 13 rilievi e 11 divergenze da chiarire. Tre rilievi sono già chiusi (commit `862bdca`). I restanti non diventano una feature dedicata: ciascuno è assegnato alla feature che ha comunque bisogno di quella decisione per procedere. Una decisione presa fuori dal contesto che la richiede è una decisione presa male.

| Voce | Contenuto | Chiusa da |
|---|---|---|
| R4 / div. 1 | definizione operativa di "segmento": genere della fonte o raggruppamento per mood | `005` |
| R7 / div. 7 | granularità di `BQ2-K2` e riformulazione di §5.2 | `005` |
| R8 | provenienza dei numeri sui dati citati nel business case | `002` |
| R11 | quali categorie video compongono `BQ1-K1` e se la selezione è una mappatura | `002` |
| R5, R6 / div. 2, 3, 4 | operatori indefiniti: intervallo occupato, metrica di distanza, pesi e commensurabilità; quadranti contro combinazione pesata | `007` |
| div. 6 | trattamento delle tracce a popolarità zero | `003` |
| div. 8 | segno della differenza e titoli privi di durata | `003` (dati) + `007` (segno) |
| div. 9 | dimensione della base utenti | `004` |
| div. 10 | governance della tabella generi → mood | `006` |
| div. 11 | posizione dell'alternativa "non entrare" | `010` |
| R13 | ambiguità minori sparse | `004`, `007` |
| R9, R10, R12 | correzioni terminologiche sul testo del business case | debito testuale, ~1 ora, da chiudere prima di `007` |
| div. 5 | soglie decisionali | ✅ chiusa dal commit `862bdca` (§3, condizioni C1-C3) |

### Nota su R11 — l'esito cambia il testo, non la North Star

Il rilievo chiedeva se la selezione delle categorie video che compongono `BQ1-K1` sia una mappatura interpretativa, nel qual caso la confidenza scenderebbe a media e la North Star andrebbe ridefinita.

Una ricognizione sulla fonte mostra che esiste **una sola categoria** a contenuto musicale dichiarato, `Music & Musicals`. Non c'è alcuna selezione da compiere fra più categorie, quindi non c'è mappatura e la **confidenza alta regge**: la North Star sopravvive.

Il rilievo si sposta però sul testo. §3 del business case descrive il contenuto misurato come "musical, documentari musicali, concerti, film sulla musica" — quattro tipologie — mentre la misura ne legge una sola etichetta. Concerti e documentari musicali sono catturati solo se la fonte li ha collocati lì, e il documento non può affermarlo. La descrizione va allineata a ciò che la misura fa davvero. Rientra nel debito testuale.

`002` formalizza il tutto con lo script che rigenera il conteggio: finché il numero non esce da un artefatto versionato, il principio II non è soddisfatto.

## Calendario previsto

| Finestra | Capacità | Contenuto atteso |
|---|---|---|
| 8 → 15 agosto | ~2 h/giorno, ~16 h | debito testuale 001, `002`, `003`, chore ambiente |
| dal 16 agosto | giornate piene, ~6 h/giorno | `004`, `005`, `006`, `007`, `008`, `010` |

Atterraggio stimato: **21-22 agosto**, con `009` escluso.

La stima iniziale di 7-10 giornate lavorative si conferma corretta come misura di sforzo: ~56 ore complessive sono 8-9 giornate piene. Non era sbagliata la stima, era sbagliato leggerla come giorni di calendario a capacità piena.

Il chore dell'ambiente è collocato nella finestra a bassa capacità di proposito: è lavoro a bassa intensità cognitiva — attese di download e di installazione — e sarebbe uno spreco consumarci una giornata piena. Va però completato entro il 15, perché `005` disegna il modello dati per lo strumento che lo ospiterà e conviene averlo visto funzionare prima.

## Rischi aperti

**Densità di `008`.** Otto ore per una sola feature sono il limite superiore del principio III, e la voce più esposta a scoprirsi più grande di così davanti allo schermo. Va scomposta in fase di `/speckit.specify` — presumibilmente struttura e pagine da una parte, storytelling e rifiniture dall'altra — non dopo averla aperta.

**Concentrazione del rischio dopo il 16 agosto.** Sei feature su otto cadono nella finestra a giornate piene, incluse le tre più dense. La finestra a bassa capacità non ha margine di recupero: se `002` o `003` sforano, lo scostamento si trasferisce intero sulla seconda finestra invece di essere assorbito.

**Nessuna verifica indipendente pianificata dopo la 001.** La revisione in contesto pulito che ha prodotto 13 rilievi sul business case è stata la fonte di gran parte del valore critico del progetto finora. Nessuna feature successiva ne prevede una. Da decidere in fase di spec dove reintrodurla — il candidato naturale è `007`, dove le decisioni di calcolo rinviate dalla 001 vengono finalmente prese.

## Rischi chiusi

**Ambiente Power BI** *(chiuso il 2026-08-08)*. Power BI Desktop non esiste per macOS. La macchina di sviluppo è però un Mac **Intel x86_64** con 16 GB di RAM e oltre 250 GB liberi: una VM Windows 11 x64 esegue Power BI Desktop in modo nativo, senza l'emulazione x64 che sarebbe stata necessaria su Apple Silicon. Il rischio si riduce al chore di predisposizione. Tableau Public resta il piano di riserva, non il percorso principale.

**Scadenza del trial Power BI Pro** *(chiuso il 2026-08-08)*. Impatto basso: il deliverable è un file `.pbix` e Power BI Desktop è gratuito e senza scadenza. Il trial abilita il Service — workspace, pubblicazione, condivisione — che non serve al deliverable dichiarato. Resta la sola azione opportunistica di pubblicare una versione di prova entro il 18, tracciata fra i chore.
