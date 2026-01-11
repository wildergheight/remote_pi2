import board
import busio
import digitalio
import struct
import adafruit_rfm9x
from time import sleep

# Global configurations
PACKET_FORMAT = "<Iddh" 
FREQ = 433.0 # Or 915.0 depending on your hardware

def setup_rfm9x():
    """Initializes the SPI bus and RFM9x radio module."""
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs = digitalio.DigitalInOut(board.D22)
    reset = digitalio.DigitalInOut(board.D26)
    
    # Enable Pin (if your board uses one, like the one in your original code)
    en = digitalio.DigitalInOut(board.D17)
    en.direction = digitalio.Direction.OUTPUT
    en.value = True

    radio = adafruit_rfm9x.RFM9x(spi, cs, reset, FREQ)
    
    # Critical: These must match the ESP32 exactly
    radio.signal_bandwidth = 125000
    radio.coding_rate = 5
    radio.spreading_factor = 7
    radio.enable_crc = True
    
    return radio

def handle_lora_traffic(radio, current_val):
    """
    Listens for a packet and sends a reply if valid data is received.
    Returns the updated val1.
    """
    # Non-blocking listen (100ms timeout keeps the loop snappy)
    packet = radio.receive(timeout=0.1)
    
    if packet is not None:
        expected_size = struct.calcsize(PACKET_FORMAT)
        
        if len(packet) == expected_size:
            timestamp, lat, lon, alt = struct.unpack(PACKET_FORMAT, packet)
            print(f"Received from ESP32: Lat {lat}, Lon {lon}")

            # --- THE HANDSHAKE ---
            # Turnaround delay for ESP32 hardware transition
            sleep(0.1) 
            
            print(f"Sending reply: {current_val}")
            reply_data = struct.pack(PACKET_FORMAT, 1, current_val, 26.78, 99)
            radio.send(reply_data)
            
            return current_val + 1.0
        else:
            print(f"Unexpected packet size: {len(packet)} (Expected {expected_size})")
            
    return current_val

# --- MAIN EXECUTION ---
rfm9x = setup_rfm9x()
val1 = 1.0

print("Responder Ready...")

while True:
    val1 = handle_lora_traffic(rfm9x, val1)
    
    # You can add other Pi tasks here (logging to CSV, etc.)
    # without blocking for long periods.
    sleep(0.01)