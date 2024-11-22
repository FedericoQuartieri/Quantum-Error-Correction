from lib import *
from circuits import *
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from numpy import sqrt, matrix
from time import sleep

n_logical = 4   
n_ancilla = 2
n_max_errors_per_axes = 2

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
# circuit.barrier(range(totalNum), label="Encoder")

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
ancilla_idx = n_max_errors_per_axes + n_logical

circuit.barrier(range(totalNum), label="Detect X-Flip")
for i in rangeLogical:
    circuit.cx(i, ancilla_idx)

circuit.barrier(range(totalNum), label="Detect Z-Flip")
for i in rangeLogical:
    circuit.append(CNOT_H_basis_control(), [i, ancilla_idx+1])
    

#----------------- measure -----------------------------------
circuit.barrier(range(totalNum), label="Measure")

# measure the ancilla, save in the first bits of classical register
idxBit = 0
for i in rangeAncilla:
    circuit.measure(i, ancCReg[idxBit])
    idxBit += 1

#------------------- simulate ------------------------------

show_circuit(circuit)

if my_token is None:
    backend = back('simulator')
else: 
    backend = back('real')

shots = 1000
new_circuit = transpile(circuit, backend)

if my_token is None:
    result = backend.run(new_circuit, shots=shots).result()
else:
    sampler = Sampler(backend)
    job = sampler.run([new_circuit], shots=shots)
    i = 0
    while not job.done():
        print(str(i*10) + ": " + job.status())
        sleep(10)
        i += 1
    result = job.result()

print(result.get_counts())

plot_histogram(result.get_counts(circuit), title=f"Ancilla results shots={shots}")
plt.tight_layout()
plt.show(block=False)

input()

