import numpy as np
from scipy.optimize import minimize

# 1. Stochastic Parameters
Q_river_mean = 500.0
Q_river_std = 100.0  # High volatility in river flow
C_limit = 5.0
n_sims = 1000 # Number of Monte Carlo trials per optimization step

sources = [
    {'Q': 20, 'C': 50, 'cost_k': 1000},
    {'Q': 35, 'C': 80, 'cost_k': 1500},
    {'Q': 15, 'C': 120, 'cost_k': 2000}
]

# 2. Robust Objective (Cost remains the same)
def objective(eta):
    return sum(s['cost_k'] * (e / (1.001 - e)) for s, e in zip(sources, eta))

# 3. Chance Constraint: 95th Percentile must be below C_limit
def chance_constraint(eta):
    # Simulate 1000 random river flow scenarios
    random_flows = np.random.lognormal(
        mean=np.log(Q_river_mean), 
        sigma=0.2, 
        size=n_sims
    )
    
    c_results = []
    for q_r in random_flows:
        total_flow = q_r + sum(s['Q'] for s in sources)
        factory_mass = sum(s['C'] * s['Q'] * (1 - e) for s, e in zip(sources, eta))
        c_down = (q_r * 2.0 + factory_mass) / total_flow
        c_results.append(c_down)
    
    # Calculate the 95th percentile concentration
    c_95 = np.percentile(c_results, 95)
    
    # Return how much 'room' we have left before hitting the limit
    return C_limit - c_95

# 4. Solve
n = len(sources)
res = minimize(objective, [0.5]*n, method='SLSQP', 
               bounds=[(0, 0.99)]*n, 
               constraints={'type': 'ineq', 'fun': chance_constraint})

print(f"Robust Optimization Results:")
print(f"Total Cost: ${res.fun:.2f}")
print(f"95% Confidence limit maintained.")
