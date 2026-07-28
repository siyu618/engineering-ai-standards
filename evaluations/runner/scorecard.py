#!/usr/bin/env python3
"""
Scorecard — tracks evaluation scores, detects regression, and enforces thresholds.

Usage:
    python scorecard.py --compare          # Compare scores against thresholds
    python scorecard.py --update cache-design:91  # Record a score
    python scorecard.py --report           # Show latest scores for all skills
"""

import argparse
import json
import os
import sys
from datetime import date

import yaml


REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "registry", "skills.yaml")


def load_registry() -> dict:
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def save_registry(data: dict):
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def compare_scores(registry: dict) -> list[dict]:
    """Compare latest scores against thresholds for all skills."""
    results = []
    skills = registry.get("skills", {})
    for name, skill in skills.items():
        ev = skill.get("evaluation", {})
        if not ev.get("enabled", False):
            continue
        threshold = ev.get("threshold", 0)
        latest = ev.get("latest_score")
        last_run = ev.get("last_run", "never")

        result = {
            "skill": name,
            "version": skill.get("version", "?"),
            "threshold": threshold,
            "latest_score": latest,
            "last_run": last_run,
            "status": "pending",
        }

        if latest is None:
            result["status"] = "not_evaluated"
        elif latest >= threshold:
            result["status"] = "passed"
        else:
            result["status"] = "regression"

        results.append(result)

    return results


def update_score(registry: dict, case_id: str, score: int):
    """Update the score for a skill by looking up which skill owns the case."""
    skills = registry.get("skills", {})
    found = False
    for name, skill in skills.items():
        ev = skill.get("evaluation", {})
        cases = ev.get("cases", [])
        if case_id in cases:
            ev["latest_score"] = score
            ev["last_run"] = str(date.today())
            found = True
            print(f"✅ Updated {name}: score={score}, date={ev['last_run']}")
            break

    if not found:
        print(f"⚠️  No skill found for case '{case_id}'")

    save_registry(registry)


def main():
    parser = argparse.ArgumentParser(description="Evaluation scorecard and regression detection.")
    parser.add_argument("--compare", action="store_true", help="Compare scores against thresholds")
    parser.add_argument("--update", help="Update score: format case_id:score (e.g., cache-design:91)")
    parser.add_argument("--report", action="store_true", help="Show score report")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    registry = load_registry()

    if args.update:
        case_id, score_str = args.update.split(":")
        score = int(score_str)
        update_score(registry, case_id, score)
        return

    if args.compare or args.report:
        results = compare_scores(registry)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print()
            print(f"{'Skill':<25} {'Ver':<6} {'Threshold':<10} {'Score':<6} {'Status':<15} {'Last Run'}")
            print("-" * 85)
            regression_found = False
            for r in results:
                score_str = str(r["latest_score"]) if r["latest_score"] is not None else "-"
                status = r["status"]
                if status == "regression":
                    regression_found = True
                    status_display = "❌ REGRESSION"
                elif status == "passed":
                    status_display = "✅ passed"
                elif status == "not_evaluated":
                    status_display = "⏳ not run"
                else:
                    status_display = "◻️  pending"
                print(f"{r['skill']:<25} {r['version']:<6} {r['threshold']:<10} {score_str:<6} {status_display:<15} {r['last_run']}")

            print()
            if regression_found:
                print("❌ Regression detected — some scores below threshold")
                sys.exit(1)
            else:
                print("✅ All evaluated skills meet or exceed thresholds")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
