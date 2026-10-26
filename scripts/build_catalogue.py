"""Build market-isolated catalogue snapshots from official source files.
Input directory: EPA expanded JSON, ASTRA CSV, ADEME JSON API and NRCan CSV.
No cross-market specification inference is performed.
"""
import csv,json,re,hashlib,datetime,sys,zipfile,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SRC=Path(sys.argv[1] if len(sys.argv)>1 else 'sources');OUT=ROOT/'assets/data/v2';OUT.mkdir(parents=True,exist_ok=True)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();markets={};sources=[]
def number(v):
 try:
  n=float(str(v).replace(',','.'));return int(n) if n.is_integer() else n
 except (ValueError,TypeError):return None
def clean(v):
 if v is None:return None
 v=str(v).strip();return v if v not in ('','-','NA','n/a') else None
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:20]
def brand(v):
 s=v.strip().upper();return {'MERCEDES-BENZ':'Mercedes-Benz','VW':'Volkswagen','VOLKSWAGEN':'Volkswagen','BMW':'BMW','MINI':'MINI','MG':'MG','DS':'DS','ALFA ROMEO':'Alfa Romeo','CITROEN':'Citroën','CITROËN':'Citroën','SKODA':'Škoda','ŠKODA':'Škoda'}.get(s,s.title())
def record(**kw):
 return dict(id=None,make=None,model=None,year=None,year_kind=None,market=None,category=None,fuel=None,displacement_l=None,transmission=None,engine_code=None,power_kw=None,approval_code=None,source=None,source_url=None,**{})|kw
def save(market,rows,source):
 unique={r['id']:r for r in rows};rows=list(unique.values());rows.sort(key=lambda r:(-(r['year'] or 0),r['make'],r['model'],r['id']))
 p=OUT/market;p.mkdir(exist_ok=True)
 for old in p.glob('*.json'):old.unlink()
 index=[]
 for start in range(0,len(rows),1500):
  name=str(start//1500);group=rows[start:start+1500]
  (p/(name+'.json')).write_text(json.dumps(group,ensure_ascii=False,separators=(',',':')))
  for r in group:index.append([r[k] for k in ['id','make','model','year','year_kind','category','fuel','displacement_l','transmission','engine_code','power_kw','approval_code']]+[name])
 (p/'index.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':')))
 meta={'count':len(rows),'makes':len({r['make'] for r in rows}),'years':sorted({r['year'] for r in rows if r['year']},reverse=True),'fields':{k:sum(r.get(k) is not None for r in rows) for k in ['engine_code','power_kw','approval_code']},'source':source,'brands':sorted({r['make'] for r in rows})}
 markets[market]=meta
 with zipfile.ZipFile(ROOT/f'assets/data/market-{market}.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for f in sorted(p.glob('*.json')):z.write(f,'v2/'+market+'/'+f.name)
 print(market,json.dumps(meta|{'brands':len(meta['brands'])}),flush=True)

# Preserve EPA records, without filling specifications from different markets.
epa=[]
for f in (ROOT/'assets/data').glob('[12][0-9][0-9][0-9].json'):
 for r in json.loads(f.read_text()):
  r['make']=brand(r['make']);r['year_kind']='Anno modello';r['source']='DOE / EPA';r['source_key']=r['source_id'];epa.append(r)
save('US',epa,'DOE / EPA — FuelEconomy.gov')

# France: current catalogue snapshot, not model year.
d=json.loads((SRC/'ademe-lines.json').read_text());assert len(d['results'])==d['total']
md=json.loads((SRC/'ademe').read_text());fr=[]
frfuel={'ESSENCE':'Benzina','GAZOLE':'Diesel','ELECTRICITE':'Elettrica','ELECTRICITÉ':'Elettrica','HYBRIDE ESSENCE':'Ibrida benzina','HYBRIDE GAZOLE':'Ibrida diesel','HYBRIDE RECHARGEABLE ESSENCE':'Ibrida plug-in benzina','HYBRIDE RECHARGEABLE GAZOLE':'Ibrida plug-in diesel','GPL':'GPL','GAZ NATUREL':'Metano'}
for r in d['results']:
 if r['Carrosserie']=='MINIBUS':continue
 ident=r['_id'];energy=r['Energie'];c=r['Carrosserie']
 fr.append(record(id='fr-'+ident,market='FR',make=brand(r['Marque']),model=r['Description_Commerciale'],model_family=r['Libellé_modèle'],year=int(md['dataUpdatedAt'][:4]),year_kind='Anno catalogo',category={'TS TERRAINS/CHEMINS':'SUV','BREAK':'Station wagon','BERLINE':'Berlina / compatta','COUPE':'Coupé','CABRIOLET':'Cabriolet'}.get(c,'Monovolume'),fuel=frfuel.get(energy,energy),displacement_l=(r['Cylindrée']/1000 if r.get('Cylindrée') else None),transmission=r.get('Type_de_boite'),gears=r.get('Nombre_rapports'),power_kw=r.get('Puissance_maximale') or None,electric_power_kw=r.get('Puissance_nominale_électrique') or None,mass_kg=r.get('Poids_à_vide'),consumption_min=r.get('Conso_vitesse_mixte_Min'),consumption_max=r.get('Conso_vitesse_mixte_Max'),co2_min=r.get('CO2_vitesse_mixte_Min'),co2_max=r.get('CO2_vitesse_mixte_Max'),test_cycle='WLTP (intervallo di configurazioni)',source='ADEME',source_url='https://data.ademe.fr/datasets/ademe-car-labelling',source_key=ident,source_updated=md['dataUpdatedAt'],source_row=r['_i']))
save('FR',fr,'ADEME — Car Labelling')

# Canada: original Canadian-cycle values, never interpreted as US MPG.
ca=[]
for f in sorted(SRC.glob('canada*.csv')):
 raw=f.read_bytes()
 try:s=raw.decode('utf-8-sig')
 except UnicodeDecodeError:s=raw.decode('cp1252')
 for r in csv.DictReader(s.splitlines()):
  c=r.get('Vehicle class','');cat=c.lower()
  if not cat or any(x in cat for x in ['pickup','van','special purpose']):continue
  year=number(r.get('Model year'))
  if not year:continue
  fuel={'X':'Benzina','Z':'Benzina premium','D':'Diesel','E':'Etanolo E85','N':'Metano'}.get(r['Fuel type'],r['Fuel type'])
  ca.append(record(id='ca-'+digest(r),market='CA',make=brand(r['Make']),model=r['Model'],year=year,year_kind='Anno modello',category='SUV' if 'utility' in cat else 'Station wagon' if 'wagon' in cat else 'Sportiva' if 'two-seater' in cat else 'Berlina / compatta',fuel=fuel,displacement_l=number(r.get('Engine size (L)')),cylinders=number(r.get('Cylinders')),transmission=r.get('Transmission'),consumption_l100km=number(r.get('Combined (L/100 km)')),co2_g_km=number(r.get('CO2 emissions (g/km)')),test_cycle='NRCan 5-cycle; 1995–2014 valori ricalcolati',source='NRCan',source_url='https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64',source_key=f.name+':'+digest(r),source_file=f.name))
save('CA',ca,'Natural Resources Canada')

# Switzerland: complete type-approval CSV, passenger car type 10, M1/M1G only.
ch=[];source=SRC/'astra-complete.csv';assert source.stat().st_size>100_000_000,'Incomplete ASTRA snapshot'
with source.open(encoding='utf-8-sig',newline='') as f:
 for r in csv.DictReader(f,delimiter=';'):
  if r['chVehicleType']!='10' or r['vehicleCategoryCode'] not in ('M1','M1G'):continue
  date=r['dateOfApproval'];year=int(date[:4]) if re.match(r'^\d{4}-',date) else None
  code=clean(r['chEngineCodeAsMarkedOnTheEngine']);eu=clean(r['typeApprovalNumber']);fuel={'B':'Benzina','D':'Diesel','E':'Elettrica','C':'Metano'}.get(r['chFuelType'],'Codice ASTRA '+r['chFuelType'])
  gears=[r[f'gearboxEmissions{i}.chGearboxType'] for i in range(1,5) if r[f'gearboxEmissions{i}.chGearboxType']]
  ch.append(record(id='ch-'+r['chTypeApprovalNumber']+'-'+r['versionNo'],market='CH',make=brand(r['makeName']),model=r['commercialName'],year=year,year_kind='Anno omologazione',category='SUV / fuoristrada' if r['chIsOffRoadVehicle'].upper()=='TRUE' else 'Autovettura M1',vehicle_category=r['vehicleCategoryCode'],fuel=fuel,fuel_source_code=r['chFuelType'],displacement_l=(number(r['engineCapacity'])/1000 if number(r['engineCapacity']) else None),cylinders=number(r['numberOfCylinders']),transmission=' / '.join(dict.fromkeys(gears)) or None,drive={'V':'Anteriore','H':'Posteriore','A':'Integrale'}.get(r['driveType'],clean(r['driveType'])),engine_code=code,engine_type=clean(r['engineType']),engine_manufacturer=clean(r['manufacturerOfTheEngine']),power_kw=number(r['maximumNetPower']),power_rpm=number(r['engineSpeedMaximumNetPower']),electric_continuous_kw=number(r['maximumContinuousRatedPower']),torque_nm=number(r['maximumTorque']),approval_code=eu,approval_extension_from=clean(r['typeApprovalNumberExtFrom']),approval_extension_to=clean(r['typeApprovalNumberExtTo']),ch_approval=r['chTypeApprovalNumber'],type=clean(r['type']),variant=clean(r['variant']),version=clean(r['version']),length_mm=number(r['lengthMinimum']),length_max_mm=number(r['lengthMaximum']),width_mm=number(r['widthMinimum']),height_mm=number(r['heightMinimum']),mass_kg=number(r['chMassOfTheVehicleInRunningOrderMinimum']),maximum_mass_kg=number(r['technicallyPermissibleMaximumLadenMassMinimum']),seats=number(r['chNrOfSeatingPositionsMinimum']),tyres=clean(r['chTyreRims']),approval_date=date,approval_expiry=clean(r['dateOfApprovalExpiry']),approval_cancellation=clean(r['cancelationDate']),source='ASTRA TAS',source_key=r['chTypeApprovalNumber']+' / versione '+r['versionNo'],source_updated=r['dateOfLastChange'],source_url='https://opendata.astra.admin.ch/ivzod/4000-Typengenehmigungen_TAS/4300-Datensaetze/'))
save('CH',ch,'ASTRA — Type Approval System')
manifest={'version':2,'imported_at':now,'markets':markets,'total':sum(m['count'] for m in markets.values()),'index_fields':['id','make','model','year','year_kind','category','fuel','displacement_l','transmission','engine_code','power_kw','approval_code','shard'],'source_checksums':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [SRC/'astra-complete.csv',SRC/'ademe-lines.json',*SRC.glob('canada*.csv')]}}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('TOTAL',manifest['total'])
