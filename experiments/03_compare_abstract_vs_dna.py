import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


# MODEL 1: our original abstract CRN
#
# X1 + X2 -> Y

k_abstract = 1.0


def abstract_reaction(t, concentrations):
    x1, x2, y = concentrations

    rate = k_abstract * x1 * x2

    return [
        -rate,   # dX1/dt
        -rate,   # dX2/dt
        +rate,   # dY/dt
    ]


abstract_initial = [
    1.0,  # X1
    1.0,  # X2
    0.0,  # Y
]

abstract_result = solve_ivp(
    abstract_reaction,
    t_span=(0, 10),
    y0=abstract_initial,
    t_eval=np.linspace(0, 10, 500),
)


# MODEL 2: reaction derived by Peppercorn
#
# A + B -> e2
#
# Peppercorn:
# k = 0.006 /nM/s
# A(0) = 10 nM
# B(0) = 10 nM

k_dna = 0.006  # 1 / (nM * s)


def dna_reaction(t, concentrations):
    a, b, e2 = concentrations

    # Since concentrations are in nM and k is /nM/s,
    # the resulting rate is nM/s.
    rate = k_dna * a * b

    return [
        -rate,   # dA/dt
        -rate,   # dB/dt
        +rate,   # de2/dt
    ]


dna_initial = [
    10.0,  # A, nM
    10.0,  # B, nM
    0.0,   # e2, nM
]

dna_result = solve_ivp(
    dna_reaction,
    t_span=(0, 300),
    y0=dna_initial,
    t_eval=np.linspace(0, 300, 500),
)


# PLOT 1
#
# Actual Peppercorn-derived DNA kinetics

plt.figure()

plt.plot(
    dna_result.t,
    dna_result.y[0],
    label="A"
)

plt.plot(
    dna_result.t,
    dna_result.y[1],
    label="B"
)

plt.plot(
    dna_result.t,
    dna_result.y[2],
    label="e2"
)

plt.xlabel("Time (s)")
plt.ylabel("Concentration (nM)")
plt.title("Peppercorn-derived reaction: A + B → e2")
plt.legend()

plt.show()



# PLOT 2
#
# Compare the SHAPE of the abstract and DNA-derived systems.
#
# To do that fairly, we normalize:
#
# concentration:
#
#     output / initial concentration
#
# time:
#
#     tau = k * C0 * t
#
# This removes the arbitrary choice of units.

abstract_y_normalized = abstract_result.y[2] / 1.0
abstract_tau = k_abstract * 1.0 * abstract_result.t

dna_y_normalized = dna_result.y[2] / 10.0
dna_tau = k_dna * 10.0 * dna_result.t


plt.figure()

plt.plot(
    abstract_tau,
    abstract_y_normalized,
    label="Abstract CRN"
)

plt.plot(
    dna_tau,
    dna_y_normalized,
    linestyle="--",
    label="Peppercorn DNA model"
)

plt.xlabel("Normalized time τ = k · C₀ · t")
plt.ylabel("Normalized output concentration")
plt.title("Abstract CRN vs Peppercorn-derived DNA reaction")
plt.legend()

plt.show()