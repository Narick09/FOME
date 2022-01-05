import Calculator as calc
import matplotlib.pyplot as plt

def potent_E(x):
    if -2 <= x and x <= 2:
        return x ** 2 / 2
    return 0

if __name__ == '__main__':
    x0 = -20
    v0 = 2
    total_time = 10
    N = 1000000
    m = 1.6e-9

    step_t = total_time / N

    t, x, v = calc.eqSolut(potent_E, m, x0, v0, total_time, step_t)

    fg = plt.figure(figsize=(12, 7))
    plt.subplot(121)
    plt.plot(t, x, label='x')
    plt.title('functions')
    plt.xlabel('t')
    plt.ylabel('x')
    plt.grid()
    plt.legend()

    plt.subplot(122)
    #t += 0.5
    plt.plot(t, v, label='v')
    plt.title('functions')
    plt.xlabel('t')
    plt.ylabel('v')
    plt.grid()
    plt.legend()
    plt.show()