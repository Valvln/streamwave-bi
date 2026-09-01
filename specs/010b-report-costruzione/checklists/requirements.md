# Specification Quality Checklist: il report che porta l'argomento a schermo — costruzione

**Purpose**: validare la completezza e la qualità della spec prima di passare al piano
**Created**: 2026-08-29
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] Nessun dettaglio di implementazione (linguaggi, framework, API)
- [x] Centrata sul valore per chi legge e sul bisogno di business
- [x] Scritta per chi non costruisce
- [x] Tutte le sezioni obbligatorie completate

**Nota sulla prima voce, che in questa feature va argomentata.** La spec nomina misure DAX, visuali e Power BI. **Non è un dettaglio di implementazione che sfugge**: è il deliverable. Una feature che costruisce un report non può dichiarare che cosa deve esistere senza nominare le entità di cui il report è fatto, e il contratto di pagina della `010a` — approvato — le nomina per prime. Ciò che la spec **non** contiene è il come: nessuna formula DAX scritta, nessuna sequenza di clic, nessuna scelta di colore o di carattere.

## Requirement Completeness

- [x] Nessun marcatore [NEEDS CLARIFICATION] rimasto
- [x] Requisiti verificabili e non ambigui
- [x] Criteri di successo misurabili
- [x] Criteri di successo indipendenti dalla tecnologia
- [x] Scenari di accettazione definiti
- [x] Casi limite identificati
- [x] Perimetro chiaramente delimitato
- [x] Dipendenze e assunzioni dichiarate

**Sui criteri di successo indipendenti dalla tecnologia.** `SC-001`, `SC-002` e `SC-005` sono verificabili leggendo, senza sapere che lo strumento è Power BI. `SC-003`, `SC-004` e `SC-007` nominano proprietà del report — coincidenza dei valori con le ancore, raggiungibilità delle pagine, grana dei valori — che sarebbero le stesse su qualunque strumento.

**Su `SC-002`, che è il criterio più esposto.** «Zero limiti orfani» è verificabile contando: si prende ogni limite scritto e si cerca l'affermazione positiva accanto. È il conteggio che la revisione della `008b` ha fatto e che ha prodotto il numero da cui l'issue `#28` nasce.

## Feature Readiness

- [x] Ogni requisito funzionale ha un criterio di accettazione chiaro
- [x] Gli scenari coprono i flussi principali
- [x] La feature soddisfa gli esiti misurabili dei criteri di successo
- [x] Nessun dettaglio di implementazione filtra nella spec

## Notes

**Tre esiti che questa spec non può garantire e che dichiara come tali**, e sono la ragione per cui il piano prevede tre punti di fermata invece di due:

1. **`CP-3`** — la sincronizzazione della selezione fra le pagine 7 e 8 poggia su un accertamento precedente **contrario** (issue `#21`). La spec ne fa un caso limite, non un requisito che si assume soddisfatto;
2. **la tenuta di una visuale davanti allo schermo** — prevista dal disegno come possibile scostamento (§19 del contratto di pagina), non come difetto;
3. **la stima** — `~8` ore di roadmap, la più incerta del progetto: le due feature GUI precedenti hanno sforato di quasi il doppio entrambe. Se il lavoro risultasse più grande, la spec prescrive di **fermarsi e riportarlo** invece di comprimere, ed è `SC-001` a stabilire che cosa la compressione distruggerebbe per primo.

Nessuna voce risulta incompleta. La spec è pronta per il punto di fermata 1 — la revisione prima che diventi un piano.
