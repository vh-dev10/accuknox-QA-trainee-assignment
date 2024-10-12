import psutil
import logging
import time
import signal
import sys

# Setup logging
LOG_FILE = "system_health_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Define thresholds
CPU_THRESHOLD = 80  # CPU usage percentage
MEMORY_THRESHOLD = 80  # Memory usage percentage
DISK_THRESHOLD = 80  # Disk usage percentage
PROCESS_THRESHOLD = 200  # Number of running processes

# Flag to continue monitoring
monitoring = True

# Function to handle user interrupt (Ctrl+C)
def signal_handler(sig, frame):
    global monitoring
    print("\nInterrupt received. Stopping monitoring...")
    monitoring = False

# Function to check CPU usage
def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        alert = f"High CPU Usage: {cpu_usage}%"
        logging.info(alert)
        print(alert)
    return cpu_usage

# Function to check memory usage
def check_memory_usage():
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    if memory_usage > MEMORY_THRESHOLD:
        alert = f"High Memory Usage: {memory_usage}%"
        logging.info(alert)
        print(alert)
    return memory_usage

# Function to check disk space usage
def check_disk_usage():
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    if disk_usage > DISK_THRESHOLD:
        alert = f"Low Disk Space: {disk_usage}% used"
        logging.info(alert)
        print(alert)
    return disk_usage

# Function to check running processes
def check_processes():
    process_count = len(psutil.pids())
    if process_count > PROCESS_THRESHOLD:
        alert = f"High number of running processes: {process_count}"
        logging.info(alert)
        print(alert)
    return process_count

# Function to monitor system health
def monitor_system_health():
    cpu_usage = check_cpu_usage()
    memory_usage = check_memory_usage()
    disk_usage = check_disk_usage()
    process_count = check_processes()

    # Print the current system status
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")
    print(f"Disk Usage: {disk_usage}%")
    print(f"Running Processes: {process_count}")

# Function to display log
def read_logs():
    try:
        with open(LOG_FILE, 'r') as log_file:
            print(log_file.read())
    except FileNotFoundError:
        print("Log file not found. No alerts generated yet.")

# Function to show the menu and handle input
def menu():
    while True:
        print("\nSystem Health Monitor Menu:")
        print("1. Start Monitoring System Health (3-sec intervals)")
        print("2. Read Logs")
        print("0. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            try:
                global monitoring
                monitoring = True
                print("Monitoring system health... Press Ctrl+C to stop.")
                
                # Register signal handler for interrupt
                signal.signal(signal.SIGINT, signal_handler)

                while monitoring:
                    monitor_system_health()
                    time.sleep(3)  # Wait for 3 seconds between checks
            except Exception as e:
                print(f"An error occurred: {e}")
        elif choice == 2:
            read_logs()
        elif choice == 0:
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

# Run the menu-driven system
if __name__ == "__main__":
    menu()
