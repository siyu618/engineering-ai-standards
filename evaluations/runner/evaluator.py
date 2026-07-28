#!/usr/bin/env python3
"""
Evaluation Engine — executes evaluation cases against agent outputs.

Usage:
    # Rule-based evaluation (keyword matching)
    python evaluator.py --case cache-design --method rule --output agent_output.md

    # LLM-as-Judge (generates judge prompt)
    python evaluator.py --case cache-design --method llm-judge --output agent_output.md

    # Human review (interactive score entry)
    python evaluator.py --case cache-design --method manual
"""

import argparse
import glob
import json
import os
import re
import sys
from string import Template

import yaml


CASES_DIR = os.path.join(os.path.dirname(__file__), "..", "cases")
JUDGE_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "judge_prompt.md")
REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "registry", "skills.yaml")


def load_case(case_id: str) -> dict:
    """Load an evaluation case by ID from the cases directory."""
    pattern = os.path.join(CASES_DIR, "**/*.yaml")
    for f in sorted(glob.glob(pattern, recursive=True)):
        with open(f) as fh:
            data = yaml.safe_load(fh)
            if data.get("id") == case_id:
                data["_file"] = os.path.relpath(f)
                # Normalize: support both flat and nested expected format
                if "expected" in data and "must_include" not in data:
                    data["must_include"] = data["expected"].get("must_include", [])
                    data["forbidden"] = data["expected"].get("forbidden", [])
                return data
    print(f"❌ Case '{case_id}' not found")
    sys.exit(1)


def load_output(path: str) -> str:
    """Load agent output from a file."""
    with open(path) as f:
        return f.read()


def score_rule_based(case: dict, output: str) -> dict:
    """Rule-based evaluation: check must_include keywords against output."""
    must_include = case.get("must_include", [])
    forbidden = case.get("forbidden", [])
    scoring = case.get("scoring", {})

    if not must_include:
        print("⚠️  No must_include items defined for this case")
        return {"score": 0, "details": "no criteria"}

    output_lower = output.lower()

    def normalize_item(item):
        """Convert must_include item to string, handling dict values."""
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return " ".join(f"{k} {v}" for k, v in item.items())
        return str(item)

    def extract_weight(dim):
        """Extract weight from scoring dimension, handling both formats."""
        val = scoring.get(dim, 0)
        if isinstance(val, dict):
            return val.get("weight", 0)
        return val if isinstance(val, (int, float)) else 0

    found = []
    missing = []
    partial = []

    for item in must_include:
        normalized = normalize_item(item)
        search_text = normalized.lower()
        if search_text in output_lower:
            found.append(normalized)
        else:
            # Check for partial match: extract key nouns/verbs
            words = [w for w in search_text.split() if len(w) > 4]
            matches = sum(1 for w in words if w in output_lower)
            if words and matches / len(words) >= 0.4:
                partial.append(normalized)
            else:
                missing.append(normalized)

    # Score: full matches count fully, partials count half
    total_items = len(must_include) or 1
    effective_matches = len(found) + (len(partial) * 0.5)
    hit_rate = effective_matches / total_items

    # Calculate dimension scores (using effective hit_rate from above)
    dimension_scores = {}
    for dim in scoring:
        w = extract_weight(dim)
        if not w:
            continue
        dimension_scores[dim] = round(hit_rate * 100)

    # Overall score: weighted average
    total_weight = sum(extract_weight(d) for d in scoring) or 100
    weighted = sum(dimension_scores.get(d, 0) * extract_weight(d) for d in scoring)
    overall = round(weighted / total_weight) if total_weight > 0 else 0

    # Check forbidden items
    violations = [item for item in forbidden if item.lower() in output_lower]

    return {
        "score": overall,
        "dimensions": dimension_scores,
        "details": {
            "method": "rule-based",
            "must_include_found": len(found),
            "must_include_partial": len(partial),
            "must_include_total": len(must_include),
            "missing": missing,
            "partial": partial,
            "violations": violations,
            "hit_rate": round(hit_rate, 2),
        },
    }


def render_judge_prompt(case: dict, output: str) -> str:
    """Render the judge prompt template with case data and agent output."""
    if not os.path.exists(JUDGE_PROMPT_PATH):
        print(f"❌ Judge prompt template not found at {JUDGE_PROMPT_PATH}")
        sys.exit(1)

    with open(JUDGE_PROMPT_PATH) as f:
        template_str = f.read()

    scoring = case.get("scoring", {})

    def extract_weight(dim):
        val = scoring.get(dim, 0)
        if isinstance(val, dict):
            return val.get("weight", 0)
        return val if isinstance(val, (int, float)) else 0

    total_weight = sum(extract_weight(d) for d in ["correctness", "completeness", "architecture", "maintainability"]) or 100

    context_str = "\n".join(f"- {c}" for c in case.get("context", []))
    must_include_str = "\n".join(f"- {m}" for m in case.get("must_include", []))
    forbidden_str = "\n".join(f"- {f}" for f in case.get("forbidden", []))

    replacements = {
        "skill": case.get("skill", "unknown"),
        "task": case.get("task", ""),
        "context": context_str,
        "must_include": must_include_str,
        "forbidden": forbidden_str,
        "output": output,
        "correctness_weight": str(scoring.get("correctness", 25)),
        "completeness_weight": str(scoring.get("completeness", 25)),
        "architecture_weight": str(scoring.get("architecture", 25)),
        "maintainability_weight": str(scoring.get("maintainability", 25)),
    }

    for key, value in replacements.items():
        template_str = template_str.replace("{{" + key + "}}", value)

    return template_str


def score_llm_judge(case: dict, output: str) -> dict:
    """LLM-as-Judge evaluation: render the judge prompt for external use."""
    prompt = render_judge_prompt(case, output)

    return {
        "score": None,  # To be filled by LLM call
        "dimensions": {},
        "details": {
            "method": "llm-judge",
            "prompt": prompt,
            "note": "Execute this prompt against an LLM to obtain scores",
        },
    }


def score_manual(case: dict) -> dict:
    """Human review: interactive score entry."""
    scoring = case.get("scoring", {})
    print(f"\n📋 Manual review for case: {case.get('id', 'unknown')}")
    print(f"   Task: {case.get('task', '')[:80]}...")
    print()

    dimension_scores = {}
    for dim, weight in scoring.items():
        while True:
            try:
                val = int(input(f"  {dim} (weight {weight}%, 0-100): "))
                if 0 <= val <= 100:
                    dimension_scores[dim] = val
                    break
                print("    Must be 0-100")
            except ValueError:
                print("    Must be an integer")

    total_weight = sum(scoring.values()) or 100
    weighted = sum(dimension_scores.get(d, 0) * w for d, w in scoring.items())
    overall = round(weighted / total_weight)

    print(f"\n  Overall score: {overall}/100")
    return {
        "score": overall,
        "dimensions": dimension_scores,
        "details": {"method": "manual-review"},
    }


def main():
    parser = argparse.ArgumentParser(description="Execute evaluation cases against agent outputs.")
    parser.add_argument("--case", required=True, help="Evaluation case ID to run")
    parser.add_argument("--method", choices=["rule", "llm-judge", "manual"], default="rule",
                        help="Evaluation method")
    parser.add_argument("--output", help="Path to agent output file (required for rule and llm-judge)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    case = load_case(args.case)

    if args.method in ("rule", "llm-judge"):
        if not args.output:
            print("❌ --output is required for rule and llm-judge methods")
            sys.exit(1)
        output = load_output(args.output)

    if args.method == "rule":
        result = score_rule_based(case, output)
    elif args.method == "llm-judge":
        result = score_llm_judge(case, output)
    else:
        result = score_manual(case)

    result["case_id"] = case.get("id")
    result["skill"] = case.get("skill")
    result["method"] = args.method

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        score = result.get("score", "N/A")
        print(f"\n{'='*50}")
        print(f"Case:     {result['case_id']}")
        print(f"Skill:    {result['skill']}")
        print(f"Method:   {result['method']}")
        print(f"Score:    {score}/100")
        if result.get("dimensions"):
            print(f"Dims:     {result['dimensions']}")
        details = result.get("details", {})
        if isinstance(details, dict):
            if details.get("missing"):
                print(f"Missing:  {details['missing']}")
            if details.get("partial"):
                print(f"Partial:  {details['partial']}")
            if details.get("violations"):
                print(f"⚠️  Violations: {details['violations']}")
        print(f"{'='*50}")

    return result


if __name__ == "__main__":
    main()
