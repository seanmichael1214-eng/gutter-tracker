class Expert:
    def __init__(self, name, specialty, notes, recommendations):
        self.name = name
        self.specialty = specialty
        self.notes = notes
        self.recommendations = recommendations


def run_expert_review():
    # Five gutter expert personas (internal, not exposed in UI)
    experts = [
        Expert(
            name="Alex the Architect",
            specialty="Data & Isolation",
            notes="Prioritizes per-user data boundaries and safe defaults.",
            recommendations=[
                "Enforce per-user inventory scoping across all endpoints.",
                "Default to current_owner_id in inventory add/edit when owner not specified.",
                "Add an audit trail for inventory mutations.",
            ],
        ),
        Expert(
            name="Bea the Builder",
            specialty="UX & Flow",
            notes="Wants clear multi-user navigation and quick switches.",
            recommendations=[
                "Enhance top navigation to cycle through user tabs with distinct colors.",
                "Ensure /home loads quickly for any selected user.",
            ],
        ),
        Expert(
            name="Cara the Compliance Lead",
            specialty="Security & Audit",
            notes="Looks for traceability and access controls.",
            recommendations=[
                "Audit logging for inventory actions.",
                "Validate ownership boundaries everywhere data is read or written.",
            ],
        ),
        Expert(
            name="Dana the DevOps",
            specialty="Reliability & Testing",
            notes="Pushes for test coverage and resilience.",
            recommendations=[
                "Add unit/integration tests for per-user inventory flows.",
                "Add CI hooks to validate patches on patch branch.",
            ],
        ),
        Expert(
            name="Eli the Economist",
            specialty="Performance & Documentation",
            notes="Wants lean queries and clear docs.",
            recommendations=[
                "Index owner_id on inventories for faster lookups.",
                "Document upgrade plan and rollback steps in RELEASE_NOTES.",
            ],
        ),
    ]

    results = []
    for e in experts:
        results.append({
            "name": e.name,
            "specialty": e.specialty,
            "notes": e.notes,
            "recommendations": e.recommendations,
        })
    return results
