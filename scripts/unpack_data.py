from pathlib import Path
import zipfile
p=Path(__file__).resolve().parents[1]/"assets/data"
with zipfile.ZipFile(p/"catalogue.zip") as z:
 for name in z.namelist():
  if Path(name).name!=name or not name.endswith(".json"):raise ValueError("Invalid catalogue member")
 z.extractall(p)
