// Thingspeak
String myAPIkey = "HANORVIE1VGNB2KE";
#include <ArduinoJson.h>
#include <SoftwareSerial.h>
#include <DHT.h>;
SoftwareSerial ESP8266(2, 3); // Rx,  Tx
/* DHT SENSOR SETUP */
int sensor, moist, lpg, co, sm, volt;
#include<LiquidCrystal_I2C.h>
#include<Wire.h>
LiquidCrystal_I2C lcd(0x27, 16, 2); //LCD 클래스 초기화

StaticJsonBuffer<100> jsonBuffer;
char c;
String phrase;
#include <SPI.h>
#include "LoRa.h"
float humidity, temp_f;
long writingTimer = 17;
long startTime = 0;
long waitTime = 0;
unsigned char check_connection = 0;
unsigned char times_check = 0;
boolean error;
int SyncWord = 0x22;
void setup()
{
  Serial.begin(9600);
  ESP8266.begin(9600);
  Serial.println("LoRa Receiver");
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    lcd.setCursor(0, 1);
    lcd.print("Lora Failed");
    
    while (1);
  }
  LoRa.setSpreadingFactor(12);           // ranges from 6-12,default 7 see API docs
  LoRa.setSignalBandwidth(62.5E3);           // for -139dB (page - 112)
  LoRa.setCodingRate4(8);                   // for -139dB (page - 112)
  LoRa.setSyncWord(SyncWord);           // ranges from 0-0xFF, default 0x12, see API docs

  Serial.print("current spreading factor : ");
  Serial.println(LoRa.getSpreadingFactor());
  Serial.print("current bandwidth : ");
  Serial.println(LoRa.getSignalBandwidth());
  Serial.println("LoRa init succeeded.");
  lcd.init();
  lcd.backlight();
   lcd.setCursor(0, 0);
  lcd.print("Welcome to");
   lcd.setCursor(0, 1);
  lcd.print("Harvestify"); 
  Serial.println("LoRa Reciever");
  startTime = millis();
  ESP8266.println("AT+RST");
  delay(2000);
  Serial.println("Connecting to Wifi");
  while (check_connection == 0)
  {
    Serial.print(".");
    ESP8266.print("AT+CWJAP=\"home WIFI\",\"shivamadappa@123.\"\r\n");
    ESP8266.setTimeout(5000);
    if (ESP8266.find("WIFI CONNECTED\r\n") == 1)
    {
      Serial.println("WIFI CONNECTED");
      break;
    }
    times_check++;
    if (times_check > 3)
    {
      times_check = 0;
      Serial.println("Trying to Reconnect..");
    }
  }
}

void loop()
{
  waitTime = millis() - startTime;
  if (waitTime > (writingTimer * 1000))
  {
    readSensors();

    startTime = millis();
  }
}

void newdata(String phrase)
{
  String a;
  
  jsonBuffer.clear();
  JsonObject& root = jsonBuffer.parseObject(phrase);
  Serial.println("new data");
  Serial.println(phrase);
 // sensor = root["age"];
 //a = root["name"];
  moist = root["moisture"];
  lpg = root["lpg"];
  co = root["co"];
  sm = root["sm"];
  volt = root["volt"];
  Serial.print("Moisture");
  Serial.println(moist);
  Serial.print("LPG");
  Serial.println(lpg);
  Serial.print("co");
  Serial.println(co);
  Serial.print("smoke");
  Serial.println(sm);
  Serial.print("Voltage");
  Serial.println(volt);


     lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print("moist:");
    lcd.print(moist);// 1
  //
    lcd.setCursor(9, 0);
    lcd.print("LPG:");
    lcd.print(lpg);// 2
  //
    lcd.setCursor(0, 1);
    lcd.print("CO:");
    lcd.print(co);// 3
  //
    lcd.setCursor(5, 1);
    lcd.print("SMK:");
    lcd.print(sm);// 4
  //

  lcd.setCursor(11, 1);
  lcd.print("Vol:");
  lcd.print(volt);// 5

  //  volt = root["Voltage"];




  Serial.println(a);
  Serial.println(sensor);
  phrase = "";
  // print RSSI of packet
  Serial.print("' with RSSI ");
  Serial.print(LoRa.packetRssi());
  Serial.println(" Snr: " + String(LoRa.packetSnr()));
  //    digitalWrite(LED_BUILTIN1, HIGH);   // turn the LED on (HIGH is the voltage level)
  //  delay(200);                       // wait for a second
  // digitalWrite(LED_BUILTIN1, LOW);    // turn the LED off by making the voltage LOW
  //delay(200);

  temp_f = sensor;//dht.readTemperature();
  humidity = 45;//dht.readHumidity();

  writeThingSpeak();


}



void  readSensors()
{
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    Serial.print("Received packet '");

    // read packet
    while (LoRa.available()) {
      c = (char)LoRa.read();
      //
      if (c != '\r') {
        phrase = String(phrase + c);
      }
    }
    newdata(phrase);
    phrase = "";
  }
}

void writeThingSpeak(void)
{
  startThingSpeakCmd();
  // preparacao da string GET
  String getStr = "GET /update?api_key=";
  getStr += myAPIkey;
  getStr += "&field1=";
  getStr += String(moist);
  getStr += "&field2=";
  getStr += String(co);
  getStr += "&field3=";
  getStr += String(sm);
  getStr += "&field4=";
  getStr += String(volt);
  getStr += "&field5=";
  getStr += String(lpg);
  
  getStr += "\r\n\r\n";
  GetThingspeakcmd(getStr);
}

void startThingSpeakCmd(void)
{
  ESP8266.flush();
  String cmd = "AT+CIPSTART=\"TCP\",\"";
  cmd += "184.106.153.149"; // api.thingspeak.com IP address
  cmd += "\",80";
  ESP8266.println(cmd);
  Serial.print("Start Commands: ");
  Serial.println(cmd);

  if (ESP8266.find("Error"))
  {
    Serial.println("AT+CIPSTART error");
    return;
  }
}

String GetThingspeakcmd(String getStr)
{
  String cmd = "AT+CIPSEND=";
  cmd += String(getStr.length());
  ESP8266.println(cmd);
  Serial.println(cmd);

  if (ESP8266.find(">"))
  {
    ESP8266.print(getStr);
    Serial.println(getStr);
    delay(500);
    String messageBody = "";
    while (ESP8266.available())
    {
      String line = ESP8266.readStringUntil('\n');
      if (line.length() == 1)
      {
        messageBody = ESP8266.readStringUntil('\n');
      }
    }
    Serial.print("MessageBody received: ");
    Serial.println(messageBody);
    return messageBody;
  }
  else
  {
    ESP8266.println("AT+CIPCLOSE");
    Serial.println("AT+CIPCLOSE");
  }
}
