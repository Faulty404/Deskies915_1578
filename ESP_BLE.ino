#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b" // Custom Service UUID
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8" // Custom Characteristic UUID
#define MOTOR_PIN 16 // Pin where the motor is connected
#define BUTTON_PIN 23 // Pin where the button is connected

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Reset pin (use -1 if not connected)
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

bool motorOn = false; // Track motor state

// Callback class to handle incoming data
class MyCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
    String value = pCharacteristic->getValue();

    if (value.length() > 0) {
      Serial.print("Received Value: ");
      Serial.println(value);

      int motorSpeed = value.toInt() * 80; // Scale the input (0-3) to PWM range
      analogWrite(MOTOR_PIN, motorSpeed);
      delay(1000);
      analogWrite(MOTOR_PIN, 0);


      // Clear the display before writing new text
      display.clearDisplay();
      display.setTextSize(2);        // Text size (1 = small, 2 = medium, etc.)
      display.setTextColor(SSD1306_WHITE); // White text color
      display.setCursor(10, 25);     // Set the cursor position (x, y)
      display.print("Speed: ");
      display.print(motorSpeed);

      // Refresh the display with new content
      display.display();
    }
  }
};

void setup() {
  Serial.begin(115200);
  Serial.println("Starting BLE...");

  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Configure button pin with pull-up resistor
  analogWrite(MOTOR_PIN, 0);   // Initially turn off the motor

  // Initialize OLED display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // 0x3C is the I2C address for most OLEDs
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); // Loop forever if display initialization fails
  }

  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 25);
  display.println(F("Hello, World!"));
  display.display();

  // Initialize BLE
  BLEDevice::init("ESP32_BLE_Receiver");
  BLEServer *pServer = BLEDevice::createServer();

  // Create BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create BLE Characteristic
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
                                        CHARACTERISTIC_UUID,
                                        BLECharacteristic::PROPERTY_READ |
                                        BLECharacteristic::PROPERTY_WRITE
                                      );

  // Set callback for receiving data
  pCharacteristic->setCallbacks(new MyCallbacks());

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();

  Serial.println("Waiting for connections...");
}

void loop() {
  // Check if the button is pressed
  if (digitalRead(BUTTON_PIN) == LOW) { // Button pressed
    delay(50); // Debounce delay
    while (digitalRead(BUTTON_PIN) == LOW); // Wait for button release

    motorOn = !motorOn; // Toggle motor state

    if (motorOn) {
      analogWrite(MOTOR_PIN, 255); // Turn motor on full speed
      Serial.println("Motor ON");
    } else {
      analogWrite(MOTOR_PIN, 0); // Turn motor off
      Serial.println("Motor OFF");
    }

    // Update display
    display.clearDisplay();
    display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(10, 25);
    if (motorOn) {
      display.print(F("Motor: ON"));
    } else {
      display.print(F("Motor: OFF"));
    }
    display.display();
  }

  delay(200); // Small delay for stability
}
