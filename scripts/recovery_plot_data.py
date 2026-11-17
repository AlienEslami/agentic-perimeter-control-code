"""Traffic-oriented displays from fixed plans and archived certificates."""
from pathlib import Path
from fractions import Fraction
import sys,json,itertools,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'output/package/PERIMETER_PARTB_CONSOLIDATED_2026-11-12'
OUT=ROOT/'output/review/simulation_figure_trim_2026_11_16'
DATA=OUT/'plot_checks'
OUT.mkdir(exist_ok=True);DATA.mkdir(exist_ok=True)
SUITE=ROOT/'benchmarks/reusable_perimeter_suite_2026-09-26'
sys.path.insert(0,str(SUITE))
import common
from scipy.integrate import solve_ivp
BLUE,TEAL,RED,GRAY='#285e8c','#007c83','#b94c34','#737f89'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,
 'axes.titlesize':10,'xtick.labelsize':8,'ytick.labelsize':8,'axes.spines.top':False,
 'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
def read(p): return json.loads(Path(p).read_text())
def save(fig,name):
 fig.savefig(PROJECT/'figures'/f'{name}.pdf',bbox_inches='tight',pad_inches=.06)
 fig.savefig(OUT/f'{name}.png',dpi=170,bbox_inches='tight',pad_inches=.06)
 plt.close(fig)
validation={}

# Reconstruct the same polynomial predictor used by the saved full-hour check.
sys.path.insert(0,str(ROOT/'benchmarks/reviewer_strengthening_2026-11-11'))
import probe
import mfd_incident_affine_reachability as af
from mfd_incident_mpc_certification import constant_command_mode
from mfd_incident_verifier import Pulse
certpath=ROOT/'benchmarks/reviewer_strengthening_2026-11-11/full_certificates/arrival_w600_lambda0.65.json'
saved=read(certpath);cert=saved['certificate'];assert cert['accepted']
cp0=cert['reachable_checkpoints'][0];center=np.array(cp0['center']);L=np.array(cp0['metric_L']);inv=np.linalg.inv(L)
pulse=Pulse(*[Fraction(v) for v in cert['proof_descriptor']['pulse']])
modes=[constant_command_mode(np.array(u),f'constant_block_{i}') for i,u in enumerate(saved['job']['commands'])]
draw=[];checks=[]
for step in cert['interval_steps']:
 left=Fraction(step['left_h']).limit_denominator(2400000);right=Fraction(step['right_h']).limit_denominator(2400000)
 if right==left:continue
 h=af.interval_fraction(right-left);mode=modes[step['segment']]
 ar,sl=pulse.affine(left,right);branch,_=af.branch_for_box(af.I(center),mode);assert branch=='gate'
 values=af.closed_field([af.I(v) for v in center],mode,ar,branch)
 fb=af.I(np.array([v.lo for v in values]),np.array([v.hi for v in values]));vel=fb.mid()
 sr=np.zeros(7);sr[6]=1
 acc=((probe.vector_imat(af.jacobian(af.I(center),mode,branch),fb)+af.I(sr)*sl)*af.I(.5)).mid()
 rad=100*probe.vector_imat(af.I(abs(inv)),af.I(step['apriori_radius'])).hi
 qhi=2000-100*step['continuous_constraint_margins_lower'][11]
 draw.append({'left':float(left),'right':float(right),'center':center.copy(),'vel':vel,'acc':acc,'rad':rad,'qhi':qhi})
 center=(af.I(center)+af.I(vel)*h+af.I(acc)*h*h).mid()
 for cp in cert['reachable_checkpoints']:
  if abs(cp['time_h']-float(right))<1e-12:
   error=max(abs(center-np.array(cp['center'])))*100;checks.append(float(error));assert error<1e-8
assert len(draw)==240
final=cert['reachable_checkpoints'][-1]
endpoint=100*np.array(final['center']);endrad=100*probe.vector_imat(af.I(abs(inv)),af.I(final['radius'])).hi


recdir=ROOT/'benchmarks/reviewer_strengthening_2026-11-11/consolidated_recovery'
plans={n:read(recdir/f'{n}_ensemble.json') for n in ['proposal','repair','backup']}
envelope=np.loadtxt(ROOT/'benchmarks/partb_traffic_presentation_2026-11-15/recovery_sampled_envelope.csv',delimiter=',',skiprows=1)
for j,key in enumerate(['final_n1','final_n2','final_queue']):
 st=plans['repair']['statistics'][key]
 assert abs(envelope[-1,1+j]-st['min'])<1e-7
 assert abs(envelope[-1,4+j]-st['max'])<1e-7
for row in envelope:
 j=min(int((row[0]+1e-10)*240),239);d=draw[j];s=row[0]-d['left'];p=100*(d['center']+d['vel']*s+d['acc']*s*s)
 assert all(row[1:3]>=p[:2]-d['rad'][:2]-1e-6)
 assert all(row[4:6]<=p[:2]+d['rad'][:2]+1e-6)
 assert row[6]<=d['qhi']+1e-5

traces={n:np.genfromtxt(recdir/f'{n}_trace.csv',delimiter=',',names=True) for n in plans}
colors={'proposal':RED,'repair':TEAL,'backup':GRAY};styles={'proposal':'--','repair':'-','backup':':'}
labels={'proposal':'Proposed','repair':'Repaired plan','backup':'Backup'}
