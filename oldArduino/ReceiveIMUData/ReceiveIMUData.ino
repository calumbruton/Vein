
#include "SoftwareSerial.h"

SoftwareSerial serial_connection(5, 6);

int i=0;


void setup()
{
  Serial.begin(9600);
  serial_connection.begin(9600);
  serial_connection.println("Ready!!!");
  Serial.println("Started");
}


void loop()
{
  serial_connection.println("Hello!!" + String(i));
  delay(1000);
  i++;
}
