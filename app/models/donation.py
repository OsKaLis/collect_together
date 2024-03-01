from app.core.db import Base
from sqlalchemy import (
    Column, ForeignKey, Integer, Text
)

from app.models import BasisDonationAndCharityProject


class Donation(Base, BasisDonationAndCharityProject):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
