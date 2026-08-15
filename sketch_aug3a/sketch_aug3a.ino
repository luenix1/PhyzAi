#include <Adafruit_LSM6DS3TRC.h>

const float WHEEL_DIAMETER_INCHES = 4.875;
const float WHEELBASE_MM      = 233.3625;
const int   ENCODER_CPR       = 200;

volatile float M1Encoder = 0;
float M1Last = 0;
volatile float M2Encoder = 0;
float M2Last = 0;

int motorFudge = 15;
float counter = 0;

float straightKP = 0.12;
float straightKI = 0.001;
float straightKD = 2.5;

float rotateKP = 0.7;
float rotateKI = 0.001;
float rotateKD = 2.5;

bool stop = false;
float target = 0;
float TargetInTicks = 0;
float error = 0; 
float prevError = 0;
float I = 0;

unsigned long time = millis();
unsigned long prevTime = millis(); 


// Motor 1 = RIGHT
#define M1_ENC_A  2
#define M1_ENC_B  4
#define M1_PWM    5
#define M1_IN1    7
#define M1_IN2    8

// Motor 2 = LEFT
#define M2_ENC_A  3
#define M2_ENC_B  6
#define M2_PWM    9
#define M2_IN1    10
#define M2_IN2    11

Adafruit_LSM6DS3TRC imu;
float heading  = 0.0;
float gyroBiasZ    = 0.0;
unsigned long lastIMU_us = 0;

void setMotor1Power(int speed){
  if (speed > 0) {digitalWrite(M1_IN1, LOW); digitalWrite(M1_IN2, HIGH);}
  else if (speed <= 0) {digitalWrite(M1_IN1, HIGH); digitalWrite(M1_IN2, LOW); speed = -speed;}
  analogWrite(M1_PWM, constrain(speed, 0 , 255));
}

void setMotor2Power(int speed){
  if (speed > 0) {digitalWrite(M2_IN1, HIGH); digitalWrite(M2_IN2, LOW);}
  else if (speed <= 0) {digitalWrite(M2_IN1, LOW); digitalWrite(M2_IN2, HIGH); speed = -speed;}
  analogWrite(M2_PWM, constrain(speed, 0 , 255));
}

void setupIMU() {
  Serial.println("start");
  if (!imu.begin_I2C()) {
    while (1) delay(100);
  }
  Serial.println("start");

  imu.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  imu.setGyroDataRate(LSM6DS_RATE_104_HZ);
  imu.setAccelDataRate(LSM6DS_RATE_104_HZ);

  delay(100);
  float biasSum = 0;
  int samples = 150;
  for (int i = 0; i < samples; i++) {
    sensors_event_t accel, gyro, temp;
    imu.getEvent(&accel, &gyro, &temp);
    biasSum += gyro.gyro.z;
    delay(10);
    Serial.println(i);
  }
  gyroBiasZ = biasSum / samples;
  lastIMU_us = micros();

  Serial.println("done");
}

void updateHeading() {
  sensors_event_t accel, gyro, temp;
  imu.getEvent(&accel, &gyro, &temp);
  unsigned long now = micros();
  float dt = (now - lastIMU_us) / 1e6f;
  lastIMU_us = now;
  heading += (gyro.gyro.z - gyroBiasZ) * dt * (180.0f / PI);
  heading = fmod(heading, 360);
  if (heading < 0) {
    heading += 360;
  }
}

void updateEncoder(){

 M1Encoder = digitalRead(M1_ENC_A); 
   if (M1Encoder != M1Last){     
     if (digitalRead(M1_ENC_B) != M1Encoder) { 
       counter ++;
     } else {
       counter --;
     }
    //  Serial.println(counter);
   } 
   M1Last = M1Encoder;

}

void turnTo(int tgta){
  float errorA = tgta;
  float prevErrorA = error;
  float IA = 0;

  while (true){
    updateHeading();
    time = millis();

    errorA = tgta - heading;

    errorA = fmod(errorA, 360);
    if (errorA > 180){
      errorA -= 360;
    }
    else if (error < -180){
      errorA += 360;
    }

    float currentTime = time;
    float dt = currentTime - prevTime;
    float errorDiff = errorA - prevErrorA;

    float P = errorA * rotateKP;
    I = errorA * dt * rotateKI;
    
    if (errorDiff > 0.5){
      I = 0;
    }

    float velocity = errorDiff / dt;

    float D = velocity * rotateKD;

    int power = P + IA + D;

    Serial.println(power);
    Serial.print("power");

    if (abs(errorA) < 1 && abs(velocity) < 1){
      break;
    }

    setMotor1Power(-power);
    setMotor2Power(power);

    prevTime = currentTime;
    prevErrorA = errorA;
  }

    setMotor1Power(0);
    setMotor2Power(0);
}

void driveStraight(){
  if (abs(error) > 1 && !stop){
    updateHeading();
    error = TargetInTicks - counter;
    time = millis();

    float currentTime = time;

    float errorDiff = error - prevError;
    float dt = currentTime - prevTime;

    float P = error * straightKP;
    I += error * dt * straightKI;
    if(abs(errorDiff) > 1){
      I = 0;
    }
    // Serial.println(I);
    // Serial.print("I");
    float velocity = (errorDiff / dt);
    float D = velocity * straightKD;

    int power = P + I + D;

    // Serial.println(D);
    // Serial.print("D");

    Serial.println("error");
    Serial.print(error);

    // Serial.println(power);
    // Serial.print("power");

    setMotor1Power(power + 15);
    setMotor2Power(power);
    // attachInterrupt(digitalPinToInterrupt(M1_ENC_A), updateEncoder, CHANGE);

    prevTime = currentTime;
    prevError = error;
  }
}

void updateStraightTgt(float inches){
  target = inches;
  TargetInTicks = ((target * ENCODER_CPR)/ WHEEL_DIAMETER_INCHES) + counter;
  error = TargetInTicks - counter;
  Serial.println(error);

  prevError = error;
  I = 0;
}

void getCommands(){
  if (Serial.available()) {
    String command = Serial.readStringUntil("\n");
    // command.trim();

    if (command.startsWith("ROTATE ")){
      float tgt = command.substring(7).toFloat();

      turnTo(tgt);
    }

    if (command.startsWith("DRIVE ")){
      float tgt = command.substring(6).toFloat();

      updateStraightTgt(tgt);
    }

    if (command.equals("STOP")){
      stop = true;
      error = 0;
    }

    if (command.equals("CONTINUE")){
      stop = false;
    }
    Serial.println(command);
  }
  // else { Serial.println("no command!");}
}
    

void setup() {
  Serial.begin(9600);
  Serial.println("ahsdadas");
  pinMode(M1_IN1, OUTPUT); pinMode(M1_IN2, OUTPUT); pinMode(M1_PWM, OUTPUT);
  pinMode(M2_IN1, OUTPUT); pinMode(M2_IN2, OUTPUT); pinMode(M2_PWM, OUTPUT);

  pinMode(M1_PWM, OUTPUT); pinMode(M2_PWM, OUTPUT);

  pinMode(M1_ENC_A, INPUT_PULLUP); pinMode(M1_ENC_B, INPUT_PULLUP);
  pinMode(M2_ENC_A, INPUT_PULLUP); pinMode(M2_ENC_B, INPUT_PULLUP);

  setupIMU();

  attachInterrupt(digitalPinToInterrupt(M1_ENC_A), updateEncoder, CHANGE);
  
}

void loop() {
  getCommands();

  updateHeading();
  
  driveStraight();
 
}
