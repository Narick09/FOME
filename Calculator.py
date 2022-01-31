import numpy as np


def accelerate_through_force(force, xCoordinate_0, dx, m):
    return force(xCoordinate_0) / m


def eqSolut(func, m, xCoordinate_0, speed_0, t_0, total_time, step_t):
    x = [xCoordinate_0]  # x0
#    x_tmp = np.array([xCoordinate_0])
    v = [speed_0]
    t = [t_0]
#    print(type(x))
#    print(type(x_tmp))
    accelerate = accelerate_through_force
    dx = 1e-10

    # a0 = accelerate(func, xCoordinate_0, dx, m)
    # v_12 = speed_0 + a0 * step_t / 2  # v_12
    # v.append(v_12)

    N = int(total_time / step_t)
    #print(N)
    for i in range(1, N):
        x_pr = x[-1]
        a0 = accelerate(func, x[-1], dx, m)
        if np.linalg.norm(a0) == 0:
            break
        v_12 = v[-1] + a0 * step_t / 2
        v.append(v_12 + a0 * step_t / 2)  # v_(n+1/2)
        t.append(t_0 + i * step_t)
        x.append(x_pr + v[-1] * step_t)
    return t, x, v


# def eqSolut(func, m, xCoordinate_0, speed_0, t_0, total_time, step_t):
#     x = [xCoordinate_0]  # x0
#     v = []
#     t = [t_0]
#
#     accelerate = accelerate_through_force
#     dx = 1e-10
#
#     a0 = accelerate(func, xCoordinate_0, dx, m)
#     v_12 = speed_0 + a0 * step_t / 2  # v_12
#     v.append(v_12)
#
#     N = int(total_time / step_t)
#
#     # kostyl begin
#     # a0 = accelerate(func, x[-1], dx, m)
#     # v.append(v[-1] + a0 * step_t)  # v_(1+1/2)
#     # t.append(t_0 + step_t)
#     # x.append(x[-1] + v[-1] * step_t)
#     # kostyl end
#     # for i in range(0, N):
#     for i in range(1, N):
#         x_pr = x[-1]
#         a0 = accelerate(func, x[-1], dx, m)
#         if np.linalg.norm(a0) == 0:
#             break
#         v.append(v[-1] + a0 * step_t)  # v_(n+1/2)
#         t.append(t_0 + i * step_t)
#         x.append(x_pr + v[-1] * step_t)
#     return t, x, v
