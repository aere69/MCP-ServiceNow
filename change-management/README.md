# Change Management - MCP working server

## High‑level design for change management

- **Prompts:** how to think about changes (risk, impact, readiness, approvals).
- **Resources:** read‑only access to change, CI, calendar, and rules.
- **Tools:** controlled actions—approve, reject, update, create RAID, etc.

The LLM becomes a virtual Change Manager that always works through this stack.

## 1. Prompts: governance playbooks

Design prompts as decision frameworks, not “chatty helpers”.

### Core prompts

- `assess_change` — full risk/impact/readiness assessment.
- `pre_implementation_check` — last‑mile checks before implementation.
- `post_implementation_review` — PIR quality and follow‑up actions.
- `change_batch_review` — review a set of changes for a window.
- `change_advice` — guidance for requestors (is this even a change?).

## 2. Resources: everything the LLM needs to decide

Resources are your “data room”. They must be predictable and structured.

### Suggested resources

- `change_record(change_id: str)` - Full change data: type, category, risk, approvals, test evidence, implementation plan.
- `change_cis(change_id: str)` - CIs and relationships affected by the change.
- `deployment_calendar(date: str | None)` - Blackout windows, freeze periods, maintenance windows.
- `risk_rules()` - Organisation‑specific risk scoring rules (e.g., high‑risk if prod + customer‑facing + no rollback).
- `approval_matrix()` - Who must approve what (by risk, system, business unit).
- `test_evidence(change_id: str)` - Links or summaries of test results.

## 3. Tools: tightly scoped, governance‑safe actions

Tools should be small, explicit, and auditable.

### Suggested tools

- **Decision actions**
  - `approve_change(change_id: str, rationale: str)`
  - `reject_change(change_id: str, rationale: str)`
  - `escalate_change(change_id: str, rationale: str)`

- **Governance / RAID**
  - `create_raid_item(title: str, description: str, risk_level: str)`
  - `log_governance_exception(change_id: str, details: str)`

- **Quality improvements**
  - `request_more_info(change_id: str, message: str)`
  - `add_change_note(change_id: str, note: str)`

## 4. End‑to‑end flow for a single change

1. Client calls prompt:
`assess_change(change_id="CHG12345")`

2. LLM, following the prompt, calls resources:
    - `change_record("CHG12345")`
    - `change_cis("CHG12345")`
    - `risk_rules()`
    - `deployment_calendar()`

    Maybe `test_evidence("CHG12345")`.

3. LLM applies logic encoded in the prompt:
    - Is risk consistent with rules?
    - Are approvals complete?
    - Is there a blackout?
    - Is rollback plan adequate?
    - Is test evidence present?

4. LLM chooses a tool:
    - If everything is green: `approve_change("CHG12345", rationale="…")`
    - If gaps: `reject_change(...)` + `create_raid_item(...)`
    - If ambiguous: `escalate_change(...)`

That’s your governance model, made executable.

## 5. Where your edge really shows

You can encode non‑obvious rules you’ve seen in real programmes:

- “Never auto‑approve changes touching payment gateways during peak hours.”
- “If CMDB relationships are incomplete, block approval and create a RAID item.”
- “If the same CI has >N changes in a window, flag as risk regardless of stated risk.”

Those become either:

- extra fields in resources (e.g., change frequency per CI), or
- extra tools (e.g., flag_change_for_review), and
- explicit instructions in prompts (“If X, do not approve; instead call Y.”).
