from lib import *
from circuits import *
from qiskit.quantum_info import Operator
from qiskit.circuit.controlledgate import ControlledGate
from qiskit.circuit.library.standard_gates import XGate, ZGate
from numpy import sqrt, matrix

n_logical = 4
n_ancilla = 2

totalNum = 2*n_logical + n_ancilla

rangeLogical = range(n_logical, 2*n_logical)
rangeAncilla = range(2*n_logical, totalNum)

# n |+ > states that are needed to control the flipping of n qubits
# there are n logic qubits and n/3 logical qubits
errReg = QuantumRegister(n_logical, "E")
logReg = QuantumRegister(n_logical, "L")
ancillaReg = QuantumRegister(n_ancilla, "A")
errCReg_x = ClassicalRegister(n_logical, "eX")
errCReg_z = ClassicalRegister(n_logical, "eZ")
ancCReg = ClassicalRegister(n_ancilla, "cA")
circuit = QuantumCircuit(errReg, logReg, ancillaReg, errCReg_x, errCReg_z, ancCReg)

# ----------- message encoding ---------------------
circuit.barrier(range(totalNum), label="Encoder")

# encoder by definition for [[4,2,2]] codespace
encoder = encoder_as_gate(n_logical)
circuit.append(encoder, logReg)

# ----------- state preparation (apply error) -----------------

circuit.barrier(range(totalNum), label="X-Error")
append_error_correction_x(circuit, n_logical)
circuit.barrier(range(totalNum), label="Z-Error")
append_error_correction_z(circuit, n_logical)

# ------- after that the first qubits are useless and the state is prepared in the second n bit.
# ------- in these n bits there is the state En (qubits with error), now it's time to apply the error correction

# -------------- error correction ------------------------
circuit.barrier(range(totalNum), label="Error Correction")

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

