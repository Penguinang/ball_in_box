import math
from math import sin
from math import cos
import random
import turtle

from .validate import validate
from .validate import intersect

__all__ = ['ball_in_box']

global t
VIEW = False

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
    max_tmp = 100
    end_tmp = 0.001
    cold_rate = 0.998
    cur_tmp = max_tmp
    circle = None
    while circle is None:
        x = random.random()*2 - 1
        y = random.random()*2 - 1
        circle = find_max_circle_at(x, y, blockers, circles)

    ###############################################
    # view
    if VIEW:
        global t
        t.penup()
        t.setposition(circle[0]*150, circle[1]*150-circle[2]*150)
        t.pendown()
        t.circle(circle[2]*150)
    ###############################################

    a = 0
    b = 0
    while cur_tmp > end_tmp:
        a += 1
        random_deg = random.random()*math.pi*2
        random_dir = (sin(random_deg), cos(random_deg))
        mov_dis = random.random()*cur_tmp/max_tmp
        next_x = x + mov_dis*random_dir[0]
        next_y = y + mov_dis*random_dir[1]
        next_circle = find_max_circle_at(next_x, next_y, blockers, circles)
        if next_circle is not None:    
            if next_circle[2] > circle[2]:
                ###############################################
                # view
                if VIEW:
                    t.color("white")
                    t.penup()
                    t.setposition(circle[0]*150, circle[1]*150-circle[2]*150)
                    t.pendown()
                    t.circle(circle[2]*150)

                    t.color("black")
                    t.penup()
                    t.setposition(next_circle[0]*150, next_circle[1]*150-next_circle[2]*150)
                    t.pendown()
                    t.circle(next_circle[2]*150)
                ###############################################
                b += 1
                circle = next_circle
            elif math.exp(next_circle[2] - circle[2])/cur_tmp/10 > random.random():
                ###############################################
                # view
                if VIEW:
                    t.color("white")
                    t.penup()
                    t.setposition(circle[0]*150, circle[1]*150-circle[2]*150)
                    t.pendown()
                    t.circle(circle[2]*150)

                    t.color("black")
                    t.penup()
                    t.setposition(next_circle[0]*150, next_circle[1]*150-next_circle[2]*150)
                    t.pendown()
                    t.circle(next_circle[2]*150)
                ###############################################
                b += 1
                circle = next_circle
        
        cur_tmp *= cold_rate
    return circle

    # x = random.random()*2 - 1
    # y = random.random()*2 - 1
    # while intersect((x, y, 0), circles, blockers) is not None:
    #     x = random.random()*2 - 1
    #     y = random.random()*2 - 1
    # return find_max_circle_at(x, y, blockers, circles)

def find_max_circle_at(x : float, y : float, blockers : list, circles : list):
    """
    Args:
        x,y: specific position to put a circle
    Return:
        max circle to put at this position
    """
    if intersect((x, y, 0), circles, blockers) is not None:
        return None
    r = 1
    inters = intersect((x, y, r), circles, blockers)
    while inters is not None:
        if inters[2] is -1:
            r = min(1-x, x+1, 1-y, y+1)
        else:
            x1 = inters[0]
            y1 = inters[1]
            r1 = inters[2]
            r = math.sqrt((x1-x)**2 + (y1-y)**2) - r1 - 1e-7
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