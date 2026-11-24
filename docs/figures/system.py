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
    ax.set(xlim=NET_XLIM, ylim=NET_YLIM, aspect='equal'); ax.axis('off')
    for j, path in PATHS.items():
        wire(ax, path)  # All pre-fault lines are connected, including L7.
    for a,b in BARS.values():
        polyline(ax,[a,b],color=INK,lw=2.3,zorder=3)
    for bus,x,y,port in [(1,2.7,13,(5,13)),(7,1.5,7.7,(3.8,7.7)),
                         (2,9.7,2.5,(9.7,5.4)),(3,19.4,2.5,(19.4,5.4))]:
        end=(x+.8,y) if bus in [1,7] else (x,y+.65)
        wire(ax,[end,port]); converter(ax,x,y)
        # Numbered by bus, as in the result plots; the lower two are labeled
        # beside the icon so the network needs no extra row below them.
        if bus in [1,7]:text(ax,x,y-1.12,f'GFM {bus}',7.5)
        elif bus==2:text(ax,x-1.05,y,f'GFM {bus}',7.5,ha='right')
        else:text(ax,x+1.05,y,f'GFM {bus}',7.5,ha='left')
    for x in [17.8,18.4,19,19.6,20.2]:
        wire(ax,[(x,15),(x+.32,15.55)])
    # Each label sits at a bar end or centered above it, away from line labels.
    labels={1:(5,15.6,'center'),4:(11,15.6,'center'),6:(21.0,15,'left'),
            7:(3.8,10.5,'center'),8:(10.2,10.3,'center'),2:(7.75,5.4,'right'),
            3:(21.4,5.4,'left'),5:(22.3,10.3,'right')}
    for b,(x,y,ha) in labels.items():
        label='Bus 6\n(Infinite bus)' if b==6 else f'Bus {b}'
        text(ax,x,y,label,7.5,ha=ha,linespacing=1.0,bbox=dict(fc='white',ec='none',pad=.2),zorder=8)
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
    ax.set(xlim=CTR_XLIM,ylim=CTR_YLIM,aspect='equal');ax.axis('off')
    # Functional view of machine()/rhs!: no PWM or DC-source dynamics implied.
    # The averaged converter applies v*_dq directly to the LCL filter, so it
    # has no block of its own. Signal labels never sit on a wire.
    y=3.2;h=1.0;top=y+h/2;bottom=y-h/2
    xp,xv,xl,xc=1.85,5.3,8.25,11.2   # primary, voltage, limiter, current control
    blocks=[(xp,3.0,'Primary control\n(Droop / VSM)'),(xv,2.0,'Voltage\ncontrol'),
            (xl,2.0,'Current\nlimiter'),(xc,2.0,'Current\ncontrol')]
    for x,w,label in blocks:
        box(ax,x,y,w,h,label,6.9)
    for (x0,w0,_),(x1,w1,_),label in zip(blocks,blocks[1:],
                                         [r'$V^*$',r'$i^*_{dq}$',r'$i^{\rm lim}_{dq}$']):
        a,b=x0+w0/2,x1-w1/2
        wire(ax,[(a,y),(b,y)],arrow=True);text(ax,(a+b)/2,y+.32,label,6.8)
    # References enter from above; the internal angle leaves from above.
    yt=4.2
    wire(ax,[(1.3,yt),(1.3,top)],arrow=True)
    text(ax,1.3,yt+.35,r'$P^*,\ Q^*,\ V_{\rm set}$',6.8)
    # Internal angle selects the local dq frame throughout the inner controls.
    wire(ax,[(2.7,top),(2.7,yt),(xc,yt),(xc,top)],arrow=True)
    text(ax,(2.7+xc)/2,yt+.3,r'$\delta$',7.2)
    # Lower row: power calculation <- measurements <- LCL filter <-> network.
    # The LCL filter sits exactly below the current controller (same edges).
    yl=1.0;hl=.95;lw=2.0;right=xc+lw/2
    box(ax,xc,yl,lw,hl,'LCL filter',6.9)
    box(ax,xp,yl,2.6,hl,'Power\ncalculation',6.9)
    wire(ax,[(xc+.6,bottom),(xc+.6,yl+hl/2)],arrow=True)
    text(ax,xc+.75,(bottom+yl+hl/2)/2,r'$v^*_{dq}$',6.8,ha='left')
    # Network interface: the grid-side filter current is injected, and the
    # network solution returns the terminal-bus voltage (voltage() in network.jl).
    wire(ax,[(right,yl+.24),(right+.9,yl+.24)],arrow=True)
    wire(ax,[(right+.9,yl-.24),(right,yl-.24)],arrow=True)
    text(ax,right+.45,yl+.55,r'$I_{\rm g}$',6.8)
    text(ax,right+.45,yl-.57,r'$V_{\rm T}$',6.8)
    text(ax,right+1.02,yl,'Network',6.9,ha='left')
    # Measurements as used in machine(): current control takes I_f (error) and
    # V_C (feedforward); voltage control takes V_C (error) and I_g (feedforward).
    # Measured quantities are uppercase as in the manuscript; dq commands lowercase.
    wire(ax,[(xc-.6,yl+hl/2),(xc-.6,bottom)],arrow=True)
    text(ax,xc-.75,(bottom+yl+hl/2)/2,r'$I_{\rm f},\ V_{\rm C}$',6.8,ha='right')
    wire(ax,[(xc-lw/2,yl),(xp+1.3,yl)],arrow=True)
    wire(ax,[(xv,yl),(xv,bottom)],arrow=True)
    # One label: voltage control and power calculation receive the same signals.
    text(ax,(xv+xc-lw/2)/2,yl+.3,r'$V_{\rm C},\ I_{\rm g}$',6.8)
    wire(ax,[(xp,yl+hl/2),(xp,bottom)],arrow=True)
    text(ax,xp+.15,(bottom+yl+hl/2)/2,r'$P,\ Q$',6.8,ha='left')


NET_XLIM,NET_YLIM=(.1,26.5),(1.7,16.1)
CTR_XLIM,CTR_YLIM=(0,14.85),(.18,4.85)


def draw():
    cfg=tomllib.loads((ROOT/'studies/inputs/study.toml').read_text())
    plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix',
                         'pdf.fonttype':42,'svg.fonttype':'none'})
    W=3.5
    span=lambda lim:lim[1]-lim[0]
    # Panel heights follow from equal aspect at the panel widths (inches).
    net_w=.99*W;net_h=net_w*span(NET_YLIM)/span(NET_XLIM)
    ctr_w=.925*W;ctr_h=ctr_w*span(CTR_YLIM)/span(CTR_XLIM)
    frame_y0=.01;ctr_y0=.03;frame_top=ctr_y0+ctr_h+.06;net_y0=frame_top+.14
    H=net_y0+net_h+.01
    fig=plt.figure(figsize=(W,H),facecolor='white')
    net=fig.add_axes([.005,net_y0/H,.99,net_h/H]);network(net,cfg)
    ctr=fig.add_axes([.035,ctr_y0/H,.925,ctr_h/H]);control(ctr)
    # The lower Bus 2 GFM expands into the model view, rather than a new device.
    y0,y1=frame_y0/H,frame_top/H
    fig.add_artist(Rectangle((.025,y0),.95,y1-y0,transform=fig.transFigure,
                             fc='none',ec='#666666',lw=.65,linestyle=(0,(3,2))))
    for start,end in [((8.9,1.85),(.025,y1)),((10.5,1.85),(.975,y1))]:
        fig.add_artist(ConnectionPatch(start,end,coordsA=net.transData,coordsB=fig.transFigure,
                                      color='#777777',lw=.6,linestyle=(0,(3,2))))
    fig.text(.08,y1,'GFM model',fontsize=7.4,va='center',
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
