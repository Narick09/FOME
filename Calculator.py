from math import *
import numpy as np

def eqSolut(F, m, xCoordinate_0, speed_0, total_time, step_t):
    x = [xCoordinate_0]#x0
    v = []
    t = [0.0]

    #dx = 1e-10  # сколько тут надо взять???

    #a0 = -1.0 * (U(xCoordinate_0 + dx) - U(xCoordinate_0)) / dx / m #заменить потенциал на силу
    a0 = F(xCoordinate_0) / m  # заменить потенциал на силу
    v_12 = speed_0 + a0 * step_t / 2 #v_12
    v.append(v_12)
    # E = m * speed_0 ** 2 / 2 + U(xCoordinate_0)
    # if speed_0 == 0:
    #
    #     tmp_x = xCoordinate_0 - dx
    #     tmp_E = E - U(tmp_x)
    #     if tmp_E > 0:
    #         x.append(tmp_x)#x1
    #         v.append(sqrt(2 * tmp_E / m))#v_1/2
    #     else:
    #         tmp_x = xCoordinate_0 + dx
    #         tmp_E = E - U(tmp_x)
    #         x.append(tmp_x + 2 * dx)#x1
    #         v.append(sqrt(2 * tmp_E / m))#v_1/2
    # else:
    #     x.append(x[-1] + speed_0 * step_t)#x1
    #     a0 = -1.0 * (U(x[-1]) - U(x[0])) / (x[-1] - x[0]) / m #заменить потенциал на силу
    #     v.append(speed_0 + a0 * step_t / 2)#sqrt(2 * tmp_E / m))#v_1/2
    # t.append(0.0 + step_t)

    N = int(total_time / step_t)

    for i in range (1, N):
        x_pr = x[-1]
        a0 = F(x[-1]) / m
        #a0 = -1.0 * (U(x[-1] + dx) - U(x[-1])) / dx / m #-1.0 * (U(x[-1]) - U(x_pr)) / (x[-1] - x_pr) / m
        v.append(v[-1] + a0 * step_t)#v_(n+1/2)
        t.append(i * step_t)
        #print(x_pr)
        x.append(x_pr + v[-1] * step_t)
#    v.append(v[-1])
    print(t[-1])
    return t, x, v
