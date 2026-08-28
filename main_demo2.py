import numpy as np
from qiskit.circuit.library import QAOAAnsatz
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize
from max_cut import create_graph, get_cost_hamiltonian

G = create_graph(num_nodes=8)
hamiltonian = get_cost_hamiltonian(G)
estimator = StatevectorEstimator()

def objective_function(params, p_depth):
    ansatz = QAOAAnsatz(cost_operator=hamiltonian, reps=p_depth)
    pub = (ansatz, [hamiltonian], [params])
    result = estimator.run([pub]).result()
    return result[0].data.evs[0]

if __name__ == "__main__":
    print("--- Phase 2: QAOA Optimization with COBYLA ---")
    
    for p in [1, 2, 3]:
        # Number of parameters based on circuit depth (2*p)
        num_params = 2 * p
        np.random.seed(10)
        initial_params = np.random.uniform(-np.pi, np.pi, num_params)

        print(f"\nOptimizing for depth p={p}...")
        res = minimize(objective_function, initial_params, args=(p), method='COBYLA', options={'maxiter': 200})
        
        print(f"Optimization Finished for p={p}:")
        print(f"Optimal Parameters: {res.x}")
        print(f"Best Expectation Value (Energy): {res.fun:.4f}")