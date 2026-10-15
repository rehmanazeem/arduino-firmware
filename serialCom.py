import serial
import time

# Replace 'COM3' with the port your Arduino is connected to (e.g., '/dev/ttyUSB0' on Linux or '/dev/ttyACM0' on Mac)
import serial.tools.list_ports

# List available ports
ports = list(serial.tools.list_ports.comports())

# Let the user choose the port
port_index = 4
arduino_port = ports[port_index].device
baud_rate = 9600  # Match the baud rate with the Arduino code

try:
    # Establish serial connection
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(1)  # Wait for the connection to initialize

    print("Connected to Arduino. Ready to send commands. Type 'q' to quit.")
    while True:
        while ser.in_waiting > 0:  # Check if data is available
            data = ser.readline().decode('utf-8').strip()  # Read and decode the data
            print(f"Response: {data}")

        # Send data to Arduino
        data = input("Command: ").upper()
        if data.lower() == 'q':
            break
        ser.write(data.encode())
        print(f"Sending Command: {data}")

        time.sleep(2)  # Wait for the data to be sent
        

except serial.SerialException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()

# # baud_rate = 9600  # Match this with the baud rate set in your Arduino sketch

# # # Initialize serial connection
# # ser = serial.Serial(arduino_port, baud_rate)
# # time.sleep(1)  # Wait for the connection to initialize

# # # Function to send data to Arduino
# # def send_data(data):
# #     ser.write(data.encode())  # Send data as bytes

# # # Example usage
# # while True:
# #     data = input("Enter data to send (type 'q' to quit): ")
# #     if data.lower() == 'q':
# #         break
    
# #     send_data(data)

# #     # # Read response from Arduino
# #     if ser.in_waiting > 0:
# #         response = ser.readline().decode("utf-8").strip()
# #         print(f"Received: {response}")

# # # Close serial connection
# # ser.close()
# # print("Serial connection closed")

# # Importing Libraries 
# import serial 
# import time 
# arduino = serial.Serial(port=arduino_port, baudrate=9600, timeout=.1) 

# def write_read(x): 
#     arduino.write(x.encode('utf-8'))
#     time.sleep(0.05) 
#     data = arduino.readline() 
#     return data 

# while True: 
#     # num = input("Enter a number: ") # Taking input from user 
#     # value = write_read(num) 
#     # print(value) # printing the value 
#     arduino.write('Hello'.encode('utf-8'))
    
#     if arduino.in_waiting > 0:
#         response = arduino.readline().decode("utf-8").strip()
#         print(f"Received: {response}")
    
