"""Add the persistent AgentCare healthcare coordination schema."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "44a0af2fd2ab"
down_revision: Union[str, Sequence[str], None] = "1e35ad531053"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    if "role" not in {column["name"] for column in inspector.get_columns("users")}:
        op.add_column("users", sa.Column("role", sa.String(length=30), nullable=False, server_default="patient"))

    if "patient_profiles" not in tables:
        op.create_table("patient_profiles", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True), sa.Column("date_of_birth", sa.Date(), nullable=True), sa.Column("phone", sa.String(length=30), nullable=True), sa.Column("preferred_language", sa.String(length=30), nullable=False, server_default="en"), sa.Column("emergency_contact", sa.String(length=100), nullable=True), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    if "departments" not in tables:
        op.create_table("departments", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=100), nullable=False, unique=True), sa.Column("description", sa.Text(), nullable=False), sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()))
    if "doctors" not in tables:
        op.create_table("doctors", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.id"), nullable=False), sa.Column("name", sa.String(length=100), nullable=False), sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()))
    if "appointment_slots" not in tables:
        op.create_table("appointment_slots", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.id"), nullable=False), sa.Column("start_time", sa.DateTime(), nullable=False), sa.Column("end_time", sa.DateTime(), nullable=False), sa.Column("status", sa.String(length=20), nullable=False, server_default="available"), sa.UniqueConstraint("doctor_id", "start_time", name="uq_doctor_slot_start"))
    if "appointments" not in tables:
        op.create_table("appointments", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient_profiles.id"), nullable=False), sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.id"), nullable=False), sa.Column("slot_id", sa.Integer(), sa.ForeignKey("appointment_slots.id"), nullable=False, unique=True), sa.Column("status", sa.String(length=20), nullable=False, server_default="confirmed"), sa.Column("reason", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    if "patient_documents" not in tables:
        op.create_table("patient_documents", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient_profiles.id"), nullable=False), sa.Column("document_type", sa.String(length=80), nullable=False), sa.Column("storage_reference", sa.String(length=500), nullable=False), sa.Column("original_filename", sa.String(length=255), nullable=False), sa.Column("checksum", sa.String(length=64), nullable=False), sa.Column("status", sa.String(length=30), nullable=False, server_default="received"), sa.Column("created_at", sa.DateTime(), nullable=False), sa.UniqueConstraint("patient_id", "checksum", name="uq_patient_document_checksum"))
    if "workflow_runs" not in tables:
        op.create_table("workflow_runs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient_profiles.id"), nullable=False), sa.Column("request_text", sa.Text(), nullable=False), sa.Column("current_step", sa.String(length=80), nullable=False, server_default="received"), sa.Column("state", sa.JSON(), nullable=False), sa.Column("status", sa.String(length=30), nullable=False, server_default="in_progress"), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    if "reminders" not in tables:
        op.create_table("reminders", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient_profiles.id"), nullable=False), sa.Column("appointment_id", sa.Integer(), sa.ForeignKey("appointments.id"), nullable=True), sa.Column("reminder_type", sa.String(length=80), nullable=False), sa.Column("message", sa.String(length=500), nullable=False), sa.Column("scheduled_at", sa.DateTime(), nullable=False), sa.Column("status", sa.String(length=30), nullable=False, server_default="scheduled"))
    if "escalations" not in tables:
        op.create_table("escalations", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("workflow_run_id", sa.Integer(), sa.ForeignKey("workflow_runs.id"), nullable=False), sa.Column("reason", sa.Text(), nullable=False), sa.Column("status", sa.String(length=30), nullable=False, server_default="open"), sa.Column("reviewed_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("reviewed_at", sa.DateTime(), nullable=True))
    if "audit_events" not in tables:
        op.create_table("audit_events", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True), sa.Column("action", sa.String(length=120), nullable=False), sa.Column("entity_type", sa.String(length=80), nullable=False), sa.Column("entity_id", sa.Integer(), nullable=True), sa.Column("details", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))

    if "departments" not in tables:
        op.bulk_insert(sa.table("departments", sa.column("name", sa.String), sa.column("description", sa.Text), sa.column("active", sa.Boolean)), [{"name": "Cardiology", "description": "Administrative coordination for heart-care appointments.", "active": True}, {"name": "General Medicine", "description": "Administrative coordination for general outpatient visits.", "active": True}])


def downgrade() -> None:
    bind = op.get_bind()
    tables = sa.inspect(bind).get_table_names()
    for table_name in ("audit_events", "escalations", "reminders", "workflow_runs", "patient_documents", "appointments", "appointment_slots", "doctors", "departments", "patient_profiles"):
        if table_name in tables:
            op.drop_table(table_name)
    if "users" in tables and "role" in {column["name"] for column in sa.inspect(bind).get_columns("users")}:
        op.drop_column("users", "role")
