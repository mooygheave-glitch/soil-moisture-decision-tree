"""ESP32 serial CSV logger. Close Arduino Serial Monitor before running."""
import csv, os, time
from datetime import datetime
import serial

SERIAL_PORT = "COM3"  # Change to the ESP32 COM port shown in Device Manager
BAUD_RATE = 115200
session = input("Session filename without .csv (e.g. uji_kering_3): ").strip()
if not session:
    raise SystemExit("Session filename cannot be empty.")
output_file = session + ".csv"
choice = input("Label: 1=kering, 2=basah: ").strip()
label = {"1": "kering", "2": "basah"}.get(choice)
if label is None:
    raise SystemExit("Invalid label.")
needs_header = not os.path.exists(output_file) or os.path.getsize(output_file) == 0
try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
        time.sleep(2)
        ser.reset_input_buffer()
        with open(output_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if needs_header:
                writer.writerow(["recorded_at", "elapsed_ms", "soil_moisture_adc", "label"])
            print(f"Recording {label} to {os.path.abspath(output_file)}. Ctrl+C to stop.")
            try:
                while True:
                    line = ser.readline().decode("utf-8", errors="replace").strip()
                    if not line or line.startswith("#") or line.startswith("elapsed_ms"):
                        continue
                    parts = line.split(",")
                    if len(parts) != 2:
                        continue
                    try:
                        elapsed_ms, adc = map(int, parts)
                    except ValueError:
                        continue
                    stamp = datetime.now().isoformat(timespec="seconds")
                    writer.writerow([stamp, elapsed_ms, adc, label])
                    f.flush()
                    print(stamp, "ADC=", adc, "label=", label)
            except KeyboardInterrupt:
                print("\nRecording stopped.")
except serial.SerialException as exc:
    print("Serial port error:", exc)
