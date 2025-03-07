"""
Midas Ruleset Linter for GitHub Actions

This script validates ruleset YAML files according to the Midas ruleset specification.
It recursively checks all YAML files, validates their structure, rule content,
and ensures that corresponding code snippets exist and match the rules.
"""

import os
import re
import sys
import yaml
from typing import Dict, Any, List, Tuple


def validate_yaml_structure(yaml_content: Dict[str, Any]) -> List[str]:
    """Validate the structure of a ruleset YAML file."""
    errors = []
    required_fields = ["rule_id", "rule_type", "rule", "author", "description"]

    for field in required_fields:
        if field not in yaml_content:
            errors.append(f"Missing required field: {field}")

    if "rule_type" in yaml_content and yaml_content["rule_type"] not in ["Regex", "Query"]:
        errors.append(f"Invalid rule_type: {yaml_content['rule_type']}. Must be 'Regex' or 'Query'")

    if "rule" in yaml_content and not yaml_content["rule"]:
        errors.append("Rule content cannot be empty")

    return errors


def validate_regex_rule(rule_content: str) -> List[str]:
    """Validate a regex rule."""
    errors = []
    try:
        re.compile(rule_content)
    except re.error as e:
        errors.append(f"Invalid regex pattern: {str(e)}")

    return errors


def validate_mql_query(query: str) -> List[str]:
    """
    Validate an MQL query.
    Basic validation for now as MQL is under development.
    """
    errors = []
    if not query.strip():
        errors.append("MQL query cannot be empty")

    # Add more MQL validation as the language specification evolves

    return errors


def get_snippet_info(yaml_path: str, yaml_content: Dict[str, Any]) -> Tuple[bool, str, str]:
    """Get snippet path and language information."""
    # Extract rule name from the rule_id field
    if "rule_id" not in yaml_content:
        return False, "", ""

    rule_name = yaml_content["rule_id"]

    # Determine language from directory structure
    path_parts = yaml_path.split(os.sep)
    language_dir_idx = -1

    # Find the language directory (c, cpp, java, py, etc.)
    for i, part in enumerate(path_parts):
        if part in ["c", "cpp", "java", "py", "go", "js", "php", "ruby", "rust", "swift"]:
            language_dir_idx = i
            break

    if language_dir_idx == -1:
        return False, "", ""

    language = path_parts[language_dir_idx]

    # Map language directory to file extension
    extension_map = {
        "c": ".c",
        "cpp": ".cpp",
        "java": ".java",
        "py": ".py",
        "go": ".go",
        "js": ".js",
        "php": ".php",
        "ruby": ".rb",
        "rust": ".rs",
        "swift": ".swift"
    }

    if language not in extension_map:
        return False, "", ""

    # Construct expected snippet path
    snippet_dir = os.path.join(os.path.dirname(yaml_path), "snippets")
    snippet_file = f"{rule_name}{extension_map[language]}"
    snippet_path = os.path.join(snippet_dir, snippet_file)

    return True, snippet_path, language


def check_snippet_exists(yaml_path: str, yaml_content: Dict[str, Any]) -> List[str]:
    """Check if a corresponding snippet exists for the rule."""
    errors = []

    success, snippet_path, _ = get_snippet_info(yaml_path, yaml_content)
    if not success:
        errors.append("Could not determine snippet information from directory structure")
        return errors

    if not os.path.exists(snippet_path):
        errors.append(f"Snippet file does not exist: {snippet_path}")

    return errors


def validate_rule_against_snippet(yaml_content: Dict[str, Any], snippet_path: str) -> Tuple[bool, List[Dict], List[str]]:
    """Validate that the rule matches the snippet content."""
    if not os.path.exists(snippet_path):
        return False, [], []

    try:
        with open(snippet_path, 'r', encoding='utf-8') as file:
            snippet_content = file.read()
    except Exception as e:
        return False, [], [f"Failed to read snippet file: {str(e)}"]

    matches = []
    errors = []

    if yaml_content["rule_type"] == "Regex":
        try:
            pattern = re.compile(yaml_content["rule"])

            # Process matches with line numbers
            lines = snippet_content.split('\n')
            for line_num, line in enumerate(lines, 1):
                findings = pattern.findall(line)
                if findings:
                    for match in findings:
                        matches.append({
                            "line": line_num,
                            "content": line.strip(),
                            "match": match
                        })

            if matches:
                return True, matches[:5], errors  # Limit to first 5 matches
            else:
                errors.append("Rule does not match any content in the snippet")
                return False, matches, errors
        except Exception as e:
            errors.append(f"Error applying regex to snippet: {str(e)}")
            return False, matches, errors

    elif yaml_content["rule_type"] == "Query":
        # MQL validation is placeholder until MQL parser is available
        errors.append("MQL validation against snippets is not implemented yet")
        return False, matches, errors

    return False, matches, errors


def lint_ruleset_file(yaml_path: str) -> tuple[list[str], list[str], list[dict]]:
    """Lint a single ruleset YAML file."""
    errors = []
    warnings = []
    matches = []

    try:
        with open(yaml_path, 'r', encoding='utf-8') as file:
            yaml_content = yaml.safe_load(file)
    except yaml.YAMLError as e:
        errors.append(f"YAML parsing error: {str(e)}")
        return errors, warnings, matches
    except FileNotFoundError:
        errors.append(f"File not found: {yaml_path}")
        return errors, warnings, matches

    # Validate YAML structure
    errors.extend(validate_yaml_structure(yaml_content))

    # If there are structural errors, don't proceed with further validation
    if errors:
        return errors, warnings, matches

    # Validate rule content based on rule_type
    if yaml_content["rule_type"] == "Regex":
        errors.extend(validate_regex_rule(yaml_content["rule"]))
    elif yaml_content["rule_type"] == "Query":
        errors.extend(validate_mql_query(yaml_content["rule"]))

    # Check for corresponding snippet
    snippet_errors = check_snippet_exists(yaml_path, yaml_content)
    errors.extend(snippet_errors)

    # If snippet exists, validate rule against it
    if not snippet_errors:
        success, snippet_info, validate_snippet_path = get_snippet_info(yaml_path, yaml_content)
        if success:
            rule_matches, match_results, rule_errors = validate_rule_against_snippet(
                yaml_content, snippet_info
            )

            if rule_errors:
                errors.extend(rule_errors)
            elif not rule_matches:
                warnings.append("Rule does not match any content in the snippet file")
            else:
                matches.extend(match_results)

    return errors, warnings, matches


def find_ruleset_files(base_dir: str) -> List[str]:
    """Find all ruleset YAML files recursively."""
    ruleset_files = []

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".yaml") and "snippets" not in root:
                ruleset_files.append(os.path.join(root, file))

    return ruleset_files


def main():
    # Start from the repository root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    files_to_lint = find_ruleset_files(base_dir)

    if not files_to_lint:
        print("No ruleset files found.")
        return 0

    errors_found = False
    warnings_found = False
    error_count = 0
    warning_count = 0
    file_count = len(files_to_lint)
    passed_count = 0

    print(f"🔍 Linting {file_count} ruleset files...")

    for yaml_path in files_to_lint:
        relative_path = os.path.relpath(yaml_path, base_dir)
        errors, warnings, matches = lint_ruleset_file(yaml_path)

        if errors:
            errors_found = True
            error_count += len(errors)
            print(f"\n❌ {relative_path}:")
            for error in errors:
                print(f"  - ERROR: {error}")

            if warnings:
                for warning in warnings:
                    print(f"  - WARNING: {warning}")
                warning_count += len(warnings)
                warnings_found = True
        elif warnings:
            print(f"\n⚠️ {relative_path}:")
            for warning in warnings:
                print(f"  - WARNING: {warning}")
            warning_count += len(warnings)
            warnings_found = True
        else:
            passed_count += 1
            print(f"✅ {relative_path}")

            if matches:
                print("  📋 Rule matches in snippet:")
                for i, match in enumerate(matches, 1):
                    line_info = f"Line {match['line']}: " if 'line' in match else ""
                    match_content = match['match'] if isinstance(match, dict) and 'match' in match else match
                    line_content = match['content'] if isinstance(match, dict) and 'content' in match else ""

                    if line_info and line_content:
                        print(f"    {i}. {line_info}{line_content}")
                        print(f"       Match: {match_content}")
                    else:
                        print(f"    {i}. {match_content}")

    print("\n=== Summary ===")
    print(f"Files checked: {file_count}")
    print(f"Files passed:  {passed_count}")
    print(f"Files with errors: {file_count - passed_count}")
    print(f"Total errors: {error_count}")
    print(f"Total warnings: {warning_count}")

    if errors_found:
        print("\n❌ Linting failed with errors")
        return 1
    elif warnings_found:
        print("\n⚠️ Linting completed with warnings")
        return 0
    else:
        print("\n✅ All checks passed successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())