---
layout: default
title: Fonti e metodo
permalink: /fonti/
---
<div class="prose" markdown="1">

<p class="eyebrow blue">CONOSCERE I LIMITI È PARTE DELLA QUALITÀ</p>

# Fonti aperte. Metodo trasparente.

OpenVehicle è un catalogo indipendente di dati automobilistici. La prima versione usa il dataset **FuelEconomy.gov del Dipartimento dell’Energia USA e dell’EPA**. Non è affiliato a questi enti.

## Copertura effettiva

Sono inclusi i record delle categorie auto, sportive a due posti, station wagon e SUV. Sono esclusi pickup, furgoni, minivan e categorie speciali ambigue. I record descrivono configurazioni per anno modello del **mercato statunitense**, non tutte le auto del mondo. Un anno modello può essere successivo all’anno solare. Più record possono riferirsi allo stesso modello con cambi o motori diversi.

Il conteggio è calcolato sui record importati, non su modelli unici. Le versioni europee non sono assimilate automaticamente a quelle USA. L’archivio europeo è una fase successiva, non una copertura già disponibile.

## Provenienza e riutilizzo

- [Dataset e documentazione ufficiale DOE / EPA](https://www.fueleconomy.gov/feg/ws/index.shtml).
- [Archivio CSV originale](https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip).
- [Catalogo pubblico della California: Vehicle Fuel Economy, dichiarato Public Domain](https://publish.data.ca.gov/dataset/vehicle-fuel-economy).
- [Manifest locale con data d’importazione e SHA-256 del download]({{ '/assets/data/manifest.json' | relative_url }}).

Il codice applicativo è distribuito con licenza MIT. I dati di terzi conservano il loro regime originario; non vengono rilicenziati come software MIT. L’immagine principale è un concept generato con AI, non una fotografia identificativa di un modello.

## Cosa significa “Importato dalla fonte”

Significa che il record è stato acquisito dal dataset indicato e sottoposto a controlli strutturali. **Non significa verifica manuale di ogni valore.** Il link nella scheda consente di controllare il record originale. Non assegniamo percentuali arbitrarie di affidabilità.

I campi non presenti nella fonte rimangono “Non disponibile”, in particolare potenza, codice motore del costruttore e omologazione UE. L’identificativo motore interno EPA non viene presentato come codice motore del costruttore.

## Unità e classificazione

Cilindrata in litri. Consumi EPA in MPG statunitensi o MPGe, secondo il combustibile; consumo elettrico in kWh/100 miglia e CO₂ in grammi/miglio. I valori EPA non sono valori WLTP e non vengono convertiti in dichiarazioni di omologazione europea. Le descrizioni tecniche originali di cambio, trazione e combustibile sono preservate in inglese.

Le etichette italiane delle categorie e delle alimentazioni sono normalizzazioni di OpenVehicle. I valori numerici assenti o negativi sono null; alcuni zeri nella fonte possono indicare campi non applicabili. La fonte originale rimane il riferimento.

## Correzioni e aggiornamenti

[Segnala un errore su GitHub](https://github.com/anomaly73bit/openvehicle/issues/new) indicando ID del record, campo contestato e fonte a supporto. Gli aggiornamenti del dataset vengono importati con uno script riproducibile. Ogni import produce un manifest; la versione Git permette di ricostruire le modifiche. Il workflow manuale propone una pull request per revisione.

Le schede sono informative: non sostituiscono COC, carta di circolazione o valutazioni tecniche ufficiali.

</div>
