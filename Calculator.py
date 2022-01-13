from math import *
import numpy as np


def accelerate_through_potential(U, xCoordinate_0, dx, m):  # пока только в одномерье!!!
    return -1.0 * (U(xCoordinate_0 + dx) - U(xCoordinate_0)) / dx / m


def accelerate_through_force(force, xCoordinate_0, dx, m):
    return force(xCoordinate_0) / m


def eqSolut(func, m, xCoordinate_0, speed_0, total_time, step_t, mode=False):
    x = [xCoordinate_0]  # x0
    v = []
    t = [0.0]

    accelerate = accelerate_through_potential
    if mode:
        accelerate = accelerate_through_force

    dx = 1e-10  # сколько тут надо взять???

    a0 = accelerate(func, xCoordinate_0, dx, m)
    v_12 = speed_0 + a0 * step_t / 2  # v_12
    v.append(v_12)

    N = int(total_time / step_t)

    for i in range (1, N):
        x_pr = x[-1]
        a0 = accelerate(func, x[-1], dx, m)
        v.append(v[-1] + a0 * step_t)  # v_(n+1/2)
        t.append(i * step_t)
        x.append(x_pr + v[-1] * step_t)
    # print(t[-1])
    return t, x, v

