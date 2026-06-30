import smbus
import time

# I2C 통신을 위한 버스 모듈을 초기화함 (라즈베리파이 기본 버스 1 사용)
bus = smbus.SMBus(1)

# PCF8591 장치의 I2C 주소 및 데이터 자동 증가 명령어 할당
i2c_address = 0x48
command = 0x44

def calculate_percentage(analog_value):
    """
    0에서 255 사이의 아날로그 원본 값을 100분율(%) 단위로 변환함.
    """
    # 최대값 255를 기준으로 비율을 계산하고 100을 곱하여 퍼센트를 산출함
    percent = (analog_value / 255.0) * 100.0
    # 소수점 둘째 자리까지 반올림하여 반환함
    return round(percent, 2)

try:
    # 지속적인 센서 데이터 획득을 위해 무한 반복문을 사용함
    while True:
        # 5바이트 블록 데이터를 한 번에 읽어옴
        # 인덱스 0: 이전 더미 데이터
        # 인덱스 1: CH0 (AIN0)
        # 인덱스 2: CH1 (AIN1)
        # 인덱스 3: CH2 (AIN2)
        # 인덱스 4: CH3 (AIN3)
        sensor_data = bus.read_i2c_block_data(i2c_address, command, 5)
        
        # CH1과 CH2에 해당하는 배열의 원본 데이터를 추출함
        ch1_raw = sensor_data[2]
        ch2_raw = sensor_data[3]
        
        # 추출한 원본 데이터를 퍼센트 수치로 변환함
        ch1_percent = calculate_percentage(ch1_raw)
        ch2_percent = calculate_percentage(ch2_raw)
        
        # 변환된 각 채널의 퍼센트 값을 화면에 출력함
        print("CH1 퍼센트: {:.2f}% | CH2 퍼센트: {:.2f}%".format(ch1_percent, ch2_percent))
        print("-" * 35)
        
        # 시스템 과부하를 방지하기 위해 1초 대기함 (동기식 지연)
        time.sleep(1)

except KeyboardInterrupt:
    # 사용자가 키보드로 프로그램 종료(Ctrl+C)를 요청하면 안전하게 종료함
    pass