import RPi.GPIO as GPIO
import time

# 스위치 핀 번호 설정 (BCM 모드 기준)
# 변수(Variable)는 데이터를 저장하는 공간입니다.
SW1_PIN = 4
SW2_PIN = 17
SW3_PIN = 18
SW4_PIN = 22
SWITCH_PINS = [SW1_PIN, SW2_PIN, SW3_PIN, SW4_PIN]

# 모터 핀 번호 설정 (BCM 모드 기준)
# 스위치 핀과 중복되지 않도록 다른 핀 번호를 사용합니다.
MOTOR_PIN1 = 12
MOTOR_PIN2 = 16
MOTOR_PIN3 = 20
MOTOR_PIN4 = 21
MOTOR_PINS = [MOTOR_PIN1, MOTOR_PIN2, MOTOR_PIN3, MOTOR_PIN4]

# 스텝 모터의 구동 신호 패턴입니다.
# 리스트(List)를 사용하여 4단계의 신호를 순서대로 묶어 저장합니다.
STEP_SIGNALS = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

def setup_gpio():
    # GPIO 핀 번호 체계를 BCM으로 설정합니다.
    GPIO.setmode(GPIO.BCM)
    
    # 스위치 핀을 입력(IN) 모드로 설정하여 전기 신호를 읽어들일 준비를 합니다.
    GPIO.setup(SWITCH_PINS, GPIO.IN)
    
    # 모터 핀을 출력(OUT) 모드로 설정하고 초기 상태를 신호 없음(LOW)으로 만듭니다.
    GPIO.setup(MOTOR_PINS, GPIO.OUT, initial=GPIO.LOW)

def rotate_motor(direction, steps, delay_time):
    # 매개변수(Parameter)로 받은 방향, 스텝 수, 대기 시간에 따라 모터를 제어합니다.
    for i in range(steps):
        if direction == "clockwise":
            # 시계 방향: 0부터 3까지 순서대로 신호를 보냅니다.
            for step_idx in range(4):
                for pin_idx in range(4):
                    GPIO.output(MOTOR_PINS[pin_idx], STEP_SIGNALS[step_idx][pin_idx])
                time.sleep(delay_time)
                
        elif direction == "counterclockwise":
            # 반시계 방향: 3부터 0까지 역순으로 신호를 보냅니다.
            for step_idx in range(3, -1, -1):
                for pin_idx in range(4):
                    GPIO.output(MOTOR_PINS[pin_idx], STEP_SIGNALS[step_idx][pin_idx])
                time.sleep(delay_time)

def stop_motor():
    # 모터의 모든 핀 출력을 LOW로 설정하여 회전을 멈추고 불필요한 전력 소모를 차단합니다.
    for pin in MOTOR_PINS:
        GPIO.output(pin, GPIO.LOW)

if __name__ == "__main__":
    setup_gpio()
    print("스위치 모터 제어 파이썬 프로그램 시작")
    
    try:
        # while True는 프로그램이 강제 종료될 때까지 무한히 반복하는 반복문입니다.
        while True:
            # 스위치 1번이 눌렸을 때 (입력이 1 즉 HIGH일 때)
            if GPIO.input(SW1_PIN) == GPIO.HIGH:
                print("스위치 1 눌림: 시계 방향 회전")
                rotate_motor("clockwise", 50, 0.002)
            
            # 스위치 2번이 눌렸을 때
            elif GPIO.input(SW2_PIN) == GPIO.HIGH:
                print("스위치 2 눌림: 반시계 방향 회전")
                rotate_motor("counterclockwise", 50, 0.002)
            
            # 스위치가 눌리지 않았을 때는 모터를 정지시킵니다.
            else:
                stop_motor()
                
            # CPU가 과부하에 걸리지 않도록 아주 짧은 시간(0.1초) 대기합니다.
            time.sleep(0.1)
            
    finally:
        # 예외가 발생하거나 프로그램이 종료될 때, 사용한 GPIO 핀을 안전하게 초기화합니다.
        GPIO.cleanup()