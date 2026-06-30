import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
MOTOR_P=19
MOTOR_M=13

if __name__ == "__main__":
    GPIO.setup(MOTOR_P, GPIO.OUT)
    GPIO.setup(MOTOR_M, GPIO.OUT)
    try:
        while(True):
            GPIO.output(MOTOR_P, GPIO.HIGH)
            GPIO.output(MOTOR_M, GPIO.LOW)
            print("Clock Wise")
            time.sleep(1)
        
            GPIO.output(MOTOR_P, GPIO.LOW)
            GPIO.output(MOTOR_M, GPIO.LOW)
            print("Stop")
            time.sleep(1)
        
            GPIO.output(MOTOR_P, GPIO.LOW)
            GPIO.output(MOTOR_M, GPIO.HIGH)
            print("Count Clock Wise")
            time.sleep(1)
 
            GPIO.output(MOTOR_P, GPIO.LOW)
            GPIO.output(MOTOR_M, GPIO.LOW)
            print("Stop")
            time.sleep(1)
        
    except KeyboardInterrupt:
    #finally:
        GPIO.cleanup()