"""Draw manuscript Fig. 1: pre-fault network and a common GFM model overview.

Run from the repository root: python studies/scripts/figure1.py
Writes vector PDF/SVG and a PNG preview under docs/figures/. No simulation.
"""
from pathlib import Path
import argparse
import sys
import tomllib

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, ConnectionPatch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from network_plot import BARS, PATHS, LINE_LABELS, polyline, ground

INK = '#151515'


def text(ax, x, y, label, size=7.5, **kw):
    return ax.text(x, y, label, fontsize=size, ha=kw.pop('ha', 'center'),
                   va=kw.pop('va', 'center'), color=INK, **kw)


def wire(ax, points, arrow=False, **kw):
    if arrow:
        if len(points) > 2:
            polyline(ax, points[:-1], color=INK, lw=.7, **kw)
        ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle='-|>',
                                    mutation_scale=6, color=INK, lw=.7, **kw))
    else:
        polyline(ax, points, color=INK, lw=.8, **kw)


def converter(ax, x, y, w=1.6, h=1.3):
    """DC/AC converter icon. It does not introduce a modeled DC subsystem."""
    ax.add_patch(Rectangle((x-w/2, y-h/2), w, h, fc='white', ec=INK, lw=.85, zorder=5))
    wire(ax, [(x-w/2, y-h/2), (x+w/2, y+h/2)], zorder=6)
    # DC: solid line over a dashed line, in the upper-left triangle.
    wire(ax, [(x-.57,y+.34),(x-.13,y+.34)], zorder=6)
    for a,b in [(-.57,-.40),(-.30,-.13)]:
        wire(ax, [(x+a,y+.19),(x+b,y+.19)], zorder=6)
    import numpy as np
    xx=np.linspace(0,.5,40)
    ax.plot(x+.12+xx, y-.27+.12*np.sin(2*np.pi*xx/.5), color=INK, lw=.8, zorder=6)


def network(ax, cfg):
    assert len(cfg['lines']) == len(PATHS), 'Update the fixed eight-bus layout for changed topology'
    ax.set(xlim=(.1,26.5), ylim=(.7,17.4), aspect='equal'); ax.axis('off')
    for j, path in PATHS.items():
        wire(ax, path)  # All pre-fault lines are connected, including L7.
    for a,b in BARS.values():
        polyline(ax,[a,b],color=INK,lw=2.3,zorder=3)
    for bus,x,y,port in [(1,2.7,13,(5,13)),(7,1.5,7.7,(3.8,7.7)),
                         (2,9.7,2.5,(9.7,5.4)),(3,19.4,2.5,(19.4,5.4))]:
        end=(x+.8,y) if bus in [1,7] else (x,y+.65)
        wire(ax,[end,port]); converter(ax,x,y)
        text(ax,x,y-1.12,'GFM',7.5)
    for x in [17.8,18.4,19,19.6,20.2]:
        wire(ax,[(x,15),(x+.32,15.55)])
    text(ax,19,16.45,'Infinite grid',7.5)
    labels={1:(5,15.6),4:(11,15.6),6:(23,15),7:(3.8,10.55),8:(9.6,10.4),
            2:(6.5,5.4),3:(23.1,5.4),5:(24.1,9.5)}
    for b,(x,y) in labels.items():
        text(ax,x,y,f'Bus {b}',7.5,bbox=dict(fc='white',ec='none',pad=.2),zorder=8)
    for j,(x,y) in LINE_LABELS.items():
        if j==7:y=11.4
        text(ax,x,y,f'L{j}',6.8,bbox=dict(fc='white',ec='none',pad=.15),zorder=7)
    wire(ax,[(20.6,9.5),(20.6,10.9),(22.8,10.9)],arrow=True)
    text(ax,23.2,11.2,'Load',7.2,ha='left')
    wire(ax,[(20.9,9.5),(22.2,9.5),(22.2,8.1)])
    for y in [8.1,7.85]:wire(ax,[(21.83,y),(22.57,y)])
    wire(ax,[(22.2,7.85),(22.2,7.15)]);ground(ax,22.2,7.15)
    text(ax,23,7.8,'Shunt\ncapacitor',7.0,ha='left')
    # A location annotation, not a grounded circuit branch or physical lightning model.
    bolt=[(11.8,10.3),(11.35,10.9),(11.65,10.9),(11.0,11.7),(11.2,11.1),(10.95,11.1)]
    ax.add_patch(Polygon(bolt,closed=True,fc=INK,ec=INK,lw=.4,zorder=9))
    text(ax,13.2,10.45,'Fault',7.0,ha='left')


def box(ax,x,y,w,h,label,size=7):
    ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,fc='white',ec=INK,lw=.7,zorder=4))
    text(ax,x,y,label,size,zorder=5)


def control(ax):
    ax.set(xlim=(0,14),ylim=(0,6));ax.axis('off')
    # Functional view of machine()/rhs!: no PWM or DC-source dynamics implied.
    y=4.45
    for x,label in [(2,'Primary control\nDroop / VSM'),(5.2,'Voltage\ncontrol'),
                    (8.4,'Current\nlimiter'),(11.6,'Current\ncontrol')]:
        box(ax,x,y,2.8 if x==2 else 2.5,1.05,label,6.2 if x==2 else 6.9)
    for a,b,label in [(3.4,3.95,r'$V^*$'),(6.45,7.15,r'$i^*_{dq}$'),(9.65,10.35,r'$i^{\rm lim}_{dq}$')]:
        wire(ax,[(a,y),(b,y)],arrow=True);text(ax,(a+b)/2,y+.65,label,6.8)
    wire(ax,[(.1,y),(.75,y)],arrow=True)
    text(ax,1.6,5.8,r'$P^*,\ Q^*,\ V_{\rm set}$',6.5)
    # Internal angle selects the local dq frame throughout the inner controls.
    wire(ax,[(2,4.975),(2,5.5),(11.6,5.5),(11.6,4.975)],arrow=True)
    text(ax,7.8,5.9,r'$\delta$ (local dq frame)',6.8)
    box(ax,11.6,2.35,2.5,1.1,'Averaged\nconverter',6.9)
    box(ax,7.8,2.35,2.7,.95,'LCL filter',7.2)
    wire(ax,[(12.85,4.45),(13.5,4.45),(13.5,2.35),(12.85,2.35)],arrow=True)
    text(ax,13.1,3.35,r'$v^*_{dq}$',6.8)
    wire(ax,[(10.35,2.35),(9.15,2.35)],arrow=True)
    wire(ax,[(6.45,2.35),(4.5,2.35)],arrow=True)
    text(ax,3.1,2.35,'Terminal bus',7.0)
    # Electrical measurements enter the inner-control subsystem, not the limiter.
    wire(ax,[(7.8,2.825),(7.8,3.3),(5.2,3.3),(5.2,3.925)],arrow=True)
    wire(ax,[(11.6,3.3),(11.6,3.925)],arrow=True)
    wire(ax,[(7.8,3.3),(11.6,3.3)])
    text(ax,7.8,3.65,r'$v_C,\ i_f,\ i_g$',6.6)
    box(ax,3.1,.85,3.5,1.1,'Power\nmeasurement',6.6)
    wire(ax,[(7.8,1.875),(7.8,.85),(4.85,.85)],arrow=True)
    text(ax,6.3,1.25,r'$V_C,\ I_g$',6.7)
    wire(ax,[(1.35,.85),(.35,.85),(.35,3.35),(2,3.35),(2,3.925)],arrow=True)
    text(ax,.8,2.15,r'$P,Q$',6.7)


def draw():
    cfg=tomllib.loads((ROOT/'studies/inputs/common.toml').read_text())
    plt.rcParams.update({'font.family':'DejaVu Serif','mathtext.fontset':'dejavuserif',
                         'pdf.fonttype':42,'svg.fonttype':'none'})
    fig=plt.figure(figsize=(3.5,4.25),facecolor='white')
    net=fig.add_axes([.005,.405,.99,.59]);network(net,cfg)
    ctr=fig.add_axes([.035,.005,.94,.30]);control(ctr)
    # The lower Bus 2 GFM expands into the model view, rather than a new device.
    frame=Rectangle((.025,.008),.95,.35,transform=fig.transFigure,
                    fc='none',ec='#666666',lw=.65,linestyle=(0,(3,2)))
    fig.add_artist(frame)
    for start,end in [((8.9,1.85),(.025,.358)),((10.5,1.85),(.975,.358))]:
        fig.add_artist(ConnectionPatch(start,end,coordsA=net.transData,coordsB=fig.transFigure,
                                      color='#777777',lw=.6,linestyle=(0,(3,2))))
    fig.text(.025,.99,'(a) Pre-fault network',fontsize=7.6)
    fig.text(.045,.345,'(b) GFM model (common to all four units)',fontsize=7.4,
             bbox=dict(fc='white',ec='none',pad=1))
    return fig


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'docs/figures')
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    fig=draw()
    for ext in ['pdf','svg','png']:
        path=args.output/f'system.{ext}'
        fig.savefig(path,dpi=350,facecolor='white',bbox_inches='tight',pad_inches=.025)
        print(path)
    plt.close(fig)


if __name__=='__main__':main()
