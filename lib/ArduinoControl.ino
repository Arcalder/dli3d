// -*- mode: C++ -*-

#include <AccelStepper.h>
#include <AFMotor.h>

AF_Stepper motor1(200, 2);
int SPEED = 50;
int STEP = 5;
String inString = "";
String steps= "";

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
void forwardstep() {  
  motor1.onestep(FORWARD, SINGLE);
}
void backwardstep() {  
  motor1.onestep(BACKWARD, SINGLE);
}

// use functions to step
AccelStepper stepper(forwardstep, backwardstep);

void setup()
{  
  // set up Serial library at 9600 bps
  Serial.begin(9600);
  Serial.println("Stepper program!");
  stepper.setMaxSpeed(200.0);
  stepper.setAcceleration(100.0);
}

void loop()
{  
  
}

void serialEvent() {
  while (Serial.available()) {
    int inChar = Serial.read();
    Serial.print("Echo:");
    Serial.write(inChar);
    Serial.println();
    if (isDigit(inChar)) {
      steps += (char)inChar; 
    }
    if (inChar == 'u') {
      Serial.print("Up:"+steps);
      Serial.println();
      long POSITION = stepper.currentPosition()+steps.toInt();
      stepper.runToNewPosition(POSITION);
      steps= "";
    }
    if (inChar == 'd') {
      Serial.print("Down:"+steps);
      Serial.println();
      long POSITION = stepper.currentPosition()-steps.toInt();
      stepper.runToNewPosition(POSITION);
      steps= "";
    }
    if (inChar == '.') {
      long POSITION = stepper.currentPosition()+STEP;
      stepper.runToNewPosition(POSITION);
    }
    if (inChar == '-') {
      long POSITION = stepper.currentPosition()-STEP;
      stepper.runToNewPosition(POSITION);
    }
  }
}
