# Quickstart — Feature 003: Data Cleaning & ETL

**Data**: 2026-08-11 | **Fase**: 1 (Design) | **Spec**: [spec.md](./spec.md)

Guida di verifica: come eseguire ciò che la feature produce e come accertare che i quindici criteri di successo siano soddisfatti. Non contiene codice di implementazione — quello vive negli artefatti del repository.

## Prerequisiti

**Python 3** e nulla d'altro. Nessuna dipendenza esterna, nessun ambiente virtuale: è la decisione T1 di [research.md](./research.md), ed è la ragione per cui questa guida non ha un passo di installazione.

Per rigenerare i dataset servono i dati di origine:

```bash
./scripts/download_data.sh   # richiede un token Kaggle
```

Per **tutto il resto** — leggere il documento, verificarne la coerenza, risalire da un numero alla sua fonte — i dati di origine non servono. È il punto di FR-041 e SC-013.

## I comandi

```bash
# 1. costruisce i dataset trasformati (richiede data/raw/)
python3 scripts/build_datasets.py

# 2. verifica la coerenza dei documenti con i due artefatti (NON richiede data/raw/)
python3 scripts/check_audit_coherence.py

# 3. verifica che l'artefatto di rendicontazione sia davvero tracciato da git
git check-ignore -v reports/cleaning_report.json   # non deve restituire nulla

# 4. verifica che nessun dataset di output sia tracciato
git status --porcelain data/                        # non deve restituire nulla
```

## Verifica dei criteri di successo

### SC-001 — Determinismo byte per byte

```bash
python3 scripts/build_datasets.py
mkdir -p /tmp/run_a && cp data/processed/*.csv /tmp/run_a/
python3 scripts/build_datasets.py
diff -r /tmp/run_a data/processed && echo "OK: identici"
```

**Atteso**: nessuna differenza. Include `reports/cleaning_report.json`, che va confrontato allo stesso modo.

**Il caso che questo comando non copre.** Due esecuzioni sulla stessa macchina condividono il locale di sistema. Il ritrovamento F6 mostra che una conversione di data dipendente dal locale passerebbe questo test e fallirebbe su un'altra macchina. La contromisura è la decisione T6 — tabella dei mesi esplicita — e la regola di lavoro che ne discende: **nessuna funzione dipendente dal locale entra nella pipeline**, né per le date, né per l'ordinamento, né per la formattazione dei numeri. Il test non può accorgersene; la revisione del codice sì.

### SC-002 — `data/raw/` immutato

```bash
find data/raw -type f -exec shasum -a 256 {} \; | sort > /tmp/raw_before.txt
python3 scripts/build_datasets.py
find data/raw -type f -exec shasum -a 256 {} \; | sort > /tmp/raw_after.txt
diff /tmp/raw_before.txt /tmp/raw_after.txt && echo "OK: sorgenti intatte"
```

### SC-003 — Le impronte registrate coincidono con i file rigenerati

```bash
python3 - <<'PY'
import json, hashlib, pathlib
rep = json.load(open('reports/cleaning_report.json'))
for o in rep['outputs']:
    h = hashlib.sha256(pathlib.Path(o['path']).read_bytes()).hexdigest()
    print(('OK  ' if h == o['sha256'] else 'DIFF'), o['path'])
PY
```

**Atteso**: `OK` su tutte le righe. È il meccanismo che sostituisce la versionatura degli output: chi rigenera i dati verifica di aver ottenuto gli stessi file senza che nessuno abbia committato un CSV.

### SC-004 — Nessun output versionato, artefatto di rendicontazione sì

```bash
git status --porcelain data/                       # atteso: vuoto
git check-ignore -v reports/cleaning_report.json   # atteso: nessun output
```

### SC-005, SC-006 — Decisioni dichiarate, decisioni ereditate chiuse

Verifica per lettura, non per comando. Si apre `docs/data_cleaning.md` e si controlla che:

- ciascuna delle **nove** decisioni di trattamento elencate in [data-model.md](./data-model.md) §2 abbia enunciato, ragione, effetto quantificato e ancora al profilo;
- ciascuna delle **cinque** decisioni ereditate D1-D5 sia dichiarata chiusa con la propria ragione.

**Il controllo automatico non copre questi due criteri**, e la ragione va detta invece che aggirata: verificare che una decisione sia *dichiarata* richiede di leggere la dichiarazione. Ciò che il comando 2 garantisce è che i numeri di quelle dichiarazioni siano veri, non che le dichiarazioni ci siano tutte.

### SC-007 — I denominatori cambiati sono tutti dichiarati

```bash
python3 - <<'PY'
import json
rep = json.load(open('reports/cleaning_report.json'))
doc = open('docs/data_cleaning.md').read()
for d in rep['denominators']:
    ok_old = d['profile_id'] in doc
    ok_new = d['cleaning_id'] in doc
    print(('OK  ' if ok_old and ok_new else 'MANCA'), d['profile_id'], '->', d['cleaning_id'])
PY
```

**Atteso**: `OK` su tutte le voci. Il blocco `denominators` è popolato dalla pipeline per ricalcolo e confronto (data-model §5), non a mano: se un denominatore è cambiato senza che nessuno se ne accorgesse, compare qui e questo comando lo segnala come mancante nel documento.

### SC-008 — Nessun campo omesso in silenzio

```bash
python3 - <<'PY'
import json, csv
prof = json.load(open('reports/data_profile.json'))
doc  = open('docs/data_cleaning.md').read()
for key, ds in (('netflix_fields','netflix'), ('spotify_fields','spotify')):
    for f in prof['catalogs'][key]:
        name = f['name'] or '(colonna senza nome)'
        print(('OK  ' if (f['name'] and f['name'] in doc) or not f['name'] else 'VERIFICA'), ds, name)
PY
```

I campi presenti negli output si verificano nell'intestazione dei CSV; quelli assenti devono comparire fra le esclusioni del documento. La colonna senza nome del catalogo musicale (T11) è l'unica esclusione attesa.

### SC-009 — Le grane sono uniche

```bash
python3 - <<'PY'
import csv, collections
attese = {
  'data/processed/netflix_titles.csv':        ('show_id',),
  'data/processed/netflix_title_category.csv':('show_id','category'),
  'data/processed/spotify_track_genre.csv':   ('track_id','track_genre'),
  'data/processed/spotify_tracks.csv':        ('track_id',),
}
for path, key in attese.items():
    rows = list(csv.DictReader(open(path, encoding='utf-8')))
    chiavi = collections.Counter(tuple(r[k] for k in key) for r in rows)
    dup = sum(v-1 for v in chiavi.values() if v > 1)
    print(('OK  ' if dup == 0 else f'DUP {dup}'), path, '/'.join(key), len(rows), 'righe')
PY
```

**Atteso**: `OK` su tutti e quattro. La pipeline verifica la stessa cosa e si ferma se fallisce (T10): questo comando è la verifica indipendente, non il presidio.

### SC-010 — Nessuna riga eliminata se non per deduplicazione

```bash
python3 - <<'PY'
import csv, json
prof = json.load(open('reports/data_profile.json'))['values']
nf = sum(1 for _ in csv.DictReader(open('data/processed/netflix_titles.csv', encoding='utf-8')))
sp = sum(1 for _ in csv.DictReader(open('data/processed/spotify_track_genre.csv', encoding='utf-8')))
print('video   :', nf, 'atteso', int(prof['NF.shape.rows']['value']), 'OK' if nf == prof['NF.shape.rows']['value'] else 'DIFF')
print('musica  :', sp, 'atteso', int(prof['SP.shape.rows']['value']), '- meno le righe rimosse dalla dedup di coppia')
PY
```

**Atteso**: il catalogo video ha esattamente le righe del profilo — nessuna eliminazione, nemmeno delle tre riparate. Il catalogo musicale alla grana coppia ne ha di meno, e la differenza deve coincidere con `CL.SP.pair.removed_rows`.

### SC-011, SC-012 — Ancoraggio e severità del controllo

```bash
# 1. stato pulito
python3 scripts/check_audit_coherence.py; echo "uscita: $?"     # atteso 0

# 2. alterazione di un valore ancorato
cp docs/data_cleaning.md /tmp/doc.bak
# si modifica a mano una cifra che porta un'ancora, poi:
python3 scripts/check_audit_coherence.py; echo "uscita: $?"     # atteso != 0, con il valore nominato

# 3. numerale non ancorato in un documento della 003
#    si aggiunge una frase con una cifra priva sia di ancora sia di <!--#-->, poi:
python3 scripts/check_audit_coherence.py; echo "uscita: $?"     # atteso != 0

cp /tmp/doc.bak docs/data_cleaning.md
```

**Attenzione alla prova 3**: la severità è diversa fra i due documenti (contratto §3.2). La stessa frase inserita in `docs/data_audit.md` produce un avviso e uscita `0`; inserita in `docs/data_cleaning.md` produce un errore. Se la prova non discrimina, la severità non è stata implementata per documento ed è il difetto da correggere.

### SC-013 — Verificabile senza i dati

```bash
mv data/raw /tmp/raw_stash
python3 scripts/check_audit_coherence.py; echo "uscita: $?"   # atteso 0
mv /tmp/raw_stash data/raw
```

**Atteso**: il controllo funziona. È la prova che il documento poggia su artefatti versionati e non sui dati.

### SC-014 — Nessun KPI, nessuna misura di posizione della popolarità per genere

```bash
grep -nE 'BQ[123]-K[0-9]' docs/data_cleaning.md          # solo riferimenti al perimetro, mai valori
grep -niE 'mediana|media|quartile' docs/data_cleaning.md # nessuna occorrenza riferita alla popolarità per genere
python3 - <<'PY'
import json
v = json.load(open('reports/cleaning_report.json'))['values']
sospetti = [k for k in v if any(t in k for t in ('.median','.mean','.q1','.q3'))]
print('valori di posizione in cleaning_report:', sospetti or 'nessuno')
PY
```

**Atteso**: nessun valore di posizione della popolarità. È il presidio della decisione ereditata D4, che ha scelto la quota di zeri proprio per non pubblicare una mediana a un passo da `BQ2-K1`.

### SC-015 — Le note in loco esistono e non cancellano nulla

```bash
git diff main -- docs/business_case.md docs/data_audit.md
```

**Atteso**: solo righe **aggiunte**. Zero righe rimosse, zero righe modificate. È la prassi di `CLAUDE.md`: il valore originale resta, la nota gli sta accanto. Una riga rimossa in questo diff è una violazione, non una rifinitura.

## Riepilogo della copertura

| Criterio | Come si verifica |
|---|---|
| SC-001, SC-002, SC-003 | comando, confronto di file e impronte |
| SC-004, SC-009, SC-010 | comando |
| SC-005, SC-006 | **lettura** — nessun comando li copre |
| SC-007, SC-008 | comando, con lettura di conferma sulle esclusioni |
| SC-011, SC-012, SC-013 | comando, incluse due prove di alterazione |
| SC-014 | comando, con lettura di conferma sui riferimenti al perimetro |
| SC-015 | comando su diff |

Due criteri su quindici non ammettono un comando, e la ragione è la stessa per entrambi: verificano che qualcosa sia *dichiarato*, e una dichiarazione si legge. È il confine della verifica automatica in questa feature, dichiarato qui e ripetuto nel documento come FR-033 richiede.
