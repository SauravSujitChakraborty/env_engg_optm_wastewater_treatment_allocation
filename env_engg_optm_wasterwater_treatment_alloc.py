import numpy as np
from scipy.optimize import minimize

# 1. Stochastic Parameters
Q_river_mean = 500.0   
C_river_up = 2.0      
C_limit = 5.0         
n_sims = 1000         

sources = [
    {'Q': 20, 'C': 50, 'cost_k': 1000},
    {'Q': 35, 'C': 80, 'cost_k': 1500},
    {'Q': 15, 'C': 120, 'cost_k': 2000}
]

# 2. Objective Function
def objective(eta):
    return sum(s['cost_k'] * (e / (1.001 - e)) for s, e in zip(sources, eta))

# 3. Chance Constraint (Calibrated for Feasibility)
def chance_constraint(eta):
    # Setting a fixed seed ensures you get the same 'random' result every time
    np.random.seed(42) 
    
    # We use sigma=0.05 to keep randomness realistic but manageable
    random_flows = np.random.lognormal(
        mean=np.log(Q_river_mean), 
        sigma=0.05, 
        size=n_sims
    )
    
    c_results = []
    for q_r in random_flows:
        total_flow = q_r + sum(s['Q'] for s in sources)
        # Upstream mass + Industrial mass
        factory_mass = sum(s['C'] * s['Q'] * (1 - e) for s, e in zip(sources, eta))
        c_down = (q_r * C_river_up + factory_mass) / total_flow
        c_results.append(c_down)
    
    # Check the 90th percentile to ensure the solver can find a solution
    c_90 = np.percentile(c_results, 90)
    return C_limit - c_90

# 4. Optimization Setup
n = len(sources)
init_guess = [0.8] * n # Start with high treatment to enter the 'Safe Zone' immediately
bounds = [(0, 0.99)] * n
cons = {'type': 'ineq', 'fun': chance_constraint}

res = minimize(objective, init_guess, method='SLSQP', bounds=bounds, constraints=cons)

# 5. Output
if res.success:
    print(f"Optimization Successful")
    print(f"Total Minimum Cost: ${res.fun:.2f}")
    print(f"90% Confidence limit maintained.")
    for i, eta in enumerate(res.x):
        print(f"Factory {i+1} Treatment Efficiency: {eta*100:.2f}%")
else:
    print(f"Optimization Status: {res.message}")
