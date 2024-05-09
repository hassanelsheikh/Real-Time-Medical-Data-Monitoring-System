import socket
import json
import redis

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a host and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

print("Server is listening for incoming connections...")

while True:
    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    # Receive data from the client
    data = b''
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        data += chunk

    if data:
        # Deserialize JSON data
        try:
            data = json.loads(data.decode())
            # Store data in Redis
            patient_id = data.get('patient_id')
            vital_signs = data.get('vital_signs')
            redis_client.set(patient_id, json.dumps(vital_signs))
            print(f"Data received and stored for patient ID: {patient_id}")
        except json.decoder.JSONDecodeError as e:
            print("Error decoding JSON:", e)

    # Close the client socket
    client_socket.close()
