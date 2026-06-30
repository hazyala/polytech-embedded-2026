import RPi.GPIO as GPIO
import time

# 1. 핀 번호 및 초기 설정 (BCM 모드) [cite: 165]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 모터 번지수 (마마의 작동 코드 기준) [cite: 330, 331]
MOTOR_P = 19
MOTOR_M = 13

# 스위치 번지수 (비급 16페이지 기준) [cite: 691-693]
SW1_FORWARD = 4   # 정회전
SW2_BACKWARD = 17 # 역회전
SW3_STOP = 18     # 정지

def setup_gpio():
    # 모터 핀 출력 설정 [cite: 283]
    GPIO.setup(MOTOR_P, GPIO.OUT)
    GPIO.setup(MOTOR_M, GPIO.OUT)
    
    # 스위치 설정: 평소에 1을 유지하도록 내부 풀업(PUD_UP) 저항을 사용하옵니다. [cite: 282]
    GPIO.setup(SW1_FORWARD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SW2_BACKWARD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SW3_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def stop_motor():
    # 모든 신호를 끊어 정지시키옵니다. [cite: 340]
    GPIO.output(MOTOR_P, GPIO.LOW)
    GPIO.output(MOTOR_M, GPIO.LOW)
    print("상태: 모터 정지")

def rotate_forward():
    # 명하신 대로 시작 전 정지부터 하옵니다! 
    stop_motor()
    time.sleep(0.1)
    GPIO.output(MOTOR_P, GPIO.HIGH)
    GPIO.output(MOTOR_M, GPIO.LOW)
    print("상태: 모터 정회전 (Clockwise)")

def rotate_backward():
    # 역회전 시에도 예우를 갖추어 정지시킨 후 돌리옵니다. 
    stop_motor()
    time.sleep(0.1)
    GPIO.output(MOTOR_P, GPIO.LOW)
    GPIO.output(MOTOR_M, GPIO.HIGH)
    print("상태: 모터 역회전 (Counter Clockwise)")

if __name__ == "__main__":
    setup_gpio()
    stop_motor()
    print("DC 모터 제어 시작 (스위치를 누르면 0이 되는 액티브 로우 방식)")

    try:
        while True:
            # 스위치 값이 0(LOW)일 때가 마마께서 누르신 상태이옵니다! [cite: 288]
            if GPIO.input(SW1_FORWARD) == GPIO.LOW:
                rotate_forward()
                time.sleep(0.3)

            elif GPIO.input(SW2_BACKWARD) == GPIO.LOW:
                rotate_backward()
                time.sleep(0.3)

            elif GPIO.input(SW3_STOP) == GPIO.LOW:
                stop_motor()
                time.sleep(0.3)

            time.sleep(0.05)

    except KeyboardInterrupt:
        GPIO.cleanup() # 리소스 반납 [cite: 290]
        print("\n프로그램 종료")