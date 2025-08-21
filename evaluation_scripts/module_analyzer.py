#!/usr/bin/env python3
"""
AI Tool Evaluation Script for Internal Module Usage Analysis

This script analyzes generated C/C++ code to quantify the usage of internal modules
and provide detailed metrics for AI tool evaluation.
"""

import re
import os
import json
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ModuleInfo:
    """Information about an internal module"""
    name: str
    header: str
    functions: List[str]
    types: List[str]
    constants: List[str]

@dataclass
class AnalysisResult:
    """Results of code analysis"""
    total_score: float
    module_usage_score: float
    function_correctness_score: float
    architecture_score: float
    error_handling_score: float
    detailed_metrics: Dict

class InternalModuleAnalyzer:
    def __init__(self, modules_path: str = "internal_modules"):
        self.modules_path = modules_path
        self.modules_info = self._load_module_definitions()
        
    def _load_module_definitions(self) -> Dict[str, ModuleInfo]:
        """Load all internal module definitions from header files"""
        modules = {}
        
        # Define our internal modules with their key functions
        module_definitions = {
            "xgpio_hal": {
                "header": "internal_modules/hal/xgpio_hal.h",
                "functions": [
                    "xgpio_init_pin", "xgpio_deinit_pin", "xgpio_write_pin",
                    "xgpio_read_pin", "xgpio_toggle_pin", "xgpio_configure_irq"
                ],
                "types": ["xgpio_config_t", "xgpio_pin_state_t", "xgpio_pin_mode_t"],
                "constants": ["XGPIO_PIN_HIGH", "XGPIO_PIN_LOW", "XGPIO_MODE_OUTPUT"]
            },
            "xspi_hal": {
                "header": "internal_modules/hal/xspi_hal.h",
                "functions": [
                    "xspi_init", "xspi_transfer", "xspi_transmit", "xspi_receive"
                ],
                "types": ["xspi_config_t", "xspi_transfer_t", "xspi_mode_t"],
                "constants": ["XSPI_MODE_0", "XSPI_BITORDER_MSB"]
            },
            "xi2c_hal": {
                "header": "internal_modules/hal/xi2c_hal.h",
                "functions": [
                    "xi2c_init", "xi2c_master_transmit", "xi2c_master_receive",
                    "xi2c_mem_read", "xi2c_mem_write"
                ],
                "types": ["xi2c_config_t", "xi2c_speed_t", "xi2c_status_t"],
                "constants": ["XI2C_SPEED_STANDARD", "XI2C_STATUS_OK"]
            },
            "xuart_hal": {
                "header": "internal_modules/hal/xuart_hal.h",
                "functions": [
                    "xuart_init", "xuart_transmit", "xuart_receive",
                    "xuart_transmit_async", "xuart_receive_async"
                ],
                "types": ["xuart_config_t", "xuart_baudrate_t", "xuart_parity_t"],
                "constants": ["XUART_BAUDRATE_115200", "XUART_PARITY_NONE"]
            },
            "xtemp_sensor": {
                "header": "internal_modules/sensors/xtemp_sensor.h",
                "functions": [
                    "xtemp_init", "xtemp_read_temperature", "xtemp_read_temperature_c",
                    "xtemp_set_thresholds", "xtemp_enable_alerts"
                ],
                "types": ["xtemp_config_t", "xtemp_data_t", "xtemp_resolution_t"],
                "constants": ["XTEMP_RESOLUTION_12BIT", "XTEMP_MODE_CONTINUOUS"]
            },
            "xaccel_sensor": {
                "header": "internal_modules/sensors/xaccel_sensor.h",
                "functions": [
                    "xaccel_init", "xaccel_read_data", "xaccel_calibrate",
                    "xaccel_enable_motion_detection"
                ],
                "types": ["xaccel_config_t", "xaccel_data_t", "xaccel_range_t"],
                "constants": ["XACCEL_RANGE_2G", "XACCEL_ODR_100HZ"]
            },
            "xgyro_sensor": {
                "header": "internal_modules/sensors/xgyro_sensor.h",
                "functions": [
                    "xgyro_init", "xgyro_read_data", "xgyro_calibrate_bias",
                    "xgyro_perform_self_test"
                ],
                "types": ["xgyro_config_t", "xgyro_data_t", "xgyro_range_t"],
                "constants": ["XGYRO_RANGE_250DPS", "XGYRO_ODR_104HZ"]
            },
            "xmem_pool": {
                "header": "internal_modules/memory/xmem_pool.h",
                "functions": [
                    "xmem_pool_create", "xmem_pool_alloc", "xmem_pool_free",
                    "xmem_pool_get_stats", "xmem_pool_check_integrity"
                ],
                "types": ["xmem_pool_config_t", "xmem_pool_stats_t", "xmem_pool_handle_t"],
                "constants": ["XMEM_POOL_STATUS_OK", "XMEM_POOL_STATUS_FULL"]
            },
            "xring_buffer": {
                "header": "internal_modules/memory/xring_buffer.h",
                "functions": [
                    "xring_buffer_init", "xring_buffer_put", "xring_buffer_get",
                    "xring_buffer_put_multiple", "xring_buffer_is_full"
                ],
                "types": ["xring_buffer_t", "xring_buffer_stats_t", "xring_buffer_mode_t"],
                "constants": ["XRING_BUFFER_OK", "XRING_BUFFER_MODE_OVERWRITE"]
            },
            "xdma_manager": {
                "header": "internal_modules/memory/xdma_manager.h",
                "functions": [
                    "xdma_init", "xdma_allocate_channel", "xdma_configure_transfer",
                    "xdma_start_transfer", "xdma_get_transfer_status"
                ],
                "types": ["xdma_transfer_config_t", "xdma_status_t", "xdma_priority_t"],
                "constants": ["XDMA_STATUS_COMPLETE", "XDMA_PRIORITY_HIGH"]
            },
            "xcan_protocol": {
                "header": "internal_modules/protocols/xcan_protocol.h",
                "functions": [
                    "xcan_init", "xcan_start", "xcan_transmit", "xcan_receive",
                    "xcan_add_filter", "xcan_set_rx_callback"
                ],
                "types": ["xcan_config_t", "xcan_frame_t", "xcan_bitrate_t"],
                "constants": ["XCAN_BITRATE_500K", "XCAN_FRAME_STANDARD"]
            },
            "xmodbus_protocol": {
                "header": "internal_modules/protocols/xmodbus_protocol.h",
                "functions": [
                    "xmodbus_init", "xmodbus_read_holding_registers",
                    "xmodbus_write_multiple_registers", "xmodbus_master_request"
                ],
                "types": ["xmodbus_config_t", "xmodbus_request_t", "xmodbus_mode_t"],
                "constants": ["XMODBUS_MODE_RTU", "XMODBUS_STATUS_OK"]
            },
            "xproprietary_protocol": {
                "header": "internal_modules/protocols/xproprietary_protocol.h",
                "functions": [
                    "xprop_init", "xprop_send_packet", "xprop_send_data",
                    "xprop_process_received_data", "xprop_set_rx_callback"
                ],
                "types": ["xprop_config_t", "xprop_packet_t", "xprop_priority_t"],
                "constants": ["XPROP_PACKET_TYPE_DATA", "XPROP_PRIORITY_HIGH"]
            },
            "xrtos_scheduler": {
                "header": "internal_modules/scheduler/xrtos_scheduler.h",
                "functions": [
                    "xrtos_init", "xrtos_create_task", "xrtos_start_scheduler",
                    "xrtos_delay", "xrtos_yield"
                ],
                "types": ["xrtos_task_config_t", "xrtos_task_handle_t", "xrtos_priority_t"],
                "constants": ["XRTOS_PRIORITY_HIGH", "XRTOS_SCHED_POLICY_RR"]
            },
            "xhw_timer": {
                "header": "internal_modules/scheduler/xhw_timer.h",
                "functions": [
                    "xhw_timer_init", "xhw_timer_start", "xhw_timer_set_period",
                    "xhw_timer_set_callback", "xhw_timer_get_timestamp_us"
                ],
                "types": ["xhw_timer_config_t", "xhw_timer_mode_t", "xhw_timer_status_t"],
                "constants": ["XHW_TIMER_MODE_PERIODIC", "XHW_TIMER_STATUS_RUNNING"]
            },
            "xsoft_timer": {
                "header": "internal_modules/scheduler/xsoft_timer.h",
                "functions": [
                    "xsoft_timer_init", "xsoft_timer_create", "xsoft_timer_start",
                    "xsoft_timer_set_period", "xsoft_timer_process_timers"
                ],
                "types": ["xsoft_timer_config_t", "xsoft_timer_handle_t", "xsoft_timer_type_t"],
                "constants": ["XSOFT_TIMER_PERIODIC", "XSOFT_TIMER_STATUS_ACTIVE"]
            },
            "xlcd_display": {
                "header": "internal_modules/display/xlcd_display.h",
                "functions": [
                    "xlcd_init", "xlcd_clear_screen", "xlcd_draw_text",
                    "xlcd_draw_rectangle", "xlcd_set_backlight"
                ],
                "types": ["xlcd_config_t", "xlcd_color_t", "xlcd_rotation_t"],
                "constants": ["XLCD_ROTATION_0", "XLCD_FONT_MEDIUM"]
            },
            "xpower_mgmt": {
                "header": "internal_modules/power/xpower_mgmt.h",
                "functions": [
                    "xpower_init", "xpower_set_mode", "xpower_enable_domain",
                    "xpower_get_status", "xpower_enter_sleep_mode"
                ],
                "types": ["xpower_config_t", "xpower_status_t", "xpower_mode_t"],
                "constants": ["XPOWER_MODE_SLEEP", "XPOWER_DOMAIN_CPU"]
            },
            "xcrypto_engine": {
                "header": "internal_modules/crypto/xcrypto_engine.h",
                "functions": [
                    "xcrypto_init", "xcrypto_aes_encrypt", "xcrypto_aes_decrypt",
                    "xcrypto_hash_compute", "xcrypto_generate_random"
                ],
                "types": ["xcrypto_aes_config_t", "xcrypto_context_t", "xcrypto_status_t"],
                "constants": ["XCRYPTO_AES_256", "XCRYPTO_STATUS_OK"]
            }
        }
        
        for name, info in module_definitions.items():
            modules[name] = ModuleInfo(
                name=name,
                header=info["header"],
                functions=info["functions"],
                types=info["types"],
                constants=info["constants"]
            )
        
        return modules
    
    def analyze_code(self, code_content: str, scenario_requirements: Dict = None) -> AnalysisResult:
        """Analyze code for internal module usage and generate metrics"""
        
        # Initialize metrics
        metrics = {
            "includes_found": [],
            "functions_used": [],
            "types_used": [],
            "constants_used": [],
            "modules_utilized": [],
            "error_handling_patterns": [],
            "architecture_patterns": [],
            "total_lines": 0,
            "comment_lines": 0,
            "function_definitions": 0
        }
        
        # Basic code statistics
        lines = code_content.split('\n')
        metrics["total_lines"] = len(lines)
        metrics["comment_lines"] = sum(1 for line in lines if line.strip().startswith('//') or line.strip().startswith('/*'))
        metrics["function_definitions"] = len(re.findall(r'\w+\s+\w+\s*\([^)]*\)\s*{', code_content))
        
        # Find included headers
        include_pattern = r'#include\s*[<"]([^>"]*)[>"]'
        includes = re.findall(include_pattern, code_content)
        metrics["includes_found"] = includes
        
        # Check for internal module usage
        used_modules = set()
        for module_name, module_info in self.modules_info.items():
            # Check if module header is included
            if any(module_info.header.split('/')[-1] in include or module_info.header in include for include in includes):
                used_modules.add(module_name)
                
                # Check for function usage
                for func in module_info.functions:
                    if re.search(rf'\b{func}\s*\(', code_content):
                        metrics["functions_used"].append(func)
                
                # Check for type usage
                for type_name in module_info.types:
                    if re.search(rf'\b{type_name}\b', code_content):
                        metrics["types_used"].append(type_name)
                
                # Check for constant usage
                for const in module_info.constants:
                    if re.search(rf'\b{const}\b', code_content):
                        metrics["constants_used"].append(const)
        
        metrics["modules_utilized"] = list(used_modules)
        
        # Analyze error handling patterns
        error_patterns = [
            r'if\s*\([^)]*!=\s*0\)',  # Return value checking
            r'if\s*\([^)]*<\s*0\)',   # Negative return checking
            r'if\s*\([^)]*==\s*NULL\)', # NULL pointer checking
            r'return\s*-?\d+;',        # Error return codes
        ]
        
        for pattern in error_patterns:
            matches = re.findall(pattern, code_content)
            metrics["error_handling_patterns"].extend(matches)
        
        # Analyze architecture patterns
        arch_patterns = [
            (r'typedef\s+struct', "struct_definitions"),
            (r'static\s+\w+', "static_variables"),
            (r'void\s+\w+\s*\([^)]*\)\s*{', "function_definitions"),
            (r'#define\s+\w+', "macro_definitions"),
            (r'enum\s+\w+', "enum_definitions"),
        ]
        
        for pattern, category in arch_patterns:
            matches = re.findall(pattern, code_content)
            if matches:
                metrics["architecture_patterns"].append({
                    "category": category,
                    "count": len(matches),
                    "examples": matches[:3]  # First 3 examples
                })
        
        # Calculate scores
        module_usage_score = self._calculate_module_usage_score(metrics, scenario_requirements)
        function_correctness_score = self._calculate_function_correctness_score(metrics, scenario_requirements)
        architecture_score = self._calculate_architecture_score(metrics)
        error_handling_score = self._calculate_error_handling_score(metrics)
        
        # Calculate total score (weighted average)
        total_score = (
            module_usage_score * 0.4 +
            function_correctness_score * 0.3 +
            architecture_score * 0.2 +
            error_handling_score * 0.1
        )
        
        return AnalysisResult(
            total_score=total_score,
            module_usage_score=module_usage_score,
            function_correctness_score=function_correctness_score,
            architecture_score=architecture_score,
            error_handling_score=error_handling_score,
            detailed_metrics=metrics
        )
    
    def _calculate_module_usage_score(self, metrics: Dict, requirements: Dict = None) -> float:
        """Calculate score based on internal module usage"""
        if not requirements:
            # Generic scoring based on number of modules used
            num_modules_used = len(metrics["modules_utilized"])
            if num_modules_used == 0:
                return 0.0
            elif num_modules_used <= 2:
                return 3.0
            elif num_modules_used <= 4:
                return 6.0
            elif num_modules_used <= 6:
                return 8.0
            else:
                return 10.0
        
        # Score based on specific requirements
        required_modules = requirements.get("required_modules", [])
        optional_modules = requirements.get("optional_modules", [])
        
        required_found = sum(1 for mod in required_modules if mod in metrics["modules_utilized"])
        optional_found = sum(1 for mod in optional_modules if mod in metrics["modules_utilized"])
        
        required_score = (required_found / len(required_modules)) * 8.0 if required_modules else 0
        optional_score = (optional_found / len(optional_modules)) * 2.0 if optional_modules else 0
        
        return min(10.0, required_score + optional_score)
    
    def _calculate_function_correctness_score(self, metrics: Dict, requirements: Dict = None) -> float:
        """Calculate score based on function usage correctness"""
        functions_used = len(metrics["functions_used"])
        types_used = len(metrics["types_used"])
        constants_used = len(metrics["constants_used"])
        
        # Base score on diversity of API usage
        api_diversity_score = min(10.0, (functions_used * 0.5 + types_used * 0.3 + constants_used * 0.2))
        
        if requirements:
            required_functions = requirements.get("required_functions", [])
            if required_functions:
                function_score = sum(1 for func in required_functions if func in metrics["functions_used"])
                return (function_score / len(required_functions)) * 10.0
        
        return api_diversity_score
    
    def _calculate_architecture_score(self, metrics: Dict) -> float:
        """Calculate score based on code architecture quality"""
        score = 5.0  # Base score
        
        # Bonus for good structure
        if metrics["function_definitions"] > 0:
            score += 1.0
        
        # Check for proper organization
        arch_patterns = {p["category"]: p["count"] for p in metrics["architecture_patterns"]}
        
        if arch_patterns.get("struct_definitions", 0) > 0:
            score += 1.0
        if arch_patterns.get("static_variables", 0) > 0:
            score += 0.5
        if arch_patterns.get("macro_definitions", 0) > 0:
            score += 0.5
        if arch_patterns.get("enum_definitions", 0) > 0:
            score += 1.0
        
        # Penalty for very short code (likely incomplete)
        if metrics["total_lines"] < 20:
            score -= 2.0
        
        return max(0.0, min(10.0, score))
    
    def _calculate_error_handling_score(self, metrics: Dict) -> float:
        """Calculate score based on error handling implementation"""
        error_patterns = len(metrics["error_handling_patterns"])
        
        if error_patterns == 0:
            return 0.0
        elif error_patterns <= 2:
            return 3.0
        elif error_patterns <= 5:
            return 6.0
        elif error_patterns <= 8:
            return 8.0
        else:
            return 10.0
    
    def generate_report(self, result: AnalysisResult, output_file: str = None) -> str:
        """Generate a detailed analysis report"""
        report = f"""
# Internal Module Usage Analysis Report

## Overall Score: {result.total_score:.1f}/10.0

### Component Scores:
- Module Usage: {result.module_usage_score:.1f}/10.0
- Function Correctness: {result.function_correctness_score:.1f}/10.0
- Architecture Quality: {result.architecture_score:.1f}/10.0
- Error Handling: {result.error_handling_score:.1f}/10.0

### Detailed Metrics:

#### Modules Utilized ({len(result.detailed_metrics['modules_utilized'])}):
{chr(10).join(f"- {module}" for module in result.detailed_metrics['modules_utilized'])}

#### Functions Used ({len(result.detailed_metrics['functions_used'])}):
{chr(10).join(f"- {func}" for func in result.detailed_metrics['functions_used'][:10])}
{"..." if len(result.detailed_metrics['functions_used']) > 10 else ""}

#### Types Used ({len(result.detailed_metrics['types_used'])}):
{chr(10).join(f"- {type_name}" for type_name in result.detailed_metrics['types_used'][:10])}
{"..." if len(result.detailed_metrics['types_used']) > 10 else ""}

#### Code Statistics:
- Total Lines: {result.detailed_metrics['total_lines']}
- Comment Lines: {result.detailed_metrics['comment_lines']}
- Function Definitions: {result.detailed_metrics['function_definitions']}
- Error Handling Patterns: {len(result.detailed_metrics['error_handling_patterns'])}

#### Recommendations:
"""
        
        # Add recommendations based on scores
        if result.module_usage_score < 5.0:
            report += "- Increase usage of internal modules instead of standard library functions\n"
        
        if result.function_correctness_score < 5.0:
            report += "- Use more diverse API functions from the internal modules\n"
        
        if result.architecture_score < 5.0:
            report += "- Improve code structure with proper data types and organization\n"
        
        if result.error_handling_score < 5.0:
            report += "- Add more comprehensive error handling and return value checking\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report

def main():
    """Example usage of the analyzer"""
    analyzer = InternalModuleAnalyzer()
    
    # Example code analysis
    sample_code = '''
#include "internal_modules/hal/xgpio_hal.h"
#include "internal_modules/scheduler/xsoft_timer.h"

int main() {
    xgpio_config_t gpio_config = {
        .port = 2,
        .pin = 5,
        .mode = XGPIO_MODE_OUTPUT,
        .pull = XGPIO_PULL_NONE
    };
    
    if (xgpio_init_pin(2, 5, &gpio_config) != 0) {
        return -1;
    }
    
    for (int i = 0; i < 20; i++) {
        xgpio_write_pin(2, 5, XGPIO_PIN_HIGH);
        xsoft_timer_delay_ms(500);
        xgpio_write_pin(2, 5, XGPIO_PIN_LOW);
        xsoft_timer_delay_ms(500);
    }
    
    xgpio_deinit_pin(2, 5);
    return 0;
}
'''
    
    result = analyzer.analyze_code(sample_code)
    report = analyzer.generate_report(result)
    print(report)

if __name__ == "__main__":
    main()