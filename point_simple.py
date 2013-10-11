from utils import modinv

class Curve:
    pass

class Point:
    def __init__(self, xx=0, yy=0, zz=0):
        self.x = xx
        self.y = yy
        self.z = zz

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.z == other.z)

    def __ne__(self, other):
        return not self.__eq__(other)


def add_simple(p1, p2, c):
    p1.z = 0
    p2.z = 0
    inf = Point()
    if(p1 == inf):
        return p2
    if(p2 == inf):
        return p1
    l = 1
    if(p1 == p2):
        if(p1.y == 0):
            return inf
        l = (((3 * (p1.x**2) % c.p) % c.p) + c.a) % c.p
        l = (l * modinv(2*p1.y, c.p)) % c.p
    else:
        if(p1.x == p2.x):
            return inf
        l = (p2.y - p1.y) % c.p
        l = (l * modinv((p2.x - p1.x) % c.p, c.p)) % c.p

    p3 = Point()
    p3.x = (((l*l) % c.p) - ((p1.x + p2.x) % c.p)) % c.p
    p3.y = ((l * ((p1.x - p3.x) % c.p)) % c.p - p1.y) % c.p
    return p3

def multiply_simple(p, r, c):
    P = Point(p.x, p.y)
    pr = Point()
    while(r > 0):
        if(r & 1):
            pr = add_simple(pr, P, c)
        r = (r >> 1)
        P = add_simple(P, P, c)

    return pr
