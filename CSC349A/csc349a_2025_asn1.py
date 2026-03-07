import numpy as np
import math
import matplotlib.pyplot as plt

def skyfall_euler(m,c,g,t0,v0,tn,n):
  # computer step size h
  h = (tn-t0)/n
  # set t, v to initial values
  t = t0
  v = v0

  # allocate array for result
  result = np.zeros((n+1,2))
  result[0] = [t,v]
  # compute v(t) over n time steps using Euler’s method
  for i in range(1,n+1):
    v=v+(g-c/m*v)*h
    t=t+h
    result[i,:] = [t,v]
  return result

# print the returned values
def output_values(result):
  print('value of t approximation v(t)\n')
  for r in result:
    t,v = r
    print(f"{t:8.3f} {v:19.4f}")

result_1a = skyfall_euler(m=68.1, c=12.5, g=9.81, t0=0, v0=0, tn=12, n=6)
output_values(result_1a)

result_1b = skyfall_euler(m=62.8, c=12.5, g=9.81, t0=0, v0=0, tn=12, n=15)
output_values(result_1b)

result_1c = skyfall_euler(m=62.8, c=12.5, g=3.71, t0=0, v0=0, tn=12, n=15)
output_values(result_1c)

def skyfall_analytic(g,m,c,t):
  # modify code as described above to return the right value
  return ((g*m)/c)*(1-(np.exp(((-c*t)/m))))

def relative_error(exact, approximate):
  # modify code as described above to return the right value
  num = (exact - approximate)/exact
  return abs(num)


def skyfall_numeric(g,m,c,t):
  # modify code as described above to return the right value
  ans = skyfall_euler(m=m, c=c, g=g, t0=0, v0=0, tn=t, n=15)
  return ans[-1,1]

p = skyfall_analytic (9.81,62.8,12.5,12)
pstar = skyfall_numeric(9.81,62.8,12.5,12)

e_a = relative_error(p, pstar)
print(f"Relative Error: {e_a:8.4f}")

def skyfall_euler2(m,k,g,t0,v0,tn,n):
  # computer step size h
  h = (tn-t0)/n
  # set t, v to initial values
  t = t0
  v = v0
  
  # modify code as described above to return the right array of times and values
  result = np.zeros((n+1,2))
  

  # allocate array for result

  result[0] = [t,v]
  # compute v(t) over n time steps using Euler’s method
  for i in range(1,n+1):
    v+=h*(g-(k/m)*(v**2))
    t=t+h
    result[i,:] = [t,v]
 
  return result

result_2a = skyfall_euler2(73.5,0.234,9.81,0,0,18,72)
output_values(result_2a)


def skyfall_analytic2(g,m,k,t):
  # modify code as described above to return the right value
  return np.sqrt((g*m)/k) * np.tanh(np.sqrt((g*k)/m) * t)

def skyfall_numeric2(g,m,c,t):
  return skyfall_euler2(g=g,m=m,k=c,t0=0,v0=0,tn=t,n=72)[-1,1]


p =  skyfall_analytic2(9.81, 73.5, 0.234, 18)
pstar = skyfall_numeric2(9.81, 73.5, 0.234, 18)
e_a = relative_error(p, pstar)

relative_error_scientific = f"{e_a:e}"  # Using f-string
print(relative_error_scientific)

def enegx_Taylor1(x,n):
  # modify code as described above to return the right value
  e = 0
  for i in range (0,n+1):
      e += ((-x)**i) / math.factorial(i)
  return e

# enegx_Taylor2 Approximates e^(-x) with 1 over
# the nth degree McLaurin polynomial for e^x

def enegx_Taylor2(x,n):
  e = 0
  for i in range (0,n+1):
    e += (x**i)/(math.factorial(i))
  return 1/e

exact = np.array([np.exp(-2.0)]*5)

approximations1 = np.array([enegx_Taylor1(2.0,i) for i in range(1, 6)])
approximations2 = np.array([enegx_Taylor2(2.0,i)for i in range(1, 6)])
    
print(exact)
print(approximations1)
print(approximations2)


relative_error1 = np.abs((exact - approximations1) / exact)
relative_error2 = np.abs((exact - approximations2) / exact)
    
print(relative_error1)
print(relative_error2)

import matplotlib.pyplot as plt
orders = range(0, len(relative_error1))
fig, ax = plt.subplots()  # Create figure and axes

plt.plot(orders, approximations1, label='Approximation 1')
plt.plot(orders, approximations2, label='Approximation 2')
plt.plot(orders, exact, label = 'Exact')


plt.xlabel("Order of polynomial approximation")
plt.ylabel("Approximate value of function")
plt.title("exp(-2.0) Taylor Series approximations")
plt.legend()

plt.savefig("csc349a_asn1_q3.png", dpi=300, bbox_inches='tight')
plt.show()
if np.abs(approximations2[-1] - exact[0]) < np.abs(approximations1[-1] - exact[0]):
  best_approximation = "Approximation 2"
else:
  best_approximation = "Approximation 1"