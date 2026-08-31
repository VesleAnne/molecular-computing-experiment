# Molecular Computing Experiments: CRNs, ODEs, and Molecular Thresholds

This document records the first experiments in a molecular-computing project.

The goal is to build intuition for chemical reaction networks (CRNs), understand how molecular computation differs from ordinary digital computation, and later connect these abstract models to DNA strand-displacement systems.

All experiments are **purely computational simulations**. No actual DNA chemistry is being performed.

---

## 1. Environment

The experiments are written in Python and use libraries:

- `NumPy` 
- `SciPy`
- `Matplotlib`

The main ODE solver is:

`solve_ivp` 

It solves an **initial value problem**: given the initial concentrations of all molecular species and equations describing how those concentrations change, it computes the system state over time.

---

# Experiment 1: An Abstract Molecular AND Gate

## Goal

The first experiment explores whether the abstract chemical reaction

$$
X_1 + X_2 \rightarrow Y
$$

can behave similarly to a Boolean `AND` operation.

In conventional programming:

```python
X1 and X2
```

has the truth table:

| X1 | X2 | Output |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 1 | 1 |

We interpret molecular inputs as concentrations:

- `X1 = 0` means species `X1` is absent.
- `X1 = 1` means species `X1` is present at one normalized concentration unit.
- The same interpretation is used for `X2`.

The output is the concentration of molecular species `Y`.

---

## Reaction Kinetics

The reaction is modeled using mass-action kinetics:

$$
r = k[X_1][X_2]
$$

where:

- $[X_1]$ is the concentration of species `X1`
- $[X_2]$ is the concentration of species `X2`
- $k$ is the reaction-rate constant
- $r$ is the instantaneous reaction rate

For the initial experiments:

$$
k = 1
$$

This value is not based on a real DNA reaction. It is a convenient normalized value used to study the qualitative behavior of the system.

The corresponding system of differential equations is:

$$
\frac{d[X_1]}{dt} = -k[X_1][X_2]
$$

$$
\frac{d[X_2]}{dt} = -k[X_1][X_2]
$$

$$
\frac{d[Y]}{dt} = k[X_1][X_2]
$$

`X1` and `X2` are consumed while `Y` is produced.

---

## Initial Conditions

We simulated all four Boolean input combinations:

```text
X1=0, X2=0
X1=1, X2=0
X1=0, X2=1
X1=1, X2=1
```

For every experiment:

$[Y]$ $(0)$ = $0$


## Result

For the first three input combinations, the reaction rate is zero because at least one factor in

$$
k[X_1][X_2]
$$

is zero.

Therefore:

$[Y]$ $(0)$ = $0$

for the entire simulation.

Only when:

```text
X1=1
X2=1
```

does the output concentration increase.

For these initial conditions and $k=1$, the analytical solution is:

$[Y]$ $(t)$ = $\frac{t}{1+t}$

so, for example:

```text
t = 0   → Y = 0
t = 1   → Y = 0.5
t = 4   → Y = 0.8
t = 10  → Y ≈ 0.91
```

---

## Observation

Unlike a digital Boolean gate, the molecular output is not produced instantaneously.

The output is a trajectory:

$[Y]$ $(t)$

rather than an immediate Boolean value.

This introduces concepts that do not normally appear in simple digital logic:

- reaction latency
- readout time
- reaction rate
- concentration thresholds
- transient behavior

---

# Experiment 2: Continuous Input Concentrations

## Goal

The first experiment artificially restricted molecular inputs to exactly `0` and `1`.

Real chemistry is continuous, so the next experiment fixed:

$[X_1]$ $(0)$ = $1$

and tested several initial concentrations of `X2`:

```text
X2 = 0.0
X2 = 0.1
X2 = 0.3
X2 = 0.5
X2 = 1.0
```

---

## Result

Because the reaction has 1:1 stoichiometry,

$$
X_1 + X_2 \rightarrow Y
$$

the smaller amount of the two reactants limits the total amount of output.

Since $[X_1]$ $(0)=1$, `X2` is the limiting reagent for all values below 1.

Therefore, approximately:

```text
X2=0.0 → Y → 0.0
X2=0.1 → Y → 0.1
X2=0.3 → Y → 0.3
X2=0.5 → Y → 0.5
X2=1.0 → Y → 1.0
```

The values are approached gradually rather than instantaneously.

---

## External Threshold

We initially introduced a logical threshold:

$$
[Y] > 0.7 \Rightarrow \mathrm{TRUE}
$$

and

$$
[Y] \leq 0.7 \Rightarrow \mathrm{FALSE}
$$

This demonstrated how continuous chemical concentrations could be interpreted as Boolean values.

However, this threshold was not part of the molecular system itself. It existed only as an external rule used by the observer.
