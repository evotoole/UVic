import math as m

a = 10000
b = -460
c = 23**2 - ((1.645)**2)*23*77

def quadratic(a,b,c):
    minus = (-b - m.sqrt((b**2) - (4*a*c)))/(2*a)
    plus = (-b + m.sqrt((b**2) - (4*a*c)))/(2*a)
    return (round(plus, 5), round(minus, 5))

print(quadratic(a,b,c))

mle = 23/100
val = 1.645
n = 100
print(mle + val*(m.sqrt((mle*(1-mle))/n)))