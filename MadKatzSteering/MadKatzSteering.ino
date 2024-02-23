#include <Joystick.h>
#include <USBAPI.h>

// Create Joystick
Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID, JOYSTICK_TYPE_JOYSTICK,
                   2, 0,
                   true, true, true, true, true, true,
                   true, true, true, true, true);

int hysteresis(int newValue, int oldValue)
{
  if (newValue < (oldValue - 2) || newValue > (oldValue + 2))
  {
    oldValue = newValue;
  }
  return oldValue;
}

void setup()
{
  pinMode(9, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  pinMode(12, INPUT_PULLUP);
  Joystick.begin();
  Joystick.setXAxisRange(0, 1023);  // steering
  Joystick.setRxAxisRange(0, 1023); // brake
  Joystick.setRyAxisRange(0, 1023); // gas
  Joystick.setSteeringRange(0, 1023);
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);

  Serial.begin(115200);
  while (!Serial)
    ; // wait for connection to open

  Serial.println("Starting...");
  Serial.println("Setup Complete");
}

const int pinToButtonMap = 9;

// Last state of the button
int lastButtonState[4] = {0, 0, 0, 0};

int oldSteeringValue = 0;
int oldGasValue = 0;
int oldBrakeValue = 0;

void loop()
{
  int steering = analogRead(A0);
  steering = hysteresis(steering, oldSteeringValue);
  Joystick.setXAxis(steering);
  Joystick.setSteering(steering);

  int brake = analogRead(A2);
  brake = hysteresis(brake, oldGasValue);
  Joystick.setRxAxis(brake);

  int gas = analogRead(A1);
  gas = hysteresis(gas, oldGasValue);
  Joystick.setRyAxis(gas);

  Serial.print("\tSteering X: [ ");
  Serial.print(steering);
  Serial.print("% ]");

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
    Serial.print("\tButton: [ ");
    Serial.print(lastButtonState[index]);
    Serial.print(" ]");
  }

  delay(50);
}
