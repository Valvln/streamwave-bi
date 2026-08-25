# Streamwave BI

> 🚧 **Work in progress** — progetto di Business Intelligence sviluppato con approccio *spec-driven* ([GitHub Spec Kit](https://github.com/github/spec-kit)).

**StreamWave**, piattaforma di streaming video, valuta l'ingresso nel verticale del **music streaming**. Questo repository contiene l'analisi e la dashboard a supporto della decisione.

Tre domande di business guidano l'intero progetto:

- **BQ1 — Posizionamento**: come si posiziona il contenuto musicale rispetto a quello video per caratteristiche "vincenti" (durata, genere, mood)? C'è overlap di audience potenziale?
- **BQ2 — Segmento di ingresso**: quale segmento musicale è più coerente con il catalogo attuale?
- **BQ3 — Impatto stimato**: quale impatto su engagement e revenue, simulato con assunzioni dichiarate?

I principi non negoziabili del progetto — etichettatura di fonte e confidenza su ogni numero, riproducibilità totale, trasparenza sui limiti — sono in [`.specify/memory/constitution.md`](.specify/memory/constitution.md). Il metodo di lavoro che ne discende, incluso il modo in cui il lavoro è diviso fra sessioni di agent, è in [`CLAUDE.md`](CLAUDE.md); il piano e il suo scostamento in [`docs/roadmap.md`](docs/roadmap.md).

## Cosa questo progetto non è

È un **case study**: un esercizio di analisi costruito per essere verificabile, non un prodotto pronto a supportare una decisione di mercato reale. Nello specifico:

- **StreamWave non esiste.** È un'azienda inventata. Nessun dato reale di StreamWave è stato usato, perché non ce n'è.
- **Netflix e Spotify sono proxy, non StreamWave.** Il catalogo Netflix rappresenta il catalogo ipotetico di StreamWave, il dataset Spotify rappresenta il mercato musicale accessibile. È l'assunzione strutturale del case study: regge il ragionamento, non la realtà di un'azienda.
- **Le metriche di business sono sintetiche.** Nessun dato di visione, ascolto, abbonamento o ricavo reale esiste in questi dataset. Tutto ciò che riguarda engagement e revenue è generato da script con assunzioni dichiarate, ed è etichettato come tale in ogni artefatto.
- **Manca il lato costi.** Licenze musicali, infrastruttura, organico: nessuno di questi dati è disponibile. Quello che segue è un business case *di opportunità*, non un business case finanziario. Chi cercasse qui un ROI non lo troverà, ed è deliberato.
- **I dati reali si fermano al 2021-2022.** Il catalogo Netflix è aggiornato al 2021, le tracce Spotify al 2022. Nessuna conclusione di questo progetto può dire alcunché sulle dinamiche di mercato successive.

I limiti analitici specifici di ogni singola analisi — cosa quel particolare KPI non risponde, quali inferenze evitare — vivono nella sezione *Limiti Dichiarati* della spec di ciascuna feature sotto [`specs/`](specs/), come richiesto dal principio IV della constitution. Questa sezione inquadra il progetto; quelle inquadrano i singoli risultati.

## Stato

Governance: [`constitution`](.specify/memory/constitution.md) v1.2.0 · [metodo di lavoro](CLAUDE.md) · [roadmap e stime](docs/roadmap.md)

| Feature | Deliverable | Stato |
|---|---|---|
| `001` Business Case & KPI Framework | [`docs/business_case.md`](docs/business_case.md) | ✅ conclusa, [revisionata](specs/001-business-case-kpi/review.md) |
| `002` Data Audit & Profiling | [`docs/data_audit.md`](docs/data_audit.md) · [`reports/data_profile.json`](reports/data_profile.json) | ✅ conclusa, [revisionata](specs/002-data-audit-profiling/review.md) |
| `003` Data Cleaning & ETL | [`docs/data_cleaning.md`](docs/data_cleaning.md) · `scripts/build_datasets.py` · [`reports/cleaning_report.json`](reports/cleaning_report.json) | ✅ conclusa, [revisionata](specs/003-data-cleaning-etl/review.md) |
| `004` Synthetic Business Metrics | [`docs/bq3_scenarios.md`](docs/bq3_scenarios.md) · [`data/benchmarks/`](data/benchmarks/) · [`reports/bq3_scenarios.json`](reports/bq3_scenarios.json) | ✅ conclusa, [revisionata](specs/004-synthetic-business-metrics/review.md) |
| `005` Data Model Design | [`docs/data_model.md`](docs/data_model.md) | ✅ conclusa, [revisionata](specs/005-data-model-design/review.md) |
| `006` Content Taxonomy Bridge | [`docs/content_taxonomy_bridge.md`](docs/content_taxonomy_bridge.md) · [`docs/mood_assignment_criteria.md`](docs/mood_assignment_criteria.md) · [`data/curated/`](data/curated/) | ✅ conclusa, [revisionata](specs/006-content-taxonomy-bridge/review.md) |
| `007a` Operatori delle misure | [`docs/kpi_operators.md`](docs/kpi_operators.md) | ✅ conclusa, [revisionata](specs/007a-kpi-operators/review.md) |
| `007b` Misure dei KPI | [`docs/kpi_measures.md`](docs/kpi_measures.md) · `scripts/build_kpi_measures.py` · [`reports/kpi_measures.json`](reports/kpi_measures.json) · [`reports/kpi_engine_check.json`](reports/kpi_engine_check.json) | ✅ conclusa, [revisionata](specs/007b-kpi-measures/review.md) |
| `008a` Dashboard — modello e pagine | il `.pbix` **non versionato**, reso ispezionabile dal [contratto di pagina](specs/008a-dashboard-model-pages/contracts/page-contract.md) e dall'[esito della costruzione](specs/008a-dashboard-model-pages/quickstart.md) | 🚧 costruita, in revisione |

Le feature successive, le stime e il debito aperto sono in [`docs/roadmap.md`](docs/roadmap.md).

## Il business case

Il primo deliverable è **[`docs/business_case.md`](docs/business_case.md)**: il framework con cui il progetto risponderà alle tre domande. Definisce 8 KPI con formula concettuale, fonte e livello di confidenza, una North Star metric e il perimetro di ciò che l'analisi non proverà a dimostrare. Non contiene risultati: quelli arriveranno dalle feature successive, ciascuno con l'etichetta di affidabilità definita qui.

Il secondo è **[`docs/data_audit.md`](docs/data_audit.md)**: il profilo dei due dataset reali, con ciò che la loro forma vincola per le feature successive. Ogni numero che contiene è rigenerato da uno script e vive in [`reports/data_profile.json`](reports/data_profile.json), versionato perché sia verificabile anche da chi non ha i dati di origine.

Il terzo è **[`docs/data_cleaning.md`](docs/data_cleaning.md)**: la dichiarazione di ogni decisione presa sui dati per portarli allo stato in cui il modello li userà, con la ragione, l'effetto misurato in righe o valori, e i valori del profilo che dopo la trasformazione non valgono più. I dataset che ne escono **non sono versionati** — lo è la pipeline che li produce — quindi il documento e [`reports/cleaning_report.json`](reports/cleaning_report.json) sono ciò che li rende verificabili da chi non può rigenerarli.

Il quarto è **[`docs/bq3_scenarios.md`](docs/bq3_scenarios.md)**: i parametri di scenario della terza domanda di business, gli unici numeri del progetto che non descrivono un dato osservato. Il tasso su cui poggiano è un **benchmark pubblicato da un terzo**, congelato in [`data/benchmarks/`](data/benchmarks/) con la propria citazione e con lo scarto fra ciò che la fonte misura e ciò per cui viene usato; da lì una derivazione deterministica ricava i sei valori di [`reports/bq3_scenarios.json`](reports/bq3_scenarios.json). Il documento esiste per dichiarare quel passaggio, non per nasconderlo: ancorare un parametro a una fonte lo rende **verificabile, non vero per StreamWave**.

Il quinto è **[`docs/data_model.md`](docs/data_model.md)**: il modello dati su cui le misure verranno calcolate — quali tabelle esistono, che cosa è una riga di ciascuna, come sono collegate e da quale campo proviene ogni colonna. Esiste come documento e non come file di Power BI perché la constitution lo impone: schema e mapping dei campi sono artefatti testuali, non contenuto di un file binario. Chiude le due ambiguità che il business case aveva lasciato aperte — che cosa sia un «segmento», e quante nozioni di grana servano per descrivere un KPI — e dichiara ciò che il modello rende **impossibile** misurare, incluse le due tabelle che non esistono di proposito. Il modello è **progettato e non materializzato**: nessuna sua affermazione è stata verificata eseguendola.

Il sesto è **[`docs/content_taxonomy_bridge.md`](docs/content_taxonomy_bridge.md)**: la tabella che assegna a ciascuna categoria del catalogo video un profilo di mood su tre assi, e il documento che dichiara come è stata costruita. Sono gli **unici valori del progetto che nessuna fonte osserva e nessuna formula calcola**: sono assegnati. Il metodo è in quattro passi, e l'ordine è il presidio: il criterio di assegnazione ([`docs/mood_assignment_criteria.md`](docs/mood_assignment_criteria.md)) è scritto e committato **prima** che qualunque valore esista, un modello linguistico propone in una sola invocazione manuale, una seconda sessione di modello — non una persona, e il documento lo dichiara — verifica riga per riga contro quel criterio e nessun altro metro, e l'esito si congela in [`data/curated/`](data/curated/) con un numero di versione. Nessuno script chiama il modello, e il documento dichiara che cosa il processo **non** garantisce — a partire dal fatto che il criterio l'ha scritto la stessa persona che pubblica la tabella.

Il settimo è **[`docs/kpi_operators.md`](docs/kpi_operators.md)**: per ciascuno degli 8 KPI, l'operatore analitico con cui la misura verrà calcolata — formula, grana, tabelle da cui legge, confidenza ereditata, limiti dichiarati — e le nove decisioni analitiche che quelle regole hanno richiesto di prendere, ciascuna con l'opzione scartata e la ragione dello scarto. **Non contiene alcun valore dei KPI**: pubblica la regola, non il numero, e ogni cifra che vi compare è un input già ancorato da una feature precedente. Esiste come feature a sé perché un operatore sbagliato non produce un valore sbagliato — li produce tutti quelli che ne dipendono — e perché una formula scritta dentro una misura è contestabile solo da chi apre lo strumento di reporting, mentre una scritta qui lo è da chiunque legga il repository.

L'ottavo è **[`docs/kpi_measures.md`](docs/kpi_measures.md)**: il valore di ciascuno degli 8 KPI, la formula DAX con cui la misura si scrive nel modello, la provenienza di ogni numero e i limiti che quel numero porta con sé. È il primo documento del progetto in cui una cifra pubblicata è un **risultato** e non un input ereditato da una feature precedente. I valori non sono letti a schermo e ricopiati: li calcola `scripts/build_kpi_measures.py`, uno script deterministico che applica le stesse regole del modello dati e degli operatori sugli stessi dati, perché chi clona il repository senza una licenza Power BI possa comunque rigenerarli.

Che script e motore DAX diano lo stesso numero **non è assunto**: il confronto è stato eseguito a mano sul modello materializzato, e il suo esito è congelato in [`reports/kpi_engine_check.json`](reports/kpi_engine_check.json) — l'unico artefatto del progetto, insieme ai benchmark, che nessuno script scrive. È servito: al primo passaggio tre KPI su otto divergevano di due ordini di grandezza, per una tipizzazione sbagliata delle colonne decimali in fase di caricamento — un difetto che nessun controllo automatico di questo repository poteva vedere, perché il `.pbix` non è un artefatto versionato.

Il nono deliverable è il primo che **non è un documento**: la dashboard Power BI in cui gli 8 KPI vanno a schermo, su quattro pagine con la propria navigazione. Il `.pbix` **non è versionato** — incorpora i dati, che per scelta stanno fuori dal repository — quindi ciò che il repository contiene non è il file ma i due artefatti che lo rendono ispezionabile da chi non può aprirlo: il **[contratto di pagina](specs/008a-dashboard-model-pages/contracts/page-contract.md)**, che disegna ogni pagina prima che lo strumento venga aperto e motiva ogni visuale contro la forma del dato, e l'**[esito della costruzione](specs/008a-dashboard-model-pages/quickstart.md)**, che dichiara che cosa esiste davvero e in che cosa differisce dal disegno. L'ordine fra i due è il presidio, ed è lo stesso del ponte fra tassonomia e mood: il disegno si committa prima, e non può quindi ratificare ciò che è stato costruito.

Costruire ha prodotto tre difetti che nessun controllo del repository poteva vedere, tutti in impostazioni che vivono solo dentro il file binario: due sono stati corretti durante la costruzione, il terzo è la tipizzazione già nota alla `007b`. È la ragione dell'issue `#20` e il limite dichiarato di questo deliverable. **Il file è leggibile, non pubblicabile**: i limiti a schermo, in forma comprensibile a un lettore non tecnico, sono il deliverable della feature successiva.

I sette documenti che pubblicano misure — l'audit, il cleaning, gli scenari, il modello, il ponte fra tassonomia e mood, gli operatori e le misure — legano ogni numero all'artefatto che lo produce con la stessa grammatica, definita in **[`docs/convenzioni-marcatura.md`](docs/convenzioni-marcatura.md)** e verificata da `scripts/check_audit_coherence.py`. Lo stesso controllo presidia la tassonomia: se le categorie del catalogo video e quelle della tabella dei mood divergessero, **fallisce** invece di avvisare.

## Setup

```bash
# 1. Dati raw (non versionati — vedi data/README.md)
./scripts/download_data.sh

# 2. Profilo dei dataset di origine (richiede i dati raw del passo 1)
python3 scripts/profile_data.py

# 3. Pipeline di trasformazione: scrive i quattro dataset in data/processed/
#    e il rendiconto reports/cleaning_report.json (richiede i dati raw)
python3 scripts/build_datasets.py

# 4. Scenari BQ3 dal benchmark congelato (NON richiede i dati raw né rete)
python3 scripts/build_bq3_scenarios.py

# 5. Misure degli 8 KPI dai dataset trasformati (richiede data/processed/)
python3 scripts/build_kpi_measures.py

# 6. Coerenza fra i sette documenti pubblicati e i sei artefatti versionati,
#    più il presidio sulla tassonomia delle categorie (NON richiede i dati raw)
python3 scripts/check_audit_coherence.py
```

Nessuna dipendenza da installare: gli script usano la sola libreria standard di Python 3. Il passo 6 funziona su una copia del repository priva di `data/raw/`, perché confronta soltanto artefatti versionati — è il modo in cui chi non ha i dati di origine verifica che i numeri dei documenti non siano stati scritti a mano.

**Non esiste un passo che rigeneri i profili di mood**, e non è un'omissione: quei valori sono assegnati, non calcolati, e nessuno script li tocca dopo il congelamento.

**Non esiste nemmeno un passo che rigeneri la dashboard.** Il `.pbix` si costruisce a mano in Power BI Desktop a partire da `data/processed/`, ed è il confine dell'automazione che la constitution traccia. Le istruzioni sono il [contratto di pagina](specs/008a-dashboard-model-pages/contracts/page-contract.md); ciò che va riverificato a ogni riapertura del file — tipizzazione, lettura dei CSV, colonne di scenario — è elencato nell'[esito della costruzione](specs/008a-dashboard-model-pages/quickstart.md) e nell'issue `#20`.

## Struttura

```
.specify/       # Spec Kit: constitution, template, script
.claude/        # comandi /speckit.* per Claude Code
.github/        # prompt /speckit.* per GitHub Copilot
data/           # raw / interim / processed (gitignored) + benchmarks/ e curated/ (versionate: non riproducibili)
docs/           # i documenti pubblicati: business case, audit, cleaning, scenari, modello dati,
                #   criterio di mood, ponte tassonomia-mood, operatori delle misure,
                #   misure dei KPI, convenzioni, roadmap
reports/        # artefatti versionati: profilo, rendiconto delle trasformazioni, scenari BQ3 e
                #   misure dei KPI (generati) + esito del confronto col motore DAX (curato a mano)
scripts/        # utility riproducibili
specs/          # una cartella per feature: spec.md, plan.md, tasks.md, review.md,
                #   contracts/ dove la feature ne pubblica uno (007a, 007b, 008a)
```

## Dati

Due dataset pubblici Kaggle (Spotify tracks + catalogo Netflix). Provenienza e licenze: [`data/README.md`](data/README.md).

## Licenza

[MIT](LICENSE) — codice e documentazione. I dataset raw restano soggetti alle rispettive licenze d'origine (vedi [`data/README.md`](data/README.md)).
