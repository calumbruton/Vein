/*
TAKEN FROM:
AUTHOR: Hazim Bitar (techbitar)
DATE: Aug 29, 2013

Connect EN to d9 and hold button on HC-05 then plug in usb
TX to D5
RX to D6
*/

#include <SoftwareSerial.h>

SoftwareSerial BTSerial(5, 6); // TX | RX

void setup()
{
  pinMode(9, OUTPUT);  // this pin will pull the HC-05 pin 34 (key pin) HIGH to switch module to AT mode
  digitalWrite(9, HIGH);
  Serial.begin(9600);
  Serial.println("Enter AT commands:");
  BTSerial.begin(38400);  // HC-05 default speed in AT command mode
}

void loop()
{

  // Keep reading from HC-05 and send to Arduino Serial Monitor
  if (BTSerial.available())
    Serial.write(BTSerial.read());

  // Keep reading from Arduino Serial Monitor and send to HC-05
  if (Serial.available())
    BTSerial.write(Serial.read());
}
