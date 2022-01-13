import math
import Calculator as calc
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
# how to Draw 2D U_?

# constants:
m = 200  # 1.67e-27
R = 6371  # Earth radius
G = 6.673e-11  # C
M = 5.9742e24  # C

step_t = 1e-4
total_time = 5
# graph range
min_border = -4
max_border = 4
koef = 0  # для отображения графика

r0 = 200000
vr_0 = 2
# r0 = [200000, 200000]
# vr_0 = [-2, 0]


def potent_oscillator(x):
    w = 3
    return m * w**2 * x ** 2 / 2


def gravitational_planet_potential(x):
    if x < R:
        return 5e-20
    return -m * M * G / x


def force_oscillator(x):
    w = 3
    return -m * w**2 * x


def gravitational_planet_force(x):
    return -m * M * G / x**2


def gravitational_planet_potential_2D(radius):  # radius = sqrt(x**2 + y**2)
    # if abs(x - R) < 10:
    #     return -m * M * G / (R + 10)
    # if abs(y - R) < 10:
    #     return -m * M * G / (R + 10)
    # if x < R:
    #     return 5e-20
    # if y < R:
    #     return 5e-20
    if radius < R:
        return 5e-20
    return -m * M * G / radius


def gravitational_planet_force_2D(r_vec):
    return [-m * M * G * 2 * r_vec[0] / (r_vec[0]**2 + r_vec[1]**2)**(3.0/2),
            -m * M * G * 2 * r_vec[1] / (r_vec[0]**2 + r_vec[1]**2)**(3.0/2)]


global U_
global Force


def set_params(mode=True):
    global min_border
    global max_border
    global koef
    global r0
    global U_
    global Force

    if mode:
        min_border = 1
        max_border = R * 100
        koef = 1
        r0 = 200000
        U_ = gravitational_planet_potential
        Force = gravitational_planet_force
    else:
        min_border = -4
        max_border = 4
        koef = 10
        r0 = -2
        U_ = potent_oscillator
        Force = force_oscillator


def update(val):
    total_time = val
    t, r, v = calc.eqSolut(func_[0], m, r0, vr_0, total_time, step_t, func_[1])
    # uncomment all it
    # E_k_tmp = [(v[i]) ** 2 * m / 2 + U_(r[i - 1]) for i in range(1, len(r) - 1)]
    # E_k_tmp.append(E_k_tmp[-1])
    # E_k_tmp.append(E_k_tmp[-1])

    # line_rv.set_xdata(r)#change to _xy
    # line_rv.set_ydata(v)

    line_tv.set_xdata(t)
    line_tv.set_ydata(v)

    line_tr.set_xdata(t)
    line_tr.set_ydata(r)

    # line_rE.set_xdata(r)
    # line_rE.set_ydata(E_k_tmp)

    fg.canvas.draw_idle()


set_params(True)  # true - Earth, false - oscillator
# func_ = [U_, False]
func_ = [Force, True]
t, r, v = calc.eqSolut(func_[0], m, r0, vr_0, total_time, step_t, func_[1])


# r_x = [r[i][0] for i in range(0, len(r))]
# r_y = [r[i][1] for i in range(0, len(r))]

fg = plt.figure(figsize=(12, 7))
plt.subplot(221)
line_tr, = plt.plot(t, r, label='r')
plt.title('Coordinate_x')
plt.xlabel('t')
plt.ylabel('r')
plt.grid()

plt.subplot(222)
line_tv, = plt.plot(t, v, label='v')
plt.title('Speed_ x')
plt.xlabel('t')
plt.ylabel('v')
plt.grid()

# plt.subplot(223)
# line_rv, = plt.plot(r_x, r_y, label='Y(x)')
# plt.title('y(x)')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.grid()

# ucomment:
# E_k_tmp = [(v[i]) ** 2 * m / 2 + U_(r[i - 1]) for i in range(1, len(r) - 1)]
# E_k_tmp.append(E_k_tmp[-1])
#
# E_k_tmp.append(E_k_tmp[-1])
# x_arr = [(i / koef) for i in range(min_border * koef, max_border * koef)]
# U_arr = [U_(i / koef) for i in range(min_border * koef, max_border * koef)]

# plt.subplot(224)
# plt.plot(x_arr, U_arr, label='U')
# line_rE, = plt.plot(r, E_k_tmp, 'r-.', label='particle Energy')
# plt.title('Energy')
# plt.xlabel('r')
# plt.ylabel('E')
# plt.grid()

ax_total_time = plt.axes([0.1, 0.025, 0.8, 0.0125])
total_time_slider = Slider(
    ax=ax_total_time,
    label="t",
    valmin=0,
    valmax=100,
    valinit=total_time,
    valstep=1
)
total_time_slider.on_changed(update)

plt.show()
