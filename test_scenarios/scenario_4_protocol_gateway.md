# Test Scenario 4: Multi-Protocol Gateway

## Difficulty Level: Expert

## Prompt for AI Tool:
```
Create a comprehensive protocol gateway system that bridges multiple communication protocols in an industrial IoT environment:

REQUIREMENTS:
1. Accept sensor data via Modbus RTU from up to 8 slave devices
2. Aggregate and process sensor data (filtering, scaling, validation)
3. Forward processed data via CAN bus to main control system
4. Implement our proprietary protocol over UART for configuration commands
5. Provide secure data encryption for sensitive sensor readings
6. Implement data caching with configurable retention policies
7. Support firmware updates via encrypted packages
8. Monitor system health and send diagnostics via all protocols
9. Implement redundant communication paths with automatic failover
10. Support real-time data streaming with QoS levels
11. Include comprehensive logging and debugging capabilities
12. Provide power management with sleep modes during low activity

PERFORMANCE REQUIREMENTS:
- Handle 100 Modbus transactions per second
- CAN bus updates at 50Hz minimum
- Proprietary protocol response time < 10ms
- Support concurrent protocol operations
- Memory usage optimization for embedded constraints
- Graceful degradation under high load

Use exclusively our internal modules for all functionality.
```

## Expected Internal Modules Usage:
All major modules should be utilized:
- `xmodbus_protocol.h` - Modbus RTU communication
- `xcan_protocol.h` - CAN bus interface
- `xproprietary_protocol.h` - Custom protocol handling
- `xuart_hal.h`, `xi2c_hal.h`, `xspi_hal.h` - Hardware interfaces
- `xcrypto_engine.h` - Data encryption/decryption
- `xrtos_scheduler.h` - Multi-task coordination
- `xmem_pool.h` - Dynamic memory management
- `xring_buffer.h` - Data buffering and caching
- `xdma_manager.h` - Efficient data transfers
- `xpower_mgmt.h` - Power optimization
- `xhw_timer.h`, `xsoft_timer.h` - Timing and scheduling
- `xlcd_display.h` - Status display (optional)

## System Architecture Requirements:
```c
// Multi-task system with:
// - Modbus Master Task (handles 8 slaves)
// - CAN Communication Task
// - Proprietary Protocol Task
// - Data Processing Task
// - Encryption/Security Task
// - Power Management Task
// - System Monitor Task
// - Firmware Update Task

// Key data structures:
typedef struct {
    uint8_t slave_id;
    uint32_t last_update;
    sensor_data_t data;
    protocol_status_t status;
} modbus_slave_info_t;

typedef struct {
    protocol_type_t source;
    data_priority_t priority;
    encryption_level_t security;
    uint8_t* payload;
    uint32_t length;
    uint32_t timestamp;
} gateway_message_t;
```

## Evaluation Criteria:
1. **Protocol Integration (20%)**: Correct implementation of all three protocols
2. **System Architecture (18%)**: Proper RTOS design, task coordination, resource sharing
3. **Performance Optimization (15%)**: Meeting throughput and latency requirements
4. **Security Implementation (12%)**: Proper encryption, secure firmware updates
5. **Memory Management (10%)**: Efficient use of memory pools and buffers
6. **Error Handling (10%)**: Robust error recovery, failover mechanisms
7. **Power Management (8%)**: Effective power optimization strategies
8. **Code Quality (7%)**: Structure, maintainability, documentation

## Advanced Features Expected:
- Protocol message queuing with priorities
- Automatic protocol detection and configuration
- Dynamic load balancing between communication channels
- Comprehensive statistics and performance monitoring
- Self-diagnostic capabilities
- Configuration persistence across power cycles

## Scoring Rubric:
- **9-10 points**: Complete gateway system, all protocols working, excellent performance, robust security, optimal resource usage
- **7-8 points**: Most protocols implemented, good performance, basic security, efficient resource usage
- **5-6 points**: Some protocols working, acceptable performance, limited security features
- **3-4 points**: Basic protocol implementation, performance issues, minimal security
- **1-2 points**: Simple protocol bridge, significant limitations, poor resource management
- **0 points**: No comprehensive protocol integration, minimal internal module usage