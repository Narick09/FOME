import math

import Calculator as calc
import matplotlib.pyplot as plt

x0 = -2
v0 = -1
total_time = 10
N = 1000000
m = 1.67e-27
step_t = total_time / N
w = 2
g = 10

def potent_E(x):
    return m * w**2 * x ** 2 / 2

def potent_E2(x):
    return m * g * x

def U_(x):
    return potent_E2(x)

if __name__ == '__main__':

    t, x, v = calc.eqSolut(U_, m, x0, v0, total_time, step_t)

    #t_x = []

    fg = plt.figure(figsize=(12, 7))
    plt.subplot(221)
    plt.plot(t, x, label='x')
    plt.title('functions')
    plt.xlabel('t')
    plt.ylabel('x')
    plt.grid()
    plt.legend()

    plt.subplot(222)
    #t += 0.5
    plt.plot(t, v, label='v')
    plt.title('functions')
    plt.xlabel('t')
    plt.ylabel('v')
    plt.grid()
    plt.legend()

    plt.subplot(223)
    plt.plot(x, v, label='v')
    plt.title('functions')
    plt.xlabel('x')
    plt.ylabel('v')
    plt.grid()
    plt.legend()

    x_arr = [(i * 0.1) for i in range(-40, 40)]
    U_arr = [U_(i * 0.1) for i in range(-40, 40)]

#    E_k_tmp = [((x[i] - x[i-1]) / step_t)**2 * m / 2 + U_(x[i - 1]) for i in range(1, len(x))]
    E_k_tmp = [(v[i]) ** 2 * m / 2 + U_(x[i - 1]) for i in range(1, len(x))]
    E_k_tmp.append(E_k_tmp[-1])

    plt.subplot(224)
    plt.plot(x_arr, U_arr, label='U')
    plt.plot(x, E_k_tmp, 'r-.', label='particle Energy')
    plt.title('Energy')
    plt.xlabel('x')
    plt.ylabel('E')
    plt.grid()
    plt.legend()

    plt.show()


def func1():
    return 0