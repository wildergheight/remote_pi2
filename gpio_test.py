from gpiozero import LED, Button
from signal import pause
from time import sleep

# Define your hardware based on GPIO pin numbers
led_red = LED(23)
led_yellow = LED(24)
led_green = LED(25)

switch_1 = Button(5)
switch_2 = Button(6)

print("Starting Hardware Test...")

# 1. Quick LED Sequence Test
print("Testing LEDs...")
leds = [led_red, led_yellow, led_green]

for led in leds:
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.2)

print("LED Test Complete.")

# 2. Interactive Switch Test
# Define what happens when buttons are pressed
def switch_one_pressed():
    print("Switch 1 (GPIO 5) pressed! Toggling Red LED.")
    led_red.toggle()

def switch_two_pressed():
    print("Switch 2 (GPIO 6) pressed! Toggling Green LED.")
    led_green.toggle()

switch_1.when_pressed = switch_one_pressed
switch_2.when_pressed = switch_two_pressed

print("---")
print("Interactive mode active:")
print("Press Switch 1 to toggle Red LED")
print("Press Switch 2 to toggle Green LED")
print("Press Ctrl+C to exit")

pause()
