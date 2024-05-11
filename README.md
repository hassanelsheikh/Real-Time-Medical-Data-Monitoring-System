# Real-Time Medical Data Monitoring System

This project implements a real-time medical data monitoring system using Python. It consists of three main components:

1. **Client**: Simulates medical devices that continuously send electrocardiogram (ECG) data for multiple patients to a server.
2. **Server**: Listens for incoming ECG data from clients and stores the data in Redis.
3. **Viewer**: A graphical user interface (GUI) that allows users to search for patient data stored in Redis and visualize the real-time ECG data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/real-time-medical-data-monitoring-system.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Make sure you have Redis installed and running on your local machine.

## Usage

### Server

1. Navigate to the `server` directory:

   ```bash
   cd server
   ```

2. Run the server script:

   ```bash
   python server.py
   ```

### Client

1. Navigate to the `client` directory:

   ```bash
   cd client
   ```

2. Run the client script:

   ```bash
   python client.py
   ```

### Viewer

1. Navigate to the `gui` directory:

   ```bash
   cd gui
   ```

2. Run the viewer script:

   ```bash
   python gui.py
   ```

3. Enter the Patient ID in the provided input field and click "Search" to visualize the real-time ECG data.

## Components

### Client

The client component simulates medical devices that send ECG data to the server. It generates random ECG data for multiple patients and sends it to the server via TCP sockets.

### Server

The server component listens for incoming ECG data from clients. Upon receiving data, it stores the data in Redis, associating each data point with the respective patient ID.

### Viewer

The viewer component provides a GUI for users to search for patient data stored in Redis and visualize the real-time ECG data. It continuously monitors Redis for updates and plots the ECG data in real-time.

## Dependencies

- Python 3
- Redis
- tkinter
- matplotlib
- numpy

