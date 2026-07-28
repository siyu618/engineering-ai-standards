# Review Policy

## Change Classification

Every change to a skill or its evaluation cases is classified by type. The type
determines the review requirements.

| Type | Description | Review Required | Evaluation Gate |
|------|-------------|----------------|-----------------|
| **Patch** | Clarification, typo fix, example update | 1 reviewer | Not required |
| **Minor** | New capability, expanded instructions | 1 reviewer + evaluation pass | Must pass all |
| **Major** | Behavior change, output format change | Architecture review + full eval suite | Must meet thresholds |
| **Breaking** | Incompatible change to skill contract | Architecture review + migration plan | Must meet thresholds + approval |

## Review Checklist

For all changes, reviewers should verify:

- [ ] **Skill metadata** is accurate (version, dependencies, category)
- [ ] **Evaluation cases** parse and pass validation
- [ ] **Registry** is updated if the skill version changed
- [ ] **CHANGELOG** is updated with the change description
- [ ] **No duplicated content** with other skills or standards
- [ ] **Examples** are consistent with the skill instructions
- [ ] **Cross-references** (links to standards/patterns) are valid

## Type Definitions

### Patch
- Correcting a typo or grammatical error
- Clarifying existing instructions without changing intent
- Adding or updating an example
- Updating a dependency path reference

### Minor
- Adding new process steps or guidance
- Expanding the scope of a skill
- Adding new evaluation cases
- Updating examples to reflect new patterns

### Major
- Changing the skill's process or methodology
- Changing the output format
- Removing a capability or feature
- Modifying scoring criteria weights

### Breaking
- Removing or renaming the skill
- Changing the skill contract in a way that breaks existing workflows
- Changing the evaluation schema
- Changing dependencies that require coordination across skills

## Escalation

If reviewers disagree on a change's classification, escalation follows:

1. Skill owner makes the initial classification
2. Reviewer may request reclassification
3. If unresolved, escalate to repository maintainers
