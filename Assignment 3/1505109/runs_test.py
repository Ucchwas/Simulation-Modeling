from scipy import stats
import numpy as np
from collections import Counter


alpha = .1
n = 500
roll = 1505109

def seed(val):
    global rand
    rand = val

def generate():
    global rand
    rand = (65539*rand) % (2**31)
    return rand / (2**31)

seed(roll)
U = []
for i in range(0,n):
    U.append(generate())

count = 0
r_arr = []

for i in range(len(U)-1):
    count += 1
    if (U[i] > U[i+1]):
        r_arr.append(count)
        count = 0

r = Counter(r_arr)

a = [[4529.4, 9044.9, 13568, 18091, 22615, 27892],
     [9044.9, 18097, 27139, 36187, 45234, 55789],
     [13568, 27139, 40721, 54281, 67852, 83685],
     [18091, 36187, 54281, 72414, 90470, 111580],
     [22615, 45234, 67852, 90470, 113262, 139476],
     [27892, 55789, 83685, 111580, 139476, 172860]]


b = [1 / 6, 5 / 24, 11 / 120, 19 / 720, 29 / 5040, 1 / 840]

sum = 0
for i in range(6):
    for j in range(6):
        sum += a[i][j] * (r[i+1] - (n*b[i])) * (r[j+1] - (n*b[j]))

R = sum / n

R_th = stats.chi2.ppf(1-alpha,6)

print("Emperical Value : ", R)
print("Theoritical Value : ", R_th)


if (R > R_th):
    print("Reject")
else :
    print("Accepted")








