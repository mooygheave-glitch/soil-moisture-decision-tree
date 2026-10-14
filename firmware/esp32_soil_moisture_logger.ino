/*
 * Project : Soil Moisture Classification using ESP32 and Decision Tree
 * File    : esp32_soil_moisture_logger.ino
 * Purpose : Read a capacitive soil-moisture sensor and stream CSV-formatted
 *           measurements to the Serial Monitor for Python data logging.
 * Board   : ESP32 DevKit
 *
 * Sensor wiring:
 *   VCC -> 3V3
 *   GND -> GND
 *   AO  -> GPIO35
 *   DO  -> Not used
 *
 * Serial output columns:
 *   elapsed_ms,soil_moisture_adc
 *
 * Notes:
 *   - ADC readings are raw values, not calibrated moisture percentages.
 *   - Each logged value is the average of 20 analogRead() samples.
 *   - One row is sent approximately every 10 seconds.
 */

#include <Arduino.h>

// Sensor configuration
const int SOIL_SENSOR_PIN = 35;

// Sampling configuration
const int SAMPLE_COUNT = 20;
const int SAMPLE_DELAY_MS = 20;
const unsigned long LOG_INTERVAL_MS = 10000UL;

/*
 * Read the sensor repeatedly and return the average ADC value.
 */
int readSoilMoistureADC() {
  long total = 0;

  for (int i = 0; i < SAMPLE_COUNT; i++) {
    total += analogRead(SOIL_SENSOR_PIN);
    delay(SAMPLE_DELAY_MS);
  }

  return total / SAMPLE_COUNT;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Configure ESP32 ADC resolution and input attenuation.
  analogReadResolution(12);
  analogSetPinAttenuation(SOIL_SENSOR_PIN, ADC_11db);

  // Metadata lines are ignored by the Python CSV logger.
  Serial.println("# Capacitive Soil Moisture Logger");
  Serial.println("# ESP32 ADC: 12-bit");
  Serial.println("elapsed_ms,soil_moisture_adc");
}

void loop() {
  static unsigned long previousLogTime = 0;
  const unsigned long currentTime = millis();

  // Log one averaged reading at the configured interval.
  if (currentTime - previousLogTime >= LOG_INTERVAL_MS) {
    previousLogTime = currentTime;

    const int adcValue = readSoilMoistureADC();

    Serial.print(currentTime);
    Serial.print(',');
    Serial.println(adcValue);
  }

  delay(10);
}
