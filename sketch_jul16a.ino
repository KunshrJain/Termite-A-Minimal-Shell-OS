extern int __heap_start, *__brkval;

int freeMemory() {
  int v;
  return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
}

bool ready = false;
const int totalRam = 2048;  
unsigned long lastRamPrintTime = 0;

void setup() {
  Serial.begin(115200);

  while (1) {
    if (Serial.available()) {
      char data = Serial.read();

      if (!ready && data == 'p') {
        int freeRam = freeMemory();
        int usedRam = totalRam - freeRam;

        Serial.print("Arduino ");
        Serial.print(32256);  
        Serial.print(" ");
        Serial.println(usedRam);

        ready = true;
        delay(1000);
        break;
      } else {
        Serial.write(data);
        ready = true;
      }
    }
  }
}

void loop() {
  if (ready) {
    unsigned long now = millis();

    if (now - lastRamPrintTime >= 1000) {
      int freeRam = freeMemory();
      int usedRam = totalRam - freeRam;
      int usedPercent = ((long)usedRam * 100L) / totalRam;

      Serial.print("ram-");
      Serial.println(usedPercent);

      lastRamPrintTime = now;
    }

    runMyProgram();
  }
}

void runMyProgram() {
  
}
