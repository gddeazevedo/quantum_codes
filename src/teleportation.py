import cirq
import random


def make_quantum_teleportation_circuit(rand_x: float, rand_y: float) -> tuple[cirq.LineQubit, cirq.Circuit]:
    circuit = cirq.Circuit()
    Q, R, S = cirq.LineQubit.range(3)

    circuit.append([cirq.H(R), cirq.CNOT(R, S)]) # emaranhando os qubits R e S
    circuit.append([cirq.XPowGate(exponent=rand_x).on(Q), cirq.YPowGate(exponent=rand_y).on(Q)]) # preparando o estado aleatório no qubit Q
    circuit.append([cirq.CNOT(Q, R), cirq.H(Q)]) # bell measurement entre Q e R
    circuit.append(cirq.measure(Q, R)) # medindo os qubits Q e R
    circuit.append([cirq.CNOT(R, S), cirq.CZ(Q, S)]) # aplicando as correções no qubit S

    return Q, circuit


rand_x = random.random()
rand_y = random.random()
Q, circuit = make_quantum_teleportation_circuit(rand_x, rand_y)

print("Circuit:")
print(circuit)

simulator = cirq.Simulator()
Q_init_state_vector = simulator\
    .simulate(cirq.Circuit(cirq.XPowGate(exponent=rand_x).on(Q), cirq.YPowGate(exponent=rand_y).on(Q)))\
    .final_state_vector

Q_b_x, Q_b_y, Q_b_z = cirq.bloch_vector_from_state_vector(Q_init_state_vector, index=0)

print(f"Alice's Bloch Sphere coords\nx: {Q_b_x}, y: {Q_b_y}, z: {Q_b_z}")

final_state_vector = simulator.simulate(circuit).final_state_vector
S_b_x, S_b_y, S_b_z = cirq.bloch_vector_from_state_vector(final_state_vector, index=2)

print(f"Bob's Bloch Sphere coords\nx: {S_b_x}, y: {S_b_y}, z: {S_b_z}")
