from math import *
import numpy as np

def eqSolut(U, m, xCoordinate_0, speed_0, total_time, step_t):
    x = [xCoordinate_0]#x0

    v = []
    t = [0.0]
#мб косяк - случай, когда тупо потенциал константа или когда просто в положении равновесия находится - надо отдельно обработать
    E = m * speed_0 ** 2 / 2 + U(xCoordinate_0)
    if speed_0 == 0:
        #если нет начальной скорости, нужно посмотреть, что будет через какой-то малый промежуток dx:
        dx = 1e-10#сколько тут надо взять???
        tmp_x = xCoordinate_0 - dx
        tmp_E = E - U(tmp_x)
        if tmp_E > 0:
            x.append(tmp_x)#x1
            v.append(sqrt(2 * tmp_E / m))#v_1/2
        else:
            tmp_x = xCoordinate_0 + dx
            tmp_E = E - U(tmp_x)#не рассмотрел еще случай, когда попадем ровно в экстремум - что тогда?
            x.append(tmp_x + 2 * dx)#x1
            v.append(sqrt(2 * tmp_E / m))#v_1/2
    else:
        x.append(x[-1] + speed_0 * step_t)#x1
        tmp_E = E - U(x[-1])
        v.append(sqrt(2 * tmp_E / m))#v_1/2
    t.append(0.0 + step_t)

    N = int(total_time / step_t)

    for i in range (2, N):
        x_pr = x[-1]
        #print(x_pr)
        x.append(x_pr + v[-1] * step_t)
        a0 = -1.0 * (U(x[-1]) - U(x_pr)) / (x[-1] - x_pr) / m
        v.append(v[-1] + a0 * step_t)#v_(n+1/2)
        t.append(i * step_t)
    v.append(v[-1])  # v_(n+1/2) - kostyl
    print(t[-1])
    return t, x, v

