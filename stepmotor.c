#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <wiringPi.h>

// wiringPi 핀 번호를 정의합니다. 
// 매크로 상수(#define)를 사용하여 핀 번호에 이름을 붙여 관리하기 쉽게 만듭니다.
#define PIN_IN1 27
#define PIN_IN2 28
#define PIN_IN3 29
#define PIN_IN4 25

// 4개의 핀 번호를 배열에 담아 반복문에서 사용하기 쉽게 묶어둡니다.
// 배열(Array)은 같은 종류의 데이터를 순서대로 나열한 주머니와 같습니다.
int motor_pins[4] = {PIN_IN1, PIN_IN2, PIN_IN3, PIN_IN4};

// 스텝 모터를 1스텝씩 움직이기 위한 전기 신호 패턴입니다.
// 2차원 배열을 사용하여 4단계의 상태를 저장합니다. 1은 전류 보냄(HIGH), 0은 차단(LOW)입니다.
int step_signals[4][4] = {
    {1, 0, 0, 0},
    {0, 1, 0, 0},
    {0, 0, 1, 0},
    {0, 0, 0, 1}
};

// 한 바퀴 회전을 위한 반복 횟수와 모터 신호 단계를 상수로 지정합니다.
int MAX_STEPS = 4;
int ROTATE_360 = 512;

// 입출력 핀을 초기화하는 함수입니다.
// 함수(Function)는 특정 작업을 수행하는 코드의 묶음입니다.
void setup_motor_pins(void) {
    // 반복문(for)을 사용하여 4개의 핀을 한 번에 출력(OUTPUT) 모드로 설정합니다.
    for(int i = 0; i < 4; i++) {
        pinMode(motor_pins[i], OUTPUT);
        // 초기 상태에서는 모터가 제멋대로 움직이지 않도록 모든 핀의 전류를 차단(LOW)합니다.
        digitalWrite(motor_pins[i], LOW);
    }
}

int main() {
    // wiringPi 라이브러리를 초기화합니다. 
    // wiringPiSetup()은 라즈베리파이의 'wiringPi 전용 핀 번호' 체계를 사용하도록 합니다.
    // 만약 초기화에 실패하면(-1 반환), 오류 메시지를 출력하고 프로그램을 종료(return 1)합니다.
    if (wiringPiSetup() == -1) {
        fprintf(stdout, "초기화 오류: %s\n", strerror(errno));
        return 1;
    }

    // 핀 설정 함수를 호출하여 사용할 준비를 마칩니다.
    setup_motor_pins();

    printf("모터 시계 방향 회전 시작\n");

    // 시계 방향으로 모터를 회전시킵니다.
    for(int i = 0; i < ROTATE_360; i++) {
        for(int step_idx = 0; step_idx < MAX_STEPS; step_idx++) {
            // 각 핀에 알맞은 신호를 순서대로 전달합니다.
            for(int pin_idx = 0; pin_idx < 4; pin_idx++) {
                digitalWrite(motor_pins[pin_idx], step_signals[step_idx][pin_idx]);
            }
            // 1밀리초(0.001초) 동안 대기하여 모터가 물리적으로 움직일 시간을 줍니다.
            delay(20);
        }
    }

    printf("모터 반시계 방향 회전 시작\n");

    // 반시계 방향으로 모터를 회전시킵니다.
    // 신호 배열을 역순(3번부터 0번까지)으로 읽어들여 방향을 뒤집습니다.
    for(int i = 0; i < ROTATE_360; i++) {
        // 원본 코드의 치명적 오류(범위를 벗어난 배열 접근)를 수정했습니다.
        // MAX_STEPS(4)부터 시작하면 없는 데이터에 접근하므로 3부터 시작하도록 고쳤습니다.
        for(int step_idx = MAX_STEPS - 1; step_idx >= 0; step_idx--) {
            for(int pin_idx = 0; pin_idx < 4; pin_idx++) {
                digitalWrite(motor_pins[pin_idx], step_signals[step_idx][pin_idx]);
            }
            delay(20);
        }
    }

    printf("모터 제어 종료\n");
    return 0; // 프로그램이 문제없이 끝났음을 운영체제에 알립니다.
}