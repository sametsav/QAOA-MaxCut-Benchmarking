import os
from dotenv import load_dotenv
from qiskit.circuit.library import QAOAAnsatz
from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService
from max_cut import create_graph, get_cost_hamiltonian

load_dotenv()

service = QiskitRuntimeService(
    channel="ibm_cloud",
    token=os.getenv("IBM_TOKEN"),
    instance="crn:v1:bluemix:public:quantum-computing:us-east:a/8c53ff01b9f0440c8230d32e0ed8630a:4dcbb948-4cc2-4b8a-9451-3ac10cf6736c::"
)

backend = service.least_busy(operational=True, simulator=False, min_num_qubits=7)

G = create_graph(num_nodes=7)
hamiltonian = get_cost_hamiltonian(G)
ansatz = QAOAAnsatz(cost_operator=hamiltonian, reps=3)

for opt_level in range(4):
    transpiled_circuit = transpile(ansatz, backend=backend, optimization_level=opt_level)
    
    print(f"\nOptimization Level {opt_level}:")
    print(f"  - Total Circuit Depth: {transpiled_circuit.depth()}")
    print(f"  - Total Gate Count: {transpiled_circuit.size()}")
    print(f"  - SWAP Count: {transpiled_circuit.count_ops().get('swap', 0)}")
    print(f"  - CNOT Count: {transpiled_circuit.count_ops().get('cx', 0)}")