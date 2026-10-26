---
layout: default
title: Copertura e fonti tecniche
permalink: /fonti/
---
<div class="prose" markdown="1">

# Copertura e fonti tecniche

VehicleData è un catalogo commerciale di informazioni automobilistiche curato da PACIFIC IT Solutions. Le schede conservano mercato, identificativo e provenienza dei dati.

| Mercato | Fonte | Contenuti |
|---|---|---|
| Svizzera | [ASTRA — Type Approval System](https://opendata.astra.admin.ch/ivzod/4000-Typengenehmigungen_TAS/4300-Datensaetze/) | Omologazioni autovetture M1/M1G, tipo/variante/versione, codice motore, kW, coppia, omologazione UE e CH, dimensioni, masse e pneumatici dove presenti |
| Francia | [ADEME — Car Labelling](https://data.ademe.fr/datasets/ademe-car-labelling) | Configurazioni commercializzate, potenza, cilindrata, cambio, masse e intervalli WLTP |
| Stati Uniti | [DOE / EPA — FuelEconomy.gov](https://www.fueleconomy.gov/feg/ws/index.shtml) | Configurazioni per anno modello, motorizzazione, cilindrata, cambio e consumi EPA |
| Canada | [Natural Resources Canada](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64) | Configurazioni per anno modello, cilindrata, cambio, consumi ed emissioni |

**La copertura attuale è limitata a questi quattro mercati e ai contenuti delle relative fonti. Non è un censimento completo di tutte le auto del mondo.** La presenza di una marca giapponese, cinese o coreana non equivale alla copertura del suo mercato nazionale. Italia, Germania e altri Paesi non vengono aggiunti come mercati sulla sola base di un’omologazione UE.

## Identificazione dei record

Gli ID iniziano con `ch-`, `fr-`, `epa-` oppure `ca-`. Un record può descrivere una configurazione, una voce di catalogo o una scheda di omologazione; non rappresenta necessariamente un modello unico. Le revisioni ASTRA sono distinte tramite numero di omologazione CH e numero di versione del documento.

Non uniamo record di mercati diversi usando solo marca e nome del modello. Non attribuiamo a una versione USA il codice motore o la potenza di una versione svizzera.

## Significato dell’anno

- **Anno modello:** indicato dalle fonti USA e Canada; può essere diverso dall’anno di produzione o prima immatricolazione.
- **Anno omologazione:** anno della data di approvazione ASTRA; non dimostra tutti gli anni di vendita della versione.
- **Anno catalogo:** anno dello snapshot ADEME; non è un anno modello dichiarato dal costruttore.

Il filtro “Anno di riferimento” usa il valore corrispondente al tipo indicato in ogni scheda.

## Codice motore, potenza e omologazione

Il codice motore ASTRA proviene dal campo `chEngineCodeAsMarkedOnTheEngine`, cioè il contrassegno motore registrato nella fonte. Il tipo motore è un campo separato. La potenza ASTRA è la potenza massima netta in kW; per ADEME è la potenza massima espressa in kW. La potenza elettrica nominale o continua è conservata separatamente e non sostituisce automaticamente la potenza di picco.

L’omologazione UE ASTRA proviene da `typeApprovalNumber`. Le estensioni iniziale e finale sono mostrate separatamente. L’omologazione CH non viene spacciata per un codice UE. Le schede possono essere storiche: quando disponibili mostriamo date di scadenza e annullamento.

I campi assenti sono indicati come “Non presente nella fonte”. Nessun valore viene dedotto dal nome commerciale. I filtri permettono di selezionare record che contengono codice motore, potenza e/o omologazione UE.

## Unità, categorie e limiti

Potenza in kW, cilindrata in litri, coppia in Nm e dimensioni in mm. Per la Svizzera la massa mostrata è la massa in ordine di marcia; per ADEME è il peso a vuoto della fonte. Eventuali intervalli sono conservati nei campi minimo/massimo disponibili.

Le descrizioni originali dei cambi e dei pneumatici possono essere in inglese, tedesco o francese. I codici combustibile ASTRA senza traduzione verificata restano esplicitamente etichettati come codici della fonte.

Consumi EPA in MPG statunitensi o MPGe e CO₂ in g/miglio. Dati canadesi in L/100 km e g/km; i valori 1995–2014 sono stime ricalcolate secondo la metodologia NRCan a cinque cicli. Gli intervalli ADEME riguardano configurazioni WLTP. Non sono misure direttamente equivalenti.

Sono escluse le classi camion, pickup, furgoni e minibus. L’importazione ASTRA seleziona autovetture tipo CH 10, categoria M1/M1G. Non vengono importati proprietari, targhe o VIN individuali.

## Attribuzione e condizioni delle fonti

- **ASTRA / USTRA:** dati tecnici delle omologazioni, distribuiti tramite la piattaforma ufficiale. Elaborazione e presentazione VehicleData; [condizioni e descrizione dei prodotti](https://www.astra.admin.ch/de/fahrzeugdaten).
- **ADEME:** Car Labelling, riutilizzato secondo la [licenza Etalab 2.0 indicata nel catalogo ufficiale](https://www.data.gouv.fr/datasets/ademe-car-labelling). Conversioni di etichette, selezione e presentazione VehicleData.
- **DOE / EPA:** FuelEconomy.gov; [descrizione e download della fonte](https://www.fueleconomy.gov/feg/ws/index.shtml).
- **Natural Resources Canada:** Fuel Consumption Ratings; riutilizzo secondo la [licenza del Governo del Canada](https://open.canada.ca/en/open-government-licence-canada). Il servizio non è affiliato né approvato dal Governo del Canada.

La natura commerciale del sito non modifica i diritti e le condizioni dei dati originari. La consultazione delle schede non costituisce certificazione del singolo veicolo. Per pratiche amministrative fanno riferimento i documenti ufficiali e il COC.

Per segnalare una correzione, comunica a [PACIFIC IT Solutions](https://pacificit.solutions) l’ID del record, il campo e la documentazione a supporto.

</div>
