from lib import *

n_logical = 2
n_ancilla = 2

totalNum = 2*n_logical + n_ancilla

rangeErrorGen = range(n_logical)
rangeLogical = range(n_logical, 2*n_logical)
rangeAncilla = range(2*n_logical, totalNum)

# n |+ > states that are needed to control the flipping of n qubits
# there are n logic qubits and n/3 logical qubits
circuit = QuantumCircuit(totalNum, totalNum)


# -----------. state preparation -----------------


#apply n haddamard gates
for i in rangeErrorGen:
    circuit.h(i)

#measure the |+> states
for i in range(n_logical):
    circuit.measure(i,i)

#flip the bit conditionally to the first n bits
for i in range(n_logical):
    circuit.x(i+n_logical).c_if(circuit.cregs[0][i], 1)

#------- after that the first n qubits are useless and the state is prepared in the second n bit.
# ------ in these n bits there is the state En (qubits with error), now it's time to apply the error correction


##------- error correction---------

for i in rangeAncilla:
    circuit.h(i)

ancilla_idx = 2*n_logical
for i in rangeLogical:
    circuit.cx(ancilla_idx, i)

for i in rangeLogical:
    circuit.cz(ancilla_idx+1, i)

#----------------- measure -----------------------------------

# reset the classical register 
# circuit.cregs[0]

# measure the ancilla, save in the first bits of classical register
idxBit = 0
for i in rangeAncilla:
    circuit.measure(i, idxBit)
    idxBit += 1


#------------------- simulate ------------------------------

show_circuit(circuit)

backend = back('simulator')
shots = 10240
new_circuit = transpile(circuit, backend)
result = backend.run(new_circuit, shots=shots).result()

print(result.get_counts())

plot_histogram(result.get_counts(circuit))
plt.show(block=False)

input()

