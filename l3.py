from l1 import simplex 
import numpy as np 

EPS = 1e-10
inf = 1e100


def __fraction(x):
    return (x + EPS) // 1 - x 


def __is_int(x):
    return abs(__fraction(x)) < EPS

def gomory(c, a, b, d_bot, d_top):
    a = np.array(a[:])
    b = np.array(b[:])
    c = np.array(c[:])
    n, m = len(c), len(b)
    __i = 1
    while True:
        x, Jb = simplex(c, a, b, d_bot, d_top)
        print("Iteration: " + str(__i))
        print("plan     : " + str([ "%.2f" % i for i in x]))
        print("basis    : " + str(Jb))
        if x is None:
            return None

        ok = True
        for i in range(n):
            ok &= __is_int(x[i])
        if ok:
            return x[:n]
        ok = True
        for v, i in enumerate(Jb):
            ok &= __is_int(x[i])
            if not ok:
                j0 = i
                k = v
                break
        Ab = a[:, Jb]
        B = np.linalg.inv(Ab)

        ej0 = np.eye(len(Jb), len(Jb))[:, k]
        y = np.dot(ej0, B)
        beta = np.dot(y, b)
        alpha = np.dot(y, a)
        row = [__fraction(i) for i in alpha]
        row.append(1)
       
        _a = np.zeros((a.shape[0]+1, a.shape[1]+1))
        _a[:-1,:-1] = a
        _a[-1,:] = row
        a = _a

        b = np.append(b, __fraction(beta))
        d_bot.append(0)
        d_top.append(inf)
        c = np.append(c, 0)
        __i += 1


if __name__ == "__main__":
    c = [-1, -3, -7, 0, -4, 0, -1]
    b = [4, 8, 24]
    a = [[1, 0, -1, 3, -2, 0, 1],
         [0, 2, 1, -1, 0, 3, -1],
         [1, 2, 1, 4, 2 ,1, 1]]
    d_top = [inf, inf, inf, inf, inf, inf, inf]
    d_bot = [0, 0, 0, 0, 0, 0, 0]

    res = gomory(c, a, b, d_bot, d_top)
    print("Optimal plan: {0}".format(res))
    print("Value is: {0}".format(np.dot(res, c)))
