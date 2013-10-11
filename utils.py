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
    return x
