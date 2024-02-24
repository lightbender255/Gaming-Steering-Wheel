#include <Joystick.h>

const bool INCLUDE_X_AXIS = true;
const bool INCLUDE_Y_AXIS = true;
const bool INCLUDE_Z_AXIS = true;
const bool INCLUDE_RX_AXIS = true;
const bool INCLUDE_RY_AXIS = true;
const bool INCLUDE_RZ_AXIS = true;
const bool INCLUDE_RUDDER = true;
const bool INCLUDE_THROTTLE = true;
const bool INCLUDE_ACCELERATOR = true;
const bool INCLUDE_BRAKE = true;
const bool INCLUDE_STEERING = true;

const int BRAKE_ADJUSTMENT = 17;
const int GAS_ADJUSTMENT = 33;
const int STEERING_ADJUSTMENT = 0;
const int BUTTON_COUNT = 4;
const int HAT_SWITCH_COUNT = 0;
const int GAS_MIN = 400;
const int BRAKE_MIN = 0;
const int STEERING_MIN = 0;
const int GAS_MAX = 1023;

const int OUTPUT_SERIAL_TEXT = false;
const int OUTPUT_SERIAL_GRAPH = true;

// Create Joystick
Joystick_ Joystick(
    JOYSTICK_DEFAULT_REPORT_ID, JOYSTICK_TYPE_JOYSTICK,
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

int previousSteeringValue = 0;
int previousGasValue = 0;
int previousBrakeValue = 0;
int brake = 0;
int gas = 0;
int steering = 0;

void loop()
{
  steering = analogRead(A0);
  steering = hysteresis(steering, previousSteeringValue);
  steering -= STEERING_ADJUSTMENT;
  Joystick.setXAxis(steering);

  gas = analogRead(A1);
  gas = hysteresis(gas, previousGasValue);
  gas = gas - GAS_ADJUSTMENT;
  gas = GAS_MAX - gas;
  if (gas < GAS_MIN)
  {
    gas = 0;
  }
  Joystick.setRyAxis(gas);

  brake = analogRead(A2);
  brake = hysteresis(brake, previousBrakeValue);
  brake = brake - BRAKE_ADJUSTMENT;
  if (brake < 0)
  {
    brake = 0;
  }
  Joystick.setRxAxis(brake);

  if (OUTPUT_SERIAL_TEXT)
  {

    Serial.print("\tSteering X: [ ");
    Serial.print(steering);
    Serial.print(" ]");

    Serial.print("\tSteering: [ ");
    Serial.print(steering);
    Serial.print(" ]");

    Serial.print("\tGas: [ ");
    Serial.print(gas);
    Serial.print(" ]");

    Serial.print("\tBrake: [ ");
    Serial.print(brake);
    Serial.print(" ]");

    Serial.println();
    delay(100);
  }

  if (OUTPUT_SERIAL_GRAPH)
  {
    Serial.print(steering);
    Serial.print(",");
    Serial.print(gas);
    Serial.print(",");
    Serial.print(brake);
  }

  for (int index = 0; index < 4; index++)
  {
    int currentButtonState = !digitalRead(index + pinToButtonMap);
    if (currentButtonState != lastButtonState[index])
    {
      Joystick.setButton(index, currentButtonState);
      lastButtonState[index] = currentButtonState;
    }

    if (OUTPUT_SERIAL_TEXT)
    {
      Serial.print("\tButton: [ ");
      Serial.print(lastButtonState[index]);
      Serial.print(" ]");
    }

    if (OUTPUT_SERIAL_GRAPH)
    {
      Serial.print(",");
      Serial.print(lastButtonState[index]);
    }

    delay(50);
  }
  Serial.println();
}