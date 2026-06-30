i2c_class.py 파일을 생성하고자 합니다. 

import smbus
import math

class read_i2c:
    bus = None
    i2c_address = None
    command = 0x44
    def __init__(self):
        self.bus = smbus.SMBus(1)
        ……
    def  vr_read():
        …..
        return VrValue
      ……..
class write_i2c:
    state = 0b00000000 
    bus = None

이영주
오후 3:21
실제 사용은 adc = read_i2c() write = write_i2c() print("VR:"+str(adc.vr_read()) +" %") print("CdS:"+str(adc.cds_read()) + " %") print("GAS:"+str(adc.gas_read())+ " GAS") print("Distance:"+str(adc.psd_read())+ " cm")

이영주
오후 3:24
ADC값은 8비트로 적용해주세요

이영주
오후 3:31
import smbus
import time


class read_i2c:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.i2c_address = 0x48

        self.VR_CMD  = 0x40
        self.CDS_CMD = 0x41
        self.GAS_CMD = 0x42
        self.PSD_CMD = 0x43

    def _read_channel(self, cmd):
        try:
            self.bus.write_byte(self.i2c_address, cmd)
            time.sleep(0.02)

            # ✅ 8비트 데이터 읽기
            raw = self.bus.read_byte(self.i2c_address)

            return raw  # 0 ~ 255

        except Exception as e:
            print("I2C Read Error:", e)
            return 0

    def vr_read(self):
        raw = self._read_channel(self.VR_CMD)
        return round((raw / 255.0) * 100, 2)

    def cds_read(self):
        raw = self._read_channel(self.CDS_CMD)
        return round((raw / 255.0) * 100, 2)

    def gas_read(self):
        raw = self._read_channel(self.GAS_CMD)
        return raw  # 필요 시 ppm 변환 가능

    def psd_read(self):
        raw = self._read_channel(self.PSD_CMD)

        if raw == 0:
            return 0

        distance = 29.988 * math.pow(raw, -1.173)
        return round(distance, 2)


class write_i2c:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.i2c_address = 0x20
        self.state = 0b00000000

    def On(self, cmd):
        # LED 켜기
        self.state = self.state | cmd
        self.bus.write_byte(self.i2c_address, self.state)

    def Off(self, cmd):
        # LED 끄기
        self.state = self.state & (~cmd)
        self.bus.write_byte(self.i2c_address, self.state)

이영주
오후 4:05
import smbus
import time
import math

class read_i2c:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.i2c_address = 0x48

        self.VR_CMD  = 0x40
        self.CDS_CMD = 0x41
        self.GAS_CMD = 0x42
        self.PSD_CMD = 0x43

    def _read_channel(self, cmd):
        try:
            self.bus.write_byte(self.i2c_address, cmd)
            time.sleep(0.02)

            self.bus.read_byte(self.i2c_address)
            # ✅ 8비트 데이터 읽기
            raw = self.bus.read_byte(self.i2c_address)

            return raw  # 0 ~ 255

        except Exception as e:
            print("I2C Read Error:", e)
            return 0

    def vr_read(self):
        raw = self._read_channel(self.VR_CMD)
        return round((raw / 255.0) * 100, 2)

    def cds_read(self):
        raw = self._read_channel(self.CDS_CMD)
        return round((raw / 255.0) * 100, 2)

    def gas_read(self):
        raw = self._read_channel(self.GAS_CMD)
        return raw  # 필요 시 ppm 변환 가능

    def psd_read(self):
        raw = self._read_channel(self.PSD_CMD)

        if raw == 0:
            return 0
            
        raw = (raw / 255.0 * 3.3) * 3 / 2
        distance = 29.988 * math.pow(raw, -1.173)
        return round(distance, 2)


class write_i2c:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.i2c_address = 0x20
        self.state = 0b00000000

    def On(self, cmd):
        # LED 켜기
        self.state = self.state | cmd
        self.bus.write_byte(self.i2c_address, self.state)

    def Off(self, cmd):
        # LED 끄기
        self.state = self.state & (~cmd)
        self.bus.write_byte(self.i2c_address, self.state)

이영주
오후 4:08
from i2c_class import read_i2c
from i2c_class import write_i2c
import I2C_LCD_driver
import time
import math

RED_LED   = 0b00000001
GREEN_LED = 0b00000010
BLUE_LED  = 0b00000100
RELAY_1   = 0b00010000
RELAY_2   = 0b00100000

textLcd = I2C_LCD_driver.lcd()
textLcd.lcd_display_string("KOPO AISW", 1)
textLcd.lcd_display_string("I2C_BUS TEST", 2)

adc = read_i2c()
write = write_i2c()


print("VR:"+str(adc.vr_read()) +" %")
print("CdS:"+str(adc.cds_read()) + " %")
print("GAS:"+str(adc.gas_read())+ " GAS")
print("Distance:"+str(adc.psd_read())+ " cm")
textLcd.lcd_display_string(str(adc.vr_read())+" %" + str(adc.cds_read()) + " %", 2)

write.On(RED_LED)
time.sleep(0.5)
write.On(GREEN_LED)
time.sleep(0.5)
write.On(BLUE_LED)
time.sleep(0.5)
write.Off(RED_LED| GREEN_LED| BLUE_LED)
time.sleep(0.5)
write.On(RELAY_1 | RELAY_2)
time.sleep(0.5)
write.Off(RELAY_1 | RELAY_2)
time.sleep(0.5)


import os

import sounddevice as sd
import scipy.io as sio
import scipy.io.wavfile
# numpy array audio data, frames per second
sample_rate = 44100  # 샘플레이트, 
seconds = 3  # 녹음시간

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "output.wav")

print("녹음 시작..녹음중")
myrecording = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=2)
sd.wait()  # 녹음이 끝날때까지 대기
print("녹음 완료")
sio.wavfile.write(file_path, sample_rate, myrecording)  # wav파일로 저장
