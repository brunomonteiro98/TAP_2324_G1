#include <Arduino.h>
#include <Adafruit_BNO08x.h>

#define BNO08X_CS 10
#define BNO08X_INT 9
#define BNO08X_RESET -1

Adafruit_BNO08x  bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

sh2_SensorId_t reportTypeLA = SH2_LINEAR_ACCELERATION;
long reportIntervalUsLA = 5000;
sh2_SensorId_t reportTypeAV = SH2_GYROSCOPE_CALIBRATED;
long reportIntervalUsAV = 5000;

void setReports(sh2_SensorId_t reportType, long report_interval) {
  Serial.println("Setting desired reports");
  if (! bno08x.enableReport(reportType, report_interval)) {
    Serial.println("Could not enable stabilized remote vector");
  }
}

void setup(void) {

  Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println("Adafruit BNO08x test!");

  if (!bno08x.begin_I2C()) {
    Serial.println("Failed to find BNO08x chip");
    while (1) { delay(10); }
  }
  Serial.println("BNO08x Found!");

  setReports(reportTypeLA, reportIntervalUsLA);
  setReports(reportTypeAV, reportIntervalUsAV);

  Serial.println("Reading events");
  delay(100);
}

void loop() {

  if (bno08x.wasReset()) {
    Serial.print("sensor was reset ");
    setReports(reportTypeLA, reportIntervalUsLA);
    setReports(reportTypeAV, reportIntervalUsAV);
  }

  if (bno08x.getSensorEvent(&sensorValue)) {

    // Read linear accelerations (m/s^2)
    float lax = sensorValue.un.linearAcceleration.x;
    float lay = sensorValue.un.linearAcceleration.y;
    float laz = sensorValue.un.linearAcceleration.z;

    // Read angular velocities (rad/s)
    float avx = sensorValue.un.gyroscope.x;
    float avy = sensorValue.un.gyroscope.y;
    float avz = sensorValue.un.gyroscope.z;

// Low pass filter for accelerations and velocities
    if (abs(lax) < 0.01 ) {
      lax = 0;
    }
    if (abs(lay) < 0.01 ) {
      lay = 0;
    }
    if (abs(laz) < 0.01 ) {
      laz = 0;
    }
    if (abs(avx) < 0.01 ) {
      avx = 0;
    }
    if (abs(avy) < 0.01 ) {
      avy = 0;
    }
    if (abs(avz) < 0.01 ) {
      avz = 0;
    }


    // High pass filter for accelerations and velocities
    if (abs(lax) > 10 ) {
      lax = 10;
    }
    if (abs(lay) > 10 ) {
      lay = 10;
    }
    if (abs(laz) > 10 ) {
      laz = 10;
    }
    if (abs(avx) > 10 ) {
      avx = 10;
    }
    if (abs(avy) > 10 ) {
      avy = 10;
    }
    if (abs(avz) > 10 ) {
      avz = 10;
    }

    // Calculate velocity adjusted (degrees/s) !!! Verificar a passagem de rad/s para degrees/s se interfere no calculate position (verificar valores)
    float avax = avx * 0.1 * 180 / 3.14159;
    float avay = avy * 0.1 * 180 / 3.14159;
    float avaz = avz * 0.1 * 180 / 3.14159;

    // Calculate accelerations adjusted (m/s^2)
    float laax = lax * 0.1;
    float laay = lay * 0.1;
    float laaz = laz * 0.1;

    static long last = 0;
    long now = micros();
    last = now;
    // Para debug
    // Serial.println("Execution time: ", now - last);
    // String send;
    // send = "Accuracy (0-3): " + String(sensorValue.status);
    // Serial.println(send);
    // send = "Angular velocity: " + String(avx) + "," + String(avy) + "," + String(avz);
    // Serial.println(send);
    // send = "Angular velocity adjusted: " + String(avax) + "," + String(avay) + "," + String(avaz);
    // Serial.println(send);
    // send = "Linear acceleration: " + String(lax) + "," + String(lay) + "," + String(laz);
    // Serial.println(send);               
    // send = "Linear acceleration adjusted: " + String(laax) + "," + String(laay) + "," + String(laaz);  
    // Serial.println(send);  
    // delay(1000);

    String data;
    data = String(laax) + "," + String(laay) + "," + String(laaz) + "," + String(avax) + "," + String(avay) + "," + String(avaz) + "," + String(now - last);
    Serial.println(data);
  }
}
