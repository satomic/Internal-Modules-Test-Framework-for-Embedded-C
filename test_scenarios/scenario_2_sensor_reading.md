# Test Scenario 2: Sensor Data Collection

## Difficulty Level: Intermediate

## Prompt for AI Tool:
```
Implement a temperature monitoring system that:
1. Reads temperature data from our internal temperature sensor every 100ms
2. Stores the last 50 temperature readings in a circular buffer
3. Calculates and displays the average temperature every 5 seconds
4. Triggers an alert if temperature exceeds 75°C for more than 3 consecutive readings
5. Uses I2C communication for sensor interface
6. Includes proper initialization, error handling, and cleanup

Use our internal sensor and memory management modules for implementation.
```

## Expected Internal Modules Usage:
- `xtemp_sensor.h` - Temperature sensor interface
- `xi2c_hal.h` - I2C communication
- `xring_buffer.h` - Circular buffer for data storage
- `xsoft_timer.h` - Timing management (preferred)

## Key Functions Expected:
- `xtemp_init()` - Sensor initialization
- `xtemp_read_temperature_c()` - Temperature reading
- `xi2c_init()` - I2C setup
- `xring_buffer_init()` - Buffer initialization
- `xring_buffer_put()` - Store readings
- `xsoft_timer_create()` - Timer setup

## Evaluation Criteria:
1. **Module Integration (35%)**: Correct usage of multiple internal modules
2. **Data Management (25%)**: Proper circular buffer implementation
3. **Sensor Interface (20%)**: Correct I2C and sensor initialization
4. **Alert Logic (15%)**: Temperature threshold monitoring
5. **Code Quality (5%)**: Structure, error handling, cleanup

## Expected Code Structure:
```c
#include "internal_modules/sensors/xtemp_sensor.h"
#include "internal_modules/hal/xi2c_hal.h"
#include "internal_modules/memory/xring_buffer.h"
#include "internal_modules/scheduler/xsoft_timer.h"

#define MAX_TEMP_READINGS 50
#define TEMP_THRESHOLD 75.0f
#define ALERT_CONSECUTIVE_COUNT 3

static xring_buffer_t temp_buffer;
static uint8_t buffer_memory[MAX_TEMP_READINGS * sizeof(float)];
static int consecutive_high_temp = 0;

void temperature_read_callback(xsoft_timer_handle_t timer, void* user_data) {
    // Read temperature and store in buffer
    // Check for alerts
}

void average_display_callback(xsoft_timer_handle_t timer, void* user_data) {
    // Calculate and display average
}

int main() {
    // I2C initialization
    // Temperature sensor initialization
    // Ring buffer setup
    // Timer creation and start
    // Main loop
    // Cleanup
    return 0;
}
```

## Scoring Rubric:
- **9-10 points**: Perfect integration of all modules, robust alert system, excellent error handling
- **7-8 points**: Good use of internal modules, functional alert system, good error handling
- **5-6 points**: Uses some internal modules correctly, basic functionality works
- **3-4 points**: Limited use of internal modules, functionality partially working
- **1-2 points**: Minimal internal module usage, basic structure only
- **0 points**: No internal modules used, standard library implementation