import TkinterPoints

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
        print(self.items)


test = segment((1,1),(2,2))
print(test.slope())

Q = Queue()

print(Q.isEmpty())

#yay it works.
Q.enqueue(test)
Q.enqueue(111)
Q.enqueue(123)
Q.dequeue()
print(Q.size())
Q.printItems()




