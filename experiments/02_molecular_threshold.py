import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt



k_production = 1.0

k_threshold = 10.0


threshold_initial = 0.7


def reaction(t, concentrations):
    x1, x2, y, threshold, waste = concentrations
    # X1 + X2 -> Y

    production_rate = k_production * x1 * x2
    # Y + T -> Waste

    threshold_rate = k_threshold * y * threshold

    dx1_dt = -production_rate
    dx2_dt = -production_rate
    dy_dt = production_rate - threshold_rate

    dthreshold_dt = -threshold_rate
    dwaste_dt = threshold_rate

    return [
        dx1_dt,
        dx2_dt,
        dy_dt,
        dthreshold_dt,
        dwaste_dt,
    ]


def simulate(x1_initial, x2_initial):

    # X1 =  input
    # X2 =  input
    # Y = 0
    # Threshold = 0.7
    # Waste = 0
    initial_state = [
        x1_initial,
        x2_initial,
        0.0,
        threshold_initial,
        0.0,
    ]

    result = solve_ivp(
        reaction,
        t_span=(0, 100),
        y0=initial_state,
        t_eval=np.linspace(0, 100, 1000),
    )

    return result


experiments = [
    (1, 0.0),
    (1, 0.1),
    (1, 0.3),
    (1, 0.5),
    (1, 0.7),
    (1, 0.8),
    (1, 1.0),
]


for x1, x2 in experiments:
    result = simulate(x1, x2)

    time = result.t

    # result.y[2] 
    y = result.y[2]

    plt.plot(
        time,
        y,
        label=f"X2={x2}",
    )


plt.xlabel("Time")
plt.ylabel("Free Y concentration")
plt.title("Molecular threshold: Y + T → Waste")
plt.legend()
plt.show()