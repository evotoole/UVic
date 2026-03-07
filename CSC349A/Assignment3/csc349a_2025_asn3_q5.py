
import numpy as np
from functools import partial



def add(x,y):
    return x + y 

add_5 = partial(add, y=5)

def spherical_tank_specific(h,):
    R = 4.1
    d = 45 
    return (np.pi * h ** 2 * (3 * R - h))/3 - d    

def spherical_tank_general(h,R,d):
    return (np.pi * h ** 2 * (3 * R - h))/3 - d

sp_tank = partial(spherical_tank_general, R=4.1, d=45)


def parachute_specific(m):
    g = 9.81
    c = 15
    t = 10
    v = 36
    return (m*g/c) * (1 - np.exp(-c*t/m)) - v
    

def parachute_general(m, g, c, t, v):
    # add your code here 
    return (m*g/c) * (1 - np.exp(-c*t/m)) - v

# edit the line below appropriately 
parachute = partial(parachute_general, g = 9.81,c = 15, t = 10, v = 36)


def bisect(xl, xu, eps, imax, f):
    i = 1
    fl=f(xl)
    print(' iteration approximation \n')
    while i <= imax:
        # add your code here 
        xr = (xl + xu)/2
        fr=f(xr)
        # uncomment the lines below 
        print('{:6.0f} {:18.9f}'.format(i,xr))

        if (fr ==0) or (((xu - xl)/abs(xu + xl)) < eps):
            return xr
        if fl*fr < 0:
            xu = xr
        else:
            xl = xr
            fl = fr
        # add your code here 
        i = i + 1

    print(' failed to converge in ', imax, ' iterations\n')
    


print(add_5(10))
root1 = bisect(0.0, 4.1, 1e-4, 20, spherical_tank_specific)
root2 = bisect(0.0, 4.1, 1e-4, 20, sp_tank)
# uncomment the lines below 
root3 = bisect(1.0, 100.0, 1e-4, 20, parachute_specific)
root4 = bisect(1.0, 100.0, 1e-4, 20, parachute)


