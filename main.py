import math
import Calculator as calc
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

r0 = -2
vr_0 = -5
total_time = 2
N = 100000
m = 1.67e-27
step_t = total_time / N


def potent_oscillator(x):
    w = 3
    return m * w**2 * x ** 2 / 2


def gravitational_potential(x):
    g = 10
    return m * g * x


def U_(x):
    return potent_oscillator(x)


def update(val):
    total_time = val
    step_t = total_time / N
    t, r, v = calc.eqSolut(U_, m, r0, vr_0, total_time, step_t)

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


t, r, v = calc.eqSolut(U_, m, r0, vr_0, total_time, step_t)
fg = plt.figure(figsize=(12, 7))
plt.subplot(221)
line_tr, = plt.plot(t, r, label='r')
plt.title('functions')
plt.xlabel('t')
plt.ylabel('r')
plt.grid()

plt.legend()
plt.subplot(222)
line_tv, = plt.plot(t, v, label='v')
plt.title('functions')
plt.xlabel('t')
plt.ylabel('v')
plt.grid()

plt.legend()
plt.subplot(223)
line_rv, = plt.plot(r, v, label='v_rad(x)')
plt.title('functions')
plt.xlabel('r')
plt.ylabel('v_rad')
plt.grid()

#    E_k_tmp = [((x[i] - x[i-1]) / step_t)**2 * m / 2 + U_(x[i - 1]) for i in range(1, len(x))]
E_k_tmp = [(v[i]) ** 2 * m / 2 + U_(r[i - 1]) for i in range(1, len(r) - 1)]
E_k_tmp.append(E_k_tmp[-1])

E_k_tmp.append(E_k_tmp[-1])
x_arr = [(i * 0.1) for i in range(-40, 40)]

U_arr = [U_(i*0.1) for i in range(-40, 40)]
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
    valmax=20,
    valinit=total_time,
    valstep=1
)
total_time_slider.on_changed(update)

plt.show()
