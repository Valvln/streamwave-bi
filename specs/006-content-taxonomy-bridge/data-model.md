# Fase 1 — Modello dei dati

**Feature**: 006 Content Taxonomy Bridge · **Data**: 2026-08-20 · **Piano**: [plan.md](./plan.md)

Come la 004, questa feature non ha un modello dati nel senso della `005`: non produce tabelle relazionali. Ha **quattro entità testuali**, nell'ordine in cui D1 le impone. Questo documento ne fissa la forma; il [contratto](./contracts/dim-category-mood-contract.md) fissa ciò che la `007` può assumere leggendo la terza.

---

## 1. Il criterio — `docs/mood_assignment_criteria.md`

Prosa, non JSON. Committato da solo (FR-001): nel suo commit nessun altro file della feature esiste ancora.

| Sezione | Contenuto obbligatorio |
|---|---|
| per ciascuno dei tre assi (`mood_energy`, `mood_valence`, `mood_danceability`) | che cosa significa ogni valore per una categoria video, su quale base si assegna |
| ancoraggio di scala, per ciascun asse | un esempio all'estremo basso e uno all'estremo alto, **entrambi a livello di categoria o genere musicale come archetipo** (D7, FR-003), citando gli identificativi già pubblicati di F3 — `SP.num.energy.min`/`.max`, `SP.num.valence.min`/`.max`, `SP.num.danceability.min`/`.max` — come base osservabile per chi verifica (FR-004) |
| nota di provenienza | che il criterio precede ogni valore della tabella, con rimando a questo piano e a D1 |

**Non contiene**: alcun valore della tabella (FR-001); alcun titolo, trama o cast (FR-003, D7).

---

## 2. La proposta — `data/curated/dim_category_mood_proposal.json`

Prodotta da un'unica invocazione manuale di un LLM (FR-005, FR-006). Mai trattata come tabella finale (FR-007); non entra in `ARTIFACTS` né in alcuna marcatura.

```jsonc
{
  "schema_version": 1,
  "model": "<nome e versione del modello invocato>",
  "prompt": "<il prompt usato, per intero>",
  "invoked_at": "AAAA-MM-GG",
  "rows": {
    "Action & Adventure": {
      "mood_energy": "0.70",
      "mood_valence": "0.55",
      "mood_danceability": "0.60"
    }
    // … le altre 41 categorie di catalogs.netflix_categories_normalized
  }
}
```

Le chiavi di `rows` sono i **nomi letterali** delle 42 categorie (non slug): questo file non entra nello spazio dei nomi marcato e non ha bisogno di identificativi validi come chiave, solo di corrispondere esattamente a `catalogs.netflix_categories_normalized` per rendere confrontabile la proposta con l'esito della verifica.

---

## 3. La tabella congelata — `data/curated/dim_category_mood.json`

L'artefatto finale (FR-012) e il quarto membro di `ARTIFACTS` (FR-023, D6). Porta la forma che `load_artifacts()` sa unire, **più** i campi propri di congelamento e verifica, che il merge ignora perché non appartengono a `values`/`catalogs`/`conventions`.

```jsonc
{
  "schema_version": 1,
  "version": 1,
  "source": {
    "proposal_file": "data/curated/dim_category_mood_proposal.json",
    "proposal_sha256": "<impronta del file letto in fase di verifica>"
  },
  "verification": {
    "verified_by": "<l'attore dispatchato per la verifica — es. 'subagent, non ha prodotto la proposta' oppure 'Valerio' — non una formula generica: deve nominare chi, non solo affermare l'indipendenza>",
    "verified_at": "AAAA-MM-GG",
    "independence_residual": "<che cosa l'indipendenza dichiarata NON copre: quale contesto entrambi gli attori condividono comunque. Dichiarato invece che taciuto>",
    "changes_count": 0,
    "changes": [
      // presente solo se changes_count > 0: una voce per cella modificata
      // { "category": "...", "axis": "mood_energy", "proposal_value": "0.70",
      //   "final_value": "0.55", "criterion_reference": "..." }
    ],
    "criterion_findings": [
      // difetti del criterio trovati dalla verifica, che NON sono celle contestate
      // { "id": "CF-1", "sections": ["§2", "§5"], "finding": "...",
      //   "resolution": "...", "cells_affected": 5 }
    ],
    "zero_changes_note": "<obbligatorio solo se changes_count == 0: dichiara il ritrovamento, non lo presenta come conferma — User Story 3, scenario 3>"
  },
  "values": {
    "MOOD.category.action_adventure.mood_energy": {
      "value": "0.70", "display": "0,70",
      "category": "Action & Adventure", "axis": "mood_energy",
      "label": "profilo di mood, asse energia", "unit": "0-1"
    }
    // … le altre 125 celle (42 categorie × 3 assi)
    ,
    "MOOD.coverage.rows": {
      "value": 42, "display": "42",
      "label": "categorie coperte dalla tabella dei profili di mood"
    },
    "MOOD.table.version": {
      "value": 1, "display": "1",
      "label": "versione della tabella al momento del congelamento"
    },
    "MOOD.review.changes_count": {
      "value": 0, "display": "0",
      "label": "righe (categoria × asse) modificate dalla verifica indipendente rispetto alla proposta"
    }
  },
  "catalogs": {
    "mood_categories": ["Action & Adventure", "Anime Features", "…"]
  },
  "conventions": {
    "mood_scale_anchor": "gli estremi 0 e 1 di ciascun asse corrispondono, per significato, agli estremi osservati sul lato musicale per lo stesso asse: SP.num.energy.min/.max, SP.num.valence.min/.max, SP.num.danceability.min/.max di reports/data_profile.json (F3, research.md). Il criterio in docs/mood_assignment_criteria.md ne fa uso come base di ancoraggio.",
    "mood_rounding": "due cifre decimali, ROUND_HALF_UP dichiarato esplicitamente. Un valore assegnato dall'analista non ha la precisione di una misura; due cifre sono la granularità con cui il criterio distingue i casi, non un limite tecnico."
  }
}
```

### I tre campi aggiunti in fase di implementazione

`verified_at`, `independence_residual` e `criterion_findings` non erano in questa sezione quando è stata scritta, e sono stati aggiunti dalla verifica di T017 il 2026-08-20. La ragione di ciascuno:

- **`verified_at`** perché `changes_count` senza una data non dice se la verifica preceda o segua il congelamento;
- **`independence_residual`** perché la condizione 4 della quinta fonte è soddisfatta dal fatto che chi verifica non abbia prodotto la proposta, ma il contesto che i due attori condividono comunque — nel caso concreto le istruzioni di progetto che il sistema inietta in entrambi — non è nullo, e un registro che dichiarasse solo l'indipendenza direbbe meno del vero. È lo stesso motivo per cui il verbale di revisione dichiara in apertura cosa è stato letto e cosa no;
- **`criterion_findings`** perché la verifica ha prodotto un esito che `changes` non poteva contenere: difetti del **criterio**, non celle contestate. Registrarli come celle spostate sarebbe stato falso; non registrarli li avrebbe persi, e sono l'esito più utile della verifica — vedi §7 del criterio, che vieta di spostare una riga senza citare il criterio, e che quindi produce necessariamente questa categoria residua.

La correzione va in questa direzione — modello allineato all'implementazione — per la stessa ragione dichiarata in T042 per il contratto: dove i due divergono, è il documento a doversi correggere, non chi legge a doverlo indovinare.

### Perché `values` è la tabella, non una sua copia

`MOOD.category.<slug>.<asse>` **è** la rappresentazione canonica delle 126 celle. Non esiste altrove nel file un secondo elenco delle stesse 126 righe: un doppione richiederebbe uno script che li tenga allineati, e nessuno script tocca questo file dopo il congelamento (FR-012, ricerca T3). Chi legge la tabella come tabella — la `007`, o una persona — la ricostruisce filtrando `values` per prefisso `MOOD.category.` e raggruppando per `category`; il [contratto](./contracts/dim-category-mood-contract.md) lo mostra in tre righe di codice.

### Gli identificativi

| Identificativo | Contenuto |
|---|---|
| `MOOD.category.<slug>.mood_energy` / `.mood_valence` / `.mood_danceability` | le 126 celle, una per categoria per asse. `<slug>` è il nome della categoria normalizzato — minuscolo, non alfanumerico → `_` (F4, research.md: nessuna collisione sulle 42 categorie) |
| `MOOD.coverage.rows` | quante categorie la tabella copre (42, o meno con la copertura parziale dichiarata — FR-014) |
| `MOOD.table.version` | il campo `version` di primo livello, ripetuto come identificativo per essere citabile in prosa |
| `MOOD.review.changes_count` | il conteggio di FR-010, ripetuto come identificativo per la stessa ragione |

Prefisso `MOOD.`, verificato disgiunto da `NF.`, `SP.`, `CL.`, `X.`, `BQ3.` (T2, research.md).

### `catalogs.mood_categories`

Le 42 chiavi `category` della tabella, nella stessa forma di `catalogs.netflix_categories_normalized`. Serve a due cose distinte: è l'insieme che D6/FR-019 confronta meccanicamente con quello della `003` (§4 più sotto), ed è la forma letterale con cui una categoria citata in prosa si ancora — `` `Horror Movies`<!--@catalogs.mood_categories--> `` — sullo stesso modello già in uso per `catalogs.netflix_categories_musical` nella `002`.

### Copertura parziale

Se una categoria non ricevesse un profilo (FR-014), le sue celle non compaiono in `values` e il suo nome non compare in `catalogs.mood_categories`. `MOOD.coverage.rows` scende sotto 42 e la differenza con `catalogs.netflix_categories_normalized` **è** la divergenza che il controllo di §4 rileverebbe: la copertura parziale dichiarata e il presidio meccanico di D6 condividono lo stesso meccanismo di confronto, con un solo esito ammesso senza fallire — quello in cui il documento pubblicato dichiara esplicitamente quali categorie mancano e perché (FR-014), e in cui la funzione di guardia (§4 del piano) lo riconosce come stato dichiarato invece che come errore. La forma esatta di questa dichiarazione — un campo aggiuntivo che marca la copertura come parziale by design, oppure l'assenza pura e semplice se il caso non si presenta — è una decisione di implementazione che questa fase lascia aperta perché **l'assunzione della spec è che l'insieme non cambi durante la costruzione**: il caso è ammesso ma non atteso.

---

## 4. Il documento pubblicato — `docs/content_taxonomy_bridge.md`

Prosa, quinto membro di `DOCUMENTS`, severità stretta fin dalla nascita (FR-023, T8 della ricerca). La struttura che FR-022 impone, in ordine:

1. **La natura interpretativa della tabella** — l'apertura della spec, prima di ogni requisito.
2. **I quattro passi di D1**, con i relativi artefatti — criterio, proposta, verifica indipendente, congelamento — e le due revisioni distinte di D9 tenute separate.
3. **Il conteggio degli spostamenti** (`MOOD.review.changes_count`), con la dichiarazione esplicita se è zero.
4. **Il contratto di versione per la `007`** (D5, FR-016): ogni valore a valle dichiara su quale versione di questa tabella è calcolato.
5. **I limiti dichiarati** della feature.

Ogni numerale in posizione di fatto misurato porta un'ancora (FR-024): `MOOD.coverage.rows`, `MOOD.table.version`, `MOOD.review.changes_count`, e — se il documento cita esempi di riga — le celle `MOOD.category.<slug>.<asse>` corrispondenti, marcate come membro letterale via `catalogs.mood_categories` per il nome della categoria e come cifra via l'identificativo di cella per il valore.

---

## Ciò che questo modello non contiene, e perché

- **nessun valore di `BQ1-K3`, `BQ2-K2`, `BQ2-K3`.** Sono calcolati dalla `007` a partire da questa tabella secondo le regole di aggregazione già fissate in §11 di `docs/data_model.md`, che questa feature eredita e non ridiscute (D2, Perimetro).
- **nessun campo generato da script.** Non esiste una funzione di derivazione in questa feature: i tre file di prosa/dati sono tutti scritti o congelati a mano, nell'ordine di D1. È la differenza strutturale con la `004` che F5 della ricerca isola.
- **nessun attributo di record individuale del catalogo video.** Né titolo, né trama, né cast, in nessuno dei quattro artefatti (D7, FR-020).
