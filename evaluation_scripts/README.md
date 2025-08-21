# Evaluation Scripts

This directory contains Python scripts for analyzing and evaluating AI-generated code against internal module usage criteria.

## Prerequisites

Before using these evaluation scripts, ensure you have:
1. **Cloned the source code repository**: https://github.com/satomic/Embedded-C-Application
2. **Set up the environment**: The evaluation scripts analyze code that uses internal modules from the Embedded-C-Application repository

## Repository Structure
- **This repository**: Contains evaluation scripts and test scenarios
- **Embedded-C-Application**: Contains actual internal modules implementation that AI tools should use

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

### Software Requirements
- Python 3.7+
- No external dependencies (uses only standard library)

### Repository Requirements
- **This repository**: For evaluation scripts and test scenarios
- **Embedded-C-Application repository**: For internal modules source code
  ```bash
  git clone https://github.com/satomic/Embedded-C-Application.git
  ```
- In the Embedded-C-Application repository, use the AI ​​programming assistant to generate code based on prompts for each scenario.

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

### Setup
```bash
# 1. Clone both repositories
git clone https://github.com/satomic/Internal-Modules-Test-Framework-for-Embedded-C.git
git clone https://github.com/satomic/Embedded-C-Application.git
```

### Generate Code with AI Assistant
1. In the Embedded-C-Application repository, use the AI programming assistant to generate code based on prompts for each scenario.
2. for example a new `my_code.c` file could be created for the basic GPIO scenario.

### Evaluation
```bash
# 1. Navigate to evaluation scripts, Evaluate single file (AI-generated code using internal modules)
cd Internal-Modules-Test-Framework-for-Embedded-C/evaluation_scripts
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

### Important Notes
- The AI-generated code being evaluated should use internal modules from the Embedded-C-Application repository
- Evaluation scripts will check for proper include statements, function calls, and usage patterns
- Make sure AI tools have access to the internal modules documentation when generating code

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