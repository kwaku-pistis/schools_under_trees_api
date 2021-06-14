from datetime import datetime
from schemas import ImageBase, SchoolImagesBase
from typing import Counter, List, cast
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, session
from sqlalchemy.sql.sqltypes import Date, DateTime, String
from database import Base
import crud


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    district = relationship('District', back_populates='region', lazy='joined')

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

    region = relationship('Region', back_populates='district', lazy='joined')
    schools = relationship('School', back_populates='district', lazy='joined')

    def __repr__(self):
        return "<(name='%s', region_id='%s')>" % (
            self.name,
            self.region_id
        )

    def get_schools(id, db):
        return crud.get_school_by_district_id(db=db, district_id=id)


class SchoolImages(Base):
    __tablename__ = 'school_images'

    id  = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    image_url = Column(String)
    category = Column(String)
    school_id = Column(Integer, ForeignKey('school_list.id'))

    # school = relationship('School', back_populates='before_images')

    def __repr__(self):
        return "<(image_url='%s', category='%s', school_id='%s')>" % (
            self.image_url,
            self.category,
            self.school_id
        )


class School(Base):
    __tablename__ = 'school_list'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    district_id = Column(Integer, ForeignKey('district.id'))
    # images_id = Column(Integer, ForeignKey('before_images.id'))
    # during_images_id = Column(Integer, ForeignKey('during_images.id'))
    # after_images_id = Column(Integer, ForeignKey('after_images.id'))

    district = relationship('District', back_populates='schools', lazy='joined')
    school_images = relationship('SchoolImages', lazy='joined')
    # during_images = relationship('DuringImages', back_populates='school')
    # after_images = relationship('AfterImages', back_populates='school')

    def __repr__(self):
        return "<(name='%s', description='%s', location='%s', district_id='%s')>" % (
            self.name,
            self.description,
            self.location,
            self.district_id,
        )

    def add_images(self, db, image_url, image_category):
        self.school_images += [
            SchoolImages(
                image_url=image_url,
                category=image_category
            )
        ]
        db.add(self)
        db.commit()
        db.refresh(self)
        return self.school_images[-1]


class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    full_name = Column(String)
    email_address = Column(String)
    contact_number = Column(String)
    message = Column(String)

    def __repr__(self):
        return "<(full_name='%s', email_address='%s', contact_number='%s', message='%s')>" % (
            self.full_name,
            self.email_address,
            self.contact_number,
            self.message
        )
