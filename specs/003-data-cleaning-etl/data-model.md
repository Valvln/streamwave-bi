# Data Model — Feature 003: Data Cleaning & ETL

**Data**: 2026-08-11 | **Fase**: 1 (Design) | **Spec**: [spec.md](./spec.md)

Descrive le entità con cui la feature lavora e i vincoli che le tengono insieme. **Non** è il modello dati del progetto: quello è della feature 005 (FR-046). Qui il soggetto è la trasformazione, non lo schema che la consumerà.

La distinzione conta perché le due cose si assomigliano e verrebbero confuse volentieri: `netflix_title_category.csv` ha la forma di una tabella ponte e non lo è ancora, perché nessuno ha deciso se il modello sarà a stella, se `category` sarà una dimensione, e con quale chiave. Questa feature produce dati normalizzati per forma; la 005 decide che ruolo abbiano.

## Le entità

### 1. Sorgente

Un file di `data/raw/`. Immutabile per il principio II.

| Attributo | Ruolo |
|---|---|
| percorso, dimensione, `sha256` | identità del contenuto |
| impronta registrata nel profilo | termine di confronto |

**Vincolo di integrità**: la pipeline confronta l'impronta letta con quella in `sources` di `reports/data_profile.json` e segnala in modo esplicito se non coincidono (T10). Non è un blocco pedante: se le impronte divergono, ogni identificativo del profilo che il documento cita descrive altri dati, e l'intero impianto di tracciabilità dice il falso senza accorgersene.

### 2. Decisione di trattamento

L'entità centrale della feature. Una scelta applicata ai dati, di cui esistono tre manifestazioni separate che devono corrispondere.

| Attributo | Dove vive |
|---|---|
| enunciato e ragione | `docs/data_cleaning.md` |
| identificativo del profilo che la motiva | ancora nel documento, risolta su `data_profile.json` |
| effetto quantificato | `reports/cleaning_report.json`, blocco `values` |
| marcatura dell'esito sui dati | colonna booleana nell'output, dove pertinente |
| regola meccanica | `scripts/build_datasets.py` |

**Vincolo**: una decisione senza effetto quantificato non è dichiarata (FR-029). In pratica: ogni decisione di trattamento ha **almeno un** identificativo `CL.` che ne misura la portata, e il documento lo cita. Una decisione che tocca zero righe è una decisione che va dichiarata con il suo zero, non omessa — perché il lettore non può distinguere «non è stato necessario» da «non è stato fatto».

**Le decisioni attese**, dalla Fase 0. Nove, di cui cinque ereditate e quattro emerse dalla ricognizione:

| # | Decisione | Origine | Marcatura sui dati |
|---|---|---|---|
| 1 | popolarità zero conservata e marcata | ereditata D1 | `is_popularity_zero` |
| 2 | riparazione dello scivolamento di colonna | ereditata D2 | `is_repaired_duration` |
| 3 | classificazione fuori dominio posta a mancante | ereditata D2, seconda mossa | — (conteggio) |
| 4 | totali di catalogo sulla grana traccia | ereditata D3 | — (regola di lettura) |
| 5 | soglia dei generi a forte concentrazione di zeri | ereditata D4 | `is_high_zero_genre` |
| 6 | deduplicazione della grana coppia | F2 | — (conteggio) |
| 7 | scelta della popolarità nelle repliche discordi | F3, T5 | `has_conflicting_popularity` |
| 8 | conversione di `date_added` in ISO | F6, T6 | — (conteggio) |
| 9 | normalizzazione del solo campo delle categorie | F7, T7 | — (esclusione dichiarata) |

La decisione ereditata D5 non compare: non è una decisione sui dati ma sulla scrittura, e la sua manifestazione è la marcatura del documento e la severità del controllo.

### 3. Output di dati

Un dataset trasformato. Quattro istanze, descritte in [contracts/output-datasets.md](./contracts/output-datasets.md) §1.

| Attributo | Ruolo |
|---|---|
| grana dichiarata | che cosa è una riga |
| chiave | i campi su cui la grana è unica |
| campi con tipo dichiarato | il contratto verso la 005 |
| righe, colonne, byte, `sha256` | registrati in `outputs` di `cleaning_report.json` |

**Vincolo di grana** (FR-011): la pipeline verifica che la chiave dichiarata sia effettivamente unica e si ferma se non lo è. È il vincolo che ha fatto emergere F2: sulla grana coppia traccia-genere la verifica sarebbe fallita, e la deduplicazione esiste perché passi.

**Vincolo di non-versionatura** (FR-007): nessun output è tracciato da git. La verifica è meccanica su `git status` dopo un'esecuzione.

### 4. Valore di rendicontazione

Un numero prodotto dalla trasformazione. Stessa forma del valore di profilo della 002 — `value`, `display`, `unit`, `label` — con prefisso `CL.`.

**Vincolo di stabilità**: l'identificativo non cambia quando cambia il valore. È ciò che permette a un diff di mostrare che un numero si è mosso invece di mostrare che una chiave è sparita.

**Vincolo di disgiunzione** (T8): nessun identificativo `CL.` collide con uno del profilo. La pipeline lo verifica invece di assumerlo, perché la risoluzione del controllo di coerenza avviene su uno spazio di nomi unito.

### 5. Denominatore cambiato

Uno scarto fra un valore del profilo e il suo corrispondente dopo la trasformazione. Vive nel blocco `denominators` di `cleaning_report.json` (contratto §2.3).

| Attributo | Ruolo |
|---|---|
| identificativo del profilo | il valore che **non vale più** sul dato trasformato |
| identificativo di rendicontazione | quello che lo sostituisce |
| ragione | perché differiscono, in una frase |
| ambito | su quale output vale il valore nuovo |

**Vincolo**: la relazione è **completa in una direzione**. Ogni valore del profilo che cambia ha una voce; un valore del profilo assente da `denominators` è, per definizione, un valore che la trasformazione non tocca. È l'asserzione che dà valore al blocco, ed è anche la più facile da violare per omissione: un denominatore cambiato e non registrato è indistinguibile da uno invariato.

**Contromisura**: le famiglie di valori esposte al cambiamento sono note dalla Fase 0 — durate dei film, completezza della classificazione, righe del catalogo musicale, quote di zeri per genere. La pipeline **ricalcola** i corrispondenti valori del profilo sul dato trasformato e confronta, invece di affidarsi alla memoria di chi scrive. Ciò che coincide non entra in `denominators`; ciò che differisce ci entra automaticamente. La completezza diventa così una proprietà dell'esecuzione e non una promessa.

### 6. Affermazione derivata

Un confronto, una graduatoria, un rapporto o una differenza costruiti su valori misurati. Per la decisione ereditata D5 è essa stessa un valore.

| Attributo | Ruolo |
|---|---|
| enunciato | la frase del documento |
| identificativo | il valore che la sostiene, in `data_profile.json` o `cleaning_report.json` |

**Vincolo**: non esiste l'affermazione derivata senza identificativo. Se il documento vuole dire che un genere è il più esposto agli zeri, quel primato è un valore calcolato dalla pipeline; se non lo è, la frase non si scrive. In pratica questo obbliga a decidere **prima** quali affermazioni derivate il documento farà, perché ciascuna diventa un requisito sulla pipeline.

### 7. Numerale non misurato

Un gruppo di cifre o un numerale in lettere che compare nel documento e **non** è un fatto sui dati: un conteggio di sezioni, un riferimento a una feature, una data, un'enumerazione retorica.

**Vincolo**: porta il marcatore `<!--#-->` (contratto §3.1). Non esiste una terza categoria: nel nuovo documento un numerale è ancorato oppure è dichiarato non misurato, e qualunque altra cosa fa fallire il controllo.

## Le relazioni che contano

```text
Sorgente ──impronta verificata──> reports/data_profile.json (002)
    │
    └──letta da──> Pipeline ──applica──> Decisione di trattamento
                      │                        │
                      │                        ├──marca──> colonna booleana nell'Output
                      │                        └──misura──> Valore di rendicontazione
                      │
                      ├──produce──> Output di dati (4, non versionati)
                      │                 └──impronta registrata in──> outputs
                      │
                      └──produce──> reports/cleaning_report.json (versionato)
                                        │
                                        ├── values ────────┐
                                        ├── denominators ──┤
                                        └── catalogs ──────┤
                                                           ↓
                    docs/data_cleaning.md ──ancore──> spazio di nomi unito
                                    ↑                        │
                                    └──verificato da── Controllo di coerenza
                                                    (non richiede data/raw/)
```

Il punto della figura è la parte in basso: il documento non tocca mai i dati e non tocca mai la pipeline. Cita due artefatti versionati, ed è per questo che un controllo può verificarlo su una macchina che i dati non li ha mai visti.

## Transizioni di stato

Nessuna entità ha stato mutevole. La pipeline è una funzione: stessi ingressi, stesse uscite (FR-003). L'unica transizione del sistema è fra due esecuzioni, e il modo di osservarla è il confronto delle impronte in `outputs` fra due versioni di `cleaning_report.json` — che essendo versionato rende visibile in un diff che un dato è cambiato, anche se il dato non è nel repository.

È l'unica cosa che la non-versionatura degli output non porta via: **il fatto che siano cambiati resta tracciato**, anche quando il loro contenuto no.
