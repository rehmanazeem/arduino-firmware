import serial

# Replace '/dev/cu.HC-05' with the correct port for your HC-05
port = '/dev/cu.HC-05'  # Update this with the correct port
baud_rate = 9600  # Default baud rate for HC-05

try:
    # Open the serial connection
    bluetooth = serial.Serial(port, baud_rate, timeout=1)
    print(f"Connected to {port} at {baud_rate} baud rate.")

    print("Enter messages to send to HC-05 (type 'exit' to quit):")
    while True:
        # Get user input for the message
        message = input(">>> ").strip()
        if message.lower() == 'exit':
            break

        # Send the message to HC-05
        bluetooth.write((message + '\r\n').encode('utf-8'))
        print(f"Sent: {message}")

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    # Close the connection when done
    if 'bluetooth' in locals() and bluetooth.is_open:
        bluetooth.close()
        print("Connection closed.")