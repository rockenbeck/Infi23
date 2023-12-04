# Hi, Infi folks! "Dank u wel" for another fun Kerstman puzzle to fill the time
#  before the Advent of Code starts getting difficult! I proudly wear the
#  "Keiharde Nerd" Infi T-shirt you gave me a few years ago. I promised last year
#  that I'd take a picture with the shirt and hat from last year by the Space Needle,
#  but I've forgotten the few times I've gone into Seattle. Maybe this year!
#  My Dutch is pretty rudimentary, but Google helped out. I started to use
#  Dutch variable names, below, but couldn't keep it up. Since I'm doing this
#  just for fun, I didn't look up any existing algorithms or vector libraries,
#  which would certainly have made this a lot simpler.
#  Hope you keep this up next year! - Bill

import re
import math

test1 = """(0, 4), (3, -2), (-1, -2), (-2, 0)"""
invoer1="""(-26, -51), (88, -80), (-98, -72), (91, -60), (-87, 8), (93, -31)
(15, -53), (91, 8), (-76, -85)
(10, -40), (-66, 45), (-18, 28)
(49, 67), (24, 33), (60, 83), (24, 71), (-9, 96), (-70, 0)
(-21, 6), (-1, 62), (-63, 59), (56, -97), (-53, -18), (85, -42)
(-89, -75), (-87, -85), (-57, 38), (-27, 7)
(-27, -11), (74, -67), (-15, -2), (44, 56)
(-22, 23), (-18, 31), (-97, 61), (-29, 7), (23, 72), (18, 2), (-15, 38)
(-19, 71), (-2, 57), (-24, 53), (-8, -74)
(-63, -67), (-90, 88), (-96, -27)
(-42, -9), (-13, 7), (35, 96), (-20, -79)
(43, 35), (-86, 1), (89, 39), (87, 50)
(51, 14), (99, 86), (-20, -58), (86, -3), (-44, -7)
(50, -18), (3, -50), (14, -41), (-90, 97), (-69, 40), (-15, -9), (-24, 5)
(-83, -23), (24, -63), (-2, -55), (-41, -11), (-47, 59), (-42, -29)
(-55, 20), (-62, 40), (86, -48)
(-40, -68), (64, 87), (29, 28), (89, 19), (58, -35)
(23, -19), (47, -76), (8, 72)
(94, 23), (-10, 92), (-51, -10)
(88, -100), (52, 10), (1, 45), (5, -76)
(-28, 84), (13, 37), (7, 70)
(39, 30), (87, 37), (34, 90), (-37, -80)
(-35, 21), (92, 28), (-90, -33)
(-27, 31), (41, 27), (-63, -91), (-44, 20), (17, -2), (-23, -25), (-60, 95)
(11, -77), (-33, 51), (-39, -38)"""

def deel1(invoer):

    som = 0.0

    for pakje in invoer.split('\n'):
        straal = 0.0
        for hoekpunt in re.findall("\((-*\d+), (-*\d+)\)", pakje):
            (x,y) = map(int, hoekpunt)
            straal = max(straal, math.sqrt(x*x + y*y))
        som += straal

    print(f"som = {int(som)}")

# deel1(invoer1)


# Making my own simple vectors. Better to use numpy, or some Python builtin?
# Numpy probably already has a method to compute the minimal enclosing circle,
# but what's the fun in that?

def midpoint(p0, p1):
    return ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0)

def minus(p0, p1):
    return (p1[0] - p0[0], p1[1] - p0[1])

def dot(vec0, vec1):
    return vec0[0] * vec1[0] + vec0[1] * vec1[1]

def normalize(vec):
    l = math.sqrt(dot(vec, vec))
    if l > 0.0:
        vec = (vec[0] / l, vec[1] / l)
    return vec

def isPointInsideCircle(center, radius, p):
    vec = minus(p, center)
    return dot(vec, vec) <= radius * radius

def circleFrom2Points(p0, p1):
    # return minimal circle which includes p0 and p1
 
    center = midpoint(p0, p1)
    vec = minus(p0, center)
    radius = math.sqrt(dot(vec, vec))

    return (center, radius)

def circleFrom3Points(p0, p1, p2):
    # Any circle passing through two points must have a center which lies on their midline.
    # Therefore to pass through all three, the center must lie where the midlines cross.

    mid01 = midpoint(p0, p1)
    d01 = minus(p1, p0)
    normal01 = (d01[1], -d01[0])

    mid02 = midpoint(p0, p2)
    d02 = minus(p2, p0)
    dot02 = dot(d02, mid02)

    # Solve dot(d02, mid01 + normal01 * t) = dot02
    # Not handling colinear points, which will result in divide-by-zero here

    t = (dot02 - dot(d02, mid01)) / dot(d02, normal01)

    center = (mid01[0] + normal01[0] * t, mid01[1] + normal01[1] * t)
    vec = (p0[0] - center[0], p0[1] - center[1])
    radius = math.sqrt(dot(vec, vec))

    return (center, radius)

def circleSmallestFrom3Points(p0, p1, p2):

    # Check each 2-point combination
    # better to find 3-point circle and check whether center of circle is outside triangle?

    center, radius = circleFrom2Points(p0, p1)
    if isPointInsideCircle(center, radius, p2):
        return (center, radius)

    center, radius = circleFrom2Points(p0, p2)
    if isPointInsideCircle(center, radius, p1):
        return (center, radius)

    center, radius = circleFrom2Points(p1, p2)
    if isPointInsideCircle(center, radius, p0):
        return (center, radius)

    # Do full triangulation to find circle which contains all three points

    return circleFrom3Points(p0, p1, p2)

def circleSmallestFromPoints(points):
    assert(len(points) >= 3)

    # I didn't look up the "standard algorithm" for this, since I'm just doing this for fun.
    #  It SEEMS like it ought to work, but I haven't quite proved it to myself.
    #  (actually the final inputs are so small, it would work fine to just brute-force it!)

    # Start with any three points as a guess for bounding circle

    i0 = 0
    i1 = 1
    i2 = 2

    while True:
        # find the smallest circle containing current points

        center, radius = circleSmallestFrom3Points(points[i0], points[i1], points[i2])
        # print(f"try ({i0, i1, i2}) => {center}, {radius}")

        # Check all other points to see whether they fall outside circle

        allInside = True
        for i in range(0, len(points)):
            if i==i0 or i==i1 or i==i2:
                continue

            if not isPointInsideCircle(center, radius, points[i]):
                # Probably faster to find point MOST outside current circle,
                #  but this is plenty good for small input we're given

                # Replace one of the current points with this point, but which one?
                # Keep the pair which when combined with new point enclose the one we're discarding

                c0, r0 = circleSmallestFrom3Points(points[i], points[i1], points[i2])
                if isPointInsideCircle(c0, r0, points[i0]):
                    i0 = i
                else:
                    c1, r1 = circleSmallestFrom3Points(points[i0], points[i], points[i2])
                    if isPointInsideCircle(c1, r1, points[i1]):
                        i1 = i
                    else:
                        # c2, r2 = circleSmallestFrom3Points(points[i0], points[i1], points[i])
                        i2 = i

                allInside = False
                break
  
        if allInside:
            return (center, radius)

def deel2(invoer):
    som = 0.0

    for pakje in invoer.split('\n'):
        # Parse line into pairs of coordinates

        hoekpunten = []
        for hoekpunt in re.findall("\((-*\d+), (-*\d+)\)", pakje):
            (x,y) = map(int, hoekpunt)
            hoekpunten.append((x,y))

        # add radii of enclosing circles
        
        centrum, straal = circleSmallestFromPoints(hoekpunten)
        som += straal

    print(f"som = {int(som)}")

# print(circleSmallestFromPoints(((1,4), (1,-4), (-1,0))))
# print(circleSmallestFromPoints(((0,0), (1,0), (.5,.8))))

deel2(invoer1)