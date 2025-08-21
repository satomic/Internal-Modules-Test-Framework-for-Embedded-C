# AI Tool Evaluation Test Scenarios

This document provides comprehensive test scenarios designed to evaluate AI programming tools' ability to understand, utilize, and correctly implement code using our internal embedded system modules.

## Important: Source Code Repository

The test scenarios in this repository require AI tools to use internal modules from a separate source code repository:

**Internal Modules Repository**: https://github.com/satomic/Embedded-C-Application

### Setup for AI Tool Testing
1. Clone both repositories:
   ```bash
   git clone https://github.com/satomic/Internal-Modules-Test-Framework-for-Embedded-C.git
   git clone https://github.com/satomic/Embedded-C-Application.git
   ```
2. Provide AI tools access to the internal modules documentation and headers from the Embedded-C-Application repository
3. Use the test scenarios from this repository to prompt AI tools
4. Evaluate the generated code using the evaluation scripts in this repository


## Evaluation Criteria

Each test scenario is evaluated on:
- **Module Usage Rate**: Percentage of required internal modules correctly used
- **Function Correctness**: Accuracy of function calls and parameter usage
- **Architecture Quality**: Code structure and embedded system best practices
- **Error Handling**: Proper error checking and resource management
- **Performance Considerations**: Appropriate use of embedded system optimizations

## Test Execution

### Prerequisites
- Clone both repositories (this framework + Embedded-C-Application)
- Ensure AI tool has access to internal modules documentation from Embedded-C-Application
- Install Python evaluation dependencies

### Execution Steps
1. **Prepare AI Tool**: Configure with access to internal modules headers and documentation from the Embedded-C-Application repository
2. **Present Scenario**: Use the test scenario prompts from this repository
3. **Generate Code**: AI tool generates code using the internal modules
4. **Analyze Code**: Use evaluation scripts to analyze the generated code
5. **Record Metrics**: Collect quantitative and qualitative assessment

### Expected Internal Modules Usage
AI-generated code should properly:
- Include appropriate headers from `internal_modules/` directory
- Use module-specific functions, types, and constants
- Follow embedded systems best practices
- Handle errors and manage resources correctly

## Scoring System

- **Score 0-2**: Basic functionality, minimal internal module usage
- **Score 3-5**: Good functionality, some internal modules used correctly
- **Score 6-8**: Advanced functionality, most internal modules used appropriately
- **Score 9-10**: Expert level implementation, optimal use of all relevant internal modules