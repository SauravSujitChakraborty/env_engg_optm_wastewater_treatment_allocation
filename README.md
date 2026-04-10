# env_engg_optm_wastewater_treatment_allocation

NOTE : This project was made by me during Jun'25, subsequently preserved and published on Apr10'26.

Stochastic Optimization of Wastewater Treatment Allocation
​
Project Overview

​In environmental engineering, deterministic models often fail because they do not account for natural volatility. This project implements Stochastic Nonlinear Programming to minimize industrial treatment costs while ensuring river water quality meets legal standards with a 95% confidence level, even under fluctuating flow conditions.

​Mathematical Theory

​1. The Stochastic Variable: River Flow $ (Q_{up}) $

​Unlike standard models that use a fixed flow rate, this project treats upstream river discharge as a random variable. We use a Log-Normal Distribution because physical flows cannot be negative and often exhibit "fat-tail" behavior during floods or droughts:


$ \ln(Q_{up}) \sim \mathcal{N}(\mu, \sigma^2) $

2. The Mass Balance Equation
The downstream concentration (C_{down}) is calculated using a mass-balance summation. This accounts for the upstream pollutant load and the treated discharge from n industrial sources:


$$ C_{down} = \frac{(Q_{up} \cdot C_{up}) + \sum_{i=1}^{n} [Q_i \cdot C_i \cdot (1 - \eta_i)]}{Q_{up} + \sum_{i=1}^{n} Q_i} $$

where,

$ \eta_i $: Treatment efficiency of factory i (the decision variable).
$ Q_i, C_i $: Constant discharge flow and concentration from factory i.


3. The Objective Function (Cost Minimization)

We assume that removal costs grow exponentially as efficiency (\eta) approaches 100%. The total economic burden Z is defined as:


$$ Z = \sum_{i=1}^{n} k_i \cdot \left( \frac{\eta_i}{1.001 - \eta_i} \right) $$

4. Chance-Constrained Optimization
   
This is the "Quant" core of the project. Instead of a simple constraint, we use a Chance Constraint. We require that the probability of violating the legal limit (C_{limit}) is less than 5%:

P(C_{down} > C_{limit}) \leq 0.05

To solve this, the algorithm performs a Monte Carlo Simulation of 1,000 scenarios at every iteration of the solver to find the 95th percentile of $ C_{down} $.

Implementation Details

Algorithm: Sequential Least Squares Programming (SLSQP).

Simulation: Monte Carlo Method for risk-adjusted constraint satisfaction.

Optimization Framework: scipy.optimize.minimize.

Key Results


Robustness: The model successfully found a treatment strategy that remains valid even during low-flow (drought) scenarios.

Efficiency: By distributing the load based on $ k_i $(cost coefficients), the solver achieved a significant reduction in total expenditure compared to a "uniform treatment" mandate
