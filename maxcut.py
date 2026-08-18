import networkx as nx
from qiskit.quantum_info import SparsePauliOp

def create_graph(num_nodes=6):
    if num_nodes not in [6, 7, 8]:
        raise ValueError("Node count must be between 6 and 8")
        
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (1, 4)]
    
    if num_nodes >= 7:
        edges.extend([(5, 6), (2, 6)])
    if num_nodes == 8:
        edges.extend([(6, 7), (3, 7), (0, 7)])
        
    G.add_edges_from(edges)
    return G

def get_cost_hamiltonian(G):
    num_nodes = G.number_of_nodes()
    pauli_list = []
    
    for i, j in G.edges():
        pauli = []
        for node in range(num_nodes):
            if node == i or node == j:
                pauli.append('Z')
            else:
                pauli.append('I')
        
        pauli_string = ""
        for char in pauli:
            pauli_string += char
            
        reversed_string = pauli_string[::-1]
        
        pauli_list.append((reversed_string, 0.5))
        
    return SparsePauliOp.from_list(pauli_list) 