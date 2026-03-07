
import numpy as np

# compute the Euler-based numerical approximation
# to the falling parachutist problem
#
# return the result as a np.array with two columns
# the first one containing the times in seconds
# and the second the values of the approximation

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

# Your code goes here
# result_1a =

# Your code goes here
# result_1b =


# Your code goes here
# result_1c =

def skyfall_analytic(g,m,c,t):
  # modify code as described above to return the right value
  return 0

def relative_error(exact, approximate):
  # modify code as described above to return the right value
  return 0


def skyfall_numeric(g,m,c,t):
  # modify code as described above to return the right value
  return 0

# this code will display the relative error once the functions are
# implemented correctly
p = skyfall_analytic (9.81,62.8,12.5,12)
pstar = skyfall_numeric(9.81,62.8,12.5,12)

e_a = relative_error(p, pstar)
print(f"Relative Error: {e_a:8.4f}")



def skyfall_euler2(m,k,g,t0,v0,tn,n):
  # modify code as described above to return the right array of times and values
  result = np.zeros((n+1,2))
  return result

result_2a = skyfall_euler2(73.5,0.234,9.81,0,0,18,72)
# output_values(result_2a)

def skyfall_analytic2(g,m,k,t):
  # modify code as described above to return the right value
  return 0

def skyfall_numeric2(g,m,c,t):
  # modify code as described above to return the right value
  return 0


p =  skyfall_analytic2(9.81, 73.5, 0.234, 18)
pstar = skyfall_numeric2(9.81, 73.5, 0.234, 18)
e_a = relative_error(p, pstar)

relative_error_scientific = f"{e_a:e}"  # Using f-string
print(relative_error_scientific)

import math

# enegx_Taylor1 Approximates e^(-x) with the
# nth degree McLaurin polynomial for e^(-x)

def enegx_Taylor1(x,n):
  # modify code as described above to return the right value
  return 0

# enegx_Taylor2 Approximates e^(-x) with 1 over
# the nth degree McLaurin polynomial for e^x

def enegx_Taylor2(x,n):
  # modify code as described above to return the right value
  return fx


# approximations1 =
# approximations2 =
# exact =

# print(exact)
# print(approximations1)
# print(approximations2)

# relative_error1 =
# relative_error2 =

# print(relative_error1)
# print(relative_error2)


import matplotlib.pyplot as plt

# your code goes here
fig, ax = plt.subplots()


plt.plot([1.0, 3.0, -2.0, 5.0, 1.5], label='Random')
# random plot - remove in your submission

# Add labels and title
plt.xlabel("Order of polynomial approximation")
plt.ylabel("Approximate value of function")

# change title appropriately
plt.title("Random Plot")

plt.legend()
# save the plot to a file
plt.savefig("csc349a_asn1_q3.png", dpi=300, bbox_inches='tight')

# Display the plot
# plt.show()


# set the best approximation to either "Approximation 1" or "Approximation 2"
# depending on which one you consider best
# best_approximation =



