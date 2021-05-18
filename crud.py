from sqlalchemy.orm.session import Session
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
