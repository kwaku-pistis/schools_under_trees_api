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
    return db.query(models.Region).filter(models.District.name == name).one()


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


def get_all_schools(db: Session):
    return db.query(models.School).all()


def get_school_by_id(db: Session, id: int):
    return db.query(models.School).filter(models.School.id == id).one_or_none()


def get_images_by_school_id(db: Session, id: int, image_category: str):
    if image_category:
        return db.query(models.SchoolImages).filter(models.SchoolImages.school_id == id, models.SchoolImages.category == image_category)

    return db.query(models.SchoolImages).filter(models.SchoolImages.school_id == id).all()


def get_all_images(db: Session, category: str):
    if category:
        return db.query(models.SchoolImages).filter(models.SchoolImages.category == category).all()

    return db.query(models.SchoolImages).all()
