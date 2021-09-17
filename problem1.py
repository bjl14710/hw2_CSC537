# import TkinterPoints
import seg_inter
import RedBlackTree
import DCEL


class point:

    def __init__(self,x,y):
        self.x = x
        self.y = y

class segment:

    def __init__(self,point1,point2):
        self.point1 = point(point1[0],point1[1])
        self.point2 = point(point2[0],point2[1])
        
    def slope(self):
        return (self.point1.y-self.point2.y)/(self.point1.x-self.point2.y)

    def createSegment(self):
        return (self.point1,self.point2)

    

#for Queing the segments
class Queue:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return (self.items == [])

    def enqueue(self,item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
    def printItems(self):
        print(str(self.items))


def compare(p1, p2):
    if p1.x < p2.x:
        return -1
    elif p1.x > p2.x:
        return 1
  
    if p1.x == p2.x:
        if p1.ptype == p2.ptype:
            if p1.y < p2.y:
                return -1
            else:
                return 1
        else:
            if p1.ptype == 0:
                return -1
            else:
                return 1








test = segment((1,1),(2,2))

print(test.slope())


#2 segments with one intersection
s1 = segment((1,1),(10,10))
s2 = segment((2,1),(10,5))
Q = Queue()

#print(Q.isEmpt.y())

#yay it works.
#printing doesn't though :/
Q.enqueue(s1)
Q.enqueue(s2)
Q.enqueue(123)
Q.dequeue()
print(Q.size())



# Q.printItems()




