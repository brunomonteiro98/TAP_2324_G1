#include <Wire.h>
#include <Adafruit_BNO08x.h>
#include <ArduinoJson.h>

// For SPI mode, we need a CS pin
#define BNO08X_CS 10
#define BNO08X_INT 9

// For SPI mode, we also need a RESET
//#define BNO08X_RESET 5
// but not for I2C or UART
#define BNO08X_RESET -1

Adafruit_BNO08x  bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

struct euler_t {
  float yaw;
  float pitch;
  float roll;
} ypr;

float acx;
float acy;
float acz;

// Variables to store integration
float velocityX = 0;
float velocityY = 0;
float velocityZ = 0;
float positionX = 0;
float positionY = 0;
float positionZ = 0;

// Time variables
unsigned long prevTime;
unsigned long currentTime;

bool originSet = false;
euler_t originYPR;

#ifdef FAST_MODE
  sh2_SensorId_t reportType = SH2_GYRO_INTEGRATED_RV;
  long reportIntervalUs = 2000;
#else
  sh2_SensorId_t reportType = SH2_ROTATION_VECTOR;
  long reportIntervalUs = 5000;
#endif

void setReports(sh2_SensorId_t reportType, long report_interval) {
  if (!bno08x.enableReport(reportType, report_interval)) {
    Serial.println("Could not enable report");
  }
}

void quaternionToEuler(float qr, float qi, float qj, float qk, euler_t* ypr, bool degrees = false) {
    float t=qi; qi=qj; qj=t; qk=-qk;

    float sqr = sq(qr);
    float sqi = sq(qi);
    float sqj = sq(qj);
    float sqk = sq(qk);

    ypr->yaw = atan2(2.0 * (qi * qj + qk * qr), (sqi - sqj - sqk + sqr));
    ypr->pitch = asin(-2.0 * (qi * qk - qj * qr) / (sqi + sqj + sqk + sqr));
    ypr->roll = atan2(2.0 * (qj * qk + qi * qr), (-sqi - sqj + sqk + sqr));

    if (degrees) {
      ypr->yaw *= RAD_TO_DEG;
      ypr->pitch *= RAD_TO_DEG;
      ypr->roll *= RAD_TO_DEG;
    }
}

void quaternionToEulerGRV(sh2_RotationVector* rotational_vector, euler_t* ypr, bool degrees = false) {
    quaternionToEuler(rotational_vector->real, rotational_vector->i, rotational_vector->j, rotational_vector->k, ypr, degrees);
}

void quaternionToEulerRV(sh2_RotationVectorWAcc_t* rotational_vector, euler_t* ypr, bool degrees = false) {
    quaternionToEuler(rotational_vector->real, rotational_vector->i, rotational_vector->j, rotational_vector->k, ypr, degrees);
}

void quaternionToEulerGI(sh2_GyroIntegratedRV_t* rotational_vector, euler_t* ypr, bool degrees = false) {
    quaternionToEuler(rotational_vector->real, rotational_vector->i, rotational_vector->j, rotational_vector->k, ypr, degrees);
}

void setOrigin() {
  if (!originSet && bno08x.getSensorEvent(&sensorValue)) {
    switch (sensorValue.sensorId) {
      case SH2_GAME_ROTATION_VECTOR:
        quaternionToEulerGRV(&sensorValue.un.gameRotationVector, &originYPR, true);
        break;
      case SH2_GYRO_INTEGRATED_RV:
        quaternionToEulerGI(&sensorValue.un.gyroIntegratedRV, &originYPR, true);
        break;
      case SH2_ROTATION_VECTOR:
        quaternionToEulerRV(&sensorValue.un.rotationVector, &originYPR, true);
        break;
    }
    originSet = true;
  }
}

void setup() {
  // Begin I2C communications:
  Wire.begin();
  delay(50);

  // IMU init:
  bno08x.begin_I2C();

  delay(10);
  setReports(reportType, reportIntervalUs);

  // Serial for testing
  Serial.begin(9600);
    while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit BNO08x test!");


  Serial.println("BNO08x Found!");

  setReports2();

  Serial.println("Reading events");

  // Initialize time variables
  prevTime = millis();

  delay(100);
}

// Here is where you define the sensor outputs you want to receive
void setReports2(void) {
  Serial.println("Setting desired reports");
  if (!bno08x.enableReport(SH2_LINEAR_ACCELERATION)) {
    Serial.println("Could not enable linear acceleration");
  }
}

void loop() {
  // Set origin if not already set
  if (!originSet) {
    setOrigin();
    return; // Exit loop until origin is set
  }

  delay(10);
  // Read IMU.
  if (bno08x.getSensorEvent(&sensorValue)) {
    // in this demo only one report type will be received depending on FAST_MODE define (above)
    switch (sensorValue.sensorId) {
      case SH2_GAME_ROTATION_VECTOR:
        quaternionToEulerGRV(&sensorValue.un.gameRotationVector, &ypr, true);
        break;
      case SH2_GYRO_INTEGRATED_RV:
        quaternionToEulerGI(&sensorValue.un.gyroIntegratedRV, &ypr, true);
        break;
      case SH2_ROTATION_VECTOR:
        quaternionToEulerRV(&sensorValue.un.rotationVector, &ypr, true);
        break;

      case SH2_LINEAR_ACCELERATION:
        acx = sensorValue.un.linearAcceleration.x;
        acy = sensorValue.un.linearAcceleration.y;
        acz = sensorValue.un.linearAcceleration.z;

        if (acx < 0.05) {
            acx = 0;
          }
        if (acy < 0.05) {
            acy = 0;
          }
        if (acz < 0.05) {
            acz = 0;
          }

        break;

      }

    // Calculate time since last loop iteration
    currentTime = millis();
    float dt = (currentTime - prevTime) / 1000.0; // Convert to seconds

    // Integrate linear acceleration to get velocity
    velocityX += acx * dt;
    velocityY += acy * dt;
    velocityZ += acz * dt;

    // Integrate velocity to get position
    positionX += velocityX * dt;
    positionY += velocityY * dt;
    positionZ += velocityZ * dt;

    prevTime = currentTime;

    // Calculate relative Euler angles from origin
    ypr.yaw -= originYPR.yaw;
    ypr.pitch -= originYPR.pitch;
    ypr.roll -= originYPR.roll;
  }

  // Create a JSON object
  StaticJsonDocument<200> doc;

  // Add data to the JSON object
  doc["Item1"] = positionX;
  doc["Item2"] = positionY;
  doc["Item3"] = positionZ;
  doc["Item4"] = ypr.yaw;
  doc["Item5"] = ypr.roll; // giving value pitch
  doc["Item6"] = ypr.pitch; // giving value roll

  // Serialize the JSON object to a string
  String jsonString;
  serializeJson(doc, jsonString);

  // Send the JSON string over serial
  Serial.println(jsonString);
}
