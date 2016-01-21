import matplotlib.pyplot as S00perMPL
from matplotlib.patches import Polygon

def blank_board(size=(10,10)):
    '''
    makes a super dank blank board and returns an axes object
    wanna add tile or something? pass the sweet object returned from this function to addTile along with coords!
    fuckin matplotlib objects mate. yeah!!!
    '''
    S00perMPL.figure(figsize=size)


    pts = [[0,12], [2,16], [0,17]]
    tl = Polygon(pts, closed=True,color='white')

    pts = [[12,16], [14,12], [14,17]]
    tr = Polygon(pts,closed=True,color='white')

    pts = [[0,12], [6,0], [0,-1]]
    bl = Polygon(pts,closed=True,color='white')

    pts = [[8,0], [14,12], [14,-1]]
    br = Polygon(pts,closed=True,color='white')


    ax = S00perMPL.gca()
    ax.add_patch(tl)
    ax.add_patch(tr)
    ax.add_patch(bl)
    ax.add_patch(br)

    for i in range(0,9):
        ax.plot([0,14],[2*i,2*i],'k-',lw=2,zorder=0)

    for i in range(0,6):
        ax.plot([2*(i),8+i],[16,2*i],'k-',lw=2,zorder=0)
        ax.plot([14-2*i,6-i],[16,2*i],'k-',lw=2,zorder=0)



    ax.plot([0,6],[12,0],'k-',lw=2)
    ax.plot([14,8],[12,0],'k-',lw=2)

    ax.plot([0,2],[12,16],'k-',lw=2)
    ax.plot([12,14],[16,12],'k-',lw=2)


    ax.set_ylim([-1,17])
    ax.axis('off')
    pts=[[2,16],[1,14],[5,14],[4,16]]
    return ax

def addTile(ax,row=0,col=0,color=(222./255,184./255,135./255)):
    '''
    Default color is 'burlywood' an excellent name for a color
    Doesn't check if passed a valid position so don't fuck up
    but if you do just call blankboard again :D
    '''
    y=16-row*2
    if row<2:
        x=(2-row)+col
        if col%2==0:
            #Pointing Up
            pts=[[x,y],[x-1,y-2],[x+1,y-2]]
        else:
            pts=[[x-1,y],[x+1,y],[x,y-2]]
    else:

        x=(-1+row)+col
        if col%2==0:
            #Pointing Down
            pts=[[x-1,y],[x+1,y],[x,y-2]]
        else:
            pts=[[x,y],[x-1,y-2],[x+1,y-2]]
    ax.add_patch(Polygon(pts,closed=True,color=color))

def addMany(ax,pts=[[0,0],[0,10],[7,1]]):
    for pt in pts:
        addTile(ax,pt[0],pt[1])

def plot_some(l,num=1,shape=None):
    plotted = 0
    for e in l:
        if plotted<num:
            if shape==None:
                e.print_board()
                plotted += 1
            else:
                if shape in e.piece_names():
                    e.print_board()
                    plotted += 1


