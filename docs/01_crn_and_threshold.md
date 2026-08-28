# Molecular Computing Experiments

This document records the first experiments in a small molecular-computing project. The goal is to build intuition for chemical reaction networks (CRNs), understand how molecular computation differs from ordinary digital computation, and later connect these abstract models to DNA strand-displacement systems.

At this stage, all experiments are **purely computational simulations**. No actual DNA chemistry is being performed yet.

## 1. Environment

The experiments are written in Python and currently use:



Main libraries:

* `NumPy` — numerical utilities and time grids
* `SciPy` — numerical integration of differential equations
* `Matplotlib` — visualization

The main ODE solver is:


`solve_ivp` solves an **initial value problem**: given the initial concentrations of all molecular species and equations describing how those concentrations change, it computes the system state over time.

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
| -- | -- | ------ |
| 0  | 0  | 0      |
| 1  | 0  | 0      |
| 0  | 1  | 0      |
| 1  | 1  | 1      |

We interpret molecular inputs as concentrations:

* `X1 = 0` means species `X1` is absent.
* `X1 = 1` means species `X1` is present at one normalized concentration unit.
* The same interpretation is used for `X2`.

The output is the concentration of molecular species `Y`.

## Reaction kinetics

The reaction is modeled using mass-action kinetics:

$$
r = k X_1 X_2
$$

where:

* \(X_1\) is the concentration of species `X1`
* \(X_2\) is the concentration of species `X2`
* \(k\) is the reaction-rate constant
* \(r\) is the instantaneous reaction rate

For the initial experiments:

$$
k=1
$$

This value is not based on a real DNA reaction. It is a convenient normalized value used to study the qualitative behavior of the system.

The corresponding system of differential equations is:

$$
\frac{dX_1}{dt}=-kX_1X_2
$$

$$
\frac{dX_2}{dt}=-kX_1X_2
$$

$$
\frac{dY}{dt}=kX_1X_2
$$

`X1` and `X2` are consumed while `Y` is produced.

## Initial conditions

We simulated all four Boolean input combinations:

```text
X1=0, X2=0
X1=1, X2=0
X1=0, X2=1
X1=1, X2=1
```

For every experiment:

```text
Y(0) = 0
```

## Result

For the first three input combinations, the reaction rate is zero because at least one factor in

$$
kX_1X_2
$$

is zero.

Therefore:

$$
Y(t)=0
$$

for the entire simulation.

Only when:

```text
X1=1
X2=1
```

does the output concentration increase.

For these initial conditions and \(k=1\), the analytical solution is:

$$
Y(t)=\frac{t}{1+t}
$$

so, for example:

```text
t = 0   → Y = 0
t = 1   → Y = 0.5
t = 4   → Y = 0.8
t = 10  → Y ≈ 0.91
```

## Observation

Unlike a digital Boolean gate, the molecular output is not produced instantaneously.

The output is a trajectory:

$$
Y(t)
$$

rather than an immediate Boolean value.

This introduces concepts that do not normally appear in simple digital logic:

* reaction latency
* readout time
* reaction rate
* concentration thresholds
* transient behavior

---

# Experiment 2: Continuous Input Concentrations

## Goal

The first experiment artificially restricted molecular inputs to exactly `0` and `1`.

Real chemistry is continuous, so the next experiment fixed:

$$
X_1=1
$$

and tested several initial concentrations of `X2`:

```text
X2 = 0.0
X2 = 0.1
X2 = 0.3
X2 = 0.5
X2 = 1.0
```

## Result

Because the reaction has 1:1 stoichiometry,

$$
X_1+X_2\rightarrow Y,
$$

the smaller amount of the two reactants limits the total amount of output.

Since \(X_1=1\), `X2` is the limiting reagent for all values below 1.

Therefore, approximately:

```text
X2=0.0 → Y → 0.0
X2=0.1 → Y → 0.1
X2=0.3 → Y → 0.3
X2=0.5 → Y → 0.5
X2=1.0 → Y → 1.0
```

The values are approached gradually rather than instantaneously.

## External threshold

We initially introduced a logical threshold:

$$
Y > 0.7 \Rightarrow TRUE
$$

and

$$
Y \leq 0.7 \Rightarrow FALSE.
$$

This demonstrated how continuous chemical concentrations could be interpreted as Boolean values.

However, this threshold was not part of the molecular system itself. It existed only as an external rule used by the observer.

Conceptually, the system was still:

```text
chemistry
    ↓
Y concentration
    ↓
external Python/human threshold
    ↓
TRUE / FALSE
```

This motivated the next experiment.

---

# Experiment 3: A Molecular Threshold

## Goal

Instead of applying a threshold externally, we introduced another molecular species:

```text
T = Threshold
```

and a second reaction:

$$
Y + T \rightarrow Waste.
$$

The idea is that `T` acts as a molecular sink that consumes the first portion of the produced `Y`.

The initial threshold concentration was:

$$
T(0)=0.7.
$$

The complete abstract reaction network became:

$$
X_1 + X_2 \rightarrow Y
$$

$$
Y + T \rightarrow Waste.
$$

## Rate equations

Two rates are now calculated:

$$
r_\text{production}
=
k_\text{production}X_1X_2
$$

and

$$
r_\text{threshold}
=
k_\text{threshold}YT.
$$

The corresponding ODEs are:

$$
\frac{dX_1}{dt}
=
-r_\text{production}
$$

$$
\frac{dX_2}{dt}
=
-r_\text{production}
$$

$$
\frac{dY}{dt}
=
r_\text{production}
-
r_\text{threshold}
$$

$$
\frac{dT}{dt}
=
-r_\text{threshold}
$$

$$
\frac{dWaste}{dt}
=
r_\text{threshold}.
$$

For the first threshold experiment:

```text
k_production = 1
k_threshold = 10
T(0) = 0.7
```

Again, these rate constants are normalized educational values rather than experimentally measured DNA parameters.

## Interpretation

Suppose the system produces:

```text
Y = 0.5
```

while:

```text
T = 0.7
```

The threshold molecules can consume all of the output:

```text
0.5 Y + 0.5 T → Waste
```

leaving approximately:

```text
free Y = 0
T = 0.2
```

If instead the system produces:

```text
Y = 1.0
```

the threshold can consume only approximately `0.7`.

The remaining free output is therefore approximately:

$$
1.0-0.7=0.3.
$$

For \(X_1=1\), the long-term output approximately follows:

$$
Y_\text{out}
\approx
\max(0,X_2-0.7).
$$

This resembles a shifted ReLU activation:

$$
\operatorname{ReLU}(x-b)
=
\max(0,x-b).
$$

In this interpretation:

```text
x = molecular input
b = threshold concentration
output = free molecular concentration
```

The threshold is no longer merely an external interpretation. It is encoded directly as the concentration of another molecular species.

---

# Experiment 4: Transient Behavior

The threshold experiment revealed an important dynamic effect.

For example, even when:

```text
X2 = 0.5
```

and the final free `Y` concentration should approach zero, the simulation initially shows a small amount of free `Y`.

This happens because at time zero:

$$
Y=0.
$$

Therefore:

$$
r_\text{threshold}
=
k_\text{threshold}YT
=
0.
$$

At the same time, production may already be active:

$$
r_\text{production}
=
k_\text{production}X_1X_2
>
0.
$$

As a result, `Y` must first appear before the threshold reaction can consume it.

This creates a temporary output peak, or **transient response**.

For inputs below the threshold, the behavior can look like:

```text
Y
│
│    /\
│   /  \
│  /    \________
│
└──────────────── time
```

The final output is approximately zero, but intermediate output is not.

## Why this matters

If a molecular computer is read too early, it may produce an incorrect interpretation.

For example, a system whose asymptotic output is:

```text
FALSE
```

may temporarily contain substantial free `Y`.

Therefore, molecular computation depends not only on logical reaction topology but also on:

```text
reaction network
+
rate constants
+
initial concentrations
+
measurement time
```

---

# Experiment 5: Effect of Reaction Rates

## Goal

We tested how the behavior changes while keeping the same reaction network but changing the threshold reaction rate.

The production rate remained:

```text
k_production = 1
```

while the threshold rate was tested at:

```text
k_threshold = 1
k_threshold = 10
k_threshold = 100
```

## Slow threshold: \(k_\text{threshold}=1\)

When the two reactions occur on similar timescales, `Y` can accumulate substantially before `T` consumes it.

This produces large transient peaks.

For some inputs below the intended threshold, free `Y` temporarily becomes quite large even though its final value approaches zero.

This means a premature measurement could produce a false positive.

## Intermediate threshold: \(k_\text{threshold}=10\)

The threshold reaction reacts significantly faster than production.

Transient peaks become smaller, and the output more closely resembles the desired threshold function.

## Fast threshold: \(k_\text{threshold}=100\)

The threshold reaction is much faster than production.

Newly created `Y` is consumed almost immediately while threshold molecules remain available.

The resulting behavior closely approximates:

$$
Y_\text{out}
=
\max(0,X_2-0.7)
$$

for \(X_1=1\).

For example:

```text
X2=0.5 → free Y ≈ 0
X2=0.7 → free Y ≈ 0
X2=0.8 → free Y ≈ 0.1
X2=1.0 → free Y ≈ 0.3
```

The most important observation is that the **logical reaction network is identical in all three cases**.

Only a kinetic parameter changed.

Yet the transient behavior of the molecular computer changed dramatically.

---

# Key Lessons So Far

## 1. Molecular programs can be represented as reaction networks

Instead of writing:

```python
if x1 and x2:
    y = True
```

we can describe a system through reactions such as:

```text
X1 + X2 -> Y
```

The computation emerges from the resulting chemical dynamics.

## 2. Molecular values are naturally continuous

Unlike digital variables, molecular species naturally represent continuous quantities through concentration.

For example:

```text
X2 = 0.37
```

is perfectly meaningful in the model.

This makes molecular computing naturally related to analog computation.

## 3. Computation takes time

The answer is not an instantaneous state.

It is a dynamical trajectory:

$$
Y(t).
$$

The time at which the system is measured can affect the apparent result.

## 4. Thresholds can themselves be molecular

Instead of interpreting a concentration threshold externally, we can introduce another chemical species that physically implements thresholding.

In the current model:

$$
Y+T\rightarrow Waste
$$

implements behavior similar to subtracting a bias followed by ReLU.

## 5. Kinetics are part of the computation

Two systems with identical reaction topology may behave very differently if their reaction rates differ.

Therefore, molecular programming requires reasoning about both:

* what reactions are possible
* how quickly those reactions occur

## 6. The current model is still abstract

The species:

```text
X1
X2
Y
T
Waste
```

are currently symbolic chemical species.

They are **not yet specific DNA strands**.

Likewise:

```text
X1 + X2 -> Y
```

does not yet represent a specific DNA strand-displacement mechanism.

The next level of the project is therefore:

```text
abstract CRN
    ↓
DNA strand-displacement architecture
    ↓
DNA domains and toeholds
    ↓
eventually concrete DNA sequences
```

---

# Current Conceptual Stack

The project currently has the following hierarchy:

```text
High-level computation

    AND / threshold / ReLU-like behavior
                 ↓

Chemical Reaction Network

    X1 + X2 -> Y
    Y + T  -> Waste
                 ↓

ODE model

    dX1/dt
    dX2/dt
    dY/dt
    dT/dt
    dWaste/dt
                 ↓

Numerical simulation

    scipy.integrate.solve_ivp
                 ↓

Observed concentration trajectories

    X1(t), X2(t), Y(t), T(t), Waste(t)
```

The next stage will add another layer below the CRN:

```text
Chemical Reaction Network
        ↓
DNA strand displacement
        ↓
DNA domains / toeholds / complexes
```

The purpose of the next experiments is to understand how an abstract reaction such as

$$
X_1+X_2\rightarrow Y
$$

can be implemented using actual DNA strand-displacement mechanisms rather than treating it as an idealized elementary reaction.
