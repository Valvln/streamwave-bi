# Contratto — `reports/data_profile.json` e marcatura dei valori

**Feature**: 002 Data Audit & Profiling | **Data**: 2026-08-08

Questo file fissa l'interfaccia fra tre cose che vivono separate: lo **script** che produce l'artefatto, la **persona** che scrive il documento di audit a mano, e il **controllo di coerenza** che verifica che le prime due siano d'accordo. Serve anche alle feature successive, che citeranno identificativi di questo artefatto senza doverne riaprire lo script.

Il motivo per cui esiste — a differenza della 001, che rifiutò `contracts/` — è argomentato nella decisione D7 di [research.md](../research.md).

## 1. Identificativi dei valori

**Forma**: `<DATASET>.<area>.<dettaglio>`, in minuscolo salvo il prefisso di dataset, separati da punti.

| Prefisso | Significato |
|---|---|
| `NF` | catalogo video (`netflix_titles.csv`) |
| `SP` | catalogo musicale (`spotify_tracks_dataset.csv`) |
| `X` | valore che attraversa entrambi i dataset |

**Regole**:

- l'identificativo è **stabile**: non cambia quando cambia il valore. È ciò che permette a una feature successiva di citarlo e a un diff di mostrare che il numero si è mosso;
- l'identificativo è **univoco** su tutto l'artefatto;
- se lo stesso numero serve in due forme di lettura diverse (una quota come percentuale e come frazione), sono **due valori con due identificativi**, non una riformulazione a mano nel documento;
- i segmenti che derivano da un valore dei dati (nome di categoria, nome di genere) sono normalizzati in minuscolo con separatori non alfanumerici sostituiti da `_`.

**Esempi**:

```
NF.shape.rows                    numero di titoli del catalogo video
NF.type.movie                    titoli di tipo film
NF.miss.director.pct             quota di titoli senza regista
NF.cat.count                     numero di categorie distinte
NF.cat.music.count               quante categorie hanno contenuto musicale dichiarato
NF.cat.music_musicals.titles     titoli distinti nella categoria musicale
NF.rating.out_of_domain          valori della classificazione fuori dominio
NF.movie.duration.median         durata mediana di un film, in minuti
SP.shape.rows                    righe del catalogo musicale
SP.genre.count                   generi distinti
SP.genre.per_genre               righe per genere (se costante)
SP.id.distinct                   identificativi di traccia distinti
SP.id.dup_share                  quota di righe che sono ripetizioni
SP.id.inflation                  eccesso del totale non deduplicato sul deduplicato
SP.pop.zero.pct                  quota di tracce a popolarità zero
SP.pop.zero.by_genre.jazz        quota a popolarità zero nel genere indicato
X.genre_lexical.count            generi musicali con corrispondenza lessicale
```

## 2. Forma del record di valore

Ogni valore è un oggetto sotto la chiave `values`, indicizzato dal proprio identificativo.

```json
"SP.pop.zero.pct": {
  "value": 14.05,
  "display": "14,05%",
  "unit": "percentuale",
  "dataset": "spotify",
  "field": "popularity",
  "granularity": "coppia traccia-genere",
  "label": "quota di righe con indice di popolarità pari a zero"
}
```

| Campo | Obbligatorio | Contenuto |
|---|---|---|
| `value` | sì | il valore grezzo, numerico. Nessuna formattazione |
| `display` | sì | la stringa **esatta** che il documento di audit deve scrivere. Convenzioni italiane: `.` per le migliaia, `,` per i decimali |
| `unit` | sì | unità o natura del valore (`conteggio`, `percentuale`, `minuti`, `secondi`, `byte`) |
| `dataset` | sì | `netflix`, `spotify` o `entrambi` |
| `field` | dove pertinente | campo di origine; `null` per i valori di forma o di censimento |
| `granularity` | dove non univoca | su cosa è calcolato: `titolo`, `traccia deduplicata`, `coppia traccia-genere`, `riga` |
| `label` | sì | descrizione breve in italiano. Descrive, non interpreta |

**Vincolo**: `label` non contiene giudizio né conseguenza. L'interpretazione vive nel documento di audit (FR-010).

## 3. Struttura dell'artefatto

```json
{
  "schema_version": "1",
  "conventions": { "missing": "...", "high_cardinality_threshold": 0, "rounding_decimals": 0 },
  "sources": [
    { "file": "data/raw/netflix_titles.csv", "bytes": 0, "sha256": "..." }
  ],
  "values": { "<identificativo>": { } },
  "inventory_001": { "V01": ["NF.shape.rows", "NF.type.movie", "NF.type.tvshow"] },
  "divergences": [
    {
      "claim_id": "V13",
      "source": "docs/business_case.md §5.2",
      "claimed": "circa un quinto",
      "regenerated": ["SP.id.dup_share", "SP.id.inflation"],
      "status": "ambiguo",
      "note": "..."
    }
  ]
}
```

| Blocco | Ruolo |
|---|---|
| `conventions` | le regole di D9 rese parte del dato: cosa conta come mancante, soglia di alta cardinalità, decimali di arrotondamento |
| `sources` | provenienza per FR-005: nome, dimensione e impronta di ciascun file di origine |
| `values` | tutti i valori del profilo |
| `inventory_001` | mappa da `V01`-`V14` dell'inventario di FR-020 agli identificativi che li rigenerano. Rende SC-003 verificabile da una macchina invece che da una lettura |
| `divergences` | esito del confronto automatico di D6. `status` ∈ `coincide`, `diverge`, `ambiguo` |

**Regole di serializzazione** (determinismo, D5): chiavi ordinate alfabeticamente; nessun timestamp di esecuzione; ogni valore non intero arrotondato ai decimali dichiarati in `conventions`; codifica UTF-8 senza escape dei caratteri non ASCII; indentazione fissa e ritorno a capo finale.

## 4. Grammatica della marcatura

**Forma**: il marcatore segue il valore **senza spazio interposto**.

```
<testo-display><!--@<identificativo>-->
```

**Esempio, come si scrive nel documento**:

```markdown
Il catalogo video contiene 8.807<!--@NF.shape.rows--> titoli, di cui
6.131<!--@NF.type.movie--> film e 2.676<!--@NF.type.tvshow--> serie.
```

**Esempio, come si legge**: il commento è invisibile in qualunque lettore Markdown.

> Il catalogo video contiene 8.807 titoli, di cui 6.131 film e 2.676 serie.

**Regole**:

1. il testo che precede immediatamente il marcatore, fino al primo spazio o inizio di riga, DEVE coincidere **carattere per carattere** con il campo `display` del valore;
2. un identificativo può essere marcato più volte nel documento;
3. il marcatore funziona ovunque, prosa o cella di tabella;
4. non esistono altre forme di marcatura. Un numero senza marcatore non è un valore di profilo e il controllo non lo legge.

## 5. Cosa il controllo di coerenza verifica

| Condizione | Esito |
|---|---|
| il testo prima del marcatore coincide con `display` | passa |
| il testo prima del marcatore **non** coincide con `display` | **errore**: riporta identificativo, atteso e trovato |
| il marcatore punta a un identificativo assente da `values` | **errore**: riporta il riferimento non risolvibile |
| un identificativo di `inventory_001` punta a un valore assente | **errore** |
| un gruppo di cifre nel documento non è adiacente ad alcun marcatore | **avviso**, non bloccante (D8) |

Il controllo legge **solo** il documento di audit e l'artefatto, entrambi versionati: non richiede `data/raw/` e non riesegue il profiling (FR-036).
