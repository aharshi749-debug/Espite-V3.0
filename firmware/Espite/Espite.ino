
#include <Arduino.h>
#include "espite_engine.h"

static Espite bot;
static float g_temp = 0.5f;
static float g_topp = 0.9f;
static int g_maxNew = 120;
static String line;

static void emitPiece(const char *piece, void *) {
  Serial.print(piece);
}

static void banner() {
  Serial.println(F("====================="));
  Serial.println(F("Espite V3 Gen 1"));
  Serial.println(F("Aharshi Deb (c) 2026"));
  Serial.println(F("====================="));
  Serial.println(F("Write anything to start chatting."));
  Serial.println();
}

static void command(const String &c) {
  if (c == "/reset") {
    espite_reset(&bot);
    Serial.println(F("[conversation cleared]"));
  } else if (c.startsWith("/temp")) {
    g_temp = c.substring(5).toFloat();
    Serial.printf("[temperature = %.2f%s]\n", g_temp, g_temp <= 0 ? " (greedy)" : "");
  } else if (c.startsWith("/len")) {
    int v = c.substring(4).toInt();
    if (v >= 8 && v <= 200) g_maxNew = v;
    Serial.printf("[max reply tokens = %d]\n", g_maxNew);
  } else if (c == "/stats") {
    Serial.printf("[context %d/%d tokens, %d turns | free heap %u | free PSRAM %u]\n",
                  bot.len, ESPITE_CTX, bot.n_turns, ESP.getFreeHeap(), ESP.getFreePsram());
  } else {
    banner();
  }
}

void setup() {
  Serial.begin(115200);
  uint32_t t0 = millis();
  while (!Serial && millis() - t0 < 4000) delay(10);
  delay(300);

  size_t need = espite_cache_bytes();
  void *mem = psramFound() ? ps_malloc(need) : nullptr;
  const char *where = "PSRAM";
  if (!mem) { mem = malloc(need); where = "internal RAM"; }
  if (!mem) {
    Serial.println(F("ESPite: not enough memory for the KV cache. Enable PSRAM (Tools > PSRAM > QSPI PSRAM)."));
    while (true) delay(1000);
  }
  espite_init(&bot, mem, esp_random());
  banner();
  Serial.printf("  KV cache: %u KB in %s\n\n", (unsigned)(need / 1024), where);
  Serial.print(F("you> "));
}

void loop() {
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\r') continue;
    if (c == 8 || c == 127) {
      if (line.length()) { line.remove(line.length() - 1); Serial.print(F("\b \b")); }
      continue;
    }
    if (c != '\n') {
      if (line.length() < 200) { line += c; Serial.print(c); }
      continue;
    }
    Serial.println();
    line.trim();
    if (line.length() == 0) { Serial.print(F("you> ")); continue; }
    if (line[0] == '/') {
      command(line);
    } else {
      Serial.print(F("espite> "));
      uint32_t t = millis();
      int n = espite_chat(&bot, line.c_str(), g_temp, g_topp, g_maxNew, emitPiece, nullptr);
      float secs = (millis() - t) / 1000.0f;
      Serial.printf("\n  [%d tokens, %.1f tok/s]\n", n,
                    secs > 0 ? (n + bot.last_prefill) / secs : 0.0f);
    }
    line = "";
    Serial.print(F("you> "));
  }
}
