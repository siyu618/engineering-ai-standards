#!/usr/bin/env python3
"""
Evaluation Runner — validates evaluation case definitions and reports results.

Usage:
    python evaluations/runner/run.py              # Validate all cases
    python evaluations/runner/run.py --case NAME  # Validate a single case
    python evaluations/runner/run.py --verbose     # Detailed output
    python evaluations/runner/run.py --registry    # Also validate registry consistency
"""

import argparse
import glob
import os
import sys
import yaml


REQUIRED_FIELDS = ["id", "skill", "category", "version", "task", "expected", "scoring"]
SCORING_DIMENSIONS = ["correctness", "completeness", "architecture", "maintainability"]
CASES_DIR = os.path.join(os.path.dirname(__file__), "..", "cases")
REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "registry", "skills.yaml")


def load_cases(case_filter: str | None = None) -> list[dict]:
    """Load all evaluation YAML files from the cases directory."""
    pattern = os.path.join(CASES_DIR, "**/*.yaml")
    files = sorted(glob.glob(pattern, recursive=True))

    if not files:
        print(f"ERROR: No YAML files found in {CASES_DIR}")
        sys.exit(1)

    cases = []
    for f in files:
        if case_filter and case_filter not in f:
            continue
        with open(f) as fh:
            try:
                data = yaml.safe_load(fh)
                data["_file"] = os.path.relpath(f)
                cases.append(data)
            except yaml.YAMLError as e:
                print(f"❌ PARSE ERROR: {f}: {e}")
                sys.exit(1)
    return cases


def load_registry() -> dict:
    """Load the skill registry. Returns empty dict if registry doesn't exist."""
    if not os.path.exists(REGISTRY_PATH):
        return {}
    with open(REGISTRY_PATH) as f:
        data = yaml.safe_load(f)
    return data.get("skills", {})


def validate_case(case: dict) -> list[str]:
    """Validate a single evaluation case. Returns list of error messages."""
    errors = []
    file_path = case.get("_file", "unknown")

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in case:
            errors.append(f"{file_path}: missing required field '{field}'")

    if errors:
        return errors

    # Validate scoring
    scoring = case.get("scoring", {})
    total_weight = 0
    for dim in SCORING_DIMENSIONS:
        if dim not in scoring:
            errors.append(f"{file_path}: missing scoring dimension '{dim}'")
            continue
        dim_data = scoring[dim]
        if not isinstance(dim_data, dict):
            errors.append(f"{file_path}: scoring.{dim} must be a dict")
            continue
        weight = dim_data.get("weight", 0)
        if not isinstance(weight, int) or weight < 0 or weight > 100:
            errors.append(f"{file_path}: scoring.{dim}.weight must be an integer 0-100")
        total_weight += weight

        if "criteria" not in dim_data:
            errors.append(f"{file_path}: scoring.{dim} missing 'criteria'")
        elif not isinstance(dim_data["criteria"], list):
            errors.append(f"{file_path}: scoring.{dim}.criteria must be a list")

    if abs(total_weight - 100) > 1:
        errors.append(f"{file_path}: scoring weights sum to {total_weight}, expected 100")

    # Validate expected.must_include
    expected = case.get("expected", {})
    if "must_include" not in expected:
        errors.append(f"{file_path}: expected.must_include is required")
    elif not isinstance(expected["must_include"], list) or len(expected["must_include"]) == 0:
        errors.append(f"{file_path}: expected.must_include must be a non-empty list")

    # Validate category
    valid_categories = {"system-design", "coding", "testing"}
    if case.get("category") not in valid_categories:
        errors.append(f"{file_path}: category must be one of {valid_categories}")

    return errors


def validate_registry_consistency(registry: dict, cases: list[dict]) -> list[str]:
    """Check that registry skills match evaluation cases."""
    warnings = []
    registry_skills = set(registry.keys())
    case_skills = set(c.get("skill", "?") for c in cases)

    for s in case_skills:
        if s not in registry_skills:
            skills_dir = os.path.join(os.path.dirname(__file__), "..", "..", "skills", s)
            if os.path.isdir(skills_dir):
                warnings.append(f"⚠️  Skill '{s}' has eval cases but is not listed in registry/skills.yaml")
            else:
                warnings.append(f"❌ Skill '{s}' referenced in eval cases but not found in skills/ or registry")

    for s in registry_skills:
        reg = registry[s]
        ev = reg.get("evaluation", {})
        if ev.get("enabled", False):
            registered_cases = set(ev.get("cases", []))
            existing_case_ids = set(c.get("id", "") for c in cases)
            missing = registered_cases - existing_case_ids
            if missing:
                warnings.append(f"⚠️  Registry skill '{s}' references missing eval cases: {missing}")

    return warnings


def main():
    parser = argparse.ArgumentParser(description="Validate evaluation case definitions.")
    parser.add_argument("--case", help="Only validate cases containing this string in path")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("--registry", action="store_true", help="Also validate registry consistency")
    args = parser.parse_args()

    cases = load_cases(args.case)

    total_errors = 0
    total_warnings = 0

    print(f"📋 Found {len(cases)} evaluation case(s)")
    print()

    for case in cases:
        name = case.get("id", case.get("_file", "unknown"))
        errors = validate_case(case)

        if errors:
            total_errors += len(errors)
            print(f"❌ {name}")
            for err in errors:
                print(f"   • {err}")
        else:
            skill = case.get("skill", "?")
            print(f"✅ {name} (skill: {skill})")

            if args.verbose:
                scoring = case.get("scoring", {})
                weights = {d: scoring[d]["weight"] for d in SCORING_DIMENSIONS if d in scoring}
                print(f"   Weights: {weights}")
                must_count = len(case.get("expected", {}).get("must_include", []))
                forbid_count = len(case.get("expected", {}).get("forbidden", []))
                print(f"   Expected: {must_count} must-include, {forbid_count} forbidden")

    # Registry consistency check
    if args.registry:
        registry = load_registry()
        if registry:
            warnings = validate_registry_consistency(registry, cases)
            if warnings:
                print()
                print("📋 Registry consistency:")
                for w in warnings:
                    if w.startswith("❌"):
                        total_errors += 1
                    else:
                        total_warnings += 1
                    print(f"   {w}")

    print()
    print("=" * 50)

    if total_errors:
        print(f"❌ {total_errors} validation error(s), {total_warnings} warning(s) found")
        sys.exit(1)
    else:
        print(f"✅ All {len(cases)} evaluation case(s) valid ({total_warnings} warning(s))")
        sys.exit(0)


if __name__ == "__main__":
    main()
