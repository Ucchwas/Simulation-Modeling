from scipy import stats
import numpy as np
from collections import Counter
import math

k = 4
alpha = .1
n = 20
roll = 1505109
d = 2

def seed(val):
    global rand
    rand = val

def generate():
    global rand
    rand = (65539*rand) % (2**31)
    return rand / (2**31)

seed(roll)

U_i = []
for i in range(0,n):
    U_i.append(generate())

l = math.floor(n/d)
U = [[] for i in range(l)]

count = 0
for i in range(l):
    for j in range(d):
        U[i].append(U_i[count])
        count += 1

dx = float(1.0/k)
f = dict()
for i in range(l):
    res = 'f'
    for j in range(d):
        s = str(math.floor(float(U[i][j] / dx)))
        res += s
    if res in f.keys():
        f[res] += 1
    else:
        f[res] = 1

sum=0
for key in f.keys():
    sum += math.pow((f[key]-float(n/(math.pow(k,d)))),2)
sum += math.pow((-float(n/(math.pow(k,d)))),2) * (math.pow(k,d)-len(f))
chi_square = sum * float(math.pow(k,d)/n)

df = math.pow(k,d)-1
chi_square_th = stats.chi2.ppf(1-alpha,df)

print("Emperical Value : ", chi_square)
print("Theoritical Value : ", chi_square_th)

if (chi_square > chi_square_th):
    print("Reject")
else:
    print("Accepted")

