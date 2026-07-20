"""Backward-compatible import location for the shared database dependency."""

from backend.app.database.session import get_db

__all__ = ["get_db"]
