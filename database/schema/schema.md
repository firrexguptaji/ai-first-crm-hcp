# Database Schema Design

## Overview

The AI-First CRM HCP Module uses PostgreSQL as the primary relational database with SQLAlchemy as the ORM.

The schema is intentionally simple and centered around the assignment requirements. It consists of two core entities:

- Healthcare Professional (HCP)
- Interaction

The relationship between these entities is one-to-many, where a single Healthcare Professional can have multiple recorded interactions.

---

# Design Principles

- Keep the schema simple and easy to explain.
- Avoid unnecessary normalization.
- Support AI-driven interaction logging.
- Design for future extensibility without over-engineering.

---

# Entity: Healthcare Professional

Represents a healthcare professional managed within the CRM.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Primary Key |
| first_name | String | Yes | HCP first name |
| last_name | String | Yes | HCP last name |
| specialization | String | Yes | Medical specialization |
| organization | String | Yes | Hospital or clinic name |
| email | String | No | Contact email |
| phone | String | No | Contact number |
| created_at | Timestamp | Yes | Record creation timestamp |
| updated_at | Timestamp | Yes | Record update timestamp |

---

# Entity: Interaction

Represents an interaction between a medical representative and an HCP.

Each interaction belongs to exactly one Healthcare Professional.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Primary Key |
| hcp_id | UUID | Yes | Foreign Key to Healthcare Professional |
| interaction_date | Timestamp | Yes | Date and time of interaction |
| channel | Enum | Yes | Interaction channel |
| raw_notes | Text | Yes | Original user input captured through AI |
| summary | Text | Yes | AI-generated structured summary |
| sentiment | Enum | Yes | Overall interaction sentiment |
| products_discussed | JSONB | No | List of products discussed |
| follow_up_required | Boolean | Yes | Indicates whether follow-up is required |
| follow_up_date | Date | No | Scheduled follow-up date |
| attendees | JSONB | No | Other people present, e.g. nurses (#72) |
| samples_distributed | JSONB | No | Product samples handed over (#72) |
| outcomes | Text | No | Agreements or results of the interaction (#72) |
| follow_up_actions | Text | No | Next steps for the representative (#72) |
| created_at | Timestamp | Yes | Record creation timestamp |
| updated_at | Timestamp | Yes | Record update timestamp |

---

# Relationship

Healthcare Professional

1

↓

Many

Interaction

Each Healthcare Professional can have multiple interactions.

Each Interaction belongs to exactly one Healthcare Professional.

---

# Enumerations

## Interaction Channel

- IN_PERSON
- PHONE
- EMAIL
- VIDEO
- OTHER

---

## Sentiment

- POSITIVE
- NEUTRAL
- NEGATIVE

---

# Constraints

## Healthcare Professional

- Primary Key on `id`
- Email should be unique when provided
- `first_name` is required
- `last_name` is required
- `specialization` is required
- `organization` is required

---

## Interaction

- Primary Key on `id`
- Foreign Key on `hcp_id`
- Cascade delete on Healthcare Professional removal
- `interaction_date` is required
- `raw_notes` is required
- `summary` is required
- `follow_up_date` is nullable
- `attendees`, `samples_distributed`, `outcomes`, `follow_up_actions` are nullable

---

# Migrations

Columns added after the initial schema are applied with SQL scripts in `database/migrations/`.

| Migration | Issue | Change |
|-----------|-------|--------|
| `001_add_interaction_fields.sql` | #72 | Add `attendees`, `samples_distributed`, `outcomes`, `follow_up_actions` |

See `database/migrations/README.md`.

---

# Indexes

## Healthcare Professional

- email
- specialization
- organization

---

## Interaction

- hcp_id
- interaction_date
- follow_up_date

---

# Future Considerations

The current schema intentionally remains minimal to satisfy the technical assignment.

Future enhancements may include:

- Product master table
- Organization master table
- AI audit logs
- Interaction attachments
- User authentication and authorization
- Activity history
- Soft deletes
- Database migrations using Alembic (manual SQL migrations are used for now)

These features are outside the current project scope and are therefore not included in the initial schema.