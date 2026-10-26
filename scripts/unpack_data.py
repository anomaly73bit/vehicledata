from pathlib import Path
import zipfile
p=Path(__file__).resolve().parents[1]/'assets/data'
for archive in sorted(p.glob('market-*.zip')):
 with zipfile.ZipFile(archive) as z:
  for name in z.namelist():
   q=Path(name)
   if q.is_absolute() or '..' in q.parts or q.suffix!='.json' or q.parts[0]!='v2':raise ValueError('Invalid catalogue member')
  z.extractall(p)
