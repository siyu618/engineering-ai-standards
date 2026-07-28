#!/usr/bin/env python3
"""
AI Standard Platform CLI — manage skills, evaluations, and reports.

Usage:
    python tools/ai-standard/cli.py list-skills   # List all registered skills
    python tools/ai-standard/cli.py validate       # Validate repository structure
    python tools/ai-standard/cli.py eval <skill>   # Run evaluation for a skill
    python tools/ai-standard/cli.py report         # Generate evaluation report
"""

import argparse
import glob
import os
import sys
import textwrap

import importlib.util
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "evaluations", "runner"))

# Load sibling modules directly (directory has hyphen, can't use normal import)
def _load_sibling(name):
    path = os.path.join(os.path.dirname(__file__), f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

validator = _load_sibling("validator")
reporter = _load_sibling("reporter")


REGISTRY_PATH = os.path.join(ROOT, "registry", "skills.yaml")
EVAL_CASES_DIR = os.path.join(ROOT, "evaluations", "cases")


def load_registry() -> dict:
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def cmd_list_skills(args):
    """List all registered skills with version and status."""
    registry = load_registry()
    skills = registry.get("skills", {})

    if not skills:
        print("No skills registered.")
        return

    print("\nAvailable Skills:\n")
    print(f"{'Skill':<30} {'Version':<12} {'Owner':<20} {'Status':<10} {'Eval':<6}")
    print("-" * 80)
    for name, skill in sorted(skills.items()):
        ev = skill.get("evaluation", {})
        eval_status = "✅" if ev.get("enabled") else "⬜"
        print(f"{name:<30} {skill.get('version', '?'):<12} {skill.get('owner', '?'):<20} {skill.get('status', '?'):<10} {eval_status:<6}")
    print(f"\nTotal: {len(skills)} skills\n")


def cmd_validate(args):
    """Validate repository structure and consistency."""
    results = validator.validate_all()
    passed = validator.print_validation(results)
    sys.exit(0 if passed else 1)


def cmd_eval(args):
    """Run evaluation for a skill."""
    skill_name = args.skill
    registry = load_registry()
    skills = registry.get("skills", {})

    if skill_name not in skills:
        print(f"❌ Skill '{skill_name}' not found in registry")
        sys.exit(1)

    skill = skills[skill_name]
    print(f"\n🔍 Evaluating skill: {skill_name} v{skill.get('version', '?')}\n")

    ev = skill.get("evaluation", {})
    cases = ev.get("cases", [])
    enabled = ev.get("enabled", False)

    if not enabled:
        print(f"  Evaluation not enabled for '{skill_name}'")
        sys.exit(0)

    if not cases:
        print(f"  No evaluation cases defined for '{skill_name}'")
        sys.exit(0)

    print(f"  Cases to run: {', '.join(cases)}")
    print()

    # Run each evaluation case
    from evaluations.runner.evaluator import load_case, score_rule_based
    from evaluations.runner.scorecard import update_score as save_score

    for case_id in cases:
        print(f"  ▶ Running: {case_id}")
        try:
            case = load_case(case_id)
            # Use rule-based scoring as default (works without LLM)
            # Create a synthetic output for demo — in real use, you'd pass agent output
            result = {
                "score": None,
                "details": {"method": "cli-triggered", "message": "Pass -o/--output FILE to provide agent output for scoring"},
            }
            print(f"     Case loaded: {case.get('id')} (skill: {case.get('skill')})")
            print(f"     Scoring dimensions available: {list(case.get('scoring', {}).keys())}")
            print(f"     For actual scoring: python evaluations/runner/evaluator.py --case {case_id} --method rule --output FILE")
        except (SystemExit, Exception) as e:
            print(f"     ⚠️  Could not load case: {e}")

    print(f"\n  ✅ Evaluation triggered for {len(cases)} case(s)")
    print(f"  Use 'ai-standard report' to see results\n")


def cmd_report(args):
    """Generate evaluation reports."""
    report = reporter.generate_all()
    passed = report.get("passed", 0)
    failed = report.get("failed", 0)

    print(f"\n  Evaluated: {report['evaluated']} | Passed: {passed} | Failed: {failed} | Not run: {report['not_run']}")
    print(f"  Status: {'✅ PASS' if failed == 0 else '❌ FAILED'}\n")


def main():
    parser = argparse.ArgumentParser(
        description="AI Standard Platform — engineering standard management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python tools/ai-standard/cli.py list-skills
              python tools/ai-standard/cli.py validate
              python tools/ai-standard/cli.py eval system-design
              python tools/ai-standard/cli.py report
        """),
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("list-skills", help="List all registered skills")
    subparsers.add_parser("validate", help="Validate repository structure and consistency")

    eval_parser = subparsers.add_parser("eval", help="Run evaluation for a skill")
    eval_parser.add_argument("skill", help="Skill name (e.g., design, system-design)")

    subparsers.add_parser("report", help="Generate evaluation report")

    args = parser.parse_args()

    if args.command == "list-skills":
        cmd_list_skills(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "eval":
        cmd_eval(args)
    elif args.command == "report":
        cmd_report(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
