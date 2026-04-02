---
name: add-esp32-sensor
description: Create a new ESP32 sensor node firmware project. Use when adding a new IoT sensor type, configuring a new ESP32 device, or extending the sensor network.
---

# Add New ESP32 Sensor Node

## Workflow

### Step 1: Create the project

Copy the template:

```bash
cp -r iot/sensor-node/ iot/<new-sensor-name>/
```

### Step 2: Configure PlatformIO

Edit `iot/<new-sensor-name>/platformio.ini`:

```ini
[env:esp32]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps =
  knolleary/PubSubClient@^2.8
  ; add sensor-specific libraries here
monitor_speed = 115200
```

### Step 3: Edit config

Edit `iot/<new-sensor-name>/include/config.h`:

```cpp
#define WIFI_SSID "happy-lab"
#define WIFI_PASS "your-password"
#define MQTT_SERVER "10.13.37.1"
#define MQTT_PORT 1883
#define NODE_ID "sensor-N"
#define MQTT_TOPIC "happy/sensor/N/<measurement>"
#define READING_INTERVAL_MS 5000
```

### Step 4: Implement main.cpp

Edit `iot/<new-sensor-name>/src/main.cpp`:

- Reuse shared libs from `iot/common/lib/`:
  - `mqtt_client` — MQTT connection and publish
  - `wifi_manager` — WiFi connect with retry
  - `sensor_base` — Base class for sensor readings

### Step 5: Assign network identity

Pick next available IP from `10.13.37.50-59` range and update:
- `core/` DHCP config (static lease)
- `docs/` network documentation

### Step 6: Verify

- [ ] Compiles: `cd iot/<name> && pio run`
- [ ] Connects to WiFi
- [ ] Publishes to MQTT topic
- [ ] Visible in Grafana dashboard
