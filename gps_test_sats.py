import serial
from micropyGPS import MicropyGPS

# Setup serial and parser
ser = serial.Serial("/dev/serial0", baudrate=230400, timeout=1)
my_gps = MicropyGPS()

print("Waiting for GPS Lock...")

try:
    while True:
        if ser.in_waiting > 0:
            sentence = ser.readline().decode('utf-8', errors='replace')
            for char in sentence:
                my_gps.update(char)
            
            # Only print once we have a valid fix
            if my_gps.satellites_in_use > 0:
                print(f"Sats: {my_gps.satellites_in_use} | "
                      f"Lat: {my_gps.latitude[0]}°{my_gps.latitude[1]}' {my_gps.latitude[2]} | "
                      f"Lon: {my_gps.longitude[0]}°{my_gps.longitude[1]}' {my_gps.longitude[2]} | "
                      f"Alt: {my_gps.altitude}m")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
