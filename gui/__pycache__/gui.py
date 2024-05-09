import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import redis
import threading
import time

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Global variable to keep track of the monitoring thread
monitoring_thread = None
# Global variable to signal thread termination
terminate_monitoring = threading.Event()

# Function to plot ECG data
def plot_ecg(patient_id, ecg_data_array):
    ax.clear()  # Clear the previous plot
    ax.set_title(f'ECG Data for Patient ID: {patient_id}')
    ax.set_xlabel('Time')
    ax.set_ylabel('ECG Value')
    ax.grid(True)
    
    # Adjust dynamic range based on the number of data points
    if len(ecg_data_array) > 20:
        start_index = len(ecg_data_array) - 20
    else:
        start_index = 0
    
    ax.plot(ecg_data_array[start_index:], linestyle='-', color='b')  # Plot the updated data array
    canvas.draw()  # Update the plot in the GUI

# Function to continuously monitor Redis for new data
def monitor_redis(patient_id, ecg_data_array):
    global terminate_monitoring
    while not terminate_monitoring.is_set():
        ecg_data = redis_client.get(patient_id)
        if ecg_data:
            ecg_data = float(ecg_data)  # Convert the string to float
            ecg_data_array.append(ecg_data)  # Append the converted float value
            # Plot the updated ECG data
            plot_ecg(patient_id, ecg_data_array)
        time.sleep(0.1)  # Adjust the sleep time as needed for real-time updates

# Function to stop the monitoring thread
def stop_monitoring_thread():
    global monitoring_thread, terminate_monitoring
    if monitoring_thread:
        terminate_monitoring.set()
        monitoring_thread.join()
        monitoring_thread = None
        terminate_monitoring.clear()
        canvas.draw_idle()  # Ensure the canvas is properly updated

# Function to handle search button click
def search_patient():
    global monitoring_thread
    if monitoring_thread:
        stop_monitoring_thread()  # Stop the previous monitoring thread if it's running
    
    patient_id = entry.get()
    if not patient_id:
        messagebox.showerror("Error", "Please enter a valid Patient ID!")
        return
    
    if redis_client.get(patient_id) is None:
        messagebox.showerror("Error", "No ECG data found for Patient ID: " + patient_id)
        return
    
    ecg_data_array = []  # Initialize an empty array to store ECG data
    # Start a new thread to monitor Redis for new data
    monitoring_thread = threading.Thread(target=monitor_redis, args=(patient_id, ecg_data_array))
    monitoring_thread.start()

# Create GUI
root = tk.Tk()
root.title("Real-Time ECG Data Viewer")

label = tk.Label(root, text="Enter Patient ID:")
label.pack()

entry = tk.Entry(root)
entry.pack()

search_button = tk.Button(root, text="Search", command=search_patient)
search_button.pack()

stopButton = tk.Button(root, text="Stop", command=stop_monitoring_thread)
stopButton.pack()

# Create a matplotlib figure and canvas
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Start GUI main loop
root.mainloop()
