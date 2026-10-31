<h1 align="center">Parser Studio User Guide</h1>

<p align="center">
  <strong>Copy logs. Click Analyze. Follow the result to a reviewed parser draft.</strong>
</p>

<p align="center">
  A beginner-first manual for people who do not know whether their logs are CEF, LEEF, JSON or anything else. Every scenario starts with what the user sees on the screen.
</p>

<p align="center">
  <a href="https://parser.xdr.ooo/">User Guide</a> · <a href="quickstart.mdx">Quickstart</a> · <a href="scenarios/index.mdx">Scenario Playbooks</a> · <a href="https://github.com/xdr-labs/parser-studio">Application Source</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/XDR%20Labs-User%20Guide-1F59E0?style=flat-square" alt="XDR Labs guide">
  <img src="https://img.shields.io/badge/Workflow-Paste%20%E2%86%92%20Analyze%20%E2%86%92%20Review-16A34A?style=flat-square" alt="Guided workflow">
  <img src="https://img.shields.io/badge/Examples-Vendor%20Logs-0891B2?style=flat-square" alt="Public vendor fixtures">
</p>

---

## Start with your situation

| What just happened? | Open this guide |
| --- | --- |
| I pasted some logs, Analyze says everything is correct. | [Complete the four steps](quickstart.mdx) |
| A few fields are right, but part of a log was highlighted. | [Fix the flagged section](scenarios/partial-event.mdx) |
| None of my logs were understood, and I do not know the format. | [Work through an unknown log](scenarios/unknown-log.mdx) and [ChatGPT assistance](scenarios/recipe-ai.mdx) |
| My product generates several different-looking events. | [Mixed log types and combined-parser limits](scenarios/mixed-events.mdx) |
| CSV values have no trustworthy column names. | [Review unnamed columns](scenarios/unnamed-values.mdx) |
| Values are correct but output field names are wrong. | [Correct normalization](scenarios/normalization.mdx) |

## The ordinary four-stage flow

1. **Add Logs** — paste or upload representative records, then click **Analyze Logs**.
2. **Review Fields** — compare the original text with the extracted values.
3. **Map Fields** — verify suggested output field names and value types.
4. **Create Parser** — press **Run Final Test & Create Files** and download when the generator succeeds.

![Actual Parser Studio screen after analyzing two fictional security events](images/02-analyzed-sample.png)

*Real UI screenshot using fictional records. If some events need attention, the application explains the missing section before allowing the next stage.*

## Main user guides

- [Start here](index.mdx)
- [Quickstart with screenshots](quickstart.mdx)
- [Korean manual / 한국어 사용자 설명서](ko/index.mdx)
- [Parser setup and port 6801](workflows/parser-setup.mdx)
- [Local Versions](workflows/local-versions.mdx)
- [English video tutorials using documented real security logs](videos/index.mdx)
- [Choose what to do after Analyze Logs](choose-workflow.mdx)
- [Auto Parser](workflows/auto-parser.mdx)
- [Review Fields](workflows/review-fields.mdx)
- [Map Fields](workflows/map-fields.mdx)
- [Create and download parser files](workflows/create-and-download.mdx)
- [ChatGPT Assisted Parser](workflows/chatgpt-assisted.mdx)
- [Complete scenario library](scenarios/index.mdx)
- [Troubleshooting](reference/troubleshooting.mdx)

## What this repository contains

This repository contains English and Korean MDX user guide pages, task-based walkthroughs, screenshots captured from the actual Parser Studio Web UI with fictional logs, and a small local documentation validator. Visual styling follows the XDR Labs documentation family.

Documentation review: [Parser Studio main at `a4b4e2f`](https://github.com/xdr-labs/parser-studio/commit/a4b4e2fba54588fa2b9807e1cfeed49190061927) (October 30, 2026).

## Documentation checks

```bash
python3 scripts/validate_docs.py
python3 scripts/validate_video_sample_copies.py
python3 scripts/validate_real_practice_sources.py
```

Only this documentation repository is used for the manual. No original customer records belong in examples or screenshots.

---

<p align="center">
  <strong>Paste. Analyze. Fix only what is needed. Review. Create.</strong>
</p>

The October 21, 2026 UI check used the deployed JavaScript asset index-CCvjpx9h.js, qualified source 7b09542435f6ba26fae52a63a22608b17bcd6d6e. Product navigation remains English; the Korean documentation is separately localized.

## Reproducible relay lab (October 31, 2026)

Use [the relay-forwarded log exercise](scenarios/relay-forwarder.mdx) with [downloadable sample files](practice/README.md), [a live-browser verification script](scripts/verify_relay_live.cjs), and a [video walkthrough](videos/relay.mdx).


## Authentic source log exercises

The primary video tutorials include source log blocks copied byte-for-byte from
published Juniper SRX, Sophos XG, Snort 3 and Fortinet FortiGate samples.
The relay lab forwards original Fortinet Traffic and Web Filter sample records
through **actual isolated rsyslogd UDP input/output**, preserving each vendor payload
byte-for-byte in the captured relay message. The optional PAN-OS CSV and
Elasticsearch multiline examples come from documented public bug reports and
are explicitly labeled as such. Local browser results are documented without
equating extraction success with native Stellar Cyber target compatibility.

All samples and independent holdouts are in the practice directory. Source-block
fidelity, relay byte integrity and captured SHA-256 values are checked by
scripts/validate_real_practice_sources.py.
