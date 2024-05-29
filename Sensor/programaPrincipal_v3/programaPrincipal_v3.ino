#include <Arduino.h>
#include <Adafruit_BNO08x.h>

#define BNO08X_CS 10
#define BNO08X_INT 9
#define BNO08X_RESET -1

struct euler_t {
  float yaw;
  float pitch;
  float roll;
} ypr, previousYPR, deltaYPR;

bool originSet = false;
euler_t originYPR;

Adafruit_BNO08x  bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

sh2_SensorId_t reportTypeXYZ = SH2_LINEAR_ACCELERATION;
long reportIntervalUsXYZ = 5000;
sh2_SensorId_t reportTypeYPR = SH2_ROTATION_VECTOR;
long reportIntervalUsYPR = 5000;

void setReports(sh2_SensorId_t reportType, long report_interval) {
  Serial.println("Setting desired reports");
  if (! bno08x.enableReport(reportType, report_interval)) {
    Serial.println("Could not enable stabilized remote vector");
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

void quaternionToEulerRV(sh2_RotationVectorWAcc_t* rotational_vector, euler_t* ypr, bool degrees = false) {
    quaternionToEuler(rotational_vector->real, rotational_vector->i, rotational_vector->j, rotational_vector->k, ypr, degrees);
}

void setOrigin() {
  if (!originSet && bno08x.getSensorEvent(&sensorValue)) {
    switch (sensorValue.sensorId) {
      case SH2_ROTATION_VECTOR:
        quaternionToEulerRV(&sensorValue.un.rotationVector, &originYPR, true);
    }
    originSet = true;
  }
}

void setup() {

  Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println("Adafruit BNO08x test!");

  if (!bno08x.begin_I2C()) {
    Serial.println("Failed to find BNO08x chip");
    while (1) { delay(10); }
  }
  Serial.println("BNO08x Found!");

  setReports(reportTypeXYZ, reportIntervalUsXYZ);
  setReports(reportTypeYPR, reportIntervalUsYPR);

  Serial.println("Reading events");
  delay(100);
}

void loop() {

  if (bno08x.wasReset()) {
    Serial.print("sensor was reset ");
    setReports(reportTypeXYZ, reportIntervalUsXYZ);
    setReports(reportTypeYPR, reportIntervalUsYPR);
  }
  
  if (!originSet) {
    setOrigin();
    return;
  }

  if (bno08x.getSensorEvent(&sensorValue)) {

    // Read linear accelerations (m/s^2)
    float lax = sensorValue.un.linearAcceleration.x;
    float lay = sensorValue.un.linearAcceleration.y;
    float laz = sensorValue.un.linearAcceleration.z;

    // // Low pass filter for accelerations
    // if (abs(lax) < 0.01 ) {
    //   lax = 0;
    // }
    // if (abs(lay) < 0.01 ) {
    //   lay = 0;
    // }
    // if (abs(laz) < 0.01 ) {
    //   laz = 0;
    // }

    // // High pass filter for accelerations
    // if (abs(lax) > 10 ) {
    //   lax = 10;
    // }
    // if (abs(lay) > 10 ) {
    //   lay = 10;
    // }
    // if (abs(laz) > 10 ) {
    //   laz = 10;
    // }

    // Calculate accelerations adjusted (m/s^2)
    float laax = lax * 0.1;
    float laay = lay * 0.1;
    float laaz = laz * 0.1;

    switch (sensorValue.sensorId) {
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

    // Store previous YPR values
    previousYPR = ypr;

    // // Low pass filter for increments
    // if (abs(deltaYPR.yaw) < 0.01 ) {
    //   deltaYPR.yaw = 0;
    // }
    // if (abs(deltaYPR.pitch) < 0.01 ) {
    //   deltaYPR.pitch = 0;
    // }
    // if (abs(deltaYPR.roll) < 0.01 ) {
    //   deltaYPR.roll = 0;
    // }

    // // High pass filter for increments
    // if (abs(deltaYPR.yaw) > 10 ) {
    //   deltaYPR.yaw = 10;
    // }
    // if (abs(deltaYPR.pitch) > 10 ) {
    //   deltaYPR.pitch = 10;
    // }
    // if (abs(deltaYPR.roll) > 10 ) {
    //   deltaYPR.roll = 10;
    // }

    // // DeltaYPR ajusted
    // float cx = deltaYPR.yaw * 0.1;
    // float cy = deltaYPR.pitch * 0.1;
    // float cz = deltaYPR.roll * 0.1;

    // Para debug
    // static long last = 0;
    // long now = micros();
    // Serial.println("Execution time: ", now - last);
    // last = now;
    // String send;
    // send = "Accuracy (0-3): " + String(sensorValue.status);
    // Serial.println(send);
    // send = "Linear acceleration: " + String(lax) + "," + String(lay) + "," + String(laz);
    // Serial.println(send);               
    // send = "Linear acceleration adjusted: " + String(laax) + "," + String(laay) + "," + String(laaz);  
    // Serial.println(send); 
    // send = "Increments: " + String(deltaYPR.yaw) + "," + String(deltaYPR.pitch) + "," + String(deltaYPR.roll);  
    // Serial.println(send); 
    // send = "Increments adjusted: " + String(cx) + "," + String(cy) + "," + String(cz);  
    // Serial.println(send); 
    // send = "Angles: " + String(ypr.yaw) + "," + String(ypr.pitch) + "," + String(ypr.roll);  
    // Serial.println(send); 
    // delay(1000);

    // Create a JSON object
    //StaticJsonDocument<200> doc;

    // Add data to the JSON object
    //doc["Item1"] = laax;
    //doc["Item2"] = laay;
    //doc["Item3"] = laaz;
    //doc["Item4"] = deltaYPR.yaw;
    //doc["Item5"] = deltaYPR.pitch;
    //doc["Item6"] = deltaYPR.roll;

    // Serialize the JSON object to a string
    //String jsonString;
    //serializeJson(doc, jsonString);

    // Send the JSON string over serial
    //Serial.println(jsonString);

    String data;
    data = "S" + String(laax) + "," + String(laay) + "," + String(laaz) + "," + String(deltaYPR.yaw) + "," + String(deltaYPR.pitch) + "," + String(deltaYPR.roll);
    Serial.println(data);
  }
}
