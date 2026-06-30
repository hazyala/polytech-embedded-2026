from tkinter import *
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np
from tensorflow.keras.models import load_model

import I2C_LCD_driver

# =========================
# LCD 초기화
# =========================
lcd = I2C_LCD_driver.lcd()

# 마지막 출력값 저장
last_label = ""

# =========================
# 모델 로드
# =========================
model = load_model('classfication.h5')
model.summary()

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
size = (224, 224)

value = None


# =========================
# 라벨 읽기
# =========================
def readLabels():
    try:
        f = open('classfication.txt', 'r')

        list_labels = []

        while True:
            line = f.readline()

            if not line:
                break

            get_label = line.split(' ')
            get_label = get_label[1].split('\n')

            list_labels.append(get_label[0])

        f.close()

        return list_labels

    except Exception as e:
        print(e)
        return []


# =========================
# 카메라 프레임 처리
# =========================
def show_frame():

    global last_label

    imglabel = readLabels()

    ret, frame = cap.read()

    # 카메라 오류 처리
    if not ret:
        lmain.after(100, show_frame)
        return

    # OpenCV -> RGB
    processImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # AI 입력용
    recog = cv2.resize(processImage, (224, 224))

    # 화면 출력용
    displayImage = cv2.resize(processImage, (640, 480))
    displayImage = Image.fromarray(displayImage)
    displayImage = ImageTk.PhotoImage(image=displayImage)

    lmain.displayImage = displayImage
    lmain.configure(image=displayImage)

    # 모델 입력 처리
    recog = Image.fromarray(recog)

    recog = ImageOps.fit(
        recog,
        size,
        Image.ANTIALIAS
    )

    image_array = np.asarray(recog)

    normalized_image_array = (
        image_array.astype(np.float32) / 127.0
    ) - 1

    data[0] = normalized_image_array

    # =========================
    # AI 추론
    # =========================
    prediction = model.predict(data, verbose=0)

    obj = []

    for i in prediction[0]:
        v = int(float(i) * 1000) / 10
        obj.append(v)

    max_value = max(obj)
    max_index = obj.index(max_value)

    result_label = imglabel[max_index]

    # tkinter 출력
    value.set(imglabel[int(obj.index(max(obj)))]+" "+str(max(obj))+" %")

    # =========================
    # LCD 출력 (70% 이상일 때)
    # =========================
    if max_value >= 70:

        # 같은 값 반복 출력 방지
        if last_label != result_label:

            lcd.lcd_clear()

            # 1행 : 객체명
            lcd.lcd_display_string(
                "Object:",
                1
            )

            # 2행 : 결과
            lcd.lcd_display_string(
                result_label + " " + str(max_value) + "%",
                2
            )

            last_label = result_label

    # 반복
    lmain.after(1, show_frame)


# =========================
# GUI 시작
# =========================
try:

    root = Tk()

    root.title('Camera')
    root.geometry("640x520+10+10")

    lmain = Label(root)
    lmain.pack()

    value = StringVar()
    value.set("텍스트")

    msg = Label(
        root,
        background="yellow",
        textvariable=value
    )

    msg.pack()

    # 카메라 스트림
    cap = cv2.VideoCapture(
        "http://raspberryAI:8090/?action=stream"
    )

    # 카메라 연결 체크
    if not cap.isOpened():
        print("Camera stream failed")
        exit()

    show_frame()

    root.mainloop()

except KeyboardInterrupt:
    lcd.lcd_clear()
    print("Exit")