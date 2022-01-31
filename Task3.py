import numpy as np
import Calculator as calc
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# true - Earth, false - Oscillator
Earth = True
Oscillator = False

choose_field = Earth  # тут выбирать, что рисовать - гравитационное, или осциллятор
# настройка параметров ниже - в функции set_params

# constants:
R = 6371000.0  # Earth radius
G = 6.673e-11  # C
M = 5.9742e24  # C

global step_t
global total_time

global m
global w

global r0
global vr_0


def trans(x, y):
    r_temp = np.sqrt(x**2 + y**2)
    temp_2 = y / r_temp
    if temp_2 > 1:
        temp_3 = np.pi / 2
    elif temp_2 < -1:
        temp_3 = -np.pi / 2
    else:
        temp_3 = np.arcsin(temp_2)

    if temp_3 >= 0:
        temp = x / r_temp
        if temp > 1:
            hi = 0.0
        elif temp < -1:
            hi = np.pi
        else:
            hi = np.arccos(temp)
    else:
        temp = x / r_temp
        if temp > 1:
            hi = 0.0
        elif temp < -1:
            hi = np.pi
        else:
            hi = 2 * np.pi - np.arccos(temp)
    return r_temp, hi


def gravitational_planet_potential(x):
    if x < R:
        return 5e-20
    return -m * M * G / x


def gravitational_planet_force_2D(r_vec):
    A = -m * M * G
    if r_vec[0]**2 + r_vec[1]**2 <= R**2:
        return np.array([0, 0])

    arr_r, arr_hi = trans(r_vec[0], r_vec[1])
    return np.array([A * np.cos(arr_hi) / arr_r**2,
                     A * np.sin(arr_hi) / arr_r**2])


def potent_oscillator(r_mod):
    return m * w * r_mod ** 2 / 2


def oscillator_force_2D(r_vec):
    return np.array([-m * w * r_vec[0], -m * w * r_vec[1]])


global U_
global Force


def set_params(mode=Earth):
    global m
    global r0
    global vr_0
    global U_
    global Force
    global w
    global total_time
    global step_t

    if mode:  # здесь настраиваются начальные параметры для 2д случая гравитационного поля
        m = 1000
        vr_0 = np.array([-4000.0, 0.0])
        total_time = 100000
        step_t = 100.0
        r0 = np.array([R + 2 * R, R + 3 * R])
        U_ = gravitational_planet_potential
        Force = gravitational_planet_force_2D
    else:  # здесь настраиваются начальные параметры для 2д случая поля осциллятора
        m = 1.67e-27
        vr_0 = np.array([-2.0, 0.0])
        w0 = 3
        w = w0**2
        total_time = 5
        step_t = 1e-3
        r0 = np.array([2.0, 1.0])
        U_ = potent_oscillator
        Force = oscillator_force_2D


def update(val):
    total_time = int(total_time_slider.val)
    t = [0.0]
    r = [r0]
    v = [vr_0]

    r_x = []
    r_y = []
    v_x = []
    v_y = []

    r_norm = []
    v_mod = []
    fi_in_v = []
    E_full = []

    v_fi = []
    x_eff = []
    U_eff = []

    last_size = 0

    koef_tmp = 2
    total_time_tmp = koef_tmp * step_t
    for i in range(0, total_time + int(step_t), int(step_t)):
        tmp_t, tmp_r, tmp_v = calc.eqSolut(func_, m, r[-1], v[-1], i, total_time_tmp, step_t)
        [t.append(tmp_t[k]) for k in range(1, len(tmp_t))]
        [r.append(tmp_r[k]) for k in range(1, len(tmp_r))]
        [v.append(tmp_v[k]) for k in range(1, len(tmp_v))]


        # этап попыток внедрения возможности изменения радиальной и тангенсиальной скоростей:
        # сюда р_х, р_у, в_х, в_у и т.п. - чтобы их вычислять, и тут же вычислять следующие параметры - Энергию и т.п.
        [r_x.append(r[k][0]) for k in range(last_size, len(t))]
        [r_y.append(r[k][1]) for k in range(last_size, len(t))]
        [v_x.append(v[k][0]) for k in range(last_size, len(t))]
        [v_y.append(v[k][1]) for k in range(last_size, len(t))]
        # r_x = [r[i][0] for i in range(0, len(r))]
        # r_y = [r[i][1] for i in range(0, len(r))]
        # v_x = [v[i][0] for i in range(0, len(v))]
        # v_y = [v[i][1] for i in range(0, len(v))]

        [r_norm.append(np.linalg.norm(r[k])) for k in range(last_size, len(t))]
        # r_norm = [np.linalg.norm(r[i]) for i in range(0, len(r))]

        [v_mod.append(trans(v_x[k], v_y[k])[0]) for k in range(last_size, len(t))]
#        [fi_in_v.append(trans(v_x[k], v_y[k])[1]) for k in range(last_size, len(t))]
        # v_mod, fi_in_v = [trans(v_x[i], v_y[i])[0] for i in range(0, len(v))], \
        #                  [trans(v_x[i], v_y[i])[1] for i in range(0, len(v))]

        [E_full.append((v_mod[k]) ** 2 * m / 2 + U_(r_norm[k])) for k in range(last_size, len(t))]
        # E_full = [(v_mod[i]) ** 2 * m / 2 + U_(r_norm[i]) for i in range(0, len(r_norm))]

        [v_fi.append( v_mod[k] * np.sqrt(abs(1 - (np.dot(v[k], r[k]) / np.linalg.norm(v[k]) / np.linalg.norm(r[k])) ** 2)) ) for
         k in range(last_size, len(t))]
        # v_fi = [v_mod[i] * np.sqrt(abs(1 - (np.dot(v[i], r[i]) / np.linalg.norm(v[i]) / np.linalg.norm(r[i])) ** 2)) for
        #         i in range(0, len(v_mod))]

        [x_eff.append(np.linalg.norm(r[k])) for k in range(last_size, len(t))]
        [U_eff.append(U_(x_eff[k]) + v_fi[k] ** 2 * m / 2) for k in range(last_size, len(t))]
        # x_eff = [(np.linalg.norm(r[i])) for i in range(0, len(v_fi))]
        # U_eff = [U_(x_eff[i]) + v_fi[i] ** 2 * m / 2 for i in range(0, len(v_fi))]

        # delete from it-------
        # if i == 93500:
        #     # считаем старые модули нужных векторов
        #     v_rad = np.sqrt(v_mod[-1] ** 2 - v_fi[-1] ** 2)  # чтобы посчитать вектор фи старый
        #     # теперь в векторах
        #     r_vector = r[-1] / r_norm[-1]
        #     v_rad_vec = v_rad * r_vector
        #     # можнно также изменить высчитанную радиальную составляющую скорости
        #     v_fi_vec = v_fi[-1] * (v[-1] - v_rad_vec)  # еще неизмененный вектор
        #     v_fi_vector = v_fi_vec / np.linalg.norm(v_fi_vec)
        #
        #     # изменяем вектора:
        #     v_fi[-1] += 100  # - и с такого изменения пересчитать х и у компоненты скорости и переприсвоить их
        #     # v_rad += ...
        #
        #
        #     print(v_fi[-1])  # ~3155 #+ 100
        # to it----------------
        last_size = len(t)  # enw of while
        #print(len(v_x), len(v_y), len(t))

    line_xy.set_xdata(r_x)
    line_xy.set_ydata(r_y)

    line_tv.set_xdata(t)
    line_tv.set_ydata(v_x)

    line_tr.set_xdata(t)
    line_tr.set_ydata(r_x)

    line_rE.set_xdata(r_norm)
    line_rE.set_ydata(E_full)

    line_Uef.set_xdata(x_eff)
    line_Uef.set_ydata(U_eff)

    fg.canvas.draw_idle()

# init
set_params(choose_field)  # true - Earth, false - oscillator
func_ = Force

t = [0.0]
r = [r0]
v = [vr_0]

koef_tmp = 2
total_time_tmp = koef_tmp * step_t
for i in range(0, total_time, int(step_t)):
    tmp_t, tmp_r, tmp_v = calc.eqSolut(func_, m, r[-1], v[-1], i, total_time_tmp, step_t)
    [t.append(tmp_t[k]) for k in range(1, len(tmp_t))]
    [r.append(tmp_r[k]) for k in range(1, len(tmp_r))]
    [v.append(tmp_v[k]) for k in range(1, len(tmp_v))]

#t, r, v = calc.eqSolut(func_, m, r0, vr_0, 0, total_time, step_t)

r_x = [r[i][0] for i in range(0, len(r))]
r_y = [r[i][1] for i in range(0, len(r))]
v_x = [v[i][0] for i in range(0, len(v))]
v_y = [v[i][1] for i in range(0, len(v))]

fg = plt.figure(figsize=(12, 7))
plt.subplot(221)
line_tr, = plt.plot(t, r_x, label='r')
plt.title('Coordinate_x')
plt.xlabel('t')
plt.ylabel('r')
plt.grid()

plt.subplot(222)
line_tv, = plt.plot(t, v_x, label='v')
plt.title('Speed_ x')
plt.xlabel('t')
plt.ylabel('v')
plt.grid()

plt.subplot(223)
if choose_field:
    circle1 = plt.Circle((0, 0), R, color='r', fill=True)
    ax = plt.gca()
    ax.add_patch(circle1)
line_xy, = plt.plot(r_x, r_y, label='Y(x)')
plt.title('y(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()


r_norm = [np.linalg.norm(r[i]) for i in range(0, len(r))]
v_mod, fi_in_v = [trans(v_x[i], v_y[i])[0] for i in range(0, len(v))], \
                 [trans(v_x[i], v_y[i])[1] for i in range(0, len(v))]
E_full = [(v_mod[i]) ** 2 * m / 2 + U_(r_norm[i]) for i in range(0, len(r_norm))]

#v_fi = [v_mod[i] / np.tan(fi_in_v[i]) for i in range(0, len(v_mod))]
v_fi = [v_mod[i] * np.sqrt(abs(1 - (np.dot(v[i], r[i]) / np.linalg.norm(v[i]) / np.linalg.norm(r[i]))**2)) for i in range(0, len(v_mod))]


x_eff = [(np.linalg.norm(r[i])) for i in range(0, len(v_fi))]
U_eff = [U_(x_eff[i]) + v_fi[i]**2 * m / 2 for i in range(0, len(v_fi))]

plt.subplot(224)
line_Uef, = plt.plot(x_eff, U_eff, label='U')
line_rE, = plt.plot(r_norm, E_full, 'r-.', label='particle Energy')
plt.title('Energy')
plt.xlabel('r')
plt.ylabel('E')
plt.grid()

ax_total_time = plt.axes([0.1, 0.025, 0.8, 0.0125])
total_time_slider = Slider(
    ax=ax_total_time,
    label="t",
    valmin=0,
    valmax=2 * total_time,
    valinit=total_time,
    valstep=1
)
total_time_slider.on_changed(update)

plt.show()
