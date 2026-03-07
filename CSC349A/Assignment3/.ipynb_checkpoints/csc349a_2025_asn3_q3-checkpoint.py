import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0.0, 6.0, 0.02)
fx = np.sqrt(x + 1)
px = 2 + (x - 3)/4 - ((x - 3)**2)/64  # or your correct Taylor formula

fig, ax = plt.subplots()

# assign the first plot to 'plot' for the autograder
plot = plt.plot(x, fx, label='sqrt(x+1)', color='red')
plt.plot(x, px, label='taylor', color='blue')

plt.title('sqrt(x+1) and taylor approximation')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()