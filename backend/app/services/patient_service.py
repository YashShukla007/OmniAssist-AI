from sqlalchemy.orm import Session

from backend.app.models.healthcare import PatientProfile
from backend.app.models.user import User
from backend.app.schemas.healthcare import PatientProfileUpdate


class PatientService:
    def get_or_create_profile(self, db: Session, user: User) -> PatientProfile:
        if user.patient_profile is not None:
            return user.patient_profile

        profile = PatientProfile(user_id=user.id)
        db.add(profile)
        db.flush()
        return profile

    def update_profile(
        self,
        db: Session,
        profile: PatientProfile,
        update: PatientProfileUpdate,
    ) -> PatientProfile:
        for field_name, value in update.model_dump(exclude_unset=True).items():
            setattr(profile, field_name, value)
        db.flush()
        return profile


patient_service = PatientService()
