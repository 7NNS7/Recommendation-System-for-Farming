
/* Comment this out to disable prints and save space */
#define BLYNK_PRINT Serial

#include <HttpClient.h>
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <DHT.h>


const int ledPin =  D0;// the number of the LED pin

// Variables will change:
int ledState = LOW;             // ledState used to set the LED

// Generally, you should use "unsigned long" for variables that hold time
// The value will quickly become too large for an int to store
unsigned long previousMillis = 0;        // will store last time LED was updated

// constants won't change:
const long interval = 7500;           // interval at which to blink (milliseconds)



// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "TtGVPcqUUMtN8vr1xqU680Fv0TXxHEUm";

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "home WIFI";
char pass[] = "shivamadappa@123.";
int j = 0;
#define DHTPIN 2          // What digital pin we're connected to

// Uncomment whatever type you're using!
#define DHTTYPE DHT11     // DHT 11
//#define DHTTYPE DHT22   // DHT 22, AM2302, AM2321
//#define DHTTYPE DHT21   // DHT 21, AM2301

DHT dht(DHTPIN, DHTTYPE);
BlynkTimer timer;

// This function sends Arduino's up time every second to Virtual Pin (5).
// In the app, Widget's reading frequency should be set to PUSH. This means
// that you define how often to send data to Blynk App.
void sendSensor()
{
  float h = dht.readHumidity();
  float t = dht.readTemperature(); // or dht.readTemperature(true) for Fahrenheit

  //  if (isnan(h) || isnan(t)) {
  //    Serial.println("Failed to read from DHT sensor!");
  //    return;
  //  }
  // You can send any value at any time.
  // Please don't send more that 10 values per second.
  j++;
  Blynk.virtualWrite(V5, j);

}

void setup()
{ pinMode(D1, OUTPUT);
  digitalWrite(D1, HIGH);
  // Debug console
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  Blynk.begin(auth, ssid, pass);
  // You can also specify server:
  //Blynk.begin(auth, ssid, pass, "blynk-cloud.com", 80);
  //Blynk.begin(auth, ssid, pass, IPAddress(192,168,1,100), 8080);

  dht.begin();

  // Setup a function to be called every second
  timer.setInterval(1000L, sendSensor);
}
int value;
BLYNK_WRITE(V1)
{
  value = param.asInt(); // Get value as integer


}


void loop()
{
  unsigned long currentMillis = millis();


  //  client.get("");

  if (currentMillis - previousMillis >= interval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;

    // if the LED is off turn it on and vice-versa:
    if (ledState == LOW) {
      ledState = HIGH;
      // client.print("http://blynk-cloud.com/TtGVPcqUUMtN8vr1xqU680Fv0TXxHEUm/update/V1?value=0");
    } else {
      ledState = LOW;
      // client.print("http://blynk-cloud.com/TtGVPcqUUMtN8vr1xqU680Fv0TXxHEUm/update/V1?value=1");
    }

    // set the LED with the ledState of the variable:
    digitalWrite(ledPin, ledState);
  }


  if (value == 1)
  {
    digitalWrite(D1, LOW);

  }
  else {
    digitalWrite(D1, HIGH);

  }
  Blynk.run();
  timer.run();
}
