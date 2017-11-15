import numpy as np
from numpy.linalg import inv
from functools import reduce

EPS = 1e-9

def not_basis(n, J_b):
    nb = []
    for index in range(n):
        if index not in J_b:
            nb.append(index)

    return nb

def get_j0(A):
    m, n = len(A), len(A[0])
    ans = {}
    ans[0] = []

    def rec(ans, vals):
        if len(vals) == m:
            if len(ans[0]) == 0 and abs(np.linalg.det(A[:, vals])) > EPS:
                ans[0] = vals[:]
            return
        prev = vals[-1] if len(vals) > 0 else -1
        for i in range(prev + 1, n):
            tvals = vals[:]
            tvals.append(i)
            rec(ans, tvals)

    rec(ans, [])

    return ans[0]

def simplex(c, A, b, d_bottom, d_top, J_b=None):
    x, y, J_b = simplex_next(c, A, b, d_bottom, d_top, J_b)
    return x, J_b

def simplex_next(c, A, b, d_bottom, d_top, J_b=None):
    c = np.array(c)
    b = np.array(b)
    A = np.array(A)
    d_bottom = np.array(d_bottom)
    d_top = np.array(d_top)

    n, m = len(c), len(b)
    if J_b == None:
        J_b = get_j0(A)
    A_b = A[:, J_b]
    print(A_b)
    B = inv(A_b)
    # print(c, J_b)
    y = np.dot(c[J_b], B)
    delta = np.dot(y, A) - c
    J_n = not_basis(n, J_b)

    Jn_plus, Jn_minus = [], []

    for index in J_n:
        if delta[index] >= EPS:
            Jn_plus.append(index)
        else:
            Jn_minus.append(index)

    _i = 0
    while _i < 100:
        _i += 1
        # print('iter: ' + str(_i))
        # print('J: {1}\n'.format(y, J_b))
        cappa = np.zeros(n)
        for i in Jn_plus:
            cappa[i] = d_bottom[i]
        for i in Jn_minus:
            cappa[i] = d_top[i]

        s = np.zeros(m)
        for i in J_n:
            s += np.dot(A[:, i], cappa[i])
        d_xi = np.dot(B, b - s)
        for val, ind in enumerate(J_b):
            cappa[ind] = d_xi[val]

        success = []
        for i in J_b:
            success.append(d_bottom[i] - EPS <= cappa[i] <= d_top[i] + EPS)

        if all(success):
            return cappa, -np.dot(c[J_b], B), J_b

        jk = np.inf

        for val, i in enumerate(J_b):
            if cappa[i] < d_bottom[i] - EPS or cappa[i] > d_top[i] + EPS:
                if jk > i:
                    jk, k = i, val

        m_j_k = 1 if cappa[jk] < d_bottom[jk] else -1
        delta_y = np.dot(m_j_k, np.dot(np.eye(m, m)[:, k], B))
        mu = np.zeros(n)
        for i in J_n:
            mu[i] = np.dot(delta_y, A[:, i])
        mu[jk] = m_j_k

        sigma = np.zeros(n)
        for i in Jn_plus:
            sigma[i] = -delta[i] / mu[i] if mu[i] < 0 else np.inf
        for j in Jn_minus:
            sigma[j] = -delta[j] / mu[j] if mu[j] > 0 else np.inf

        sigma0 = min(sigma[J_n])
        if sigma0 == np.inf:
            print('function not limited with {0}'.format(sigma0))
            return None

        for i in J_n:
            if sigma[i] == sigma0:
                j0 = i

        for i in J_n:
            delta[i] += np.dot(sigma0, mu[i])
        delta[jk] = np.dot(sigma0, mu[jk])

        for i in J_b:
            if i != jk:
                delta[i] = 0.0

        J_b[J_b.index(jk)] = j0
        
        A_b = A[:, J_b]
        J_n = not_basis(n, J_b)
        if m_j_k == 1:
            if j0 in Jn_plus:
                Jn_plus.remove(j0)
                Jn_plus.append(jk)
            else:
                Jn_plus.append(jk)
        if m_j_k == -1:
            if j0 in Jn_plus:
                Jn_plus.remove(j0)

        Jn_minus = []
        for i in J_n:
            if not i in Jn_plus:
                Jn_minus.append(i)

        z = np.dot(B, A_b[:, k])
        d = z.copy()
        d[k] = -1
        q = np.dot(-(1.0 / z[k]), d)
        E = np.eye(m, m)
        E[:, k] = q.copy()
        B = np.dot(E, B)

    return None

if __name__ == '__main__':
    A = np.array([
       [2, 1, -1, 0, 0, 1],
       [1, 0, 1, 1, 0, 0],
       [0, 1, 0, 0, 1, 0]
    ])
    b = np.array([2, 5, 0])
    c = np.array([3, 2, 0, 3, -2, -4])
    dl = np.array([0, -1, 2, 1, -1, 0])
    dh = np.array([2, 4, 4, 3, 3, 5])
    J_b = [0, 2, 1]

    x, J_b = simplex(c, A , b, dl, dh, J_b)
    print('X: {0}\nJ: {1}\nresult: {2}'.format(x, J_b, np.dot(c, x), J_b, x))



