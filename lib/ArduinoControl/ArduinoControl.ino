// -*- mode: C++ -*-

#include <AccelStepper.h>
#include <AFMotor.h>
#include <Servo.h> 

AF_Stepper motor1(200, 2);
Servo myservo;
int pos = 0;
int SPEED = 50;
int STEP = 5;
int MAXPOS = 180;
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
  myservo.attach(9); 
  myservo.write(pos);
}

void loop()
{  
  
}

void open_valve(){
for(pos = 0; pos < MAXPOS; pos += 1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(1);                       // waits 15ms for the servo to reach the position 
  } 
}
void close_valve(){
  for(pos = MAXPOS; pos>=1; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(1);                       // waits 15ms for the servo to reach the position 
  } 
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
    if (inChar == 'o') {
      if(!pos){
        open_valve();
      }
    }
    if (inChar == 'c') {
      if(pos){
        close_valve();
      }
    }
  }
}
