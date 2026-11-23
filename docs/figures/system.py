"""Draw manuscript Fig. 1: pre-fault network and a common GFM model overview.

Run from the repository root: python docs/figures/system.py
Writes vector PDF/SVG and a PNG preview next to this script. No simulation.
Self-contained drawing code: only the branch list in studies/inputs/study.toml
is read, to check that the drawn topology still matches the study.
"""
from pathlib import Path
import argparse
import tomllib

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, ConnectionPatch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INK = '#151515'


def polyline(ax, points, **kw):
    xy = np.array(points); ax.plot(xy[:,0], xy[:,1], solid_capstyle='butt', **kw)


def ground(ax, x, y):
    for k, w in enumerate([.32,.22,.11]):
        polyline(ax, [(x-w,y-.12*k),(x+w,y-.12*k)], color=INK, lw=1.1)


def text(ax, x, y, label, size=7.5, **kw):
    return ax.text(x, y, label, fontsize=size, ha=kw.pop('ha', 'center'),
                   va=kw.pop('va', 'center'), color=INK, **kw)


def wire(ax, points, arrow=False, **kw):
    if arrow:
        if len(points) > 2:
            polyline(ax, points[:-1], color=INK, lw=.7, **kw)
        ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle='-|>',
                                    mutation_scale=6, color=INK, lw=.7,
                                    shrinkA=0, shrinkB=0, zorder=6, **kw))
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
    xx=np.linspace(0,.5,40)
    ax.plot(x+.12+xx, y-.27+.12*np.sin(2*np.pi*xx/.5), color=INK, lw=.8, zorder=6)


# Fixed eight-bus layout. Lines from above and below Bus 5 are offset so none
# appears to pass through it; Bus 5 is long enough to carry the load and capacitor.
TOPOLOGY={1:(1,4),2:(4,6),3:(5,6),4:(3,5),5:(2,3),6:(2,5),7:(4,5),8:(2,8),9:(2,7),10:(7,8),11:(5,8)}
BARS={1:((5,11.7),(5,14.7)),4:((11,11.7),(11,14.7)),6:((17.5,15),(20.6,15)),
      7:((3.8,5.9),(3.8,9.6)),8:((8,9.5),(12.4,9.5)),2:((8,5.4),(12.4,5.4)),
      5:((16.6,9.5),(22.3,9.5)),3:((16.6,5.4),(21,5.4))}
PATHS={1:[(5,13),(11,13)],2:[(11,13.9),(18,13.9),(18,15)],3:[(19.0,9.5),(19.0,15)],
       4:[(19.6,5.4),(19.6,9.5)],5:[(12,5.4),(12,4.2),(17.2,4.2),(17.2,5.4)],
       6:[(11.6,5.4),(11.6,6.7),(17.8,6.7),(17.8,9.5)],7:[(11,12.2),(18.3,12.2),(18.3,9.5)],
       8:[(10.4,5.4),(10.4,9.5)],9:[(8.8,5.4),(8.8,7),(3.8,7)],
       10:[(3.8,8.3),(8.5,8.3),(8.5,9.5)],11:[(17.2,9.5),(17.2,8.35),(11.6,8.35),(11.6,9.5)]}
# Every horizontal line is labeled above it, except L5 below.
LINE_LABELS={1:(8,13.9),2:(14.7,14.65),3:(19.5,12.4),4:(18.7,7.55),5:(14.6,3.35),
             6:(14.6,7.4),7:(14.6,12.85),8:(11.05,7.65),9:(5.4,6.45),10:(6.2,8.95),11:(14.5,9.0)}


def network(ax, cfg):
    drawn = {j: tuple(b) for j, b in enumerate(cfg['network']['branches'], 1)}
    assert drawn == TOPOLOGY, 'Update the fixed eight-bus layout for changed topology'
    ax.set(xlim=(.1,26.5), ylim=(.7,17.4), aspect='equal'); ax.axis('off')
    for j, path in PATHS.items():
        wire(ax, path)  # All pre-fault lines are connected, including L7.
    for a,b in BARS.values():
        polyline(ax,[a,b],color=INK,lw=2.3,zorder=3)
    for bus,x,y,port in [(1,2.7,13,(5,13)),(7,1.5,7.7,(3.8,7.7)),
                         (2,9.7,2.5,(9.7,5.4)),(3,19.4,2.5,(19.4,5.4))]:
        end=(x+.8,y) if bus in [1,7] else (x,y+.65)
        wire(ax,[end,port]); converter(ax,x,y)
        text(ax,x,y-1.12,f'GFM {bus}',7.5)  # numbered by bus, as in the result plots
    for x in [17.8,18.4,19,19.6,20.2]:
        wire(ax,[(x,15),(x+.32,15.55)])
    text(ax,19,16.45,'Infinite bus',7.5)
    # Each label sits at a bar end or centered above it, away from line labels.
    labels={1:(5,15.6,'center'),4:(11,15.6,'center'),6:(21.0,15,'left'),
            7:(3.8,10.5,'center'),8:(10.2,10.3,'center'),2:(7.75,5.4,'right'),
            3:(21.4,5.4,'left'),5:(22.3,10.3,'right')}
    for b,(x,y,ha) in labels.items():
        text(ax,x,y,f'Bus {b}',7.5,ha=ha,bbox=dict(fc='white',ec='none',pad=.2),zorder=8)
    for j,(x,y) in LINE_LABELS.items():
        ha='left' if j==3 else 'center'
        text(ax,x,y,f'L{j}',6.8,ha=ha,bbox=dict(fc='white',ec='none',pad=.15),zorder=7)
    # Shunt capacitor (unlabeled; named in the caption) inside, load at the bar end.
    wire(ax,[(20.7,9.5),(20.7,8.45)])
    for y in [8.45,8.2]:wire(ax,[(20.28,y),(21.12,y)])
    wire(ax,[(20.7,8.2),(20.7,7.6)]);ground(ax,20.7,7.6)
    wire(ax,[(21.9,9.5),(21.9,7.9)],arrow=True)
    text(ax,22.25,8.45,'Load',7.0,ha='left')
    # A location annotation on L7 at its Bus 4 end, not a grounded circuit branch.
    bolt=[(12.1,10.9),(11.65,11.55),(12.0,11.5),(11.35,12.2),(11.55,11.65),(11.2,11.7)]
    ax.add_patch(Polygon(bolt,closed=True,fc=INK,ec=INK,lw=.4,zorder=9))
    text(ax,12.45,11.35,'Fault',7.0,ha='left')


def box(ax,x,y,w,h,label,size=7):
    ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,fc='white',ec=INK,lw=.7,zorder=4))
    text(ax,x,y,label,size,zorder=5)


def control(ax):
    ax.set(xlim=(0,14.2),ylim=(0,6));ax.axis('off')
    # Functional view of machine()/rhs!: no PWM or DC-source dynamics implied.
    # Signal labels sit in the gaps between blocks, never on a wire.
    y=4.45;h=1.05
    blocks=[(1.85,3.0,'Primary control\n(Droop / VSM)'),(5.35,2.0,'Voltage\ncontrol'),
            (8.35,2.0,'Current\nlimiter'),(11.35,2.0,'Current\ncontrol')]
    for x,w,label in blocks:
        box(ax,x,y,w,h,label,6.9)
    for (x0,w0,_),(x1,w1,_),label in zip(blocks,blocks[1:],
                                         [r'$V^*$',r'$i^*_{dq}$',r'$i^{\rm lim}_{dq}$']):
        a,b=x0+w0/2,x1-w1/2
        wire(ax,[(a,y),(b,y)],arrow=True);text(ax,(a+b)/2,y+.32,label,6.8)
    top=y+h/2
    # References enter from above; the internal angle leaves from above.
    wire(ax,[(1.3,5.35),(1.3,top)],arrow=True)
    text(ax,1.3,5.72,r'$P^*,\ Q^*,\ V_{\rm set}$',6.8)
    # Internal angle selects the local dq frame throughout the inner controls.
    wire(ax,[(2.7,top),(2.7,5.35),(11.35,5.35),(11.35,top)],arrow=True)
    text(ax,7.0,5.68,r'$\delta$',7.2)
    box(ax,11.35,2.35,2.3,1.05,'Averaged\nconverter',6.9)
    box(ax,7.6,2.35,2.2,.95,'LCL filter',6.9)
    wire(ax,[(12.35,y),(13.0,y),(13.0,2.35),(12.5,2.35)],arrow=True)
    text(ax,13.15,3.4,r'$v^*_{dq}$',6.8,ha='left')
    wire(ax,[(10.2,2.35),(8.7,2.35)],arrow=True)
    wire(ax,[(6.5,2.35),(4.7,2.35)],arrow=True)
    text(ax,4.55,2.35,'Terminal bus',6.9,ha='right')
    # Electrical measurements enter the inner-control subsystem, not the limiter.
    wire(ax,[(7.6,2.825),(7.6,3.3),(5.35,3.3),(5.35,y-h/2)],arrow=True)
    wire(ax,[(11.35,3.3),(11.35,y-h/2)],arrow=True)
    wire(ax,[(7.6,3.3),(11.35,3.3)])
    text(ax,9.45,3.6,r'$v_C,\ i_f,\ i_g$',6.8)
    box(ax,3.1,.85,3.0,1.05,'Power\nmeasurement',6.9)
    wire(ax,[(7.6,1.875),(7.6,.85),(4.6,.85)],arrow=True)
    text(ax,6.1,1.15,r'$V_C,\ I_g$',6.8)
    wire(ax,[(1.6,.85),(.2,.85),(.2,3.3),(1.85,3.3),(1.85,y-h/2)],arrow=True)
    text(ax,.38,2.05,r'$P,\ Q$',6.8,ha='left')


def draw():
    cfg=tomllib.loads((ROOT/'studies/inputs/study.toml').read_text())
    plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix',
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
    fig.text(.08,.345,'GFM model',fontsize=7.4,
             bbox=dict(fc='white',ec='none',pad=1))
    return fig


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=HERE)
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    fig=draw()
    for ext in ['pdf','svg','png']:
        path=args.output/f'system.{ext}'
        fig.savefig(path,dpi=350,facecolor='white',bbox_inches='tight',pad_inches=.025)
        if ext == 'svg':
            path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')
        print(path)
    plt.close(fig)


if __name__=='__main__':main()
