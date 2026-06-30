#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <wiringPi.h>

// 스위치 핀 번호를 정의합니다 (wiringPi 핀 번호 기준).
// 매크로(Macro)를 사용하여 변하지 않는 고정된 값을 이름으로 지정합니다.
#define SW1_PIN 7
#define SW2_PIN 0
#define SW3_PIN 1
#define SW4_PIN 3

// 모터 핀 번호를 정의합니다 (wiringPi 핀 번호 기준).
#define MOTOR_PIN1 27
#define MOTOR_PIN2 28
#define MOTOR_PIN3 29
#define MOTOR_PIN4 25

// 모터 핀 번호를 배열에 저장하여 반복문에서 쉽게 꺼내 쓸 수 있도록 합니다.
int motor_pins[4] = {MOTOR_PIN1, MOTOR_PIN2, MOTOR_PIN3, MOTOR_PIN4};

// 스텝 모터 구동 신호입니다.
int step_signals[4][4] = {
    {1, 0, 0, 0},
    {0, 1, 0, 0},
    {0, 0, 1, 0},
    {0, 0, 0, 1}
};

void setup_gpio(void) {
    // 스위치 핀을 입력(INPUT) 모드로 설정합니다.
    pinMode(SW1_PIN, INPUT);
    pinMode(SW2_PIN, INPUT);
    pinMode(SW3_PIN, INPUT);
    pinMode(SW4_PIN, INPUT);

    // 모터 핀을 출력(OUTPUT) 모드로 설정하고 초기 상태를 LOW(0)로 설정합니다.
    for(int i = 0; i < 4; i++) {
        pinMode(motor_pins[i], OUTPUT);
        digitalWrite(motor_pins[i], LOW);
    }
}

void rotate_motor(int is_clockwise, int steps, int delay_ms) {
    // 모터를 지정된 스텝 수와 방향으로 회전시키는 함수입니다.
    for(int i = 0; i < steps; i++) {
        if (is_clockwise == 1) {
            // 시계 방향: 배열을 0번부터 3번까지 차례대로 읽습니다.
            for(int step_idx = 0; step_idx < 4; step_idx++) {
                for(int pin_idx = 0; pin_idx < 4; pin_idx++) {
                    digitalWrite(motor_pins[pin_idx], step_signals[step_idx][pin_idx]);
                }
                delay(delay_ms);
            }
        } else {
            // 반시계 방향: 배열을 3번부터 0번까지 거꾸로 읽습니다.
            for(int step_idx = 3; step_idx >= 0; step_idx--) {
                for(int pin_idx = 0; pin_idx < 4; pin_idx++) {
                    digitalWrite(motor_pins[pin_idx], step_signals[step_idx][pin_idx]);
                }
                delay(delay_ms);
            }
        }
    }
}

void stop_motor() {
    // 모터의 전력을 차단하여 정지시키는 함수입니다.
    for(int i = 0; i < 4; i++) {
        digitalWrite(motor_pins[i], LOW);
    }
}

int main(void) {
    // wiringPi 라이브러리를 초기화합니다.
    if (wiringPiSetup() == -1) {
        fprintf(stdout, "초기화 오류: %s\n", strerror(errno));
        return 1;
    }

    setup_gpio();
    printf("스위치 모터 제어 C 프로그램 시작\n");

    // 끝없이 작동하는 무한 반복문입니다.
    for (;;) {
        // 스위치 1번이 눌렸을 때 (신호가 HIGH일 때)
        if (digitalRead(SW1_PIN) == HIGH) {
            printf("스위치 1 눌림: 시계 방향\n");
            // 1(시계방향)으로 50스텝 이동하며 2밀리초 대기합니다.
            rotate_motor(1, 50, 2);
        }
        // 스위치 2번이 눌렸을 때
        else if (digitalRead(SW2_PIN) == HIGH) {
            printf("스위치 2 눌림: 반시계 방향\n");
            // 0(반시계방향)으로 50스텝 이동하며 2밀리초 대기합니다.
            rotate_motor(0, 50, 2);
        }
        // 스위치가 눌리지 않았을 때
        else {
            stop_motor();
        }
        
        // 너무 빠른 반복으로 라즈베리파이가 지치지 않게 잠시 숨을 고릅니다.
        delay(100);
    }

    return 0;
}