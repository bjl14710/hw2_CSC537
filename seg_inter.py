from RedBlackTree import *
from functools import cmp_to_key
import math 
import random
from tkinter import *
import copy
import time
import matplotlib.pyplot as plt

YSIZE = 1000
PSIZE = 4

#-----------------------------------------------------------------
# Event class for endpts and intersection pts in our event queue
#-----------------------------------------------------------------
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

#-----------------------------------------------------------------
# checks if line segment p1p2 and p3p4 intersect
#-----------------------------------------------------------------
#find if the point is on the line segment




def find_B(p1,m):
    # y-mx
    if m is None:
        return 
    return (p1[1]-p1[0]*m)
    
def slopeOf(s):
    if (s[1][0]-s[0][0]) == 0:
        return 
    return (s[1][1]-s[0][1])/(s[1][0]-s[0][0])


def intersect(p1, p2, p3, p4):

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
    return x,y
    




intersectPts = []
 

def find_intersections(event):
    global S
    global cnt
    global intersectPts
    Q = RedBlackTree()
    label = 0
    for s in S:
        if s[0][0] > s[1][0]:
            S[label] = (s[1],s[0])
            s = S[label]
        Q.insert(s[0][0], Event(s[0][0], s[0][1], True, False, s[1], label))
        Q.insert(s[1][0], Event(s[1][0], s[1][1], False, False, s[0], label))
        label += 1
  
    T = RedBlackTree()
    
    intersections = []
    cnt = 0
    while not Q.is_empty():
        min_node = Q.minimum()
        event = min_node.data
        Q.delete(min_node)
        if event.is_left:
            node = T.insert_segment(event.label, Event(event.x, event.y, False, False, event.other_end, event.label))
            pred = T.predecessor(node)
            if pred:
                if intersect((node.data.x,node.data.y),node.data.other_end,(pred.data.x,pred.data.y),pred.data.other_end):
                    Q.insert_segment(event.label,Event(event.x, event.y, True, True, event.other_end, event.label,event.label,((event.x,event.y),event.other_end)))
                    intersectPoint = intersect((node.data.x,node.data.y),node.data.other_end,(pred.data.x,pred.data.y),pred.data.other_end)
                    intersections.append((intersectPoint[0],intersectPoint[1]))
            succ = T.successor(node)
            if succ:
                if intersect((node.data.x,node.data.y),node.data.other_end,(succ.data.x,succ.data.y),succ.data.other_end):
                    Q.insert_segment(event.label,Event(event.x, event.y, False, True, event.other_end, event.label,None,None,event.label,((event.x,event.y),event.other_end)))
                    
                    intersectPoint = intersect((node.data.x,node.data.y),node.data.other_end,(succ.data.x,succ.data.y),succ.data.other_end)
                    
                    intersections.append((intersectPoint[0],intersectPoint[1]))
                    print("intersect succ")
        elif not event.is_intersection: 
            node = T.searchx(event.label, ((event.x,event.y),event.other_end), event.x)
            pred = T.predecessor(node)
            succ = T.successor(node)
            if pred and succ:
                if intersect(pred[0],pred[1],succ[0],succ[1]):
                    Q.insert_segment(event.label,Event(event.x, event.y, False, False))                       
            try:
                T.delete(node)
            except:
                print("couldn't delete node")
            
            print("right event")
        else:
            intersections.append((event.x,event.y))
            n1 = T.searchx(event.plabel,event.psegment,event.x)
            n2 = T.searchx(event.slabel,event.ssegment,event.x)
            T.swap(n1,n2,event.x)
            pred = T.predecessor(n1)
            succ = T.successor(n2)
            if pred:
                if intersect((pred.data.x,pred.data.y),pred.data.other_end, (succ.data.x,succ.data.y),succ.data.other_end):
                    Q.insert_segment(event.label,Event(event.x, event.y, True, True, event.other_end, event.label,event.label,((event.x,event.y),event.other_end)))
                    try:
                        T.delete(n1)
                    except:
                        print("couldn't delete node")
            if succ:
                if intersect((pred.data.x,pred.data.y),pred.data.other_end, (succ.data.x,succ.data.y),succ.data.other_end):
                    Q.insert_segment(event.label,Event(event.x, event.y, False, True, event.other_end, event.label,event.label,None,None,((event.x,event.y),event.other_end)))
                try:
                    T.delete(n2)
                except:
                    print("couldn't delete node")
            print("intersection event")
    count = 0
    for i in intersections:
        intersectPts.append(i)
        count = count + 1
        drawPoint(i)
    print(intersectPts)
    print(intersections)
    
    


def drawSegments(S):
    for s in S:
        drawLine(s[0], s[1], 'black')

def drawLine(p1, p2, color):
    p1 = (p1[0], YSIZE - p1[1])
    p2 = (p2[0], YSIZE - p2[1])
    canvas.create_line(p1, p2, fill=color)

def drawPoint(point):
    p = (point[0], YSIZE - point[1])
    canvas.create_oval(p[0] - PSIZE, p[1] - PSIZE, p[0] + PSIZE, p[1] + PSIZE, fill='red', w=2)

def timeSegmentIntersections():
    times = []
    
    for x in range(0,300,10):
        start_time = time.time()
        list2 = find_intersections(randomSegments[0:x])
        elapsed_time = time.time()-start_time
        times.append(elapsed_time)
    return times
# =========================================
root = Tk()
root.title("Segments")
root.geometry(str(YSIZE)+'x'+str(YSIZE)) #("800x800")

canvas = Canvas(root, width=YSIZE, height=YSIZE, bg='#FFF', highlightbackground="#999")
canvas.bind("<Button-1>", find_intersections)
canvas.grid(row=0, column=0)

S = [((210,530),(900,450)), ((90,50),(850,200)),((80,200),(900,400)),((100,500),(920,200)),((82,300),(150,220))]
# S = [((random.randint(100, 900), random.randint(100, 900)),(random.randint(100, 900), random.randint(100, 900))) for _ in range(10)]
randomSegments = [((random.randint(100, 300), random.randint(100, 300)),(random.randint(100, 300), random.randint(100, 300))) for _ in range(300)]

complexityPoints = []
complexityPoints = timeSegmentIntersections()
plt.plot(range(0,300,10),complexityPoints)
#plt.plot(range(2),complexityPoints)
plt.xlabel('size: N')
plt.ylabel('time(S)')
plt.title('Run Time for Bentley-Ottman')
plt.show()

print(S)
drawSegments(S)


# drawPoint((100,100))
root.mainloop()


