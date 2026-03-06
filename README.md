# MCP-ServiceNow

MCP ServiceNow Servers

A complete FastMCP architecture for a **ServiceNow‑focused Transformation PM toolkit** works best when prompts, resources, and tools are designed as a single operating model. The goal is to let the LLM behave like a governance‑aligned delivery partner that can read data, apply structured reasoning, and trigger actions safely.

## Architecture overview

The system works as three coordinated layers:

- **Prompts** define how the LLM thinks (governance, structure, reasoning).
- **Resources** provide the data (records, CMDB, workflows, configs).
- **Tools** perform actions (update, create, approve, transform).

The LLM becomes the orchestrator that moves between these layers.

## Prompts: governance, structure, and reasoning

Prompts act as reusable “playbooks” that enforce consistent behaviour across workflows. They are the backbone of your governance model.

### Core prompt categories

- **Assessment prompts**
  - Change risk assessment
  - Incident severity classification
  - CMDB CI impact analysis

- **Governance prompts**
  - RAID evaluation
  - Go/No‑Go readiness
  - Compliance and audit checks

- **OCM prompts**
  - Stakeholder impact analysis
  - Communications drafting
  - Training needs assessment

- **Delivery prompts**
  - Sprint planning
  - Dependency mapping
  - Executive summary generation

**Example:** Change assesment prompt

```py
@mcp.prompt()
def assess_change(change_id: str):
    return [
        {"role": "system", "content": "You are a Change Manager. Use ITIL and organisational governance rules."},
        {"role": "user", "content": f"Assess change {change_id}. Fetch the 'change_record' resource and evaluate risk, impact, and readiness."}
    ]
```

This prompt tells the LLM how to think and what steps to follow.

## Resources: structured access to ServiceNow and delivery data

Resources expose the data the LLM needs to make decisions. They are read‑only, safe, and predictable.

### Resource categories

- **ServiceNow data**
  - Change records
  - Incident records
  - CMDB CIs
  - Knowledge articles
  - HRSD cases

- **Delivery data**
  - RAID logs
  - Sprint boards
  - Architecture diagrams
  - Operating model documents

- **Configuration resources**
  - Risk scoring rules
  - Approval matrices
  - Deployment windows

**Example:** Change record resource

```py
@mcp.resource()
def change_record(change_id: str):
    return servicenow_api.get_change(change_id)
```

This gives the LLM the data it needs to follow the prompt’s instructions.

## Tools: controlled actions and workflow execution

Tools are the “levers” the LLM can pull. They perform actions that change state or trigger workflows.

### Tool categories

- **ServiceNow actions**
  - Approve/reject change
  - Update incident
  - Create problem record
  - Update CMDB CI

- **Delivery actions**
  - Add RAID item
  - Update sprint task
  - Generate status report

- **OCM actions**
  - Draft communication
  - Create training plan
  - Log stakeholder feedback

**Example:** Approve change tool

```py
@mcp.tool()
def approve_change(change_id: str):
    return servicenow_api.approve(change_id)
```

Tools are only called after the LLM has followed the prompt and analysed the resource.

## How the three layers work together in a real workflow

A typical governance‑aligned workflow looks like this:

1. **Client requests a prompt**

    The user or system calls:

    ```py
    assess_change(change_id="CHG12345")
    ```

    The prompt returns structured instructions.

2. **LLM fetches resources**

    The LLM reads:

    ```py
    change_record("CHG12345")
    cmdb_ci("CI001")
    risk_rules()
    ```

    It now has the data.

3. **LLM applies governance logic**

    Using the prompt’s instructions, the LLM:
    - evaluates risk
    - checks dependencies
    - reviews CI impact
    - checks blackout windows
    - identifies missing approvals

4. **LLM decides whether to call a tool**

    If the change is compliant and low‑risk, it may call:

    ```py
    approve_change("CHG12345")
    ```

    If not, it may call:

    ```py
    create_raid_item("Missing test evidence for CHG12345")
    ```

    This is where your governance and delivery expertise becomes encoded into the system.

## Recommended architecture

**Layer 1: Prompts (thinking)**

- Change assessment
- Incident triage
- CMDB impact analysis
- Governance checks
- RAID evaluation
- Executive summary generation
- OCM impact analysis

**Layer 2: Resources (data)**

- Change/incident/problem records
- CMDB CIs and relationships
- Deployment calendars
- Approval matrices
- Risk scoring rules
- Sprint boards
- RAID logs

**Layer 3: Tools (actions)**

- Approve/reject change
- Update incident
- Create problem
- Add RAID item
- Update sprint task
- Generate report text

## A non‑obvious insight

The real power comes when prompts teach the LLM when to use tools and when not to.
For example:

- “Only approve a change if all mandatory fields are present, test evidence is attached, and CI impact is low.”

- “If risk is medium or high, create a RAID item instead of approving.”

- “If a CI is missing relationships, request CMDB update rather than proceeding.”

This is how you encode governance and reduce operational risk.
