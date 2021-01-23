from scipy import stats
import numpy as np
from collections import Counter
import math
from numpy.matlib import rand

roll = 1505109
alpha = 0.1

def seed(val):
    global rand
    rand = val

def generate():
    global rand
    rand = (65539*rand) % (2**31)
    return rand / (2**31)

seed(roll)

def uniformity_test(n,k):
    print("Uniformity Test")
    U = []
    for i in range(0,n):
        U.append(generate())

    k_s = []
    k_s.append(0.0)
    interval = 1 / k
    index = 0
    count = 0
    f_j = []

    while (index < 1.0):
        index += interval
        k_s.append(index)

    for i in range(len(k_s)-1):
        for j in range(len(U)):
            if (U[j] >= k_s[i]):
                if (U[j] < k_s[i+1]):
                    count += 1
        f_j.append(count)
        count = 0

    chi = 0
    for i in range(len(f_j)):
        chi += (f_j[i] - (n / k))*(f_j[i] - (n / k))

    chi_square = (k / n) * chi

    chi_square_th = stats.chi2.ppf(1-alpha,k-1)

    print("Emperical Value : ", chi_square)
    print("Theoritical Value : ", chi_square_th)

    if (chi_square > chi_square_th):
        print("Rejected")
    else:
        print("Accepted")

#uniformity_test(500,20)

def serial_test(n,k,d):
    print("Serial Test")
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
        print("Rejected")
    else:
        print("Accepted")

#serial_test(20,4,2)

def runs_test(n):
    print("Runs Test")
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
        print("Rejected")
    else :
        print("Accepted")

#runs_test(500)

def correlation_test(n,j):
    print("Correaltion Test")
    U = []
    for i in range(0,n):
        U.append(generate())

    h = math.floor(((n-1)/j)-1)
    sum = 0
    for i in range(0,h):
        sum += (U[1+i*j]*U[1+(i+1)*j])
    sum -= 3

    roj = (12/(h+1)) * sum

    var = ((13*h+7)/((h+1)**2))

    aj = roj / math.sqrt(var)

    if (aj < 0):
        aj = aj*(-1)
    print("A : ", aj)
    z_alpha = stats.norm.ppf(1-(alpha/2))
    print("Z alpha :",z_alpha)
    if (aj > z_alpha):
        print("Rejected")
    else:
        print("Accepted")

#correlation_test(20,1)


#uniformity_test(10000,20)
#serial_test(10000,8,3)
#runs_test(10000)
#correlation_test(10000,5)