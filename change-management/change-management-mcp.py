from datetime import datetime
from typing import List, Dict, Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ChangeManagement")


# -------------------------------------------------------------------
# ServiceNow + data access stubs (replace with real integrations)
# -------------------------------------------------------------------

class ServiceNowAPI:
    def get_change(self, change_id: str) -> Dict[str, Any]:
        # TODO: Replace with real ServiceNow call
        return {
            "number": change_id,
            "type": "Normal",
            "category": "Application",
            "risk": "Medium",
            "state": "Assess",
            "implementation_plan": "Deploy version 2.3.1 via standard pipeline.",
            "backout_plan": "Rollback to version 2.3.0.",
            "test_evidence": True,
            "start_date": "2026-03-10 20:00",
            "end_date": "2026-03-10 21:00",
            "business_service": "Online Banking",
            "assignment_group": "Payments Platform",
            "approvals": [
                {"role": "CAB", "status": "approved"},
                {"role": "Service Owner", "status": "approved"},
            ],
        }

    def get_change_cis(self, change_id: str) -> List[Dict[str, Any]]:
        # TODO: Replace with real CMDB relationship query
        return [
            {"ci": "PAYMENTS-API-01", "environment": "PROD", "tier": "Critical"},
            {"ci": "DB-PAYMENTS-01", "environment": "PROD", "tier": "Critical"},
        ]

    def add_work_note(self, change_id: str, note: str) -> None:
        # TODO: Replace with real ServiceNow work note call
        print(f"[SNOW] Work note on {change_id}: {note}")

    def approve_change(self, change_id: str) -> None:
        # TODO: Replace with real approval call
        print(f"[SNOW] Change {change_id} approved")

    def reject_change(self, change_id: str, reason: str) -> None:
        # TODO: Replace with real rejection call
        print(f"[SNOW] Change {change_id} rejected: {reason}")

    def escalate_change(self, change_id: str, reason: str) -> None:
        # TODO: Replace with real escalation call
        print(f"[SNOW] Change {change_id} escalated: {reason}")

servicenow_api = ServiceNowAPI()


def get_risk_rules() -> Dict[str, Any]:
    # In reality this might come from a config repo or DB
    return {
        "high_risk_conditions": [
            "environment == 'PROD' and tier == 'Critical'",
        ],
        "mandatory_fields": [
            "implementation_plan",
            "backout_plan",
            "test_evidence_present",
        ],
    }


def get_deployment_calendar() -> Dict[str, Any]:
    # Example blackout window
    return {
        "blackouts": [
            {
                "name": "Month-end freeze",
                "start": "2026-03-30 00:00",
                "end": "2026-04-02 23:59",
                "scope": "ALL_PROD",
            }
        ]
    }


# -------------------------------------------------------------------
# Resources: read-only data for the LLM
# -------------------------------------------------------------------

@mcp.resource()
def change_record(change_id: str) -> Dict[str, Any]:
    """
    Structured change record for the given ID.
    """
    record = servicenow_api.get_change(change_id)
    return {
        "id": record["number"],
        "type": record["type"],
        "category": record["category"],
        "risk": record["risk"],
        "state": record["state"],
        "implementation_plan": record["implementation_plan"],
        "backout_plan": record["backout_plan"],
        "test_evidence_present": bool(record.get("test_evidence")),
        "requested_start": record["start_date"],
        "requested_end": record["end_date"],
        "business_service": record["business_service"],
        "assignment_group": record["assignment_group"],
        "approvals": record["approvals"],
    }


@mcp.resource()
def change_cis(change_id: str) -> List[Dict[str, Any]]:
    """
    CIs affected by the change.
    """
    return servicenow_api.get_change_cis(change_id)


@mcp.resource()
def risk_rules() -> Dict[str, Any]:
    """
    Organisation-specific risk rules.
    """
    return get_risk_rules()


@mcp.resource()
def deployment_calendar(date: str | None = None) -> Dict[str, Any]:
    """
    Deployment windows and blackout periods.
    Optionally filter by date (YYYY-MM-DD).
    """
    cal = get_deployment_calendar()
    if date:
        # You could filter blackouts by date here if needed
        _ = datetime.strptime(date, "%Y-%m-%d")
    return cal


# -------------------------------------------------------------------
# Tools: controlled actions
# -------------------------------------------------------------------

@mcp.tool()
def approve_change(change_id: str, rationale: str) -> Dict[str, Any]:
    """
    Approve a change with documented rationale.
    Only call this if all governance checks pass.
    """
    servicenow_api.add_work_note(change_id, f"Approved by LLM: {rationale}")
    servicenow_api.approve_change(change_id)
    return {"status": "approved", "change_id": change_id, "rationale": rationale}


@mcp.tool()
def reject_change(change_id: str, rationale: str) -> Dict[str, Any]:
    """
    Reject a change with documented rationale.
    """
    servicenow_api.add_work_note(change_id, f"Rejected by LLM: {rationale}")
    servicenow_api.reject_change(change_id, rationale)
    return {"status": "rejected", "change_id": change_id, "rationale": rationale}


@mcp.tool()
def escalate_change(change_id: str, rationale: str) -> Dict[str, Any]:
    """
    Escalate a change for human review.
    """
    servicenow_api.add_work_note(change_id, f"Escalated by LLM: {rationale}")
    servicenow_api.escalate_change(change_id, rationale)
    return {"status": "escalated", "change_id": change_id, "rationale": rationale}


@mcp.tool()
def create_raid_item(title: str, description: str, risk_level: str) -> Dict[str, Any]:
    """
    Create a RAID item for tracking governance or delivery risk.
    """
    # TODO: integrate with your RAID store (Jira, Planner, SNOW, etc.)
    raid_id = f"RAID-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    print(f"[RAID] {raid_id}: {title} ({risk_level}) - {description}")
    return {
        "raid_id": raid_id,
        "title": title,
        "description": description,
        "risk_level": risk_level,
    }


@mcp.tool()
def request_more_info(change_id: str, message: str) -> Dict[str, Any]:
    """
    Request more information from the change owner.
    """
    servicenow_api.add_work_note(change_id, f"Info requested by LLM: {message}")
    return {"status": "info_requested", "change_id": change_id, "message": message}


# -------------------------------------------------------------------
# Prompts: governance playbooks
# -------------------------------------------------------------------

@mcp.prompt()
def assess_change(change_id: str):
    """
    Full risk/impact/readiness assessment for a change.

    The LLM MUST:
    - Fetch 'change_record(change_id)'
    - Fetch 'change_cis(change_id)'
    - Fetch 'risk_rules()'
    - Fetch 'deployment_calendar()'
    - Evaluate: risk, impact, approvals, blackout windows, test evidence, rollback
    - Decide: APPROVE, REJECT, or ESCALATE
    - If REJECT or ESCALATE, consider creating a RAID item and/or requesting more info
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a Change Manager following ITIL and organisational governance. "
                "Be strict, evidence-based, and risk-aware. "
                "You must explain your reasoning clearly before calling any tools."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Assess change {change_id}. "
                "Use the available resources and only call tools once your assessment is complete."
            ),
        },
    ]


@mcp.prompt()
def pre_implementation_check(change_id: str):
    """
    Final pre-implementation check before the change window.

    The LLM MUST:
    - Confirm implementation and backout plans are clear and complete
    - Confirm test evidence is present and adequate
    - Confirm no blackout window conflicts
    - Confirm approvals are complete
    - Decide whether to proceed, delay, or escalate
    """
    return [
        {
            "role": "system",
            "content": (
                "You are performing a pre-implementation check for a change. "
                "Your goal is to prevent avoidable incidents by catching gaps early."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Perform a pre-implementation check for change {change_id}. "
                "Use 'change_record', 'change_cis', 'risk_rules', and 'deployment_calendar'. "
                "If there are gaps, consider 'reject_change', 'request_more_info', or 'create_raid_item'."
            ),
        },
    ]


@mcp.prompt()
def post_implementation_review(change_id: str):
    """
    Post-implementation review (PIR) for a completed change.

    The LLM SHOULD:
    - Review the change record and any incident/problem links (if available as resources)
    - Identify what went well, what didn't, and lessons learned
    - Suggest follow-up actions (e.g., RAID items, documentation updates)
    """
    return [
        {
            "role": "system",
            "content": (
                "You are conducting a Post-Implementation Review (PIR) for a change. "
                "Be objective, constructive, and focused on learning and risk reduction."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Conduct a PIR for change {change_id}. "
                "Summarise outcomes, issues, and recommendations. "
                "If you identify ongoing risks, consider creating a RAID item."
            ),
        },
    ]


# -------------------------------------------------------------------
# Entry point (if you want to run as a standalone MCP server)
# -------------------------------------------------------------------

if __name__ == "__main__":
    # This will depend on how you're hosting/running FastMCP.
    # Often it's something like:
    #
    #   mcp.run()
    #
    # Check FastMCP docs for the exact server start pattern.
    mcp.run()
