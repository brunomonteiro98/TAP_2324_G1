#include <Adafruit_ICM20X.h>
#include <Adafruit_ICM20948.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_ICM20948 icm;
uint16_t measurement_delay_us = 65535; // Delay between measurements for testing

#define SCREEN_WIDTH 128      // OLED display width, in pixels
#define SCREEN_HEIGHT 64      // OLED display height, in pixels
#define OLED_RESET    -1      // Reset pin # (or -1 if sharing Arduino reset pin)

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit ICM20948 test!");

  Wire.begin();          // Initialize I2C communication

  if (!icm.begin_I2C()) {
    Serial.println("Failed to find ICM20948 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("ICM20948 Found!");

  Serial.print("Accelerometer range set to: ");
  switch (icm.getAccelRange()) {
    case ICM20948_ACCEL_RANGE_2_G:
      Serial.println("+-2G");
      break;
    case ICM20948_ACCEL_RANGE_4_G:
      Serial.println("+-4G");
      break;
    case ICM20948_ACCEL_RANGE_8_G:
      Serial.println("+-8G");
      break;
    case ICM20948_ACCEL_RANGE_16_G:
      Serial.println("+-16G");
      break;
  }
  Serial.println("OK");

  Serial.print("Gyro range set to: ");
  switch (icm.getGyroRange()) {
    case ICM20948_GYRO_RANGE_250_DPS:
      Serial.println("250 degrees/s");
      break;
    case ICM20948_GYRO_RANGE_500_DPS:
      Serial.println("500 degrees/s");
      break;
    case ICM20948_GYRO_RANGE_1000_DPS:
      Serial.println("1000 degrees/s");
      break;
    case ICM20948_GYRO_RANGE_2000_DPS:
      Serial.println("2000 degrees/s");
      break;
  }

  uint16_t accel_divisor = icm.getAccelRateDivisor();
  float accel_rate = 1125 / (1.0 + accel_divisor);

  Serial.print("Accelerometer data rate divisor set to: ");
  Serial.println(accel_divisor);
  Serial.print("Accelerometer data rate (Hz) is approximately: ");
  Serial.println(accel_rate);

  uint8_t gyro_divisor = icm.getGyroRateDivisor();
  float gyro_rate = 1100 / (1.0 + gyro_divisor);

  Serial.print("Gyro data rate divisor set to: ");
  Serial.println(gyro_divisor);
  Serial.print("Gyro data rate (Hz) is approximately: ");
  Serial.println(gyro_rate);

  Serial.print("Magnetometer data rate set to: ");
  switch (icm.getMagDataRate()) {
    case AK09916_MAG_DATARATE_SHUTDOWN:
      Serial.println("Shutdown");
      break;
    case AK09916_MAG_DATARATE_SINGLE:
      Serial.println("Single/One shot");
      break;
    case AK09916_MAG_DATARATE_10_HZ:
      Serial.println("10 Hz");
      break;
    case AK09916_MAG_DATARATE_20_HZ:
      Serial.println("20 Hz");
      break;
    case AK09916_MAG_DATARATE_50_HZ:
      Serial.println("50 Hz");
      break;
    case AK09916_MAG_DATARATE_100_HZ:
      Serial.println("100 Hz");
      break;
  }
  Serial.println();

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // Initialize OLED display
}

void loop() {
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t mag;
  sensors_event_t temp;
  icm.getEvent(&accel, &gyro, &temp, &mag);

  Serial.print("\t\tTemperature ");
  Serial.print(temp.temperature);
  Serial.println(" deg C");

  Serial.print("\t\tAccel X: ");
  Serial.print(accel.acceleration.x);
  Serial.print(" \tY: ");
  Serial.print(accel.acceleration.y);
  Serial.print(" \tZ: ");
  Serial.print(accel.acceleration.z);
  Serial.println(" m/s^2 ");

  Serial.print("\t\tMag X: ");
  Serial.print(mag.magnetic.x);
  Serial.print(" \tY: ");
  Serial.print(mag.magnetic.y);
  Serial.print(" \tZ: ");
  Serial.print(mag.magnetic.z);
  Serial.println(" uT");

  Serial.print("\t\tGyro X: ");
  Serial.print(gyro.gyro.x);
  Serial.print(" \tY: ");
  Serial.print(gyro.gyro.y);
  Serial.print(" \tZ: ");
  Serial.print(gyro.gyro.z);
  Serial.println(" radians/s ");
  Serial.println();

  delay(100);

  // Read accelerometer values from the ICM20948 sensor
  float accelerationX = accel.acceleration.x ;
  float accelerationY = accel.acceleration.y ;
  float accelerationZ = accel.acceleration.z ;

  // Display accelerometer values on OLED display
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print("Acc X: ");
  display.println(accelerationX);
  display.print("Acc Y: ");
  display.println(accelerationY);
  display.print("Acc Z: ");
  display.println(accelerationZ);
  display.display();

  delay(100);  // Delay between readings
}