import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (BCM 방식 사용)
BUZZER_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 부저 제어를 위한 PWM 설정 (초기 주파수 440Hz)
pwm = GPIO.PWM(BUZZER_PIN, 440)

# 고양이의 춤 음계 주파수 정의
# D#5: 622, C#5: 554, F#4: 370, G#4: 415, A#4: 466, F4: 349
notes = [
    (622, 0.15), (554, 0.15), (370, 0.3), # 따라단
    (0, 0.1),                             # 쉼표
    (370, 0.15), (0, 0.1), (370, 0.15),   # 딴 딴
    (622, 0.15), (554, 0.15), (370, 0.3), # 따라단
    (0, 0.1),                             # 쉼표
    (370, 0.15), (0, 0.1), (370, 0.15),   # 딴 딴
    (622, 0.15), (554, 0.15), (415, 0.15), (370, 0.15), (311, 0.3) # 마무리
]

def play_cat_dance():
    """고양이의 춤 멜로디 재생 함수"""
    pwm.start(50) # 듀티 사이클 50%로 시작 함
    
    try:
        for freq, duration in notes:
            if freq == 0:
                pwm.ChangeDutyCycle(0) # 0Hz 대신 출력 정지 함
            else:
                pwm.ChangeDutyCycle(50) # 소리 출력 함
                pwm.ChangeFrequency(freq) # 주파수 변경 함
            
            time.sleep(duration) # 음 길이만큼 대기 함
            
            # 음 분리를 위해 잠시 멈춤
            pwm.ChangeDutyCycle(0)
            time.sleep(0.05)
            
    finally:
        pwm.stop()
        GPIO.cleanup() # GPIO 자원 해제 함

if __name__ == "__main__":
    print("고양이의 춤 연주를 시작합니다.")
    play_cat_dance()
    print("연주 종료.")