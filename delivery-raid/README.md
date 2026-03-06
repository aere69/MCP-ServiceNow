# Delivery/RAID Managemet - MCP Server

Delivery/RAID is where you turn all that ITSM and CMDB structure into programme control: visibility, risk management, and decision‑ready narratives. In FastMCP terms, it’s about giving the LLM a way to see the delivery picture, reason about it, and log/shape actions without becoming a rogue PM.

## What delivery/RAID needs to cover

At a minimum:

- **Delivery control:** milestones, dependencies, sprints, scope, blockers.
- **RAID discipline:** risks, assumptions, issues, dependencies—logged, owned, and tracked.
- **Narratives:** exec summaries, status reports, Go/No‑Go views.
- **Bridges:** link delivery/RAID to Change, Incident/Problem, and CMDB.

FastMCP is perfect for this because you can encode your governance style directly into prompts and tools.

## Prompts for delivery and RAID

Prompts become your playbooks for control—how the LLM thinks about delivery health, risk, and decisions.

### Core prompts

- **delivery_status_review(project_id)**  
Assess overall status, RAG, key risks, and next steps.
- **raid_review(project_id)**  
Scan RAID items, highlight critical ones, and propose actions.
- **dependency_analysis(project_id)**  
Identify critical path, cross‑team dependencies, and risk hotspots.
- **go_no_go_assessment(release_id)**  
Combine change, incident, and CMDB signals into a Go/No‑Go view.
- **exec_summary(project_id)**  
Generate a concise, C‑suite‑ready summary with clear asks/decisions.
- **risk_brainstorm(project_id)**  
Structured risk identification for upcoming phases or releases.

## Resources for delivery/RAID

Resources give the LLM the delivery picture—plans, boards, RAID, releases—without letting it mutate anything directly.

### Recommended resources

- **project_overview(project_id)**  
Objectives, scope, key milestones, sponsors, RAG.
- **sprint_board(project_id)**  
Epics, stories, status, throughput, blockers.
- **raid_log(project_id)**  
Risks, assumptions, issues, dependencies with owners and status.
- **release_calendar(project_id)**
Upcoming releases, change windows, blackout periods.
- **change_risk_feed(project_id)**  
Aggregated risk from related changes (from your Change MCP).
- **incident_trend_feed(project_id)**  
Incident/problem trends for in‑scope services.
- **cmdb_impact_feed(project_id)**  
Key CIs/services touched by the programme and their risk.

## Tools for delivery/RAID

Tools let the LLM log and shape control actions—but still keep humans in the loop.

### RAID tools

- **create_raid_item(project_id, item_type, title, description, impact, owner)**  
Log new risks/issues/dependencies.
- **update_raid_item(raid_id, fields)**  
Adjust status, owner, mitigation, etc.
- **escalate_raid_item(raid_id, reason)**  
Flag for steering committee / senior review.

### Delivery tools

- **add_status_note(project_id, note)**  
Append a governance note to the status log.
- **propose_milestone_change(project_id, milestone_id, new_date, rationale)**  
Log a proposed change, not auto‑apply it.
- **log_decision(project_id, decision, rationale, owner)**  
Capture key decisions and context.

## How delivery/RAID ties back to Change, Incident, CMDB

This is where it gets powerful:

- **From Change:**
  - feed high‑risk changes into RAID
  - block Go/No‑Go if critical changes are non‑compliant

- From Incident/Problem:
  - recurring incidents become risks/issues
  - major incidents feed into programme risk and cutover planning

- **From CMDB:**
  - poor CI quality becomes a risk
  - missing relationships become dependencies and cutover risks

In FastMCP terms, your delivery/RAID prompts can explicitly say:

    “Use `change_risk_feed`, `incident_trend_feed`, and `cmdb_impact_feed` to inform your risk assessment and RAID updates.”

That’s you encoding **true cross‑functional governance** into the system.