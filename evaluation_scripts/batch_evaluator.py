#!/usr/bin/env python3
"""
Batch evaluation script for testing multiple AI tools across all scenarios

This script allows for systematic evaluation of multiple AI tools across all test scenarios,
generating comparative reports and statistical analysis.
"""

import os
import json
import argparse
import statistics
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime
from scenario_evaluator import ScenarioEvaluator

class BatchEvaluator:
    def __init__(self):
        self.evaluator = ScenarioEvaluator()
        self.scenarios = ['basic_gpio', 'sensor_reading', 'motor_control', 'protocol_gateway']
        
    def evaluate_tool(self, tool_name: str, code_directory: str, output_directory: str) -> Dict[str, Any]:
        """Evaluate a single AI tool across all scenarios"""
        
        tool_results = {
            'tool_name': tool_name,
            'evaluation_timestamp': datetime.now().isoformat(),
            'scenario_results': {},
            'summary_metrics': {}
        }
        
        scenario_scores = []
        
        for scenario in self.scenarios:
            code_file = Path(code_directory) / f"{scenario}.c"
            
            if not code_file.exists():
                print(f"Warning: Code file not found for {tool_name} - {scenario}")
                continue
            
            with open(code_file, 'r') as f:
                code_content = f.read()
            
            # Evaluate scenario
            try:
                results = self.evaluator.evaluate_scenario(scenario, code_content)
                tool_results['scenario_results'][scenario] = {
                    'total_score': results['analysis_result'].total_score,
                    'scenario_score': results['scenario_result']['scenario_score'],
                    'module_usage_score': results['analysis_result'].module_usage_score,
                    'function_correctness_score': results['analysis_result'].function_correctness_score,
                    'architecture_score': results['analysis_result'].architecture_score,
                    'error_handling_score': results['analysis_result'].error_handling_score,
                    'modules_used': results['analysis_result'].detailed_metrics['modules_utilized'],
                    'functions_used_count': len(results['analysis_result'].detailed_metrics['functions_used']),
                    'requirement_compliance': results['scenario_result']['requirement_compliance']
                }
                scenario_scores.append(results['analysis_result'].total_score)
                
            except Exception as e:
                print(f"Error evaluating {tool_name} - {scenario}: {e}")
                tool_results['scenario_results'][scenario] = {'error': str(e)}
        
        # Calculate summary metrics
        if scenario_scores:
            tool_results['summary_metrics'] = {
                'average_score': statistics.mean(scenario_scores),
                'median_score': statistics.median(scenario_scores),
                'min_score': min(scenario_scores),
                'max_score': max(scenario_scores),
                'score_std_dev': statistics.stdev(scenario_scores) if len(scenario_scores) > 1 else 0,
                'scenarios_completed': len(scenario_scores),
                'total_scenarios': len(self.scenarios)
            }
        
        # Save individual tool results
        output_file = Path(output_directory) / f"{tool_name}_results.json"
        with open(output_file, 'w') as f:
            json.dump(tool_results, f, indent=2)
        
        return tool_results
    
    def compare_tools(self, tools_results: List[Dict[str, Any]], output_directory: str) -> Dict[str, Any]:
        """Generate comparative analysis between multiple AI tools"""
        
        comparison = {
            'comparison_timestamp': datetime.now().isoformat(),
            'tools_evaluated': [tool['tool_name'] for tool in tools_results],
            'scenario_comparison': {},
            'overall_ranking': [],
            'detailed_analysis': {}
        }
        
        # Compare performance across scenarios
        for scenario in self.scenarios:
            scenario_data = {}
            scenario_scores = []
            
            for tool_result in tools_results:
                if scenario in tool_result['scenario_results']:
                    scenario_result = tool_result['scenario_results'][scenario]
                    if 'error' not in scenario_result:
                        scenario_data[tool_result['tool_name']] = scenario_result
                        scenario_scores.append((tool_result['tool_name'], scenario_result['total_score']))
            
            # Sort by score for this scenario
            scenario_scores.sort(key=lambda x: x[1], reverse=True)
            scenario_data['ranking'] = scenario_scores
            comparison['scenario_comparison'][scenario] = scenario_data
        
        # Overall ranking based on average scores
        overall_scores = []
        for tool_result in tools_results:
            if 'average_score' in tool_result['summary_metrics']:
                overall_scores.append((
                    tool_result['tool_name'],
                    tool_result['summary_metrics']['average_score'],
                    tool_result['summary_metrics']
                ))
        
        overall_scores.sort(key=lambda x: x[1], reverse=True)
        comparison['overall_ranking'] = overall_scores
        
        # Detailed analysis
        comparison['detailed_analysis'] = self._generate_detailed_analysis(tools_results)
        
        # Save comparison results
        output_file = Path(output_directory) / "comparison_results.json"
        with open(output_file, 'w') as f:
            json.dump(comparison, f, indent=2)
        
        return comparison
    
    def _generate_detailed_analysis(self, tools_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate detailed statistical analysis"""
        
        analysis = {
            'module_usage_analysis': {},
            'performance_by_category': {},
            'consistency_analysis': {},
            'strengths_weaknesses': {}
        }
        
        # Analyze module usage patterns
        all_modules_used = set()
        module_usage_by_tool = {}
        
        for tool_result in tools_results:
            tool_name = tool_result['tool_name']
            module_usage_by_tool[tool_name] = set()
            
            for scenario, scenario_result in tool_result['scenario_results'].items():
                if 'modules_used' in scenario_result:
                    modules = scenario_result['modules_used']
                    all_modules_used.update(modules)
                    module_usage_by_tool[tool_name].update(modules)
        
        # Calculate module usage statistics
        for module in all_modules_used:
            usage_count = sum(1 for tool_modules in module_usage_by_tool.values() if module in tool_modules)
            analysis['module_usage_analysis'][module] = {
                'usage_frequency': usage_count / len(tools_results),
                'used_by_tools': [tool for tool, modules in module_usage_by_tool.items() if module in modules]
            }
        
        # Performance by category analysis
        categories = ['module_usage_score', 'function_correctness_score', 'architecture_score', 'error_handling_score']
        
        for category in categories:
            category_scores = {}
            for tool_result in tools_results:
                tool_name = tool_result['tool_name']
                scores = []
                for scenario_result in tool_result['scenario_results'].values():
                    if category in scenario_result:
                        scores.append(scenario_result[category])
                
                if scores:
                    category_scores[tool_name] = {
                        'average': statistics.mean(scores),
                        'min': min(scores),
                        'max': max(scores),
                        'std_dev': statistics.stdev(scores) if len(scores) > 1 else 0
                    }
            
            analysis['performance_by_category'][category] = category_scores
        
        # Consistency analysis (standard deviation of scores)
        for tool_result in tools_results:
            tool_name = tool_result['tool_name']
            if 'score_std_dev' in tool_result['summary_metrics']:
                analysis['consistency_analysis'][tool_name] = {
                    'score_std_dev': tool_result['summary_metrics']['score_std_dev'],
                    'consistency_rating': self._rate_consistency(tool_result['summary_metrics']['score_std_dev'])
                }
        
        return analysis
    
    def _rate_consistency(self, std_dev: float) -> str:
        """Rate consistency based on standard deviation"""
        if std_dev < 1.0:
            return "Very Consistent"
        elif std_dev < 2.0:
            return "Consistent"
        elif std_dev < 3.0:
            return "Moderately Consistent"
        else:
            return "Inconsistent"
    
    def generate_report(self, comparison_results: Dict[str, Any], output_file: str):
        """Generate human-readable comparison report"""
        
        report = f"""
# AI Tool Evaluation Comparison Report

Generated: {comparison_results['comparison_timestamp']}

## Executive Summary

This report compares the performance of {len(comparison_results['tools_evaluated'])} AI programming tools across {len(self.scenarios)} embedded systems programming scenarios.

### Tools Evaluated:
{chr(10).join(f"- {tool}" for tool in comparison_results['tools_evaluated'])}

## Overall Rankings

"""
        
        for i, (tool_name, avg_score, metrics) in enumerate(comparison_results['overall_ranking'], 1):
            report += f"**{i}. {tool_name}**\n"
            report += f"   - Average Score: {avg_score:.1f}/10.0\n"
            report += f"   - Scenarios Completed: {metrics['scenarios_completed']}/{metrics['total_scenarios']}\n"
            report += f"   - Score Range: {metrics['min_score']:.1f} - {metrics['max_score']:.1f}\n"
            report += f"   - Consistency: {metrics['score_std_dev']:.1f} (std dev)\n\n"
        
        report += "## Scenario-by-Scenario Analysis\n\n"
        
        for scenario, scenario_data in comparison_results['scenario_comparison'].items():
            report += f"### {scenario.replace('_', ' ').title()}\n\n"
            if 'ranking' in scenario_data:
                for i, (tool_name, score) in enumerate(scenario_data['ranking'], 1):
                    report += f"{i}. **{tool_name}**: {score:.1f}/10.0\n"
            report += "\n"
        
        # Module usage analysis
        if 'module_usage_analysis' in comparison_results['detailed_analysis']:
            report += "## Module Usage Analysis\n\n"
            report += "### Most Commonly Used Internal Modules:\n\n"
            
            module_usage = comparison_results['detailed_analysis']['module_usage_analysis']
            sorted_modules = sorted(module_usage.items(), key=lambda x: x[1]['usage_frequency'], reverse=True)
            
            for module, data in sorted_modules[:10]:
                report += f"- **{module}**: Used by {data['usage_frequency']:.1%} of tools\n"
            
            report += "\n"
        
        # Performance by category
        if 'performance_by_category' in comparison_results['detailed_analysis']:
            report += "## Performance by Category\n\n"
            
            categories = {
                'module_usage_score': 'Module Usage',
                'function_correctness_score': 'Function Correctness',
                'architecture_score': 'Architecture Quality',
                'error_handling_score': 'Error Handling'
            }
            
            for category_key, category_name in categories.items():
                if category_key in comparison_results['detailed_analysis']['performance_by_category']:
                    report += f"### {category_name}\n\n"
                    category_data = comparison_results['detailed_analysis']['performance_by_category'][category_key]
                    sorted_tools = sorted(category_data.items(), key=lambda x: x[1]['average'], reverse=True)
                    
                    for tool_name, scores in sorted_tools:
                        report += f"- **{tool_name}**: {scores['average']:.1f} (±{scores['std_dev']:.1f})\n"
                    report += "\n"
        
        # Consistency analysis
        if 'consistency_analysis' in comparison_results['detailed_analysis']:
            report += "## Consistency Analysis\n\n"
            consistency_data = comparison_results['detailed_analysis']['consistency_analysis']
            sorted_consistency = sorted(consistency_data.items(), key=lambda x: x[1]['score_std_dev'])
            
            for tool_name, data in sorted_consistency:
                report += f"- **{tool_name}**: {data['consistency_rating']} (σ = {data['score_std_dev']:.1f})\n"
            report += "\n"
        
        report += """
## Recommendations

### For AI Tool Selection:
- Choose tools with high overall scores for general embedded systems programming
- Consider consistency ratings for production use cases
- Evaluate specific category performance based on your primary use cases

### For AI Tool Improvement:
- Focus on increasing internal module usage rates
- Improve error handling implementations
- Enhance code architecture quality for complex scenarios

---
*This report was generated using the Internal Module Evaluation Framework*
"""
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        return report

def main():
    """Command line interface for batch evaluation"""
    parser = argparse.ArgumentParser(description='Batch evaluate multiple AI tools across all scenarios')
    parser.add_argument('tools_directory', help='Directory containing subdirectories for each AI tool')
    parser.add_argument('--output', '-o', default='evaluation_results', help='Output directory for results')
    parser.add_argument('--report', '-r', help='Output file for comparison report')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    evaluator = BatchEvaluator()
    tools_results = []
    
    # Find all tool directories
    tools_dir = Path(args.tools_directory)
    for tool_dir in tools_dir.iterdir():
        if tool_dir.is_dir():
            tool_name = tool_dir.name
            print(f"Evaluating {tool_name}...")
            
            try:
                tool_result = evaluator.evaluate_tool(tool_name, str(tool_dir), args.output)
                tools_results.append(tool_result)
                print(f"  Average score: {tool_result['summary_metrics'].get('average_score', 'N/A'):.1f}")
            except Exception as e:
                print(f"  Error: {e}")
    
    if len(tools_results) > 1:
        # Generate comparison
        print("\nGenerating comparison analysis...")
        comparison_results = evaluator.compare_tools(tools_results, args.output)
        
        # Generate report
        report_file = args.report or os.path.join(args.output, "comparison_report.md")
        evaluator.generate_report(comparison_results, report_file)
        print(f"Comparison report saved to: {report_file}")
        
        # Print summary
        print("\n" + "="*50)
        print("EVALUATION SUMMARY")
        print("="*50)
        for i, (tool_name, avg_score, _) in enumerate(comparison_results['overall_ranking'], 1):
            print(f"{i}. {tool_name}: {avg_score:.1f}/10.0")
    
    else:
        print("Need at least 2 tools to generate comparison analysis")

if __name__ == "__main__":
    main()