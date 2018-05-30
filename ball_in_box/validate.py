import math

def validate(circles, blockers):
    # Is circle in the box?
    for circle in circles:
        xmr = circle[0] - circle[2]
        xpr = circle[0] + circle[2]
        ymr = circle[1] - circle[2]
        ypr = circle[1] + circle[2]

        if (not (xmr <= 1 and xmr >=-1 )) \
           or (not (xpr <= 1 and xpr >=-1 )) \
           or (not (ymr <= 1 and ymr >=-1 )) \
           or (not (ypr <= 1 and ypr >=-1 )):
            return False

    # Is circle good for blockers?
    if blockers is not None and len(blockers) > 0:
        for circle in circles:
            for block in blockers:
                x = circle[0]
                y = circle[1]
                r = circle[2]
                bx = block[0]
                by = block[1]
                if math.sqrt((x - bx)**2 + (y - by)**2) < r:
                    return False

    # Is circle good for each other?
    for i in range(len(circles)):
        for j in range(i+1, len(circles)):
            circle1 = circles[i]
            circle2 = circles[j]
            x1 = circle1[0]
            y1 = circle1[1]
            r1 = circle1[2]
            x2 = circle2[0]
            y2 = circle2[1]
            r2 = circle2[2]
            if math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < (r1 + r2):
                return False

    # all good
    return True

def intersect(circle : tuple, circles : list, blockers : list):
    """
    Args:
        circle: next a circle to check whether could be in current box
        circles: circles which have been put in box
        blockers: blockers
    Return:
        A list of circle in the circles which overlap with arg circle
    """
    inters = []

    # Does circle intersect with the box?
    xmr = circle[0] - circle[2]
    xpr = circle[0] + circle[2]
    ymr = circle[1] - circle[2]
    ypr = circle[1] + circle[2]

    if xmr < -1:
        inters.append((1, 0, -1))
    if xpr > 1:
        inters.append((-1, 0, -1))
    if ymr < -1:
        inters.append((0, 1, -1))
    if ypr > 1:
        inters.append((0, -1, -1))
        
    # Does circle intersect with blockers?
    if blockers is not None and len(blockers) > 0:
        for block in blockers:
            x = circle[0]
            y = circle[1]
            r = circle[2]
            bx = block[0]
            by = block[1]
            if math.sqrt((x - bx)**2 + (y - by)**2) < r:
                inters.append((bx, by, 0))

    # Does circle intersect with other circles?
    for circle1 in circles:
        x1 = circle1[0]
        y1 = circle1[1]
        r1 = circle1[2]
        x = circle[0]
        y = circle[1]
        r = circle[2]
        if math.sqrt((x1 - x)**2 + (y1 - y)**2) < (r1 + r):
            inters.append(circle1)

    # Intersect with nothing
    return inters
