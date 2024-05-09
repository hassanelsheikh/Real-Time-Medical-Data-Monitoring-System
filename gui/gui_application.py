import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QTimer
import socket
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ECGMonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Medical Data Monitoring System")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Patient ID label
        self.patient_id_label = QLabel("Patient ID: ")
        layout.addWidget(self.patient_id_label)

        # Search bar
        self.search_label = QLabel("Enter Patient ID:")
        self.search_edit = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_patient)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Plot area
        self.canvas = ECGPlot()
        layout.addWidget(self.canvas)

        # Start button
        self.start_button = QPushButton("Start Monitoring")
        self.start_button.clicked.connect(self.start_monitoring)

        layout.addWidget(self.start_button)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.is_monitoring = False

        # Socket connection
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 12345)

    def start_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.start_button.setDisabled(True)
            self.timer.start(100)  # Update plot every 100 milliseconds

            # Connect to the server
            self.client_socket.connect(self.server_address)

    def update_plot(self):
        if self.is_monitoring:
            # Update patient ID label
            patient_id = self.search_edit.text()
            self.patient_id_label.setText(f"Patient ID: {patient_id}")

            # Check if a patient ID is provided
            if patient_id:
                # Generate random ECG data
                ecg_data = np.random.normal(loc=0, scale=0.5, size=1000)  # Placeholder data
                self.canvas.plot(ecg_data)

                # Send data to the server
                vital_signs = ecg_data.tolist()  # Convert numpy array to list
                data = json.dumps({'patient_id': patient_id, 'vital_signs': vital_signs})
                self.client_socket.sendall(data.encode())

    def search_patient(self):
        if not self.is_monitoring:
            # Fetch patient's vital sign data from Redis using patient_id
            # Update the plot with the retrieved data
            pass


class ECGPlot(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)

    def plot(self, ecg_data):
        self.ax.clear()
        self.ax.plot(ecg_data, color='blue')
        self.ax.set_title('ECG Data')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Amplitude')
        self.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ecg_monitor = ECGMonitor()
    ecg_monitor.show()
    sys.exit(app.exec_())
