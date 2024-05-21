#include <Wire.h>
#include <Adafruit_BNO08x.h>
#include <ArduinoJson.h>

#define BNO08X_CS 10
#define BNO08X_INT 9
#define BNO08X_RESET -1

Adafruit_BNO08x bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

// Struct for Euler angles
struct euler_t {
  float yaw;
  float pitch;
  float roll;
} ypr, previousYPR, deltaYPR;

bool originSet = false;
euler_t originYPR;

#ifdef FAST_MODE
  sh2_SensorId_t reportType = SH2_GYRO_INTEGRATED_RV;
  long reportIntervalUs = 2000;
#else
  sh2_SensorId_t reportType = SH2_ROTATION_VECTOR;
  long reportIntervalUs = 5000;
#endif

float position[3] = {0, 0, 0};
float velocity[3] = {0, 0, 0};
unsigned long lastUpdate = 0;

void setReports(sh2_SensorId_t reportType, long report_interval) {
  if (!bno08x.enableReport(reportType, report_interval)) {
    Serial.println("Could not enable report");
  }
}

void quaternionToEuler(float qr, float qi, float qj, float qk, euler_t* ypr, bool degrees = false) {
  float t = qi; qi = qj; qj = t; qk = -qk;

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
  if (!bno08x.begin_I2C()) {
    Serial.println("Failed to find BNO08x chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("BNO08x Found!");

  setReports(reportType, reportIntervalUs);

  // Serial for testing
  Serial.begin(9600);

  delay(500);

  // Enable linear acceleration report
  if (!bno08x.enableReport(SH2_LINEAR_ACCELERATION)) {
    Serial.println("Could not enable linear acceleration");
  }

  lastUpdate = millis();
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
    // Get current time
    unsigned long currentTime = millis();
    float dt = (currentTime - lastUpdate) / 1000.0; // convert ms to seconds
    lastUpdate = currentTime;

    // Read linear acceleration
    float ax = sensorValue.un.linearAcceleration.x;
    float ay = sensorValue.un.linearAcceleration.y;
    float az = sensorValue.un.linearAcceleration.z;
    float gx = sensorValue.un.gyroscope.x;
    float gy = sensorValue.un.gyroscope.y;
    float gz = sensorValue.un.gyroscope.z;

    // Calculate increments (changes) from the previous readings
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
    }

    // Calculate relative Euler angles from origin
    ypr.yaw -= originYPR.yaw;
    ypr.pitch -= originYPR.pitch;
    ypr.roll -= originYPR.roll;

    // Calculate increments (changes) from the previous readings
    deltaYPR.yaw = ypr.yaw - previousYPR.yaw;
    deltaYPR.pitch = ypr.pitch - previousYPR.pitch;
    deltaYPR.roll = ypr.roll - previousYPR.roll;

    if (abs(deltaYPR.yaw) < 0.01 ) {
      deltaYPR.yaw = 0;
    } //else if (abs(deltaYPR.yaw) > 10) {
    //   deltaYPR.yaw = 10;
    // }

    if (abs(deltaYPR.pitch) < 0.01 ) {
      deltaYPR.pitch = 0;
    } //else if (abs(deltaYPR.pitch) > 10) {
    //   deltaYPR.pitch = 10;
    // }

    if (abs(deltaYPR.roll) < 0.01 ) {
      deltaYPR.roll = 0;
    } else if (abs(deltaYPR.roll) > 10) {
      deltaYPR.roll = 10;
    }

    // Calculate acceleration with threshold
    float bx = ax * 0.1;
    float by = ay * 0.1;
    float bz = az * 0.1;

    float cx = deltaYPR.yaw * 0.1;
    float cy = deltaYPR.pitch * 0.1;
    float cz = deltaYPR.roll * 0.1;

    // Create a JSON object
    StaticJsonDocument<200> doc;

    // Add data to the JSON object
    doc["Item1"] = bx;
    doc["Item2"] = by;
    doc["Item3"] = bz;
    doc["Item4"] = gz;
    doc["Item5"] = gy;
    doc["Item6"] = gx;

    // Serialize the JSON object to a string
    String jsonString;
    serializeJson(doc, jsonString);

    // Send the JSON string over serial
    Serial.println(jsonString);
  }
}