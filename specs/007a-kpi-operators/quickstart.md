# Quickstart: verifica di `docs/kpi_operators.md`

**Feature**: 007a-kpi-operators | **Data**: 2026-08-21

Dieci prove, in ordine di esecuzione. Le prime sette sono per ispezione (si legge il documento), le ultime tre sono meccaniche (si esegue uno script o si confronta con un altro file). Nessuna richiede dati, pipeline o Power BI — coerente con il perimetro della feature.

## Prerequisiti

- `docs/kpi_operators.md` scritto (blocco B del piano di lavoro).
- `scripts/check_audit_coherence.py` esteso con la sesta riga in `DOCUMENTS` (blocco C).
- Working directory: radice del repository.

## Le dieci prove

### 1 — Otto operatori, uno per KPI (SC-001)

Confrontare l'elenco degli otto nomi semantici in `docs/kpi_operators.md` con la tabella di `docs/business_case.md` §5.5. Atteso: coincidenza esatta, nessun KPI mancante o duplicato.

### 2 — Nessun valore numerico dei KPI (SC-002, FR-019)

Leggere il documento cercando qualunque cifra presentata come *risultato* di un calcolo sui dati reali (non come input citato da un artefatto). Atteso: nessuna. Ogni numero deve portare un'ancora verso un artefatto di una feature precedente (verificato meccanicamente alla prova 8).

### 3 — Le quattro decisioni più esposte, con opzione scartata (US1, SC-003)

Leggere D1-D4. Atteso: ciascuna cita almeno un'opzione scartata con la ragione dello scarto, non solo l'opzione scelta — coerente con quanto già riportato in forma compatta al terzo punto di stop.

### 4 — L'operatore di C1 distinto da quello della quota (US2)

Leggere la voce `BQ1-K1`. Atteso: due operatori separati e nominati come tali — D9.2 per C1 (graduatoria delle 42 categorie), D9.3 per la quota (`music_adjacent_catalog_share`) — non un solo paragrafo che li confonde.

### 5 — L'invariante di D9.1 è verificabile sui tre identificativi che cita

Aprire `reports/data_profile.json` e `reports/cleaning_report.json`; verificare che `NF.shape.rows` = 8.807, `CL.NF.titles.rows.after` = 8.807, `CL.NF.duration.repaired.rows` = 3, e che il testo di `docs/kpi_operators.md` citi tutti e tre nell'argomentare l'invariante. Atteso: coincidenza, nessun identificativo mancante.

### 6 — Nessuna confidenza alterata (US3, SC-005)

Confrontare la confidenza dichiarata per ciascun KPI in `docs/kpi_operators.md` con `docs/business_case.md` §5.4. Atteso: otto corrispondenze esatte.

### 7 — La soglia di D6 limitata al confronto delle quote di zeri (FR-010)

Cercare nel documento ogni occorrenza di "0,5 punti percentuali". Atteso: ogni occorrenza è esplicitamente qualificata come limitata al confronto profilo/cleaning sulle quote di zeri per genere, mai presentata come regola generale.

### 8 — Verifica meccanica delle ancore (US5, SC-004)

```bash
python3 scripts/check_audit_coherence.py
```

Atteso: uscita verde (nessun errore) in severità stretta su tutti e sei i documenti di `DOCUMENTS`, inclusa la riga nuova per `docs/kpi_operators.md`.

### 9 — Registrazione in `convenzioni-marcatura.md` (FR-022)

Verificare che la tabella di Provenienza di `docs/convenzioni-marcatura.md` contenga una riga per `docs/kpi_operators.md` con data e feature (`007a`).

### 10 — README allineato (FR-023, SC-007)

Verificare nella tabella di stato del README la riga della `007a` con link a `specs/007a-kpi-operators/review.md`; la frase sui documenti che pubblicano misure estesa al sesto documento; il commento del passo 5 di `Setup` e la sezione `Struttura` aggiornati di conseguenza.

## Esito atteso

Tutte e dieci le prove passano prima che la feature si consideri conclusa. Le prove 1-7 e 9-10 sono ispezione umana (parte della revisione in contesto pulito); la prova 8 è l'unica automatizzabile da riga di comando.
