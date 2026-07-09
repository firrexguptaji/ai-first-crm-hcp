# Entity Relationship Diagram (ERD)

## Overview

The AI-First CRM HCP Module is built around two primary entities:

- Healthcare Professional (HCP)
- Interaction

A Healthcare Professional can have multiple interactions, while each interaction belongs to exactly one Healthcare Professional.

---

## Entity Relationship

```text
                        +----------------------------------+
                        |      HealthcareProfessional      |
                        +----------------------------------+
                        | PK  id : UUID                    |
                        | first_name : String              |
                        | last_name : String               |
                        | specialization : String          |
                        | organization : String            |
                        | email : String                   |
                        | phone : String                   |
                        | created_at : Timestamp           |
                        | updated_at : Timestamp           |
                        +----------------------------------+
                                      │
                                      │ 1
                                      │
                                      │
                                      │ *
                        +----------------------------------+
                        |          Interaction            |
                        +----------------------------------+
                        | PK  id : UUID                   |
                        | FK  hcp_id : UUID               |
                        | interaction_date : Timestamp    |
                        | channel : Enum                 |
                        | raw_notes : Text               |
                        | summary : Text                 |
                        | sentiment : Enum               |
                        | products_discussed : JSONB     |
                        | follow_up_required : Boolean   |
                        | follow_up_date : Date          |
                        | created_at : Timestamp         |
                        | updated_at : Timestamp         |
                        +----------------------------------+
```

---

## Relationship

### Healthcare Professional

- One Healthcare Professional can have many interactions.

### Interaction

- Each interaction belongs to exactly one Healthcare Professional.

---

## Cardinality

```text
HealthcareProfessional (1)
            │
            │
            └──────────────< Interaction (Many)
```

---

## Primary Keys

### Healthcare Professional

- `id`

### Interaction

- `id`

---

## Foreign Keys

### Interaction

- `hcp_id` → `HealthcareProfessional.id`

---

## Design Notes

The schema intentionally consists of only two entities to keep the application aligned with the technical assignment.

Additional entities such as Product, Organization, User, Chat Session, or AI Audit Logs are intentionally excluded because they are outside the current project scope.

Future enhancements can be introduced without requiring significant changes to the existing relationship structure.