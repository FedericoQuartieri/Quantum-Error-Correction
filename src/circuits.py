from lib import *

def encoder_as_gate(n_base : int):
    circuit = QuantumCircuit(n_base)
    circuit.cx(0, 2)
    circuit.cx(1, 2)
    circuit.h(3)
    circuit.cx(3, 2)
    circuit.cx(3, 1)
    circuit.cx(3, 0)

    return circuit.to_gate(label="Encoder")

def append_error_correction_x(circuit : QuantumCircuit, n_logical : int):
    rangeErrorGen = range(n_logical)
    #apply n haddamard gates
    for i in rangeErrorGen:
        circuit.h(i)

    #measure the |+> states
    for i in rangeErrorGen:
        circuit.measure(i,i)

    #flip the bit conditionally to the first n bits
    for i in rangeErrorGen:
        circuit.x(i+n_logical).c_if(circuit.cregs[0][i], 1)


def append_error_correction_z(circuit : QuantumCircuit, n_logical : int):
    rangeErrorGen = range(n_logical)
    #apply n hadamard gates
    for i in rangeErrorGen:
        circuit.h(i)

    #measure the |+> states
    for i in rangeErrorGen:
        circuit.measure(i,i+n_logical)

    #flip the bit conditionally to the first n bits
    for i in rangeErrorGen:
        circuit.z(i+n_logical).c_if(circuit.cregs[1][i], 1)

    #------- after that the first qubits are useless and the state is prepared in the second n_logical qubits.
    # ------ in these n bits there is the state En (qubits with error), now it's time to apply the error correction
