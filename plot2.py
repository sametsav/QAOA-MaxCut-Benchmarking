import os
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
from qiskit_aer.primitives import Estimator as LocalEstimator
from qiskit.circuit.library import QAOAAnsatz
from max_cut import create_graph, get_cost_hamiltonian

load_dotenv()

graph = create_graph()
hamiltonian = get_cost_hamiltonian(graph)

local_estimator = LocalEstimator()
ansatz = QAOAAnsatz(cost_operator=hamiltonian, reps=1)
sample_parameters = [0.5, 1.0]  
bound_circuit = ansatz.assign_parameters(sample_parameters)

job_local = local_estimator.run(circuits=[bound_circuit], observables=[hamiltonian])
result_local = job_local.result()
qaoa_sim = float(result_local.values[0])

service = QiskitRuntimeService(
    channel="ibm_cloud",
    token=os.getenv("IBM_TOKEN"),
    instance="crn:v1:bluemix:public:quantum-computing:us-east:a/8c53ff01b9f0440c8230d32e0ed8630a:4dcbb948-4cc2-4b8a-9451-3ac10cf6736c::"
)
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=7)

estimator_noisy = Estimator(mode=backend)
estimator_noisy.options.resilience_level = 0

estimator_mitigated = Estimator(mode=backend)
estimator_mitigated.options.resilience_level = 1 
estimator_mitigated.options.resilience.zne_mitigation = True

isa_circuit = transpile(bound_circuit, backend=backend, optimization_level=1)
isa_hamiltonian = hamiltonian.apply_layout(isa_circuit.layout)
pub_hardware = (isa_circuit, [isa_hamiltonian])

job_noisy = estimator_noisy.run([pub_hardware])
result_noisy = job_noisy.result()
qaoa_noisy = float(np.atleast_1d(result_noisy[0].data.evs)[0])

job_mitigated = estimator_mitigated.run([pub_hardware])
result_mitigated = job_mitigated.result()
qaoa_mitigated = float(np.atleast_1d(result_mitigated[0].data.evs)[0])

exact_energy = -12.5       
ratio_sim = abs(qaoa_sim / exact_energy)
ratio_noisy = abs(qaoa_noisy / exact_energy)
ratio_mitigated = abs(qaoa_mitigated / exact_energy)

print(f"Simulator: {ratio_sim:.3f}, Noisy: {ratio_noisy:.3f}, Mitigated: {ratio_mitigated:.3f}")

labels = ['Simulator', 'Noisy', 'Mitigated']
ratios = [ratio_sim, ratio_noisy, ratio_mitigated]
colors = ['#99ff99', '#ff9999', '#66b3ff']

plt.figure(figsize=(8, 5))
plt.bar(labels, ratios, color=colors, width=0.5)
plt.ylabel('Approximation Ratio ($\Gamma = E_{qaoa} / E_{exact}$)')
plt.title(f'Phase 5: Benchmark Comparison')
plt.ylim(0, 1.2)
plt.axhline(1.0, color='gray', linestyle='--', linewidth=1)
plt.tight_layout()
plt.show()