import socket
import json
import redis

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Define the server address
server_address = ('localhost', 3001)

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(1)

print("Waiting for a connection...")

while True:
    # Wait for a connection
    connection, client_address = server_socket.accept()
    print("Connection established with", client_address)

    try:
        buffer = b''  # Initialize buffer to store received data
        while True:
            # Receive data from the client
            received_data = connection.recv(4096)
            if not received_data:
                break
            
            buffer += received_data
            # Split received data at delimiter ('\n') to extract individual JSON objects
            while b'\n' in buffer:
                json_str, buffer = buffer.split(b'\n', 1)
                # Deserialize JSON data
                data = json.loads(json_str.decode())
                
                # Extract relevant information
                patient_id = data.get('patient_id')
                ecg_data = data.get('ecg_value')
                print(f"Data received for patient ID: {patient_id, ecg_data}...")
                
                # Check if the received data is different from the data already stored in Redis
                old_ecg_data = redis_client.get(patient_id)
                print("Old data in Redis", old_ecg_data)
                if old_ecg_data != json.dumps(ecg_data):
                    # Store new data in Redis
                    redis_client.set(patient_id, json.dumps(ecg_data))
                    print("Data stored in Redis", patient_id, "...")
                else:
                    print("Received data is the same as the one in Redis. Ignoring...")
                
    except Exception as e:
        print("An error occurred:", e)
        break
    
    finally:
        # Close the connection
        connection.close()
