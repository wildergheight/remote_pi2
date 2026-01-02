import board
import busio
import digitalio
import struct
import adafruit_rfm9x
from time import sleep

# <Iffh is 14 bytes. The RFM9x library adds 4 bytes of header = 18 bytes total.
packet_format = "<Iffh" 

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
CS = digitalio.DigitalInOut(board.D22)
RESET = digitalio.DigitalInOut(board.D26)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)

# Critical: These must match the ESP32 exactly
rfm9x.signal_bandwidth = 125000
rfm9x.coding_rate = 5
rfm9x.spreading_factor = 7
rfm9x.enable_crc = True

print("Responder Ready...")

val1 = 1.0

while True:
    # Listen for the ESP32
    packet = rfm9x.receive(timeout=2.0)
    
    if packet is not None:
        print(f"Received request (Size: {len(packet)})")
        
        # Check size (RadioHead/CircuitPython strips the 4-byte header for you on receive)
        if len(packet) == struct.calcsize(packet_format):
            timestamp, lat, lon, alt = struct.unpack(packet_format, packet)
            print(f"Data from ESP32: Lat {lat}, Lon {lon}")

            # --- THE HANDSHAKE ---
            # Wait 100ms so the ESP32 has time to move from TX mode to RX mode
            sleep(0.1) 
            
            print(f"Sending reply: {val1}")
            reply_data = struct.pack(packet_format, 1, val1, 26.78, 99)
            rfm9x.send(reply_data)
            
            val1 += 1.0
        else:
            print("Received packet with unexpected length")