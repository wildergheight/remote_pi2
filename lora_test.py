import board
import busio
import digitalio
import struct
import adafruit_rfm9x
from time import sleep

# The format string '<If f h' means:
# < : Little-endian (Standard for ESP32/Pi)
# I : Unsigned Int (4 bytes) - Timestamp
# f : Float (4 bytes)        - Latitude
# f : Float (4 bytes)        - Longitude
# h : Short (2 bytes)        - Altitude
packet_format = "<Iffh"
tele_packet_format = "<Iffh"

# 1. Setup LEDs (GPIO numbers, not physical pins)
led_red = digitalio.DigitalInOut(board.D23)
led_yel = digitalio.DigitalInOut(board.D24)
led_grn = digitalio.DigitalInOut(board.D25)

val1 = 1.01

leds = [led_red, led_yel, led_grn]
for led in leds:
    led.direction = digitalio.Direction.OUTPUT

# 2. Setup LoRa Pins
CS = digitalio.DigitalInOut(board.D22)    # Physical Pin 15
RESET = digitalio.DigitalInOut(board.D26) # Physical Pin 37
EN = digitalio.DigitalInOut(board.D17)    # Physical Pin 11
EN.direction = digitalio.Direction.OUTPUT
EN.value = True

# 3. Initialize SPI and Radio
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    rfm9x.signal_bandwidth = 125000
    rfm9x.coding_rate = 5
    rfm9x.spreading_factor = 7
    rfm9x.enable_crc = True
    print("LoRa Receiver Active... Waiting for ESP32...")
    while True:
        # # Check for a packet (non-blocking, waits 0.5s)
        # packet = rfm9x.receive(timeout=1.0)
        
        # if packet is not None:
        #     # We got something! 
        #     # rssi = rfm9x.last_rssi

            
        #     if len(packet) == struct.calcsize(packet_format):
                
        #         timestamp, lat, lon, alt = struct.unpack(packet_format, packet)
        #         # lat, lon, alt = struct.unpack(packet_format, packet)
        #         print(f"--- New Data ---")
        #         print(f"Time: {timestamp}ms")
        #         print(f"GPS: {lat:.6f}, {lon:.6f}")
        #         print(f"Alt: {alt/100:.2f}m")
        #         print(f"RSSI: {rfm9x.last_rssi} dBm")
        #     else:
        #         print(f"Received unexpected packet size: {len(packet)}")
        #         print(f"Raw Hex: {packet.hex()}")
            
        #     # Visual Notification: Flash LEDs
        #     # for _ in range(2):
        #     #     for led in leds: led.value = True
        #     #     sleep(0.1)
        #     #     for led in leds: led.value = False
        #     #     sleep(0.1)
            
        #     # NOW: Prepare the reply
        #     # We only pack the 14 bytes of actual data
        #     sleep(0.1)
        #     print("Sending Reply")
        #     reply_data = struct.pack(tele_packet_format, 1, 12.38, 26.78, 99)
            
        #     # This function sends the 4-byte header + our 14-byte payload
        #     rfm9x.send(reply_data)
        #     print("Response sent back to ESP32")
        print(f"Sending Reply: {val1}")
        reply_data = struct.pack(tele_packet_format, 1, val1, 26.78, 99)

        
        
        # This function sends the 4-byte header + our 14-byte payload
        rfm9x.send(reply_data)
        print("Response sent back to ESP32")
        val1 += 1
        sleep(1.5)
                    

except Exception as e:
    print(f"Error: {e}")
finally:
    for led in leds: led.value = False
