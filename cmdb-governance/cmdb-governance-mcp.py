from datetime import datetime
from typing import Dict, Any, List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CMDBGovernance")

# -------------------------------------------------------------------
# CMDB stubs (replace with real ServiceNow / CMDB integrations)
# -------------------------------------------------------------------

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
        print(f"[CMDB] Work note on {ci_id}: {note}")

cmdb_api = CMDBAPI()

# -------------------------------------------------------------------
# Governance rules (could come from config/DB in real life)
# -------------------------------------------------------------------

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
        "lifecycle_rules": {
            "In Use": ["owner", "environment", "tier"],
            "Retired": [],
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

def get_ci_ownership_matrix() -> Dict[str, Any]:
    return {
        "Application": "Platform Engineering",
        "Database": "Database Operations",
        "Infrastructure": "Infrastructure Team",
    }

def get_cmdb_health_dashboard() -> Dict[str, Any]:
    return {
        "overall_completeness": 0.82,
        "overall_accuracy": 0.78,
        "last_full_audit": "2026-02-15 09:00",
        "high_risk_cis": 42,
    }

# -------------------------------------------------------------------
# Resources
# -------------------------------------------------------------------

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
def ci_ownership_matrix():
    return get_ci_ownership_matrix()

@mcp.resource()
def cmdb_health_dashboard():
    return get_cmdb_health_dashboard()

# -------------------------------------------------------------------
# Tools
# -------------------------------------------------------------------

@mcp.tool()
def update_ci(ci_id: str, fields: Dict[str, Any]):
    """
    Update CI attributes (owner, lifecycle, environment, etc.).
    Use only after a clear governance decision.
    """
    cmdb_api.update_ci(ci_id, fields)
    return {"status": "updated", "ci_id": ci_id, "fields": fields}

@mcp.tool()
def add_ci_relationship(ci_id: str, target_ci: str, relationship_type: str):
    """
    Add a missing relationship between CIs.
    """
    cmdb_api.add_ci_relationship(ci_id, target_ci, relationship_type)
    return {
        "status": "relationship_added",
        "ci_id": ci_id,
        "target_ci": target_ci,
        "relationship_type": relationship_type,
    }

@mcp.tool()
def remove_ci_relationship(ci_id: str, target_ci: str):
    """
    Remove an invalid relationship between CIs.
    """
    cmdb_api.remove_ci_relationship(ci_id, target_ci)
    return {
        "status": "relationship_removed",
        "ci_id": ci_id,
        "target_ci": target_ci,
    }

@mcp.tool()
def flag_ci_for_review(ci_id: str, reason: str):
    """
    Flag a CI for human governance review.
    """
    cmdb_api.add_ci_work_note(ci_id, f"Flagged for review: {reason}")
    return {"status": "flagged", "ci_id": ci_id, "reason": reason}

@mcp.tool()
def add_ci_work_note(ci_id: str, note: str):
    """
    Add a governance work note to the CI.
    """
    cmdb_api.add_ci_work_note(ci_id, note)
    return {"status": "note_added", "ci_id": ci_id, "note": note}

@mcp.tool()
def log_data_quality_issue(ci_id: str, issue: str, severity: str):
    """
    Log a data quality issue for tracking and remediation.
    """
    issue_id = f"DQ-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    print(f"[DQ] {issue_id} for {ci_id} ({severity}): {issue}")
    return {
        "status": "dq_issue_logged",
        "issue_id": issue_id,
        "ci_id": ci_id,
        "issue": issue,
        "severity": severity,
    }

@mcp.tool()
def request_ci_owner_update(ci_id: str, message: str):
    """
    Request the CI owner (or default owner) to update CI details.
    """
    cmdb_api.add_ci_work_note(ci_id, f"Owner update requested: {message}")
    return {"status": "owner_update_requested", "ci_id": ci_id, "message": message}

# -------------------------------------------------------------------
# Prompts
# -------------------------------------------------------------------

@mcp.prompt()
def ci_quality_review(ci_id: str):
    """
    Review CI completeness, accuracy, lifecycle, ownership, and relationships.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a CMDB Governance Analyst. Evaluate CI completeness, accuracy, "
                "relationships, lifecycle state, and ownership. Identify gaps and propose "
                "corrective actions. Use structured, evidence-based reasoning."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Review CI {ci_id}. "
                "Fetch 'ci_record', 'ci_relationships', 'ci_policy_rules', "
                "'ci_data_quality_metrics', and 'ci_service_mapping'. "
                "Recommend corrections and whether to flag for review or log data quality issues."
            ),
        },
    ]

@mcp.prompt()
def ci_relationship_validation(ci_id: str):
    """
    Validate upstream/downstream relationships and service mapping.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are validating CI relationships. Check for missing or incorrect "
                "upstream/downstream dependencies and service mappings. Focus on impact "
                "to change, incident, and problem management."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Validate relationships for CI {ci_id}. "
                "Use 'ci_record', 'ci_relationships', and 'ci_service_mapping'. "
                "Identify missing or incorrect relationships and propose corrections."
            ),
        },
    ]

@mcp.prompt()
def ci_policy_compliance(ci_id: str):
    """
    Check CI against naming standards, mandatory attributes, and lifecycle rules.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are checking CI policy compliance. Validate naming conventions, "
                "mandatory attributes, lifecycle rules, and environment-specific requirements."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Check policy compliance for CI {ci_id}. "
                "Use 'ci_record', 'ci_policy_rules', and 'ci_ownership_matrix'. "
                "Highlight non-compliance and suggest specific updates."
            ),
        },
    ]

@mcp.prompt()
def ci_risk_assessment(ci_id: str):
    """
    Assess operational risk based on CI tier, dependencies, and data quality.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are assessing operational risk for a CI. Consider tier, environment, "
                "relationships, data quality, and service mapping. Focus on potential impact "
                "to availability, change risk, and incident response."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Assess risk for CI {ci_id}. "
                "Use 'ci_record', 'ci_relationships', 'ci_data_quality_metrics', "
                "and 'ci_service_mapping'. Provide a clear risk rating and rationale."
            ),
        },
    ]

@mcp.prompt()
def cmdb_service_map_review(ci_id: str):
    """
    Review service mapping for a CI.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are reviewing service mapping. Ensure the CI is correctly mapped to "
                "business and technical services, and that dependencies reflect reality."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Review service mapping for CI {ci_id}. "
                "Use 'ci_record', 'ci_service_mapping', and 'ci_relationships'. "
                "Identify gaps or inconsistencies and propose corrections."
            ),
        },
    ]

@mcp.prompt()
def cmdb_data_quality_report():
    """
    Summarise CMDB data quality and highlight key issues.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are generating a CMDB data quality report. Summarise overall health, "
                "highlight high-risk areas, and propose governance actions."
            ),
        },
        {
            "role": "user",
            "content": (
                "Generate a CMDB data quality report using 'cmdb_health_dashboard'. "
                "Provide key metrics, risks, and recommended actions."
            ),
        },
    ]

# -------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
