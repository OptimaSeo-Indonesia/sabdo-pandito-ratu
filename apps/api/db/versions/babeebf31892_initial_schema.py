"""initial_schema

Revision ID: babeebf31892
Revises:
Create Date: 2026-07-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "babeebf31892"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "advisors",
        sa.Column("persona", sa.String(50), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("system_prompt", sa.Text(), nullable=False),
        sa.Column("active", sa.Integer(), server_default="1"),
        sa.Column("capability_requirements", postgresql.JSONB(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "decision_cases",
        sa.Column("case_id", sa.String(36), primary_key=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("domain", sa.String(50), server_default="general"),
        sa.Column("verdict", sa.String(50), nullable=False),
        sa.Column("confidence", sa.Float(), server_default="0.0"),
        sa.Column("wisdom_score", postgresql.JSONB(), nullable=True),
        sa.Column("outcome", sa.String(100), nullable=True),
        sa.Column("outcome_score", sa.Float(), nullable=True),
        sa.Column("lessons_learned", postgresql.JSONB(), server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "deliberation_sessions",
        sa.Column("session_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("context", postgresql.JSONB(), server_default="{}"),
        sa.Column("status", sa.String(30), server_default="pending"),
        sa.Column("domain", sa.String(50), server_default="general"),
        sa.Column("stakes", sa.String(20), server_default="unknown"),
        sa.Column("time_sensitivity", sa.String(20), server_default="moderate"),
        sa.Column("affected_stakeholders", postgresql.JSONB(), server_default="[]"),
        sa.Column("data_gaps", postgresql.JSONB(), server_default="[]"),
        sa.Column("key_constraints", postgresql.JSONB(), server_default="[]"),
        sa.Column("wisdom_score", postgresql.JSONB(), nullable=True),
        sa.Column("reflection", postgresql.JSONB(), nullable=True),
        sa.Column("scores", postgresql.JSONB(), nullable=True),
        sa.Column("verdict", postgresql.JSONB(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "advisor_responses",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("deliberation_sessions.session_id"), nullable=False),
        sa.Column("persona", sa.String(50), nullable=False),
        sa.Column("stance", sa.String(20), nullable=False),
        sa.Column("summary", sa.Text(), server_default=""),
        sa.Column("reasoning", sa.Text(), server_default=""),
        sa.Column("confidence", sa.Float(), server_default="0.5"),
        sa.Column("key_points", postgresql.JSONB(), server_default="[]"),
        sa.Column("data_sources", postgresql.JSONB(), server_default="[]"),
        sa.Column("assumptions", postgresql.JSONB(), server_default="[]"),
    )

    op.create_table(
        "disagreements",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("deliberation_sessions.session_id"), nullable=False),
        sa.Column("conflict_type", sa.String(30), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("between_personas", postgresql.JSONB(), server_default="[]"),
        sa.Column("root_cause", sa.Text(), server_default=""),
        sa.Column("resolution", sa.Text(), nullable=True),
    )

    op.create_table(
        "model_selections",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("deliberation_sessions.session_id"), nullable=False),
        sa.Column("persona", sa.String(50), nullable=False),
        sa.Column("selected_adapter", sa.String(100), nullable=False),
        sa.Column("selected_model", sa.String(100), nullable=False),
        sa.Column("selection_reason", sa.Text(), server_default=""),
        sa.Column("fallback_occurred", sa.Integer(), server_default="0"),
        sa.Column("fallback_from", sa.String(100), nullable=True),
    )

    op.create_table(
        "llm_call_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("deliberation_sessions.session_id"), nullable=False),
        sa.Column("persona", sa.String(50), nullable=False),
        sa.Column("provider", sa.String(100), nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("step", sa.String(30), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("success", sa.Integer(), server_default="1"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("retry_count", sa.Integer(), server_default="0"),
        sa.Column("fallback_occurred", sa.Integer(), server_default="0"),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "principle_evaluations",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("deliberation_sessions.session_id"), nullable=False),
        sa.Column("principle", sa.String(50), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("rationale", sa.Text(), server_default=""),
        sa.Column("concerns", postgresql.JSONB(), server_default="[]"),
    )

    op.create_table(
        "scenarios",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("deliberation_sessions.session_id"), nullable=False),
        sa.Column("scenario_name", sa.String(100), nullable=False),
        sa.Column("time_horizon", sa.String(30), nullable=False),
        sa.Column("probability", sa.Float(), server_default="0.5"),
        sa.Column("uncertainty_level", sa.String(20), server_default="medium"),
        sa.Column("net_impact", sa.Float(), server_default="0.0"),
        sa.Column("positive_outcomes", postgresql.JSONB(), server_default="[]"),
        sa.Column("negative_outcomes", postgresql.JSONB(), server_default="[]"),
        sa.Column("assumptions", postgresql.JSONB(), server_default="[]"),
    )


def downgrade() -> None:
    op.drop_table("scenarios")
    op.drop_table("principle_evaluations")
    op.drop_table("llm_call_logs")
    op.drop_table("model_selections")
    op.drop_table("disagreements")
    op.drop_table("advisor_responses")
    op.drop_table("deliberation_sessions")
    op.drop_table("decision_cases")
    op.drop_table("advisors")
