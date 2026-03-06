from datetime import datetime
from typing import Dict, Any, List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DeliveryRAID")

# -------------------------------------------------------------------
# Delivery / RAID stubs (replace with real integrations: Jira, SNOW, etc.)
# -------------------------------------------------------------------

class DeliveryAPI:
    def get_project_overview(self, project_id: str) -> Dict[str, Any]:
        return {
            "id": project_id,
            "name": "Payments Platform Modernisation",
            "sponsor": "CIO",
            "rag": "Amber",
            "scope": "Modernise payments platform and migrate to Azure.",
            "milestones": [
                {"id": "M1", "name": "Architecture Signed Off", "date": "2026-03-15", "status": "Complete"},
                {"id": "M2", "name": "UAT Start", "date": "2026-04-10", "status": "At Risk"},
                {"id": "M3", "name": "Go-Live", "date": "2026-05-01", "status": "On Track"},
            ],
        }

    def get_sprint_board(self, project_id: str) -> List[Dict[str, Any]]:
        return [
            {"id": "EPIC-1", "type": "Epic", "title": "API Gateway Migration", "status": "In Progress"},
            {"id": "STORY-101", "type": "Story", "title": "Implement retry logic", "status": "Blocked"},
            {"id": "STORY-102", "type": "Story", "title": "Update monitoring dashboards", "status": "In Progress"},
        ]

    def get_raid_log(self, project_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "id": "R-001",
                "type": "Risk",
                "title": "CMDB quality may delay cutover",
                "probability": "High",
                "impact": "High",
                "owner": "CMDB Lead",
                "status": "Open",
                "mitigation": "Complete CI validation before UAT start",
            },
            {
                "id": "I-003",
                "type": "Issue",
                "title": "Integration test environment unstable",
                "impact": "Medium",
                "owner": "Test Manager",
                "status": "In Progress",
            },
        ]

    def get_release_calendar(self, project_id: str) -> List[Dict[str, Any]]:
        return [
            {"id": "REL-2026-04-10", "name": "UAT Start", "date": "2026-04-10", "type": "UAT"},
            {"id": "REL-2026-05-01", "name": "Go-Live", "date": "2026-05-01", "type": "Production"},
        ]

    def add_status_note(self, project_id: str, note: str):
        print(f"[STATUS] {project_id}: {note}")

    def log_decision(self, project_id: str, decision: str, rationale: str, owner: str):
        print(f"[DECISION] {project_id}: {decision} ({owner}) - {rationale}")

delivery_api = DeliveryAPI()

# Cross-domain feeds (would be wired to other MCPs in reality)

def get_change_risk_feed(project_id: str) -> List[Dict[str, Any]]:
    return [
        {"change_id": "CHG12345", "risk": "High", "summary": "Payments API deployment near go-live"},
    ]

def get_incident_trend_feed(project_id: str) -> List[Dict[str, Any]]:
    return [
        {"service": "Online Banking", "sev1_last_30_days": 1, "sev2_last_30_days": 3},
    ]

def get_cmdb_impact_feed(project_id: str) -> List[Dict[str, Any]]:
    return [
        {"ci": "PAYMENTS-API-01", "tier": "Critical", "data_quality": "Medium"},
    ]

# -------------------------------------------------------------------
# Resources
# -------------------------------------------------------------------

@mcp.resource()
def project_overview(project_id: str):
    return delivery_api.get_project_overview(project_id)

@mcp.resource()
def sprint_board(project_id: str):
    return delivery_api.get_sprint_board(project_id)

@mcp.resource()
def raid_log(project_id: str):
    return delivery_api.get_raid_log(project_id)

@mcp.resource()
def release_calendar(project_id: str):
    return delivery_api.get_release_calendar(project_id)

@mcp.resource()
def change_risk_feed(project_id: str):
    return get_change_risk_feed(project_id)

@mcp.resource()
def incident_trend_feed(project_id: str):
    return get_incident_trend_feed(project_id)

@mcp.resource()
def cmdb_impact_feed(project_id: str):
    return get_cmdb_impact_feed(project_id)

# -------------------------------------------------------------------
# Tools
# -------------------------------------------------------------------

@mcp.tool()
def create_raid_item(
    project_id: str,
    item_type: str,
    title: str,
    description: str,
    impact: str,
    owner: str,
):
    raid_id = f"{item_type[0]}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    print(f"[RAID] {raid_id} ({project_id}) {item_type}: {title} - {impact} - {owner}")
    return {
        "status": "created",
        "raid_id": raid_id,
        "project_id": project_id,
        "type": item_type,
        "title": title,
        "description": description,
        "impact": impact,
        "owner": owner,
    }

@mcp.tool()
def update_raid_item(raid_id: str, fields: Dict[str, Any]):
    print(f"[RAID] Update {raid_id}: {fields}")
    return {"status": "updated", "raid_id": raid_id, "fields": fields}

@mcp.tool()
def escalate_raid_item(raid_id: str, reason: str):
    print(f"[RAID] Escalate {raid_id}: {reason}")
    return {"status": "escalated", "raid_id": raid_id, "reason": reason}

@mcp.tool()
def add_status_note(project_id: str, note: str):
    delivery_api.add_status_note(project_id, note)
    return {"status": "note_added", "project_id": project_id, "note": note}

@mcp.tool()
def propose_milestone_change(
    project_id: str,
    milestone_id: str,
    new_date: str,
    rationale: str,
):
    print(f"[MILESTONE] Proposal for {project_id} {milestone_id}: {new_date} - {rationale}")
    return {
        "status": "proposal_logged",
        "project_id": project_id,
        "milestone_id": milestone_id,
        "new_date": new_date,
        "rationale": rationale,
    }

@mcp.tool()
def log_decision(project_id: str, decision: str, rationale: str, owner: str):
    delivery_api.log_decision(project_id, decision, rationale, owner)
    return {
        "status": "decision_logged",
        "project_id": project_id,
        "decision": decision,
        "rationale": rationale,
        "owner": owner,
    }

# -------------------------------------------------------------------
# Prompts
# -------------------------------------------------------------------

@mcp.prompt()
def delivery_status_review(project_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a Delivery Lead. Assess scope, schedule, risks, issues, and "
                "dependencies. Provide a clear RAG status, key risks, and next actions."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Review delivery status for project {project_id}. "
                "Use 'project_overview', 'sprint_board', 'raid_log', and 'release_calendar'. "
                "Highlight key risks, blockers, and decisions needed."
            ),
        },
    ]

@mcp.prompt()
def raid_review(project_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are reviewing the RAID log. Identify the most critical risks, issues, "
                "and dependencies. Focus on impact to milestones and go-live."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Review the RAID log for project {project_id}. "
                "Use 'raid_log', 'change_risk_feed', 'incident_trend_feed', "
                "and 'cmdb_impact_feed' to inform your assessment."
            ),
        },
    ]

@mcp.prompt()
def dependency_analysis(project_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are analysing delivery dependencies. Identify cross-team, technical, "
                "and organisational dependencies that could impact milestones."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Analyse dependencies for project {project_id}. "
                "Use 'project_overview', 'sprint_board', and 'raid_log'. "
                "Highlight critical path items and dependency risks."
            ),
        },
    ]

@mcp.prompt()
def go_no_go_assessment(release_id: str, project_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are performing a Go/No-Go assessment. Consider delivery readiness, "
                "change risk, incident trends, and CMDB/CI risk. Be conservative and "
                "explicit about assumptions."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Assess Go/No-Go for release {release_id} in project {project_id}. "
                "Use 'project_overview', 'raid_log', 'change_risk_feed', "
                "'incident_trend_feed', and 'cmdb_impact_feed'. "
                "Provide a clear recommendation (GO, NO-GO, or GO WITH CONDITIONS) "
                "and rationale."
            ),
        },
    ]

@mcp.prompt()
def exec_summary(project_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are writing an executive summary. Be concise, outcome-focused, and "
                "explicit about risks, decisions, and asks."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Generate an executive summary for project {project_id}. "
                "Use 'project_overview', 'raid_log', and 'release_calendar'. "
                "Include: current RAG, key achievements, top 3 risks/issues, "
                "and decisions required."
            ),
        },
    ]

@mcp.prompt()
def risk_brainstorm(project_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are facilitating a risk identification session. Think broadly across "
                "technology, people, process, vendor, and regulatory dimensions."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Identify potential risks for upcoming phases of project {project_id}. "
                "Use 'project_overview', 'release_calendar', and any patterns from "
                "'change_risk_feed' and 'incident_trend_feed'. "
                "Propose risks in a structured list with probability, impact, and "
                "suggested owners."
            ),
        },
    ]

# -------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
