from datetime import datetime
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.operators import exists
import models, schemas


def create_region(db: Session, region: schemas.RegionBase):
    data = models.Region(
        name = region.name
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def get_all_regions(db: Session):
    return db.query(models.Region).all()


def get_region_by_id(db: Session, id: int):
    return db.query(models.Region).filter(models.Region.id == id).one()

def get_region_by_name(db: Session, name: str):
    return db.query(models.Region).filter(models.Region.name == name).one()


def create_district(db: Session, district: schemas.DistrictBase):
    data = models.District(
        name = district.name,
        region_id = district.region_id
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def get_all_districts(db: Session):
    return db.query(models.District).all()


def get_district_by_id(db: Session, id: int):
    return db.query(models.District).filter(models.District.id == id).one()


def get_district_by_name(db: Session, name: str):
    return db.query(models.Region).filter(models.District.name.ilike('%'+name+'%')).all()


def insert_regions(regions: List, db: Session):
    data = []
    for region in regions:
        result = db.query(models.Region).filter(models.Region.name == region).one_or_none()
        print("##", result)
        if not result:
            region_data = schemas.RegionBase(name=region)
            res = create_region(db=db, region=region_data)
            data.append(res.name)
    return data


def create_school(db: Session, school: schemas.SchoolBase):
    data = models.School(
        name=school.name,
        description=school.description,
        location=school.location,
        district_id=school.district_id
    )
    
    db.add(data)
    db.commit()
    db.refresh(data)

    if school.school_images:
        for image in school.school_images:
            models.School.add_images(
                self=data,
                db=db, 
                image_url=image.image_url, 
                image_category=image.category
            )

    return data


def get_all_schools(db: Session):
    return db.query(models.School).all()


def get_school_by_id(db: Session, id: int):
    return db.query(models.School).filter(models.School.id == id).one_or_none()


def get_school_by_name(db: Session, name: str):
    return db.query(models.School).filter(models.School.name.ilike('%'+name+'%')).all()


def get_school_by_district_id(db: Session, district_id: int):
    return db.query(models.School).filter(models.School.district_id == district_id).all()


def update_school_location(db: Session, location: schemas.LocationBase):
    result = db.query(models.School).filter(models.School.id == location.school_id).one()
    if result:
        result.location = location.url
        db.add(result)
        db.commit()
        db.refresh(result)
    return result


def get_images_by_school_id(db: Session, id: int, image_category: str):
    if image_category:
        return db.query(models.SchoolImages).filter(models.SchoolImages.school_id == id, models.SchoolImages.category == image_category).all()

    return db.query(models.SchoolImages).filter(models.SchoolImages.school_id == id).all()


def get_all_images(db: Session, category: str):
    if category:
        return db.query(models.SchoolImages).filter(models.SchoolImages.category == category).all()

    return db.query(models.SchoolImages).all()


def save_email(db: Session, email: schemas.Email):
    data = models.Email(
        full_name=email.full_name,
        email_address=email.email,
        contact_number=email.contact_number,
        message=email.message
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
