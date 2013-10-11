from utils import modinv

class Curva:
    pass

class Ponto:
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
    inf = Ponto()
    if(p1 == inf):
        return p2
    if(p2 == inf):
        return p1

    p3 = Ponto()

    u1 = (p1.x * p2.z**2) % c.p
    u2 = (p2.x * p1.z**2) % c.p
    s1 = (p1.y * p2.z**3) % c.p
    s2 = (p2.y * p1.z**3) % c.p
    if(u1 == u2):
        if(s1 != s2):
            return p3
        else: # point double
            if(p1.y == 0):
                return p3
            s = (4 * p1.x * p1.y**2) % c.p
            m = (3 * p1.x**2 + (c.a * p1.z**4) % c.p) % c.p
            p3.x = (m**2 - 2*s) % c.p
            p3.y = (m * (s - p3.x) - 8 * p1.y**4) % c.p
            p3.z = (2 * p1.y * p1.z) % c.p
            return p3

    h = (u2 - u1) % c.p
    r = (s2 - s1) % c.p
    p3.x = (r**2 % c.p - h**3 % c.p - 2*u1*h**2 % c.p) % c.p
    p3.y = ((r * (u1 * h**2 - p3.x) % c.p) - (s1 * h**3) % c.p) % c.p
    p3.z = (h * p1.z * p2.z) % c.p

    return p3

# Does point multiplication p*r on the curve c
def multiply(p, r, c):
    P = Ponto(p.x, p.y)
    pr = Ponto()
    while(r > 0):
        if(r & 1):
            pr = add(pr, P, c)
        r = (r >> 1)
        P = add(P, P, c)

    return pr

def binary_montgomery(x, y, p, r):
    pr = 0
    for i in xrange(r.bit_length()-1):
        a = pr + ((x&(1<<i)) >> i) * y
        pr = (a>>1) if ((a & 1) == 0) else ((a + p)>>1)
        #print a, pr
    return (pr - p) if (pr >= p) else pr


def convert(p, c):
    if(p.z == 0):
        return Ponto()
    p.x = (p.x * modinv(p.z**2 % c.p, c.p)) % c.p
    p.y = (p.y * modinv(p.z**3 % c.p, c.p)) % c.p
    p.z = 1
    return p
