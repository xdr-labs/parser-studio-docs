<h1 align="center">Parser Studio User Guide</h1>

<p align="center">
  <strong>Practical, step-by-step documentation for building and reviewing security log parsers.</strong>
</p>

<p align="center">
  Start with a sample log, follow the product's visible controls, validate your field mappings, and work through task-based examples at your own pace.
</p>

<p align="center">
  <strong>English</strong> · <a href="https://github.com/xdr-labs/parser-studio">Parser Studio</a> · <a href="quickstart.mdx">Quickstart</a> · <a href="scenarios/index.mdx">Scenario Playbooks</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/content-User%20Manual-2563EB?style=flat-square" alt="User Manual">
  <img src="https://img.shields.io/badge/guides-Step%20by%20Step-7C3AED?style=flat-square" alt="Step-by-step guides">
  <img src="https://img.shields.io/badge/playbooks-12%20Scenarios-16A34A?style=flat-square" alt="12 scenario playbooks">
  <img src="https://img.shields.io/badge/examples-Synthetic-0891B2?style=flat-square" alt="Synthetic examples">
</p>

---

## What this guide covers

This repository is the **user manual for [Parser Studio](https://github.com/xdr-labs/parser-studio)**, organized around what a first-time user actually wants to accomplish.

It explains how to:

- create a parser through the four guided **Auto Parser** stages
- understand extracted fields, unresolved source regions, and record boundaries
- review and correct Stellar Cyber normalization mappings
- work with JSON, Syslog/KV, CEF, LEEF, CSV, and other reviewed source structures
- use **ChatGPT Assisted Parser** with manually masked examples and structured recipe review
- validate proposed changes with independent sample records
- download generated files and a standalone Python test sender
- save, compare, and restore browser-local parser drafts

## Start here

| Guide | What you will learn |
| --- | --- |
| [Overview](index.mdx) | What Parser Studio does and how to begin |
| [Quickstart](quickstart.mdx) | Build your first parser from fictional JSON events |
| [Choose a workflow](choose-workflow.mdx) | Decide between Auto Parser and ChatGPT assistance |
| [Auto Parser](workflows/auto-parser.mdx) | Add Logs → Review Fields → Map Fields → Create Parser |
| [Review Fields](workflows/review-fields.mdx) | Compare raw records with extracted fields and values |
| [Map Fields](workflows/map-fields.mdx) | Review field destinations, types, and mapping conflicts |
| [Create and Download](workflows/create-and-download.mdx) | Generate and inspect integrity-checked draft files |
| [ChatGPT Assisted Parser](workflows/chatgpt-assisted.mdx) | Copy, review, import, and validate structured suggestions |

## Scenario playbooks

Each scenario provides a goal, fictional input or prerequisites, a guided UI procedure, an expected review outcome, and a recovery path.

| Scenario | Focus |
| --- | --- |
| [JSON firewall logs](scenarios/first-firewall-json.mdx) | First parser and nested fields |
| [Syslog with KV](scenarios/syslog-kv.mdx) | Header versus message-body extraction |
| [CEF and LEEF](scenarios/cef-leef.mdx) | Structured headers and extension delimiters |
| [CSV with a definition](scenarios/csv-with-spec.mdx) | Verified ordered column names |
| [Positional firewall CSV](scenarios/panos-positional.mdx) | Avoiding guessed field meanings |
| [Unknown log](scenarios/unknown-log.mdx) | Diagnosing incomplete or uncertain parsing |
| [Mixed events](scenarios/mixed-events.mdx) | Accounting for different event structures |
| [Multiline Java exceptions](scenarios/multiline-java.mdx) | Reviewing event framing |
| [Normalization](scenarios/normalization.mdx) | Correcting target fields and value types |
| [ChatGPT-assisted recovery](scenarios/recipe-ai.mdx) | Privacy-reviewed proposals and additional validation |
| [Python test sender](scenarios/test-sender.mdx) | Generating synthetic event variations |
| [Local versions](scenarios/revisions.mdx) | Comparing and restoring mapping experiments |

See the [complete scenario index](scenarios/index.mdx) to choose your next exercise.

## Using the examples

1. Start with the [Quickstart](quickstart.mdx) and paste the provided fictional log samples.
2. Follow **Auto Parser** in the product; compare every important extracted field against the original text.
3. Review normalization suggestions instead of assuming every proposed destination is correct.
4. Resolve incomplete records or mapping issues before generating files.
5. Use the matching scenario guide when working with a different record format.

Examples are for learning and review. A successful result on a small sample does **not** prove that all variations from the same product or vendor will be parsed correctly.

## Reference

- [Supported formats and boundaries](reference/supported-formats.mdx)
- [Generated output artifacts](reference/output-artifacts.mdx)
- [Source data and privacy](reference/source-privacy.mdx)
- [Troubleshooting](reference/troubleshooting.mdx)
- [Glossary](reference/glossary.mdx)
- [Frequently asked questions](reference/faq.mdx)

## Documentation scope

This repository contains **product usage instructions**, not the application source code. User-facing content is English-only to match Parser Studio. The examples use synthetic values and reserved documentation addresses; do not commit private customer logs.

The current manual was checked against [Parser Studio source revision `ec6a9e6`](https://github.com/xdr-labs/parser-studio/commit/ec6a9e6bfc26214dd10f07c09021c1c8c2742a7c). Check the actual product UI for newer behavior.

## Related projects

- [Parser Studio](https://github.com/xdr-labs/parser-studio) — application and parser authoring workflow
- [XDR Labs Portal](https://xdr.ooo/) — XDR Labs project portal

---

<p align="center">
  <strong>Learn by example. Review every field. Keep the result reproducible.</strong>
</p>
