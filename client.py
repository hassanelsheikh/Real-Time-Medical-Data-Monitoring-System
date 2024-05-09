import socket
import json
import time
import random

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)
client_socket.connect(server_address)

# Number of patients
num_patients = 5

while True:
    for patient_index in range(1, num_patients + 1):
        # Simulate data generation for heart rate and blood pressure
        heart_rate = random.randint(60, 100)
        blood_pressure = random.randint(80, 120)

        # Serialize data to JSON
        data = json.dumps({'patient_id': patient_index, 'heart_rate': heart_rate, 'blood_pressure': blood_pressure})

        # Send data to the server
        client_socket.sendall(data.encode())

        print(f"Data sent for patient ID: {patient_index}, Heart Rate: {heart_rate}, Blood Pressure: {blood_pressure}")

    time.sleep(1)  # Send data every second

# Close the socket
client_socket.close()
