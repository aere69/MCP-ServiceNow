from datetime import datetime
from typing import Dict, Any, List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("UnifiedITSM")

# ===================================================================
# STUB BACKENDS (replace with real ServiceNow / Jira / CMDB / etc.)
# ===================================================================

# ---------------------- Change Management ---------------------------

class ServiceNowChangeAPI:
    def get_change(self, change_id: str) -> Dict[str, Any]:
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
        return [
            {"ci": "PAYMENTS-API-01", "environment": "PROD", "tier": "Critical"},
            {"ci": "DB-PAYMENTS-01", "environment": "PROD", "tier": "Critical"},
        ]

    def add_work_note(self, change_id: str, note: str):
        print(f"[CHANGE] Note on {change_id}: {note}")

    def approve_change(self, change_id: str):
        print(f"[CHANGE] Approved {change_id}")

    def reject_change(self, change_id: str, reason: str):
        print(f"[CHANGE] Rejected {change_id}: {reason}")

    def escalate_change(self, change_id: str, reason: str):
        print(f"[CHANGE] Escalated {change_id}: {reason}")

change_api = ServiceNowChangeAPI()

def get_change_risk_rules() -> Dict[str, Any]:
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

# ---------------- Incident & Problem Management ---------------------

class ServiceNowIncidentAPI:
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
        print(f"[INC] Note on {incident_id}: {note}")

    def update_incident(self, incident_id: str, fields: Dict[str, Any]):
        print(f"[INC] Update {incident_id}: {fields}")

    def escalate_incident(self, incident_id: str, reason: str):
        print(f"[INC] Escalate {incident_id}: {reason}")

    def resolve_incident(self, incident_id: str, resolution_code: str, notes: str):
        print(f"[INC] Resolve {incident_id}: {resolution_code} - {notes}")

    def create_problem(self, incident_id: str, summary: str) -> str:
        problem_id = f"PRB{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        print(f"[PRB] {problem_id} created from {incident_id}: {summary}")
        return problem_id

    def get_problem(self, problem_id: str) -> Dict[str, Any]:
        return {
            "number": problem_id,
            "short_description": "Intermittent API failures",
            "description": "Root cause under investigation.",
            "state": "Analysis",
            "assignment_group": "Platform Engineering",
        }

incident_api = ServiceNowIncidentAPI()

# ---------------------- CMDB Governance -----------------------------

class CMDBAPI:
    def get_ci(self, ci_id: str) -> Dict[str, Any]:
        return {
            "sys_id": ci_id,
            "name": "PAYMENTS-API-01",
            "type": "Application",
            "environment": "PROD",
            "tier": "Critical",
            "owner": "Platform Engineering",
            "lifecycle": "In Use",
            "sys_updated_on": "2026-03-05 12:00",
            "attributes": {
                "ip_address": "10.0.0.10",
                "os": "Linux",
                "version": "2.3.1",
            },
        }

    def get_ci_relationships(self, ci_id: str) -> List[Dict[str, Any]]:
        return [
            {"source": ci_id, "target": "DB-PAYMENTS-01", "type": "depends_on"},
            {"source": "WEB-FRONTEND-01", "target": ci_id, "type": "calls"},
        ]

    def update_ci(self, ci_id: str, fields: Dict[str, Any]):
        print(f"[CMDB] Update CI {ci_id}: {fields}")

    def add_ci_relationship(self, ci_id: str, target_ci: str, relationship_type: str):
        print(f"[CMDB] Add relationship {ci_id} -({relationship_type})-> {target_ci}")

    def remove_ci_relationship(self, ci_id: str, target_ci: str):
        print(f"[CMDB] Remove relationship {ci_id} -> {target_ci}")

    def add_ci_work_note(self, ci_id: str, note: str):
        print(f"[CMDB] Note on {ci_id}: {note}")

cmdb_api = CMDBAPI()

def get_ci_policy_rules() -> Dict[str, Any]:
    return {
        "mandatory_fields_by_type": {
            "Application": ["name", "environment", "tier", "owner", "lifecycle"],
            "Database": ["name", "environment", "tier", "owner"],
        },
        "naming_conventions": {
            "Application": "^[A-Z0-9-]+$",
            "Database": "^DB-[A-Z0-9-]+$",
        },
        "environment_rules": {
            "PROD": {
                "require_owner": True,
                "require_relationships": True,
                "require_service_mapping": True,
            },
            "DEV": {
                "require_owner": False,
                "require_relationships": False,
                "require_service_mapping": False,
            },
        },
    }

def get_ci_data_quality_metrics(ci_id: str) -> Dict[str, Any]:
    return {
        "ci_id": ci_id,
        "completeness_score": 0.85,
        "accuracy_score": 0.8,
        "last_audit": "2026-02-28 10:00",
    }

def get_ci_service_mapping(ci_id: str) -> Dict[str, Any]:
    return {
        "ci_id": ci_id,
        "business_service": "Online Banking",
        "technical_service": "Payments Platform",
        "mapped": True,
    }

def get_cmdb_health_dashboard() -> Dict[str, Any]:
    return {
        "overall_completeness": 0.82,
        "overall_accuracy": 0.78,
        "last_full_audit": "2026-02-15 09:00",
        "high_risk_cis": 42,
    }

# ---------------------- Delivery / RAID -----------------------------

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

# ===================================================================
# RESOURCES (grouped by domain)
# ===================================================================

# -------- Change --------

@mcp.resource()
def change_record(change_id: str):
    record = change_api.get_change(change_id)
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
def change_cis(change_id: str):
    return change_api.get_change_cis(change_id)

@mcp.resource()
def change_risk_rules():
    return get_change_risk_rules()

@mcp.resource()
def deployment_calendar():
    return get_deployment_calendar()

# -------- Incident / Problem --------

@mcp.resource()
def incident_record(incident_id: str):
    return incident_api.get_incident(incident_id)

@mcp.resource()
def incident_cis(incident_id: str):
    return incident_api.get_incident_cis(incident_id)

@mcp.resource()
def recent_changes(ci_id: str):
    return incident_api.get_recent_changes(ci_id)

@mcp.resource()
def service_impact_matrix():
    return {
        "Online Banking": "Tier 1",
        "Payments": "Tier 1",
        "Internal Tools": "Tier 3",
    }

@mcp.resource()
def monitoring_alerts(ci_id: str):
    return [
        {"timestamp": "2026-03-06 14:55", "alert": "High latency detected"},
        {"timestamp": "2026-03-06 14:57", "alert": "Error rate spike"},
    ]

@mcp.resource()
def problem_record(problem_id: str):
    return incident_api.get_problem(problem_id)

# -------- CMDB --------

@mcp.resource()
def ci_record(ci_id: str):
    record = cmdb_api.get_ci(ci_id)
    return {
        "id": record["sys_id"],
        "name": record["name"],
        "type": record["type"],
        "environment": record["environment"],
        "tier": record["tier"],
        "owner": record["owner"],
        "lifecycle": record["lifecycle"],
        "last_updated": record["sys_updated_on"],
        "attributes": record["attributes"],
    }

@mcp.resource()
def ci_relationships(ci_id: str):
    return cmdb_api.get_ci_relationships(ci_id)

@mcp.resource()
def ci_policy_rules():
    return get_ci_policy_rules()

@mcp.resource()
def ci_service_mapping(ci_id: str):
    return get_ci_service_mapping(ci_id)

@mcp.resource()
def ci_data_quality_metrics(ci_id: str):
    return get_ci_data_quality_metrics(ci_id)

@mcp.resource()
def cmdb_health_dashboard():
    return get_cmdb_health_dashboard()

# -------- Delivery / RAID --------

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
def delivery_change_risk_feed(project_id: str):
    return get_change_risk_feed(project_id)

@mcp.resource()
def incident_trend_feed(project_id: str):
    return get_incident_trend_feed(project_id)

@mcp.resource()
def cmdb_impact_feed(project_id: str):
    return get_cmdb_impact_feed(project_id)

# ===================================================================
# TOOLS (grouped by domain)
# ===================================================================

# -------- Change --------

@mcp.tool()
def change_approve(change_id: str, rationale: str):
    change_api.add_work_note(change_id, f"Approved by LLM: {rationale}")
    change_api.approve_change(change_id)
    return {"status": "approved", "change_id": change_id, "rationale": rationale}

@mcp.tool()
def change_reject(change_id: str, rationale: str):
    change_api.add_work_note(change_id, f"Rejected by LLM: {rationale}")
    change_api.reject_change(change_id, rationale)
    return {"status": "rejected", "change_id": change_id, "rationale": rationale}

@mcp.tool()
def change_escalate(change_id: str, rationale: str):
    change_api.add_work_note(change_id, f"Escalated by LLM: {rationale}")
    change_api.escalate_change(change_id, rationale)
    return {"status": "escalated", "change_id": change_id, "rationale": rationale}

# -------- Incident / Problem --------

@mcp.tool()
def incident_update(incident_id: str, fields: Dict[str, Any]):
    incident_api.update_incident(incident_id, fields)
    return {"status": "updated", "incident_id": incident_id, "fields": fields}

@mcp.tool()
def incident_add_note(incident_id: str, note: str):
    incident_api.add_incident_work_note(incident_id, note)
    return {"status": "note_added", "incident_id": incident_id, "note": note}

@mcp.tool()
def incident_escalate(incident_id: str, reason: str):
    incident_api.escalate_incident(incident_id, reason)
    return {"status": "escalated", "incident_id": incident_id, "reason": reason}

@mcp.tool()
def incident_resolve(incident_id: str, resolution_code: str, notes: str):
    incident_api.resolve_incident(incident_id, resolution_code, notes)
    return {"status": "resolved", "incident_id": incident_id}

@mcp.tool()
def problem_create_from_incident(incident_id: str, summary: str):
    problem_id = incident_api.create_problem(incident_id, summary)
    return {"status": "problem_created", "problem_id": problem_id}

# -------- CMDB --------

@mcp.tool()
def ci_update(ci_id: str, fields: Dict[str, Any]):
    cmdb_api.update_ci(ci_id, fields)
    return {"status": "updated", "ci_id": ci_id, "fields": fields}

@mcp.tool()
def ci_add_relationship(ci_id: str, target_ci: str, relationship_type: str):
    cmdb_api.add_ci_relationship(ci_id, target_ci, relationship_type)
    return {
        "status": "relationship_added",
        "ci_id": ci_id,
        "target_ci": target_ci,
        "relationship_type": relationship_type,
    }

@mcp.tool()
def ci_remove_relationship(ci_id: str, target_ci: str):
    cmdb_api.remove_ci_relationship(ci_id, target_ci)
    return {"status": "relationship_removed", "ci_id": ci_id, "target_ci": target_ci}

@mcp.tool()
def ci_flag_for_review(ci_id: str, reason: str):
    cmdb_api.add_ci_work_note(ci_id, f"Flagged for review: {reason}")
    return {"status": "flagged", "ci_id": ci_id, "reason": reason}

# -------- Delivery / RAID --------

@mcp.tool()
def raid_create(
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
def raid_update(raid_id: str, fields: Dict[str, Any]):
    print(f"[RAID] Update {raid_id}: {fields}")
    return {"status": "updated", "raid_id": raid_id, "fields": fields}

@mcp.tool()
def raid_escalate(raid_id: str, reason: str):
    print(f"[RAID] Escalate {raid_id}: {reason}")
    return {"status": "escalated", "raid_id": raid_id, "reason": reason}

@mcp.tool()
def delivery_add_status_note(project_id: str, note: str):
    delivery_api.add_status_note(project_id, note)
    return {"status": "note_added", "project_id": project_id, "note": note}

@mcp.tool()
def delivery_log_decision(project_id: str, decision: str, rationale: str, owner: str):
    delivery_api.log_decision(project_id, decision, rationale, owner)
    return {
        "status": "decision_logged",
        "project_id": project_id,
        "decision": decision,
        "rationale": rationale,
        "owner": owner,
    }

# ===================================================================
# PROMPTS (grouped by domain)
# ===================================================================

# -------- Change --------

@mcp.prompt()
def change_assess(change_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a Change Manager. Evaluate risk, impact, readiness, approvals, "
                "and blackout conflicts. Be strict and evidence-based."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Assess change {change_id}. Use 'change_record', 'change_cis', "
                "'change_risk_rules', and 'deployment_calendar'. "
                "Recommend APPROVE, REJECT, or ESCALATE with rationale."
            ),
        },
    ]

# -------- Incident / Problem --------

@mcp.prompt()
def incident_triage(incident_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are an Incident Manager. Classify severity, assess impact, "
                "and decide whether escalation is required."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Triage incident {incident_id}. Use 'incident_record', 'incident_cis', "
                "'recent_changes', 'service_impact_matrix', and 'monitoring_alerts'. "
                "Recommend next actions and whether to escalate."
            ),
        },
    ]

@mcp.prompt()
def problem_rca(problem_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are performing root cause analysis. Use structured methods "
                "like 5 Whys and causal chain mapping."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Conduct RCA for problem {problem_id}. Use 'problem_record', "
                "'incident_cis', and 'recent_changes'. Summarise root cause and "
                "proposed corrective actions."
            ),
        },
    ]

# -------- CMDB --------

@mcp.prompt()
def ci_quality_review(ci_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a CMDB Governance Analyst. Evaluate CI completeness, accuracy, "
                "relationships, lifecycle, and ownership."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Review CI {ci_id}. Use 'ci_record', 'ci_relationships', "
                "'ci_policy_rules', 'ci_data_quality_metrics', and 'ci_service_mapping'. "
                "Highlight gaps and propose corrections."
            ),
        },
    ]

@mcp.prompt()
def cmdb_data_quality_report():
    return [
        {
            "role": "system",
            "content": (
                "You are generating a CMDB data quality report. Summarise health and "
                "highlight high-risk areas."
            ),
        },
        {
            "role": "user",
            "content": (
                "Use 'cmdb_health_dashboard' to produce a concise CMDB data quality report "
                "with key metrics and recommended actions."
            ),
        },
    ]

# -------- Delivery / RAID --------

@mcp.prompt()
def delivery_status_review(project_id: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a Delivery Lead. Assess scope, schedule, risks, issues, and "
                "dependencies. Provide a clear RAG and next actions."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Review delivery status for project {project_id}. Use 'project_overview', "
                "'sprint_board', 'raid_log', and 'release_calendar'. "
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
                "and dependencies, using ITSM and CMDB signals."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Review RAID for project {project_id}. Use 'raid_log', "
                "'delivery_change_risk_feed', 'incident_trend_feed', "
                "and 'cmdb_impact_feed'. Summarise top items and actions."
            ),
        },
    ]

# ===================================================================
# ENTRY POINT
# ===================================================================

if __name__ == "__main__":
    mcp.run()
