#include <Joystick.h>
#include <SimRacing.h>

// Create Joystick
Joystick_ Joystick;

void setup() {
  pinMode(9, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  pinMode(12, INPUT_PULLUP);
  Joystick.begin();
  Joystick.setXAxisRange(0, 1023);
  Joystick.setRxAxisRange(0, 1023);
  Joystick.setRyAxisRange(0, 1023);
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);

  Serial.begin(115200);
  while (!Serial);  // wait for connection to open

  Serial.println("Starting...");
  Serial.print("setup complete");
}

const int pinToButtonMap = 9;

// Last state of the button
int lastButtonState[4] = {0, 0, 0, 0};


void loop() {


  int steering = analogRead(A0);
  int gas = analogRead(A1);
  int brake = analogRead(A2);
  Joystick.setXAxis(steering);
  Joystick.setRyAxis(gas);
  Joystick.setRxAxis(brake);

  Serial.print("Pedals:");

  Serial.print("\tSteering: [ ");
  Serial.print(steering);
  Serial.print("% ]");

  Serial.print("\tGas: [ ");
  Serial.print(gas);
  Serial.print("% ]");

  Serial.print("\tBrake: [ ");
  Serial.print(brake);
  Serial.print("% ]");

  Serial.println();
  delay(100);

  for (int index = 0; index < 4; index++)
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
