# Data Model — Feature 002: Data Audit & Profiling

**Data**: 2026-08-09 | **Fase**: 1 (Design) | **Spec**: [spec.md](./spec.md)

Le entità di questa feature non sono tabelle di un modello dati analitico: il modello dati del progetto è la feature 005. Qui sono gli oggetti che il profiling produce e che il controllo di coerenza verifica. La loro forma serializzata è fissata in [contracts/profile-artifact.md](./contracts/profile-artifact.md); questo documento ne descrive semantica, relazioni e vincoli di integrità.

## Entità

### Sorgente

Un file di `data/raw/` sottoposto a profiling.

| Attributo | Descrizione |
|---|---|
| percorso | posizione relativa alla radice del repository |
| dimensione | byte |
| impronta | digest del contenuto |

**Vincoli**: una sorgente è **immutabile** (principio II). Il profiling la legge e non vi scrive. Due artefatti sono confrontabili solo se le loro sorgenti hanno la stessa impronta: è ciò che distingue "il numero è cambiato" da "i dati sono cambiati".

**Cardinalità**: due, fissate dalla constitution nella sezione delle fonti ammesse. La feature non ne aggiunge.

---

### Campo

Una colonna di una sorgente.

| Attributo | Descrizione |
|---|---|
| nome | come compare nell'intestazione. **Può essere vuoto** — vedi F5 in [research.md](./research.md) |
| tipo osservato | dedotto dai valori presenti, non dichiarato dalla fonte |
| completezza | conteggio e quota di valori mancanti, secondo la convenzione dichiarata |
| cardinalità | valori distinti |
| multi-valore | se una singola cella contiene più valori atomici |

**Vincoli**:

- ogni campo di ogni sorgente è profilato **oppure** elencato fra le esclusioni con la ragione (FR-019). Non esiste una terza possibilità;
- un campo multi-valore produce conteggi in **due** granularità, entrambe dichiarate (FR-018);
- il tipo osservato non è una promessa sul dominio: F4 mostra un campo di classificazione che contiene durate. Il tipo descrive ciò che c'è, non ciò che dovrebbe esserci.

---

### Valore di profilo

L'unità atomica dell'artefatto e il fulcro dell'intera feature: è ciò che il documento cita e ciò che il controllo verifica.

| Attributo | Descrizione |
|---|---|
| identificativo | stabile e univoco, secondo la convenzione del contratto |
| valore | il numero grezzo |
| forma di visualizzazione | la stringa esatta che il documento deve scrivere |
| unità | conteggio, percentuale, minuti, secondi, byte |
| granularità | su cosa è calcolato, dove non è univoco |
| etichetta | descrizione breve, **senza** interpretazione |

**Vincoli di integrità**:

1. **stabilità**: l'identificativo non cambia quando cambia il valore. Un identificativo che cambiasse con il dato renderebbe impossibile vedere in un diff che un numero si è mosso;
2. **univocità**: nessun identificativo compare due volte;
3. **una forma, un identificativo**: la stessa quantità in due letture (percentuale e frazione) è due valori. Il documento non riformula mai a mano;
4. **nessuna interpretazione**: l'etichetta descrive il calcolo, non la conseguenza (FR-010);
5. **rigenerabilità**: ogni valore è prodotto dallo script. Nessun valore è scritto a mano nell'artefatto (FR-011).

**Relazioni**: un valore appartiene a una Sorgente e, dove pertinente, a un Campo. I valori che attraversano entrambe le sorgenti non appartengono a nessun Campo singolo.

---

### Categoria del catalogo video

Un'etichetta della classificazione assegnata dalla fonte.

| Attributo | Descrizione |
|---|---|
| nome | l'etichetta, come la fonte la scrive |
| titoli distinti | quanti titoli la portano |
| contenuto musicale dichiarato | se l'etichetta dichiara contenuto musicale |

**Vincoli**:

- il censimento è **completo**: tutte le categorie, nessuna selezione a monte (FR-021). È la condizione perché la risposta a R11 sia verificabile e non asserita;
- la somma dei titoli per categoria **supera** il totale dei titoli, perché un titolo porta più etichette. Il profilo dichiara la granularità di ciascun conteggio invece di lasciar credere che siano sommabili;
- l'attributo "contenuto musicale dichiarato" è assegnato secondo un criterio esplicito, dichiarato nel documento di audit. È l'unico attributo di questa entità che non sia lettura diretta, ed è per questo che il criterio va scritto.

---

### Ritrovamento

Un fatto osservato che vincola il lavoro a valle. Vive nel documento di audit, poggia sull'artefatto.

| Attributo | Descrizione |
|---|---|
| enunciato | cosa si è osservato |
| valori a sostegno | gli identificativi che lo reggono |
| conseguenza | cosa vincola per le feature successive |

**Vincoli**: ogni ritrovamento cita almeno un valore di profilo tramite marcatore. Un ritrovamento senza numero a sostegno è un'opinione, ed è esattamente la condizione che il rilievo R8 contestava alla 001.

---

### Affermazione della 001

Un numero che la 001 cita in prosa e che questa feature rigenera. Sono i quattordici dell'inventario di FR-020.

| Attributo | Descrizione |
|---|---|
| sigla | `V01`-`V14` |
| enunciato | come la 001 lo scrive |
| collocazione | documento e sezione in cui compare |
| valori che lo rigenerano | uno o più identificativi |

**Vincoli**: ogni sigla dell'inventario si risolve su almeno un valore esistente. È il vincolo che rende SC-003 verificabile da una macchina.

---

### Divergenza

Uno scarto fra un'Affermazione della 001 e i valori che la rigenerano.

| Attributo | Descrizione |
|---|---|
| affermazione | la sigla interessata |
| valore citato | come la 001 lo scriveva |
| valore rigenerato | cosa dice il profilo |
| stato | `coincide`, `diverge`, `ambiguo` |
| ipotesi sulla causa | perché i due non tornano |
| nota di correzione | riferimento alla nota applicata all'artefatto della 001 |

**Vincoli**:

- lo stato `ambiguo` esiste perché è già occorso in Fase 0: l'affermazione F2 non è né vera né falsa, è sotto-determinata. Costringerla in `coincide` o `diverge` significherebbe scegliere per conto della 001 quale delle due letture intendeva;
- ogni divergenza con stato `diverge` o `ambiguo` ha una nota corrispondente nell'artefatto della 001 (FR-031). Zero divergenze registrate senza nota;
- il valore originale della 001 non viene cancellato: la nota affianca, non sostituisce.

## Diagramma delle relazioni

```
Sorgente ──1:N── Campo ──1:N── Valore di profilo
    │                              │
    │                              │ citato da (marcatore)
    │                              ▼
    └──1:N── Categoria         Ritrovamento
             (solo NF)             (documento di audit)

Affermazione 001 ──1:N── Valore di profilo
        │
        └──0:1── Divergenza ──0:1── Nota di correzione (artefatto 001)
```

## Cosa questo modello non contiene

Nessuna entità rappresenta un titolo, una traccia o un genere come **riga di dato**. Il profiling non materializza i dataset: li legge e ne emette misure aggregate. Le entità di dominio — titolo, traccia, segmento — appartengono al modello dati della feature 005, e introdurle qui anticiperebbe decisioni che questa feature non ha il contesto per prendere.
