from typing import List, Optional
from sqlalchemy.orm.interfaces import SessionExtension
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.base import SchemaEventTarget
import uvicorn
from fastapi import FastAPI, Depends
import models, schemas, crud, factories
from database import SessionLocal, engine


models.Base.metadata.create_all(engine)


app = FastAPI(
    title="SCHOOLS UNDER TREES",
    description="The api to communicate with the schools under trees web app",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

regions = [
    "Greater Accra Region",
    "Central Region",
    "Eastern Region",
    "Western Region",
    "Ashanti Region",
    "Northern Region",
    "Upper East Region",
    "Upper West Region",
    "Volta Region",
    "Brong Ahafo Region",
    "Oti Region",
    "Western North Region",
    "Ahafo Region",
    "Bono East Region",
    "Savannah Region",
    "North East Region"
]

data = crud.insert_regions(regions=regions, db=get_db_session())
print('Data count:', len(data))


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Schools Under Trees Web Api"}


@app.post('/create-region/')
def create_region(region: schemas.RegionBase, db: Session = Depends(get_db)):
    """
        Create regions in Ghana with the following information

        - **name**: The name of the region and this is required.
    """
    return crud.create_region(db=db, region=region)


@app.get('/regions/')
def get_all_regions(db: Session = Depends(get_db)):
    return crud.get_all_regions(db=db)


@app.post('/create-district/')
def create_district(district: schemas.DistrictBase, db: Session = Depends(get_db)):
    region_record = crud.get_region_by_id(db=db, id=district.region_id)
    result = region_record.add_district(db=db, name=district.name)
    return {"status": 201, "message": result}


@app.get('/districts/')
def get_all_districts(db: Session = Depends(get_db)):
    return crud.get_all_districts(db=db)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)