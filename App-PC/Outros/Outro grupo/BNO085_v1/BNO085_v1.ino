// Basic demo for readings from Adafruit BNO08x
#include <Adafruit_BNO08x.h>

////////// Display
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
////////// Display

// For SPI mode, we need a CS pin
#define BNO08X_CS 10
#define BNO08X_INT 9

// For SPI mode, we also need a RESET
//#define BNO08X_RESET 5
// but not for I2C or UART
#define BNO08X_RESET -1

////////// Display
#define SCREEN_WIDTH 128  // OLED display width, in pixels
#define SCREEN_HEIGHT 32  // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The pins for I2C are defined by the Wire-library.
// On an arduino UNO:       A4(SDA), A5(SCL)
// On an arduino MEGA 2560: 20(SDA), 21(SCL)
// On an arduino LEONARDO:   2(SDA),  3(SCL), ...
#define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C  ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define NUMFLAKES 10  // Number of snowflakes in the animation example

#define LOGO_HEIGHT 16
#define LOGO_WIDTH 16
static const unsigned char PROGMEM logo_bmp[] = { 0b00000000, 0b11000000,
                                                  0b00000001, 0b11000000,
                                                  0b00000001, 0b11000000,
                                                  0b00000011, 0b11100000,
                                                  0b11110011, 0b11100000,
                                                  0b11111110, 0b11111000,
                                                  0b01111110, 0b11111111,
                                                  0b00110011, 0b10011111,
                                                  0b00011111, 0b11111100,
                                                  0b00001101, 0b01110000,
                                                  0b00011011, 0b10100000,
                                                  0b00111111, 0b11100000,
                                                  0b00111111, 0b11110000,
                                                  0b01111100, 0b11110000,
                                                  0b01110000, 0b01110000,
                                                  0b00000000, 0b00110000 };
////////// Display

Adafruit_BNO08x bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

// Variables definitions

float acceleration[3];

float accelerationsum[3];

float accelerationoffset[3] = { 0, 0, 0 };

float finalacceleration[3] = { 0, 0, 0 };

float velocity[3] = { 0, 0, 0 };  // Initialize with zero velocity

float position[3] = { 0, 0, 0 };  // Initialize with zero position

unsigned long priorTime = 0;
unsigned long it = 0;  // Integration interval in milliseconds
unsigned long currentTime;

void setup(void) {
  Serial.begin(115200);

  ////////// Display
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;  // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(2000);  // Pause for 2 seconds

  // Clear the buffer
  display.clearDisplay();

  // Show the display buffer on the screen. You MUST call display() after
  // drawing commands to make them visible on screen!
  display.display();
  delay(2000);
  // display.display() is NOT necessary after every single drawing command,
  // unless that's what you want...rather, you can batch up a bunch of
  // drawing operations and then update the screen all at once by calling
  // display.display(). These examples demonstrate both approaches...


  // Invert and restore display, pausing in-between
  display.invertDisplay(true);
  delay(1000);
  display.invertDisplay(false);
  delay(1000);
  ////////// Display

  while (!Serial)
    delay(10);  // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit BNO08x test!");

  // Try to initialize!
  if (!bno08x.begin_I2C()) {
    // if (!bno08x.begin_UART(&Serial1)) {  // Requires a device with > 300 byte
    // UART buffer! if (!bno08x.begin_SPI(BNO08X_CS, BNO08X_INT)) {
    Serial.println("Failed to find BNO08x chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("BNO08x Found!");

    for (int n = 0; n < bno08x.prodIds.numEntries; n++) {
    Serial.print("Part ");
    Serial.print(bno08x.prodIds.entry[n].swPartNumber);
    Serial.print(": Version :");
    Serial.print(bno08x.prodIds.entry[n].swVersionMajor);
    Serial.print(".");
    Serial.print(bno08x.prodIds.entry[n].swVersionMinor);
    Serial.print(".");
    Serial.print(bno08x.prodIds.entry[n].swVersionPatch);
    Serial.print(" Build ");
    Serial.println(bno08x.prodIds.entry[n].swBuildNumber);
    
  }

  setReports();

  for (int i = 0; i < 2000; i++) {
    while (!bno08x.getSensorEvent(&sensorValue)) {
    }
    acceleration[0] = (sensorValue.un.linearAcceleration.x);
    acceleration[1] = (sensorValue.un.linearAcceleration.y);
    acceleration[2] = (sensorValue.un.linearAcceleration.z);
    for (int j = 0; j < 3; j++) {
      accelerationsum[j] += acceleration[j];
    }
  }

  accelerationoffset[0] = accelerationsum[0] / 2000;
  accelerationoffset[1] = accelerationsum[1] / 2000;
  accelerationoffset[2] = accelerationsum[2] / 2000;

  Serial.println("Offset em x: ");
  Serial.println( accelerationoffset[0], 4);
  Serial.println("Offset em y: ");
  Serial.println(accelerationoffset[1], 4);
  Serial.println("Offset em z: ");
  Serial.println(accelerationoffset[2], 4);

  Serial.println("Reading events");
  delay(2000);
  priorTime = micros();

}
// Here is where you define the sensor outputs you want to receive
void setReports(void) {
  Serial.println("Setting desired reports");
  if (!bno08x.enableReport(SH2_LINEAR_ACCELERATION)) {
    Serial.println("Could not enable linear acceleration");
  }
}

void loop() {

  if (bno08x.wasReset()) {
    Serial.print("sensor was reset ");
    setReports();
  }

  // if (~(!bno08x.getSensorEvent(&sensorValue))) {
    
  //   Serial.println("Não");
  // }

  
  // while ((!bno08x.getSensorEvent(&sensorValue))) {
  //   Serial.println("not");
  // }

  float a = acceleration[0];

  acceleration[0] = (sensorValue.un.linearAcceleration.x);
  acceleration[1] = (sensorValue.un.linearAcceleration.y);
  acceleration[2] = (sensorValue.un.linearAcceleration.z);

  currentTime = micros();
  it = currentTime - priorTime;
  priorTime = currentTime;

  for (int i = 0; i < 3; i++) { 
    finalacceleration[i] = (acceleration[i]-accelerationoffset[i]);
  }

  
  if (abs(finalacceleration[0]) > abs(20*a) ){ 
      finalacceleration[0] = a;
      Serial.print("acelerou muito");
  }

  if (abs(finalacceleration[0]) < abs(a/20) ){ 
      finalacceleration[0] = a;
      Serial.print("travou muito");
  }

  for (int i = 0; i < 3; i++) {
    if (finalacceleration[i] <= 0.04 & finalacceleration[i] >= -0.04) {
      finalacceleration[i] = 0;
    }
  }

  for (int i = 0; i < 3; i++) {
    if (velocity[i] <= 0.0 & velocity[i] >= -0.0) {
      velocity[i] = 0;
    }
  }

  for (int i = 0; i < 3; i++) {
    velocity[i] = (velocity[i] / 100 + (finalacceleration[i]) * (it / 1000000.0)) * 100;
  }

  // for (int i = 0; i < 3; i++) {
  //   position[i] = position[i] + (velocity[i]) * (it / 1000.0);
  // }

                          Serial.print("  ");
                          Serial.print("Linear acceleration - x: ");
                          Serial.print(finalacceleration[0],4);
                          Serial.print(" y: ");
                          Serial.print(finalacceleration[1],4);
                          Serial.print(" z: ");
                          Serial.print(finalacceleration[2],4);
                          Serial.println("  ");

                          Serial.print("  ");
                          Serial.print("Linear Velocity - x: ");
                          Serial.print(velocity[0]);
                          Serial.print(" y: ");
                          Serial.print(velocity[1]);
                          Serial.print(" z: ");
                          Serial.print(velocity[2]);
                          Serial.println("  ");

  // Serial.print("  ");
  // Serial.print("Position - x: ");
  // Serial.print(position[0]);
  // Serial.print(" y: ");
  // Serial.print(position[1]);
  // Serial.print(" z: ");
  // Serial.print(position[2]);
  // Serial.println("  ");

  //////////////////////////////////
  //////////////////////////////////
  //////////////////////////////////

  ////////// Display acel
  // display.clearDisplay();

  // display.setTextSize(1);
  // display.setCursor(0, 1);
  // display.setTextColor(WHITE);

  // display.println("ACELERACOES:");

  // display.print("X: ");
  // display.print(finalacceleration[0]);
  // display.println(" m/s^2");
  // display.print("Y: ");
  // display.print(finalacceleration[1]);
  // display.println(" m/s^2");
  // display.print("Z: ");
  // display.print(finalacceleration[2]);
  // display.println(" m/s^2");
  // display.display();
  // ////////// Display

  // // ////////// Display vel
  display.clearDisplay();

  display.setTextSize(1);
  display.setCursor(0, 1);
  display.setTextColor(WHITE);

  display.println("VELOCIDADES:");
  display.print("X: ");
  display.print(velocity[0], 2);
  display.println(" cm/s");
  display.print("Y: ");
  display.print(velocity[1], 2);
  display.println(" cm/s");
  display.print("Z: ");
  display.print(velocity[2], 2);
  display.println(" cm/s");
  display.display();
  // // ////////// Display

  //////// Display pos
  // display.clearDisplay();

  // display.setTextSize(1);
  // display.setCursor(0, 1);
  // display.setTextColor(WHITE);

  // display.println("POSICOES:");
  // display.print("X: ");
  // display.print(position[0]);
  // display.println(" cm");
  // display.print("Y: ");
  // display.print(position[1]);
  // display.println(" cm");
  // display.print("Z: ");
  // display.print(position[2]);
  // display.println(" cm");
  // display.display();
  ////////// Display
}
