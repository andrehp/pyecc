from utils import modinv
import utils

class Curve:
    pass

class Point:
    def __init__(self, xx=0, yy=0, zz=0):
        self.x = xx
        self.y = yy
        if((xx != 0 or yy != 0) and zz == 0):
            self.z = 1
        else:
            self.z = zz

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.z == other.z)

    def __ne__(self, other):
        return not self.__eq__(other)

# Point addition, does p1 + p2 on the curve c
def add(p1, p2, c):
    inf = Point()
    if(p1 == inf):
        return p2
    if(p2 == inf):
        return p1

    bm = utils.binary_montgomery
    am = utils.add_mod
    sm = utils.sub_mod
    r, r2, p = c.r, c.r2, c.p

    x1, y1, z1 = p1.x, p1.y, p1.z
    x2, y2, z2 = p2.x, p2.y, p2.z

    # transformar constantes!

    p3 = Point()

    z12 = bm(z1, z1, p, r)
    z22 = bm(z2, z2, p, r)
    u1 = bm(x1, z22, p, r)
    u2 = bm(x2, z12, p, r)
    s1 = bm(y1, bm(z22, z2, p, r), p, r)
    s2 = bm(y2, bm(z12, z1, p, r), p, r)
    if(u1 == u2):
        if(s1 != s2):
            return p3
        else: # point double
            if(p1.y == 0):
                return p3

            s = bm(x1, bm(y1, y1, p, r), p, r)
            s = bm(bm(4, r2, p, r), s, p, r)
            m = bm(bm(3, r2, p, r), bm(x1, x1, p, r), p, r)
            m = am(m, bm(c.a, bm(z12, z12, p, r), p, r), p)
            p3.x = sm(bm(m, m, p, r), am(s, s, p), p)
            y12 = bm(y1, y1, p, r)
            y14 = bm(y12, y12, p, r)
            p3.y = bm(m, sm(s, p3.x, p), p, r)
            p3.y = sm(p3.y, bm(bm(8, r2, p, r), y14, p, r), p)
            p3.z = am(bm(y1, z1, p, r), bm(y1, z1, p, r), p)
            return p3

    h = sm(u2, u1, p)
    s = sm(s2, s1, p)
    p3.x = sm(bm(s, s, p, r), bm(h, bm(h, h, p, r), p, r), p)
    tmp = bm(bm(2, r2, p, r), bm(u1, bm(h, h, p, r), p, r), p, r)
    p3.x = sm(p3.x, tmp, p)

    tmp = sm(bm(u1, bm(h, h, p, r), p, r), p3.x, p)
    tmp = bm(s, tmp, p, r)
    p3.y = sm(tmp, bm(s1, bm(h, bm(h, h, p, r), p, r), p, r), p)

    p3.z = bm(h, bm(z1, z2, p, r), p, r)
    return p3

# Does point multiplication p*r on the curve c
def multiply(p, r, c):
    P = Point(p.x, p.y, p.z)
    pr = Point()
    while(r > 0):
        if(r & 1):
            pr = add(pr, P, c)
        r = (r >> 1)
        P = add(P, P, c)

    return pr
