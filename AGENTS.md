# Parser Studio User Docs — Repository Rules

Canonical Engineering System: https://github.com/datarelay-labs/engineering-system

## Read first

1. Read this file and `.engineering/project.yaml`.
2. Read the README and existing topic pages.
3. Read the Parser Studio product's `AGENTS.md` and `.engineering/project.yaml` **without modifying that repository** before documenting newly implemented features.
4. Tie current product behavior to a pinned source revision.

## Scope

Only the Parser Studio user manual, how-to workflows and practical usage scenarios belong in this repository. Do not edit application repositories or unrelated documentation.

- Preserve English on the original site routes. Author requested (2026-10-21) complete Korean localized user docs under ko/ with Korean explanations; keep exact English product UI labels, code, raw log data and serialized fields unchanged.
- A playbook includes prerequisites or a sample, exact UI steps, expected observed behavior and recovery guidance.
- Preserve factual scope: do not claim completeness for unseen vendor logs based on one sample.
- Use reserved documentation addresses, fictional identities and neutral sample data.
- Clarify that customer source data should be reviewed and masked before manual disclosure.
- Do not add publishing-service setup instructions or infrastructure configuration.
- Run the repository's local documentation checks before commit and push.
