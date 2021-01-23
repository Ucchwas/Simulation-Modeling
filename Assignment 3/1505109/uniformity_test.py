from scipy import stats
import numpy as np

k = 20
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
    print("Reject")
else:
    print("Accepted")













