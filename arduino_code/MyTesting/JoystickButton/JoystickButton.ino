
// Simple example application that shows how to read four Arduino
// digital pins and map them to the USB Joystick library.
//
// The digital pins 9, 10, 11, and 12 are grounded when they are pressed.
//
// NOTE: This sketch file is for use with Arduino Leonardo and
//       Arduino Micro only.
//
// by Matthew Heironimus
// 2015-11-20
//--------------------------------------------------------------------

#include <Joystick.h>
#include <Arduino.h>

const int DIGITAL_PADDLE_RIGHT = 9;
const int DIGITAL_PADDLE_LEFT = 10;
const int ANALOG_STEERING_0 = A0;
const int ANALOG_STEERING_1 = A1;
const int ANALOG_GAS = A2;
const int ANALOG_BRAKE = A3;
const int TOTAL_BUTTONS = 2;

void setup()
{
  // Initialize Button Pins
  pinMode(DIGITAL_PADDLE_RIGHT, INPUT_PULLUP);
  pinMode(DIGITAL_PADDLE_LEFT, INPUT_PULLUP);

  // Initialize Analog Pins
  pinMode(ANALOG_STEERING_0, INPUT_PULLUP);
  pinMode(ANALOG_STEERING_1, INPUT_PULLUP);
  pinMode(ANALOG_GAS, INPUT_PULLUP);
  pinMode(ANALOG_BRAKE, INPUT_PULLUP);

  // Initialize Joystick Library
  Joystick.begin();  
}

// Constant that maps the phyical pin to the joystick button.
const int pinToButtonMap = 9;

// Last state of the button
int lastButtonState[TOTAL_BUTTONS] = {0, 0};

void loop()
{
  // Read analog values
  int steering = analogRead(A0);
  int gas = analogRead(A1);
  int brake = analogRead(A2);
  Joystick.setXAxis(steering);
  Joystick.setRyAxis(gas);
  Joystick.setRxAxis(brake);

  // Read pin values
  for (int index = 0; index < TOTAL_BUTTONS; index++)
  {
    int currentButtonState = !digitalRead(index + pinToButtonMap);
    if (currentButtonState != lastButtonState[index])
    {
      Joystick.setButton(index, currentButtonState);
      lastButtonState[index] = currentButtonState;
    }
  }

  delay(50);
}
