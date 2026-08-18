import unittest
from max_cut import create_graph, get_cost_hamiltonian
from qiskit.circuit.library import QAOAAnsatz

class TestQAOA(unittest.TestCase):
    
    def setUp(self):
        self.graph = create_graph()
        self.hamiltonian = get_cost_hamiltonian(self.graph)
        
    def test_graph_nodes(self):
        self.assertEqual(self.graph.number_of_nodes(), 6)
        
    def test_hamiltonian_qubits(self):
        self.assertEqual(self.hamiltonian.num_qubits, 6)
        
    def test_ansatz_parameters_p1(self):
        ansatz = QAOAAnsatz(cost_operator=self.hamiltonian, reps=1)
        self.assertEqual(ansatz.num_parameters, 2)
        
    def test_ansatz_parameters_p2(self):
        ansatz = QAOAAnsatz(cost_operator=self.hamiltonian, reps=2)
        self.assertEqual(ansatz.num_parameters, 4)

if __name__ == '__main__':
    unittest.main(verbosity=2)