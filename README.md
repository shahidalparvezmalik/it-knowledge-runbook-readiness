# IT Knowledge & Runbook Readiness Review

A compact offline proof of concept for reviewing synthetic IT knowledge records and runbooks before people rely on them during support or incident response. It flags missing ownership, unconfirmed service mappings, stale review dates, and gaps in operational guidance, then produces a human-review queue.

> Deterministic rules, synthetic data only. This is a review aid, not a knowledge platform, technical validation engine, readiness certification, or automated action system.

## Why this project
A runbook can look complete while leaving an on-call engineer unsure who owns it, which service it applies to, whether its instructions were recently checked, or how to validate the outcome. The prototype makes some of those documentation gaps visible from a CSV snapshot. It complements the portfolio's change-readiness and service-continuity work while focusing on knowledge stewardship rather than approvals, recovery planning, search, or AI.

Google's SRE Workbook recommends reviewing incident plans and playbooks. PeopleCert's 2026 knowledge-management article discusses knowledge management in ITSM. These sources motivate the topic; they do not validate this prototype's rules.

## What it checks
- Required ownership, service, purpose, preconditions, steps, validation, and escalation/fallback information.
- Review dates against supplied intervals; future dates and invalid dates are flagged.
- Explicit confirmation state for owners and service mappings.
- Rollback or escalation guidance for records labeled high risk.
- CSV and JSON reason-coded reports.

## Run
Requires Python 3.10+; standard library only.

```bash
python -m unittest discover -v
python -m knowledge_readiness.cli --input data/knowledge_items.csv --output-dir reports --today 2026-11-16
```

Observed sample: `Reviewed 5 knowledge item(s); 3 flagged; human review required. Reports: reports`

`HUMAN_REVIEW` means a configured check flagged an item. `CHECKS_PASSED_REVIEW_REQUIRED` means these limited checks found no flags; it is not approval or proof of correctness. Read [decision rules](docs/DECISION_RULES.md), [data dictionary](docs/DATA_DICTIONARY.md), and [operating model and limits](docs/OPERATING_MODEL.md).

No AI, retrieval, write-back, live integrations, access control, or action execution. Synthetic fixtures only. The prototype does not verify technical instructions, certify readiness, measure outcomes, or claim ITIL/SRE conformance.

## About
Shahid Al Parvez Malik is a Senior IT Infrastructure & Service Delivery Manager with 20+ years of professional IT experience. [Portfolio](https://shahidalparvezmalik.com/) · [LinkedIn](https://www.linkedin.com/in/shahidalparvezmalik/)
