#include <Arduino.h>
#include <Adafruit_BNO08x.h>

#define BNO08X_CS 10
#define BNO08X_INT 9
#define BNO08X_RESET -1

struct euler_t {
  float yaw;
  float pitch;
  float roll;
} ypr, originYPR, prevYPR, yprIncrement;

struct XYZ {
  float x;
  float y;
  float z;
} speed = {0, 0, 0}, position = {0, 0, 0}, positionIncrement = {0, 0, 0};

Adafruit_BNO08x bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

sh2_SensorId_t reportTypeXYZ = SH2_LINEAR_ACCELERATION;
long reportIntervalUsXYZ = 4000;
sh2_SensorId_t reportTypeYPR = SH2_ROTATION_VECTOR;
long reportIntervalUsYPR = 4000;

bool originSet = false; // Flag to check if origin is set
bool debug = false; // Set this to true to enable debug prints, false to disable

const float stationaryThreshold = 0.05; // To know if isStationary  MODIFICAR
const int resetThreshold = 10;  // Number of consecutive low readings to reset velocity MODIFICAR
int lowPassCount = 0;

const float processNoise = 1e-5;  // 1e-5  MODIFICAR
const float measurementNoise = 1e-2;  // 1e-2  MODIFICAR
const float estimationError = 1;  // 1
const float initialValue = 0;  // 0

class KalmanFilter {
private:
  float Q, R, P, x, K;
public:
  KalmanFilter(float Q, float R, float P, float initial_x) {
    this->Q = Q; // Process noise covariance (+ = adapta-se + rápido mas mais noise; - = mais conservador mas mais lento)!
    this->R = R; // Measurement noise covariance (+ = confia mais nos dados do sensor; - = contrário)!
    this->P = P; // Estimation error covariance
    this->x = initial_x; // Initial value of the estimated signal
  }
  float update(float measurement) {
    // Prediction update
    this->P += this->Q;
    
    // Measurement update
    this->K = this->P / (this->P + this->R);
    this->x += this->K * (measurement - this->x);
    this->P *= (1 - this->K);
    
    return this->x;
  }
};

KalmanFilter kalmanX(processNoise, measurementNoise, estimationError, initialValue);
KalmanFilter kalmanY(processNoise, measurementNoise, estimationError, initialValue);
KalmanFilter kalmanZ(processNoise, measurementNoise, estimationError, initialValue);

void setReports(sh2_SensorId_t reportType, long report_interval) {
  if (debug) {
    Serial.println("Setting desired reports");
  }
  if (!bno08x.enableReport(reportType, report_interval)) {
    if (debug) {
      Serial.println("Could not enable report");
    }
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

void calculate_position(XYZ* speed, XYZ* position, XYZ* positionIncrement, euler_t* yprIncrement, float lax, float lay, float laz, float t) {
  speed->x += lax * t;
  speed->y += lay * t;
  speed->z += laz * t;

  positionIncrement->x = speed->x * t * 1e3; // Convert to mm
  positionIncrement->y = speed->y * t * 1e3; // Convert to mm
  positionIncrement->z = speed->z * t * 1e3; // Convert to mm

  position->x += positionIncrement->x;
  position->y += positionIncrement->y;
  position->z += positionIncrement->z;

  // Calculate yaw, pitch, and roll increments
  yprIncrement->yaw = ypr.yaw - prevYPR.yaw;
  yprIncrement->pitch = ypr.pitch - prevYPR.pitch;
  yprIncrement->roll = ypr.roll - prevYPR.roll;

  // Update previous yaw, pitch, and roll values for next iteration
  prevYPR = ypr;
}

bool isStationary(float ax, float ay, float az) {
  // return (abs(ax) < stationaryThreshold) && (abs(ay) < stationaryThreshold) && (abs(az) < stationaryThreshold);
  return (abs(ax) < stationaryThreshold) && (abs(ay) < stationaryThreshold);
}

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  if (debug) {
    Serial.println("Adafruit BNO08x test!");
  }

  if (!bno08x.begin_I2C()) {
    if (debug) {
      Serial.println("Failed to find BNO08x chip");
    }
    while (1) { delay(10); }
  }
  
  if (debug) {
    Serial.println("BNO08x Found!");
  }

  // Ensure sensor stabilization before setting origin
  delay(1000);

  setReports(reportTypeXYZ, reportIntervalUsXYZ);
  setReports(reportTypeYPR, reportIntervalUsYPR);

  if (debug) {
    Serial.println("Reading events");
  }
}

void loop() {
  if (bno08x.wasReset()) {
    if (debug) {
      Serial.println("Sensor was reset");
    }
    delay(1000); // Allow sensor to stabilize
    originSet = false; // Reset originSet flag
    setReports(reportTypeXYZ, reportIntervalUsXYZ);
    setReports(reportTypeYPR, reportIntervalUsYPR);

    // Reset position and speed
    speed = {0, 0, 0};
    position = {0, 0, 0};
    positionIncrement = {0, 0, 0};
  }

  if (bno08x.getSensorEvent(&sensorValue)) {
    switch (sensorValue.sensorId) {
      case SH2_ROTATION_VECTOR:
        quaternionToEulerRV(&sensorValue.un.rotationVector, &ypr, true);

        if (!originSet) {
          originYPR = ypr;
          originSet = true;
          if (debug) {
            Serial.print("Origin set to: ");
            Serial.print("Yaw: "); Serial.print(originYPR.yaw);
            Serial.print(", Pitch: "); Serial.print(originYPR.pitch);
            Serial.print(", Roll: "); Serial.println(originYPR.roll);
          }
          break; // Exit switch case
        } else {
          // Calculate relative Euler angles from origin
          ypr.yaw -= originYPR.yaw;
          ypr.pitch -= originYPR.pitch;
          ypr.roll -= originYPR.roll;
          
          // // Ensure angles are within -180 to 180 degrees
          // if (ypr.yaw < -180) ypr.yaw += 360;
          // if (ypr.yaw > 180) ypr.yaw -= 360;
          // if (ypr.pitch < -180) ypr.pitch += 360;
          // if (ypr.pitch > 180) ypr.pitch -= 360;
          // if (ypr.roll < -180) ypr.roll += 360;
          // if (ypr.roll > 180) ypr.roll -= 360;
        }
        break;
    }

    // Read linear accelerations (m/s^2)
    float lax = sensorValue.un.linearAcceleration.x;
    float lay = sensorValue.un.linearAcceleration.y;
    float laz = sensorValue.un.linearAcceleration.z;

    static long last = 0;
    if (last == 0) {
      last = micros();
    }
    long now = micros();
    float t = (now - last) / 1e6; // Convert to seconds
    last = now;

    // Check if the sensor is stationary
    if (!isStationary(lax, lay, laz)) {
      lax = kalmanX.update(lax);
      lay = kalmanX.update(lay);
      laz = kalmanX.update(laz);

      calculate_position(&speed, &position, &positionIncrement, &yprIncrement, lax, lay, laz, t);
    } else {
      lowPassCount++;
      if (lowPassCount >= resetThreshold) {
        speed = {0, 0, 0};
        lowPassCount = 0;
      } else {
        lowPassCount = 0;
      }
    }

    if (debug) {
      // For debugging
      String send;
      // send = "Accuracy (0-3): " + String(sensorValue.status);
      // Serial.println(send);
      send = "Linear acceleration: " + String(lax) + "," + String(lay) + "," + String(laz);
      Serial.println(send);
      send = "Increments: " + String(positionIncrement.x) + "," + String(positionIncrement.y) + "," + String(positionIncrement.z);
      Serial.println(send);
      // send = "Angles: " + String(ypr.yaw) + "," + String(ypr.pitch) + "," + String(ypr.roll);
      // Serial.println(send);
      // send = "Angle Increments: " + String(yprIncrement.yaw) + "," + String(yprIncrement.pitch) + "," + String(yprIncrement.roll);
      // Serial.println(send);
      delay(500);
    }

    String data;
    // data = String(positionIncrement.x) + "," + String(positionIncrement.y) + "," + String(positionIncrement.z) + "," + String(yprIncrement.yaw) + "," + String(yprIncrement.pitch) + "," + String(yprIncrement.roll);
    data = String(position.x) + "," + String(position.y) + "," + String(position.z) + "," + String(ypr.yaw) + "," + String(ypr.pitch) + "," + String(ypr.roll);
    Serial.println(data);
  } else {
    if (debug) {
      Serial.println("No sensor event received.");
    }
  }
}

