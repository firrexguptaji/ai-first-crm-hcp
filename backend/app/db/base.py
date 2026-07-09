from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so SQLAlchemy registers them
from app.models.healthcare_professional import HealthcareProfessional
from app.models.interaction import Interaction