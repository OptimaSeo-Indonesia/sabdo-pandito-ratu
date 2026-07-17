# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class AdvisorModel(Base):
    __tablename__ = "advisors"

    persona = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    system_prompt = Column(Text, nullable=False)
    active = Column(Integer, default=1)
    capability_requirements = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DeliberationSessionModel(Base):
    __tablename__ = "deliberation_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True)
    question = Column(Text, nullable=False)
    context = Column(JSONB, default=dict)
    status = Column(String(30), default="pending")
    domain = Column(String(50), default="general")
    stakes = Column(String(20), default="unknown")
    time_sensitivity = Column(String(20), default="moderate")
    affected_stakeholders = Column(JSONB, default=list)
    data_gaps = Column(JSONB, default=list)
    key_constraints = Column(JSONB, default=list)
    wisdom_score = Column(JSONB, nullable=True)
    reflection = Column(JSONB, nullable=True)
    scores = Column(JSONB, nullable=True)
    verdict = Column(JSONB, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    responses = relationship("AdvisorResponseModel", back_populates="session", cascade="all, delete-orphan")
    conflicts = relationship("DisagreementModel", back_populates="session", cascade="all, delete-orphan")
    selections = relationship("ModelSelectionModel", back_populates="session", cascade="all, delete-orphan")
    call_logs = relationship("LLMCallLogModel", back_populates="session", cascade="all, delete-orphan")
    principle_evaluations = relationship("PrincipleEvaluationModel", back_populates="session", cascade="all, delete-orphan")
    scenarios = relationship("ScenarioModel", back_populates="session", cascade="all, delete-orphan")


class AdvisorResponseModel(Base):
    __tablename__ = "advisor_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("deliberation_sessions.session_id"), nullable=False)
    persona = Column(String(50), nullable=False)
    stance = Column(String(20), nullable=False)
    summary = Column(Text, default="")
    reasoning = Column(Text, default="")
    confidence = Column(Float, default=0.5)
    key_points = Column(JSONB, default=list)
    data_sources = Column(JSONB, default=list)
    assumptions = Column(JSONB, default=list)

    session = relationship("DeliberationSessionModel", back_populates="responses")


class DisagreementModel(Base):
    __tablename__ = "disagreements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("deliberation_sessions.session_id"), nullable=False)
    conflict_type = Column(String(30), nullable=False)
    description = Column(Text, nullable=False)
    between_personas = Column(JSONB, default=list)
    root_cause = Column(Text, default="")
    resolution = Column(Text, nullable=True)

    session = relationship("DeliberationSessionModel", back_populates="conflicts")


class ModelSelectionModel(Base):
    __tablename__ = "model_selections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("deliberation_sessions.session_id"), nullable=False)
    persona = Column(String(50), nullable=False)
    selected_adapter = Column(String(100), nullable=False)
    selected_model = Column(String(100), nullable=False)
    selection_reason = Column(Text, default="")
    fallback_occurred = Column(Integer, default=0)
    fallback_from = Column(String(100), nullable=True)

    session = relationship("DeliberationSessionModel", back_populates="selections")


class LLMCallLogModel(Base):
    __tablename__ = "llm_call_logs"

    id = Column(String(36), primary_key=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("deliberation_sessions.session_id"), nullable=False)
    persona = Column(String(50), nullable=False)
    provider = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    step = Column(String(30), nullable=False)
    latency_ms = Column(Integer, nullable=True)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    success = Column(Integer, default=1)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    fallback_occurred = Column(Integer, default=0)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("DeliberationSessionModel", back_populates="call_logs")


class PrincipleEvaluationModel(Base):
    __tablename__ = "principle_evaluations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("deliberation_sessions.session_id"), nullable=False)
    principle = Column(String(50), nullable=False)
    score = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    rationale = Column(Text, default="")
    concerns = Column(JSONB, default=list)

    session = relationship("DeliberationSessionModel", back_populates="principle_evaluations")


class ScenarioModel(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("deliberation_sessions.session_id"), nullable=False)
    scenario_name = Column(String(100), nullable=False)
    time_horizon = Column(String(30), nullable=False)
    probability = Column(Float, default=0.5)
    uncertainty_level = Column(String(20), default="medium")
    net_impact = Column(Float, default=0.0)
    positive_outcomes = Column(JSONB, default=list)
    negative_outcomes = Column(JSONB, default=list)
    assumptions = Column(JSONB, default=list)

    session = relationship("DeliberationSessionModel", back_populates="scenarios")


class DecisionCaseModel(Base):
    __tablename__ = "decision_cases"

    case_id = Column(String(36), primary_key=True)
    question = Column(Text, nullable=False)
    domain = Column(String(50), default="general")
    verdict = Column(String(50), nullable=False)
    confidence = Column(Float, default=0.0)
    wisdom_score = Column(JSONB, nullable=True)
    outcome = Column(String(100), nullable=True)
    outcome_score = Column(Float, nullable=True)
    lessons_learned = Column(JSONB, default=list)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
