import RPi.GPIO as GPIO
import time

# 핀 번호 체계 설정 [cite: 690]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 비급에 적힌 스위치와 모터 번지수 [cite: 330, 331, 691, 692, 693]
SW_PINS = [4, 17, 18]
MOTOR_P = 19
MOTOR_M = 13

def setup():
    # 스위치 설정: 유령 신호를 막기 위해 PULL_DOWN 저항을 강제로 소환하옵니다!
    for pin in SW_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # 모터 설정 [cite: 334]
    GPIO.setup(MOTOR_P, GPIO.OUT)
    GPIO.setup(MOTOR_M, GPIO.OUT)

if __name__ == "__main__":
    setup()
    print("--- 스위치 상태 진단 시작 ---")
    try:
        while True:
            # 현재 스위치들의 상태를 읽어오옵니다 [cite: 699]
            sw1 = GPIO.input(4)
            sw2 = GPIO.input(17)
            sw3 = GPIO.input(18)
            
            # 화면에 현재 값을 출력하여 유령이 있는지 확인하옵니다 [cite: 700]
            print(f"SW1(정):{sw1} | SW2(역):{sw2} | SW3(정지):{sw3}", end="\r")
            
            # 만약 아무것도 안 눌렀는데 1이 뜬다면, pull_up_down 설정을 PUD_UP으로 바꿔야 하옵니다!
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup() # 리소스 반납 [cite: 703]