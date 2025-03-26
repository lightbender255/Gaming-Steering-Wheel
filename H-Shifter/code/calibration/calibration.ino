// Upload this file first to your controller to gather the coordinates for each 8 gears

#include <Joystick.h>

// Define the analog pins connected to the potentiometers
#define POTENTIOMETER_PIN_X A2
#define POTENTIOMETER_PIN_Y A3

// Create an instance of the Joystick class
Joystick_ joystick;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Initialize the joystick with 0 buttons
  joystick.begin(0);
}

void loop() {
  // Read the analog values from the potentiometers
  int potXValue = analogRead(POTENTIOMETER_PIN_X);
  int potYValue = analogRead(POTENTIOMETER_PIN_Y);

  // Print the current X and Y coordinates
  Serial.print("X: ");
  Serial.print(potXValue);
  Serial.print("\tY: ");
  Serial.println(potYValue);

  // Delay for stability
  delay(100); // Adjust delay as needed
}
