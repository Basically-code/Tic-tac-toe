# imports
import turtle
import math
# for slash function on line 80
#from itertools import combinations  

# globals
xSize = 600
ySize = 600
#Note some of these variables can't be accessed by the functions, so a global function is used
is_on = True # this variable changes from X to O
v = []        #All points
vO = []       #This list  contains all Os of the already marked boxes
vX = []       #This list contains all Xs of the already marked boxes
wn   = turtle.Screen()
turt = turtle.Turtle()

#NOTE: In order to access some of the tuples on calling, there is a use of "_" to identify as unused variables in the tuple


# Refer first to onBoard()
# draw X 
def drawX(qX, qY):
    q1,q2,w1,w2,_ = onBoard(qX, qY) #Refer to line 14
    pos = [(q1,q2),(w1,w2)]
    for p in pos:
        turt.penup()
        turt.goto(p[0])
        turt.pendown()
        turt.goto(p[1])

# draw O
def drawO(qX, qY):
    q1,q2,_,_,_ = onBoard(qX, qY) #Refer to line 14
    cx = (q1[0] + q2[0]) / 2
    cy = (q1[1] + q2[1]) / 2
    r  = (xSize / 3) / 2 
    turt.penup()
    #NOTE cx and cy are center points, so (cy-r) moves it to the bottom of the box for the circle to draw 
    turt.goto(cx,cy-r)
    turt.pendown()
    turt.circle(r)

# This function returns the parallel co-ordinates of each box, and which box it was
def onBoard(qX, qY):
    #Since the turtle starts at the middle half the size is the maximum of both sides 
    dx = xSize / 2
    # This lists all the possible X-axis (Columns) tuples 
    box_X = [
        (- dx,   -(dx/3), 2),
        (-(dx/3), (dx/3), 1),
        ( (dx/3),  dx,    0)
        ]
    dy = ySize / 2
    # This lists all the possible Y-axis (Rows) tuples
    box_Y = [
        (- dy,   -(dy/3), 2),
        (-(dy/3), (dy/3), 1),
        ( (dy/3),  dy,    0)
        ]
    #Since the intersection of two rows and two columns forms a box boundary
    for x1,x2,p1 in box_X:
        for y1,y2,p2 in box_Y:
            #If the X-coordinate and Y-coordinate are within the boundary
            # NOTE the return are sequential diagonal points  eg. (x1,y2), (x2,y1) are opposite(They face each other diagoally)
            # (p1,p2) represents the box itself
            if (x1 <= qX < x2) and (y1 <= qY < y2):
                px = (x1 + x2 ) / 2
                py = (y2 + y1 ) / 2
                return (x1,y2), (x2,y1), (x2,y2), (x1, y1), (px,py)

def slashConditions(a1, a2, a3):
    # Find the slopes of the two points if the same, they are collinear
    m1 = (a2[1] - a1[1]) * (a3[0] - a2[0])
    m2 = (a3[1] - a2[1]) * (a2[0] - a1[0])
    if (m1 == m2):
        return True
    return False

#Note this Function is when a more optimized slash (from stackoverflow) import on line 3 first on use
# def slash(p, v):
#     v.append(p)
#     if len(v) >= 3:
#         # This picks unique triplets only (no duplicates, no reversed versions)
#         #Combination is from a library itertools 
#         for p1, p2, p3 in combinations(v, 3):
#             if slashConditions(p1, p2, p3):
#                 turt.penup()
#                 turt.goto(p1)
#                 turt.pendown()
#                 turt.goto(p2)
#                 turt.goto(p3)

#This I made but has problems on repitition
def slash(p,v):
    v.append(p)
    if len(v) >= 3:
        # This picks unique triplets only (no duplicates, no reversed versions)
        #Combination of 3 points 
        for p1 in v:
            for p2 in v:
                for p3 in v:
                    if slashConditions(p1, p2, p3) and (p1!=p2 and p2!=p3 and p1!=p3):
                        turt.penup()
                        turt.goto(p1)
                        turt.pendown()
                        turt.color("red")
                        turt.goto(p2)
                        turt.goto(p3)
    turt.color("black")
                        
# return which quadrant was clicked in
#
# +-----+-----+-----+
# |     |     |     |
# | 2,0 | 2,1 | 2,2 |
# |     |     |     |
# +-----+-----+-----+
# |     |     |     |
# | 1,0 | 1,1 | 1,2 |
# |     |     |     |
# +-----+-----+-----+
# |     |     |     |
# | 0,0 | 0,1 | 0,2 |
# |     |     |     |
# +-----+-----+-----+
#

#This function examines if the player has played that box already
def validPlay(x,y):
    _,_,_,_,p = onBoard(x, y)
    #Refer to line 14
    global v
    if p not in v:
        v.append(p)
        print(p)
        return True,p
    return False,p


# when we click on the turtle window we call this function
# when the click occurs, the X and Y co-ord of where we clicked is passed in as the x and y paramaters
s1,s2 = 1 , 0
def boardClick(x, y):
    print("Clicked on Co-Ords")
    print("X: " + str(x))
    print("Y: " + str(y))
    global is_on #Refer to line 8
    valid, point = validPlay(x,y)
    print(point)
    if valid:
        if  is_on:
            drawO(x, y)
            s1,s2 = 0,1
            slash(point,vO)
        else:
            drawX(x, y)
            s1,s2 = 1,0
            slash(point,vX)
        is_on = not(is_on)
    else:
        pass
        

def drawSquare(xSz, ySz):
    turt.forward(xSz)
    turt.right(90)
    turt.forward(ySz)
    turt.right(90)
    turt.forward(xSz)
    turt.right(90)
    turt.forward(ySz)
    turt.right(90)
    


# draw starting board
def drawBoard():
    xBlockSize = xSize/3
    yBlockSize = ySize/3

    # 3 rows and 3 columns
    for i in range(3):
        for j in range(3):
            turt.penup()
            turt.goto(i*xBlockSize - (xSize/2), j*yBlockSize - (ySize/2)+(yBlockSize))     # draw centered
            turt.pendown()
            drawSquare(xBlockSize, yBlockSize)



# that main method boy!
def main():
    turt.speed(100)
    
    drawBoard()
    wn.onclick(boardClick)  # create callback

    turtle.mainloop()       # enter into mainloop and wait for click events



# if we are the one being called, call main :D
if __name__ == "__main__":
    main()


