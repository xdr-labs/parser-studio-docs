# Parser Studio — User Documentation

This repository contains the **English-only user manual and practical scenario playbooks** for Parser Studio. It is organized around tasks a first-time user can complete in the actual product.

- Product source reviewed: [xdr-labs/parser-studio](https://github.com/xdr-labs/parser-studio), main commit `ec6a9e6bfc26214dd10f07c09021c1c8c2742a7c` (2026-10-18).
- Product authoring methods: **Auto Parser** and **ChatGPT Assisted Parser**.
- Main Auto Parser stages: **Add Logs → Review Fields → Map Fields → Create Parser**.
- Readers: first-time users, analysts, solutions engineers and parser reviewers.

## Start reading

- [Overview](index.mdx)
- [Create your first parser](quickstart.mdx)
- [Choose the right workflow](choose-workflow.mdx)
- [Auto Parser end-to-end](workflows/auto-parser.mdx)
- [ChatGPT-assisted workflow](workflows/chatgpt-assisted.mdx)
- [Scenario playbooks](scenarios/index.mdx)
- [Troubleshooting and common questions](reference/troubleshooting.mdx)

## Covered user scenarios

- Firewall JSON and nested fields
- Syslog with key/value body
- CEF and LEEF extension fields
- CSV with an explicit field-order specification
- Positional firewall CSV
- Unknown, partially extracted or mixed logs
- Multiline Java exceptions with explicit record framing
- Stellar Cyber metadata mapping review
- Manual ChatGPT-assisted rule recovery with independent tests
- Downloadable, standalone Python test sender
- Browser-local draft version comparison

## Maintain accuracy

Document only product behavior backed by the pinned source revision or subsequent verified evidence. The user-facing content is **English only**, following the Parser Studio source policy. Examples use fictional data; never commit private customer logs. Keep each scenario task-oriented: starting point, input, UI actions, expected review result and recovery path.

Run the local documentation checks after edits:

~~~bash
python3 scripts/validate_docs.py
~~~

This is a documentation-only repository. Product code and runtime settings do not belong here.
