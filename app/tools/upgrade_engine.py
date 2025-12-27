def generate_upgrade_plan(feedback=None):
    # Turn expert feedback into a concrete upgrade plan (high level)
    plan = [
        {
            "id": "upgrade-1",
            "title": "Enforce per-user data isolation across inventory endpoints",
            "description": "Filter inventories by the active owner_id across list/add/edit flows; prevent cross-user data exposure.",
            "priority": "high",
            "patches": [
                "Update /inventory GET to filter by session current_owner_id",
                "Update /inventory/add to assign owner_id from session when not provided",
                "Update /inventory/edit to preserve owner_id when not provided",
                "Add server-side checks to ensure item.owner_id matches current_owner_id on read",
            ],
        },
        {
            "id": "upgrade-2",
            "title": "Persist current user context across app session",
            "description": "Store active owner_id in user session and reference it in relevant endpoints.",
            "priority": "high",
            "patches": [
                "Set session['current_owner_id'] in /home when customer_id provided",
                "Read session['current_owner_id'] in inventory/api endpoints as default owner",
            ],
        },
        {
            "id": "upgrade-3",
            "title": "Inventory audit trail",
            "description": "Log inventory mutations to an audit table for traceability.",
            "priority": "medium",
            "patches": [
                "Add InventoryAudit model and relationship",
                "Insert audit row on inventory create/update/delete",
            ],
        },
        {
            "id": "upgrade-4",
            "title": "Targeted tests for per-user inventory",
            "description": "Add unit/integration tests for multi-user inventory flows.",
            "priority": "medium",
            "patches": [
                "Add tests for /home per-user inventory loading",
                "Add tests for /inventory with owner scoping",
            ],
        },
        {
            "id": "upgrade-5",
            "title": "Documentation & handoff artifacts",
            "description": "Add release notes and upgrade map to document persona-driven upgrades.",
            "priority": "low",
            "patches": [
                "Add RELEASE_NOTES/docs describing upgrades",
                "Provide a one-page upgrade plan for handoff",
            ],
        },
    ]
    return plan
