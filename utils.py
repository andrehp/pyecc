import copy
import point

def egcd(a, b):
    x, lx = 0, 1
    y, ly = 1, 0
    
    while(b != 0):
        quo = a / b
        a, b = b, a % b
        x, lx = lx - quo*x, x
        y, ly = ly - quo*y, y

    return lx, ly

def modinv(a, p):
    x, y = egcd(a, p)
    if(x < 0):
        x = x + p
    return x

def projective_to_standard(p, c):
    if(p.z == 0):
        return point.Point()
    p.x = (p.x * modinv(p.z**2 % c.p, c.p)) % c.p
    p.y = (p.y * modinv(p.z**3 % c.p, c.p)) % c.p
    p.z = 1
    return p

# Adds a+b mod p, both a is [0,p-1] and b is [-p+1, p-1]
def add(a, b, p):
    if(b < 0):
        return sub(a, -b, p)
    c = a+b
    return c

def sub(a, b, p):
    c = a - b
    return c

# Adds a+b mod p, both a is [0,p-1] and b is [-p+1, p-1]
def add_mod(a, b, p):
    if(b < 0):
        return sub_mod(a, -b, p)
    c = a+b
    if c >= p:
        c = c - p
    if(c >= p or c < 0):
        print "Error add"
    return c

def sub_mod(a, b, p):
    c = a - b
    if c < 0:
        c = c + p
    if(c >= p or c < 0):
        print "Error"
    return c

# Calculates the montgomery product of x and y
def binary_montgomery(x, y, p, r):
    pr = 0
    for i in xrange(r.bit_length()-1):
        a = pr + ((x&(1<<i)) >> i) * y
        pr = (a>>1) if ((a & 1) == 0) else ((a + p)>>1)
        #print a, pr
    return (pr - p) if (pr >= p) else pr

def montgomery(x, y, c):
    M, Mt, Mp = c.p, c.pt, c.pp
    R, Rm = c.r, c.r_minus1
    k, n, d = c.k, c.n, c.d
    mask = (1<<k) - 1
    yp = y

    q = [0] * (n+d+2)
    S = [0] * (n+d+3)
    Y = [0] * (n+d+2)
    for i in xrange(n):
        Y[i] = (y & mask)
        y = (y>>k)

    for i in xrange(n+d+1):
        q[i+d] = (S[i] & mask)
        S[i+1] = (S[i]>>k) + q[i]*((Mt+1) >> (k*(d+1))) + Y[i] * x

    S[n+d+2] = (1<<(k*d)) * S[n+d+1]
    for j in xrange(d):
        S[n+d+2] = S[n+d+2] + (q[n+j+d+1]<<(k*j))

    while(S[n+d+2] >= c.p):
        S[n+d+2] = S[n+d+2] - c.p

    return S[n+d+2]



def convert_point_to_montgomery(q, p, r, r2):
    qq = copy.copy(q)
    qq.x = binary_montgomery(q.x, r2, p, r)
    qq.y = binary_montgomery(q.y, r2, p, r)
    qq.z = binary_montgomery(q.z, r2, p, r)
    return qq

def convert_point_to_standard(q, p, r):
    qq = copy.copy(q)
    qq.x = binary_montgomery(q.x, 1, p, r)
    qq.y = binary_montgomery(q.y, 1, p, r)
    qq.z = binary_montgomery(q.z, 1, p, r)
    return qq

def convert_curve_to_montgomery(c, p, r, r2):
    cc = copy.copy(c)
    cc.a = binary_montgomery(c.a % p, r2, p, r)
    cc.b = binary_montgomery(c.b % p, r2, p, r)
    return cc

def convert_int_to_montgomery(x, p, r, r2):
    return binary_montgomery(x, r2, p, r)

def convert_int_to_standard(x, p, r):
    return binary_montgomery(x, 1, p, r)
