from lib import *
from numpy import sqrt, matrix
from qiskit.circuit.library import UnitaryGate

def encoder_as_gate(n_base : int):
    circuit = QuantumCircuit(n_base)
    circuit.cx(0, 2)
    circuit.cx(1, 2)
    circuit.h(3)
    circuit.cx(3, 2)
    circuit.cx(3, 1)
    circuit.cx(3, 0)

    return circuit.to_gate(label="Encoder")

def append_error_x(circuit : QuantumCircuit, n_max_errors : int):
    rangeErrorGen = range(n_max_errors)
    #apply n haddamard gates
    for i in rangeErrorGen:
        circuit.h(i)

    #measure the |+> states
    for i in rangeErrorGen:
        circuit.measure(i,i)

    #flip the bit conditionally to the first n bits
    for i in rangeErrorGen:
        circuit.x(i+n_max_errors).c_if(circuit.cregs[0][i], 1)


def append_error_z(circuit : QuantumCircuit, n_max_errors : int):
    rangeErrorGen = range(n_max_errors)
    #apply n hadamard gates
    for i in rangeErrorGen:
        circuit.h(i)

    #measure the |+> states
    for i in rangeErrorGen:
        circuit.measure(i,i+n_max_errors)

    #flip the bit conditionally to the first n bits
    for i in rangeErrorGen:
        circuit.z(i+n_max_errors).c_if(circuit.cregs[1][i], 1)

    #------- after that the first qubits are useless and the state is prepared in the second n_logical qubits.
    # ------ in these n bits there is the state En (qubits with error), now it's time to apply the error correction

def CNOT_H_basis_control():
    plusZero = 1/sqrt(2) * matrix([1,1,0,0]).transpose()
    plusOne = 1/sqrt(2) * matrix([0,0,1,1]).transpose()
    minusZero = 1/sqrt(2) * matrix([1,-1,0,0]).transpose()
    minusOne = 1/sqrt(2) * matrix([0,0,1,-1]).transpose()

    o1 = plusZero*plusOne.transpose()
    o2 = plusOne*plusZero.transpose()
    o3 = minusZero*minusZero.transpose()
    o4 = minusOne*minusOne.transpose()
    # This gate applies X gate to target if control is |+>
    return UnitaryGate(o1+o2+o3+o4, label="CNOT_H-Basis")


#instead of CNOT_H_basis_control
def my_gate():
    cz_matrix = np.array([
        [0.5, -0.5, 0.5, 0.5],
        [-0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, -0.5],
        [0.5, 0.5, -0.5, 0.5]
    ])
    return UnitaryGate(cz_matrix, label="MyGate")


# Dump for x4 z4 gates

#add 4 x gate (doesn't work, why?)
# x4_gate = QuantumCircuit(n_logical)
# for i in range(n_logical):
#     x4_gate.x(i)
# x4_gate = x4_gate.to_gate(label="X").control(1)

# qbitlist = list(rangeLogical)
# qbitlist.insert(0, ancilla_idx)
# circuit.append(x4_gate, qbitlist)

#  add 4 z gate (doesn't work, why?)
# z4_gate = QuantumCircuit(n_logical)
# for i in range(n_logical):
#     z4_gate.x(i)
# z4_gate = z4_gate.to_gate(label="Z").control(1)
# qbitlist[0] = ancilla_idx+1
# circuit.append(z4_gate, qbitlist)
