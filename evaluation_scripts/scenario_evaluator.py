#!/usr/bin/env python3
"""
Scenario-specific evaluation script for AI tool testing

This script provides scenario-specific evaluation logic for different test scenarios,
offering detailed analysis based on the specific requirements of each test case.
"""

import json
import argparse
from typing import Dict, List, Any
from module_analyzer import InternalModuleAnalyzer, AnalysisResult
from pathlib import Path

class ScenarioEvaluator:
    def __init__(self):
        self.analyzer = InternalModuleAnalyzer()
        self.scenario_configs = self._load_scenario_configurations()
    
    def _load_scenario_configurations(self) -> Dict[str, Dict]:
        """Load scenario-specific evaluation configurations"""
        return {
            "basic_gpio": {
                "required_modules": ["xgpio_hal"],
                "optional_modules": ["xhw_timer", "xsoft_timer"],
                "required_functions": [
                    "xgpio_init_pin", "xgpio_write_pin", "xgpio_deinit_pin"
                ],
                "expected_patterns": [
                    "gpio_config", "main loop", "timing implementation"
                ],
                "performance_requirements": {
                    "timing_accuracy": "500ms intervals",
                    "duration": "10 seconds",
                    "resource_cleanup": True
                },
                "weight_adjustments": {
                    "module_usage": 0.4,
                    "function_correctness": 0.3,
                    "architecture": 0.2,
                    "error_handling": 0.1
                }
            },
            "sensor_reading": {
                "required_modules": ["xtemp_sensor", "xi2c_hal", "xring_buffer"],
                "optional_modules": ["xsoft_timer", "xhw_timer"],
                "required_functions": [
                    "xtemp_init", "xtemp_read_temperature_c", "xi2c_init",
                    "xring_buffer_init", "xring_buffer_put"
                ],
                "expected_patterns": [
                    "circular buffer", "temperature monitoring", "alert system"
                ],
                "performance_requirements": {
                    "sampling_rate": "100ms",
                    "buffer_size": "50 readings",
                    "alert_threshold": "75°C",
                    "consecutive_alerts": 3
                },
                "weight_adjustments": {
                    "module_usage": 0.35,
                    "function_correctness": 0.25,
                    "architecture": 0.25,
                    "error_handling": 0.15
                }
            },
            "motor_control": {
                "required_modules": [
                    "xgpio_hal", "xhw_timer", "xcan_protocol", "xrtos_scheduler"
                ],
                "optional_modules": [
                    "xdma_manager", "xmem_pool", "xlcd_display", "xring_buffer"
                ],
                "required_functions": [
                    "xrtos_create_task", "xcan_init", "xhw_timer_init",
                    "xgpio_configure_irq"
                ],
                "expected_patterns": [
                    "PID control", "real-time tasks", "safety features",
                    "CAN communication", "interrupt handling"
                ],
                "performance_requirements": {
                    "pid_frequency": "1kHz",
                    "can_update_rate": "100ms",
                    "real_time_constraints": True,
                    "safety_implementation": True
                },
                "weight_adjustments": {
                    "module_usage": 0.25,
                    "function_correctness": 0.20,
                    "architecture": 0.35,
                    "error_handling": 0.20
                }
            },
            "protocol_gateway": {
                "required_modules": [
                    "xmodbus_protocol", "xcan_protocol", "xproprietary_protocol",
                    "xrtos_scheduler", "xcrypto_engine"
                ],
                "optional_modules": [
                    "xmem_pool", "xring_buffer", "xdma_manager", "xpower_mgmt",
                    "xi2c_hal", "xuart_hal", "xspi_hal"
                ],
                "required_functions": [
                    "xmodbus_init", "xcan_init", "xprop_init",
                    "xrtos_create_task", "xcrypto_aes_encrypt"
                ],
                "expected_patterns": [
                    "multi-protocol", "data aggregation", "encryption",
                    "concurrent tasks", "failover mechanisms"
                ],
                "performance_requirements": {
                    "modbus_throughput": "100 transactions/sec",
                    "can_update_rate": "50Hz",
                    "protocol_response_time": "10ms",
                    "concurrent_operations": True
                },
                "weight_adjustments": {
                    "module_usage": 0.20,
                    "function_correctness": 0.18,
                    "architecture": 0.35,
                    "error_handling": 0.27
                }
            }
        }
    
    def evaluate_scenario(self, scenario_name: str, code_content: str, 
                         output_file: str = None) -> Dict[str, Any]:
        """Evaluate code against a specific scenario"""
        
        if scenario_name not in self.scenario_configs:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        
        config = self.scenario_configs[scenario_name]
        
        # Perform basic analysis
        result = self.analyzer.analyze_code(code_content, config)
        
        # Apply scenario-specific evaluation
        scenario_result = self._evaluate_scenario_specific(scenario_name, result, config)
        
        # Generate comprehensive report
        report = self._generate_scenario_report(scenario_name, result, scenario_result, config)
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump({
                    'scenario': scenario_name,
                    'scores': {
                        'total_score': result.total_score,
                        'module_usage_score': result.module_usage_score,
                        'function_correctness_score': result.function_correctness_score,
                        'architecture_score': result.architecture_score,
                        'error_handling_score': result.error_handling_score,
                        'scenario_specific_score': scenario_result['scenario_score']
                    },
                    'detailed_metrics': result.detailed_metrics,
                    'scenario_analysis': scenario_result,
                    'report': report
                }, f, indent=2)
        
        return {
            'scenario': scenario_name,
            'analysis_result': result,
            'scenario_result': scenario_result,
            'report': report
        }
    
    def _evaluate_scenario_specific(self, scenario_name: str, result: AnalysisResult, 
                                   config: Dict) -> Dict[str, Any]:
        """Perform scenario-specific evaluation"""
        
        scenario_result = {
            'scenario_score': 0.0,
            'requirement_compliance': {},
            'performance_analysis': {},
            'recommendations': []
        }
        
        if scenario_name == "basic_gpio":
            scenario_result = self._evaluate_basic_gpio(result, config)
        elif scenario_name == "sensor_reading":
            scenario_result = self._evaluate_sensor_reading(result, config)
        elif scenario_name == "motor_control":
            scenario_result = self._evaluate_motor_control(result, config)
        elif scenario_name == "protocol_gateway":
            scenario_result = self._evaluate_protocol_gateway(result, config)
        
        return scenario_result
    
    def _evaluate_basic_gpio(self, result: AnalysisResult, config: Dict) -> Dict[str, Any]:
        """Evaluate basic GPIO scenario"""
        score = 0.0
        compliance = {}
        recommendations = []
        
        # Check required modules
        required_modules = config["required_modules"]
        modules_found = [m for m in required_modules if m in result.detailed_metrics["modules_utilized"]]
        compliance["required_modules"] = len(modules_found) / len(required_modules)
        score += compliance["required_modules"] * 3.0
        
        # Check GPIO configuration
        gpio_functions = ["xgpio_init_pin", "xgpio_write_pin", "xgpio_deinit_pin"]
        gpio_funcs_found = [f for f in gpio_functions if f in result.detailed_metrics["functions_used"]]
        compliance["gpio_functions"] = len(gpio_funcs_found) / len(gpio_functions)
        score += compliance["gpio_functions"] * 3.0
        
        # Check for timing implementation
        timing_indicators = ["delay", "timer", "sleep", "500"]
        has_timing = any(indicator in str(result.detailed_metrics).lower() for indicator in timing_indicators)
        compliance["timing_implementation"] = 1.0 if has_timing else 0.0
        score += compliance["timing_implementation"] * 2.0
        
        # Check for proper cleanup
        has_cleanup = "xgpio_deinit_pin" in result.detailed_metrics["functions_used"]
        compliance["resource_cleanup"] = 1.0 if has_cleanup else 0.0
        score += compliance["resource_cleanup"] * 2.0
        
        if compliance["required_modules"] < 1.0:
            recommendations.append("Use xgpio_hal module for GPIO operations")
        if compliance["timing_implementation"] < 1.0:
            recommendations.append("Implement proper timing for 500ms intervals")
        if compliance["resource_cleanup"] < 1.0:
            recommendations.append("Add proper GPIO cleanup with xgpio_deinit_pin")
        
        return {
            'scenario_score': min(10.0, score),
            'requirement_compliance': compliance,
            'performance_analysis': {
                'timing_accuracy': compliance["timing_implementation"],
                'resource_management': compliance["resource_cleanup"]
            },
            'recommendations': recommendations
        }
    
    def _evaluate_sensor_reading(self, result: AnalysisResult, config: Dict) -> Dict[str, Any]:
        """Evaluate sensor reading scenario"""
        score = 0.0
        compliance = {}
        recommendations = []
        
        # Check required modules
        required_modules = config["required_modules"]
        modules_found = [m for m in required_modules if m in result.detailed_metrics["modules_utilized"]]
        compliance["required_modules"] = len(modules_found) / len(required_modules)
        score += compliance["required_modules"] * 2.5
        
        # Check sensor interface
        sensor_functions = ["xtemp_init", "xtemp_read_temperature", "xi2c_init"]
        sensor_funcs_found = [f for f in sensor_functions if f in result.detailed_metrics["functions_used"]]
        compliance["sensor_interface"] = len(sensor_funcs_found) / len(sensor_functions)
        score += compliance["sensor_interface"] * 2.5
        
        # Check buffer management
        buffer_functions = ["xring_buffer_init", "xring_buffer_put"]
        buffer_funcs_found = [f for f in buffer_functions if f in result.detailed_metrics["functions_used"]]
        compliance["buffer_management"] = len(buffer_funcs_found) / len(buffer_functions)
        score += compliance["buffer_management"] * 2.5
        
        # Check alert system
        alert_indicators = ["threshold", "alert", "75", "consecutive"]
        has_alert_system = any(indicator in str(result.detailed_metrics).lower() for indicator in alert_indicators)
        compliance["alert_system"] = 1.0 if has_alert_system else 0.0
        score += compliance["alert_system"] * 2.5
        
        if compliance["required_modules"] < 1.0:
            recommendations.append("Use all required modules: temperature sensor, I2C HAL, and ring buffer")
        if compliance["sensor_interface"] < 1.0:
            recommendations.append("Implement proper sensor initialization and data reading")
        if compliance["buffer_management"] < 1.0:
            recommendations.append("Use ring buffer for storing temperature readings")
        if compliance["alert_system"] < 1.0:
            recommendations.append("Implement temperature threshold alert system")
        
        return {
            'scenario_score': min(10.0, score),
            'requirement_compliance': compliance,
            'performance_analysis': {
                'data_collection': compliance["sensor_interface"],
                'data_storage': compliance["buffer_management"],
                'alert_functionality': compliance["alert_system"]
            },
            'recommendations': recommendations
        }
    
    def _evaluate_motor_control(self, result: AnalysisResult, config: Dict) -> Dict[str, Any]:
        """Evaluate motor control scenario"""
        score = 0.0
        compliance = {}
        recommendations = []
        
        # Check RTOS usage
        rtos_functions = ["xrtos_create_task", "xrtos_init", "xrtos_start_scheduler"]
        rtos_funcs_found = [f for f in rtos_functions if f in result.detailed_metrics["functions_used"]]
        compliance["rtos_implementation"] = len(rtos_funcs_found) / len(rtos_functions)
        score += compliance["rtos_implementation"] * 2.0
        
        # Check CAN communication
        can_functions = ["xcan_init", "xcan_transmit", "xcan_receive"]
        can_funcs_found = [f for f in can_functions if f in result.detailed_metrics["functions_used"]]
        compliance["can_communication"] = len(can_funcs_found) / len(can_functions)
        score += compliance["can_communication"] * 2.0
        
        # Check PWM/Timer usage
        timer_functions = ["xhw_timer_init", "xhw_timer_start", "xhw_timer_set_period"]
        timer_funcs_found = [f for f in timer_functions if f in result.detailed_metrics["functions_used"]]
        compliance["timer_usage"] = len(timer_funcs_found) / len(timer_functions)
        score += compliance["timer_usage"] * 2.0
        
        # Check GPIO interrupt handling
        has_gpio_irq = "xgpio_configure_irq" in result.detailed_metrics["functions_used"]
        compliance["interrupt_handling"] = 1.0 if has_gpio_irq else 0.0
        score += compliance["interrupt_handling"] * 2.0
        
        # Check for safety features
        safety_indicators = ["emergency", "stop", "limit", "overcurrent", "safety"]
        has_safety = any(indicator in str(result.detailed_metrics).lower() for indicator in safety_indicators)
        compliance["safety_features"] = 1.0 if has_safety else 0.0
        score += compliance["safety_features"] * 2.0
        
        return {
            'scenario_score': min(10.0, score),
            'requirement_compliance': compliance,
            'performance_analysis': {
                'real_time_capability': compliance["rtos_implementation"],
                'communication_protocols': compliance["can_communication"],
                'motor_control_precision': compliance["timer_usage"],
                'safety_implementation': compliance["safety_features"]
            },
            'recommendations': self._generate_motor_control_recommendations(compliance)
        }
    
    def _evaluate_protocol_gateway(self, result: AnalysisResult, config: Dict) -> Dict[str, Any]:
        """Evaluate protocol gateway scenario"""
        score = 0.0
        compliance = {}
        
        # Check multi-protocol implementation
        protocol_modules = ["xmodbus_protocol", "xcan_protocol", "xproprietary_protocol"]
        protocol_modules_found = [m for m in protocol_modules if m in result.detailed_metrics["modules_utilized"]]
        compliance["multi_protocol"] = len(protocol_modules_found) / len(protocol_modules)
        score += compliance["multi_protocol"] * 2.0
        
        # Check encryption usage
        crypto_functions = ["xcrypto_init", "xcrypto_aes_encrypt", "xcrypto_aes_decrypt"]
        crypto_funcs_found = [f for f in crypto_functions if f in result.detailed_metrics["functions_used"]]
        compliance["encryption"] = len(crypto_funcs_found) / len(crypto_functions)
        score += compliance["encryption"] * 2.0
        
        # Check RTOS implementation
        has_rtos = "xrtos_scheduler" in result.detailed_metrics["modules_utilized"]
        compliance["concurrent_processing"] = 1.0 if has_rtos else 0.0
        score += compliance["concurrent_processing"] * 2.0
        
        # Check memory management
        memory_modules = ["xmem_pool", "xring_buffer", "xdma_manager"]
        memory_modules_found = [m for m in memory_modules if m in result.detailed_metrics["modules_utilized"]]
        compliance["memory_optimization"] = len(memory_modules_found) / len(memory_modules)
        score += compliance["memory_optimization"] * 2.0
        
        # Check power management
        has_power_mgmt = "xpower_mgmt" in result.detailed_metrics["modules_utilized"]
        compliance["power_management"] = 1.0 if has_power_mgmt else 0.0
        score += compliance["power_management"] * 2.0
        
        return {
            'scenario_score': min(10.0, score),
            'requirement_compliance': compliance,
            'performance_analysis': {
                'protocol_integration': compliance["multi_protocol"],
                'security_implementation': compliance["encryption"],
                'system_architecture': compliance["concurrent_processing"],
                'resource_optimization': compliance["memory_optimization"]
            },
            'recommendations': self._generate_gateway_recommendations(compliance)
        }
    
    def _generate_motor_control_recommendations(self, compliance: Dict) -> List[str]:
        """Generate specific recommendations for motor control scenario"""
        recommendations = []
        
        if compliance["rtos_implementation"] < 1.0:
            recommendations.append("Implement proper RTOS task structure for real-time motor control")
        if compliance["can_communication"] < 1.0:
            recommendations.append("Add complete CAN bus communication for commands and status")
        if compliance["timer_usage"] < 1.0:
            recommendations.append("Use hardware timers for precise PWM generation")
        if compliance["interrupt_handling"] < 1.0:
            recommendations.append("Implement GPIO interrupts for encoder feedback")
        if compliance["safety_features"] < 1.0:
            recommendations.append("Add safety features: emergency stop, limits, overcurrent protection")
        
        return recommendations
    
    def _generate_gateway_recommendations(self, compliance: Dict) -> List[str]:
        """Generate specific recommendations for protocol gateway scenario"""
        recommendations = []
        
        if compliance["multi_protocol"] < 1.0:
            recommendations.append("Implement all three protocols: Modbus, CAN, and proprietary")
        if compliance["encryption"] < 1.0:
            recommendations.append("Add data encryption for secure communication")
        if compliance["concurrent_processing"] < 1.0:
            recommendations.append("Use RTOS for concurrent protocol handling")
        if compliance["memory_optimization"] < 1.0:
            recommendations.append("Implement memory pools and efficient buffering")
        if compliance["power_management"] < 1.0:
            recommendations.append("Add power management for low-power operation")
        
        return recommendations
    
    def _generate_scenario_report(self, scenario_name: str, result: AnalysisResult, 
                                 scenario_result: Dict, config: Dict) -> str:
        """Generate a comprehensive scenario-specific report"""
        
        report = f"""
# Scenario Evaluation Report: {scenario_name.replace('_', ' ').title()}

## Overall Performance
- **Total Score**: {result.total_score:.1f}/10.0
- **Scenario-Specific Score**: {scenario_result['scenario_score']:.1f}/10.0

## Component Analysis
- **Module Usage**: {result.module_usage_score:.1f}/10.0
- **Function Correctness**: {result.function_correctness_score:.1f}/10.0
- **Architecture Quality**: {result.architecture_score:.1f}/10.0
- **Error Handling**: {result.error_handling_score:.1f}/10.0

## Requirement Compliance
"""
        
        for requirement, score in scenario_result['requirement_compliance'].items():
            status = "✅" if score >= 0.8 else "⚠️" if score >= 0.5 else "❌"
            report += f"- **{requirement.replace('_', ' ').title()}**: {score:.1%} {status}\n"
        
        report += f"""
## Performance Analysis
"""
        for metric, value in scenario_result['performance_analysis'].items():
            report += f"- **{metric.replace('_', ' ').title()}**: {value:.1%}\n"
        
        if scenario_result['recommendations']:
            report += f"""
## Recommendations for Improvement
"""
            for rec in scenario_result['recommendations']:
                report += f"- {rec}\n"
        
        report += f"""
## Module Utilization Details
- **Modules Used**: {', '.join(result.detailed_metrics['modules_utilized']) or 'None'}
- **Functions Called**: {len(result.detailed_metrics['functions_used'])}
- **Types Utilized**: {len(result.detailed_metrics['types_used'])}
- **Constants Used**: {len(result.detailed_metrics['constants_used'])}

## Code Quality Metrics
- **Total Lines**: {result.detailed_metrics['total_lines']}
- **Function Definitions**: {result.detailed_metrics['function_definitions']}
- **Error Handling Patterns**: {len(result.detailed_metrics['error_handling_patterns'])}
"""
        
        return report

def main():
    """Command line interface for scenario evaluation"""
    parser = argparse.ArgumentParser(description='Evaluate AI-generated code against specific scenarios')
    parser.add_argument('scenario', choices=['basic_gpio', 'sensor_reading', 'motor_control', 'protocol_gateway'],
                       help='Test scenario to evaluate against')
    parser.add_argument('code_file', help='Path to C/C++ code file to analyze')
    parser.add_argument('--output', '-o', help='Output file for results (JSON format)')
    parser.add_argument('--report', '-r', help='Output file for human-readable report')
    
    args = parser.parse_args()
    
    # Read code file
    with open(args.code_file, 'r') as f:
        code_content = f.read()
    
    # Perform evaluation
    evaluator = ScenarioEvaluator()
    results = evaluator.evaluate_scenario(args.scenario, code_content, args.output)
    
    # Output report
    if args.report:
        with open(args.report, 'w') as f:
            f.write(results['report'])
    else:
        print(results['report'])
    
    print(f"\nOverall Score: {results['analysis_result'].total_score:.1f}/10.0")
    print(f"Scenario Score: {results['scenario_result']['scenario_score']:.1f}/10.0")

if __name__ == "__main__":
    main()