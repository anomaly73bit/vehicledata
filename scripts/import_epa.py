"""Import public EPA/DOE vehicle records. No owner or VIN data is collected."""
import csv,io,json,zipfile,urllib.request,datetime,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
URL='https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip'
raw=Path(sys.argv[1]).read_bytes() if len(sys.argv)>1 else urllib.request.urlopen(URL,timeout=120).read()
z=zipfile.ZipFile(io.BytesIO(raw)); rows=csv.DictReader(io.StringIO(z.read('vehicles.csv').decode('utf-8-sig')))
out=[]
for r in rows:
 c=r['VClass']
 if not ('Cars' in c or 'Wagons' in c or 'Sport Utility' in c or c=='Two Seaters'):continue
 fuel='Elettrica' if r['fuelType1']=='Electricity' else 'Ibrida plug-in' if r['atvType']=='Plug-in Hybrid' else 'Ibrida' if r['atvType']=='Hybrid' else 'Diesel' if r['fuelType1']=='Diesel' else 'Benzina' if r['fuelType1'] in ['Regular Gasoline','Premium Gasoline','Midgrade Gasoline'] else r['fuelType1']
 def num(k):
  try:return float(r[k]) if float(r[k])>=0 else None
  except (ValueError,KeyError):return None
 out.append(dict(id='epa-'+r['id'],make=r['make'],model=r['model'],year=int(r['year']),category='SUV' if 'Sport Utility' in c else 'Station wagon' if 'Wagons' in c else 'Sportiva' if c=='Two Seaters' else 'Berlina / compatta',fuel=fuel,displacement_l=num('displ'),cylinders=num('cylinders'),transmission=r['trany'] or None,drive=r['drive'] or None,epa_class=c,fuel_primary=r['fuelType1'],fuel_secondary=r['fuelType2'] or None,combined_mpg=num('comb08'),electric_kwh_100mi=num('combE'),co2_g_mile=num('co2'),engine_description=r['eng_dscr'] or None,engine_code=None,approval_code=None,power_kw=None,market='US',source_url='https://www.fueleconomy.gov/feg/noframes/'+r['id']+'.shtml',source_id=r['id'],verification='Importato dalla fonte',source_updated=r['modifiedOn']))
out.sort(key=lambda r:(-r['year'],r['make'],r['model'],r['id']))
assert len(out)>20000 and len({r['id'] for r in out})==len(out)
p=ROOT/'assets/data';p.mkdir(parents=True,exist_ok=True)
for year in sorted({r['year'] for r in out}):
 (p/f'{year}.json').write_text(json.dumps([r for r in out if r['year']==year],ensure_ascii=False,separators=(',',':')))
keys=['id','make','model','year','category','fuel','displacement_l','transmission']
(p/'index.json').write_text(json.dumps([{k:r[k] for k in keys} for r in out],ensure_ascii=False,separators=(',',':')))
meta=dict(count=len(out),makes=len({r['make'] for r in out}),min_year=min(r['year'] for r in out),max_year=max(r['year'] for r in out),imported_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_url=URL,sha256=hashlib.sha256(raw).hexdigest(),market='US',source='US DOE / EPA — FuelEconomy.gov',years=sorted({r['year'] for r in out},reverse=True))
(p/'manifest.json').write_text(json.dumps(meta,indent=2))
print(json.dumps(meta,indent=2))

with zipfile.ZipFile(p/"catalogue.zip", "w", zipfile.ZIP_DEFLATED) as archive:
 for f in sorted(p.glob("*.json")):
  archive.write(f,f.name)
