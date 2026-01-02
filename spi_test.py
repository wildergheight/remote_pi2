import board
import busio
import digitalio
import adafruit_rfm9x

# 1. Setup Pins based on your wiring
# Note: board.DXX refers to the GPIO number, not the physical pin number.
CS = digitalio.DigitalInOut(board.D22)    # Physical Pin 15 is GPIO 22
RESET = digitalio.DigitalInOut(board.D26) # Physical Pin 37 is GPIO 26
# LORA_EN (Pin 11 / GPIO 17) needs to be pulled HIGH to power the board
EN = digitalio.DigitalInOut(board.D17)
EN.direction = digitalio.Direction.OUTPUT
EN.value = True

# 2. Initialize SPI bus
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# 3. Attempt to initialize the RFM95 radio
try:
    print("Attempting to connect to RFM95...")
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0) # Frequency in MHz
    print("LoRa Radio detected successfully!")
    
    # Check the chip version (standard for RFM95 is 0x12)
    print(f"Radio Version: {hex(rfm9x.version)}")
    
    # Try to send a test packet
    print("Sending test packet...")
    rfm9x.send(bytes("Hello World\r\n", "utf-8"))
    print("Packet sent!")

except Exception as e:
    print(f"Error: {e}")
    print("\nCheck your wiring!")
    print("Physical 15 -> GPIO 22 (CS)")
    print("Physical 37 -> GPIO 26 (RST)")
    print("Physical 11 -> GPIO 17 (EN)")
