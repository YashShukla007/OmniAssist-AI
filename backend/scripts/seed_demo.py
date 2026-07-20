"""Provision a synthetic staff or administrator account for local demos.

This command is intentionally outside the HTTP API so public registration can
remain patient-only while reviewers can still exercise staff-only workflows.
"""

from __future__ import annotations

import argparse
from getpass import getpass

from sqlalchemy import select

from backend.app.core.security import hash_password
from backend.app.database.session import SessionLocal
from backend.app.models.user import User


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a synthetic local AgentCare staff account.")
    parser.add_argument("--role", choices=("hospital_staff", "administrator"), default="hospital_staff")
    parser.add_argument("--username", default="Demo Hospital Staff")
    parser.add_argument("--email", default="staff@agentcare-demo.com")
    parser.add_argument("--password", help="Optional local demo password. If omitted, a secure prompt is shown.")
    args = parser.parse_args()
    password = args.password or getpass("Local demo password: ")
    if len(password) < 8:
        parser.error("Password must contain at least 8 characters.")

    with SessionLocal() as db:
        existing = db.scalar(select(User).where(User.email == args.email))
        if existing is not None:
            parser.error(f"An account already exists for {args.email}. Use a different email instead of changing its role.")
        user = User(
            username=args.username,
            email=args.email,
            password_hash=hash_password(password),
            role=args.role,
        )
        db.add(user)
        db.commit()
        print(f"Created synthetic {args.role} account: {args.email}")


if __name__ == "__main__":
    main()
