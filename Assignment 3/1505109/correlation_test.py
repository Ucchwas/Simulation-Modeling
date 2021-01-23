from scipy import stats
import numpy as np
from collections import Counter
import math

alpha = .1
n = 20
j = 1

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

h = math.floor(((n-1)/j)-1)
sum=0
for i in range(0,h):
    sum += (U[1+i*j]*U[1+(i+1)*j])
sum -= 3

roj = (12/(h+1)) * sum

var = ((13*h+7)/((h+1)**2))

aj = roj / math.sqrt(var)

if (aj < 0):
    aj = aj*(-1)
print(aj)
z_alpha = stats.norm.ppf(1-(alpha/2))

if (aj > z_alpha):
    print("Rejected")
else:
    print("Accepted")
