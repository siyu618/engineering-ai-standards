# Release Process

## Versioning

Skills follow [semantic versioning](https://semver.org/) independently of the
repository version. The repository itself also follows semantic versioning for
structural changes.

### Skill Versioning

Given a version MAJOR.MINOR.PATCH:

| Increment | When | Example |
|-----------|------|---------|
| MAJOR | Breaking change to the skill contract | `1.0.0` → `2.0.0` |
| MINOR | New capabilities, backwards compatible | `1.0.0` → `1.1.0` |
| PATCH | Fixes, clarifications, no behavior change | `1.0.0` → `1.0.1` |

### Repository Versioning

| Increment | When | Example |
|-----------|------|---------|
| MAJOR | Breaking structural change | `1.0.0` → `2.0.0` |
| MINOR | New capability (registry, governance, etc.) | `1.2.0` → `1.3.0` |
| PATCH | Fixes, clarifications to existing content | `1.2.0` → `1.2.1` |

## Release Checklist

### For a Skill Change

1. **Update the skill's CHANGELOG.md** with the change description
2. **Bump version** in `metadata.yaml` and `registry/skills.yaml` (both the skill version and the registry version)
3. **Run evaluation**: `python evaluations/runner/run.py --registry`
4. **Verify no regression** (all scores meet thresholds defined in registry)
5. **Create PR** with the changes
6. **Obtain review** per [review-policy.md](review-policy.md)
7. **Merge to main**

### For a Repository Structural Change

1. **Update CHANGELOG.md** at the repository root
2. **Document ADRs** if architectural decisions change
3. **Update cross-references** in README, CONTRIBUTING, AGENTS.md
4. **Update CI workflows** if structure changes affect validation paths
5. **Create PR** with the changes
6. **Merge to main**

## Version Tracking

Versions are tracked in these locations:

| Location | What | Update When |
|----------|------|-------------|
| `registry/skills.yaml` | Skill versions + registry version | Every skill change |
| `skills/*/metadata.yaml` | Per-skill version | Every skill change |
| `skills/*/CHANGELOG.md` | Per-skill changelog | Every skill change |
| `CHANGELOG.md` (root) | Repository-level changelog | Every structural change |
