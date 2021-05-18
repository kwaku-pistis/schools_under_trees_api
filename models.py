from datetime import datetime
from typing import Counter
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime, String
from database import Base


class Schools(Base):
    __tablename__ = 'school_list'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    district_id = Column(Integer, ForeignKey('districts.id', ondelete='CASCADE'))

    # district = relationship('district', back_populates='school_list')
    # region = relationship('', back_populates='school_list')

    def __repr__(self):
        return "<(name='%s', description='%s', location='%s')>" % (
            self.name,
            self.description,
            self.location
        )


class District(Base):
    __tablename__ = 'districts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    region_id = Column(Integer, ForeignKey('regions.id', ondelete='CASCADE'))

    # region = relationship('regions', back_populates='districts')

    def __repr__(self):
        return "<(name='%s')>" % (
            self.name
        )


class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)
