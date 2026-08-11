# Contratto — dataset di output, `reports/cleaning_report.json` e marcatura del non-misurato

**Feature**: 003 Data Cleaning & ETL | **Data**: 2026-08-11

Questo file fissa l'interfaccia fra quattro cose che vivono separate: la **pipeline** che produce i dataset, la **feature 005** che ne disegnerà il modello dati senza riaprire questo codice, la **persona** che scrive il documento delle trasformazioni a mano, e il **controllo di coerenza** che verifica che le ultime due siano d'accordo.

Estende il contratto della 002, [`specs/002-data-audit-profiling/contracts/profile-artifact.md`](../../002-data-audit-profiling/contracts/profile-artifact.md), e non lo sostituisce. Le sezioni 1-5 di quel file restano vere: identificativi, forma del record di valore, regole di serializzazione e grammatica della marcatura si applicano identiche qui. Ciò che segue aggiunge, non riscrive.

**Vincolo che vale su tutto il documento**: i dataset di output **non sono versionati**. Questo contratto è, insieme alla pipeline e al documento, ciò che li rende verificabili da chi non può rigenerarli. Se il contratto e la pipeline divergono, è il contratto a essere sbagliato — ma nessuno se ne accorge leggendo i dati, perché i dati non ci sono. È la ragione della sezione 4.

## 1. I quattro dataset di output

Tutti sotto `data/processed/`, tutti CSV, tutti esclusi da git dal blanket su `*.csv` (decisione T1 di [research.md](../research.md)).

| File | Grana — cosa è una riga | Chiave | Origine |
|---|---|---|---|
| `netflix_titles.csv` | un titolo del catalogo video | `show_id` | `netflix_titles.csv` |
| `netflix_title_category.csv` | l'assegnazione di una categoria a un titolo | `show_id` + `category` | `listed_in`, normalizzato |
| `spotify_track_genre.csv` | l'appartenenza di una traccia a un genere | `track_id` + `track_genre` | righe deduplicate di coppia |
| `spotify_tracks.csv` | una traccia, indipendentemente dai suoi generi | `track_id` | tracce deduplicate |

**Regola di lettura, non negoziabile.** I due dataset musicali **non sono intercambiabili**. Un totale di catalogo si calcola su `spotify_tracks.csv` (decisione ereditata D3 della spec); un'analisi per genere si calcola su `spotify_track_genre.csv`. Sommare conteggi per genere non restituisce il numero di tracce, perché una traccia appartiene fino a nove generi. La stessa avvertenza vale fra `netflix_titles.csv` e `netflix_title_category.csv`.

**Ordinamento** (T3): ordine di sorgente, prima occorrenza in caso di deduplicazione. Nella tabella titolo-categoria le categorie compaiono nell'ordine in cui il campo `listed_in` le elenca.

**Scrittura** (T4): terminatore di riga `\n`, quoting minimale, UTF-8 senza BOM, intestazione presente, nessuna riga finale vuota.

### 1.1 `netflix_titles.csv`

| Campo | Tipo dichiarato | Nota |
|---|---|---|
| `show_id` | testo | chiave. Univoca, verificata come invariante |
| `type` | enumerato: `Movie`, `TV Show` | dominio chiuso, verificato |
| `title` | testo | |
| `director` | testo, ammette vuoto | multi-valore non normalizzato (T7) |
| `cast` | testo, ammette vuoto | multi-valore non normalizzato (T7) |
| `country` | testo, ammette vuoto | multi-valore non normalizzato (T7) |
| `date_added` | data ISO `YYYY-MM-DD`, ammette vuoto | convertita da forma testuale inglese (T6) |
| `release_year` | intero | |
| `rating` | enumerato su `conventions.rating_domain`, ammette vuoto | i valori fuori dominio sono posti a vuoto (FR-015) |
| `movie_duration_min` | intero, vuoto per le serie | da `duration` (FR-014) |
| `tvshow_seasons` | intero, vuoto per i film | da `duration` (FR-014) |
| `listed_in` | testo | **conservato come stringa di sorgente** accanto alla tabella normalizzata |
| `description` | testo | |
| `is_repaired_duration` | booleano | `True` sulle righe toccate dalla riparazione di D2 |

**Perché `listed_in` resta anche qui**: rimuoverlo obbligherebbe chi legge il solo dataset alla grana titolo a fare una giunzione per sapere di che cosa parla un titolo. Conservarlo non crea ambiguità purché nessuno lo conti — ed è ciò che la regola di lettura qui sopra vieta.

**Cosa non compare**: nulla. Tutti e dodici i campi di origine sono presenti, due dei quali riscritti (`duration` separato in due, `rating` ripulito) e uno convertito (`date_added`).

### 1.2 `netflix_title_category.csv`

| Campo | Tipo dichiarato | Nota |
|---|---|---|
| `show_id` | testo | riferimento a `netflix_titles.csv` |
| `category` | testo | una delle 42 etichette di `catalogs.netflix_categories` |

Il numero di righe di questo file è il numero di assegnazioni, che il profilo registra come `NF.cat.assignments`. **Non** è il numero di titoli.

### 1.3 `spotify_track_genre.csv`

Tutti i campi di origine tranne la colonna indice senza nome (T11), più:

| Campo aggiunto | Tipo dichiarato | Nota |
|---|---|---|
| `is_popularity_zero` | booleano | decisione ereditata D1: le righe non si eliminano, si marcano |
| `is_high_zero_genre` | booleano | decisione ereditata D4: quota di zeri del genere superiore al 50% |
| `is_duration_zero` | booleano | valore degenere, contato e marcato, mai corretto (FR-023) |

`is_high_zero_genre` è **costante entro un genere**: è una proprietà del genere, replicata sulla riga per comodità di lettura. La quota che la determina è ricalcolata su questo stesso file, non ripresa dal profilo (decisione ereditata D4, ritrovamento F4).

### 1.4 `spotify_tracks.csv`

Tutti i campi di `spotify_track_genre.csv` tranne `track_genre`, `is_high_zero_genre` e la colonna indice, più:

| Campo aggiunto | Tipo dichiarato | Nota |
|---|---|---|
| `genre_count` | intero, da 1 a 9 | in quanti generi la traccia compare |
| `has_conflicting_popularity` | booleano | `True` sulle 720 tracce di F3, dove le repliche discordavano |

`popularity` su questo file è il **massimo osservato** fra le repliche (T5). Su una riga con `has_conflicting_popularity` pari a `True`, il valore non coincide necessariamente con quello che la stessa traccia porta in `spotify_track_genre.csv`: è la perdita della deduplicazione, ed è marcata proprio perché non resti implicita.

## 2. `reports/cleaning_report.json`

**Versionato**, a differenza dei dataset. Stessa struttura, stesse regole di serializzazione e stessa forma del record di valore del contratto della 002, sezioni 2 e 3.

### 2.1 Identificativi

Prefisso **`CL.`**, disgiunto da `NF.`, `SP.` e `X.` del profilo (T8). Forma: `CL.<dataset>.<area>.<dettaglio>`.

```
CL.NF.rating.out_of_domain.blanked      valori di classificazione posti a mancante
CL.NF.rating.missing.after              valori mancanti nel campo dopo la trasformazione
CL.NF.duration.repaired.rows            righe toccate dalla riparazione di D2
CL.NF.duration.movie.count.after        film con durata valorizzata dopo la riparazione
CL.NF.date_added.trimmed                valori con spazio iniziale normalizzato
CL.NF.date_added.missing                valori vuoti lasciati vuoti
CL.SP.pair.duplicate_pairs              coppie traccia-genere ripetute nella fonte
CL.SP.pair.removed_rows                 righe rimosse dalla deduplicazione di coppia
CL.SP.pair.rows.after                   righe della grana coppia dopo la deduplicazione
CL.SP.track.rows.after                  tracce della grana deduplicata
CL.SP.track.popularity_conflict.tracks  tracce con repliche discordi su popularity
CL.SP.track.popularity_conflict.spread_max   scarto massimo fra le repliche discordi
CL.SP.zero.by_genre.jazz.after          quota di zeri del genere dopo la trasformazione
CL.SP.zero.high_genres.count            generi che superano la soglia del 50%
CL.SP.zero.high_genres.nearest_below    quota del genere più vicino da sotto la soglia
CL.out.netflix_titles.rows              righe del file di output
CL.out.netflix_titles.bytes             dimensione del file di output
```

### 2.2 Blocchi

| Blocco | Ruolo |
|---|---|
| `schema_version` | come nel profilo |
| `sources` | nome, dimensione e impronta dei file di `data/raw/` letti, **confrontati** con quelli del profilo (T10) |
| `conventions` | le regole di questa feature rese dato: soglia di D4, regola di scelta della popolarità, forma riconosciuta dalla riparazione di D2, mappa dei mesi |
| `values` | tutti i valori di rendicontazione. Ogni `value` è un numero, nessuna eccezione |
| `catalogs` | elenchi di etichette: generi che superano la soglia di D4, identificativi dei titoli riparati, valori originali spostati dalla riparazione |
| `outputs` | per ciascun file prodotto: percorso, righe, colonne, dimensione in byte, `sha256` (FR-008) |
| `denominators` | il blocco che realizza FR-030 |

### 2.3 Il blocco `denominators`

È la parte di questo contratto che vale più delle altre, perché è l'unica che esiste per proteggere qualcuno che non è ancora entrato nel progetto.

```json
"denominators": [
  {
    "profile_id": "NF.num.movie_duration_min.count",
    "cleaning_id": "CL.NF.duration.movie.count.after",
    "reason": "la riparazione di D2 restituisce la durata a tre film che nella fonte ne erano privi",
    "scope": "netflix_titles.csv"
  }
]
```

| Campo | Contenuto |
|---|---|
| `profile_id` | l'identificativo del profilo che **non vale più** sul dato trasformato |
| `cleaning_id` | l'identificativo che lo sostituisce dopo la trasformazione |
| `reason` | la ragione della differenza, in italiano, una frase |
| `scope` | su quale output vale il valore nuovo |

**Regola**: ogni valore del profilo che dopo la trasformazione cambia DEVE avere una voce qui. Il documento la cita; il controllo verifica che entrambi gli identificativi esistano e che il documento non citi il vecchio dove intende il nuovo.

Le voci attese, dalla Fase 0: le durate dei film (riparazione), la completezza della classificazione per età (svuotamento), le righe del catalogo musicale (deduplicazione di coppia), e le quote di zeri dei 48 generi che cambiano (F4).

## 3. Marcatura: la quarta forma

Il contratto della 002 ammette tre forme — cifre, numerale in lettere, letterale. Questa feature ne aggiunge una quarta e cambia la severità di una condizione.

### 3.1 Il marcatore di non-misurato

**Forma**: `<testo><!--#-->`, senza spazio interposto, come le altre.

```markdown
Le due<!--#--> letture aritmetiche danno valori diversi: 27,03%<!--@SP.id.inflation-->
è quella adottata. La riparazione tocca 3<!--@CL.NF.duration.repaired.rows--> righe.
```

Il primo numerale è una proprietà del discorso — *ci sono due letture perché questo documento ne elenca due* — e non un fatto misurato sui dati. Il secondo e il terzo lo sono.

**Semantica**: `<!--#-->` non asserisce nulla sul valore. Dichiara che chi scrive **ha considerato** quel numerale e afferma che non è un fatto sui dati. Il controllo non lo verifica: registra che la decisione è stata presa.

**Cosa non può fare**: marcare come non-misurato un fatto che lo è. Nessun meccanismo lo impedisce, ed è il confine di questa garanzia — dichiarato qui e ripetuto nel documento come FR-033 richiede. Ciò che il marcatore elimina è la categoria dell'omissione distratta, che è quella in cui la 002 ha perso tre affermazioni. Non elimina la categoria della dichiarazione falsa, contro cui esiste la revisione in contesto pulito.

### 3.2 Severità, sul nuovo documento

| Condizione | Su `docs/data_audit.md` (002) | Su `docs/data_cleaning.md` (003) |
|---|---|---|
| testo ancorato che non corrisponde | errore | errore |
| identificativo non risolvibile | errore | errore |
| cifra o numerale **senza alcun marcatore** | avviso | **errore** |

È il corollario (c) della decisione ereditata D5, ed è tutta la differenza fra un controllo che elenca e uno che ferma.

**Perché la severità non è retroattiva**: applicarla a `docs/data_audit.md` richiederebbe di rimarcare un documento già mergiato — l'esecuzione del controllo attuale su quel file produce decine di avvisi, tutti legittimi. Non entra nelle 7 ore di questa feature. È un ritrovamento registrato per la regia, secondo il precedente FR-032 della 002.

### 3.3 Risoluzione degli identificativi

Il controllo unisce le mappe `values` dei due artefatti in un unico spazio di nomi. La disgiunzione dei prefissi (T8) garantisce che l'unione non abbia collisioni, e la pipeline **verifica** che non ne abbia invece di assumerlo. Restano risolvibili anche `catalogs.<chiave>` e `conventions.<chiave>` di entrambi gli artefatti, con la semantica di appartenenza già definita dalla 002.

## 4. Cosa questo contratto garantisce e cosa no

**Garantisce** che chi possiede `data/raw/` possa rigenerare i quattro file e verificarne l'identità confrontando le impronte di `outputs` — senza fidarsi di nulla e senza che nessuno abbia versionato un CSV.

**Non garantisce** che i file descritti esistano sulla macchina di chi legge. Non essendo versionati, per chi non ha i dati questo contratto è una descrizione, non una constatazione. È il limite dichiarato nella spec e non va attenuato: la verifica di chi non ha i dati passa dalla pipeline, da `cleaning_report.json` e dal documento, che sono tre artefatti versionati e ispezionabili.

**Non garantisce** che le colonne aggiunte siano un modello dati. `is_high_zero_genre` è una marcatura, non una dimensione; `genre_count` è un conteggio, non una misura. Il disegno del modello è della feature 005 (FR-046), e questo contratto è un ingresso per quel lavoro, non una sua anticipazione.
