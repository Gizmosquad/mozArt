//import stepper library
#include <Stepper.h>

//this is the number of steps the stepper has per revolution
const int stepsPerRevolution = 200;

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8,9,10,11);            

void setup() {
  // set the speed at 100 rpm:
  myStepper.setSpeed(100);
  // initialize the serial port:
  Serial.begin(9600);
}

void loop() {
  // step one revolution  in one direction:
  //slighty more than 200 due to physical imperfections in the stepper
  myStepper.step(205);
  //wait 10ms before next revolution
  delay(10);
  
}

