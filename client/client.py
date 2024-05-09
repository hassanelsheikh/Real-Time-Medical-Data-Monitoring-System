import socket
import json
import numpy as np
import time

# Define the server address
server_address = ('localhost', 3001)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# Define the number of patients
num_patients = 5

while True:
    # Generate and send one value for each patient
    for patient_id in range(1, num_patients + 1):
        # Generate a single ECG value for the patient
        ecg_value = np.random.normal(loc=0, scale=1)
        
        # Create data dictionary for the patient
        data = {
            'patient_id': patient_id,
            'ecg_value': ecg_value
        }
        
        # Serialize the data
        json_str = json.dumps(data)
        
        # Send the data to the server
        client_socket.sendall(json_str.encode() + b'\n')
        print(f"Data sent for patient ID: {patient_id}...", ecg_value)
        
        # Sleep for 10 milliseconds before sending data for the next patient
        time.sleep(0.01)
    
    # Wait for a short interval before sending the next batch of data
    time.sleep(0.1)
