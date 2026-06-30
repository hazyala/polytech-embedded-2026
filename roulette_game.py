# roulette_game.py
from tkinter import *
import RPi.GPIO as GPIO
import smbus
import time
import random
import threading
import os
import I2C_LCD_driver

SW1 = 4
STEP_PINS = [16, 20, 21, 26]

RED_LED = 5
GREEN_LED = 6

ADC_ADDR = 0x48
ADC_COMMAND = 0x44

TOTAL_NUMBERS = 36
TOTAL_POSITIONS = 72
STEPS_PER_SLOT = 57
HALF_STEP_PATTERN = [28, 28]
half_step_index = 0
POSITION_FILE = "roulette_position.txt"

running = False
landing = False

target_number = random.randint(1, TOTAL_NUMBERS)
motor_value = 27.5
selected_value = None

speed_level = 1
result_text = "WAITING"

last_button_time = 0
step_index = 0

bus = smbus.SMBus(1)
lcd_lock = threading.Lock()
textLcd = I2C_LCD_driver.lcd()

FULL_STEP = [
    [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH]
]


def normalize_value(value):
    while value > 36.5:
        value -= 36
    while value < 1:
        value += 36
    return round(value, 1)


def format_value(value):
    value = normalize_value(value)
    if value == int(value):
        return str(int(value))
    return str(value)


def save_position(value):
    with open(POSITION_FILE, "w") as f:
        f.write(format_value(value))


def load_position():
    if not os.path.exists(POSITION_FILE):
        return 27.5

    try:
        with open(POSITION_FILE, "r") as f:
            value = float(f.read().strip())

        if 1 <= value <= 36.5 and (value * 10) % 5 == 0:
            return normalize_value(value)
    except:
        pass

    return 27.5


def lcd_message(line1="", line2=""):
    with lcd_lock:
        try:
            textLcd.lcd_clear()
            time.sleep(0.03)
            textLcd.lcd_display_string(str(line1)[:16], 1)
            textLcd.lcd_display_string(str(line2)[:16], 2)
        except Exception as e:
            print("LCD ERROR:", e)


def read_vr():
    try:
        bus.write_byte(ADC_ADDR, ADC_COMMAND)
        bus.read_byte(ADC_ADDR)
        return bus.read_byte(ADC_ADDR)
    except:
        return 0


def vr_to_level(value):
    level = int(value / 25.6) + 1
    return max(1, min(10, level))


def level_to_delay(level):
    delays = {
        1: 0.007,
        2: 0.006,
        3: 0.005,
        4: 0.004,
        5: 0.0035,
        6: 0.003,
        7: 0.0025,
        8: 0.002,
        9: 0.0016,
        10: 0.0013
    }
    return delays.get(level, 0.003)


def step_motor_once(delay=0.003):
    global step_index

    signal = FULL_STEP[step_index]

    for pin, value in zip(STEP_PINS, signal):
        GPIO.output(pin, value)

    step_index = (step_index - 1) % len(FULL_STEP)
    time.sleep(delay)


def stop_motor():
    for pin in STEP_PINS:
        GPIO.output(pin, GPIO.LOW)


def set_led(success=None):
    if success is True:
        GPIO.output(GREEN_LED, GPIO.HIGH)
        GPIO.output(RED_LED, GPIO.LOW)
    elif success is False:
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.HIGH)
    else:
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.LOW)


def spin_motor_loop():
    global speed_level, motor_value, half_step_index

    step_count = 0
    current_half_steps = HALF_STEP_PATTERN[half_step_index]

    while True:
        vr_value = read_vr()
        speed_level = vr_to_level(vr_value)

        if running and not landing:
            step_motor_once(level_to_delay(speed_level))
            step_count += 1

            if step_count >= current_half_steps:
                step_count = 0

                motor_value = normalize_value(motor_value + 0.5)
                save_position(motor_value)

                half_step_index = (half_step_index + 1) % len(HALF_STEP_PATTERN)
                current_half_steps = HALF_STEP_PATTERN[half_step_index]
        else:
            time.sleep(0.02)


def check_result():
    global result_text

    if motor_value == target_number:
        result_text = "SUCCESS"
        set_led(True)
        lcd_message("SUCCESS!", f"T:{target_number} S:{format_value(motor_value)}")
    else:
        result_text = "FAIL"
        set_led(False)
        lcd_message("FAIL!", f"T:{target_number} S:{format_value(motor_value)}")


def toggle_game(channel=None):
    global running, target_number, result_text
    global last_button_time, selected_value

    now = time.time()

    if now - last_button_time < 0.4:
        return

    last_button_time = now

    if landing:
        return

    if not running:
        running = True
        selected_value = None
        target_number = random.randint(1, TOTAL_NUMBERS)
        result_text = "RUNNING"
        set_led(None)
        lcd_message(f"TARGET : {target_number}", "Running...")
    else:
        running = False
        selected_value = motor_value
        result_text = f"SELECT {format_value(selected_value)}"
        lcd_message(f"SELECT : {format_value(selected_value)}", "Checking...")
        check_result()


class RouletteGUI:
    def __init__(self, master):
        self.master = master
        master.title("Roulette Challenge")
        master.geometry("740x760+100+100")
        master.resizable(False, False)
        master.configure(bg="#1E1E2E")

        Label(
            master,
            text="ROULETTE CHALLENGE",
            font=("Arial", 24, "bold"),
            bg="#1E1E2E",
            fg="#FFFFFF"
        ).pack(pady=20)

        self.card = Frame(master, bg="#313244", width=620, height=510)
        self.card.pack(pady=10)
        self.card.pack_propagate(False)

        self.target_label = Label(
            self.card,
            text="TARGET -",
            font=("Arial", 20, "bold"),
            bg="#313244",
            fg="#F9E2AF"
        )
        self.target_label.pack(pady=25)

        self.current_label = Label(
            self.card,
            text="-",
            font=("Arial", 78, "bold"),
            bg="#313244",
            fg="#89B4FA"
        )
        self.current_label.pack(pady=5)

        self.selected_label = Label(
            self.card,
            text="SELECTED -",
            font=("Arial", 18, "bold"),
            bg="#313244",
            fg="#FFFFFF"
        )
        self.selected_label.pack(pady=10)

        self.speed_label = Label(
            self.card,
            text="SPEED LEVEL -",
            font=("Arial", 17),
            bg="#313244",
            fg="#FFFFFF"
        )
        self.speed_label.pack(pady=8)

        self.motor_label = Label(
            self.card,
            text="MOTOR POSITION -",
            font=("Arial", 17),
            bg="#313244",
            fg="#BAC2DE"
        )
        self.motor_label.pack(pady=8)

        self.result_label = Label(
            self.card,
            text="RESULT WAITING",
            font=("Arial", 22, "bold"),
            bg="#313244",
            fg="#FFFFFF"
        )
        self.result_label.pack(pady=16)

        Label(
            master,
            text="Switch1 = START / STOP     VR = SPEED LEVEL 1~10",
            font=("Arial", 13),
            bg="#1E1E2E",
            fg="#BAC2DE"
        ).pack(pady=10)

        Button(
            master,
            text="종료",
            width=18,
            height=2,
            command=self.close
        ).pack(pady=8)

        self.update_gui()

    def update_gui(self):
        self.target_label.config(text=f"TARGET  {target_number}")
        self.current_label.config(text=format_value(motor_value))

        if selected_value is None:
            self.selected_label.config(text="SELECTED  -")
        else:
            self.selected_label.config(text=f"SELECTED  {format_value(selected_value)}")

        self.speed_label.config(text=f"SPEED LEVEL  {speed_level}")
        self.motor_label.config(text=f"MOTOR POSITION  {format_value(motor_value)}")

        if result_text == "SUCCESS":
            self.result_label.config(text="RESULT  SUCCESS", fg="#A6E3A1")
        elif result_text == "FAIL":
            self.result_label.config(text="RESULT  FAIL", fg="#F38BA8")
        elif running:
            self.result_label.config(text="RESULT  RUNNING", fg="#A6E3A1")
        else:
            self.result_label.config(text=f"RESULT  {result_text}", fg="#FFFFFF")

        self.master.after(50, self.update_gui)

    def close(self):
        stop_motor()
        set_led(None)
        GPIO.cleanup()
        self.master.destroy()


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for pin in STEP_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    set_led(None)

    motor_value = load_position()

    lcd_message("Roulette Game", "Press SW1")

    GPIO.add_event_detect(
        SW1,
        GPIO.FALLING,
        callback=toggle_game,
        bouncetime=300
    )

    t = threading.Thread(target=spin_motor_loop)
    t.daemon = True
    t.start()

    root = Tk()
    app = RouletteGUI(root)

    try:
        root.mainloop()
    finally:
        stop_motor()
        set_led(None)
        GPIO.cleanup()