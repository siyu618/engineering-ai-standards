# Skill Development Guide

## Overview

A skill is a reusable engineering capability module. Each skill lives under `skills/<name>/`
and contains:

```
skills/<name>/
├── SKILL.md               # Process instructions for AI agents
├── metadata.yaml           # Machine-readable metadata
├── CHANGELOG.md            # Version history
└── examples/               # Usage examples (optional for v1, recommended)
    └── <example>.md
```

## Step-by-Step: Creating a New Skill

### 1. Create the directory

```bash
mkdir skills/my-skill
```

### 2. Write SKILL.md

Include YAML frontmatter with name, version, category, dependencies, and evaluation config:

```yaml
---
name: my-skill
version: 1.0.0
category:
  - domain
  - subdomain
dependencies:
  - principles/engineering-principles.md
evaluation:
  enabled: false
---
```

The body contains the skill's process instructions:

```markdown
## Role

Act as a [Role] specializing in [Domain].

## Process

### Step 1: [Name]
Description of the step.

### Step 2: [Name]
Description of the step.
```

### 3. Create metadata.yaml

Mirrors the frontmatter for machine parsing:

```yaml
---
name: my-skill
version: 1.0.0
category:
  - domain
dependencies:
  - principles/engineering-principles.md
evaluation:
  enabled: false
---
```

### 4. Create CHANGELOG.md

```markdown
# My Skill Changelog

## [1.0.0] - 2026-07-28

- Initial release.
```

### 5. Register in the registry

Add the skill to `registry/skills.yaml`:

```yaml
my-skill:
  version: 1.0.0
  owner: your-team
  status: stable
  compatibility:
    claude: true
    cursor: true
    copilot: true
  dependencies:
    - principles/engineering-principles.md
  evaluation:
    enabled: false
```

### 6. Validate

```bash
python tools/ai-standard/cli.py validate
```

## Adding Evaluation Cases

Once a skill is stable, enable evaluation:

1. Create cases in `evaluations/cases/<category>/`
2. Update `metadata.yaml`: `evaluation.enabled: true`
3. Update `evaluation.cases` with case IDs
4. Set a `threshold` (minimum passing score)
5. Run `python evaluations/runner/run.py --verbose`

## Versioning

Skills follow semantic versioning independently of the repository:

- **MAJOR**: Breaking change to the skill contract
- **MINOR**: New capabilities, backwards compatible
- **PATCH**: Fixes, clarifications, no behavior change

Bump the version in both `metadata.yaml` and `registry/skills.yaml`.
