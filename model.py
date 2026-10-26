"""Hourly price-taking battery dispatch with binary charge/discharge exclusion."""
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint

def dispatch(prices,power=1,capacity=4,rte=.9,cycles=1,wear=0):
 p=np.asarray(prices,float);n=len(p)
 if n==0 or not np.isfinite(p).all() or power<=0 or capacity<=0 or not 0<rte<=1 or cycles<0 or wear<0:raise ValueError('Invalid parameters')
 eta=np.sqrt(rte)
 # Variables: grid charge MWh, grid discharge MWh, end-hour stored MWh, binary charging mode.
 objective=np.r_[p,-p+wear,np.zeros(2*n)]
 low=np.zeros(4*n);high=np.r_[np.full(2*n,power),np.full(n,capacity),np.ones(n)]
 A=[];lo=[];hi=[]
 def add(row,l,u):A.append(row);lo.append(l);hi.append(u)
 for t in range(n):
  r=np.zeros(4*n);r[t]=-eta;r[n+t]=1/eta;r[2*n+t]=1
  if t:r[2*n+t-1]=-1
  add(r,0,0)
  r=np.zeros(4*n);r[t]=1;r[3*n+t]=-power;add(r,-np.inf,0)
  r=np.zeros(4*n);r[n+t]=1;r[3*n+t]=power;add(r,-np.inf,power)
 r=np.zeros(4*n);r[3*n-1]=1;add(r,0,0)
 r=np.zeros(4*n);r[n:2*n]=1/eta;add(r,-np.inf,cycles*capacity)
 result=milp(objective,integrality=np.r_[np.zeros(3*n),np.ones(n)],bounds=Bounds(low,high),constraints=LinearConstraint(np.array(A),lo,hi),options={'mip_rel_gap':1e-8})
 if not result.success:raise RuntimeError(result.message)
 c,d,s=result.x[:n],result.x[n:2*n],result.x[2*n:3*n]
 assert np.max(np.abs(s-np.r_[0,s[:-1]]-eta*c+d/eta))<1e-6
 assert max(c*d)<1e-6 and abs(s[-1])<1e-6
 gross=float(p@(d-c));degradation=float(wear*d.sum())
 return dict(charge=c.tolist(),discharge=d.tolist(),soc=s.tolist(),gross=gross,wear_cost=degradation,net=gross-degradation,discharged_mwh=float(d.sum()),equivalent_cycles=float(d.sum()/eta/capacity))
