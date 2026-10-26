import csv,json,hashlib,itertools
from pathlib import Path
from datetime import datetime,timedelta
from model import dispatch
root=Path(__file__).parent;raw=root/'data/20261025damlbmp_zone.csv'
zones='CAPITL CENTRL DUNWOD GENESE HUD_VL LONGIL MHK_VL MILLWD N.Y.C. NORTH WEST'.replace('_',' ').split('|')
zones=['CAPITL','CENTRL','DUNWOD','GENESE','HUD VL','LONGIL','MHK VL','MILLWD','N.Y.C.','NORTH','WEST']
groups={z:[] for z in zones}
for line,r in enumerate(csv.DictReader(raw.open()),2):
 if r['Name'] in groups:groups[r['Name']].append((datetime.strptime(r['Time Stamp'],'%m/%d/%Y %H:%M'),float(r['LBMP ($/MWHr)']),line))
out={}
for z,rows in groups.items():
 rows.sort();assert len(rows)==24 and len(set(t for t,p,l in rows))==24
 assert all(rows[i][0]-rows[i-1][0]==timedelta(hours=1) for i in range(1,24))
 out[z]={'prices':[p for t,p,l in rows],'source_rows':[l for t,p,l in rows],'scenarios':{}}
 for duration,rte,cycles,wear in itertools.product([2,4,8],[.8,.9,1.],[1,2],[0,10]):
  key=f'{duration}|{rte:g}|{cycles}|{wear}';out[z]['scenarios'][key]=dispatch(out[z]['prices'],capacity=duration,rte=rte,cycles=cycles,wear=wear)
(root/'results.json').write_text(json.dumps(out))
manifest={'url':'https://mis.nyiso.com/public/csv/damlbmp/20261025damlbmp_zone.csv','retrieved':'2026-10-26','sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'market':'NYISO zonal day-ahead LBMP','date':'2026-10-25','interval_hours':1,'zones':zones,'excluded':'external proxy locations','scenarios':396,'solver':'scipy.optimize.milp / HiGHS','constraints':'1 MW grid charge/discharge; empty initial/final storage; binary mode; internal-energy cycle budget'}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Built',sum(len(x['scenarios']) for x in out.values()),'scenarios')
