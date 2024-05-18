#include <Wire.h>
#include <Adafruit_BNO08x.h>
#include <ArduinoJson.h>

#define BNO08X_RESET -1

Adafruit_BNO08x  bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

struct euler_t {
  float yaw;
  float pitch;
  float roll;
} ypr;


bool originSet = false;
euler_t originYPR;

#ifdef FAST_MODE
  sh2_SensorId_t reportType = SH2_GYRO_INTEGRATED_RV;
  // virgin - 2000
  long reportIntervalUs = 10000;
#else
  sh2_SensorId_t reportType = SH2_ROTATION_VECTOR;
  // virgin - 5000
  long reportIntervalUs = 10000;
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
  Serial.begin(9600,SERIAL_8N1);

  delay(500);
}

void loop() {
  float Y
  float P
  float R
  float YN
  float PN
  float RN
  float IY
  float IP
  float IR

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
    }

    // // Calculate relative Euler angles from origin
    // ypr.yaw -= originYPR.yaw;
    // ypr.pitch -= originYPR.pitch;
    // ypr.roll -= originYPR.roll;
  }

  // // Create a JSON object
  // StaticJsonDocument<200> doc;

  // // Add data to the JSON object
  // doc["Item1"] = 0;
  // doc["Item2"] = 0;
  // doc["Item3"] = 0;
  // doc["Item4"] = ypr.yaw;
  // doc["Item5"] = ypr.roll;
  // doc["Item6"] = ypr.pitch;

  // // Serialize the JSON object to a string
  // String jsonString;
  // serializeJson(doc, jsonString);

  // // Send the JSON string over serial
  // Serial.println(jsonString);

  Y = ypr.yaw;
  P = ypr.pitch;
  R = ypr.roll;

  delay(10);

  YN = ypr.yaw;
  PN = ypr.pitch;
  RN = ypr.roll;

  IY=YN-Y;
  IP=PN-P;
  IR=RN-R;

  String data;
  data = "S" + String(0) + "," + String(0) + "," + String(0) + "," + String(IY) + "," + String(IR) + "," + String(IP);
  Serial.println(data);
  
}
