from l1 import *
import numpy as np
from collections import deque



def get_plan(c, A, b, d_bottom, d_top):
    b, A, c = np.array(b), np.array(A), np.array(c)
    if (b < 0).any():
        indexes = b < 0
        b[indexes] *= (-1)
        A[indexes, :] *= (-1)

    m = len(A)
    n = len(A[0]) - m

    real_indexes = [i for i in range(n)]
    false_indexes = [i for i in range(n, n + m)]

    X = simplex(c, A, b, d_bottom, d_top, false_indexes)

    if X is None:
        print('inconsistent task')
        exit()

    X, J_b = X
    real_not_in_J_b = np.array(list(set(real_indexes) - set(J_b)))

    if J_b not in false_indexes:
        return J_b

    J_b.sort()
    k = 0
    while k < len(J_b):
        ind = J_b[k]
        if ind in false_indexes:
            A_inv_b = inv(ext_A[:, J_b])
            is_found = False
            for j in real_not_in_J_b:
                l = np.dot(A_inv_b, A[:, j])

                if l[k] != 0:
                    J_b[k] = j
                    is_found = True
                    break
            if not is_found:
                i = ind - n
                A = np.delete(A, k, axis=0)
                ext_A = np.delete(ext_A, k, axis=0)
                b = np.delete(b, k)
                for t, false_index in enumerate(false_indexes):
                    if false_index == ind:
                        false_indexes = np.delete(false_indexes, t)
                        break
                J_b = np.delete(J_b, k)
                continue
        k += 1

    return J_b


def smp_solver(c, A, b, got_bou):
    d_bottom = list(map(lambda i: i[0], got_bou))
    d_top =list(map(lambda i: i[1], got_bou))

    J_b = get_plan(c, A, b, d_bottom, d_top)
    x_opt, J_b = simplex(c, A, b, d_bottom, d_top, J_b)

    return x_opt



def checkint(mb_int):
    if abs((mb_int + 1e-6) // 1 - mb_int) < 1e-6:
        return True


def integer_prog_task_solve(c, A, b, x_bounds):
    epsilon = 1e-6
    answer = -np.inf
    mu0 = 0
    mu = np.zeros(len(c))
    Q = deque()
    Q.append(x_bounds)
    ii = 0
    while len(Q) != 0:
        ii += 1
        print(ii)
        got_bou = Q.popleft()
        r_ = smp_solver(c, A, b, got_bou)
        if r_ is None:
            print('con')
            continue

        if any(not checkint(value) for value in r_):
            if np.dot(r_, c) < answer:
                continue

        finish_flag = False

        for i in range(len(r_)):
            if not checkint(r_[i]):
                b1, b2 = got_bou[:], got_bou[:]
                b1[i], b2[i] = [got_bou[i][0], (r_[i] + epsilon) // 1], \
                               [(r_[i] + epsilon) // 1 + 1, got_bou[i][1]]
                if got_bou != b1:
                    Q.append(b1)
                if got_bou != b2:
                    Q.append(b2)
                finish_flag = True
                break

        if finish_flag:
            continue

        _answer = np.dot(r_, c)
        if _answer > answer:
            mu, mu0, answer = r_, 1, _answer

    return mu if mu0 == 1 else None


if __name__ == "__main__":
 
    a = [
       [2, 1, -1, 0, 0, 1],
       [1, 0, 1, 1, 0, 0],
       [0, 1, 0, 0, 1, 0]
    ]

    b = [2, 5, 0]
    c = [3, 2, 0, 3, -2, -4]
    bounds = [[0, 2], [-1, 4],[ 2, 4],[ 1, 3], [-1, 3],[ 0, 5]]

    answer = integer_prog_task_solve(c, a, b, bounds)
    if answer is not None:
        print("X: {0}".format(answer))
        print("result: {0}".format(np.dot(answer, c)))
    else:
        print("NONE")
