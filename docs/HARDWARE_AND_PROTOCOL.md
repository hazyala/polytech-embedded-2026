# 장비와 파일별 실행 경계

## 룰렛

`roulette_game.py`는 BCM switch 4, step pins 16/20/21/26, RED LED 5, GREEN LED 6과 SMBus(1)의 ADC 0x48/command 0x44를 사용한다. LCD driver와 Tkinter UI를 함께 초기화한다. 숫자·반 칸 위치를 `roulette_position.txt`에 저장하고 복원한다. 실제 모터 보정값은 `STEPS_PER_SLOT`, `HALF_STEP_PATTERN` 상수를 확인한다.

## 거리 전송

`server_psd.py`는 TCP 10000에서 한 client를 받아 sender thread로 데이터를 보낸다. PCF8591 ADC block의 값을 전압으로 바꾸고 `29.988 * voltage**-1.173`을 적용한다. `PSD,<값>\n` UTF-8 데이터를 0.3초 간격으로 전송한다. 이는 설정된 전송 간격이며 실측 latency가 아니다.

`server.py`도 TCP 10000을 사용하므로 동시에 bind할 수 없다. `client.py`의 서버 주소는 192.168.25.209:10000이며 원래 실습 네트워크 값이다. TCP stream의 메시지 경계와 GUI 갱신 처리는 각 client 구현을 확인한다. HTTP endpoint나 WebSocket이 아니다.

## 카메라·모델

`apple_banana.py`는 `classfication.h5`와 `classfication.txt`를 현재 디렉터리에서 읽고 LCD를 초기화한다. `mytf_example_cam.py`는 `keras_model.h5`, `labels.txt`, `http://raspberryAI:8090/?action=stream`을 사용한다. 프레임을 224×224로 변환하고 픽셀을 127.0으로 나누어 -1을 빼는 전처리를 한다.

일부 예제는 `Image.ANTIALIAS` 등 과거 Pillow API를 사용한다. 고정 requirements가 없어 최신 라이브러리 설치만으로 호환된다고 보장할 수 없다. 학습 데이터·모델 성능은 이 코드만으로 확인되지 않는다.

[룰렛](../roulette_game.py) · [PSD 서버](../server_psd.py) · [PSD client](../psd_client.py) · [카메라 추론](../mytf_example_cam.py)
