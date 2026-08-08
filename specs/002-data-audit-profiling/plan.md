# Implementation Plan: Data Audit & Profiling

**Branch**: `002-data-audit-profiling` | **Date**: 2026-08-08 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-data-audit-profiling/spec.md`

## Summary

La feature produce tre artefatti nel repository e un contratto che li tiene insieme: uno **script di profiling** che legge `data/raw/` in sola lettura, un **artefatto JSON di soli numeri** versionato sotto `reports/`, e un **documento di audit** in italiano che cita quei numeri senza possederli. Un quarto artefatto — il **controllo di coerenza** — è ciò che impedisce ai primi due di divergere in silenzio.

L'approccio emerso dalla Fase 0 poggia su due decisioni che semplificano tutto il resto. Primo, **sola libreria standard**: a 8.807 e 114.000 righe non c'è nulla che un dataframe risolva, mentre la promessa "clona ed esegui" vale solo se non c'è nulla da installare, e il determinismo richiesto da FR-003 è dimostrabile con `statistics` e una regola di arrotondamento dichiarata mentre con pandas sarebbe soltanto sperato. Secondo, **ogni valore porta con sé la stringa esatta con cui va scritto**: il controllo di coerenza confronta due stringhe identiche invece di interpretare la formattazione italiana dei numeri, e la fragilità che FR-025 vieta non entra mai nel sistema.

La ricognizione di Fase 0 ha inoltre già trovato tre cose che il piano deve saper accogliere: R11 ha una risposta (**una sola** categoria musicale, quindi la North Star regge), l'affermazione "sovrastima di circa un quinto" della 001 è **sotto-determinata** e non semplicemente giusta o sbagliata, e il conteggio delle corrispondenze lessicali **cambia con la regola di confronto**. Le ultime due sono i primi ingressi del registro delle divergenze.

## Technical Context

**Linguaggio/Versione**: Python 3 (verificato su 3.14.6). Nessuna funzionalità oltre a quelle disponibili da 3.8

**Dipendenze primarie**: nessuna. Solo libreria standard — `csv`, `statistics`, `hashlib`, `json`, `re`. Decisione D1 in [research.md](./research.md)

**Storage**: file. Ingresso `data/raw/*.csv` in sola lettura; uscita `reports/data_profile.json` e `docs/data_audit.md`, entrambi versionati

**Testing**: verifica per esecuzione secondo [quickstart.md](./quickstart.md) — determinismo per doppia esecuzione e diff, controllo di coerenza con prova di alterazione, prova di esecuzione senza `data/raw/`. Nessun framework di test introdotto: la feature ha quattro comportamenti verificabili da riga di comando e un framework sarebbe più grande di ciò che verifica

**Piattaforma target**: qualunque sistema con Python 3. Sviluppo su macOS

**Tipo di progetto**: due script da riga di comando più un documento. Nessuna applicazione, nessun servizio

**Obiettivi di performance**: nessuno vincolante. 122.807 righe complessive si profilano in pochi secondi con la libreria standard

**Vincoli**: `data/raw/` immutabile (principio II, FR-002); artefatto identico byte per byte fra due esecuzioni (FR-003); artefatto non intercettabile da `.gitignore` (FR-007); controllo di coerenza eseguibile senza i dati di origine (FR-036); nessun KPI calcolato (FR-039); ~4 ore di lavoro effettivo (principio III)

**Scala/Ambito**: 2 dataset, 33 campi complessivi, 42 categorie video, 114 generi musicali, 14 affermazioni della 001 da rigenerare, 8 misure del framework da verificare in copertura

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni valore dichiara fonte e confidenza | ✅ tabella compilata nella spec: 8 famiglie, tutte a confidenza alta per il criterio D5 della 001 | ✅ la provenienza diventa meccanica: `sources` registra impronta e dimensione dei file di origine (FR-005) |
| **II. Riproducibilità** | ogni trasformazione è codice versionato; `data/raw/` intatto | ✅ è il principio che la feature esiste per soddisfare (rilievo R8) | ✅ D1 elimina anche la dipendenza da un ambiente da ricostruire; SC-002 verifica l'immutabilità delle sorgenti |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ stima ~4 ore, entro il limite di 6-7 | ⚠️ regge, ma il margine è più stretto di quanto la roadmap prevedesse — vedi "Budget e rischio" |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde | ✅ 10 voci in "Limiti Dichiarati", 3 inferenze da evitare | ✅ F4 dà sostanza a un limite che era teorico: tre campi valorizzati al 100% e sbagliati |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ nessuna GUI coinvolta | ✅ invariato |
| **VI. Coerenza Narrativa** | riconducibile alle domande di business | ✅ feature fondativa e strumentale: serve tutte e tre | ✅ F1 tocca direttamente la confidenza della North Star di BQ1 |

**Esito**: nessuna violazione, prima e dopo il design. La tabella "Complexity Tracking" resta vuota.

Un punto di attenzione sul principio III, non una violazione: la stima resta dentro il limite, ma la Fase 0 ha allargato il perimetro reale del profilo (F5: dodici campi invece di nove, più una colonna senza nome) e ha aggiunto due divergenze da istruire (F2, F3). Il margine si è ridotto. La contromisura è dichiarata sotto e non consiste nel tagliare requisiti.

## Project Structure

### Documentation (this feature)

```text
specs/002-data-audit-profiling/
├── spec.md                      # specifica approvata
├── plan.md                      # questo file
├── research.md                  # Fase 0: ritrovamenti F1-F6, decisioni D1-D9
├── data-model.md                # Fase 1: entità del profiling e vincoli di integrità
├── quickstart.md                # Fase 1: come eseguire e come verificare ogni SC
├── contracts/
│   └── profile-artifact.md      # Fase 1: schema dell'artefatto e grammatica della marcatura
├── checklists/
│   └── requirements.md          # checklist di qualità della spec (16/16 + gate)
└── tasks.md                     # output di /speckit.tasks — non creato qui
```

A differenza della 001, questa feature **produce** una cartella `contracts/`. La ragione è argomentata in D7: qui il consumatore del contratto è una persona che scrive marcatori a mano, che ha bisogno di un riferimento diverso dal codice sorgente, e la divergenza fra contratto e implementazione è impedita meccanicamente dal controllo di coerenza — la garanzia che alla 001 mancava.

### Artefatti nel repository

```text
scripts/
├── download_data.sh             # già presente
├── profile_data.py              # nuovo: profiling deterministico di data/raw/
└── check_audit_coherence.py     # nuovo: controllo documento ↔ artefatto

reports/
└── data_profile.json            # nuovo: artefatto di soli numeri, versionato

docs/
├── business_case.md             # esistente — riceve le note di correzione di FR-031
└── data_audit.md                # nuovo: il documento di audit
```

**Structure Decision**: nessuna cartella `src/` e nessuna `tests/`. Due script da riga di comando in `scripts/`, accanto a quello che già c'è, sono la forma proporzionata al problema; introdurre ora un albero di pacchetto anticiperebbe una struttura che la feature 003 potrà scegliere quando avrà codice sufficiente a giustificarla. `reports/` viene creata da questa feature ed è già prevista da `.gitignore`, che ne esclude solo le figure PNG.

## Fase 0 — Outline & Research

**Completata**. Output: [research.md](./research.md).

Sei ritrovamenti sui dati reali (F1-F6) e nove decisioni tecniche (D1-D9). In sintesi, cosa hanno cambiato:

- **F1**: il catalogo video ha **una sola** categoria a contenuto musicale dichiarato. R11 si chiude come la roadmap anticipava: nessuna mappatura, confidenza alta di `BQ1-K1` confermata. Resta da produrre il numero, non da asserirlo
- **F2**: "sovrastima di circa un quinto" ammette due letture aritmetiche che danno ≈21% e ≈27%. L'artefatto espone entrambe; è una divergenza di stato `ambiguo`
- **F3**: le corrispondenze lessicali fra i nomi di genere sono 6 o 4 a seconda della regola di confronto. Il valore non esiste senza la sua regola
- **F4**: tre righe hanno una durata nel campo della classificazione per età. "18 valori distinti" è vero come cardinalità e fuorviante come dominio
- **F5**: la 001 profilava 9 campi su 12, e il catalogo musicale ha una prima colonna priva di nome
- **D1**: sola libreria standard, nessun ambiente virtuale
- **D3**: ogni valore porta la stringa esatta con cui va scritto, e il controllo confronta stringhe
- **D6**: le affermazioni della 001 sono codificate e confrontate dallo script, non a occhio
- **D8**: il divieto di valori non marcati è presidiato da un avviso, non da un errore — con il limite dichiarato apertamente

## Fase 1 — Design & Contracts

**Completata**. Output: [data-model.md](./data-model.md), [contracts/profile-artifact.md](./contracts/profile-artifact.md), [quickstart.md](./quickstart.md).

`data-model.md` descrive le sei entità del profiling — sorgente, campo, valore di profilo, categoria del catalogo video, ritrovamento, affermazione della 001 e divergenza — con i vincoli che le tengono insieme: stabilità e univocità degli identificativi, completezza obbligatoria del censimento delle categorie, esistenza di uno stato `ambiguo` per le divergenze sotto-determinate.

`contracts/profile-artifact.md` fissa le tre cose su cui script, autore e controllo devono essere d'accordo: la convenzione di denominazione degli identificativi, la forma del record di valore, la grammatica della marcatura `valore<!--@ID-->`.

`quickstart.md` mappa ciascuno dei dodici criteri di successo su un comando eseguibile o, per i tre che non ne ammettono uno, sulla lettura che li verifica.

## Budget e rischio

Ripartizione della stima di ~4 ore:

| Blocco | Ore | Nota |
|---|---|---|
| script di profiling | ~1,75 | il grosso: profilazione generica dei campi, statistiche, formattazione, impronte, serializzazione deterministica |
| confronto con le affermazioni della 001 | ~0,25 | quattordici voci codificate più il blocco delle divergenze |
| controllo di coerenza | ~0,5 | ridotto da D3 e D4: due confronti di stringhe e un avviso |
| documento di audit | ~1,5 | prosa in italiano, marcatura, copertura delle otto misure, sezione divergenze |

**Il rischio dichiarato nella spec si è ridotto ma spostato.** Il controllo di coerenza non è più il pezzo esposto: le decisioni D3 e D4 lo hanno portato a due confronti di stringhe. Il blocco che oggi può sforare è lo **script di profiling**, perché F5 lo allarga a dodici campi invece dei nove che la 001 aveva profilato, e perché i casi particolari trovati in Fase 0 — colonna senza nome, campo multi-valore, valori fuori dominio — vanno gestiti ognuno esplicitamente.

**Se il lavoro sfora, cosa cade e cosa no.** Cade per primo l'avviso sui gruppi di cifre non marcati (D8), che è un ausilio alla revisione e non un requisito: FR-033-FR-036 restano soddisfatti senza. Cade per secondo il dettaglio per genere della concentrazione degli zeri, riducendolo ai generi che la 001 cita invece che a tutti e 114. **Non cadono** in nessun caso il determinismo, il censimento completo delle categorie, il registro delle divergenze e la marcatura: sono i quattro punti per cui la feature esiste.

## Complexity Tracking

Nessuna violazione della constitution da giustificare.
