from typing import Optional
from sqlalchemy.orm.session import Session
import uvicorn
from fastapi import FastAPI, Depends
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(engine)


app = FastAPI(
    title="SCHOOLS UNDER TREES",
    description="The api to communicate with the schools under trees web app",
    version="1.0.0"
)


origins = [
    "http://localhost:8000",
    "http://localhost",
    "http://localhost:8080",
    "https://schoolsundertrees.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    "Bono Region",
    "Oti Region",
    "Western North Region",
    "Ahafo Region",
    "Bono East Region",
    "Savannah Region",
    "North East Region"
]

data = crud.insert_regions(regions=sorted(regions), db=get_db_session())
print('Data count:', len(data))


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Schools Under Trees Web Api"}


@app.post('/create-region/', tags=["Region"])
def create_region(region: schemas.RegionBase, db: Session = Depends(get_db)):
    """
        Create regions in Ghana with the following information

        - **name**: The name of the region and this is required.
    """
    return crud.create_region(db=db, region=region)


@app.get('/regions/', tags=["Region"])
def get_all_regions(db: Session = Depends(get_db)):
    return crud.get_all_regions(db=db)


@app.post('/create-district/', tags=["District"])
def create_district(district: schemas.DistrictBase, db: Session = Depends(get_db)):
    """
        This api is to create a district and tie it to a region. 
        So a region is specified using the id of the region.

        - **region_id**: a foreign key to the regions table. So the id specified must be present in the regions table.
    """
    region_record = crud.get_region_by_id(db=db, id=district.region_id)
    result = region_record.add_district(db=db, name=district.name)
    return {"status": 201, "message": result}


@app.get('/districts/', tags=["District"])
def get_all_districts(db: Session = Depends(get_db)):
    return crud.get_all_districts(db=db)


@app.get('/district-schools/', tags=["District"])
def get_district_schools(id: int, db: Session = Depends(get_db)):
    return crud.get_school_by_district_id(db=db, district_id=id)


@app.post('/create-school/', tags=["School"])
def create_school(school: schemas.SchoolBase, db: Session = Depends(get_db)):
    # district_record = crud.get_district_by_id(db=db, id=school.district_id)
    # if district_record:
    #     result = district_record.add_schools(
    #         db=db, 
    #         name=school.name, 
    #         description=school.description, 
    #         location=school.location,
    #         images=school.school_images
    #     )
    #     return {"status": 201, "message": result}

    return crud.create_school(db=db, school=school)



@app.get('/all-schools/', tags=["School"])
def get_all_schools(db: Session = Depends(get_db)):
    return crud.get_all_schools(db=db)


@app.get('/school/', tags=["School"])
def get_school_by_name(name: str, db: Session = Depends(get_db)):
    return crud.get_school_by_name(db=db, name=name)


@app.post('/add-images/', tags=["School"])
def add_images_to_school(image: schemas.SchoolImagesBase, db: Session = Depends(get_db)):
    school_record = crud.get_school_by_id(db=db, id=image.school_id)
    if school_record:
        result = school_record.add_images(
            db=db,
            image_url=image.image_url,
            image_category=image.category
        )
        return {"status": 201, "message": result}


@app.get('/school-images/', tags=["School"])
def get_school_images(school_id: int, image_category: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_images_by_school_id(db=db, id=school_id, image_category=image_category)


@app.get('/all-images/', tags=["School"])
def get_school_images_by_category(category: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_all_images(db=db, category=category)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)