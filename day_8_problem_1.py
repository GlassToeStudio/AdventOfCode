import math
from collections import Counter

f = open("Data/day-8.txt", "r")
a = f.read()


def B(c, d, e):
    f = []
    g = 0
    h = d * e
    i = int(len(c) / h)
    j = h
    for k in range(i):
        f.append([int(x) for x in c[g:j]])
        g = j
        j += h
    return f


def L(m, n):
    o = 0
    p = math.inf
    for q in range(len(m)):
        c = R(m[q], n)
        if c < p:
            o = q
            p = c
    return o


def R(s, t):
    u = Counter(s)
    return u[t]


def V(w, x):
    y = L(w, x)
    z = R(w[y], 1)
    aa = R(w[y], 2)
    return z * aa


if __name__ == "__main__":
    ab = B(a, 25, 6)
    print(V(ab, 0))

# Your puzzle answer was 2016
