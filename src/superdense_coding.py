import cirq


def bitstring(bits):
    return ''.join('1' if b else '0' for b in bits)


qreg = [cirq.LineQubit(i) for i in range(2)]
circuit = cirq.Circuit()

message_operations = {
    "00": [],
    "01": [cirq.X(qreg[0])],
    "10": [cirq.Z(qreg[0])],
    "11": [cirq.X(qreg[0]), cirq.Z(qreg[0])]
}

circuit.append(cirq.H(qreg[0]))
circuit.append(cirq.CNOT(qreg[0], qreg[1]))

message_to_send = "10"
print("Alice wants to send the message:", message_to_send)

circuit.append(message_operations[message_to_send])

circuit.append(cirq.CNOT(qreg[0], qreg[1]))
circuit.append(cirq.H(qreg[0]))
circuit.append([cirq.measure(qreg[0]), cirq.measure(qreg[1])])

print("Circuit:")
print(circuit)

simulator = cirq.Simulator()
result = simulator.simulate(circuit)
print("\n", result.measurements.values())
print("\nBob's received message =", bitstring(result.measurements.values()))
