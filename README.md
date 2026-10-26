# VehicleData

Commercial Jekyll automobile catalogue by PACIFIC IT Solutions.

Source repository: anomaly73bit/vehicledata (rename from openvehicle).
Domain: https://vehicledata.pacificit.solutions/

## Data model

Four market-isolated snapshots: ASTRA CH, ADEME FR, EPA US, NRCan CA. Not worldwide-complete coverage. Source credits and field definitions are in fonti.md. No cross-market enrichment by commercial name. Manufacturer engine code, kW and EU approval are populated only when explicitly available. Model years, approval years and catalogue snapshot years have distinct labels.

Compressed snapshots: assets/data/market-{CH,FR,US,CA}.zip. Run `python3 scripts/unpack_data.py` before Jekyll. Manifest: assets/data/v2/manifest.json. Each market has a compact index and detail shards of at most 1,500 records. The browser loads only the selected market unless all markets is selected.

Build: GitHub Actions Pages workflow. Source: GitHub Actions in repository Settings/Pages. Custom domain: vehicledata.pacificit.solutions. DNS CNAME vehicledata -> anomaly73bit.github.io (DNS only).

Development: `python3 scripts/unpack_data.py`; `bundle install`; `bundle exec jekyll serve`.

Data rebuild: obtain the official source snapshots documented in fonti.md into a source directory. Run the legacy EPA importer if needed, then `python3 scripts/build_catalogue.py sources`. Validate all output with `python3 scripts/validate_catalogue.py`. No unattended data refresh is enabled; the manual validation workflow validates the committed snapshots.

The application is a commercial catalogue. There are no public download buttons, source-code promotion, authenticated backend, paywall or active billing. Browser-rendered technical data remain retrievable by visitors; this is not DRM or an access-control implementation. Previously granted licenses remain applicable to prior releases. Third-party source licenses remain unchanged.
