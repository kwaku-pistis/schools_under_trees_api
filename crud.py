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
