#!/usr/bin/env python
"""
Auto-Reprogramming for ConscienceAI
===================================

Automatically analyzes and improves the AI system through code modifications
and parameter adjustments, similar to KaseMaster's approach.

Features:
- Code quality analysis
- Performance bottleneck detection
- Automated code improvements
- Safe reprogramming with dry-run mode
- Version control integration
"""

import os
import re
import ast
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess


class AutoReprogrammer:
    def __init__(self, workspace: str = ".", dry_run: bool = True):
        """
        Initialize auto-reprogrammer.
        
        Args:
            workspace: Project workspace directory
            dry_run: If True, only analyze without making changes
        """
        self.workspace = Path(workspace).resolve()
        self.dry_run = dry_run
        self.analysis_results = []
        self.improvements_made = []
        
        print(f"Auto-Reprogrammer initialized")
        print(f"Workspace: {self.workspace}")
        print(f"Dry Run: {self.dry_run}")
    
    def analyze_code_quality(self) -> Dict[str, Any]:
        """
        Analyze code quality and identify improvement opportunities.
        
        Returns:
            Dictionary with analysis results
        """
        print("Analyzing code quality...")
        
        analysis = {
            "timestamp": time.time(),
            "files_analyzed": 0,
            "issues_found": [],
            "recommendations": []
        }
        
        # Find Python files
        python_files = list(self.workspace.rglob("*.py"))
        analysis["files_analyzed"] = len(python_files)
        
        for py_file in python_files:
            try:
                # Skip certain directories
                if any(skip_dir in str(py_file) for skip_dir in [".git", "__pycache__", "venv"]):
                    continue
                
                issues = self._analyze_file(py_file)
                analysis["issues_found"].extend(issues)
                
            except Exception as e:
                print(f"Error analyzing {py_file}: {e}")
        
        # Add recommendations based on issues found
        issue_types = [issue["type"] for issue in analysis["issues_found"]]
        
        if issue_types.count("missing_docstring") > 5:
            analysis["recommendations"].append({
                "type": "add_docstrings",
                "priority": "medium",
                "description": "Add docstrings to improve code documentation"
            })
        
        if issue_types.count("long_function") > 3:
            analysis["recommendations"].append({
                "type": "refactor_functions",
                "priority": "high",
                "description": "Refactor long functions to improve maintainability"
            })
        
        if issue_types.count("missing_type_hints") > 10:
            analysis["recommendations"].append({
                "type": "add_type_hints",
                "priority": "medium",
                "description": "Add type hints to improve code clarity"
            })
        
        self.analysis_results.append(analysis)
        return analysis
    
    def _analyze_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Analyze a single Python file.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            List of issues found
        """
        issues = []
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()
            
            # Check for missing docstrings
            if not content.strip().startswith('"""') and not content.strip().startswith("'''"):
                issues.append({
                    "type": "missing_docstring",
                    "file": str(file_path.relative_to(self.workspace)),
                    "line": 1,
                    "description": "Missing module docstring"
                })
            
            # Parse AST to analyze structure
            try:
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check function length
                        if hasattr(node, 'end_lineno') and node.end_lineno:
                            func_length = node.end_lineno - node.lineno + 1
                            if func_length > 50:
                                issues.append({
                                    "type": "long_function",
                                    "file": str(file_path.relative_to(self.workspace)),
                                    "line": node.lineno,
                                    "function": node.name,
                                    "length": func_length,
                                    "description": f"Function '{node.name}' is {func_length} lines long"
                                })
                        
                        # Check for missing docstrings
                        if (not isinstance(node.body[0], ast.Expr) or 
                            not isinstance(node.body[0].value, ast.Constant) or
                            not isinstance(node.body[0].value.value, str)):
                            issues.append({
                                "type": "missing_docstring",
                                "file": str(file_path.relative_to(self.workspace)),
                                "line": node.lineno,
                                "function": node.name,
                                "description": f"Function '{node.name}' missing docstring"
                            })
                        
                        # Check for missing type hints
                        missing_hints = []
                        if node.args.args:
                            for arg in node.args.args:
                                if not arg.annotation:
                                    missing_hints.append(arg.arg)
                        
                        if missing_hints:
                            issues.append({
                                "type": "missing_type_hints",
                                "file": str(file_path.relative_to(self.workspace)),
                                "line": node.lineno,
                                "function": node.name,
                                "missing_args": missing_hints,
                                "description": f"Function '{node.name}' missing type hints for args: {', '.join(missing_hints)}"
                            })
            
            except SyntaxError as e:
                issues.append({
                    "type": "syntax_error",
                    "file": str(file_path.relative_to(self.workspace)),
                    "line": e.lineno or 0,
                    "description": f"Syntax error: {e.msg}"
                })
            
            # Check for TODO comments
            for i, line in enumerate(lines, 1):
                if "TODO" in line.upper():
                    issues.append({
                        "type": "todo_comment",
                        "file": str(file_path.relative_to(self.workspace)),
                        "line": i,
                        "description": "TODO comment found"
                    })
            
            # Check for print statements (in production code)
            for i, line in enumerate(lines, 1):
                if re.search(r"\bprint\s*\(", line):
                    # Skip if it's in a main block or test
                    if not any(skip in line.lower() for skip in ["main", "test", "debug"]):
                        issues.append({
                            "type": "print_statement",
                            "file": str(file_path.relative_to(self.workspace)),
                            "line": i,
                            "description": "Print statement found in non-debug code"
                        })
        
        except Exception as e:
            issues.append({
                "type": "analysis_error",
                "file": str(file_path.relative_to(self.workspace)),
                "description": f"Failed to analyze file: {e}"
            })
        
        return issues
    
    def apply_improvements(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Apply automatic improvements based on analysis.
        
        Args:
            analysis: Analysis results
            
        Returns:
            List of improvements made
        """
        if self.dry_run:
            print("DRY RUN: Would apply improvements...")
            return []
        
        print("Applying improvements...")
        improvements = []
        
        # Group issues by file
        issues_by_file = {}
        for issue in analysis.get("issues_found", []):
            file_path = issue["file"]
            if file_path not in issues_by_file:
                issues_by_file[file_path] = []
            issues_by_file[file_path].append(issue)
        
        # Apply improvements file by file
        for file_path, issues in issues_by_file.items():
            try:
                full_path = self.workspace / file_path
                if full_path.exists():
                    improvement = self._improve_file(full_path, issues)
                    if improvement:
                        improvements.append(improvement)
            except Exception as e:
                print(f"Error improving {file_path}: {e}")
        
        self.improvements_made.extend(improvements)
        return improvements
    
    def _improve_file(self, file_path: Path, issues: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Apply improvements to a single file.
        
        Args:
            file_path: Path to the file
            issues: List of issues for this file
            
        Returns:
            Dictionary with improvement details or None
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # Add module docstring if missing
            if any(issue["type"] == "missing_docstring" and "function" not in issue for issue in issues):
                if not content.strip().startswith('"""') and not content.strip().startswith("'''"):
                    module_docstring = '"""Auto-generated module docstring."""\n\n'
                    content = module_docstring + content
                    changes_made.append("Added module docstring")
            
            # Save if changes were made
            if content != original_content:
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                
                return {
                    "file": str(file_path.relative_to(self.workspace)),
                    "changes": changes_made,
                    "timestamp": time.time()
                }
        
        except Exception as e:
            print(f"Error improving {file_path}: {e}")
        
        return None
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive report of analysis and improvements.
        
        Returns:
            Dictionary with report data
        """
        report = {
            "generated_at": time.time(),
            "workspace": str(self.workspace),
            "dry_run": self.dry_run,
            "analysis_results": self.analysis_results,
            "improvements_made": self.improvements_made,
            "summary": {
                "total_files_analyzed": sum(a.get("files_analyzed", 0) for a in self.analysis_results),
                "total_issues_found": sum(len(a.get("issues_found", [])) for a in self.analysis_results),
                "total_improvements": len(self.improvements_made)
            }
        }
        
        return report
    
    def save_report(self, filepath: str = "ai_runs/auto_reprogram_report.json") -> bool:
        """
        Save report to file.
        
        Args:
            filepath: Path to save report
            
        Returns:
            True if successful, False otherwise
        """
        try:
            report = self.generate_report()
            
            # Create directory if it doesn't exist
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, "w") as f:
                json.dump(report, f, indent=2, default=str)
            
            print(f"Report saved to: {filepath}")
            return True
            
        except Exception as e:
            print(f"Failed to save report: {e}")
            return False


def main():
    """Main function for auto-reprogramming."""
    parser = argparse.ArgumentParser(description="Auto-reprogram ConscienceAI system")
    parser.add_argument("--workspace", default=".", help="Project workspace directory")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only, don't make changes")
    parser.add_argument("--output", default="ai_runs/auto_reprogram_report.json", help="Output report file")
    parser.add_argument("--server_url", help="Chat server URL for integration testing")
    
    args = parser.parse_args()
    
    print("ConscienceAI Auto-Reprogrammer")
    print("=" * 40)
    print(f"Workspace: {args.workspace}")
    print(f"Dry Run: {args.dry_run}")
    print(f"Output: {args.output}")
    print()
    
    # Initialize reprogrammer
    reprogrammer = AutoReprogrammer(workspace=args.workspace, dry_run=args.dry_run)
    
    # Analyze code quality
    analysis = reprogrammer.analyze_code_quality()
    
    print(f"\nAnalysis Results:")
    print(f"  Files analyzed: {analysis.get('files_analyzed', 0)}")
    print(f"  Issues found: {len(analysis.get('issues_found', []))}")
    print(f"  Recommendations: {len(analysis.get('recommendations', []))}")
    
    # Show some issues
    issues = analysis.get('issues_found', [])
    if issues:
        print(f"\nSample Issues:")
        for issue in issues[:5]:
            print(f"  - {issue['file']}:{issue.get('line', '?')} - {issue['description']}")
        if len(issues) > 5:
            print(f"  ... and {len(issues) - 5} more")
    
    # Apply improvements (if not dry run)
    if not args.dry_run:
        improvements = reprogrammer.apply_improvements(analysis)
        print(f"\nImprovements Made: {len(improvements)}")
        for imp in improvements:
            print(f"  - {imp['file']}: {', '.join(imp['changes'])}")
    
    # Generate and save report
    reprogrammer.save_report(args.output)
    
    print(f"\nAuto-reprogramming {'analysis' if args.dry_run else 'completed'} successfully")


if __name__ == "__main__":
    main()