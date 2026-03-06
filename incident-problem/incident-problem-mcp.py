from datetime import datetime, timedelta
from typing import Dict, Any, List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("IncidentProblemManagement")

# -------------------------------------------------------------------
# ServiceNow + monitoring stubs (replace with real integrations)
# -------------------------------------------------------------------

class ServiceNowAPI:
    def get_incident(self, incident_id: str) -> Dict[str, Any]:
        return {
            "number": incident_id,
            "short_description": "Payments API returning 500 errors",
            "description": "Multiple customers report payment failures.",
            "impact": "2",
            "urgency": "2",
            "priority": "2",
            "state": "In Progress",
            "assignment_group": "Payments Support",
            "business_service": "Online Banking",
            "opened_at": "2026-03-06 15:00",
            "caller_id": "customer_support",
        }

    def get_incident_cis(self, incident_id: str) -> List[Dict[str, Any]]:
        return [
            {"ci": "PAYMENTS-API-01", "environment": "PROD", "tier": "Critical"},
            {"ci": "DB-PAYMENTS-01", "environment": "PROD", "tier": "Critical"},
        ]

    def get_recent_changes(self, ci_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "change_id": "CHG12345",
                "ci": ci_id,
                "implemented_at": "2026-03-06 13:00",
                "summary": "Deploy API version 2.3.1",
            }
        ]

    def add_incident_work_note(self, incident_id: str, note: str):
        print(f"[SNOW] Work note on {incident_id}: {note}")

    def update_incident(self, incident_id: str, fields: Dict[str, Any]):
        print(f"[SNOW] Update {incident_id}: {fields}")

    def escalate_incident(self, incident_id: str, reason: str):
        print(f"[SNOW] Escalate {incident_id}: {reason}")

    def resolve_incident(self, incident_id: str, resolution_code: str, notes: str):
        print(f"[SNOW] Resolve {incident_id}: {resolution_code} - {notes}")

    def create_problem(self, incident_id: str, summary: str) -> str:
        problem_id = f"PRB{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        print(f"[SNOW] Problem {problem_id} created from {incident_id}: {summary}")
        return problem_id

    def get_problem(self, problem_id: str) -> Dict[str, Any]:
        return {
            "number": problem_id,
            "short_description": "Intermittent API failures",
            "description": "Root cause under investigation.",
            "state": "Analysis",
            "assignment_group": "Platform Engineering",
        }

servicenow_api = ServiceNowAPI()

# -------------------------------------------------------------------
# Resources
# -------------------------------------------------------------------

@mcp.resource()
def incident_record(incident_id: str):
    return servicenow_api.get_incident(incident_id)

@mcp.resource()
def incident_cis(incident_id: str):
    return servicenow_api.get_incident_cis(incident_id)

@mcp.resource()
def recent_changes(ci_id: str):
    return servicenow_api.get_recent_changes(ci_id)

@mcp.resource()
def service_impact_matrix():
    return {
        "Online Banking": "Tier 1",
        "Payments": "Tier 1",
        "Internal Tools": "Tier 3",
    }

@mcp.resource()
def knowledge_articles(query: str):
    return [
        {"id": "KB001", "title": "API 500 error troubleshooting", "relevance": 0.9},
        {"id": "KB002", "title": "Database latency issues", "relevance": 0.7},
    ]

@mcp.resource()
def monitoring_alerts(ci_id: str):
    return [
        {"timestamp": "2026-03-06 14:55", "alert": "High latency detected"},
        {"timestamp": "2026-03-06 14:57", "alert": "Error rate spike"},
    ]

@mcp.resource()
def problem_record(problem_id: str):
    return servicenow_api.get_problem(problem_id)

# -------------------------------------------------------------------
# Tools
# -------------------------------------------------------------------

@mcp.tool()
def update_incident(incident_id: str, fields: Dict[str, Any]):
    servicenow_api.update_incident(incident_id, fields)
    return {"status": "updated", "incident_id": incident_id, "fields": fields}

@mcp.tool()
def add_incident_work_note(incident_id: str, note: str):
    servicenow_api.add_incident_work_note(incident_id, note)
    return {"status": "note_added", "incident_id": incident_id, "note": note}

@mcp.tool()
def escalate_incident(incident_id: str, reason: str):
    servicenow_api.escalate_incident(incident_id, reason)
    return {"status": "escalated", "incident_id": incident_id, "reason": reason}

@mcp.tool()
def resolve_incident(incident_id: str, resolution_code: str, notes: str):
    servicenow_api.resolve_incident(incident_id, resolution_code, notes)
    return {"status": "resolved", "incident_id": incident_id}

@mcp.tool()
def create_problem_from_incident(incident_id: str, summary: str):
    problem_id = servicenow_api.create_problem(incident_id, summary)
    return {"status": "problem_created", "problem_id": problem_id}

@mcp.tool()
def add_problem_work_note(problem_id: str, note: str):
    print(f"[SNOW] Problem note on {problem_id}: {note}")
    return {"status": "note_added", "problem_id": problem_id, "note": note}

@mcp.tool()
def propose_corrective_action(problem_id: str, action: str):
    print(f"[SNOW] Corrective action for {problem_id}: {action}")
    return {"status": "corrective_action_logged", "problem_id": problem_id, "action": action}

# -------------------------------------------------------------------
# Prompts
# -------------------------------------------------------------------

@mcp.prompt()
def incident_triage(incident_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are an Incident Manager. Classify severity, assess business impact, "
                "identify affected CIs, correlate with recent changes, and determine "
                "whether escalation is required. Use structured reasoning."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Triage incident {incident_id}. "
                "Fetch 'incident_record', 'incident_cis', 'recent_changes', "
                "'service_impact_matrix', and 'monitoring_alerts'. "
                "Recommend next actions and whether escalation is needed."
            ),
        },
    ]

@mcp.prompt()
def incident_diagnosis(incident_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are diagnosing an incident. Analyse symptoms, CI alerts, "
                "recent changes, and knowledge articles. Identify likely root causes."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Diagnose incident {incident_id}. "
                "Use 'incident_record', 'incident_cis', 'recent_changes', "
                "'monitoring_alerts', and 'knowledge_articles'."
            ),
        },
    ]

@mcp.prompt()
def incident_resolution_plan(incident_id: str):
    return [
        {
            "role": "system",
            "content": (
                "Create a structured resolution plan. Include immediate actions, "
                "rollback options, communication steps, and validation checks."
            ),
        },
        {
            "role": "user",
            "content": f"Generate a resolution plan for incident {incident_id}.",
        },
    ]

@mcp.prompt()
def problem_identification(incident_id: str):
    return [
        {
            "role": "system",
            "content": (
                "Determine whether this incident indicates a deeper systemic issue. "
                "Consider recurrence, CI patterns, and recent changes."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Assess whether incident {incident_id} should become a problem record. "
                "Use 'incident_record', 'incident_cis', and 'recent_changes'."
            ),
        },
    ]

@mcp.prompt()
def problem_root_cause_analysis(problem_id: str):
    return [
        {
            "role": "system",
            "content": (
                "Perform root cause analysis using structured methods such as 5 Whys "
                "and causal chain mapping. Identify contributing factors."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Conduct RCA for problem {problem_id}. "
                "Use 'problem_record', 'incident_cis', 'recent_changes', and 'monitoring_alerts'."
            ),
        },
    ]

@mcp.prompt()
def problem_recommendations(problem_id: str):
    return [
        {
            "role": "system",
            "content": (
                "Recommend corrective and preventive actions. "
                "Focus on long-term stability and operational resilience."
            ),
        },
        {
            "role": "user",
            "content": f"Provide recommendations for problem {problem_id}.",
        },
    ]

# -------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
