# Soil Moisture Classification using ESP32 and Decision Tree

## 1. Project overview
This project demonstrates a Machine Learning pipeline to classify soil measurements as `kering` (dry) or `basah` (wet) using data from a capacitive soil-moisture sensor connected to an ESP32.

## 2. Hardware and data acquisition
- ESP32 DevKit
- Capacitive soil-moisture sensor
- Sensor VCC: 3.3 V; GND: GND; AO: GPIO35
- Arduino IDE for sensor logging
- Python serial logger for CSV capture

## 3. Features and target
The baseline model uses two input features:
- `soil_moisture_adc`: raw analog reading from the sensor
- `jam_pengukuran`: hour of day extracted from `recorded_at` (0–23)

Target:
- `label`: `kering` or `basah`

`recorded_at` is parsed as a datetime. `jam_pengukuran` is extracted with pandas `.dt.hour`. The timestamp itself is retained for traceability and is not directly passed to the model. `elapsed_ms` is also retained for traceability but is not a predictor in this A-option design.

## 4. Dataset
Four latest CSV sessions are stored in `data/raw/`:
- `uji_kering_1.csv`: 55 rows
- `uji_kering_2.csv`: 70 rows
- `uji_basah_1.csv`: 25 rows
- `uji_basah_2.csv`: 27 rows

Total: **177 rows** (125 dry, 52 wet). The processed dataset in `data/processed/soil_moisture_dataset.csv` adds `session` and `jam_pengukuran` columns while preserving the original measurements.

## 5. Important limitation: time and label are confounded
The dry sessions were recorded on 13 October 2026 around 20:22–21:49, while the wet sessions were recorded on 14 October 2026 around 12:56–13:05. Therefore, `jam_pengukuran` is strongly associated with the label in the current dataset. The Decision Tree may learn the collection schedule rather than a general relationship between time and soil moisture.

This is a limitation of the experiment, not something to hide. The model can be used to demonstrate a two-feature ML pipeline for coursework, but a high accuracy score must **not** be interpreted as proof that the model generalizes to other measurement times.

For a stronger future experiment, collect dry and wet measurements at overlapping hours and evaluate on independent sessions.

## 6. Baseline model
- Algorithm: `DecisionTreeClassifier`
- Features: `soil_moisture_adc`, `jam_pengukuran`
- Target: `label`
- `max_depth=3`
- `class_weight="balanced"`
- Stratified random split: 75% train / 25% test, `random_state=42`

See `results/metrics.txt`, `results/confusion_matrix.png`, `results/decision_tree.png`, and `results/hour_label_distribution.png` for the reproducible baseline output. Run the notebook to reproduce the metrics in your own environment.

## 7. Run the notebook
Open `notebooks/decision_tree_baseline.ipynb` in Jupyter or Google Colab and run all cells from top to bottom. The notebook expects the project folder structure as provided. In Colab, upload and extract the ZIP, then set `DATA_DIR` to the extracted `data/raw` folder.

Install local dependencies using:
`pip install -r requirements.txt`

## 8. Limitations and next steps
- Raw ADC is not a calibrated moisture percentage.
- There are only four measurement sessions and class counts are imbalanced.
- Soil type, water distribution, insertion depth, and sensor conditions can affect ADC.
- Time of day is confounded with the labels in this dataset.
- Do not claim general deployment performance based on this baseline alone.

## 9. Firmware — ESP32
The Arduino firmware is located in firmware/esp32_soil_moisture_logger.ino.

- The firmware reads the capacitive soil-moisture sensor through GPIO34, averages 20 ADC readings per sample, and sends the elapsed time and ADC value through Serial at 115200 baud. Data are logged approximately every 10 seconds.

- The Serial output is processed by the Python data-collection script. The resulting CSV files contain the measurement timestamp, elapsed time, ADC reading, and soil-condition label.

- The ADC values represent raw sensor readings and are not calibrated moisture percentages.
