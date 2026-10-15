import socket
import time

esp_ip = "192.168.x.x"  # Replace with your ESP8266's IP address
port = 8080

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10)  # Set a timeout for the connection
    print("Attempting to connect to ESP8266...")
    client.connect((esp_ip, port))
    print("Connection established.")
except socket.error as e:
    print(f"Error connecting to ESP8266: {e}")
    exit(1)

print("Connected to ESP8266 at", esp_ip)
try:
    while True:
        num = input("Enter a number: ")
        if not num.isdigit():
            print("Please enter a valid number.")
            continue

        client.send((num + '\n').encode())  # Send number with newline
        time.sleep(0.2) # Wait for ESP8266 to process
        response = client.recv(1024).decode()
        print("ESP8266 says:", response)
        
        if num == "99":
            break
except KeyboardInterrupt:
    client.close()
