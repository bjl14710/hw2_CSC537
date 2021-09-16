import random
from tkinter import *

YSIZE = 800
PSIZE = 2

def drawPoints(points):
    for p in points:
        p = (p[0], YSIZE - p[1])
        canvas.create_oval(p[0] - PSIZE, p[1] - PSIZE, p[0] + PSIZE, p[1] + PSIZE, w=2)

def drawLine(p1, p2, color):
    p1 = (p1[0], YSIZE - p1[1])
    p2 = (p2[0], YSIZE - p2[1])
    canvas.create_line(p1, p2, fill=color)

def drawPolygon(points, fill, outline):
    new_points = []
    for p in points:
        new_points.append((p[0], YSIZE - p[1]))
    canvas.create_polygon(new_points, fill=fill, outline=outline)

def DrawHull(event):
    global points
    print(points)
    drawPolygon(points, '', 'black')




# =========================================
root = Tk()
root.title("Points")
root.geometry(str(YSIZE)+'x'+str(YSIZE))

canvas = Canvas(root, width=YSIZE, height=YSIZE, bg='#FFF', highlightbackground="#999")
canvas.bind("<Button-1>", DrawHull)
canvas.grid(row=0, column=0)

points = [(random.randint(200, 600), random.randint(200, 600)) for _ in range(7)]
points = [(200, 200), (225, 350), (400, 200), (226, 500), (450, 500)]

drawPoints(points)

root.mainloop()