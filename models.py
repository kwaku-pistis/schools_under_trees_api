from datetime import datetime
from schemas import SchoolImagesBase
from typing import Counter, List, cast
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, session
from sqlalchemy.sql.sqltypes import Date, DateTime, String
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

    def add_schools(self, db, name, description, location, images: SchoolImagesBase):
        self.schools += [
            School(
                name=name, 
                description=description,
                location=location,
            )
        ]
        # add images to school
        for image in images:
            self.schools.add_images(db=db, image_url=image.image_url, image_category=image.category)

        db.add(self)
        db.commit()
        db.refresh(self)
        return self.schools[-1]


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


# class DuringImages(Base):
#     __tablename__ = 'during_images'

#     id  = Column(Integer, primary_key=True, index=True)
#     date_created = Column(DateTime, default=datetime.utcnow)
#     image_url = Column(String)
#     school_id = Column(Integer, ForeignKey('school_list.id'))

#     school = relationship('School', back_populates='during_images')

#     def __repr__(self):
#         return "<(image_url='%s', school_id='%s')>" % (
#             self.image_url,
#             self.school_id
#         )


# class AfterImages(Base):
#     __tablename__ = 'after_images'

#     id  = Column(Integer, primary_key=True, index=True)
#     date_created = Column(DateTime, default=datetime.utcnow)
#     image_url = Column(String)
#     school_id = Column(Integer, ForeignKey('school_list.id'))

#     school = relationship('School', back_populates='after_images')

#     def __repr__(self):
#         return "<(image_url='%s', school_id='%s')>" % (
#             self.image_url,
#             self.school_id
#         )


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

    district = relationship('District', back_populates='schools')
    school_images = relationship('SchoolImages')
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


