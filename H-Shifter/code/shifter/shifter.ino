// Once you have used the calbration sketch to the controller and gatherd the 8 coordinates for each gear position update this file
#include <Joystick.h>

// Define the analog pins connected to the potentiometers
#define POTENTIOMETER_PIN_X A2
#define POTENTIOMETER_PIN_Y A3

const int positionsX[8] = {0, 0, 494, 335, 805, 570, 1023, 1023}; // Example X coordinates for each gear position
const int positionsY[8] = {0, 1021, 0, 1023, 0, 1023, 0, 1023};    // Example Y coordinates for each gear position
const float threshold = 0.1; // Define threshold as 10%
const int maxCoordinateValue = 1024; // Maximum possible coordinate value

Joystick_ joystick;

int previousGear = -1; // Variable to store the previous gear selection

void setup() {
  Serial.begin(9600); // Initialize serial communication
  joystick.begin();   // Initialize the joystick library
}

void loop() {
  int potXValue = analogRead(POTENTIOMETER_PIN_X); // Read X potentiometer value
  int potYValue = analogRead(POTENTIOMETER_PIN_Y); // Read Y potentiometer value
  
  // Calculate the maximum allowed deviation from target position
  float deviationThreshold = threshold * maxCoordinateValue;

  int currentGear = -1; // Variable to store the current gear selection

  // Check each gear position
  for (int i = 0; i < 8; i++) {
    bool withinRange = (abs(positionsX[i] - potXValue) <= deviationThreshold) && 
                      (abs(positionsY[i] - potYValue) <= deviationThreshold);
    if (withinRange) {
      currentGear = i + 21; // Store the current gear selection
    }
  }

  // Check if gear selection has changed
  if (currentGear != previousGear) {
    if (currentGear != -1) {
      Serial.print("Gear ");
      Serial.print(currentGear);
      Serial.println(" selected.");
      joystick.setButton(currentGear, 1); // Set button corresponding to current gear position
    }
    if (previousGear != -1) {
      joystick.releaseButton(previousGear); // Release button corresponding to previous gear position
    }
    previousGear = currentGear; // Update the previous gear selection
  }

  delay(100); // Delay for stability
}
