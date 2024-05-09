import socket
import json
import numpy as np
import time

# Define the server address
server_address = ('localhost', 3001)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

#5 patients with different ECG data
patients = {
    # Patient 1
    1: np.random.normal(loc=0, scale=1, size=100),
    # Patient 2
    2: np.random.normal(loc=0, scale=1, size=100),
    # Patient 3
    3: np.random.normal(loc=0, scale=1, size=100),
    # Patient 4
    4: np.random.normal(loc=0, scale=1, size=100),
    # Patient 5
    5: np.random.normal(loc=0, scale=1, size=100),
}

#send ECG data for each patient to server

while True:
    #send ECG for each patient at the same time
    for patient_id, ecg_data in patients.items():
        data = {
            'patient_id': patient_id,
            'vital_signs': ecg_data.tolist()
        }
        # Serialize the data
        json_str = json.dumps(data)
        # Send the data to the server
        client_socket.sendall(json_str.encode() + b'\n')
        print(f"Data sent for patient ID: {patient_id}...")
    # Wait for 1 second

    time.sleep(1)


