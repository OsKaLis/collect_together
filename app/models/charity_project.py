from app.core.db import Base
from sqlalchemy import (
    Column, String, Text
)

from app.models import BasisDonationAndCharityProject


class CharityProject(Base, BasisDonationAndCharityProject):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
