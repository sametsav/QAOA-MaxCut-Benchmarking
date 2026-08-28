import numpy as np
from qiskit.circuit.library import QAOAAnsatz
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.providers.fake_provider import GenericBackendV2
from max_cut import create_graph, get_cost_hamiltonian

backend = GenericBackendV2(num_qubits=6)
G = create_graph(num_nodes=6)
hamiltonian = get_cost_hamiltonian(G)
ansatz = QAOAAnsatz(cost_operator=hamiltonian, reps=3)

for opt_level in range(4):
    transpiled_circuit = transpile(ansatz, backend=backend, optimization_level=opt_level)
    
    print(f"\nOptimization Level {opt_level}:")
    print(f"  - Total Circuit Depth: {transpiled_circuit.depth()}")
    print(f"  - Total Gate Count: {transpiled_circuit.size()}")
    print(f"  - SWAP Count: {transpiled_circuit.count_ops().get('swap', 0)}")
    print(f"  - CNOT (cx) Count: {transpiled_circuit.count_ops().get('cx', 0)}")