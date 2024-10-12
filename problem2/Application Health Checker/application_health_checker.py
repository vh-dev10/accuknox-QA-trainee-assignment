import requests
import logging
import time

# Setup logging
LOG_FILE = "application_uptime_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to check the application's status
def check_application_status(app_url):
    try:
        # Send a GET request to the application's URL
        response = requests.get(app_url, timeout=5)
        
        # Check the HTTP status code
        if response.status_code == 200:
            status = "UP"
            print(f"Application is {status}. Status code: {response.status_code}")
        else:
            status = "DOWN"
            print(f"Application is {status}. Status code: {response.status_code}")
        
        # Log the result
        log_message = f"Application is {status}. Status code: {response.status_code}"
        logging.info(log_message)
        
    except requests.exceptions.RequestException as e:
        # If there is a network issue or the server is down, log it as DOWN
        status = "DOWN"
        print(f"Application is {status}. Error: {e}")
        
        # Log the error
        logging.info(f"Application is {status}. Error: {e}")

# Function to monitor the application periodically
def monitor_application(app_url, interval=60):
    print(f"Monitoring application at {app_url} every {interval} seconds. Press Ctrl+C to stop.")
    try:
        while True:
            check_application_status(app_url)
            time.sleep(interval)  # Wait for the specified interval before the next check
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

# Function to display logs
def read_logs():
    try:
        with open(LOG_FILE, 'r') as log_file:
            print(log_file.read())
    except FileNotFoundError:
        print("Log file not found. No logs generated yet.")

# Function to show menu and handle input
def menu():
    while True:
        print("\nApplication Uptime Checker Menu:")
        print("1. Start Monitoring Application")
        print("2. Read Logs")
        print("0. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            app_url = input("Enter the URL of the application to monitor: ")
            interval = int(input("Enter the monitoring interval (in seconds): "))
            monitor_application(app_url, interval)
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
