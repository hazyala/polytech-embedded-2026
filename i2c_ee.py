import smbus
import time

# I2C 버스 설정 (라즈베리파이 기본: 1)
bus = smbus.SMBus(1)

# PCF8591 주소
address = 0x48

# 채널별 컨트롤 바이트
control_bytes = [
    0x40,  # AIN0
    0x41,  # AIN1
    0x42,  # AIN2
    0x43   # AIN3
]

def read_channel(control):
    # 컨트롤 바이트 전송
    bus.write_byte(address, control)
    
    # dummy read
    bus.read_byte(address)
    
    # 실제 데이터 읽기 (0~255)
    value = bus.read_byte(address)
    return value

while True:
    values = []
    
    for ctrl in control_bytes:
        val = read_channel(ctrl)
        values.append(val)
    
    # 첫 번째 채널(AIN0)을 퍼센트로 변환
    ch0_percent = (values[0] / 255.0) * 100.0
    
    print("채널 값:", values)
    print("CH0 퍼센트: {:.2f}%".format(ch0_percent))
    print("-" * 30)
    
    time.sleep(1)