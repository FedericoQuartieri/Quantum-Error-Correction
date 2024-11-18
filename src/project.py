from lib import *

n = 3

circuit = QuantumCircuit(2*n,2*n)
# n |+ > states that are needed to control the flipping of n qubits
# there are n logic qubits and n/3 logical qubits


print_statevector(circuit)


#apply n haddamard gates
for i in range (n):
    circuit.h(i)

#measure the |+> states
for i in range (n):
    circuit.measure(i,i)

for i in range (n):
    circuit.x(n+i).c_if(circuit.cregs[0], 1 << i)

for i in range (n,2*n):
    circuit.measure(i,i)

show_circuit(circuit)



backend = back('simulator')
shots = 1024
new_circuit = transpile(circuit, backend, shots)
result = backend.run(new_circuit).result()

print(result.get_counts())

plot_histogram(result.get_counts(circuit))
plt.show(block=False)
input()


#show(circuit)
circuit = QuantumCircuit(2*n,2*n)
# n |+ > states that are needed to control the flipping of n qubits
# there are n logic qubits and n/3 logical qubits