# Quickstart — Verifica di conformità del business case

**Data**: 2026-08-07 | **Fase**: 1 (Design) | **Spec**: [spec.md](./spec.md) | **Modello**: [data-model.md](./data-model.md)

Come stabilire che `docs/business_case.md` è conforme alla spec. Due livelli: controlli strutturali, che una macchina può eseguire, e una sessione di revisione, che verifica ciò che nessun conteggio può verificare — se il documento si capisce.

## Prerequisiti

Il documento esiste in `docs/business_case.md`. Nessun dato serve per la verifica: questa feature non calcola nulla.

## Livello 1 — Controlli strutturali

Da eseguire dalla radice del repository. Ogni comando è accompagnato dall'esito atteso.

### Cardinalità dei KPI (vincoli 1 e 3 del modello)

```bash
# sigle KPI distinte: atteso un valore tra 6 e 9
grep -o 'BQ[123]-K[0-9]' docs/business_case.md | sort -u | wc -l

# distribuzione per domanda: atteso 2 o 3 per ciascuna delle tre
grep -o 'BQ[123]-K[0-9]' docs/business_case.md | sort -u | cut -c1-3 | uniq -c

# nomi semantici duplicati: atteso nessun output
grep -oE '`[a-z][a-z0-9_]+`' docs/business_case.md | sort | uniq -d
```

### Presenza delle sezioni obbligatorie (FR-002, FR-008, FR-009, FR-012)

```bash
# atteso: le otto sezioni previste da data-model.md
grep -n '^## ' docs/business_case.md
```

Devono comparire inquadramento, assunzioni strutturali, North Star, le tre domande, framework KPI, scala di confidenza, impatto economico, out of scope.

```bash
# voci fuori scope: atteso >= 5
sed -n '/^## Out of scope/,/^## /p' docs/business_case.md | grep -c '^- '
```

### Coerenza confidenza-formato (vincolo 4 — il più importante)

```bash
# righe della tabella riepilogativa marcate a confidenza bassa
grep -i '| *basso *|' docs/business_case.md
```

Ogni riga restituita deve riportare `range` nella colonna del formato di presentazione. Una riga a confidenza bassa con formato puntuale viola il principio I della constitution e da sola invalida il documento.

### Assenza di numeri di risultato (FR-016, SC-007)

```bash
# percentuali e cifre nel documento: ogni occorrenza va ispezionata a mano
grep -nE '[0-9]+([.,][0-9]+)?%|€ *[0-9]' docs/business_case.md
```

Non è un test automatico: è una lista da leggere. Ogni numero trovato deve essere un **input di scenario** dichiarato come assunzione (prezzi dei tier, orizzonte a 12 mesi, soglie di riferimento) e mai un esito di calcolo. Se un numero non è riconducibile a un'assunzione dichiarata, va rimosso.

### Assenza di sintassi tecnica nelle formule (FR-007)

```bash
# atteso: nessun output
grep -nE 'CALCULATE|SUMX|DIVIDE|SELECT .* FROM|import |df\.|track_genre|listed_in' docs/business_case.md
```

I nomi fisici di colonna dei dataset non devono comparire nelle formule concettuali. Possono comparire nelle note metodologiche, dove servono a dichiarare la provenienza: in quel caso il comando restituisce righe, e vanno ispezionate una per una.

### Tracciabilità (vincolo 2, FR-006)

```bash
# ogni scheda KPI deve citare la propria domanda: atteso un conteggio pari al numero di KPI
grep -c 'Domanda di business' docs/business_case.md
```

## Livello 2 — Sessione di revisione in contesto pulito

Verifica SC-001 e SC-005, che nessun conteggio può coprire. Richiesta da FR-019.

**Procedura**: si apre una sessione nuova, priva della storia del progetto, e si fornisce **solo** `docs/business_case.md`. Nessun accesso alla spec, alla constitution o a questa conversazione: il punto è misurare se il documento si regge da solo.

Tre prove:

1. **Comprensione dell'inquadramento (SC-001)** — chiedere di riformulare la decisione in gioco, la North Star metric e due esclusioni di perimetro. Superata se la riformulazione è corretta e non arrivano domande di chiarimento.
2. **Univocità delle formule (SC-005)** — fornire la sola formula concettuale di ciascun KPI, senza il resto della scheda, e chiedere di descrivere calcolo e granularità. Superata se la descrizione coincide con quella attesa per almeno l'80% dei KPI.
3. **Tenuta del perimetro (SC-007)** — chiedere quale sia la raccomandazione del documento sull'espansione. Superata se la risposta è che il documento non ne contiene una: se il revisore ne estrae una, il documento sta implicando una conclusione che non ha il diritto di sostenere.

**Output**: `specs/001-business-case-kpi/review.md`, versionato, con l'esito di ciascuna prova e le divergenze rilevate. Le divergenze sulla prova 2 diventano punti da chiarire nella feature successiva, non necessariamente difetti da correggere subito.

## Definizione di completo

La feature è conclusa quando: tutti i controlli di livello 1 danno l'esito atteso, le tre prove di livello 2 sono superate, `review.md` è versionato e la checklist [requirements.md](./checklists/requirements.md) resta a 20/20.
