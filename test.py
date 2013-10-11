import point
import utils
import point_simple

def test():

    print "Binary Montgomery:"
    x, y, z, w, p, r = 18, 5, 22, 18, 29, 256
    print "Expected: %d" % (((x*y - z)*w)**2%p)
    r_minus1 = utils.modinv(r % p, p)
    r2 = (r**2) % p
    bm = utils.binary_montgomery
    x, y, z, w = bm(x, r2, p, r), bm(y, r2, p, r), bm(z, r2, p, r), bm(w, r2, p, r)
    ret = bm(x, y, p, r)
    ret = utils.sub_mod(ret, z, p)
    ret = bm(ret, w, p, r)
    ret = bm(ret, ret, p, r);
    ret = utils.convert_int_to_standard(ret, p, r)
    print "Result: %d" % (ret)

    c = point.Curve()
    c.a, c.b, c.p = 4, 20, 29
    c.r = 256
    c.r_minus1 = utils.modinv(c.r - c.p, c.p) # r > p
    c.r2 = (c.r**2) % c.p

    c2 = utils.convert_curve_to_montgomery(c, c.p, c.r, c.r2) 

    print "Addition:"
    p1s = point_simple.Point(1, 5)
    p2s = point_simple.Point(20, 3)

    p1 = point.Point(1, 5)
    p2 = point.Point(20, 3)
    p1 = utils.convert_point_to_montgomery(p1, c.p, c.r, c.r2)
    p2 = utils.convert_point_to_montgomery(p2, c.p, c.r, c.r2)

    p3s = point_simple.add_simple(p1s, p1s, c)
    p3 = point.add(p1, p1, c2)
    p3 = utils.convert_point_to_standard(p3, c.p, c.r)
    p3 = utils.projective_to_standard(p3, c)
    print "Expected: (%d, %d)" % (p3s.x, p3s.y)
    print "Result: (%d, %d, %d)" % (p3.x, p3.y, p3.z)


    p3 = point.add(p1, p2, c2)
    p3 = utils.convert_point_to_standard(p3, c.p, c.r)
    p3 = utils.projective_to_standard(p3, c)
    p3s = point_simple.add_simple(p1s, p2s, c)
    print "Expected: (%d, %d)" % (p3s.x, p3s.y)
    print "Result: (%d, %d, %d)" % (p3.x, p3.y, p3.z)

    p2 = point.Point()
    p3 = point.add(p2, p1, c2)
    p3 = utils.convert_point_to_standard(p3, c.p, c.r)
    p3 = utils.projective_to_standard(p3, c)
    p2s = point_simple.Point()
    p3s = point_simple.add_simple(p1s, p2s, c)
    print "Expected: (%d, %d)" % (p3s.x, p3s.y)
    print "Result: (%d, %d, %d)" % (p3.x, p3.y, p3.z)

    print "Multiplication:"

    p3 = point.multiply(p1, 7, c2)
    p3 = utils.convert_point_to_standard(p3, c.p, c.r)
    p3 = utils.projective_to_standard(p3, c)
    p3s = point_simple.multiply_simple(p1s, 7, c)
    print "Expected: (%d, %d)" % (p3s.x, p3s.y)
    print "Result: (%d, %d, %d)" % (p3.x, p3.y, p3.z)

    
    print "Binary Montgomery:"
    x, y, p, r = 202, 236, 239, 256
    print "Expected: %d" % ((x*y)%p)
    r2 = (r**2) % p
    bm = utils.binary_montgomery
    x, y = bm(x, r2, p, r), bm(y, r2, p, r)
    z = bm(x, y, p, r)
    z = bm(z, 1, p, r)
    print "Z = %d" % (z)
