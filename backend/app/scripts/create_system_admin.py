import argparse
import getpass
import os
from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository
from app.repositories.system_setting_repository import SystemSettingRepository


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the private CareerVault system administrator account."
    )
    parser.add_argument(
        "--email",
        default=os.getenv("SYSTEM_ADMIN_EMAIL"),
        help="Administrator email (or set SYSTEM_ADMIN_EMAIL)",
    )
    parser.add_argument(
        "--name",
        default=os.getenv("SYSTEM_ADMIN_FULL_NAME", "CareerVault Administrator"),
        help="Administrator display name",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.email:
        raise SystemExit("Provide --email or set SYSTEM_ADMIN_EMAIL.")

    password = os.getenv("SYSTEM_ADMIN_PASSWORD") or getpass.getpass(
        "System administrator password: "
    )
    with SessionLocal() as db:
        minimum, maximum = SystemSettingRepository(
            db
        ).get_password_length_policy()
        if not minimum <= len(password) <= maximum:
            raise SystemExit(
                f"The administrator password must contain between {minimum} "
                f"and {maximum} characters."
            )
        repository = UserRepository(db)
        existing = repository.get_by_email(args.email)
        if existing is not None:
            if existing.role != UserRole.SYSTEM_ADMIN:
                raise SystemExit(
                    "That email belongs to a job applicant. Use a separate administrator email."
                )
            repository.update(
                existing,
                full_name=args.name.strip(),
                hashed_password=hash_password(password),
                is_active=True,
            )
            print(f"Updated system administrator: {existing.email}")
            return

        now = datetime.now(timezone.utc)
        administrator = repository.create(
            email=args.email.strip().lower(),
            full_name=args.name.strip(),
            hashed_password=hash_password(password),
            is_active=True,
            role=UserRole.SYSTEM_ADMIN,
            created_at=now,
            updated_at=now,
        )
        print(f"Created system administrator: {administrator.email}")


if __name__ == "__main__":
    main()
