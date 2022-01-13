import math
import numpy as np
import Calculator as calc
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
# how to Draw 2D U_?

# constants:
m = 1000  # 1.67e-27
R = 6371000.0  # Earth radius
G = 6.673e-11  # C
M = 5.9742e24  # C

step_t = 100
total_time = 512700  # граничное время, при котором
# graph range - задается в set_params
# min_border = -4
# max_border = 4
# koef = 0  # для отображения графика

# r0 = 200000
# vr_0 = 2
global r0  # = np.array([0, 0])
global vr_0  # = np.array([0, 0])


# def potent_oscillator(x):
#     w = 3
#     return m * w**2 * x ** 2 / 2
#
#
# def gravitational_planet_potential(x):
#     if x < R:
#         return 5e-20
#     return -m * M * G / x
#
#
# def force_oscillator(x):
#     w = 3
#     return -m * w**2 * x
#
#
# def gravitational_planet_force(x):
#     return -m * M * G / x**2
#
#
# def gravitational_planet_potential_2D(radius):  # radius = sqrt(x**2 + y**2)
#     # if abs(x - R) < 10:
#     #     return -m * M * G / (R + 10)
#     # if abs(y - R) < 10:
#     #     return -m * M * G / (R + 10)
#     # if x < R:
#     #     return 5e-20
#     # if y < R:
#     #     return 5e-20
#     if radius < R:
#         return 5e-20
#     return -m * M * G / radius


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

def gravitational_planet_force_2D(r_vec):
    A = -m * M * G
    if r_vec[0]**2 + r_vec[1]**2 <= R**2:
        return np.array([0, 0])  # до радиуса Земли разгоняемся, потом - нет
    # надо попробовать указать здесь числа зза вычетом радиуса
    # внизу просто формула (А / |r|**2) * (r / |r|), преобразованная
    # (поделил каждую компоненту на х и у соответственно), чтобы знаменатели
    # были не такими большими и не выдавали nan

    arr_r, arr_hi = trans(r_vec[0], r_vec[1])
    # print(arr_r)
    # print(arr_hi)
    return np.array([A * np.cos(arr_hi) / arr_r**2,
                     A * np.sin(arr_hi) / arr_r**2])
    # scale = 10
    # if r_vec[0] > scale and r_vec[1] > scale:
    #     return np.array([A / ((r_vec[0])**(4.0/3) + (r_vec[1] / (r_vec[0])**(1.0/3))**2)**(3.0/2),
    #                      A / ((r_vec[0] / (r_vec[1])**(1.0/3))**2 + (r_vec[1])**(4.0/3))**(3.0/2)])
    # elif r_vec[0] <= scale < r_vec[1]:
    #     return np.array([A * r_vec[0] / r_vec[1] ** 1.5,
    #                      A / ((r_vec[0] / (r_vec[1])**(1.0/3))**2 + (r_vec[1])**(4.0/3))**(3.0/2)])
    # elif r_vec[1] <= scale < r_vec[0]:
    #     return np.array([A / ((r_vec[0])**(4.0/3) + (r_vec[1] / (r_vec[0])**(1.0/3))**2)**(3.0/2),
    #                      A * r_vec[1] / r_vec[0] ** 1.5])
    # else:
    #     return np.array([A * r_vec[0] / r_vec[1] ** 1.5,
    #                      A * r_vec[1] / r_vec[0] ** 1.5])
    # return np.array([A * r_vec[0] / ((r_vec[0])**2 + (r_vec[1])**2)**(3.0/2),
    #                  A * r_vec[1] / ((r_vec[0])**2 + (r_vec[1])**2)**(3.0/2)])


#global U_
global Force


def set_params(mode=True):
    # global min_border
    # global max_border
    # global koef
    global r0
    global vr_0
    global U_
    global Force

    if mode:  # здесь настраиваются начальные параметры для 2д случая
        vr_0 = np.array([-4000.0, 0.0])  # начальная скорость - из положительной области х движемся влево
        # такое число, потому что иначе будет тупо перпендикулярное падение на Землю
        # при попытке увеличить время, выдает ошибку, что сильно большие числа. Мб скорость становится слишком уж большой
        # скорее всего, где-то неправильно считается сила
        # min_border = 1
        # max_border = R * 100
        # koef = 1
        r0 = np.array([R + 2 * R, R + 3 * R])
        # U_ = gravitational_planet_potential
        Force = gravitational_planet_force_2D
    else:
        vr_0 = np.array([-2, 0])
        # min_border = -4
        # max_border = 4
        # koef = 10
        r0 = -2
        # U_ = potent_oscillator
        # Force = force_oscillator


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

#print(gravitational_planet_force_2D(r0))

t, r, v = calc.eqSolut(func_[0], m, r0, vr_0, total_time, step_t, func_[1])


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
circle1 = plt.Circle((0, 0), R, color='r', fill=True)
line_xy, = plt.plot(r_x, r_y, label='Y(x)')
ax=plt.gca()
ax.add_patch(circle1)
#plt.axis('scaled')
plt.title('y(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()

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
    valmax=10 * total_time,
    valinit=total_time,
    valstep=1
)
total_time_slider.on_changed(update)

plt.show()
