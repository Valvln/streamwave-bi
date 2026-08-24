# Contratto: cosa `008b` e `010` possono presupporre sul `.pbix` costruito dalla `008a`

**Feature**: 008a-dashboard-model-pages | **Data**: 2026-08-24

Come i contratti della `007a` e della `007b`, non è un'interfaccia software: è il contratto di lettura fra questa feature e le due che la useranno — `008b` (narrazione, limiti a schermo, rifiniture) e `010` (case study e portfolio). Dichiara che cosa possono dare per garantito senza riaprire questa feature, e che cosa resta a loro carico.

**Una differenza rispetto ai due contratti precedenti, ed è la più importante.** Quelli garantivano proprietà di artefatti versionati, verificabili da chiunque eseguendo uno script. Questo garantisce proprietà di **un file binario non versionato che vive su una macchina sola**. Nessuno script può controllarlo, e la garanzia poggia interamente su tre presidi umani: il contratto di pagina scritto prima della costruzione, la sezione di esito scritta dopo, la revisione in contesto pulito su entrambi. Chi legge questo documento deve saperlo prima di fidarsene.

**Stato**: scritto in fase di piano contro la spec approvata; **va riallineato all'esito reale nel blocco D**, dopo la costruzione. Fino ad allora dichiara ciò che la feature si impegna a produrre, non ciò che ha prodotto.

## Che cosa la `008a` garantisce

1. **Tutti e otto i KPI sono a schermo**, nessuno mancante e nessuno in più, ciascuno con il valore pubblicato da `docs/kpi_measures.md` (`FR-011`).
2. **Ogni KPI porta accanto la propria etichetta di fonte e di confidenza**, nella forma di `business_case.md` §5.4 (`F5`, `FR-012`). La `008b` eredita etichette già presenti: il suo compito è spiegarle, non aggiungerle.
3. **Nessun valore a schermo esiste a una grana non pubblicata.** Le grane sono tre — catalogo intero, segmento, scenario — e nessuna interazione offerta dalle pagine ne produce una quarta (`F2`, `FR-019`). In particolare nessuna pagina che espone `BQ1-K3` offre un filtro di categoria video, che è la forma in cui l'issue `#18` è neutralizzata.
4. **La graduatoria di `BQ2-K3` espone tutti i 114 segmenti**, senza troncamenti, con la regola dei pari merito preservata e la quota di zeri accanto a ogni indice di domanda (`F3`, `FR-015`, `FR-016`). I sette segmenti `is_high_zero_genre` portano l'avvertimento accanto al nome.
5. **`BQ3` è a schermo solo come intervallo a tre scenari**, mai come valore singolo, e nessuna visuale moltiplica l'uplift per una base utenti o per una durata (`F4`, `FR-013`, `FR-014`).
6. **Le due soglie del quadrante, dove compaiono, sono misure e non costanti digitate**, e la loro lettura è stata confrontata una volta con i valori pubblicati in `kpi_measures.md` §7.1 (`F7`). L'esito di quel confronto è dichiarato nella sezione di esito.
7. **Nessuna visuale rende possibile una delle tre letture prive di significato** dichiarate da `data_model.md` §18: conteggio di righe per segmento, somma di una quantità su più segmenti, asse temporale (`FR-018`).
8. **I nomi delle misure nel modello sono i nomi semantici** di `business_case.md` §5.1 (`F8`). Chi scrive una visuale nuova trova il vocabolario già usato da cinque documenti pubblicati.
9. **Le colonne di mood sono state verificate nel dominio `0-1` prima che la prima pagina fosse costruita** (`FR-007`), e l'esito è dichiarato.
10. **Ogni differenza fra il disegno approvato e ciò che esiste è elencata** nella sezione di esito, con la propria ragione (`F9`, `FR-023`).

## Che cosa la `008a` non garantisce, e resta a carico di `008b` e `010`

1. **Che il `.pbix` sia pubblicabile.** Non lo è: alla chiusura di questa feature mancano a schermo i limiti dichiarati (principio IV), l'assunzione strutturale dei proxy che la constitution impone in ogni artefatto rivolto all'utente finale, e la narrazione. È il deliverable della `008b`, ed è registrato come deviazione consapevole nel Complexity Tracking di [plan.md](../plan.md). **Il file è leggibile, non pubblicabile**, e non va mostrato a un lettore esterno prima che la `008b` chiuda.
2. **Che i limiti tecnici siano comprensibili a chi guarda una pagina.** Le etichette di fonte e confidenza ci sono; il *perché* di quella confidenza no. `kpi_operators.md` §12 assegna esplicitamente questo alla `008b`.
3. **Che la regola di decisione della North Star sia esponibile.** Non lo è: `C2` non esiste come valore ancorato in alcun artefatto, ed è parte dell'issue `#17`. Le pagine portano `C1` e `C3` accanto al proprio KPI e nessun verdetto congiunto (`F6`). **La `008b` non può scrivere «due condizioni su tre» né «tre su tre» finché `C2` non è pubblicata**: sarebbe un'affermazione derivata senza ancora, che la regola di `convenzioni-marcatura.md` §7 vieta.
4. **Che l'issue `#18` sia chiusa.** Non lo è. La formula di `mood_profile_overlap` è quella pubblicata, ancora priva dell'`ALL` sul filtro di categoria. Chiunque, in `008b` o dopo, voglia esporre `BQ1-K3` in un contesto filtrabile per categoria deve prima chiudere quell'issue: **non può presupporre che la misura regga il filtro solo perché nessuna pagina attuale lo offre.**
5. **Che l'issue `#11` sia chiusa.** La tipizzazione è stata verificata una volta, su una materializzazione. Il `.pbix` non è versionato e nessun controllo del repository entra nel modello: chi lo riapre, o chi lo ricostruisce, deve rifare la verifica. Costa una lettura.
6. **Che il debito della `004` sulla verificabilità del benchmark sia risolto.** Non lo è, ed è una decisione di governance che questa feature non poteva prendere. I valori di `BQ3` vanno a schermo con quel debito aperto, ed è dichiarato.
7. **Che le pagine costruite siano quelle disegnate**, se la sezione di esito elenca scostamenti. Chi legge questo contratto deve leggere anche quella sezione: **il disegno approvato non è la fonte autorevole su ciò che esiste, l'esito lo è.**
8. **Che il file esista sulla macchina di chi legge.** Il `.pbix` non è versionato (`FR-029`) e non è rigenerabile da una copia pulita del repository — è la conseguenza dichiarata del principio V. `010` deve prevederlo: ciò che il repository contiene è il disegno e l'esito, non il file.

## Come si verifica che il contratto è rispettato

Che la `008a` abbia costruito ciò che dichiara si verifica con [quickstart.md](../quickstart.md), le cui prove sono per la maggior parte **manuali per costruzione**: richiedono il `.pbix` aperto, e nessuno script di questo repository potrà mai eseguirle.

Che `008b` e `010` abbiano letto correttamente questo contratto si verificherà quando quelle feature apriranno la propria spec e dichiareranno, pagina per pagina, che cosa aggiungono e su che cosa poggiano. Non è verificabile da questa feature, che si ferma alla costruzione e al suo esito.
