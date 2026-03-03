/*
  SealinkOEM_Basic.ino
  Minimal Arduino example for Sealink-OEM UART protocol.

  Hardware assumptions:
  - Board has Serial (USB debug) and Serial1 (hardware UART to modem)
  - Modem UART: 9600 8N1, 3.3V logic

  Wiring (example):
  - Arduino Serial1 TX -> Sealink RX
  - Arduino Serial1 RX -> Sealink TX
  - GND shared
*/

static const unsigned long RESPONSE_TIMEOUT_MS = 8000;

String buildSentence(const String &bodyWithoutDollar) {
  uint8_t checksum = 0;
  for (size_t i = 0; i < bodyWithoutDollar.length(); ++i) {
    checksum ^= (uint8_t)bodyWithoutDollar[i];
  }

  char hex[3];
  snprintf(hex, sizeof(hex), "%02X", checksum);

  String sentence = "$";
  sentence += bodyWithoutDollar;
  sentence += "*";
  sentence += hex;
  sentence += "\r\n";
  return sentence;
}

void sendSealink(const String &bodyWithoutDollar) {
  String full = buildSentence(bodyWithoutDollar);
  Serial1.print(full);
  Serial.print("TX -> ");
  Serial.print(full);
}

bool readLineFromSealink(String &line, unsigned long timeoutMs) {
  unsigned long start = millis();
  line = "";
  while (millis() - start < timeoutMs) {
    while (Serial1.available() > 0) {
      char c = (char)Serial1.read();
      if (c == '\n') {
        line.trim();
        return line.length() > 0;
      }
      line += c;
    }
  }
  return false;
}

void printRangeIfPUWV3(const String &line) {
  if (!line.startsWith("$PUWV3,")) {
    return;
  }

  int comma1 = line.indexOf(',');
  int comma2 = line.indexOf(',', comma1 + 1);
  int comma3 = line.indexOf(',', comma2 + 1);
  int comma4 = line.indexOf(',', comma3 + 1);

  if (comma3 < 0 || comma4 < 0) {
    Serial.println("RX parse: invalid PUWV3 format");
    return;
  }

  String tpStr = line.substring(comma3 + 1, comma4);
  float propagationSec = tpStr.toFloat();
  float distanceM = propagationSec * 1500.0f;

  Serial.print("RX propagation: ");
  Serial.print(propagationSec, 4);
  Serial.print(" s, approx range: ");
  Serial.print(distanceM, 1);
  Serial.println(" m");
}

void doPing(uint8_t txCh, uint8_t rxCh) {
  String body = "PUWV2," + String(txCh) + "," + String(rxCh) + ",0";
  sendSealink(body);

  String response;
  if (readLineFromSealink(response, RESPONSE_TIMEOUT_MS)) {
    Serial.print("RX <- ");
    Serial.println(response);
    printRangeIfPUWV3(response);
  } else {
    Serial.println("RX timeout waiting for ping response");
  }
}

void doDeviceInfo() {
  sendSealink("PUWV?,0");

  String response;
  if (readLineFromSealink(response, RESPONSE_TIMEOUT_MS)) {
    Serial.print("RX <- ");
    Serial.println(response);
  } else {
    Serial.println("RX timeout waiting for device info");
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial) {}

  Serial1.begin(9600);

  Serial.println("Sealink OEM Arduino example ready.");
  Serial.println("Commands over USB Serial monitor:");
  Serial.println("  i            -> device info");
  Serial.println("  p            -> ping tx=0 rx=0");
  Serial.println("  p <tx> <rx>  -> ping with channels");
}

void loop() {
  if (!Serial.available()) {
    return;
  }

  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  if (cmd.length() == 0) {
    return;
  }

  if (cmd == "i") {
    doDeviceInfo();
    return;
  }

  if (cmd == "p") {
    doPing(0, 0);
    return;
  }

  if (cmd.startsWith("p ")) {
    int firstSpace = cmd.indexOf(' ');
    int secondSpace = cmd.indexOf(' ', firstSpace + 1);
    if (secondSpace > firstSpace) {
      uint8_t tx = (uint8_t)cmd.substring(firstSpace + 1, secondSpace).toInt();
      uint8_t rx = (uint8_t)cmd.substring(secondSpace + 1).toInt();
      doPing(tx, rx);
      return;
    }
  }

  Serial.println("Unknown command. Use: i | p | p <tx> <rx>");
}
