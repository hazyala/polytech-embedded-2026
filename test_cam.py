import cv2

# 백엔드 파라미터(cv2.CAP_FFMPEG)를 추가하여 스트리밍임을 명시함
url = 'http://127.0.0.1:8090/?action=stream'
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("서버에 연결할 수 없음. MJPG-streamer가 실행 중인지 확인 필요함.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없음.")
            break
            
        cv2.imshow("Stream Test", frame)
        
        if cv2.waitKey(33) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()