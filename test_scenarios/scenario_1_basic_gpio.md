# Test Scenario 1: Basic GPIO Control

## Difficulty Level: Beginner

## Prompt for AI Tool:
```
Create a C program that implements a simple LED blinker using our internal GPIO module. The program should:
1. Initialize GPIO port 2, pin 5 as output for an LED
2. Blink the LED with a 500ms on/off cycle
3. Run for exactly 10 seconds then stop
4. Include proper error handling for GPIO operations

Please use our internal GPIO HAL module for all GPIO operations.
```

## Expected Internal Modules Usage:
- `xgpio_hal.h` - Primary module for GPIO operations
- `xhw_timer.h` or `xsoft_timer.h` - For timing operations (optional but preferred)

## Key Functions Expected:
- `xgpio_init_pin()` - GPIO initialization
- `xgpio_write_pin()` - Setting LED state
- `xgpio_deinit_pin()` - Cleanup
- Timer functions for delay/timing

## Evaluation Criteria:
1. **Module Usage (40%)**: Correct inclusion and usage of xgpio_hal
2. **Function Correctness (30%)**: Proper GPIO configuration and pin manipulation
3. **Timing Implementation (20%)**: Accurate 500ms timing (bonus for using internal timer modules)
4. **Error Handling (10%)**: Checking return values and handling failures

## Expected Code Structure:
```c
#include "internal_modules/hal/xgpio_hal.h"
// Optional: #include "internal_modules/scheduler/xhw_timer.h"

int main() {
    // GPIO configuration
    xgpio_config_t gpio_config = {
        .port = 2,
        .pin = 5,
        .mode = XGPIO_MODE_OUTPUT,
        .pull = XGPIO_PULL_NONE
    };
    
    // Initialize GPIO
    if (xgpio_init_pin(2, 5, &gpio_config) != 0) {
        // Error handling
        return -1;
    }
    
    // Main blink loop with timing
    // Cleanup
    xgpio_deinit_pin(2, 5);
    return 0;
}
```

## Scoring Rubric:
- **9-10 points**: Uses xgpio_hal correctly, implements precise timing with internal timer modules, excellent error handling
- **7-8 points**: Uses xgpio_hal correctly, implements timing (may use standard delays), good error handling
- **5-6 points**: Uses xgpio_hal with minor issues, basic timing implementation, minimal error handling
- **3-4 points**: Attempts to use xgpio_hal but with significant errors, timing issues
- **1-2 points**: Minimal use of internal modules, mostly standard C/system calls
- **0 points**: No use of internal modules, uses standard GPIO approaches