import math
from math import sin
from math import cos
import random
import turtle

from .validate import validate
from .validate import intersect

__all__ = ['ball_in_box']

global t
# whether display detail process
# VIEW = True
VIEW = False
EPSILON = 1e-5

def ball_in_box(m=5, blockers=[(0.5, 0.5), (0.5, -0.5), (0.5, 0.3)]):
    """
    Args:
        m: the number circles.
        n: is the list of coordinates of tiny blocks.
    Return:
        This returns a list of tuple, composed of x,y of the circle and r of the circle.
    """
    ###############################
    # view
    if VIEW:
        turtle.setup(400, 400)
        global t
        t = turtle.Turtle()
        t.penup()
        t.setposition(-150, -150)
        t.pendown()
        t.setposition(-150, 150)
        t.setposition(150, 150)
        t.setposition(150, -150)
        t.setposition(-150, -150)

        for blocker in blockers:
            t.penup()
            t.setposition(blocker[0]*150, blocker[1]*150)
            t.pendown()
            t.circle(1)
    ###############################

    circles = []
    while len(circles) < m:
        next_circle = find_step_max(blockers, circles)
        circles.append(next_circle)
    
    if not VIEW:
        view_circles(circles, blockers)
    return circles

def find_step_max(blockers : list, circles : list):
    """
    Args:
        blockers: blockers
        circles: current circles in box
    Return:
        next circle which can be put in current box
    """

    circle = None
    while circle is None:
        x = random.random()*2 - 1
        y = random.random()*2 - 1
        circle = find_max_circle_at(x, y, blockers, circles)
    
    # 速度衰减速率
    coll_v_rate = 0.98
    # 初始速度
    velocity = vec(0.7, 0.7)

    while True:
        inters = intersect((circle[0], circle[1], circle[2]), circles, blockers)
        while len(inters) is 0:
            circle = find_max_circle_at(circle[0], circle[1], blockers, circles)
            circle = (circle[0], circle[1], circle[2]+EPSILON*100)
            inters = intersect((circle[0], circle[1], circle[2]), circles, blockers)

        # norm - 接触面法向
        if inters[0][2] is -1:
            norm = vec(inters[0][0], inters[0][1])
        else: 
            norm = vec(circle[0]-inters[0][0], circle[1]-inters[0][1])

        dot_a = norm.dot(velocity) / (norm.magnitude()*velocity.magnitude())
        if dot_a < 0:
            if abs(dot_a) < abs(cos(math.pi/9*4)):
                velocity = norm.normal()*velocity.magnitude()
            velocity = velocity*-coll_v_rate
            velocity.mirror(norm)
        
        if velocity.magnitude() < 0.1:
            while len(inters) > 0:
                circle = (circle[0], circle[1], circle[2]*0.99)
                inters = intersect((circle[0], circle[1], circle[2]), circles, blockers)
            return circle

        print("Velocity is %f"%(velocity.magnitude()))
        circle = (circle[0] + velocity.x * 0.05,circle[1] + velocity.y * 0.05, circle[2])

        ###############################################
        # view
        if VIEW:
            if random.random() > 0.4:
                continue
            global t

            t.color("black")
            t.penup()
            t.setposition(circle[0]*150, circle[1]*150-circle[2]*150)
            t.pendown()
            t.circle(circle[2]*150)

            t.color("white")
            t.penup()
            t.setposition(circle[0]*150, circle[1]*150-circle[2]*150)
            t.pendown()
            t.circle(circle[2]*150)
        ###############################################

def find_max_circle_at(x : float, y : float, blockers : list, circles : list):
    """
    Args:
        x,y: specific position to put a circle
    Return:
        max circle to put at this position
    """
    if len(intersect((x, y, 0), circles, blockers)) is not 0:
        return None
    r = 1
    inters = intersect((x, y, r), circles, blockers)
    while len(inters) is not 0:
        for inter in inters:
            if inter[2] is -1:
                tmp_r = min(1-x, x+1, 1-y, y+1) - EPSILON
            else:
                x1 = inter[0]
                y1 = inter[1]
                r1 = inter[2]
                tmp_r = math.sqrt((x1-x)**2 + (y1-y)**2) - r1 - EPSILON
            if r > tmp_r:
                r = tmp_r
        inters = intersect((x, y, r), circles, blockers)
    return (x, y, r)

def view_circles(circles : list, blockers : list):
    turtle.setup(400, 400)
    t = turtle.Turtle()

    t.penup()
    t.setposition(-150, -150)
    t.pendown()
    t.setposition(-150, 150)
    t.setposition(150, 150)
    t.setposition(150, -150)
    t.setposition(-150, -150)

    for blocker in blockers:
        t.penup()
        t.setposition(blocker[0]*150, blocker[1]*150)
        t.pendown()
        t.circle(1)
    
    for circle in circles:
        t.penup()
        t.setposition(circle[0]*150, circle[1]*150-circle[2]*150)
        t.pendown()
        t.circle(circle[2]*150)

class vec:
    '2d Vector'

    def __init__(self, *arg):
        self.x = arg[0]
        self.y = arg[1]
    def __mul__(self, value):
        return vec(self.x*value, self.y*value)
    def __truediv__(self, value):
        return vec(self.x/value, self.y/value)
    def __neg__(self):
        return vec(-self.x, -self.y)
    
    def to_tuple(self):
        return (self.x, self.y)

    def dot(self, value):
        return self.x*value.x + self.y*value.y

    def cross(self, value):
        return vec(self.x*value.x, self.y*value.y)
    
    def mirror(self, vec2):
        m =  vec2 * (self.dot(vec2)/vec2.dot(vec2))
        self.x = 2*m.x - self.x
        self.y = 2*m.y - self.y
    
    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
    def normal(self):
        return self/self.magnitude()
