# Data Model: Operatori delle misure

**Feature**: 007a-kpi-operators | **Data**: 2026-08-21

## Perché questo file non descrive tabelle

Ogni `data-model.md` precedente del progetto (`005`, `006`) descrive righe e colonne di un artefatto sotto `data/`. Questa feature non ne produce nessuno: il suo unico deliverable è un documento di prosa. Ciò che segue non è quindi lo schema di un dataset, ma la **forma** che ogni voce di `docs/kpi_operators.md` deve avere per essere completa — l'equivalente, per un documento, di uno schema per una tabella: i campi obbligatori di ciascuna delle otto voci-KPI e delle nove decisioni, derivati direttamente dai requisiti FR-014 (provenienza), FR-015 (confidenza), FR-016/FR-017 (limiti ereditati) e dalla sezione "Key Entities" di [spec.md](./spec.md).

## Entità 1 — Voce-KPI

Una voce-KPI è il blocco di `docs/kpi_operators.md` dedicato a uno degli otto KPI di `business_case.md` §5.5. Ce ne sono otto, una per riga della tabella di Provenienza e Confidenza già fissata in spec.md.

| Campo | Obbligatorio | Origine del vincolo | Contenuto atteso |
|---|---|---|---|
| `nome_semantico` | sì | identità del KPI, business_case.md §5.5 | es. `music_adjacent_catalog_share` |
| `formula` | sì, tranne `BQ3-K1`/`BQ3-K2` | FR-019 | l'espressione dell'operatore, in prosa o notazione, senza calcolarne il valore |
| `grana` | sì | FR-014 | la tabella e il livello (riga, categoria, segmento) su cui l'operatore opera — es. "per riga di `bridge_title_category`, raggruppata per categoria" (D9.2) |
| `provenienza_modello_dati` | sì | FR-014 | tabelle e colonne esatte di `docs/data_model.md` da cui l'operatore legge |
| `confidenza` | sì | FR-015 | il livello già fissato da `business_case.md` §5.4, mai alterato — invariato per costruzione, non un campo che questa feature decide |
| `limiti_ereditati` | dove applicabile | FR-016, FR-017 | vincoli di CF-1, campione sbilanciato, ancoraggio solo agli estremi, dichiarati come fatto e non come giudizio |
| `decisione_di_riferimento` | sì | Key Entities di spec.md | l'identificativo D1-D9 (e sotto-decisioni) che fissa questo operatore |

**Le otto istanze**, con la decisione che le fissa (dalla tabella di Provenienza e Confidenza di spec.md):

| KPI | Decisione |
|---|---|
| `BQ1-K1` | D9 (D9.1 numeratore/invariante, D9.2 operatore di C1, D9.3 rapporto non pubblicato per giustapposizione) |
| `BQ1-K2` | D5 (segno e verso), D8 (direzione della graduatoria non si applica qui — D8 è su `BQ2-K3`; per `BQ1-K2` la parte residua di R13 è chiusa da D5 stessa) |
| `BQ1-K3` | D1 (prodotto cartesiano), D7 (non si applica — D7 è sulla popolarità, non sul mood; `BQ1-K3` eredita solo FR-016 per la stabilità degli assi) |
| `BQ2-K1` | D6 (precisione del confronto, dove citata come esempio), D7 (quota di zeri obbligatoria) |
| `BQ2-K2` | D2 (metrica), D7 (non si applica — D7 è sulla popolarità) |
| `BQ2-K3` | D3 (pesi e scala), D4 (quadranti e combinazione pesata), D8 (direzione della graduatoria) |
| `BQ3-K1` | nessuna — già chiuso dalla `004`, nessun operatore nuovo (FR-019 lo dichiara esplicitamente per completezza, non lo ridefinisce) |
| `BQ3-K2` | nessuna — già chiuso dalla `004`, come sopra |

**Correzione alla tabella sopra**: la lettura "D7 non si applica" per `BQ1-K3`/`BQ2-K2` va scritta in [kpi_operators.md] come assenza esplicita, non come omissione silenziosa — un lettore che non trova la quota di zeri accanto a un KPI di mood deve poter concludere che è perché quel KPI non tocca la popolarità, non perché l'operatore l'ha dimenticata. È un vincolo di scrittura per la fase B, non un campo nuovo.

## Entità 2 — Decisione (D1-D9)

Nove blocchi (D9 con tre sotto-parti), ciascuno già scritto per intero in spec.md. La forma che ciascuno deve mantenere quando viene trasposto in `docs/kpi_operators.md`:

| Campo | Contenuto |
|---|---|
| `identificativo` | D1...D9, con D9.1/D9.2/D9.3 come sotto-identificativi |
| `origine` | il rilievo o la divergenza puntuale che l'ha sollevata (es. "divergenza 2 della revisione 001") |
| `opzioni_scartate` | almeno una, con la ragione dello scarto — mai solo l'opzione scelta |
| `decisione` | l'opzione presa, in forma operativa (eseguibile da chi implementa, non solo descrittiva) |
| `ragione` | perché questa opzione e non le altre, ancorata a un vincolo già fissato altrove quando esiste |
| `limite_introdotto` | dove la decisione stessa introduce un limite (D1, D2), dichiarato esplicitamente, non lasciato da dedurre |

**Relazione fra le due entità**: ogni voce-KPI cita una o più decisioni; ogni decisione può vincolare più di una voce-KPI (D7 vincola sia `BQ2-K1` sia, per composizione, `BQ2-K3`; D9 vincola solo `BQ1-K1` ma in tre parti). Nessuna decisione resta senza una voce-KPI che la cita, e nessuna voce-KPI manca della propria decisione — è la proprietà che SC-001 verifica per le voci e che la struttura di questo file rende esplicita per le decisioni.

## Entità 3 — Numerale citato come esempio

Ogni volta che una voce-KPI o una decisione cita un numero concreto (375, 8.807, 0,5 punti percentuali, 114 segmenti, 42 categorie), quel numero è un'istanza di questa terza entità, non un valore libero:

| Campo | Contenuto |
|---|---|
| `valore` | il numero come appare nel testo |
| `ancora` | l'identificativo esatto nell'artefatto sorgente (es. `NF.cat.music_musicals.titles`) o il marcatore esplicito di non-misurato |
| `artefatto_sorgente` | uno fra `reports/data_profile.json`, `reports/cleaning_report.json`, `data/curated/dim_category_mood.json`, `docs/data_model.md` |
| `stato` | `input-già-ancorato` (il caso normale: il numero è un dato di un'altra feature, non un risultato di questa) — mai `risultato-calcolato`, perché questa feature non calcola nulla (FR-019) |

Questa è l'entità che `scripts/check_audit_coherence.py` verifica meccanicamente (FR-021): la sua estensione non introduce una nuova classe di controllo, applica quella già esistente (usata da `data_model.md`) a un sesto documento.
