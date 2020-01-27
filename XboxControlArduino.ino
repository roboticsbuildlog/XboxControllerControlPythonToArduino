String incomingByte;

//Motor Pins
#define PWMA 12    //Motor A Speed
#define DIRA1 34
#define DIRA2 35  //Motor A Direction
#define PWMB 8    //Motor B Speed
#define DIRB1 37
#define DIRB2 36  //Motor B Direction
#define PWMC 9   //Motor C Speed
#define DIRC1 43
#define DIRC2 42  //Motor C Direction
#define PWMD 5    //Motor D Speed
#define DIRD1 26
#define DIRD2 27  //Motor A Direction


int error = 0;
byte type = 0;
byte vibrate = 0;

void (* resetFunc) (void) = 0;

//Motor A
#define MOTORA_FORWARD(pwm)    do{digitalWrite(DIRA1,LOW); digitalWrite(DIRA2,HIGH);analogWrite(PWMA,pwm);}while(0)
#define MOTORA_STOP(x)         do{digitalWrite(DIRA1,LOW); digitalWrite(DIRA2,LOW); analogWrite(PWMA,0);}while(0)
#define MOTORA_BACKOFF(pwm)    do{digitalWrite(DIRA1,HIGH);digitalWrite(DIRA2,LOW); analogWrite(PWMA,pwm);}while(0)

//Motor B
#define MOTORB_FORWARD(pwm)    do{digitalWrite(DIRB1,HIGH); digitalWrite(DIRB2,LOW);analogWrite(PWMB,pwm);}while(0)
#define MOTORB_STOP(x)         do{digitalWrite(DIRB1,LOW); digitalWrite(DIRB2,LOW); analogWrite(PWMB,0);}while(0)
#define MOTORB_BACKOFF(pwm)    do{digitalWrite(DIRB1,LOW);digitalWrite(DIRB2,HIGH); analogWrite(PWMB,pwm);}while(0)

//Motor C
#define MOTORC_FORWARD(pwm)    do{digitalWrite(DIRC1,LOW); digitalWrite(DIRC2,HIGH);analogWrite(PWMC,pwm);}while(0)
#define MOTORC_STOP(x)         do{digitalWrite(DIRC1,LOW); digitalWrite(DIRC2,LOW); analogWrite(PWMC,0);}while(0)
#define MOTORC_BACKOFF(pwm)    do{digitalWrite(DIRC1,HIGH);digitalWrite(DIRC2,LOW); analogWrite(PWMC,pwm);}while(0)

//Motor D
#define MOTORD_FORWARD(pwm)    do{digitalWrite(DIRD1,HIGH); digitalWrite(DIRD2,LOW);analogWrite(PWMD,pwm);}while(0)
#define MOTORD_STOP(x)         do{digitalWrite(DIRD1,LOW); digitalWrite(DIRD2,LOW); analogWrite(PWMD,0);}while(0)
#define MOTORD_BACKOFF(pwm)    do{digitalWrite(DIRD1,LOW);digitalWrite(DIRD2,HIGH); analogWrite(PWMD,pwm);}while(0)

#define SERIAL  Serial

#define LOG_DEBUG

#ifdef LOG_DEBUG
#define M_LOG SERIAL.print
#else
#define M_LOG
#endif

#define MAX_PWM   200
#define MIN_PWM   130
int Motor_PWM = 130;

//Controlling Motor Motion Macro Definition


//    ↑A-----B↑
//     |  ↑  |
//     |  |  |
//    ↑C-----D↑
void ADVANCE()
{
  MOTORA_FORWARD(Motor_PWM); MOTORB_FORWARD(Motor_PWM);
  MOTORC_FORWARD(Motor_PWM); MOTORD_FORWARD(Motor_PWM);
}

//    ↓A-----B↓
//     |  |  |
//     |  ↓  |
//    ↓C-----D↓
void BACK()
{
  MOTORA_BACKOFF(Motor_PWM); MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM); MOTORD_BACKOFF(Motor_PWM);
}
//    ↑A-----B=
//     |   ↖ |
//     | ↖   |
//    =C-----D↑
void LEFT_1()
{
  MOTORA_FORWARD(Motor_PWM); MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM); MOTORD_FORWARD(Motor_PWM);
}

//    ↓A-----B↑
//     |  ←  |
//     |  ←  |
//    ↑C-----D↓
void LEFT_2()
{
  MOTORA_BACKOFF(Motor_PWM); MOTORB_FORWARD(Motor_PWM);
  MOTORC_FORWARD(Motor_PWM); MOTORD_BACKOFF(Motor_PWM);
}
//    ↓A-----B=
//     | ↙   |
//     |   ↙ |
//    =C-----D↓
void LEFT_3()
{
  MOTORA_BACKOFF(Motor_PWM); MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM); MOTORD_BACKOFF(Motor_PWM);
}
//    ↓A-----B↑
//     |  ←  |
//     | ↓  ↑ |
//     |  →  |
//    ↓C-----D↑
void LEFT_4()
{
  MOTORA_BACKOFF(Motor_PWM); MOTORB_FORWARD(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM); MOTORD_FORWARD(Motor_PWM);
}
//    =A-----B↑
//     | ↗   |
//     |   ↗ |
//    ↑C-----D=
void RIGHT_1()
{
  MOTORA_STOP(Motor_PWM); MOTORB_FORWARD(Motor_PWM);
  MOTORC_FORWARD(Motor_PWM); MOTORD_STOP(Motor_PWM);
}
//    ↑A-----B↓
//     |  →  |
//     |  →  |
//    ↓C-----D↑
void RIGHT_2()
{
  MOTORA_FORWARD(Motor_PWM); MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM); MOTORD_FORWARD(Motor_PWM);
}
//    =A-----B↓
//     |   ↘ |
//     | ↘   |
//    ↓C-----D=
void RIGHT_3()
{
  MOTORA_STOP(Motor_PWM); MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM); MOTORD_STOP(Motor_PWM);
}
//    ↑A-----B↓
//     |  →  |
//     | ↑  ↓ |
//     |  ←  |
//    ↑C-----D↓
void RIGHT_4()
{
  MOTORA_FORWARD(Motor_PWM); MOTORB_BACKOFF(Motor_PWM);
  MOTORC_FORWARD(Motor_PWM); MOTORD_BACKOFF(Motor_PWM);
}
//    =A-----B=
//     |  =  |
//     |  =  |
//    =C-----D=
void STOP()
{
  MOTORA_STOP(Motor_PWM); MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM); MOTORD_STOP(Motor_PWM);
}
void UART_Control()
{
  char Uart_Date = 0;
  SERIAL.print(Uart_Date);
  if (SERIAL.available())
  {
    Uart_Date = SERIAL.read();
    SERIAL.print(Uart_Date);
  }
  switch (Uart_Date)
  {
    case 'A':  ADVANCE();  M_LOG("Run!\r\n");        break;
    case 'B':  RIGHT_1();  M_LOG("Right up!\r\n");     break;
    case 'C':  RIGHT_2();  M_LOG("Right Straffe!\r\n");        break;
    case 'D':  RIGHT_3();  M_LOG("Right down!\r\n");   break;
    case 'I':  RIGHT_4();  M_LOG("Right Rotate!\r\n");        break;
    case 'E':  BACK();     M_LOG("Run!\r\n");        break;
    case 'J':  LEFT_4();   M_LOG("Left Rotate!\r\n");        break;
    case 'F':  LEFT_3();   M_LOG("Left down!\r\n");    break;
    case 'G':  LEFT_2();   M_LOG("Left Straffe!\r\n");       break;
    case 'H':  LEFT_1();   M_LOG("Left up!\r\n");  break;
    case 'Z':  STOP();     M_LOG("Stop!\r\n");       break;
    case 'L':  Motor_PWM = 240;                      break;
    case 'M':  Motor_PWM = 130;                       break;
  }
}
void IO_init()
{
  pinMode(PWMA, OUTPUT);
  pinMode(DIRA1, OUTPUT);
  pinMode(DIRA2, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(DIRB1, OUTPUT);
  pinMode(DIRB2, OUTPUT);
  pinMode(PWMC, OUTPUT);
  pinMode(DIRC1, OUTPUT);
  pinMode(DIRC2, OUTPUT);
  pinMode(PWMD, OUTPUT);
  pinMode(DIRD1, OUTPUT);
  pinMode(DIRD2, OUTPUT);
  STOP();
}
void setup()
{


  Serial.begin(115200);
  delay(300);

  SERIAL.print(incomingByte);
}
void loop()
{
  if (Serial.available() > 0) {

    incomingByte = Serial.readStringUntil('\n');

  }
  UART_Control();
}
