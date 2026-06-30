import time
from bready.autovehicle_utils.autovehicleControlClient import AutoVehicleControlClient

# 차량 제어 서버 주소 및 포트 설정 함 [cite: 383, 877]
# 로컬 호스트(127.0.0.1) 및 포트 8886 사용 함
vehicle_server = AutoVehicleControlClient("127.0.0.1", 8886)
time.sleep(3) # 서버 연결 안정화를 위해 대기 함

def move_servo(angle):
    """
    서보모터의 각도를 제어하는 함수
    매개변수: angle (0 ~ 180 사이의 정수) 
    """
    print(f"모터를 {angle}도로 이동합니다.")
    # 조향 장치의 각도를 설정 함 [cite: 884]
    vehicle_server.controlDirection(int(angle))
    # 설정된 데이터를 서버로 전송 함 [cite: 885]
    vehicle_server.sendData()
    time.sleep(1) # 모터가 이동할 시간을 줌

try:
    print("서보모터 제어 테스트를 시작합니다.")
    
    # 공주마마께서 요청하신 25도 방향으로 이동 함
    move_servo(25)
    
    # 반복 동작 수행 (0 -> 180 -> 90)
    move_servo(0)   # 왼쪽 끝
    move_servo(180) # 오른쪽 끝
    move_servo(90)  # 정중앙 (영점) [cite: 750, 890]

except KeyboardInterrupt:
    # 사용자가 강제 종료(Ctrl+C)했을 때 예외 처리 함
    print("사용자에 의해 중단되었습니다.")

finally:
    # 서버 연결을 안전하게 종료 함 [cite: 899, 900]
    vehicle_server.disconnect()
    vehicle_server.close()
    print("프로그램 종료 함.")