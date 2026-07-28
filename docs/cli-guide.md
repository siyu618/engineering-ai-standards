# CLI Guide

The `ai-standard` CLI tool manages skills, evaluations, and reports.

## Installation

No installation required. Run directly:

```bash
python tools/ai-standard/cli.py <command>
```

## Commands

### list-skills

List all registered skills with version, owner, status, and evaluation status.

```bash
python tools/ai-standard/cli.py list-skills
```

Example output:
```
Available Skills:

Skill                          Version      Owner                Status     Eval
--------------------------------------------------------------------------------
design                         1.0.0        architecture-team    stable     ✅
python-development             1.0.0        backend-team         stable     ✅
...
```

### validate

Validate the repository structure, skill metadata, registry consistency, and evaluation references.

```bash
python tools/ai-standard/cli.py validate
```

Example output:
```
Validation Result:

  Directories:     PASS
  Files:           PASS
  Skills:          PASS
  Registry:        PASS
  Evaluations:     PASS

  ✅ All checks passed
```

### eval

Trigger evaluation for a specific skill. Loads the skill's evaluation cases and reports status.

```bash
python tools/ai-standard/cli.py eval design
```

For actual scoring, pipe agent output through the evaluator:

```bash
python evaluations/runner/evaluator.py --case cache-design --method rule --output response.md
```

### report

Generate evaluation report as JSON and Markdown in the `reports/` directory.

```bash
python tools/ai-standard/cli.py report
```

Output is written to:
- `reports/latest.json` — machine-readable scores
- `reports/latest.md` — human-readable report
- `reports/history.json` — chronological score history

## Common Workflows

### Full validation cycle

```bash
python tools/ai-standard/cli.py validate
python tools/ai-standard/cli.py list-skills
python tools/ai-standard/cli.py report
```

### Evaluate all enabled skills

```bash
for skill in $(python tools/ai-standard/cli.py list-skills 2>&1 | grep "✅" | awk '{print $1}'); do
  python tools/ai-standard/cli.py eval "$skill"
done
```
