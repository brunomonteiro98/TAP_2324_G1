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
long reportIntervalUsLA = 1000;
sh2_SensorId_t reportTypeYPR = SH2_ROTATION_VECTOR;
long reportIntervalUsRV = 5000;

const float accelerationThresholdX = 0.05;
const float accelerationThresholdY = 0.05;
const float accelerationThresholdZ = 0.10;
const int resetThreshold = 10; // Number of consecutive low readings to reset velocity

int lowPassCountX = 0;
int lowPassCountY = 0;
int lowPassCountZ = 0;

const float processNoise = 1e-5; // (+ = adapta-se + rápido mas mais noise; - = mais conservador mas mais lento)
const float measurementNoise = 1e-2; // (+ = confia mais nos dados do sensor; - = contrário)
const float estimationError = 1;
const float initialValue = 0;

bool originSet = false;
bool debug = false;

class KalmanFilter {
private:
  float Q, R, P, x, K;
public:
  KalmanFilter(float Q, float R, float P, float initial_x) {
    this->Q = Q;
    this->R = R;
    this->P = P;
    this->x = initial_x;
  }
  float update(float measurement) {
    this->P += this->Q;
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

void calculate_position(XYZ* speed, XYZ* position, XYZ* positionIncrement, float lax, float lay, float laz, float t) {
  speed->x += lax * t;
  speed->y += lay * t;
  speed->z += laz * t;

  positionIncrement->x = speed->x * t * 1e3; // Convert to mm
  positionIncrement->y = speed->y * t * 1e3; // Convert to mm
  positionIncrement->z = speed->z * t * 1e3; // Convert to mm

  position->x += positionIncrement->x;
  position->y += positionIncrement->y;
  position->z += positionIncrement->z;
}

void calculate_angle_increments(euler_t* yprIncrement) {
  yprIncrement->yaw = ypr.yaw - prevYPR.yaw;
  yprIncrement->pitch = ypr.pitch - prevYPR.pitch;
  yprIncrement->roll = ypr.roll - prevYPR.roll;
  prevYPR = ypr;
}

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  if (!bno08x.begin_I2C()) {
    if (debug) {
      Serial.println("Failed to find BNO08x chip");
    }
    while (1) {
      delay(10);
    }
  }

  delay(1000);
  setReports(reportTypeXYZ, reportIntervalUsLA);
  setReports(reportTypeYPR, reportIntervalUsRV);
}

void loop() {
  float lax, lay, laz;
  long now;
  float t;

  if (bno08x.wasReset()) {
    delay(1000);
    originSet = false;
    setReports(reportTypeXYZ, reportIntervalUsLA);
    setReports(reportTypeYPR, reportIntervalUsRV);
    speed = {0, 0, 0};
    position = {0, 0, 0};
    positionIncrement = {0, 0, 0};
  }

  if (bno08x.getSensorEvent(&sensorValue)) {
    switch (sensorValue.sensorId) {
      case SH2_LINEAR_ACCELERATION:
        lax = sensorValue.un.linearAcceleration.x;
        lay = sensorValue.un.linearAcceleration.y;
        laz = sensorValue.un.linearAcceleration.z;

        if (abs(lax) < accelerationThresholdX) {
          lowPassCountX++;
          if (lowPassCountX >= resetThreshold) {
            speed.x = 0;
            lowPassCountX = 0;
          }
          lax = 0;
        } else {
          lowPassCountX = 0;
        }

        if (abs(lay) < accelerationThresholdY) {
          lowPassCountY++;
          if (lowPassCountY >= resetThreshold) {
            speed.y = 0;
            lowPassCountY = 0;
          }
          lay = 0;
        } else {
          lowPassCountY = 0;
        }

        if (abs(laz) < accelerationThresholdZ) {
          lowPassCountZ++;
          if (lowPassCountZ >= resetThreshold) {
            speed.z = 0;
            lowPassCountZ = 0;
          }
          laz = 0;
        } else {
          lowPassCountZ = 0;
        }

        // Low-pass filter
        lax = lax * 0.25 + kalmanX.update(lax) * 0.75;
        lay = lay * 0.25 + kalmanY.update(lay) * 0.75;
        laz = laz * 0.25 + kalmanZ.update(laz) * 0.75;

        static long last = micros();
        now = micros();
        t = (now - last) / 1e6; // Convert to seconds
        last = now;

        calculate_position(&speed, &position, &positionIncrement, lax, lay, laz, t);
        break;

      case SH2_ROTATION_VECTOR:
        quaternionToEulerRV(&sensorValue.un.rotationVector, &ypr, true);

        if (!originSet) {
          originYPR = ypr;
          originSet = true;
          break;
        } else {
          ypr.yaw -= originYPR.yaw;
          ypr.pitch -= originYPR.pitch;
          ypr.roll -= originYPR.roll;

          if (ypr.yaw < -180) ypr.yaw += 360;
          if (ypr.yaw > 180) ypr.yaw -= 360;
          if (ypr.pitch < -180) ypr.pitch += 360;
          if (ypr.pitch > 180) ypr.pitch -= 360;
          if (ypr.roll < -180) ypr.roll += 360;
          if (ypr.roll > 180) ypr.roll -= 360;
        }

        calculate_angle_increments(&yprIncrement);
        break;
    }

    String data;
    data = String(positionIncrement.x,10) + "," + String(positionIncrement.y,10) + "," + String(positionIncrement.z,10) + "," + String(yprIncrement.yaw,10) + "," + String(yprIncrement.pitch,10) + "," + String(yprIncrement.roll,10);
    //data = String(position.x,10) + "," + String(position.y,10) + "," + String(position.z,10) + "," + String(ypr.yaw,10) + "," + String(ypr.pitch,10) + "," + String(ypr.roll,10);
    Serial.println(data);
  }}
