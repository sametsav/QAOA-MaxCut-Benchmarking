import numpy as np
from qiskit.circuit.library import QAOAAnsatz
from qiskit.primitives import StatevectorEstimator
from max_cut import create_graph, get_cost_hamiltonian

G = create_graph(num_nodes=6)
hamiltonian = get_cost_hamiltonian(G)
estimator = StatevectorEstimator()

def objective_function(params, p_depth):
    ansatz = QAOAAnsatz(cost_operator=hamiltonian, reps=p_depth)
    pub = (ansatz, [hamiltonian], [params])
    result = estimator.run([pub]).result()
    return result[0].data.evs[0]