import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Константа скорости реакции.
#
# Мы моделируем реакцию:
#
# X1 + X2 -> Y
#
# и предполагаем, что скорость реакции равна:
#
# rate = k * X1 * X2
#
# Сейчас k=1 выбрано условно, чтобы получить удобную шкалу времени.
k = 1.0

# Определяем функцию, которая описывает "законы физики"
# нашей химической системы.
#
# solve_ivp будет вызывать эту функцию много раз,
# каждый раз спрашивая:
#
# "Вот сейчас время t и вот текущие концентрации.
#  С какой скоростью они сейчас меняются?"

def reaction(t, concentrations):
    x1, x2, y = concentrations
    # Вычисляем скорость химической реакции.
    #
    # Закон действующих масс:
    #
    # X1 + X2 -> Y
    #
    # rate = k * [X1] * [X2]
    #
    # Чем больше X1 и X2, тем чаще они "встречаются",
    # поэтому тем быстрее идет реакция.

    rate = k * x1 * x2

    dx1_dt = -rate
    dx2_dt = -rate
    dy_dt = rate

    return [dx1_dt, dx2_dt, dy_dt]

def simulate(x1_initial, x2_initial):
    # Начальное состояние системы.
    #
    # В момент t=0:
    #
    # X1 = x1_initial
    # X2 = x2_initial
    # Y  = 0
    #
    # Y=0 потому, что продукт реакции
    # в начале эксперимента еще не появился.
    initial_state = [x1_initial, x2_initial, 0.0]

    result = solve_ivp(
        reaction,
        t_span=(0,10),
        y0=initial_state,
        t_eval=np.linspace(0, 10, 200),
    )

    return result.t, result.y[2]

#first experiment

#experiments = [
#    (0, 0),
#    (1, 0),
#    (0, 1),
#    (1, 1),
#]


#for x1, x2 in experiments:
#    t, y = simulate(x1, x2)
#    plt.plot(t, y, label=f"X1={x1}, X2={x2}")

#plt.xlabel("Time")
#plt.ylabel("Y concentration")
#plt.title("Molecular AND: X1 + X2 → Y")
#plt.legend()
#plt.show()

#second

# X1 оставляем максимальным: X1 = 1.
# А концентрацию X2 постепенно увеличиваем.
experiments = [
    (1, 0.0),
    (1, 0.1),
    (1, 0.3),
    (1, 0.5),
    (1, 1.0),
]

for x1, x2 in experiments:
    t, y = simulate(x1, x2)

    plt.plot(
        t,
        y,
        label=f"X2={x2}"
    )


# Допустим, мы решили:
#
# если концентрация Y выше 0.7,
# считаем логический выход TRUE.
threshold = 0.7

plt.axhline(
    y=threshold,
    linestyle="--",
    label="TRUE threshold = 0.7"
)

plt.xlabel("Time")
plt.ylabel("Y concentration")
plt.title("Molecular AND with different X2 concentrations")
plt.legend()
plt.show()
