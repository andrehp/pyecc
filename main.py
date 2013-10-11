import point
import utils

def main():
    c = point.Curve()
    c.a, c.b, c.p = 14, 18, 23
    c.r = 256
    c.r_minus1 = utils.modinv(c.r - c.p, c.p) # r > p
    c.r2 = (c.r**2) % c.p

    print "Addition:"
    p1 = point.Point(2, 10)
    p2 = point.Point(5, 12)
    p3 = point.add(p1, p2, c)
    p3 = point.convert(p3, c)
    print "Expected: (19, 17)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    p3 = point.add(p1, p1, c)
    p3 = point.convert(p3, c)
    print "Expected: (20, 8)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    c.a, c.b, c.p = 4, 20, 29
    p1 = point.Point(1, 5)
    p3 = point.add(p1, p1, c)
    p3 = point.convert(p3, c)
    print "Expected: (4, 19)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    p2 = point.Point()
    p3 = point.add(p2, p1, c)
    p3 = point.convert(p3, c)
    print "Expected: (1, 5)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    print "Multiplication:"

    p3 = point.multiply(p1, 7, c)
    p3 = point.convert(p3, c)
    print "Expected: (24, 22)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    
    print "Binary Montgomery:"
    x, y, p, r = 202, 236, 239, 256
    print "Expected: %d" % ((x*y)%p)
    r_minus1 = utils.modinv(r % p, p)
    print "r^-1", r_minus1
    r2 = (r**2) % p
    bm = point.binary_montgomery
    x, y = bm(x, r2, p, r), bm(y, r2, p, r)
    z = bm(x, y, p, r)
    z = bm(z, 1, p, r)
    print "Z = %d" % (z)

main()
