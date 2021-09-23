from RedBlackTree import *
# from dcel1 import *
import math 
import random
from tkinter import *
from DCEL import *


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
def intersect(p1, p2, p3, p4):
    # *** need to implement *** 
    # 
    # Is this the code for when we hit an intersection?
    # or for finding it?   
    A1 = p2[1]-p1[1]
    B1 = p1[0]-p2[0]
    A2 = p4[1]-p3[1]
    B2 = p3[0]-p4[0]
    C1 = A1*p1[0] + B1*p1[1]
    C2 = A2*p2[0] + B2*p2[1]

    
    det = A1*B2 - A2*B1
    if det == 0:
        return None
    # C = Ax1+By1
    


# (B2 * C1 - B1 * C2) / det
#   double y = (A1 * C2 - A2 * C1) / det
    x = (B2 * C1 - B1 * C2) / det
    y = (A1 * C2 - A2 * C1) / det

    return x,y



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
  
    T = RedBlackTree()
    
    intersections = []

    MapOverlayIntersection = []

    cnt = 0
    while not Q.is_empty():
        min_node = Q.minimum()
        event = min_node.data
        # holdNode = min_node
        Q.delete(min_node)
        # if hasattr(event, is_left):
        #     print("testing")
        if event.is_left:
            print("left event")
        # *** need to implement ***
            # from Pseudocode in class; predecessor
            # label is event.
            node = T.insert_segment(event.label, Event(event.x, event.y, False, False, event.other_end, event.label))
            #Event(s[0][0], s[0][1], True, False, s[1], label)

            # maybe the .data is how we get the information from the nodes. .data or at least for event, there is an x and a y
            
            # OK so event has a .x and a .y AND IT has an Other_end: which is a tuple. So that might be a segment????

            # Q.insert has an attribute of data=None. So, if there is no event that is put in the insert function, then we only get the 
            # segment. This is why sometimes we don't get the event.is_left to occur.
            pred = T.predecessor(node)
            # pred = Q.predecessor(holdNode)
            if pred:
                # this is taking a different approach. Need to check out if this is correct.
                # This is different than the pseudo code so need to take a look at it later.
                # need the predecessor for the S[cnt+1] segment. pred is a node, so how do I get the semgents?
                if intersect((node.data.x,node.data.y),node.data.other_end,(pred.data.x,pred.data.y),pred.data.other_end):
                    # Q.insert_segment(event.label,(node.data[0],node.data[1]))
                    #  x, y, is_left=True, is_intersection=False, other_end=None, label=None, pl=None, ps=None, sl = None, ss=None
                    Q.insert_segment(event.label,Event(event.x, event.y, True, True, event.other_end, event.label,event.label,((event.x,event.y),event.other_end)))
                    
                    # Q.insert_segment(event.label,Event(event.x, event.y, False, True, event.other_end, event.label))
                    intersectPoint = intersect((node.data.x,node.data.y),node.data.other_end,(pred.data.x,pred.data.y),pred.data.other_end)
                    
                    intersections.append((intersectPoint[0],intersectPoint[1]))
                    

                    # intersections.append(line_intersection(node.data[0],node.data[1]),(pred.data[0],pred.data[1]))
                    # point = intersect(node.data[0],node.data[1],succ.data[0],succ.data[1])
                        
                    # intersections.append(point)
                    
                    # Q.insert_segment(line_intersection(node.data[0],node.data[1]),(node.data[0],node.data[1]))
                    print("intersect pred")
                    
            # Successor :: should we the Q and T's be switched, I switched it as I saw our T tree was empty
            # Q and T's be switched, I switched it as I saw our T tree was empty
            #  but the pseudo code has it but the pseudo code has it
            #  switched.
            # What should the node be??? I am using the smallest from the Q.
            succ = T.successor(node)
            if succ:
                # if intersect(p1, p2, p3, p4)
                # need the succ and the pred for above, so then we can. Then we need to send an event through the insert segment
                # if intersect(node[0],node[1],succ[0],succ[1]):
                # if intersect(node.data[0],node.data[1],succ.data[0],succ.data[1]):
                if intersect((node.data.x,node.data.y),node.data.other_end,(succ.data.x,succ.data.y),succ.data.other_end):
                    # Q.insert_segment(event.label,(node.data[0],node.data[1]))
                    # Q.insert_segment(event.label,Event(event.x, event.y, False, True, event.other_end, event.label))
                    Q.insert_segment(event.label,Event(event.x, event.y, False, True, event.other_end, event.label,None,None,event.label,((event.x,event.y),event.other_end)))
                    
                    intersectPoint = intersect((node.data.x,node.data.y),node.data.other_end,(succ.data.x,succ.data.y),succ.data.other_end)
                    
                    intersections.append((intersectPoint[0],intersectPoint[1]))
                    # point = intersect(node.data[0],node.data[1],succ.data[0],succ.data[1])
                    # intersections.append(point)
                    # intersections.append(line_intersection(node.data[0],node.data[1]),(succ.data[0],succ.data[1]))
                    # intersections = line_intersection(node.data[0],node.data[1]),(succ.data[0],succ.data[1])
                #         Q.insert(int.pt,Event(...))
                #         insert_segment(label, segment) So the label is somewhat like a key.
                #  THE KEY IS THE VALUE IN THE NODE! I THINK
                    print("intersect succ")
                        # Q.insert_segment(line_intersection((node.data.x,node.data.y),holdNode.data.other_end,(pred.data.x,pred.data.y),pred.data.other_end),event)

        elif not event.is_intersection:
            
            
            node = T.searchx(event.label, ((event.x,event.y),event.other_end), event.x)
            # node = T.search(s[event])
            pred = T.predecessor(node)
            succ = T.successor(node)
            if pred and succ:
                if intersect((pred.data.x,pred.data.y),pred.data.other_end,(succ.data.x,succ.data.y),succ.data.other_end):
                    # Q.insert_segment(event.label,(node.data[0],node.data[1]))
                    Q.insert_segment(event.x,Event(event.x, event.y, False, False,event.other_end))                       
            try:
                T.delete(node)
            except:
                print("idk")
            
            print("right event")
        # *** need to implement ***

        else:
            # T.append(x,y) or is it I.append(x,y)
            # n1 = t.search(seg1) n2 = t.search(seg2)
            intersections.append((event.x,event.y))
            print("ddd")
            n1 = T.searchx(event.plabel,event.psegment,event.x)
            n2 = T.searchx(event.slabel,event.ssegment,event.x)
            

            print("test")
            
            # T.swap(self,nn1,nn2,x) is x event[0]. Since that is the point
            # where we intersect.
            T.swap(n1,n2,event.x)
            pred = T.predecessor(n1)
            succ = T.successor(n2)
            if pred:
                if intersect((pred.data.x,pred.data.y),pred.data.other_end, (succ.data.x,succ.data.y),succ.data.other_end):
                    Q.insert_segment(event.label,Event(event.x, event.y, True, True, event.other_end, event.label,event.label,((event.x,event.y),event.other_end)))
                    # intersections.append(intersect(pred[0], pred[1], succ[0], succ[1]))
                    try:
                        T.delete(n1)
                    except:
                        print("well")
            if succ:
                if intersect((pred.data.x,pred.data.y),pred.data.other_end, (succ.data.x,succ.data.y),succ.data.other_end):
                    Q.insert_segment(event.label,Event(event.x, event.y, False, True, event.other_end, event.label,event.label,None,None,((event.x,event.y),event.other_end)))
                    # intersections.append(intersect(pred[0], pred[1], succ[0], succ[1]))
                    # event.label,Event(event.x, event.y, True, True, event.other_end, event.label,event.label,((event.x,event.y),event.other_end))
                try:
                    T.delete(n2)
                except:
                    print("hmmm")
            print("intersection event")
    # cnt = cnt + 1
    # *** need to implement ***  
    for i in range(len(intersections)):
        drawPoint(intersections[i])
        if i+1 < len(intersections):
            MapOverlayIntersection.append((intersections[i],intersections[i+1]))
    MapOverlayIntersection.append((intersections[len(intersections)-1],intersections[0]))
    drawSegments(MapOverlayIntersection)
    print(MapOverlayIntersection)
    print(intersections)
    

#####
    
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





root.mainloop()

