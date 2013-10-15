import point
import utils
import point_simple
import random

def test():

    #print "Binary Montgomery:"
    x, y, z, w, p, r = 18, 5, 22, 18, 29, 256
    expected = (((x*y - z)*w)**2%p)
    r2 = (r**2) % p
    bm = utils.binary_montgomery
    x, y, z, w = bm(x, r2, p, r), bm(y, r2, p, r), bm(z, r2, p, r), bm(w, r2, p, r)
    ret = bm(x, y, p, r)
    ret = utils.sub_mod(ret, z, p)
    ret = bm(ret, w, p, r)
    ret = bm(ret, ret, p, r);
    ret = utils.convert_int_to_standard(ret, p, r)
    if(expected != ret):
        print "Binary Montgomery multiplication is broken"
        exit(1)

    c = point.Curve()
    c.a, c.b, c.p = 4, 20, 29
    c.r = 256
    c.r_minus1 = utils.modinv(c.r - c.p, c.p) # r > p
    c.r2 = (c.r**2) % c.p

    c2 = utils.convert_curve_to_montgomery(c, c.p, c.r, c.r2) 

    #print "Addition:"
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
    if(p3s.x != p3.x or p3s.y != p3.y):
        print "addition is broken!"
        exit(1)

    p3 = point.add(p1, p2, c2)
    p3 = utils.convert_point_to_standard(p3, c.p, c.r)
    p3 = utils.projective_to_standard(p3, c)
    p3s = point_simple.add_simple(p1s, p2s, c)
    if(p3s.x != p3.x or p3s.y != p3.y):
        print "addition is broken!"
        exit(1)

    p2 = point.Point()
    p3 = point.add(p2, p1, c2)
    p3 = utils.convert_point_to_standard(p3, c.p, c.r)
    p3 = utils.projective_to_standard(p3, c)
    p2s = point_simple.Point()
    p3s = point_simple.add_simple(p1s, p2s, c)
    if(p3s.x != p3.x or p3s.y != p3.y):
        print "addition is broken!"
        exit(1)

    #print "Multiplication:"

    for i in xrange(37):
        p3 = point.multiply(p1, i, c2)
        p3 = utils.convert_point_to_standard(p3, c.p, c.r)
        p3 = utils.projective_to_standard(p3, c)
        p3s = point_simple.multiply_simple(p1s, i, c)
        if(p3s.x != p3.x or p3s.y != p3.y):
            print "Point multiplication is broken!"
            exit(1)

    test_nist_p256()

    print "All tests successful!"

def test_nist_p256():
    random.seed(42)

    c = point.Curve()
    c.a, c.b = -3, 41058363725152142129326129780047268409114441015993725554835256314039467401291
    c.p = 2**256 - 2**224 + 2**192 + 2**96 - 1 
    c.r = 2**256
    c.r2 = (c.r**2) % c.p

    c2 = utils.convert_curve_to_montgomery(c, c.p, c.r, c.r2) 
    p1s = point_simple.Point(48439561293906451759052585252797914202762949526041747995844080717082404635286, 36134250956749795798585127919587881956611106672985015071877198253568414405109)

    p1 = point.Point(48439561293906451759052585252797914202762949526041747995844080717082404635286, 36134250956749795798585127919587881956611106672985015071877198253568414405109)
    p1 = utils.convert_point_to_montgomery(p1, c.p, c.r, c.r2)

    for i in xrange(10):

        j = random.randint(1, c.p)

        p3 = point.multiply(p1, j, c2)
        p3 = utils.convert_point_to_standard(p3, c.p, c.r)
        p3 = utils.projective_to_standard(p3, c)

        p3s = point_simple.multiply_simple(p1s, j, c)
        if(p3s.x != p3.x or p3s.y != p3.y):
            print i
            print "(%d, %d)" % (p3.x, p3.y)
            print "(%d, %d)" % (p3s.x, p3s.y)
            print "Point multiplication is broken!"
            exit(1)


# Binary Montgomery is being much slower than standard multiplication, even when compared to affine coordinates
def test_nist_p384():

    random.seed(42)

    c = point.Curve()
    c.a, c.b = -3, 27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575
    c.p = 2**384 - 2**128 - 2**96 + 2**32 - 1 
    c.r = 2**384 
    c.r2 = (c.r**2) % c.p

    c2 = utils.convert_curve_to_montgomery(c, c.p, c.r, c.r2) 

    p1s = point_simple.Point(26247035095799689268623156744566981891852923491109213387815615900925518854738050089022388053975719786650872476732087, 8325710961489029985546751289520108179287853048861315594709205902480503199884419224438643760392947333078086511627871) 

    p1 = point.Point(26247035095799689268623156744566981891852923491109213387815615900925518854738050089022388053975719786650872476732087, 8325710961489029985546751289520108179287853048861315594709205902480503199884419224438643760392947333078086511627871) 
    p1 = utils.convert_point_to_montgomery(p1, c.p, c.r, c.r2)

    for i in xrange(10):

        j = random.randint(1, c.p)

        p3 = point.multiply(p1, j, c2)
        p3 = utils.convert_point_to_standard(p3, c.p, c.r)
        p3 = utils.projective_to_standard(p3, c)
        p3s = point_simple.multiply_simple(p1s, j, c)
        if(p3s.x != p3.x or p3s.y != p3.y):
            print i
            print "(%d, %d)" % (p3.x, p3.y)
            print "(%d, %d)" % (p3s.x, p3s.y)
            print "Point multiplication is broken!"
            exit(1)
