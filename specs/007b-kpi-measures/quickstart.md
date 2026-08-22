# Quickstart: verifica di `docs/kpi_measures.md` e `reports/kpi_measures.json`

**Feature**: 007b-kpi-measures | **Data**: 2026-08-22

Dodici prove, in ordine di esecuzione. Le prime nove sono eseguibili da chiunque abbia clonato il repository; l'ultima non lo è per costruzione (E9), ed è comunque parte della lista perché è una condizione di successo della feature, non un'aggiunta opzionale.

## Prerequisiti

- `data/raw/` presente (scaricato con `scripts/download_data.sh` e un token Kaggle).
- Working directory: radice del repository.

## Le dodici prove

### 1 — La catena intera è riproducibile (US1, SC-002)

```bash
python3 scripts/build_datasets.py
python3 scripts/build_kpi_measures.py
```

Atteso: entrambi terminano con successo; `reports/kpi_measures.json` viene prodotto. Ripetere la seconda riga: il file non cambia byte per byte.

### 2 — Otto valori, ciascuno ancorato (SC-001)

Aprire `docs/kpi_measures.md`; per ciascuno degli otto KPI, verificare che il valore pubblicato porti un'ancora verso `reports/kpi_measures.json` (sei KPI) o `reports/bq3_scenarios.json` (`BQ3-K1`, `BQ3-K2`). Atteso: nessun valore scritto a mano, nessuna delle otto voci mancante.

### 3 — L'invarianza della North Star è verificata o dichiarata come ritrovamento (US2, SC-004)

Leggere la sezione `BQ1-K1`. Atteso: il conteggio diretto su `netflix_title_category.csv` è ancorato, il confronto con `375` è esplicito, e l'esito — coincidenza o divergenza — è dichiarato in prosa, non lasciato dedurre dai due numeri accostati.

### 4 — La quota di zeri e l'avvertimento sui 7 segmenti (US3)

Cercare nel documento i 7 segmenti con `is_high_zero_genre` vero (l'elenco è in `catalogs.high_zero_segments` dell'artefatto). Atteso: ciascuno porta l'avvertimento testuale esplicito accanto al proprio valore di `segment_demand_index`; ogni altro segmento porta comunque la quota di zeri, senza l'avvertimento.

### 5 — Le due varianti della mediana di durata e la quota di film (E3, E4)

Leggere la sezione `BQ1-K2`. Atteso: entrambe le varianti della mediana musicale (con e senza la riga `is_duration_zero`) sono pubblicate con la loro differenza; la quota di film sul catalogo video è pubblicata accanto al valore principale.

### 6 — I tre vincoli di `kpi_operators.md` §12 e le issue `#7`/`#8` (US4, SC-005)

Aprire `docs/kpi_operators.md` §12. Atteso: nessuno dei tre vincoli (mediana, durata degenere, arrotondamento) compare più come aperto — ciascuno cita **D10**, **D11** o la tabella di E5. Aprire le issue `#7` e `#8` su GitHub: entrambe proposte per la chiusura con riferimento al commit corrispondente (la chiusura effettiva resta a Valerio, FR-027).

### 7 — Verifica meccanica delle ancore (US5, SC-003)

```bash
python3 scripts/check_audit_coherence.py
```

Atteso: uscita verde in severità stretta su sette documenti (sei in severità stretta più `docs/data_audit.md` ad avvisi) e cinque artefatti nello spazio dei nomi unito.

### 8 — Registrazione in `convenzioni-marcatura.md`

Verificare che la tabella di severità e la tabella di provenienza di `docs/convenzioni-marcatura.md` contengano una riga per `docs/kpi_measures.md`, con data e feature (`007b`).

### 9 — La nota in loco su `business_case.md` §3 (US6)

Leggere `business_case.md` §3. Atteso: il testo originale («musical, documentari musicali, concerti, film sulla musica») è intatto; la nota in loco accanto dichiara data, feature, causa, e che la misura legge la sola etichetta `Music & Musicals`.

### 10 — README allineato (SC-007)

Verificare nella tabella di stato del README la riga della `007b` con link a `specs/007b-kpi-measures/review.md`; la frase sui documenti che pubblicano misure estesa all'ottavo documento; `Setup` e `Struttura` aggiornati; il conteggio dei documenti sotto controllo di coerenza aggiornato da sei a sette.

### 11 — Il verbale di revisione esiste ed è committato prima delle correzioni (SC-006)

```bash
git log --oneline --reverse -- specs/007b-kpi-measures/review.md docs/kpi_measures.md
```

Atteso: il primo commit che tocca `review.md` precede — o coincide con — qualunque commit successivo che modifica `docs/kpi_measures.md` per applicare un rilievo della revisione.

### 12 — L'esito di E9 è dichiarato per ciascuna misura, non simulabile da questo repository (SC-008)

Aprire `docs/kpi_measures.md` dopo che Valerio ha eseguito il confronto manuale. Atteso: ciascuna delle otto misure dichiara «verificato contro il motore reale» oppure una nota in loco con entrambi i numeri e la causa, se identificabile. **Questa prova non è automatizzabile**: nessuno script di questo repository può aprire Power BI Desktop, incollare il DAX o leggere il valore restituito — è esattamente il confine del principio V. Prima che Valerio esegua il confronto, l'esito atteso è che ogni misura dichiari lo stato di default «calcolato da script», mai «verificato» in anticipo.

## Esito atteso

Le prove 1-11 passano prima che la revisione in contesto pulito riceva il documento; la prova 12 passa prima del merge, non prima. Le prove 1, 7 e 11 sono le uniche automatizzabili da riga di comando; le altre sono ispezione umana.

**Questa non è la revisione in contesto pulito.** Le dodici prove sono verifica di lavorazione, eseguite da chi ha scritto lo script e il documento (o chiunque altro, leggendo l'intero repository). La revisione in contesto pulito è un atto distinto e successivo: un revisore isolato che riceve **solo** `docs/kpi_measures.md`, sul modello di `specs/007a-kpi-operators/review.md`.
