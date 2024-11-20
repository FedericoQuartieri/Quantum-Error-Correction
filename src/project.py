from lib import *
from qiskit.quantum_info import Operator
from qiskit.circuit.library import XGate, ZGate
from math import sqrt

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

# encode message as per [[4,2,2]] detection code logical space definition
# TODO calculate equivalent matrix for the logical space
# |0000>  becomes 1/sqrt(2) |0000>+|1111>
# |0100>  becomes 1/sqrt(2) |0110>+|1001>
# |1000>  becomes 1/sqrt(2) |1010>+|0101>
# |1100>  becomes 1/sqrt(2) |1100>+|0011>
baseSet = [0 for i in range(16)]
print(baseSet)
def getBaseState(i):
    s = list(baseSet)
    s[i] = 1
    return Statevector(s)
def getBellState(i1, i2):
    s = list(baseSet)
    s[i1] = 1/sqrt(2)
    s[i2] = 1/sqrt(2)
    return Statevector(s)

# TODO getBaseState(0) * getBellState(0, 15).conjugate()

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
idxBit = 2
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

