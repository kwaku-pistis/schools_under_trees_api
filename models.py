from datetime import datetime
from typing import Counter
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, session
from sqlalchemy.sql.sqltypes import DateTime, String
from database import Base


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    district = relationship('District', back_populates='region')

    def __repr__(self):
        return "<(name='%s')>" % {
            self.name
        }

    def add_district(self, db, name):
        self.district += [District(name=name)]
        db.add(self)
        db.commit()
        db.refresh(self)
        return self.district[-1]


class District(Base):
    __tablename__ = 'district'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    region_id = Column(Integer, ForeignKey('region.id'))

    region = relationship('Region', back_populates='district')
    schools = relationship('School', back_populates='district')

    def __repr__(self):
        return "<(name='%s', region_id='%s')>" % (
            self.name,
            self.region_id
        )


class School(Base):
    __tablename__ = 'school_list'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    district_id = Column(Integer, ForeignKey('district.id'))
    image_url = Column(String)

    district = relationship('District', back_populates='schools')

    def __repr__(self):
        return "<(name='%s', description='%s', location='%s', district_id='%s', image_url='%s')>" % (
            self.name,
            self.description,
            self.location,
            self.distric_id,
            self.image_url,
        )

