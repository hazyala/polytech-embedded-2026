import socket
import sys
import time
import RPi.GPIO as GPIO

BUZZER_PIN = 12
HOST = ""
PORT = 10000

SCALE = {
    "do": 261,
    "re": 294,
    "mi": 330,
    "fa": 349,
    "sol": 392,
    "la": 440,
    "ti": 493
}


class BuzzerServer:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)

        self.pwm = GPIO.PWM(BUZZER_PIN, 100)
        self.pwm.start(0)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def play_note(self, note):
        if note not in SCALE:
            print(f"invalid note: {note}")
            return

        frequency = SCALE[note]
        self.pwm.ChangeFrequency(frequency)
        self.pwm.ChangeDutyCycle(50)

        print(f"RECEIVE Message >> [Sensor]: buzzer [Value]: {note}")

        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(0)

    def run(self):
        try:
            server_address = (HOST, PORT)
            self.sock.bind(server_address)
            self.sock.listen(1)

            print(f"The Server is waiting. IP: {server_address[0]} PORT: {server_address[1]}")
            print("Waiting for Client access...")

            while True:
                connection, client_address = self.sock.accept()

                try:
                    print("Connection from", client_address)

                    while True:
                        data = connection.recv(4096)

                        if not data:
                            print("Disconnect")
                            break

                        msg_str = data.decode("utf-8").strip()
                        msg = msg_str.split(",")

                        if len(msg) != 2:
                            print(f"invalid command format: {msg_str}")
                            continue

                        device = msg[0].strip()
                        value = msg[1].strip()

                        if device == "buzzer":
                            self.play_note(value)
                        else:
                            print(f"unknown device: {device}")

                except Exception as err:
                    print(err)

                finally:
                    connection.close()

        except Exception as err:
            print(err)

        finally:
            print("Closing socket and cleanup GPIO")
            self.pwm.ChangeDutyCycle(0)
            self.pwm.stop()
            self.sock.close()
            GPIO.cleanup()


if __name__ == "__main__":
    try:
        server = BuzzerServer()
        server.run()

    except KeyboardInterrupt:
        print("Program force quit")
        GPIO.cleanup()
        sys.exit()