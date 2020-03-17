#define         MQ_PIN                       (1)     //define which analog input channel you are going to use
#define         RL_VALUE                     (5)     //define the load resistance on the board, in kilo ohms
#define         RO_CLEAN_AIR_FACTOR          (9.83)  //RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
//which is derived from the chart in datasheet
#define         CALIBARAION_SAMPLE_TIMES     (50)    //define how many samples you are going to take in the calibration phase
#define         CALIBRATION_SAMPLE_INTERVAL  (500)   //define the time interal(in milisecond) between each samples in the
//cablibration phase
#define         READ_SAMPLE_INTERVAL         (50)    //define how many samples you are going to take in normal operation
#define         READ_SAMPLE_TIMES            (5)     //define the time interal(in milisecond) between each samples in 


#define         GAS_LPG                      (0)
#define         GAS_CO                       (1)
#define         GAS_SMOKE                    (2)
float           LPGCurve[3]  =  {2.3, 0.21, -0.47}; //two points are taken from the curve.
float           COCurve[3]  =  {2.3, 0.72, -0.34};  //two points are taken from the curve.
float           SmokeCurve[3] = {2.3, 0.53, -0.44}; //two points are taken from the curve.
float           Ro           =  10;                 //Ro is initialized to 10 kilo ohms
int sensor_pin = A0;
int output_value ;
int lpg;
int smoke;

#include <ArduinoJson.h>
int co;
int counter = 0;
int LED_BUILTIN1 = 3;
int ID = 2;  // 0x11 for 1 and 0x22 for 2
int SyncWord = 0x22;


#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include "LoRa.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <stdlib.h>
#include<ACS712.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);


float MQResistanceCalculation(int raw_adc)
{
  return ( ((float)RL_VALUE * (1023 - raw_adc) / raw_adc));
}

float MQCalibration(int mq_pin)
{
  int i;
  float val = 0;

  for (i = 0; i < CALIBARAION_SAMPLE_TIMES; i++) {      //take multiple samples
    val += MQResistanceCalculation(analogRead(mq_pin));
    delay(CALIBRATION_SAMPLE_INTERVAL);
  }
  val = val / CALIBARAION_SAMPLE_TIMES;                 //calculate the average value

  val = val / RO_CLEAN_AIR_FACTOR;                      //divided by RO_CLEAN_AIR_FACTOR yields the Ro
  //according to the chart in the datasheet
  return val;
}

float MQRead(int mq_pin)
{
  int i;
  float rs = 0;

  for (i = 0; i < READ_SAMPLE_TIMES; i++) {
    rs += MQResistanceCalculation(analogRead(mq_pin));
    delay(READ_SAMPLE_INTERVAL);
  }
  rs = rs / READ_SAMPLE_TIMES;
  return rs;
}


int MQGetGasPercentage(float rs_ro_ratio, int gas_id)
{
  if ( gas_id == GAS_LPG ) {
    return MQGetPercentage(rs_ro_ratio, LPGCurve);
  } else if ( gas_id == GAS_CO ) {
    return MQGetPercentage(rs_ro_ratio, COCurve);
  } else if ( gas_id == GAS_SMOKE ) {
    return MQGetPercentage(rs_ro_ratio, SmokeCurve);
  }

  return 0;
}


int  MQGetPercentage(float rs_ro_ratio, float *pcurve)
{
  return (pow(10, ( ((log(rs_ro_ratio) - pcurve[1]) / pcurve[2]) + pcurve[0])));
}
#define DHTPIN 2
#define DHTTYPE DHT11
//DHT dht(DHTPIN, DHTTYPE);
ACS712 sensor(ACS712_20A, A2);  // curent sensor
unsigned long last_time = 0;
unsigned long current_time = 0;
const int voltageSensor = A3;   // voltage sensor
float vOUT = 0.0;
int vIN = 0.0;
float R1 = 30000.0;
float R2 = 7500.0;
int value = 0;
int moisture;


void setup()
{
  // Debug console
  // Serial.begin(9600);

  // Blynk will work through Serial
  // Do not read or write this serial manually in your sketch
  Serial.begin(9600);
  Serial.print("im testing");
  Serial.print("Calibrating...\n");
  Ro = MQCalibration(MQ_PIN);                       //Calibrating the sensor. Please make sure the sensor is in clean air
  //when you perform the calibration
  Serial.print("Calibration is done...\n");
  Serial.print("Ro=");
  Serial.print(Ro);
  Serial.print("kohm");
  Serial.print("\n");
  sensor.calibrate();
  lcd.init();
  lcd.backlight();
  Serial.println("LoRa Sender");


  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setSpreadingFactor(12);           // ranges from 6-12,default 7 see API docs
  LoRa.setSignalBandwidth(62.5E3 );           // for -139dB (page - 112)
  LoRa.setCodingRate4(8);                   // for -139dB (page - 112)
  LoRa.setSyncWord(SyncWord);

  Serial.print("current spreading factor : ");
  Serial.println(LoRa.getSpreadingFactor());
  Serial.print("current bandwidth : ");
  Serial.println(LoRa.getSignalBandwidth());
  Serial.println("LoRa init succeeded.");

  lcd.clear();
  lcd.setCursor(0, 0);

  int s = LoRa.getSpreadingFactor();
  lcd.print("currentspreadingfactor:");
  lcd.setCursor(0, 1);
  lcd.print("factor:");
  lcd.print(s);
  int b = LoRa.getSignalBandwidth();
  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("currentbandwidth");
  lcd.setCursor(0, 1);
  lcd.print(b);
  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("LoRa succeeded.");

  //dht.begin();
  //Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);


  // Setup a function to be called every second


  DynamicJsonBuffer jsonBuffer;

  String input =
    "{\"sensor\":\"gps\",\"time\":1351824120,\"data\":[48.756080,2.302038]}";

  JsonObject& root = jsonBuffer.parseObject(input);
  //  JsonObject.stringify(root);
}



void loop()
{
  Serial.println("im testing");
  // float h = dht.readHumidity();
  //float t = dht.readTemperature(); // or dht.readTemperature(true) for Fahrenheit

  //if (isnan(h) || isnan(t)) {
  // Serial.println("Failed to read from DHT sensor!");
  // return;
  // }

  output_value = analogRead(sensor_pin);
  output_value = map(output_value, 784, 423, 0, 100);
  Serial.print("Mositure : ");
  Serial.print(output_value);
  Serial.println("%");
  lpg = MQGetGasPercentage(MQRead(MQ_PIN) / Ro, GAS_LPG);
  co  = MQGetGasPercentage(MQRead(MQ_PIN) / Ro, GAS_CO);
  smoke = MQGetGasPercentage(MQRead(MQ_PIN) / Ro, GAS_SMOKE);

  value = analogRead(voltageSensor);
  vOUT = (value * 5.0) / 1024.0;
  vIN = vOUT / (R2 / (R1 + R2)); //print vin


  //  float I = sensor.getCurrentAC();
  //  float P = vIN * I;

  //last_time = current_time;
  //  current_time = millis();
  //float  U = U +  P * (( current_time - last_time) / 3600000.0) ;

  //Serial.print(moisture);
  String mois;
  String lp;
  String c;
  String sm;
  String v;

  Serial.print("lpg:");
  Serial.println(lpg + "0");
  Serial.print("co:");
  Serial.println(co + "0");
  Serial.print("vOLTAGE:");
  Serial.println(vIN);
  mois = output_value;
  lp = lpg;
  c = co;
  sm = smoke;
  v = vIN;


  DynamicJsonBuffer jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject("{\"sensor\":\"gps\",\"time\":1351824120,"
                     "\"data\":[48.756080,2.302038]}");
//  String s = "shiva";
//  String l = ("{\"sensor\":\"" + mois + "", "\"time\":\"shiva\"," "\"data\":[48]}");
//  String o = "{\"firstname\":\"jsoh""}";
//     String m = "{name: ""\"John\"," "age: \""+mois+"\", city: ""\"New York\"""}";
    String  t = "{\"moisture\": \""+mois+"\"," "\"co\": \""+mois+"\"," "\"sm\": \""+mois+"\"," "\"lpg\": \""+mois+"\"," "\"volt\": \""+mois+"\"}";
     LoRa.idle();
  Serial.print("Sending packet: ");
  Serial.println(counter);
  //LoRa.print();
  LoRa.beginPacket();
  // LoRa.print("LPG:");
  LoRa.print(t);

  //  LoRa.print("CO:");
  //  LoRa.print(c);
  //  LoRa.print("sm:");
  //  LoRa.print(sm);
  //  LoRa.print("vol:");
  //  LoRa.print(v);
  //  LoRa.print("mois:");
  //  LoRa.print(mois);
  LoRa.print('\r');
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("packet sent");
  LoRa.endPacket();
  LoRa.sleep();

  lcd.setCursor(0, 0);
  lcd.clear();
  lcd.print("moist:");
  lcd.print(output_value);// 1
Serial.println(t);
  lcd.setCursor(9, 0);
  lcd.print("LPG:");
  lcd.print(lp);// 2

  lcd.setCursor(0, 1);
  lcd.print("CO:");
  lcd.print(c);// 3

  lcd.setCursor(5, 1);
  lcd.print("SMK:");
  lcd.print(sm);// 4


  lcd.setCursor(11, 1);
  lcd.print("Vol:");
  lcd.print(v);// 5




  delay(1000);

}
