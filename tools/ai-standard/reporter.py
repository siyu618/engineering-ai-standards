"""
Reporter — generates evaluation reports in JSON and Markdown format.
"""

import json
import os
import sys
from datetime import date

import yaml


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REGISTRY_PATH = os.path.join(ROOT, "registry", "skills.yaml")
REPORTS_DIR = os.path.join(ROOT, "reports")


def load_registry() -> dict:
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def generate_report(registry: dict = None) -> dict:
    """Generate a report from the current registry state."""
    if registry is None:
        registry = load_registry()

    skills = registry.get("skills", {})
    evaluations = []
    regressions = []

    for name, skill in sorted(skills.items()):
        ev = skill.get("evaluation", {})
        if not ev.get("enabled", False):
            continue
        entry = {
            "skill": name,
            "version": skill.get("version", "?"),
            "threshold": ev.get("threshold", 0),
            "score": ev.get("latest_score"),
            "last_run": ev.get("last_run", "never"),
            "status": "unknown",
        }
        score = entry["score"]
        threshold = entry["threshold"]
        if score is None:
            entry["status"] = "not_run"
        elif score >= threshold:
            entry["status"] = "pass"
        else:
            entry["status"] = "regression"
            regressions.append(entry)
        evaluations.append(entry)

    report = {
        "generated": str(date.today()),
        "total_skills": len(skills),
        "evaluated": len(evaluations),
        "passed": sum(1 for e in evaluations if e["status"] == "pass"),
        "failed": sum(1 for e in evaluations if e["status"] == "regression"),
        "not_run": sum(1 for e in evaluations if e["status"] == "not_run"),
        "regressions": regressions,
        "evaluations": evaluations,
    }

    return report


def save_json_report(report: dict):
    """Save report as JSON."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = os.path.join(REPORTS_DIR, "latest.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"  📄 reports/latest.json")

    # Append to history
    history_path = os.path.join(REPORTS_DIR, "history.json")
    history = []
    if os.path.exists(history_path):
        with open(history_path) as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    history.append({
        "date": report["generated"],
        "total_skills": report["total_skills"],
        "evaluated": report["evaluated"],
        "passed": report["passed"],
        "failed": report["failed"],
        "not_run": report["not_run"],
    })
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)
    print(f"  📄 reports/history.json")


def save_markdown_report(report: dict):
    """Save report as Markdown."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = os.path.join(REPORTS_DIR, "latest.md")

    lines = []
    lines.append("# Engineering AI Evaluation Report\n")
    lines.append(f"**Generated:** {report['generated']}\n")
    lines.append(f"**Skills:** {report['total_skills']} total, {report['evaluated']} evaluated\n")
    lines.append(f"**Passed:** {report['passed']} | **Failed:** {report['failed']} | **Not Run:** {report['not_run']}\n")
    lines.append("---\n")

    if report["regressions"]:
        lines.append("## Regressions Detected\n")
        for r in report["regressions"]:
            lines.append(f"- ❌ **{r['skill']}**: score {r['score']} below threshold {r['threshold']}")
        lines.append("")

    lines.append("## Evaluation Results\n")
    lines.append("| Skill | Version | Threshold | Score | Status | Last Run |")
    lines.append("|-------|---------|-----------|-------|--------|----------|")
    for e in report["evaluations"]:
        score_str = str(e["score"]) if e["score"] is not None else "-"
        if e["status"] == "pass":
            status = "✅ pass"
        elif e["status"] == "regression":
            status = "❌ regression"
        else:
            status = "⏳ not run"
        lines.append(f"| {e['skill']} | {e['version']} | {e['threshold']} | {score_str} | {status} | {e['last_run']} |")

    lines.append("")
    if report["failed"] > 0:
        lines.append("---")
        lines.append("**Status: FAILED** — regressions detected. Review needed before release.")
    else:
        lines.append("**Status: PASS** — all evaluated skills meet thresholds.")

    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  📄 reports/latest.md")


def generate_all():
    """Generate all report formats."""
    print("\nGenerating reports...")
    report = generate_report()
    save_json_report(report)
    save_markdown_report(report)
    print("  ✅ Reports generated")
    return report
