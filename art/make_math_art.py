"""
Based on https://stackoverflow.com/questions/70721139/pyplot-how-to-plot-math-art

"""
import matplotlib.pyplot as plt
from math import sin, cos, pi
import numpy as np

num = 14000
theta = np.linspace(0, 2*pi, 361)

fig, ax = plt.subplots(figsize=(10, 10))

for k in range(1, num + 1):
    x = cos(10*pi*k/num)*(1 - 1/2*(cos(16*pi*k/num))**2)
    y = sin(10*pi*k/num)*(1 - 1/2*(cos(16*pi*k/num))**2)
    r = 1/200 + 1/10*(sin(52*pi*k/num))**4

    x_vec = r*np.cos(theta) + x
    y_vec = r*np.sin(theta) + y

    ax.plot(x_vec, y_vec, color='blue', linewidth=0.1)

ax.set_axis_off()
plt.savefig(f'make_math_art_{num}.png', bbox_inches='tight')
plt.close()
