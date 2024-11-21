from lib import *
from qiskit.quantum_info import Operator
from qiskit.circuit.library import XGate, ZGate
from numpy import sqrt, matrix

n_logical = 4
n_ancilla = 2

totalNum = 2*n_logical + n_ancilla

rangeErrorGen = range(n_logical)
rangeLogical = range(n_logical, 2*n_logical)
rangeAncilla = range(2*n_logical, totalNum)

# n |+ > states that are needed to control the flipping of n qubits
# there are n logic qubits and n/3 logical qubits
circuit = QuantumCircuit(totalNum, n_logical+n_ancilla)

# ----------- message encoding ---------------------

# message to be transmitted is |00>_L 
for i in rangeLogical:
    circuit.initialize([1,0], i)

# encoder by definition for [[4,2,2]] codespace
circuit.cx(n_logical, n_logical+2)
circuit.cx(n_logical+1, n_logical+2)
circuit.h(n_logical+3)
circuit.cx(n_logical+3, n_logical+2)
circuit.cx(n_logical+3, n_logical+1)
circuit.cx(n_logical+3, n_logical)


circuit.barrier(range(totalNum), label="Encoder")
# ----------- state preparation (apply error) -----------------

#apply n haddamard gates
for i in rangeErrorGen:
    circuit.h(i)

#measure the |+> states
for i in rangeErrorGen:
    circuit.measure(i,i)

#flip the bit conditionally to the first n bits
for i in rangeErrorGen:
    circuit.x(i+n_logical).c_if(circuit.cregs[0][i], 1)

#------- after that the first qubits are useless and the state is prepared in the second n bit.
# ------ in these n bits there is the state En (qubits with error), now it's time to apply the error correction

circuit.barrier(range(totalNum))

#apply n haddamard gates
for i in rangeErrorGen:
    circuit.h(i)

#measure the |+> states
for i in rangeErrorGen:
    circuit.measure(i,i)

#flip the bit conditionally to the first n bits
for i in rangeErrorGen:
    circuit.z(i+n_logical).c_if(circuit.cregs[0][i], 1)

circuit.barrier(range(totalNum))
##------- error correction---------

for i in rangeAncilla:
    circuit.h(i)

ancilla_idx = 2*n_logical
for i in rangeLogical:
    circuit.cx(ancilla_idx, i)

for i in rangeLogical:
    circuit.cz(ancilla_idx+1, i)

for i in rangeAncilla:
    circuit.h(i)

#----------------- measure -----------------------------------

# measure the ancilla, save in the first bits of classical register
idxBit = n_logical
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

plot_histogram(result.get_counts(circuit), title=f"Ancilla results shots={shots}")
plt.show(block=False)

input()

