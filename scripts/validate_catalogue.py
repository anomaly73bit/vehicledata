"""Validate published market snapshots, references, IDs and coverage totals."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'assets/data/v2'
m=json.loads((p/'manifest.json').read_text()); all_ids=set(); total=0
for market, meta in m['markets'].items():
    index=json.loads((p/market/'index.json').read_text())
    assert len(index)==meta['count'], market
    shards={}
    for f in (p/market).glob('*.json'):
        if f.stem=='index': continue
        records=json.loads(f.read_text()); assert len(records)<=1500
        shards[f.stem]={r['id']:r for r in records}
        assert len(shards[f.stem])==len(records)
    counts=dict.fromkeys(meta['fields'],0)
    for values in index:
        assert len(values)==len(m['index_fields'])
        r=dict(zip(m['index_fields'],values)); full=shards[r['shard']][r['id']]
        assert full['market']==market and r['id'] not in all_ids
        all_ids.add(r['id'])
        assert full['source_url'].startswith('https://')
        for k in m['index_fields'][:-1]: assert r[k]==full[k], (r['id'],k)
        for k in counts: counts[k]+=full.get(k) is not None
        if market=='CH': assert full['vehicle_category'] in ('M1','M1G')
    assert counts==meta['fields'], (market,counts)
    assert sum(map(len,shards.values()))==len(index)
    total+=len(index)
    print(market,len(index),'OK',counts)
assert total==m['total']
print('PASS:',total,'unique market records')
