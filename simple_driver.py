import serial

import time

import sys

import termios

import tty

import select



SERIAL_PORT = '/dev/ttyUSB0'

BAUD_RATE = 115200



def get_key_nonblocking():

    dr, _, _ = select.select([sys.stdin], [], [], 0)

    if dr:

        return sys.stdin.read(1)

    return None



def send_cmd(esp32, right, left):

    cmd = f"R:{right:.2f},L:{left:.2f}\n"

    esp32.write(cmd.encode("utf-8"))



def smooth_turn(esp32, direction):

    """direction: 'left' or 'right'"""

    # Step 1: small forward roll to get momentum

    send_cmd(esp32, -1.0, 1.0)

    time.sleep(0.25)

    send_cmd(esp32, -1.0, 1.0)

    time.sleep(0.25)



    # Step 2: apply gentle bias

    if direction == 'left':

        send_cmd(esp32, -0.85, 1.0)

        print("Smooth Left Turn")

    else:

        send_cmd(esp32, -1.0, 0.85)

        print("Smooth Right Turn")



def main():

    print("--- Simple Python Cart Controller ---")

    print("Controls: w/s/a/d = move, space = stop, q = quit")

    print("------------------------------------")



    try:

        esp32 = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0)

        print(f"Connected to {SERIAL_PORT}")

        time.sleep(2)

    except serial.SerialException as e:

        print(f"Error: {e}")

        return



    old_settings = termios.tcgetattr(sys.stdin)

    tty.setcbreak(sys.stdin.fileno())



    try:

        running = True

        while running:

            char = get_key_nonblocking()

            if char:

                if char == 'w':

                    print("Forward")

                    send_cmd(esp32, -1.0, 1.0)

                elif char == 's':

                    print("Reverse")

                    send_cmd(esp32, 1.0, -1.0)

                elif char == 'a':

                    smooth_turn(esp32, 'left')

                elif char == 'd':

                    smooth_turn(esp32, 'right')

                elif char == ' ':

                    print("STOP")

                    send_cmd(esp32, 0.0, 0.0)

                elif char == 'q':

                    print("Quitting...")

                    running = False



            while esp32.in_waiting > 0:

                incoming = esp32.readline().decode('utf-8', errors='ignore').strip()

                if incoming:

                    print(f"[ESP32] {incoming}")



            time.sleep(0.01)



    except KeyboardInterrupt:

        print("\nStopping...")

    finally:

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        send_cmd(esp32, 0.0, 0.0)

        esp32.close()

        print("Serial port closed.")



if __name__ == "__main__":

    main()
