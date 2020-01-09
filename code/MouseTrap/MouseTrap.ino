#include <Bounce2.h>

// Targeted at ATTiny85

#define LED_PIN 1
#define PHOTOTRANSISTOR_PIN 2
#define BUZZER_PIN 3
#define SOLENOID_PIN 4

Bounce debouncer = Bounce(); 

void setup() {
  pinMode(SOLENOID_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(PHOTOTRANSISTOR_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);

  debouncer.attach(PHOTOTRANSISTOR_PIN);
  debouncer.interval(100);
}

void loop() {
  debouncer.update();

  if (debouncer.rose())
  {
    digitalWrite(LED_PIN, HIGH);
    digitalWrite(SOLENOID_PIN, HIGH);
    delay(100);
    digitalWrite(SOLENOID_PIN, LOW);

    while (true)
    {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(50);
      digitalWrite(BUZZER_PIN, LOW);
      delay(30000);
    }
  }
}
