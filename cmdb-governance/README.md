# CMDB Governance - MCP working server

CMDB governance works best when it’s treated as a control system, not a data store. In a FastMCP context, that means giving the LLM three coordinated capabilities:

- **Prompts** that enforce governance logic (completeness, accuracy, relationships, compliance).
- **Resources** that expose CI data, relationships, ownership, and policy rules.
- **Tools** that allow safe, auditable corrections or escalations.

This mirrors how a strong configuration management function operates in real programmes: structured, evidence‑based, and aligned with operational resilience.

## CMDB governance responsibilities

A well‑designed CMDB governance layer supports four core responsibilities:

- **Data quality** — completeness, accuracy, consistency, freshness.
- **Relationship integrity** — upstream/downstream dependencies, service mapping.
- **Policy compliance** — naming standards, lifecycle states, ownership.
- **Operational readiness** — impact analysis, change correlation, risk detection.

FastMCP is ideal for this because it lets you encode these rules into prompts and tools that the LLM must follow.

## Prompts for CMDB governance

Prompts act as reusable governance playbooks. They define how the LLM should evaluate CIs, relationships, and compliance.

### Key prompts

- **ci_quality_review** — completeness, accuracy, lifecycle, ownership.
- **ci_relationship_validation** — upstream/downstream dependencies, service mapping gaps.
- **ci_policy_compliance** — naming standards, mandatory attributes, environment rules.
- **ci_risk_assessment** — operational risk based on CI tier, dependencies, and recent changes.
- **cmdb_service_map_review** — validate service maps for correctness and completeness.
- **cmdb_data_quality_report** — summarise issues across a set of CIs.

## Resources for CMDB governance

Resources provide structured, read‑only data that the LLM uses to evaluate compliance and quality.

### Recommended resources

- **ci_record(ci_id)** — core CI attributes: name, type, environment, owner, lifecycle, last updated.
- **ci_relationships(ci_id)** — upstream/downstream dependencies.
- **ci_policy_rules()** — naming standards, mandatory fields, lifecycle rules.
- **ci_service_mapping(ci_id)** — business service, technical service, application mapping.
- **recent_changes(ci_id)** — changes affecting the CI (useful for risk and accuracy checks).
- **ci_data_quality_metrics(ci_id)** — completeness score, accuracy score, last audit date.
- **ci_ownership_matrix()** — who owns what (platform, service, business).
- **cmdb_health_dashboard()** — aggregated quality metrics.

## Tools for CMDB governance

Tools allow the LLM to perform safe, auditable corrections or escalations.

### CI correction tools

- **update_ci(ci_id, fields)** — update attributes (owner, lifecycle, environment).
- **add_ci_relationship(ci_id, target_ci, relationship_type)** — add missing dependencies.
- **remove_ci_relationship(ci_id, target_ci)** — remove invalid links.
- **flag_ci_for_review(ci_id, reason)** — escalate to human governance.
- **add_ci_work_note(ci_id, note)** — document governance findings.

### Service mapping tools

- **update_service_mapping(ci_id, service)** — correct business/technical service.
- **create_service_map_gap(ci_id, description)** — log missing relationships.

### Data quality tools

- **log_data_quality_issue(ci_id, issue, severity)** — track governance issues.
- **request_ci_owner_update(ci_id, message)** — notify owner of required corrections.

## How the layers work together in real CMDB governance

A typical CI review flow looks like this:

### 1. User or system calls the prompt

`ci_quality_review("CI001234")`

### 2. LLM fetches resources

- ci_record
- ci_relationships
- ci_policy_rules
- recent_changes
- ci_data_quality_metrics

### 3. LLM applies governance logic

- Are mandatory fields present?
- Is the CI in the correct lifecycle state?
- Are relationships complete and accurate?
- Does the CI comply with naming standards?
- Is the owner correct?
- Are there recent changes that contradict CI attributes?

### 4. LLM calls tools

- update_ci
- add_ci_relationship
- log_data_quality_issue
- request_ci_owner_update

### 4. If systemic issues detected

- escalate to governance
- create service map gap
- propose corrective actions

This mirrors how a mature CMDB governance function operates.

## A deeper layer: governance rules encoded as resources

The real power comes from encoding your governance rules into structured resources:

- Mandatory fields by CI class
- Allowed lifecycle transitions
- Naming conventions
- Environment rules (e.g., PROD CIs must have owner + relationships)
- Tiering rules (Tier 1 must have upstream/downstream mapping)
- Data freshness rules (must be updated every X days)

These rules become the backbone of your prompts.
