from typing import List
from sqlalchemy.orm.session import Session
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
        result = db.query(models.Region).filter(models.Region.name == region).one()
        print("##", result)
        if not result:
            region_data = schemas.RegionBase(name=region)
            res = create_region(db=db, region=region_data)
            data.append(res.name)
    return data
