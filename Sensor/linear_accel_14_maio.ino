#include <Adafruit_BNO08x.h>

#define BNO08X_CS 10
#define BNO08X_INT 9
#define BNO08X_RESET -1

Adafruit_BNO08x bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

void setup() {
  Serial.begin(115200);
  while (!Serial)
    delay(10); 

  Serial.println("Adafruit BNO08x test!");

  if (!bno08x.begin_I2C()) {
    Serial.println("Failed to find BNO08x chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("BNO08x Found!");

  if (!bno08x.enableReport(SH2_LINEAR_ACCELERATION)) {
    Serial.println("Could not enable linear acceleration");
  }
}

void loop() {
  delay(10);

  if (!bno08x.getSensorEvent(&sensorValue)) {
    return;
  }

  // // Print the accelerometer values
  // Serial.print("Accelerometer - x: ");
  // Serial.print(sensorValue.un.accelerometer.x);
  // Serial.print(" y: ");
  // Serial.print(sensorValue.un.accelerometer.y);
  // Serial.print(" z: ");
  // Serial.println(sensorValue.un.accelerometer.z);

  // Print linear acceleration values
  Serial.print("Linear Acceleration - x: ");
  Serial.print(sensorValue.un.linearAcceleration.x);
  Serial.print(" y: ");
  Serial.print(sensorValue.un.linearAcceleration.y);
  Serial.print(" z: ");
  Serial.println(sensorValue.un.linearAcceleration.z);
}
