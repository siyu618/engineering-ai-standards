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
- `CHANGELOG.md` tracks version history for that skill.
- `eval.yaml` defines evaluation cases. Fields follow the standardized format: `id`, `skill`, `category`, `version`, `task`, `context`, `expected.must_include`, `expected.forbidden`, `scoring`.
- Skill `version` follows semantic versioning independently of the repository version.
- All eval.yaml files must pass `python evaluations/runner/run.py`.

### 4. Maintain Consistency

- Use the same heading structure as related files
- Reference existing files with relative links
- Keep language concise and unambiguous
- Use active voice and imperative mood for rules

### 5. Version Management

Every skill change must:

1. Update the skill's `CHANGELOG.md` and the root `CHANGELOG.md`
2. Add or update evaluation cases in `evaluations/cases/`
3. Run `python evaluations/runner/run.py` to validate evaluation structure
4. Verify scoring weights sum to 100 per case

### 5. Pull Request Process

1. Create a feature branch from `main`
2. Make your changes following the above guidelines
3. If adding a skill, include evaluation cases
4. If changing an adapter, update the reference only — do not duplicate skill content
5. Submit the PR with a clear description of what changed and why

### 6. Review Criteria

Pull requests are evaluated on:

- **Correctness**: Is the content accurate and technically sound?
- **Consistency**: Does it follow the established structure and style?
- **Clarity**: Can both humans and AI agents parse it?
- **Necessity**: Does it fill a genuine gap vs. duplicate existing content?
