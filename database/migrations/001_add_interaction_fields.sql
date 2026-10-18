-- Migration 001: Add additional interaction fields (#72)
--
-- Adds the fields shown on the Interaction Details form that were
-- not stored before. All columns are nullable, so existing rows stay
-- valid and no data is lost.
--
-- Safe to run more than once (IF NOT EXISTS).
--
-- Run with:
--   psql -U postgres -d ai_first_crm_hcp -f database/migrations/001_add_interaction_fields.sql
-- or paste into the pgAdmin Query Tool.

BEGIN;

ALTER TABLE interactions
    ADD COLUMN IF NOT EXISTS attendees JSONB,
    ADD COLUMN IF NOT EXISTS samples_distributed JSONB,
    ADD COLUMN IF NOT EXISTS outcomes TEXT,
    ADD COLUMN IF NOT EXISTS follow_up_actions TEXT;

COMMIT;
