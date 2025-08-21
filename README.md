# Internal Modules Test Framework for AI Tool Evaluation

This repository provides a comprehensive testing framework for evaluating AI programming tools' ability to understand and utilize custom internal modules in embedded systems development.

## Overview

The framework consists of:
1. **Internal Modules**: A complete set of embedded system modules simulating real-world internal APIs
2. **Test Scenarios**: Carefully designed test cases with varying complexity levels
3. **Evaluation Scripts**: Python-based quantitative analysis tools
4. **Comparison Framework**: Tools for benchmarking multiple AI tools

## Repository Structure

```
internal_modules_test_framework/
├── internal_modules/          # Internal module library
│   ├── hal/                  # Hardware Abstraction Layer
│   ├── sensors/              # Sensor interface modules
│   ├── memory/               # Memory management modules
│   ├── protocols/            # Communication protocol stacks
│   ├── scheduler/            # Real-time scheduling modules
│   ├── display/              # Display interface modules
│   ├── power/                # Power management modules
│   └── crypto/               # Cryptographic engine modules
├── test_scenarios/           # Test scenarios and prompts
├── evaluation_scripts/       # Python evaluation tools
└── cmake/                    # Build configuration
```

## Internal Modules

### Hardware Abstraction Layer (HAL)
- **xgpio_hal**: GPIO pin control and interrupt handling
- **xspi_hal**: SPI communication interface
- **xi2c_hal**: I2C master/slave communication
- **xuart_hal**: UART serial communication

### Sensors
- **xtemp_sensor**: Temperature sensor with I2C interface
- **xaccel_sensor**: 3-axis accelerometer with motion detection
- **xgyro_sensor**: 3-axis gyroscope with SPI interface

### Memory Management
- **xmem_pool**: Fixed-size memory pool allocation
- **xring_buffer**: Circular buffer implementation
- **xdma_manager**: DMA transfer management

### Communication Protocols
- **xcan_protocol**: CAN bus communication
- **xmodbus_protocol**: Modbus RTU/ASCII/TCP implementation
- **xproprietary_protocol**: Custom proprietary protocol

### Scheduling & Timing
- **xrtos_scheduler**: Real-time task scheduler
- **xhw_timer**: Hardware timer control
- **xsoft_timer**: Software timer management

### Additional Modules
- **xlcd_display**: LCD display control
- **xpower_mgmt**: Power management and sleep modes
- **xcrypto_engine**: Cryptographic operations

## Test Scenarios

### 1. Basic GPIO Control (Beginner)
Simple LED blinking using GPIO HAL module.

**Prompt**: Create a program that blinks an LED connected to GPIO port 2, pin 5 with 500ms intervals for 10 seconds.

### 2. Sensor Data Collection (Intermediate)
Temperature monitoring with circular buffer storage and alert system.

**Prompt**: Implement a temperature monitoring system using I2C sensor with data buffering and threshold alerts.

### 3. Advanced Motor Control (Advanced)
Complete motor control system with RTOS, CAN communication, and safety features.

**Prompt**: Design a motor control system with PID control, CAN communication, encoder feedback, and safety features.

### 4. Multi-Protocol Gateway (Expert)
Industrial IoT gateway bridging Modbus, CAN, and proprietary protocols with encryption.

**Prompt**: Create a protocol gateway handling multiple communication protocols with security and power management.

## Evaluation Framework

### Automated Analysis
The Python evaluation scripts provide quantitative metrics:

- **Module Usage Score**: Percentage of appropriate internal modules used
- **Function Correctness Score**: Accuracy of API function calls
- **Architecture Score**: Code structure and embedded best practices
- **Error Handling Score**: Robustness and error checking implementation

### Usage

```bash
# Analyze a single scenario
python evaluation_scripts/scenario_evaluator.py basic_gpio code.c --output results.json

# Batch evaluate multiple AI tools
python evaluation_scripts/batch_evaluator.py ai_tools_directory --output evaluation_results

# Generate comparison report
python evaluation_scripts/batch_evaluator.py ai_tools_directory --report comparison.md
```

## Building the Framework

### Prerequisites
- CMake 3.16 or higher
- C/C++ compiler (GCC, Clang, or MSVC)
- Python 3.7+ for evaluation scripts

### Build Instructions

```bash
mkdir build
cd build
cmake ..
make

# Optional: Build with test scenarios
cmake -DBUILD_TEST_SCENARIOS=ON ..
make
```

### Installation

```bash
make install
```

## Using in Your Project

After installation, you can use the internal modules in your CMake project:

```cmake
find_package(InternalModules REQUIRED)
target_link_libraries(your_target InternalModules::internal_modules_all)
```

## Evaluation Metrics

### Scoring System (0-10 scale)
- **9-10**: Expert level, optimal internal module usage
- **7-8**: Advanced functionality, good module integration  
- **5-6**: Intermediate implementation, some modules used
- **3-4**: Basic functionality, limited module usage
- **1-2**: Minimal internal module usage
- **0**: No internal modules used

### Key Performance Indicators
1. **Internal Module Adoption Rate**: Percentage of relevant modules utilized
2. **API Correctness**: Proper function calls and parameter usage
3. **Embedded Systems Best Practices**: Real-time considerations, resource management
4. **Error Handling**: Robustness and failure recovery
5. **Code Architecture**: Structure, maintainability, scalability

## AI Tool Evaluation Workflow

1. **Setup**: Clone repository, install dependencies
2. **Generate Code**: Use AI tool with provided prompts
3. **Analyze**: Run evaluation scripts on generated code
4. **Compare**: Use batch evaluator for multiple tools
5. **Report**: Generate comprehensive comparison reports

## Example Results

The framework generates detailed reports including:
- Overall scores and rankings
- Scenario-by-scenario performance
- Module usage patterns
- Consistency analysis
- Specific recommendations for improvement

## Contributing

This framework is designed for AI tool evaluation and benchmarking. Contributions welcome for:
- Additional test scenarios
- New internal modules
- Enhanced evaluation metrics
- Analysis improvements

## License

This project is provided for evaluation and benchmarking purposes. See LICENSE file for details.

## Validation

The framework has been designed to:
- ✅ Provide distinct, non-standard APIs different from C/C++ standard library
- ✅ Cover major embedded systems domains (HAL, sensors, protocols, RTOS)
- ✅ Scale from beginner to expert difficulty levels
- ✅ Generate quantitative, reproducible evaluation metrics
- ✅ Support comparative analysis of multiple AI tools
- ✅ Include comprehensive documentation and usage examples

This framework enables objective assessment of AI programming tools' capability to understand and utilize domain-specific internal modules in embedded systems development.