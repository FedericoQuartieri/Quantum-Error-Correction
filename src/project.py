from lib import *
from circuits import *
from qiskit.quantum_info import Operator
from qiskit.circuit.controlledgate import ControlledGate
from qiskit.circuit.library.standard_gates import XGate, ZGate
from numpy import sqrt, matrix

n_logical = 4   
n_ancilla = 2
n_max_errors_per_axes = 1

totalNum = n_max_errors_per_axes + n_logical + n_ancilla

rangeLogical = range(n_max_errors_per_axes, n_max_errors_per_axes + n_logical)
rangeAncilla = range(n_max_errors_per_axes + n_logical, totalNum)

# n |+ > states that are needed to control the flipping of n qubits

errReg = QuantumRegister(n_max_errors_per_axes, "E")
logReg = QuantumRegister(n_logical, "L")
ancillaReg = QuantumRegister(n_ancilla, "A")
errCReg_x = ClassicalRegister(n_max_errors_per_axes, "eX")
errCReg_z = ClassicalRegister(n_max_errors_per_axes, "eZ")
ancCReg = ClassicalRegister(n_ancilla, "cA")
circuit = QuantumCircuit(errReg, logReg, ancillaReg, errCReg_x, errCReg_z, ancCReg)

# ----------- message encoding ---------------------
circuit.barrier(range(totalNum), label="Encoder")

# encoder by definition for [[4,2,2]] codespace
encoder = encoder_as_gate(n_logical)
circuit.append(encoder, logReg)


print_statevector(circuit)

# ----------- state preparation (apply error) -----------------

circuit.barrier(range(totalNum), label="X-Error")
append_error_x(circuit, n_max_errors_per_axes)
circuit.barrier(range(totalNum), label="Z-Error")
append_error_z(circuit, n_max_errors_per_axes)

# ------- after that the first qubits are useless and the state is prepared in the second n bit.
# ------- in these n bits there is the state En (qubits with error), now it's time to apply the error correction

# -------------- error detection ------------------------
circuit.barrier(range(totalNum), label="Error Detection")

for i in rangeAncilla:
    circuit.h(i)

#add 4 x gate
x4_gate = QuantumCircuit(n_logical)
for i in range(n_logical):
    x4_gate.x(i)
x4_gate = x4_gate.to_gate(label="X").control(1)

ancilla_idx = n_max_errors_per_axes + n_logical
qbitlist = list(rangeLogical)
qbitlist.insert(0, ancilla_idx)
circuit.append(x4_gate, qbitlist)

#add 4 z gate
z4_gate = QuantumCircuit(n_logical)
for i in range(n_logical):
    z4_gate.x(i)
z4_gate = z4_gate.to_gate(label="Z").control(1)
qbitlist[0] = ancilla_idx+1
circuit.append(z4_gate, qbitlist)

for i in rangeAncilla:
    circuit.h(i)

#----------------- measure -----------------------------------

# measure the ancilla, save in the first bits of classical register
idxBit = 0
for i in rangeAncilla:
    circuit.measure(i, ancCReg[idxBit])
    idxBit += 1

#------------------- simulate ------------------------------

show_circuit(circuit)

backend = back('simulator')
shots = 10000
new_circuit = transpile(circuit, backend)
result = backend.run(new_circuit, shots=shots).result()

print(result.get_counts())

plot_histogram(result.get_counts(circuit), title=f"Ancilla results shots={shots}")
plt.tight_layout()
plt.show(block=False)

input()

