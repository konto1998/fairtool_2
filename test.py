import json
from pathlib import Path

path = Path("/home/ravindra/codes/devel/neelravi/fairtool_kon2/tests/VASP/example01/fair_parsed_vasprun.json")

data = json.loads(path.read_text())

print(data.keys())
print(data.get("results", {}).keys())
print(data.get("results", {}).get("properties", {}).keys())

