from RedBlackTree import *
from functools import cmp_to_key
import math 
import random
from tkinter import *
import copy

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
def onLine(p1,p2, point):
    if (point[0] <= max(p1[0],p2[0]) and point[0] <= min(p1[0],p2[0])
    and point[1] <= max(p1[1], p2[1]) and point[1] <= min(p1[1], p2[1])):
        return True
    else:
        return False

def direction(p1,p2,p3):
    # (b.y-a.y)*(c.x-b.x)-(b.x-a.x)*(c.y-b.y)
    val = (p2[1]-p1[1])*(p3[0]-p2[0])-(p2[0]-p1[0])*(p3[1]-p2[1])
    if val == 0:
        #collinear
        return 0
    elif val < 0:
        #counter-clockwise
        return -1
    else:
        #clockwise
        return 1

def intersect(p1, p2, p3, p4):
    # *** need to implement *** 
    # 
    # Is this the code for when we hit an intersection?
    # or for finding it?   
    dir1 = direction(p1, p2, p3)
    dir2 = direction(p1, p2, p4)
    dir3 = direction(p3, p4, p1)
    dir4 = direction(p3, p4, p2)

    if not (dir1 == dir2) and (not(dir3 == dir4)):
        return True
    elif dir1 == 0 and onLine(p1, p2, p3):
        return True
    elif dir2 == 0 and onLine(p1, p2, p4):
        return True
    elif dir3 == 0 and onLine(p3, p4, p1):
        return True
    elif dir4 == 0 and onLine(p3, p4, p2):
        return True

    return False           


#-----------------------------------------------------------------
# find_intersections callback
#-----------------------------------------------------------------
def find_intersections(event):
    global S
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
    
    while not Q.is_empty():
        min_node = Q.minimum()
        event = min_node.data
        Q.delete(min_node)
        if event.is_left:
            print("left event")
	    # *** need to implement ***
            # from Pseudocode in class; predecessor
            # label is event.
            
            
            # node = T.insert_segment(event, segment)
            # pred = T.predecessor(node)
            # if pred:
            #     if intersect(node,pred):
            #         Q.insert(int.pt,Event())
            # # Successor
            # succ = T.successor(node)
            # if succ:
            #     if intersect(node[0],node[1],succ[0],succ[1]):
            #         Q.insert(int.pt,Event(...))

        elif not event.is_intersection:
            
            
            # node = T.search(S[event])
            # pred = T.predecessor(node)
            # succ = T.successor(node)
            # if pred and succ:
            #     if intersect(pred,succ):
            #         Q.insert(inter.pt,Event(...))
            # T.delete(node)
            
            
            print("right event")
	    # *** need to implement ***

        else:
            # T.append(x,y) or is it I.append(x,y)
            # n1 = t.search(seg1) n2 = t.search(seg2)
            T.append(event[0],event[1])
            # n1 = T.search(s1)
            # n2 = T.search(s2)
            
            # T.swap(self,nn1,nn2,x) is x event[0]. Since that is the point
            # where we intersect.
            T.swap(n1,n2,event[0])
            pred = T.predecessor(n1)
            succ = T.successor(n2)
            # if pred:
            #     if intersect(p1, p2, p3, p4):
            #         Q.insert(key)
            # if succ:
            #     if intersect(p1, p2, p3, p4):
            #         Q.insert(key)
            print("intersection event")
	    # *** need to implement ***
          
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


# =========================================
root = Tk()
root.title("Segments")
root.geometry(str(YSIZE)+'x'+str(YSIZE)) #("800x800")

canvas = Canvas(root, width=YSIZE, height=YSIZE, bg='#FFF', highlightbackground="#999")
canvas.bind("<Button-1>", find_intersections)
canvas.grid(row=0, column=0)

#S = [((20,50),(900,400)), ((80,500),(850,200))]
S = [((random.randint(100, 900), random.randint(100, 900)),(random.randint(100, 900), random.randint(100, 900))) for _ in range(10)]

print(S)
drawSegments(S)

root.mainloop()