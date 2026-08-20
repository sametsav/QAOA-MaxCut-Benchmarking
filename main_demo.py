import numpy as np
from qiskit.circuit.library import QAOAAnsatz
from qiskit.primitives import StatevectorEstimator
from max_cut import create_graph, get_cost_hamiltonian

def run_phase1_simulation(p_depth):
    G = create_graph(num_nodes=6)
    hamiltonian = get_cost_hamiltonian(G)
    
    ansatz = QAOAAnsatz(cost_operator=hamiltonian, reps=p_depth)
    
    # Generate random parameters just to test the circuit (no optimization yet)
    np.random.seed(42)
    test_params = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)
    
    estimator = StatevectorEstimator()
    
    # Pub format: (circuit, observable, parameter_values)
    pub = (ansatz, [hamiltonian], [test_params])
    result = estimator.run([pub]).result()
    
    expectation_value = result[0].data.evs[0]
    
    return test_params, expectation_value

if __name__ == "__main__":
    print("--- Phase 1: Exact Statevector Simulation (No Optimization) ---")
    
    for p in [1, 2]:
        params, ev = run_phase1_simulation(p)
        print(f"\nDepth p={p}:")
        print(f"Test Parameters: {params}")
        print(f"Expectation Value: {ev:.4f}")