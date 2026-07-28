"""
Validator — checks skill structure, registry consistency, and required files.
"""

import glob
import os
import sys
import yaml


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILLS_DIR = os.path.join(ROOT, "skills")
REGISTRY_PATH = os.path.join(ROOT, "registry", "skills.yaml")
EVAL_CASES_DIR = os.path.join(ROOT, "evaluations", "cases")
REQUIRED_DIRS = [
    "principles", "standards/coding", "standards/testing", "standards/architecture",
    "patterns", "skills", "adapters", "evaluations/cases", "evaluations/runner",
    "templates", "docs/adr", "workflows", "registry", "governance", "runtime",
]


def check_required_dirs() -> list[str]:
    errors = []
    for d in REQUIRED_DIRS:
        path = os.path.join(ROOT, d)
        if not os.path.isdir(path):
            errors.append(f"Missing directory: {d}")
    return errors


def check_required_files() -> list[str]:
    errors = []
    for f in ["README.md", "CONTRIBUTING.md", "CHANGELOG.md", "LICENSE", "AGENTS.md"]:
        if not os.path.isfile(os.path.join(ROOT, f)):
            errors.append(f"Missing file: {f}")
    return errors


def check_skill_structure() -> list[str]:
    errors = []
    for skill_dir in sorted(glob.glob(os.path.join(SKILLS_DIR, "*", ""))):
        name = os.path.basename(os.path.dirname(skill_dir))
        for required in ["SKILL.md", "metadata.yaml", "CHANGELOG.md"]:
            if not os.path.isfile(os.path.join(skill_dir, required)):
                errors.append(f"{name}: missing {required}")
        # Check metadata.yaml is valid YAML
        meta_path = os.path.join(skill_dir, "metadata.yaml")
        if os.path.isfile(meta_path):
            try:
                with open(meta_path) as f:
                    data = yaml.safe_load(f)
                if not data or "name" not in data:
                    errors.append(f"{name}: metadata.yaml missing required field 'name'")
                if not data or "version" not in data:
                    errors.append(f"{name}: metadata.yaml missing required field 'version'")
            except yaml.YAMLError:
                errors.append(f"{name}: metadata.yaml is not valid YAML")
    return errors


def check_registry() -> list[str]:
    errors = []
    if not os.path.isfile(REGISTRY_PATH):
        errors.append("registry/skills.yaml not found")
        return errors

    with open(REGISTRY_PATH) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError:
            errors.append("registry/skills.yaml is not valid YAML")
            return errors

    if not data or "skills" not in data:
        errors.append("registry/skills.yaml missing 'skills' key")
        return errors

    skills = data["skills"]
    # Check all registered skills have a matching directory
    for name in skills:
        if not os.path.isdir(os.path.join(SKILLS_DIR, name)):
            errors.append(f"registry: skill '{name}' has no matching skills/{name}/ directory")

    # Check all skill directories are in registry
    registered = set(skills.keys())
    present = set(os.path.basename(d.rstrip("/")) for d in glob.glob(os.path.join(SKILLS_DIR, "*", "")))
    for name in sorted(present - registered):
        errors.append(f"skill '{name}' exists in skills/ but is not registered in registry/skills.yaml")

    return errors


def check_eval_references() -> list[str]:
    errors = []
    if not os.path.isfile(REGISTRY_PATH):
        return errors
    with open(REGISTRY_PATH) as f:
        data = yaml.safe_load(f)
    if not data:
        return errors

    # Collect all eval case IDs from files
    case_ids = set()
    for f in glob.glob(os.path.join(EVAL_CASES_DIR, "**/*.yaml"), recursive=True):
        try:
            with open(f) as fh:
                case = yaml.safe_load(fh)
                if case and "id" in case:
                    case_ids.add(case["id"])
        except yaml.YAMLError:
            continue

    # Check registry references
    for name, skill in data.get("skills", {}).items():
        ev = skill.get("evaluation", {})
        for case_id in ev.get("cases", []):
            if case_id not in case_ids:
                errors.append(f"registry skill '{name}' references eval case '{case_id}' but no matching file found")

    return errors


def validate_all() -> dict:
    """Run all validations. Returns {category: (pass_count, fail_count, [messages])}."""
    results = {}

    dir_errors = check_required_dirs()
    results["Directories"] = (0 if dir_errors else 1, len(dir_errors), dir_errors)

    file_errors = check_required_files()
    results["Files"] = (0 if file_errors else 1, len(file_errors), file_errors)

    skill_errors = check_skill_structure()
    results["Skills"] = (0 if skill_errors else 1, len(skill_errors), skill_errors)

    reg_errors = check_registry()
    results["Registry"] = (0 if reg_errors else 1, len(reg_errors), reg_errors)

    eval_errors = check_eval_references()
    results["Evaluations"] = (0 if eval_errors else 1, len(eval_errors), eval_errors)

    return results


def print_validation(results: dict):
    print("\nValidation Result:\n")
    all_pass = True
    for category, (status, count, messages) in results.items():
        if count == 0:
            print(f"  {category}:     PASS")
        else:
            all_pass = False
            print(f"  {category}:     FAIL ({count} issue(s))")
            for msg in messages[:5]:
                print(f"    • {msg}")
            if len(messages) > 5:
                print(f"    ... and {len(messages)-5} more")
    print()
    print("  " + ("✅ All checks passed" if all_pass else "❌ Some checks failed"))
    return all_pass
