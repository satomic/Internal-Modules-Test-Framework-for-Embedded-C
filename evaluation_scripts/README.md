# Evaluation Scripts

This directory contains Python scripts for analyzing and evaluating AI-generated code against internal module usage criteria.

## Scripts Overview

### 1. module_analyzer.py
Core analysis engine that examines C/C++ code for internal module usage.

**Features:**
- Identifies included internal module headers
- Tracks function, type, and constant usage
- Analyzes code architecture patterns
- Evaluates error handling implementation
- Generates detailed metrics and scores

**Usage:**
```python
from module_analyzer import InternalModuleAnalyzer

analyzer = InternalModuleAnalyzer()
result = analyzer.analyze_code(code_content)
report = analyzer.generate_report(result)
```

### 2. scenario_evaluator.py
Scenario-specific evaluation with tailored requirements and scoring.

**Features:**
- Scenario-specific requirement checking
- Customized scoring weights per scenario
- Performance requirement validation
- Targeted recommendations
- Detailed compliance reports

**Usage:**
```bash
python scenario_evaluator.py basic_gpio code.c --output results.json --report report.md
```

### 3. batch_evaluator.py
Batch processing and comparative analysis of multiple AI tools.

**Features:**
- Multi-tool evaluation across all scenarios
- Statistical analysis and rankings
- Consistency metrics
- Comparative reporting
- Export to multiple formats

**Usage:**
```bash
python batch_evaluator.py ai_tools_directory --output results --report comparison.md
```

## Evaluation Metrics

### Core Scores (0-10 scale)
1. **Module Usage Score (40% weight)**: Usage of appropriate internal modules
2. **Function Correctness Score (30% weight)**: Proper API usage
3. **Architecture Score (20% weight)**: Code structure quality
4. **Error Handling Score (10% weight)**: Robustness implementation

### Scenario-Specific Metrics
Each scenario includes additional targeted metrics:
- **Basic GPIO**: Timing accuracy, resource cleanup
- **Sensor Reading**: Data management, alert system
- **Motor Control**: Real-time capability, safety features
- **Protocol Gateway**: Multi-protocol integration, security

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Output Formats

### JSON Results
```json
{
  "scenario": "basic_gpio",
  "scores": {
    "total_score": 8.5,
    "module_usage_score": 9.0,
    "function_correctness_score": 8.5,
    "architecture_score": 8.0,
    "error_handling_score": 8.5
  },
  "detailed_metrics": {
    "modules_utilized": ["xgpio_hal", "xsoft_timer"],
    "functions_used": ["xgpio_init_pin", "xgpio_write_pin"],
    "requirement_compliance": {...}
  }
}
```

### Markdown Reports
Human-readable reports with:
- Executive summary
- Detailed scoring breakdown
- Module usage analysis
- Recommendations for improvement
- Comparative rankings (for batch evaluation)

## Customization

### Adding New Scenarios
1. Define scenario configuration in `scenario_evaluator.py`
2. Implement scenario-specific evaluation logic
3. Add scenario markdown file to `../test_scenarios/`

### Extending Module Definitions
Update module definitions in `module_analyzer.py`:
```python
module_definitions = {
    "new_module": {
        "header": "internal_modules/category/new_module.h",
        "functions": ["func1", "func2"],
        "types": ["type1_t", "type2_t"],
        "constants": ["CONST1", "CONST2"]
    }
}
```

## Example Workflow

```bash
# 1. Evaluate single file
python scenario_evaluator.py basic_gpio my_code.c

# 2. Batch evaluate multiple tools
mkdir ai_tools_results
mkdir ai_tools_results/tool_a
mkdir ai_tools_results/tool_b
# Place scenario code files in each tool directory

python batch_evaluator.py ai_tools_results --output evaluation_results

# 3. View results
cat evaluation_results/comparison_report.md
```

## Validation and Testing

The evaluation scripts include built-in validation:
- Code parsing robustness
- Metric calculation accuracy
- Scenario requirement validation
- Report generation integrity

Run the built-in tests:
```bash
python module_analyzer.py  # Runs example analysis
python scenario_evaluator.py --help  # Shows usage options
```