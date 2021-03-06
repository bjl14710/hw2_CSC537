from RedBlackTree import *
# from dcel1 import *
import math 
import random
from tkinter import *
from DCEL import *
import time
import matplotlib.pyplot as plt


YSIZE = 1000
PSIZE = 4
colors = ['red', 'green', 'blue', 'yellow']
color_idx = 0


####

class Event:
    def __init__(self, x, y, is_left=True, is_intersection=False, other_end=None, label=None, pl=None, ps=None, sl = None, ss=None):
        self.x = x
        self.y = y
        self.is_left = is_left
        self.is_intersection = is_intersection
        self.other_end = other_end
        self.label = label
        # fields for intersection events
        self.plabel=pl
        self.psegment=ps
        self.slabel=sl
        self.ssegment=ss
    def __str__(self):
        return str(self.label) + ' ' + str(self.plabel) + ' ' + str(self.slabel)



####
    
def find_intersections(event):
    global myDCEL
    segs = []
    for i in range(0,len(myDCEL.faces),2):  # only take inner or outer face, not both
        h = myDCEL.faces[i].halfEdge
        while (h.next != myDCEL.faces[i].halfEdge):
            segs.append(((h.tail.x, h.tail.y),(h.next.tail.x, h.next.tail.y)))
            h = h.next
        segs.append(((h.tail.x, h.tail.y),(h.next.tail.x, h.next.tail.y)))
            
    print(segs)
    drawSegments(segs)
    find_inters(segs)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def line_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
    """ returns a (x, y) tuple or None if there is no intersection """
    d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    if d:
        uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
    else:
        return
    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        return
    x = Ax1 + uA * (Ax2 - Ax1)
    y = Ay1 + uA * (Ay2 - Ay1)
 
    return x, y

####
def find_B(p1,m):
    # y-mx
    if m is None:
        return 
    return (p1[1]-p1[0]*m)
    
def slopeOf(s):
    if (s[1][0]-s[0][0]) == 0:
        return 
    return (s[1][1]-s[0][1])/(s[1][0]-s[0][0])

####
def intersect(p1, p2, p3, p4, xlow, xhigh):
    # *** need to implement *** 
    # 
    # Is this the code for when we hit an intersection?
    # or for finding it?   
    m1 = slopeOf((p1,p2))
    m2 = slopeOf((p3,p4))

    B1 = find_B(p1, m1)
    B2 = find_B(p3, m2)

    if m1 == None or m2 == None or B1 == None or B2 == None:
        return 
    if(m1-m2 == 0):
        return 
    x = (B2-B1)/(m1-m2)
    y = m1*((B2-B1)/(m1-m2))+B1
    if x < xhigh and x>xlow:
        return x,y
    return



def find_inters(S):
    print("find_inters")  # code from Q1
    Q = RedBlackTree()
    label = 0
    for s in S:
        if s[0][0] > s[1][0]:
            S[label] = (s[1],s[0])
            s = S[label]
        Q.insert(s[0][0], Event(s[0][0], s[0][1], True, False, s[1], label))
        Q.insert(s[1][0], Event(s[1][0], s[1][1], False, False, s[0], label))
        label += 1
    
    
    
    intersections = []
    
    for s in S:
        for j in S:
            if not intersect(s[0], s[1], j[0], j[1],min(s[0][0], s[1][0], j[0][0], j[1][0]),
                max(s[0][0], s[1][0], j[0][0], j[1][0])) == None:
                intersections.append(intersect(s[0], s[1], j[0], j[1],min(s[0][0], s[1][0], j[0][0], j[1][0]),
                max(s[0][0], s[1][0], j[0][0], j[1][0])))
    T = RedBlackTree()

    faceSegment = []

    for i in range(len(intersections)):
        drawPoint(intersections[i])
        if i < len(intersections)-2:
            faceSegment.append((intersections[i],intersections[i+1]))
    
    faceSegment.append((intersections[len(intersections)-1],intersections[0]))
    drawSegments(faceSegment)

    # myDCEL = DCEL()
    # myDCEL.build_dcel(intersections, faceSegment)
    # drawFaces(myDCEL)

    

    
def drawSegments(S):
    for s in S:
        drawLine(s[0], s[1], 'black')

def drawFaces(dcel):
    global color_idx
    for f in dcel.faces:
        print('polygon')
        verts = []
        h = f.halfEdge
        while (h.next != f.halfEdge):
            print((h.tail.x, h.tail.y), end="->")
            verts.append(h.tail.x)
            verts.append(YSIZE - h.tail.y)
            h = h.next
        verts.append(h.tail.x)
        verts.append(YSIZE - h.tail.y)
        print('\nverts ', verts)
        canvas.create_polygon(verts, outline='black', fill=colors[color_idx], width=2)    
        color_idx = (color_idx + 1) % 4
        print('\n')

def drawLine(p1, p2, color):
    p1 = (p1[0], YSIZE - p1[1])
    p2 = (p2[0], YSIZE - p2[1])
    canvas.create_line(p1, p2, fill=color)

def drawPoint(point):
    p = (point[0], YSIZE - point[1])
    canvas.create_oval(p[0] - PSIZE, p[1] - PSIZE, p[0] + PSIZE, p[1] + PSIZE, fill='red', w=2)


# =========================================
root = Tk()
root.title("DCEL Test")
root.geometry(str(YSIZE)+'x'+str(YSIZE)) #("800x800")

canvas = Canvas(root, width=YSIZE, height=YSIZE, bg='#FFF', highlightbackground="#999")
canvas.bind("<Button-1>", find_intersections)
canvas.grid(row=0, column=0)


P1 = [(100, 500), (400, 800), (600, 200), (100, 100)]
    
S1 = [[ P1[0], P1[1]],
     [ P1[1], P1[2]],
     [ P1[2], P1[3]],
     [ P1[3], P1[0]],
    ]
    
# myDCEL = DCEL()
# myDCEL.build_dcel(P1, S1)
# drawFaces(myDCEL)


P2 = [(500, 900), (700, 800), (350, 100), (200, 500)]
    
S2 = [[ P2[0], P2[1]],
     [ P2[1], P2[2]],
     [ P2[2], P2[3]],
     [ P2[3], P2[0]],
    ]
    
#myDCEL = DCEL()
#myDCEL.build_dcel(P2, S2)
#drawFaces(myDCEL)


P3 = P1.copy()
P3.extend(P2)
S3 = S1.copy()
S3.extend(S2)

find_inters(S3)

# canvas.create_line(x, y, x+1, y, fill="#ff0000")

myDCEL = DCEL()
myDCEL.build_dcel(P3, S3)
#drawFaces(myDCEL)

def timeSegmentIntersections():
    times = []
    
    for x in range(0,300,10):
        start_time = time.time()
        list2 = find_intersections(randomSegments[0:x])
        elapsed_time = time.time()-start_time
        times.append(elapsed_time)
    return times


randomSegments = [((random.randint(100, 300), random.randint(100, 300)),(random.randint(100, 300), random.randint(100, 300))) for _ in range(300)]

complexityPoints = []
complexityPoints = timeSegmentIntersections()
plt.plot(range(0,300,10),complexityPoints)
#plt.plot(range(2),complexityPoints)
plt.xlabel('size: N')
plt.ylabel('time(S)')
plt.title('Run Time for DCEL Intersections')
plt.show()




root.mainloop()

