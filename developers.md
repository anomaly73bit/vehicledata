---
layout: default
title: Dati aperti per sviluppatori
permalink: /developers/
---
<div class="prose" markdown="1">
<p class="eyebrow blue">BUILD WITH OPENVEHICLE</p>

# Dai dati al tuo prossimo progetto.

Il catalogo pubblico è gratuito. Puoi scaricare i risultati della ricerca in CSV oppure usare i file JSON statici.

| Risorsa | Contenuto |
|---|---|
| [manifest.json]({{ '/assets/data/manifest.json' | relative_url }}) | Copertura, data importazione, fonte e checksum |
| [index.json]({{ '/assets/data/index.json' | relative_url }}) | Tutti i record ricercabili, con ID stabile EPA |
| [2026.json]({{ '/assets/data/2026.json' | relative_url }}) | Schede complete dell’anno modello 2026 |

Gli altri anni seguono la forma `assets/data/ANNO.json`; l’elenco degli anni si trova nel manifest. I file sono risorse statiche, **non un’API con autenticazione, SLA o filtri server**. È consigliato scaricare e memorizzare una copia per elaborazioni ripetute.

```javascript
const response = await fetch('/openvehicle/assets/data/2026.json');
if (!response.ok) throw new Error('Download non riuscito');
const vehicles = await response.json();
const porsche = vehicles.filter(vehicle => vehicle.make === 'Porsche');
```

## Identità e campi mancanti

`id` usa il prefisso `epa-` seguito dall’ID originale. `market` distingue il mercato della fonte. `source_url` collega ogni record alla fonte. `null` significa dato non disponibile: non va sostituito con zero. L’anno è l’anno modello.

Il catalogo non contiene targhe, proprietari o VIN individuali. La fusione futura di fonti europee richiederà identificatori di tipo/variante/versione; il nome commerciale da solo non è sufficiente.

## Codice e licenze

[Repository GitHub](https://github.com/anomaly73bit/openvehicle) · Codice MIT. Dati DOE / EPA con provenienza documentata nella pagina [Fonti e metodo]({{ '/fonti/' | relative_url }}).

Per integrazioni, mapping dei campi e forniture personalizzate: [OpenVehicle per aziende]({{ '/pro/' | relative_url }}).

</div>
