from lib import *

n = 6

# n |+ > states that are needed to control the flipping of n qubits
# there are n logic qubits and n/3 logical qubits
circuit = QuantumCircuit(2*n,2*n)


# -----------. state preparation -----------------


#apply n haddamard gates
for i in range (n):
    circuit.h(i)

#measure the |+> states
for i in range (n):
    circuit.measure(i,i)

#flip the bit conditionally to the first n bits
for i in range (n):
    circuit.x(n+i).c_if(circuit.cregs[0][i], 1)

#------- after that the first n qubits are useless and the state is prepared in the second n bit.
# ------ in these n bits there is the state En (qubits with error), now it's time to apply the error correction


##------- error correction---------






#----------------- measure -----------------------------------

for i in range (n,2*n):
    circuit.measure(i,i)


#------------------- simulate ------------------------------


show_circuit(circuit)

backend = back('simulator')
shots = 10240
new_circuit = transpile(circuit, backend, shots)
result = backend.run(new_circuit).result()

print(result.get_counts())

plot_histogram(result.get_counts(circuit))
plt.show(block=False)
input()

