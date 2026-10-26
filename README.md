# OpenVehicle

Jekyll automobile catalogue by PACIFIC IT Solutions. Italian UI, responsive custom theme, generated transparent automotive hero, client-side search and filters, three-vehicle comparison, CSV export and source-linked specification dialogs.

## Data

38,485 records initially imported from US DOE / EPA FuelEconomy.gov; 124 makes; model years 1984–2027. These are US-market configuration/year records, NOT a complete global catalogue and NOT unique models. Automobiles, wagons and SUVs only. No fabricated EU approval or manufacturer engine codes. See fonti.md for provenance and limits.

- `assets/data/index.json`: compact searchable index.
- `assets/data/YYYY.json`: full records grouped by model year.
- `assets/data/manifest.json`: source URL, import timestamp, count, archive checksum.
- `python3 scripts/import_epa.py`: fetch and normalize source.
- `python3 scripts/import_epa.py /path/to/vehicles.csv.zip`: reproduce from archive.

## GitHub Pages

1. Push the contents of this directory to `anomaly73bit/openvehicle`, default branch `main`.
2. In Settings → Pages choose **GitHub Actions** as Source.
3. Run or observe **Build and deploy Jekyll**.
4. Expected URL, once deployment succeeds: `https://openvehicle.pacificit.solutions/`.

Custom domain is configured as `openvehicle.pacificit.solutions` with an empty baseurl. To change it, change `url`, set `baseurl: ""`, add `CNAME`, and configure the DNS separately. No custom domain has been assumed or provisioned.

Local development requires Ruby/Bundler: `python3 scripts/unpack_data.py`, `bundle install` then `bundle exec jekyll serve`. The source files contain Jekyll Liquid and need a Jekyll build.

## Updates

The data refresh workflow is **manual**, creates a review PR and does not overwrite production directly. Repository Actions settings must permit PR creation. It is intentionally not scheduled until ownership, monitoring and desired frequency are configured.

## Commercial model

Public catalogue and data downloads remain free. Integration, custom data delivery and managed API work are offered by enquiry; payment, advertisements and a hosted API are not implemented. See BUSINESS.md.

## License

Application code MIT. Data retain source terms. See LICENSE and fonti.md. Hero image generated with OpenAI Imagegen; prompt: unbranded silver graphite European coupe, three-quarter front view, cyan accents, isolated transparent background, no text or logos. Asset: assets/images/hero-car.png.

The source repository stores the dataset in `assets/data/catalogue.zip`; the build safely extracts JSON before Jekyll compilation.
