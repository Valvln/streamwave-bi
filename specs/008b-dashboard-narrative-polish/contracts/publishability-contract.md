# Contratto di pubblicabilità: che cosa la `010` può presupporre sul `.pbix`

**Feature**: 008b-dashboard-narrative-polish | **Data**: 2026-08-28

## Perché questo documento è scritto dopo la costruzione e non prima

Il contratto di narrazione è stato scritto **prima** che Power BI venisse riaperto, ed è un vincolo. Questo è scritto **dopo**, ed è un accertamento: dichiara che cosa esiste, non che cosa deve esistere.

L'ordine è deliberato e corregge un difetto della `008a`, che scrisse il proprio `dashboard-contract.md` in Fase 1 e dovette riallinearlo al risultato reale in coda alla feature (`T036` di quella lista). Un contratto che dichiara un file pubblicabile e viene scritto prima di guardarlo non accerta: ratifica.

**Il criterio contro cui l'accertamento è stato fatto è però anteriore**, ed è `N8` di [spec.md](../spec.md), fissato prima di costruire. Le due cose stanno insieme: il metro è di prima, la misura è di dopo.

**Che cosa questo documento non è**: la fonte autorevole su ciò che esiste a schermo. Quella è la sezione «Esito della costruzione» di [quickstart.md](../quickstart.md), e dove i due divergono prevale quella.

> **Nota in loco — 2026-08-29, feature `008b`. La dichiarazione di pubblicabilità è ritirata.**
>
> **Affermazione precedente**: il `.pbix` è pubblicabile dal 2026-08-28, e la `010` può presupporre su di esso ciò che la §1 elenca.
>
> **Affermazione corretta**: il `.pbix` **non è dichiarato pubblicabile**. Tutto ciò che questo documento accerta — le otto voci della §1, le cinque condizioni di `N8` verificate in [quickstart.md](../quickstart.md) — resta un accertamento vero su che cosa esiste nel file. Ciò che cade è la conclusione che se ne traeva: che quel file possa essere mostrato a chi non ha letto nulla di questo repository senza che ne tragga una conclusione che i dati non sostengono.
>
> **Causa della divergenza**: la §4 di questo stesso documento elenca **la revisione in contesto pulito come il primo dei tre presidi** su cui la garanzia poggia. Quella revisione è tornata con venticinque rilievi e un no sul metro dichiarato — la leggibilità per un decisore che non ha letto alcun documento del repository. Un presidio che si nomina come fondamento e si ignora quando risponde no non è un presidio.
>
> **Che cosa non è caduto: il criterio.** `N8` non era sbagliato ed era stato fissato **prima** di costruire; il revisore lo dice per primo, e le cinque condizioni sono state verificate una per una senza allargarne nessuna. Quello che è caduto è **la misura, non il metro**. Le due obiezioni riguardano la *ragione in una riga*, che prometteva sul lettore più di quanto le cinque condizioni sostengano (`R6`), e la *tempistica*, cioè una riga della legenda di confidenza tronca a schermo il giorno stesso della dichiarazione (`R5b`). Nessuna delle due chiedeva di riscrivere `N8`.
>
> **Perché la riparazione non è stata fatta.** La regia ha deciso il 2026-08-28 che la dashboard a quattro pagine è **superata**: non viene rifinita, viene sostituita da un report a 8-12 pagine disegnato lungo la spina di una raccomandazione che il progetto non ha ancora scritto (`009`, `010a`, `010b`). Riparare la riga tronca significherebbe rifinire un artefatto che non andrà a schermo. La riga tronca si **dichiara**, non si ripara.
>
> **Fonte verificabile**: [`review.md`](../review.md) — rilievi `R5b` e `R6`, §5 «Giudizio complessivo sul metro dichiarato», e il blocco di chiusura in coda al verbale.

---

## 1. Che cosa la `010` può presupporre

Il case study leggerà questo repository da fuori e **non potrà aprire il `.pbix`**: non è versionato, non è rigenerabile da una copia pulita, ed è la conseguenza dichiarata del principio V. Ciò che segue è quindi tutto ciò su cui può poggiare.

| Presupposto | Dove è accertato |
|---|---|
| quattro pagine — ingresso, `BQ1`, `BQ2`, `BQ3` — invariate rispetto alla `008a` | prova 3, chiusa da `T026` |
| otto KPI a schermo, ciascuno con la propria etichetta di fonte e confidenza nella forma di `business_case.md` §5.4 | contratto di pagina `008a` §1.1, più la correzione `SC-2` di questo esito |
| il *perché* di ogni livello di confidenza, per tutti e otto | condizione 2 di `N8`, verificata |
| l'assunzione strutturale dei proxy sulla pagina di ingresso | `BL-IN-1`, condizione 1 di `N8` |
| i limiti dichiarati su tutte e quattro le pagine, in forma non tecnica | prova 4, esaustività in entrambe le direzioni |
| trentadue blocchi di narrazione, il cui testo letterale vive in [narrative-contract.md](./narrative-contract.md) | il contratto è nel repository: chi non può aprire il file può leggere che cosa dice |
| nessun verdetto sulla regola di decisione della North Star | prova 7 |
| quattordici misure, otto tabelle, cinque relazioni, nessun filtro né slicer | prova 3 |

**Il punto che rende questa lista utile alla `010`**: il testo a schermo esiste nel repository **prima** di esistere nel file. Chi scrive il case study non deve descrivere una dashboard che non può vedere — può citare il contratto.

## 2. Che cosa «pubblicabile» non significa

Ripetuto qui perché questo documento verrà letto da solo, e la metà rassicurante di un'affermazione viaggia più veloce dell'altra.

- **Non** significa pubblicato. Il `.pbix` resta locale e non versionato; nessuna pubblicazione sul servizio è nel perimetro di alcuna feature.
- **Non** significa che le issue aperte siano chiuse. Sette lo sono e restano tali (§3).
- **Non** significa che il debito della `004` sulla verificabilità del benchmark sia risolto. È aperto, ed è dichiarato **a schermo** da `BL-Q3-9` — che è ciò che rende il file mostrabile, non ciò che lo impedisce.
- **Non** significa che i numeri descrivano StreamWave. Non lo fanno, e la pagina di ingresso lo dice per prima.
- **Non** significa che tutto il testo si legga in un colpo d'occhio. Le caselle **scorrono** (`SC-3`): niente è dietro un clic, ma chi non scorre non legge la seconda metà di un blocco.
- **Non** significa che ogni limite assegnato a questa feature sia a schermo **per intero**. Tre di essi dicono meno di quanto la fonte prescriva, e l'elenco è nella §13.1 di [narrative-contract.md](./narrative-contract.md).

## 3. Le issue che restano aperte

Nessuna è chiusa da questa feature. `#11`, `#17`, `#18`, `#20`, `#21` sono ereditate; `#26` e `#27` sono aperte qui. Lo stato di ciascuna, con l'evidenza che le manca, è nella sezione «Lo stato delle cinque issue» di [quickstart.md](../quickstart.md).

**Quella che la `010` deve conoscere prima delle altre è `#20`**: dichiara che tre impostazioni del modello possono riperdersi a ogni riapertura del file, e non è chiudibile finché il `.pbix` non è versionato. Chiunque riapra quel file rifà le tre verifiche, o scrive prosa accanto a numeri che potrebbero non essere più quelli.

## 4. Su che cosa poggia questa garanzia

**Su tre presidi umani e su nessuno script.**

1. **La revisione in contesto pulito** su contratto ed esito, il cui metro dichiarato non è la conformità agli obblighi ma la leggibilità per il destinatario.
2. **Le undici prove manuali** di [quickstart.md](../quickstart.md), di cui sette confrontano un testo con un altro testo e una verifica un'esaustività. Sono verifiche di lettura, non di misura.
3. **La disciplina con cui gli scostamenti sono stati scritti mentre accadevano**, invece che ricostruiti a memoria alla fine.

> **Nota in loco — 2026-08-29, feature `008b`. Il conteggio del presidio 2 è sbagliato, e il presidio 1 ha risposto no.**
>
> **Affermazione precedente**: *«Le undici prove manuali»*.
>
> **Affermazione corretta**: le prove manuali effettivamente eseguite sono **dieci**. Delle dodici prove di [quickstart.md](../quickstart.md), la 1 è **eseguibile** — è `check_audit_coherence.py`, che questo stesso documento esclude dai presidi sei righe più sotto — e la 12 è dichiarata **non eseguita**.
>
> **Causa della divergenza**: un conteggio a memoria in una sezione di sintesi, in un documento la cui tesi è che nessun numero sta senza fonte. Il numero originale resta sopra perché è la traccia di ciò che il documento affermava.
>
> **Sul presidio 1, e vale più del conteggio**: la revisione in contesto pulito ha avuto luogo ed è tornata con un no. La garanzia che questa §4 sostiene è **ritirata** — vedi la nota in apertura del documento.
>
> **Fonte verificabile**: la tabella «L'esito delle dodici prove» di [quickstart.md](../quickstart.md), e il rilievo `R18` caso 4 di [`review.md`](../review.md).

**`scripts/check_audit_coherence.py` non è fra i presidi.** Non entra nel `.pbix` e non legge `specs/`: il suo verde riguarda le ancore dei sette documenti pubblicati, e il deliverable di questa feature è la sola cosa del repository che quel controllo non può leggere per costruzione.

**Che cosa nessuno dei tre presidi garantisce**: che un lettore reale, davanti allo schermo, capisca. Contro questo non esiste presidio dentro il processo — solo un lettore reale.
