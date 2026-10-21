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
  <img src="https://img.shields.io/badge/Examples-Synthetic-0891B2?style=flat-square" alt="Fictional examples">
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

The previous source snapshot was [Parser Studio main at `90e4c53`](https://github.com/xdr-labs/parser-studio/commit/90e4c53f0ba5f87262c3c027a1024047ea4b173f).

## Documentation checks

```bash
python3 scripts/validate_docs.py
```

Only this documentation repository is used for the manual. No original customer records belong in examples or screenshots.

---

<p align="center">
  <strong>Paste. Analyze. Fix only what is needed. Review. Create.</strong>
</p>

The October 21, 2026 UI check used the deployed JavaScript asset index-CCvjpx9h.js, qualified source 7b09542435f6ba26fae52a63a22608b17bcd6d6e. Product navigation remains English; the Korean documentation is separately localized.
