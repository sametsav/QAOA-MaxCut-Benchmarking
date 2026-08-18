from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager 


qc = QuantumCircuit(3, 3)

qc.x(0)
qc.barrier()

qc.h(1)
qc.cx(1, 2)
qc.barrier()

qc.cx(0, 1)
qc.h(0)
qc.barrier()

qc.measure([0, 1], [0, 1])
qc.barrier()

qc.cx(1, 2)
qc.cz(0, 2)
qc.measure(2, 2)

print("Circuit successfully created, connecting to IBM Cloud...")

service = QiskitRuntimeService(
    channel="ibm_cloud",
    token="q_l81WCGysaiR8quz1UfQcCc88mXU3XodyWGcIr_1saS",
    instance="crn:v1:bluemix:public:quantum-computing:us-east:a/8c53ff01b9f0440c8230d32e0ed8630a:4dcbb948-4cc2-4b8a-9451-3ac10cf6736c::"
)

backend = service.least_busy(operational=True, simulator=False)
print(f"Selected real quantum device: {backend.name}")

print("Transpiling the circuit for the target hardware's physical architecture...")
pm = generate_preset_pass_manager(target=backend.target, optimization_level=1)
isa_qc = pm.run(qc) 

sampler = Sampler(backend)
job = sampler.run([isa_qc], shots=1000) 

print(f"Job queued. Job ID: {job.job_id()}")
print("Job is in the IBM queue, results will be displayed when the device is available (please wait)...")

result = job.result()
pub_result = result[0]
counts = pub_result.data.c.get_counts() 

print("\nResults from the real quantum device:")
print(counts)