# Implementation Plan: Data Cleaning & ETL

**Branch**: `003-data-cleaning-etl` | **Date**: 2026-08-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-data-cleaning-etl/spec.md`

## Summary

La feature produce **una pipeline** che porta i due dataset reali da `data/raw/` a quattro file trasformati, **un artefatto di rendicontazione versionato** che ne misura ogni decisione, e **un documento** che le dichiara. Un quarto pezzo — l'estensione del controllo di coerenza — è ciò che impedisce al documento di divergere dagli artefatti.

L'asimmetria che governa tutto il piano è questa: **i dati escono dal repository, i numeri che li descrivono no.** Gli output non sono versionati, quindi non esiste alcun modo di ispezionarli per chi non può rigenerarli. Ne discende la scelta strutturale della feature: `reports/cleaning_report.json` è l'artefatto che rende verificabile ciò che i dati non possono più testimoniare da soli, ed è il motivo per cui una feature di ETL produce un file JSON versionato accanto ai CSV che non lo sono.

Tre decisioni tecniche semplificano il resto. **Sola libreria standard e CSV in uscita** (T1): a queste dimensioni nulla richiede un dataframe, e il determinismo byte per byte di un CSV scritto con il modulo standard è dimostrabile, mentre quello di un Parquet dipende da versioni e metadati che nessuno decide. **I valori non trasformati viaggiano verbatim** (T2): un valore che nessuna decisione tocca non passa per una conversione e ritorno, il che elimina per costruzione la classe di differenze dovute alla rappresentazione dei decimali. **Il non-misurato si dichiara** (T9): invece di far indovinare al controllo se un numerale sia un fatto sui dati, lo si marca — ed è ciò che rende realizzabile dentro la stima il corollario (c) della decisione ereditata D5, che chiede al controllo di fallire e non di avvisare.

La Fase 0 ha inoltre trovato quattro cose che il piano ha dovuto accogliere: la grana coppia traccia-genere **non è unica** nella fonte, la deduplicazione a traccia **non è priva di perdita**, la separazione delle due durate video è **un'invariante e non un'euristica**, e la conversione di `date_added` è una **trappola di determinismo** che nessun test sulla macchina di sviluppo avrebbe scoperto.

## Technical Context

**Linguaggio/Versione**: Python 3 (verificato su 3.14.6). Nessuna funzionalità oltre a quelle disponibili da 3.8

**Dipendenze primarie**: nessuna. Solo libreria standard — `csv`, `json`, `hashlib`, `re`. Decisione T1 in [research.md](./research.md)

**Storage**: file. Ingresso `data/raw/*.csv` in sola lettura; uscita `data/processed/*.csv` **non versionati**, più `reports/cleaning_report.json` e `docs/data_cleaning.md`, entrambi versionati

**Testing**: verifica per esecuzione secondo [quickstart.md](./quickstart.md) — determinismo per doppia esecuzione e diff, impronte confrontate, grane verificate, controllo di coerenza con due prove di alterazione, prova di esecuzione senza `data/raw/`. Nessun framework di test introdotto, per la stessa ragione della 002: i comportamenti verificabili sono una decina e si verificano da riga di comando

**Piattaforma target**: qualunque sistema con Python 3. Sviluppo su macOS. **Vincolo aggiunto dalla Fase 0**: nessuna funzione dipendente dal locale entra nella pipeline (F6, T6)

**Tipo di progetto**: uno script di trasformazione da riga di comando, un controllo esteso, un documento. Nessuna applicazione, nessun servizio

**Obiettivi di performance**: nessuno vincolante. 122.807 righe si trasformano in pochi secondi con la libreria standard

**Vincoli**: `data/raw/` immutabile (principio II, FR-002); output identici byte per byte fra due esecuzioni (FR-003); output **non** versionati e artefatto di rendicontazione versionato (FR-007, FR-025); controllo eseguibile senza i dati di origine (FR-041); nessun KPI e nessuna misura di posizione della popolarità per genere (FR-044); ~7 ore di lavoro effettivo, revisione inclusa (principio III)

**Scala/Ambito**: 2 sorgenti, 4 output, 33 campi di origine, 9 decisioni di trattamento di cui 5 ereditate, 42 categorie video, 114 generi musicali, 15 criteri di successo

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni valore dichiara fonte e confidenza | ✅ tabella compilata nella spec: 6 famiglie, 4 ad alta e 2 a media con la ragione della distinzione | ✅ la provenienza diventa meccanica: `sources` confrontato con quello del profilo (T10), e `denominators` rende esplicito ogni valore che cambia |
| **II. Riproducibilità** | ogni trasformazione è codice versionato; `data/raw/` intatto | ✅ è il principio che la feature esiste per applicare ai dati | ⚠️ **regge, ma con una tensione da dichiarare** — vedi sotto |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ stima 7 ore, al limite superiore di 6-7 | ⚠️ regge, margine nullo — vedi "Budget e rischio" |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde | ✅ 12 voci in "Limiti Dichiarati", 4 inferenze da evitare | ✅ F3 dà sostanza a un limite che era teorico: la deduplicazione non è priva di perdita, e ora se ne conosce l'entità |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ nessuna GUI coinvolta | ✅ invariato |
| **VI. Coerenza Narrativa** | riconducibile alle domande di business | ✅ feature strumentale: serve BQ1 e BQ2, non BQ3 | ✅ invariato. Il contributo passa dai dataset, non da un'affermazione |

**Esito**: nessuna violazione. La tabella "Complexity Tracking" resta vuota. Due punti di attenzione, entrambi dichiarati e nessuno dei due risolvibile tagliando requisiti.

**La tensione sul principio II.** Il principio chiede che «chiunque cloni il repository DEVA poter rigenerare ogni dataset intermedio e finale partendo solo dal codice versionato e dai dataset pubblici di origine». La feature lo soddisfa alla lettera: la pipeline è versionata e deterministica. Ma i dataset pubblici di origine richiedono un token Kaggle, quindi «chiunque» è in pratica «chiunque abbia un account». Per gli altri, gli output non esistono e la verifica passa interamente da tre artefatti versionati — pipeline, `cleaning_report.json`, documento. Non è una violazione: è il perimetro reale del principio, che la 002 aveva già incontrato e risolto versionando il profilo. Questa feature applica lo stesso rimedio, ed è la ragione per cui `cleaning_report.json` esiste. Il limite resta e va scritto nel documento (spec, "Limiti Dichiarati"), non attenuato.

## Project Structure

### Documentation (this feature)

```text
specs/003-data-cleaning-etl/
├── spec.md                       # specifica approvata, con le 5 decisioni ereditate chiuse
├── plan.md                       # questo file
├── research.md                   # Fase 0: ritrovamenti F1-F8, decisioni tecniche T1-T11
├── data-model.md                 # Fase 1: 7 entità della trasformazione e vincoli
├── quickstart.md                 # Fase 1: come eseguire e come verificare ciascun SC
├── contracts/
│   └── output-datasets.md        # Fase 1: schema dei 4 output, cleaning_report, marcatura
├── checklists/
│   └── requirements.md           # checklist di qualità della spec (16/16 + gate)
└── tasks.md                      # output di /speckit.tasks — non creato qui
```

La cartella `contracts/` esiste per la stessa ragione della 002, più una nuova: qui il contratto descrive artefatti che **non sono nel repository**. Per la feature 005, che disegnerà il modello dati, `contracts/output-datasets.md` è l'unico modo di sapere che forma hanno i dati senza possederli.

### Artefatti nel repository

```text
scripts/
├── download_data.sh              # esistente
├── profile_data.py               # esistente
├── check_audit_coherence.py      # esteso: secondo documento, secondo artefatto, severità per documento
└── build_datasets.py             # nuovo: la pipeline di trasformazione

reports/
├── data_profile.json             # esistente — letto, mai scritto
└── cleaning_report.json          # nuovo: artefatto di rendicontazione, versionato

docs/
├── business_case.md              # esistente — riceve la nota in loco di FR-035
├── data_audit.md                 # esistente — riceve la nota in loco di FR-036
└── data_cleaning.md              # nuovo: il documento delle trasformazioni

data/processed/                   # NON versionato — 4 CSV prodotti dalla pipeline
```

**Structure Decision**: nessuna cartella `src/`, nessuna `tests/`. La 002 aveva rimandato la scelta di un albero di pacchetto a «quando ci sarà codice sufficiente a giustificarla»; con `build_datasets.py` il repository arriva a tre script e circa milletrecento righe complessive, che è ancora sotto la soglia in cui un pacchetto ripaga il proprio costo. La decisione si ripropone alla 005, che introdurrà codice di modellazione.

`data/interim/` **non viene usata**. La pipeline è un passaggio solo: introdurre uno stadio intermedio produrrebbe file che nessuno legge, e la spec lo dichiara già fra le assunzioni.

## Fase 0 — Outline & Research

**Completata**. Output: [research.md](./research.md).

Otto ritrovamenti sui dati reali (F1-F8) e undici decisioni tecniche (T1-T11). In sintesi, cosa hanno cambiato:

- **F1**: la corrispondenza fra le tre righe senza durata e le tre con classificazione fuori dominio è **totale in entrambe le direzioni**. La riparazione della decisione ereditata D2 ha un raggio d'azione dichiarabile e verificabile
- **F2**: la grana coppia traccia-genere **non è unica**: 444 coppie ripetute, 450 righe eccedenti, repliche identiche su ogni attributo. Ritrovamento nuovo, che aggiunge una decisione di trattamento non prevista dalla spec — e priva di perdita
- **F3**: la deduplicazione a traccia **non** è priva di perdita: 720 tracce con repliche discordi, e discordi **solo** su `popularity`. Mediana dello scarto 1 punto, massimo 44
- **F4**: le quote di zeri per genere cambiano su 48 generi dopo F2, ma **l'insieme selezionato dal criterio di D4 è identico** prima e dopo. Il genere più vicino alla soglia dista 1,55 punti — meno knife-edge del 60% che la revisione ha scartato
- **F5**: la separazione delle due durate video è un'invariante verificabile, non un'euristica
- **F6**: `date_added` ha 88 valori con spazio iniziale e mesi in inglese, e `strptime` con `%B` **dipende dal locale**: la conversione ovvia produrrebbe risultati diversi su macchine diverse
- **T2**: i valori non trasformati viaggiano verbatim; i tipi sono dichiarati nel contratto e **validati**
- **T5**: nelle repliche discordi si conserva la popolarità **massima**, con la distorsione verso l'alto dichiarata
- **T9**: il non-misurato si marca, invece di essere indovinato dal controllo
- **T10**: sette invarianti verificate a ogni esecuzione, non assunte

## Fase 1 — Design & Contracts

**Completata**. Output: [data-model.md](./data-model.md), [contracts/output-datasets.md](./contracts/output-datasets.md), [quickstart.md](./quickstart.md).

`data-model.md` descrive le sette entità della trasformazione — sorgente, decisione di trattamento, output di dati, valore di rendicontazione, denominatore cambiato, affermazione derivata, numerale non misurato — e i vincoli che le tengono insieme. Il vincolo che porta più peso è quello sui **denominatori cambiati**: la relazione è completa in una direzione, e la completezza è ottenuta per **ricalcolo e confronto** invece che per memoria di chi scrive. È la differenza fra una promessa e una proprietà dell'esecuzione.

`contracts/output-datasets.md` fissa la grana, la chiave e i tipi dei quattro output, lo schema di `cleaning_report.json` con il blocco `denominators`, e la quarta forma della marcatura — il marcatore di non-misurato — con la tabella di severità che distingue il documento della 002 da quello della 003.

`quickstart.md` mappa ciascuno dei quindici criteri di successo su un comando eseguibile o, per i due che non ne ammettono uno, sulla lettura che li verifica. Dichiara inoltre il caso che SC-001 **non** copre: due esecuzioni sulla stessa macchina condividono il locale, quindi il test del determinismo non vedrebbe mai F6.

## Budget e rischio

Ripartizione della stima di 7 ore:

| Blocco | Ore | Nota |
|---|---|---|
| pipeline di trasformazione | ~2,5 | il grosso: due sorgenti, quattro output, nove decisioni, sette invarianti, scrittura deterministica |
| artefatto di rendicontazione | ~0,5 | riusa lo schema del profilo (T8); il pezzo nuovo è `denominators` per ricalcolo |
| estensione del controllo di coerenza | ~0,75 | quarta forma di marcatura, secondo artefatto, severità per documento |
| documento delle trasformazioni | ~1,75 | prosa in italiano, nove decisioni, cinque ereditate, marcatura di ogni numerale |
| note in loco su artefatti mergiati | ~0,25 | FR-035 e FR-036 |
| revisione in contesto pulito e chiusura dei rilievi | ~1,0 | prassi dalla roadmap, dentro la stima da questa feature |

**Il rischio dichiarato nella spec si è ridotto.** La spec indicava il corollario (c) di D5 come il pezzo esposto a gonfiarsi, perché «riconoscere un numerale in posizione di fatto misurato» richiede di interpretare la prosa. La decisione T9 elimina il problema invece di risolverlo: l'onere passa a chi scrive, che sa in un istante ciò che nessuna euristica distingue. Il ripiego dichiarato nella spec — elenco esplicito delle forme ammesse — non serve più.

**Il rischio si è spostato sul documento.** T9 rende il controllo facile e la scrittura più lenta: ogni numerale del documento richiede una decisione consapevole. Su un testo di quella lunghezza sono qualche centinaio di micro-decisioni, ed è la ragione per cui il blocco del documento è stimato a 1,75 ore invece che a 1,5.

**Il margine sul principio III è nullo.** Sette ore su un limite di sei-sette, con la revisione dentro. La Fase 0 ha inoltre aggiunto una decisione di trattamento che la spec non prevedeva (F2). Non si tratta di un allargamento di perimetro — quella decisione era già implicita in FR-011, che chiede la verifica della grana — ma di lavoro che prima non era contato.

**Se il lavoro sfora, cosa cade e cosa no.** Cade per primo il dettaglio per genere in `cleaning_report.json`: le quote ricalcolate dei 114 generi si riducono ai sette selezionati più i due limitrofi, che è ciò di cui il documento ha bisogno. Cade per secondo la colonna `is_duration_zero`, che marca **una** riga e il cui conteggio basta. **Non cadono** in nessun caso il determinismo, il blocco `denominators`, la severità del controllo sul nuovo documento e le cinque decisioni ereditate: sono i quattro punti per cui la feature esiste, e i primi tre sono anche quelli che nessuna feature successiva potrebbe aggiungere a posteriori senza rifare il lavoro.

**Il punto di stop.** La sessione dell'11 agosto si chiude sui task. L'implementazione cade nella finestra del 15 agosto o oltre, con tre giorni non pianificati in mezzo: è la ragione per cui il piano lascia in `research.md` e in `contracts/` tutto ciò che serve a riprendere senza ricostruire il contesto — inclusi i numeri della ricognizione, che altrimenti andrebbero riverificati da capo.

## Complexity Tracking

Nessuna violazione della constitution da giustificare.
