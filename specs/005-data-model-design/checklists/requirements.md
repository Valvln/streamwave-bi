# Specification Quality Checklist: Data Model Design

**Purpose**: validare completezza e qualità della spec prima di passare alla pianificazione
**Created**: 2026-08-17
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] Nessun dettaglio di implementazione (linguaggi, framework, API)
- [x] Centrata sul valore per l'utente e sul bisogno di business
- [x] Scritta per un lettore non tecnico
- [x] Tutte le sezioni obbligatorie compilate

**Nota su «nessun dettaglio di implementazione».** La spec nomina Power BI Desktop come strumento di destinazione e nomina i quattro dataset di `data/processed/`. Non è una fuga di implementazione: lo strumento è fissato dalla constitution (principio V) e dalla roadmap, e i dataset sono l'ingresso dichiarato della feature. La spec non nomina alcun nome di tabella, di colonna o di misura: quelli sono l'esito, e vivono nel piano e nel documento.

## Requirement Completeness

- [x] Nessun marcatore `[NEEDS CLARIFICATION]` residuo
- [x] Requisiti verificabili e non ambigui
- [x] Criteri di successo misurabili
- [x] Criteri di successo indipendenti dalla tecnologia
- [x] Scenari di accettazione definiti per tutte e tre le storie
- [x] Casi limite identificati
- [x] Perimetro delimitato in modo esplicito
- [x] Dipendenze e assunzioni identificate

**Nota su `SC-004`.** Nomina `scripts/check_audit_coherence.py`, che è uno script del repository e non una tecnologia. Il criterio resta verificabile da chi non conosce lo script: termina con esito positivo, oppure no.

## Feature Readiness

- [x] Ogni requisito funzionale ha un criterio di accettazione riconducibile
- [x] Gli scenari coprono i flussi principali
- [x] La feature soddisfa i risultati misurabili dichiarati
- [x] Nessun dettaglio di implementazione filtrato nella spec

## Gate di feature — Constitution

- [x] **Principio VI**: la spec dichiara a quale domanda di business risponde e in che modo vi contribuisce. Il ponte è scritto per esteso, non asserito
- [x] **Principio IV**: sezione «Limiti Dichiarati» compilata, e dichiara cosa il modello rende **impossibile** misurare oltre a cosa abilita
- [x] **Principio I**: sezione «Provenienza e Confidenza» compilata per ogni struttura introdotta, con la dichiarazione esplicita che la feature non introduce metriche
- [x] **Principio III**: verificato sul piano — la stima rivista è risultata dentro le 6-7 ore, e la scomposizione `005a`/`005b` non si è attivata

## Note

- Il riquadro del principio III è stato spuntato in fase di rifinitura, sulla stima del piano. Lo **scostamento fra quella stima e il lavoro effettivo** è materia del riporto alla regia, non di questa lista: qui si verifica che la feature fosse dimensionata come una giornata, non quanto sia poi costata.
- Due esiti della spec vanno approvati dalla regia prima di procedere: la decisione `D1` su «segmento» e la domanda sulla materializzazione del modello (ritrovamento `F2`).
