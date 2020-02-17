/* ============================================
Feinstaubboxen Schelztor-Gymnasium Arduino Script
     (c) 2020 F.Bisinger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
===============================================
*/

/*
 *   The circuit:
 *   
 *   SD card attached to SPI bus as follows:
 *   MOSI - pin D11 on Arduino Nano
 *   MISO - pin D12 on Arduino Nano
 *   SCK - pin D13 on Arduino Nano
 *   CS - depends on your SD card shield or module. (D10)
 *   
 *   DHT22 attached as follows:
 *   Data - pin D2 on Arduino Nano
 *   
 *   DS3231(RTC) attached as follows:
 *   SDA - pin A4 on Arduino Nano
 *   SCL - pin A5 on Arduino Nano
 *   
 *   SDS011(Particle Sensor) attached as follows:
 *   TXD - pin D5 on Arduino Nano
 *   RXD - pin D6 on Arduino Nano
 *   
 *   LEDs attached as follows:
 *   LED_RED - pin D3 on Arduino Nano
 *   LED_GREEN - pin D4 on Arduino Nano
 */

// Librarys
  // include the SD library:
  #include <SPI.h>
  #include <SD.h>
  // include the DS3231 library:
  #include <DS3231.h>
  // include the DHT22 library:
  #include <DHT.h>
  // include the SDS011 library:
  #include <SDS011.h>
  // include start-up credentials:
  #include "info.h"
  // Init the DS3231 using the hardware interface:
  DS3231  rtc(SDA, SCL);
  // Init the SDS011:
  SDS011 pm_sensor;

// Constants
  // CS pin for SD card reader
  const int chipSelect = 10;
  // Pin which is connected to the DHT sensor.
  #define DHTPIN            2

  // Uncomment the type of sensor in use:
  //#define DHTTYPE           DHT11     // DHT 11 
  #define DHTTYPE           DHT22     // DHT 22 (AM2302)
  //#define DHTTYPE           DHT21     // DHT 21 (AM2301)
  // Initialize DHT sensor
  DHT dht(DHTPIN, DHTTYPE);
  // Variables to store pm measurements
  float pm10,pm25;
  // Variable to store filename
  String fileName;
  // boolean for cr
  boolean cr = true;
  // Variables for status LEDs
  int LED_RED = 3;
  int LED_GREEN = 4;

// Options: Uncomment this if you want to use the SDS011 sleep mode capabilities 
//(leads to: longer battery life & longer lifetime of the sensor)
//  #define SLEEPMODE
  
void setup() {
  // Initialize the rtc object
  rtc.begin();
  // Initialize the dht object
  dht.begin();
  // Initialize the pm_sensor object
  pm_sensor.begin(5,6); //TX,RX
  // define pins
  pinMode(LED_RED,OUTPUT);
  pinMode(LED_GREEN,OUTPUT);
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  // print cr info
  Serial.println(CR);
  
  // create new filename
  String dow = rtc.getDOWStr(FORMAT_SHORT);
  String month = rtc.getMonthStr(FORMAT_SHORT);
  fileName =  month + dow + ".txt";
  
  Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // toggle status LEDs
    digitalWrite(LED_RED,HIGH);
    digitalWrite(LED_GREEN,LOW);
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");
}

void loop() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
  // Measure pm
  if (! pm_sensor.read(&pm25,&pm10)) {        //returns a 0 when reading was successfully
    ;
  }
  
  else {
    Serial.println("Error reading sensor data. Check wiring!");
    }
  
  //short delay
  delay(500);
  
  File dataFile = SD.open(fileName, FILE_WRITE);
  
  if (dataFile) {
    // toggle status LEDs
    digitalWrite(LED_GREEN,HIGH);
    digitalWrite(LED_RED,LOW);
    if(cr == true) {
      dataFile.println(CR);
      dataFile.println(INFO);
      cr = false;
    }
      digitalWrite(LED_GREEN,LOW);
      delay(100);
      dataFile.print(rtc.getDOWStr());
      dataFile.print(" ");
      digitalWrite(LED_GREEN,HIGH);
      delay(100);
      dataFile.print(rtc.getDateStr());
      dataFile.print(" ");
      digitalWrite(LED_GREEN,LOW);
      delay(100);
      dataFile.print(rtc.getTimeStr());
      dataFile.print(",");
      digitalWrite(LED_GREEN,HIGH);
      delay(100);
      dataFile.print(t);
      dataFile.print(",");
      digitalWrite(LED_GREEN,LOW);
      delay(100);
      dataFile.print(h);
      dataFile.print(",");
      digitalWrite(LED_GREEN,HIGH);
      delay(100);
      dataFile.print(pm10);
      dataFile.print(",");
      digitalWrite(LED_GREEN,LOW);
      delay(100);
      dataFile.println(pm25);
      dataFile.close();
      digitalWrite(LED_GREEN,HIGH);
      delay(100);
      
      // print to the serial port too:
      // Send Day-of-Week
      Serial.print(rtc.getDOWStr());
      Serial.print(" ");
      
      // Send date
      Serial.print(rtc.getDateStr());
      Serial.print(" ");
    
      // Send time
      Serial.print(rtc.getTimeStr());

      // Send data
      Serial.print(",");
      Serial.print(t);
      Serial.print(",");
      Serial.print(h);
      Serial.print(",");
      Serial.print(pm10);
      Serial.print(",");
      Serial.println(pm25);
    }
    // if the file isn't open, pop up an error:
    else {
      Serial.println("error opening " + fileName);
      // toggle status LEDs
      digitalWrite(LED_RED,HIGH);
      digitalWrite(LED_GREEN,LOW);
    }
  #ifdef SLEEPMODE
  pm_sensor.sleep();
  delay(55000);                                 //sleeps for 55 seconds (The fan stops spinning & senor turns into sleeping mode => longer lifetime + lower power consumption)
  pm_sensor.wakeup();
  delay(5000);                                  //some reaction time for the sensor
  #endif

  #ifndef SLEEPMODE
  delay(60000);
  #endif
  
}
