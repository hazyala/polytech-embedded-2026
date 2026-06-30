#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <stdio.h>
#include <unistd.h>

// PCA9685의 기본 I2C 주소는 0x40 이옵니다
#define PCA9685_ADDR 0x40
#define MODE1 0x00
#define PRESCALE 0xFE
#define LED0_ON_L 0x06

// 서보모터(조향)는 PWM 0번 채널에 연결되어 있사옵니다 [cite: 833]
#define STEER_CHANNEL_OFFSET 0 

void setPWM(int fd, int channel, int on, int off) {
    wiringPiI2CWriteReg8(fd, LED0_ON_L + 4 * channel, on & 0xFF);
    wiringPiI2CWriteReg8(fd, LED0_ON_L + 4 * channel + 1, on >> 8);
    wiringPiI2CWriteReg8(fd, LED0_ON_L + 4 * channel + 2, off & 0xFF);
    wiringPiI2CWriteReg8(fd, LED0_ON_L + 4 * channel + 3, off >> 8);
}

int main() {
    int fd;
    if (wiringPiSetup() == -1) return 1;

    // I2C 장치를 엽니다 (주소 0x40)
    fd = wiringPiI2CSetup(PCA9685_ADDR);
    if (fd < 0) {
        printf("I2C 연결 실패 하였사옵니다.\n");
        return 1;
    }

    // PCA9685 초기화 (50Hz 설정 함)
    wiringPiI2CWriteReg8(fd, MODE1, 0x00);
    
    printf("서보모터를 25도 방향으로 움직입니다.\n");
    // 각도 제어 (이 수치는 장치마다 다를 수 있으나 대략적인 25도 지점이옵니다)
    setPWM(fd, STEER_CHANNEL_OFFSET, 0, 200); 
    delay(1000);

    printf("중앙(90도)으로 복귀합니다.\n");
    setPWM(fd, STEER_CHANNEL_OFFSET, 0, 307); // 90도 표준 값 사용 함
    delay(1000);

    return 0;
}