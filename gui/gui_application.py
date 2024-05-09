import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QTimer, pyqtSignal, QThread
import socket
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import redis
import time

class ECGMonitor(QWidget):
    # Define a signal to trigger updating the plot
    update_plot_signal = pyqtSignal(str)

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

        # Error label
        self.error_label = QLabel("")
        layout.addWidget(self.error_label)

        # Plot area
        self.canvas = ECGPlot()
        layout.addWidget(self.canvas)

        # Start/Stop buttons
        self.start_button = QPushButton("Start Monitoring")
        self.start_button.clicked.connect(self.start_monitoring)

        self.stop_button = QPushButton("Stop Monitoring")
        self.stop_button.setDisabled(True)
        self.stop_button.clicked.connect(self.stop_monitoring)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.timer = QTimer()
        self.is_monitoring = False

        # Redis connection
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

        # Connect the signal to the update_plot function
        self.update_plot_signal.connect(self.update_plot)

        # Thread for sending ECG data
        self.ecg_thread = ECGThread()
    def start_monitoring(self):
        if not self.is_monitoring:
            patient_id = self.search_edit.text()
            if patient_id:
                if self.redis_client.exists(patient_id):
                    self.is_monitoring = True
                    self.start_button.setDisabled(True)
                    self.stop_button.setEnabled(True)
                    self.timer.timeout.connect(self.timer_timeout)
                    self.timer.start(100)

                    self.ecg_thread.start()
                else:
                    self.error_label.setText("Error: Patient ID not found.")
            else:
                self.error_label.setText("Error: Please enter a valid Patient ID.")

    def stop_monitoring(self):
        if self.is_monitoring:
            self.is_monitoring = False
            self.start_button.setEnabled(True)
            self.stop_button.setDisabled(True)
            self.timer.stop()

            # Stop the ECG data thread
            self.ecg_thread.stop()

            # Clear the canvas
            self.canvas.plot([])

    def timer_timeout(self):
        # Trigger updating the plot
        self.update_plot_signal.emit(self.search_edit.text())

    def update_plot(self, patient_id):
        if patient_id:
            # Retrieve ECG data from Redis
            ecg_data_json = self.redis_client.get(patient_id)

            if ecg_data_json:
                try:
                    # Deserialize the received JSON data
                    ecg_data = json.loads(ecg_data_json.decode())

                    # Plot the received ECG data
                    self.canvas.plot(ecg_data)

                    # Update the patient ID label
                    self.patient_id_label.setText(f"Patient ID: {patient_id}")

                except Exception as e:
                    print("Error processing JSON data:", e)
            else:
                print("No ECG data found in Redis for patient ID:", patient_id)
        else:
            print("No patient ID provided")

    def search_patient(self):
        if not self.is_monitoring:
            # Obtain the patient ID from the GUI
            patient_id = self.search_edit.text()
            if patient_id:
                print("asdasdasd",self.redis_client.get(patient_id))
                if self.redis_client.get(patient_id):
                    # Update the patient ID for the ECG data thread
                    self.error_label.setText("")  # Clear error message
                    # Start the ECG data thread
                    self.ecg_thread.start()
                else:
                    # Display error message for invalid patient ID
                    self.error_label.setText("Error: Patient ID not found.")
                    # Clear the canvas if no ECG data found
                    self.canvas.plot([])
                    # Update the patient ID label
                    self.patient_id_label.setText(f"Patient ID: {patient_id}")


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

class ECGThread(QThread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.patient_id = ""


    def stop(self):
        self.running = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ecg_monitor = ECGMonitor()
    ecg_monitor.show()
    sys.exit(app.exec_())
