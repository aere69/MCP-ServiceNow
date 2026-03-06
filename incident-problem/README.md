# Incident and Problem Management - MCP working server

Incident and problem management benefit from the same three‑layer FastMCP architecture you used for change management, but the logic shifts from governance and approval to triage, diagnosis, correlation, and root‑cause prevention. The goal is to give the LLM a safe, structured operating model that mirrors how a strong ITSM function behaves: fast, consistent, evidence‑based, and aligned with operational resilience.

## Incident and problem management in FastMCP

The architecture breaks into three coordinated layers:

- **Prompts** shape how the LLM reasons about incidents and problems.
- **Resources** provide structured data from ServiceNow and related systems.
- **Tools** perform controlled actions such as updating incidents, creating problems, or adding work notes.

This mirrors the real-world flow: triage → diagnosis → action → prevention.

## Prompts for incident and problem workflows

Prompts act as reusable playbooks that enforce consistent triage, severity classification, and RCA logic.

### Key prompts

- **incident_triage** — classify severity, identify impact, and propose next actions.
- **incident_diagnosis** — analyse logs, CI relationships, and recent changes.
- **incident_resolution_plan** — propose a structured recovery plan.
- **problem_identification** — determine whether an incident should become a problem.
- **problem_root_cause_analysis** — guide the LLM through RCA frameworks (5 Whys, Ishikawa).
- **problem_recommendations** — propose corrective and preventive actions.

## Resources for incident and problem data

Resources provide the LLM with the structured information it needs to make decisions. They are read‑only and safe.

### Recommended resources

- **incident_record(incident_id)** — core incident data: symptoms, impact, assignment group, priority.
- **incident_cis(incident_id)** — CIs linked to the incident.
- **recent_changes(ci_id)** — changes in the last X hours for a CI (critical for correlation).
- **service_impact_matrix()** — maps business services to impact levels.
- **problem_record(problem_id)** — for RCA and follow-up.
- **knowledge_articles(query)** — relevant troubleshooting guides.
- **monitoring_alerts(ci_id)** — recent alerts from monitoring tools.

## Tools for incident and problem actions

Tools are tightly scoped actions that the LLM can perform only after reasoning through prompts and resources.

### Incident tools

- **update_incident(incident_id, fields)** — update priority, assignment group, or notes.
- **add_incident_work_note(incident_id, note)** — document analysis or actions.
- **escalate_incident(incident_id, reason)** — escalate to major incident or resolver group.
- **resolve_incident(incident_id, resolution_code, notes)** — close with documented resolution.

### Problem tools

- **create_problem_from_incident(incident_id, summary)** — convert incident to problem.
- **add_problem_work_note(problem_id, note)** — document RCA progress.
- **propose_corrective_action(problem_id, action)** — log preventive measures.

## How the layers work together in real workflows

A typical incident flow looks like this:

### 1. User or system calls the prompt

`incident_triage("INC12345")`

### 2. LLM fetches resources

- incident_record
- incident_cis
- recent_changes
- service_impact_matrix

### 3. LLM applies triage logic

- classify severity
- identify business impact
- check for related changes
- determine if escalation is needed

### 4. LLM calls tools

- escalate_incident
- update_incident
- add_incident_work_note

### 5. If systemic issue detected

- create_problem_from_incident
- propose_corrective_action

This mirrors how a strong ITIL-aligned operations team behaves.

## A deeper layer: correlation and RCA logic

Incident and problem management benefit from encoded reasoning patterns:

- **Change correlation** — “If a CI has a change in the last 24 hours, evaluate it as a potential cause.”
- **Impact mapping** — “If the business service is Tier 1, severity cannot be lower than SEV2.”
- **RCA frameworks** — 5 Whys, fault tree analysis, causal chain mapping.
- **Noise reduction** — “If multiple incidents affect the same CI, propose a problem record.”

These become part of your prompts and resources, giving the LLM a structured, repeatable way to diagnose issues.
