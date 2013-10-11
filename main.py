import ponto

def main():
    c = ponto.Curva()
    c.a, c.b, c.p = 14, 18, 23

    print "Addition:"
    p1 = ponto.Ponto(2, 10)
    p2 = ponto.Ponto(5, 12)
    p3 = ponto.add(p1, p2, c)
    p3 = ponto.convert(p3, c)
    print "Expected: (19, 17)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    p3 = ponto.add(p1, p1, c)
    p3 = ponto.convert(p3, c)
    print "Expected: (20, 8)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    c.a, c.b, c.p = 4, 20, 29
    p1 = ponto.Ponto(1, 5)
    p3 = ponto.add(p1, p1, c)
    p3 = ponto.convert(p3, c)
    print "Expected: (4, 19)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    p2 = ponto.Ponto()
    p3 = ponto.add(p2, p1, c)
    p3 = ponto.convert(p3, c)
    print "Expected: (1, 5)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    print "Multiplication:"

    p3 = ponto.multiply(p1, 7, c)
    p3 = ponto.convert(p3, c)
    print "Expected: (24, 22)"
    print "(%d, %d, %d)" % (p3.x, p3.y, p3.z)

    
    print "Binary Montgomery:"
    x, y, p, r = 202, 236, 239, 256
    print "Expected: %d" % ((x*y)%p)
    r_minus1 = ponto.modinv(r % p, p)
    r2 = (r**2) % p
    bm = ponto.binary_montgomery
    x, y = bm(x, r2, p, r), bm(y, r2, p, r)
    z = bm(x, y, p, r)
    z = bm(z, 1, p, r)
    print "Z = %d" % (z)

main()
