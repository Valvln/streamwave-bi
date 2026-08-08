# Quickstart — Feature 002: Data Audit & Profiling

**Data**: 2026-08-08 | **Fase**: 1 (Design) | **Spec**: [spec.md](./spec.md)

Guida di verifica: come eseguire ciò che la feature produce e come accertare che i criteri di successo siano soddisfatti. Non contiene codice di implementazione — quello vive negli artefatti del repository.

## Prerequisiti

**Python 3** e nulla d'altro. Nessuna dipendenza esterna, nessun ambiente virtuale: è la decisione D1 di [research.md](./research.md), e la ragione per cui questa guida non ha un passo di installazione.

Per rigenerare il profilo servono i dati di origine:

```bash
./scripts/download_data.sh   # richiede un token Kaggle
```

Per **tutto il resto** — leggere il documento, verificarne la coerenza, risalire da un numero alla sua fonte — i dati di origine non servono. È il punto di FR-036 e SC-007.

## I tre comandi

```bash
# 1. rigenera il profilo (richiede data/raw/)
python3 scripts/profile_data.py

# 2. verifica la coerenza fra documento e profilo (NON richiede data/raw/)
python3 scripts/check_audit_coherence.py

# 3. verifica che l'artefatto sia davvero tracciato da git
git check-ignore -v reports/data_profile.json    # non deve restituire nulla
```

## Verifica dei criteri di successo

### SC-001 — Determinismo

```bash
python3 scripts/profile_data.py
cp reports/data_profile.json /tmp/profile_a.json
python3 scripts/profile_data.py
diff /tmp/profile_a.json reports/data_profile.json && echo "OK: identici"
```

Attesa: nessuna differenza. Se il diff mostra righe che cambiano a ogni esecuzione, una delle quattro regole di determinismo di D5 è stata violata — nella pratica, quasi sempre un timestamp o un ordinamento non stabile.

### SC-002 — `data/raw/` immutato

```bash
shasum -a 256 data/raw/*.csv > /tmp/raw_before.txt
python3 scripts/profile_data.py
shasum -a 256 data/raw/*.csv | diff /tmp/raw_before.txt - && echo "OK: sorgenti intatte"
```

Attesa: nessuna differenza. Verifica il principio II nel punto in cui è più facile violarlo per distrazione.

### SC-003 — I quattordici valori della 001 sono rigenerati

```bash
python3 -c "
import json; d=json.load(open('reports/data_profile.json'))
inv, vals = d['inventory_001'], d['values']
missing = {k: [i for i in v if i not in vals] for k,v in inv.items()}
missing = {k:v for k,v in missing.items() if v}
print('sigle presenti:', len(inv), '/ 14')
print('riferimenti non risolti:', missing or 'nessuno')
"
```

Attesa: 14 sigle, nessun riferimento non risolto.

### SC-004 — Nessun campo omesso in silenzio

Lettura assistita: si confronta l'elenco dei campi profilati nell'artefatto con l'intestazione dei due file di origine.

```bash
head -1 data/raw/netflix_titles.csv | tr ',' '\n' | wc -l          # atteso: 12
head -1 data/raw/spotify_tracks_dataset.csv | tr ',' '\n' | wc -l  # atteso: 21
```

Attesa: ogni campo compare nel profilo **oppure** nell'elenco delle esclusioni con la ragione. Attenzione ai due casi che la Fase 0 ha già individuato (F5): la prima colonna del catalogo musicale è **priva di nome**, e il catalogo video ha tre campi che la 001 non profilava.

### SC-005 — Ogni valore del profilo nel documento è marcato

Verifica **in due parti**, ed è la sola della lista che non si chiude con un comando.

```bash
python3 scripts/check_audit_coherence.py
```

La parte automatica: il comando fallisce se un valore marcato non coincide o se un riferimento non si risolve. La parte assistita: il comando elenca come **avvisi** i gruppi di cifre non adiacenti a un marcatore, e quell'elenco va letto. Ogni voce è una di tre cose — un valore di profilo da marcare (da correggere), una data o un riferimento a una sezione (da ignorare), un numero che non viene dal profilo (da ignorare).

Il motivo per cui questa direzione non è automatizzabile è la decisione D8: distinguere in prosa italiana un valore di profilo da una data richiederebbe l'estrazione euristica che FR-025 vieta.

### SC-006 — Il controllo fallisce quando deve

```bash
python3 scripts/check_audit_coherence.py; echo "esito su documento intatto: $?"   # atteso 0

cp docs/data_audit.md /tmp/audit_backup.md
# alterare a mano un singolo valore marcato, poi:
python3 scripts/check_audit_coherence.py; echo "esito su documento alterato: $?"  # atteso 1
cp /tmp/audit_backup.md docs/data_audit.md
```

Attesa: esito `0` sul documento intatto, esito `1` su quello alterato, con l'identificativo, il valore atteso e quello trovato nel messaggio. Un controllo che segnala senza fallire verrebbe ignorato (FR-034).

### SC-007 — Verificabile senza i dati di origine

```bash
mv data/raw /tmp/raw_hidden
python3 scripts/check_audit_coherence.py && echo "OK: funziona senza sorgenti"
python3 scripts/profile_data.py; echo "atteso errore esplicito: $?"
mv /tmp/raw_hidden data/raw
```

Attesa: il controllo di coerenza passa, perché confronta due artefatti entrambi versionati. Il profiling invece **fallisce con un errore che nomina il file mancante** e rimanda a `scripts/download_data.sh`, senza lasciare un artefatto parziale (FR-004).

### SC-008 — La risposta a R11

```bash
python3 -c "
import json; v=json.load(open('reports/data_profile.json'))['values']
print(v['NF.cat.count']['display'], 'categorie totali')
print(v['NF.cat.music.count']['display'], 'con contenuto musicale dichiarato')
"
```

Attesa: il numero di categorie musicali è nell'artefatto, e il documento dichiara il criterio di riconoscimento applicato più la conseguenza per la confidenza di `BQ1-K1`. La Fase 0 anticipa che la risposta sia **una sola** categoria (ritrovamento F1), ma il valore che conta è quello che lo script produce, non quello che la ricognizione ha visto.

### SC-009, SC-010, SC-011 — Lettura

Non hanno un comando e non devono averne uno.

- **SC-009**: si scorrono le otto misure del framework 001 e si verifica che il documento dica, per ciascuna, se i campi che la alimentano esistono e con quale completezza.
- **SC-010**: si confronta il blocco `divergences` dell'artefatto con la sezione delle divergenze del documento, e per ciascuna voce `diverge` o `ambiguo` si verifica che esista la nota corrispondente nell'artefatto della 001. La Fase 0 ne ha già due candidate: F2 (l'ambiguità di "circa un quinto") e F3 (il conteggio delle corrispondenze lessicali).
- **SC-011**: rilettura mirata alla ricerca di valori di KPI o risposte a BQ1, BQ2, BQ3. Attesa: nessuno.

### SC-012 — L'artefatto è tracciato

```bash
git check-ignore -v reports/data_profile.json; echo "esito: $? (atteso 1 = non ignorato)"
git ls-files --error-unmatch reports/data_profile.json && echo "OK: versionato"
```

Attesa: `git check-ignore` non restituisce nulla ed esce con `1`. È il controllo che impedisce al vincolo di essere annullato in silenzio da `.gitignore`, ed è la ragione per cui l'artefatto sta sotto `reports/` e non sotto `data/`.

## Ordine consigliato di verifica

1. `profile_data.py` due volte → SC-001, SC-002
2. ispezione dell'artefatto → SC-003, SC-004, SC-008, SC-012
3. lettura del documento → SC-009, SC-011
4. `check_audit_coherence.py` → SC-005 (parte automatica), SC-006
5. prova di alterazione e prova senza `data/raw/` → SC-006, SC-007
6. lettura degli avvisi e confronto delle divergenze → SC-005 (parte assistita), SC-010

I passi 1 e 5 modificano temporaneamente lo stato del repository o della cartella dei dati. Entrambi ripristinano ciò che hanno spostato: eseguirli fino in fondo, non interromperli a metà.
