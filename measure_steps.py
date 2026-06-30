import RPi.GPIO as GPIO
import time

STEP_IN1 = 16
STEP_IN2 = 20
STEP_IN3 = 21
STEP_IN4 = 26

pins = [STEP_IN1, STEP_IN2, STEP_IN3, STEP_IN4]

GPIO.setmode(GPIO.BCM)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

FULL_STEP = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
]

step_index = 0
step_count = 0


def step_motor_once():
    global step_index

    signal = FULL_STEP[step_index]

    for pin, value in zip(pins, signal):
        GPIO.output(pin, value)

    step_index = (step_index + 1) % 4


try:

    print()
    print("====================================")
    print("스텝 측정 모드")
    print("현재 숫자를 정확히 1에 맞춰주세요.")
    print("준비되면 엔터")
    print("====================================")
    input()

    print()
    print("숫자가 정확히 2가 되는 순간 ENTER")
    print()

    start_time = time.time()

    while True:

        step_motor_once()
        step_count += 1

        if step_count % 10 == 0:
            print(f"현재 스텝: {step_count}", end="\r")

        time.sleep(0.01)

        # 엔터 입력 체크
        import select
        import sys

        if select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()
            break

    print()
    print("====================================")
    print(f"1 → 2 이동 스텝 수 = {step_count}")
    print("====================================")

finally:

    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

    GPIO.cleanup()