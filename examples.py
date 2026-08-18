from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

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
qc.cx(0, 1)
qc.measure(2, 2)


print("Circuit Diagram:")
print(qc) 

sim = AerSimulator()
job = sim.run(qc, shots=1000)
result = job.result().get_counts()

print("\nResults of 1000 shots: ")
print(result)