extern int __heap_start, *__brkval;

int getFree() {
  int v;
  return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
}

bool isReady = false;
const int ramMax = 2048;  
unsigned long tLast = 0;

void setup() {
  Serial.begin(115200);

  while (1) {
    if (Serial.available()) {
      char ch = Serial.read();

      if (!isReady && ch == 'p') {
        int free = getFree();
        int used = ramMax - free;

        Serial.print("Esp32 ");
        Serial.print(32256);  // Flash
        Serial.print(" ");
        Serial.println(used); // RAM used

        isReady = true;
        delay(1000);
        break;
      } else {
        Serial.write(ch); // Echo
        isReady = true;
      }
    }
  }
}

void loop() {
  if (isReady) {
    unsigned long tNow = millis();

    if (tNow - tLast >= 1000) {
      int free = getFree();
      int used = ramMax - free;
      int pct = ((long)used * 100L) / ramMax;

      Serial.print("ram-");
      Serial.println(pct);

      tLast = tNow;
    }

    runMain();
  }
}

void runMain() {
  // Your main program 

  // End
}
