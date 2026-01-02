import serial
import time

# On Raspberry Pi, /dev/serial0 is the default alias for the GPIO UART
# The standard baud rate for most GPS modules is 9600
port = "/dev/serial0"
baud = 230400

try:
    ser = serial.Serial(port, baudrate=baud, timeout=1)
    print(f"Connected to {port} at {baud} baud.")
    print("Waiting for data... (Press Ctrl+C to stop)")
    print("-" * 40)

    while True:
        if ser.in_waiting > 0:
            # Read a line of data from the GPS
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line:
                print(f"Received: {line}")
        time.sleep(0.1)

except serial.SerialException as e:
    print(f"Error: Could not open serial port {port}: {e}")
except KeyboardInterrupt:
    print("\nTest stopped by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
