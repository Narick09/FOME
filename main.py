import math
import Calculator as calc
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

r0 = 200000#-2
vr_0 = -2
total_time = 5
m = 1.67e-27
step_t = 1e-4
min_border = -40
max_border = 40
R = 1e-2 #мат точка
#R = 6371 #Earth radius
G = 6.673e-11  # C
M = 5.9742e24  # C

def potent_oscillator(x):
    w = 3
    global min_border
    min_border = -40
    global max_border
    max_border = 40
    return m * w**2 * x ** 2 / 2


def gravitational_potential(x):
    g = 10
    global min_border
    min_border = -40
    global max_border
    max_border = 40
    return m * g * x


def gravitational_planet_potential(x):
    global min_border
    min_border = 1
    global max_border
    max_border = r0 + 1000
    # if abs(x - R) < 10:
    #     return -m * M * G / (R + 10)
    if abs(x) < R:
        return -m * M * G / R
    return -m * M * G / x


def U_(x):
    return gravitational_planet_potential(x)

def gravitational_planet_force(x):
    if abs(x) < R:
        return -m * M * G / (R**2)
    return -m * M * G / (x**2)

def Force(x):
    return gravitational_planet_force(x)

def update(val):
    total_time = val
    t, r, v = calc.eqSolut(Force, m, r0, vr_0, total_time, step_t)

    E_k_tmp = [(v[i]) ** 2 * m / 2 + U_(r[i - 1]) for i in range(1, len(r) - 1)]
    E_k_tmp.append(E_k_tmp[-1])
    E_k_tmp.append(E_k_tmp[-1])

    line_rv.set_xdata(r)
    line_rv.set_ydata(v)

    line_tv.set_xdata(t)
    line_tv.set_ydata(v)

    line_tr.set_xdata(t)
    line_tr.set_ydata(r)

    line_rE.set_xdata(r)
    line_rE.set_ydata(E_k_tmp)

    fg.canvas.draw_idle()


t, r, v = calc.eqSolut(Force, m, r0, vr_0, total_time, step_t)
fg = plt.figure(figsize=(12, 7))
plt.subplot(221)
line_tr, = plt.plot(t, r, label='r')
plt.title('Coordinate')
plt.xlabel('t')
plt.ylabel('r')
plt.grid()

plt.subplot(222)
line_tv, = plt.plot(t, v, label='v')
plt.title('Speed')
plt.xlabel('t')
plt.ylabel('v')
plt.grid()

plt.subplot(223)
line_rv, = plt.plot(r, v, label='v_rad(x)')
plt.title('V (x)')
plt.xlabel('r')
plt.ylabel('v_rad')
plt.grid()

#    E_k_tmp = [((x[i] - x[i-1]) / step_t)**2 * m / 2 + U_(x[i - 1]) for i in range(1, len(x))]
E_k_tmp = [(v[i]) ** 2 * m / 2 + U_(r[i - 1]) for i in range(1, len(r) - 1)]
E_k_tmp.append(E_k_tmp[-1])

E_k_tmp.append(E_k_tmp[-1])
# x_arr = [(i * 0.1) for i in range(-40, 40)]
# U_arr = [U_(i*0.1) for i in range(-40, 40)]

x_arr = [i for i in range(1, r0 + 1000)]
U_arr = [U_(i) for i in range(1, r0 + 1000)]

plt.subplot(224)
plt.plot(x_arr, U_arr, label='U')
line_rE, = plt.plot(r, E_k_tmp, 'r-.', label='particle Energy')
plt.title('Energy')
plt.xlabel('r')
plt.ylabel('E')
plt.grid()

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
