# Contributing to Engineering AI Standards

## How to Contribute

### 1. Propose Changes

Open an issue or pull request describing your proposed change. Explain why the change is needed and how it fits within the existing architecture.

### 2. Follow the Architecture

Ensure your addition follows the separation of concerns:

- **Principles** → philosophy, not rules
- **Standards** → mandatory rules, not preferences
- **Patterns** → reusable solutions, not mandates
- **Skills** → AI instructions, not human documentation
- **Adapters** → tool-specific formats, not duplicated content

### 3. Skill Module Creation

When creating or modifying a skill module under `skills/<name>/`:

- `SKILL.md` must include YAML frontmatter with `name`, `version`, `category`, `dependencies`, and `evaluation` fields.
- `metadata.yaml` mirrors the frontmatter for machine parsing.
- `CHANGELOG.md` tracks version history for that skill.
- `examples/` directory contains usage examples.
- `eval/` directory contains one YAML file per evaluation case.
- Skill `version` follows semantic versioning independently of the repository version.
- After creating a skill, register it in `registry/skills.yaml` with owner, status, dependencies, and evaluation threshold.
- All eval files must pass `python evaluations/runner/run.py --registry`.

### 4. Workflow Creation

When creating or modifying a workflow under `workflows/`:

- Document entry criteria (what must be true before starting).
- Define the step-by-step flow with references to skills in `skills/`.
- Specify quality gates between steps (checks that must pass).
- Document exit criteria (definition of done).

### 5. Maintain Consistency

- Use the same heading structure as related files
- Reference existing files with relative links
- Keep language concise and unambiguous
- Use active voice and imperative mood for rules

### 6. Version Management

Every skill change must:

1. Update the skill's `CHANGELOG.md` and the root `CHANGELOG.md`
2. Bump version in `metadata.yaml` and `registry/skills.yaml`
3. Add or update evaluation cases in `evaluations/cases/` or `skills/*/eval/`
4. Run `python evaluations/runner/run.py --registry` to validate evaluation structure and registry consistency
5. Verify scoring weights sum to 100 per case

### 7. Pull Request Process

1. Create a feature branch from `main`
2. Make your changes following the above guidelines
3. If adding a skill, include evaluation cases and update the registry
4. If adding a workflow, reference existing skills
5. If changing an adapter, update the reference only — do not duplicate skill content
6. Follow the [review policy](governance/review-policy.md) for change classification
7. Submit the PR with a clear description of what changed and why

### 8. Review Criteria

Pull requests are evaluated on:

- **Correctness**: Is the content accurate and technically sound?
- **Consistency**: Does it follow the established structure and style?
- **Clarity**: Can both humans and AI agents parse it?
- **Governance compliance**: Does the change follow review policy and release process?
- **Necessity**: Does it fill a genuine gap vs. duplicate existing content?
