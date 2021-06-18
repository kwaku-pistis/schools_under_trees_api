from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm.session import Session
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import HTMLResponse
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import models, schemas, crud
import uvicorn
import pyrebase


models.Base.metadata.create_all(engine)


app = FastAPI(
    title="SCHOOLS UNDER TREES",
    description="The api to communicate with the schools under trees web app",
    version="1.0.0"
)

# adding pyrebase config
config = {
  "apiKey": "AIzaSyB9CpPZhGUPls3Coe6j6TB285MacUWVlPM",
  "authDomain": "principal-yen-314412.firebaseapp.com",
  "databaseURL": "",
  "storageBucket": "principal-yen-314412.appspot.com"
}

firebase = pyrebase.initialize_app(config)

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


# @app.get("/", include_in_schema=False)
# async def main():
#     content = """
#         <body>
#         <form action="/files/" enctype="multipart/form-data" method="post">
#         <input name="files" type="file" multiple>
#         <input type="submit">
#         </form>
#         <form action="/upload-images/" enctype="multipart/form-data" method="post">
#         <input name="files" type="file" multiple>
#         <input type="submit">
#         </form>
#         </body>
#     """
#     return HTMLResponse(content=content)


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


@app.post('/send-email/', tags=["Email"])
async def send_email(email: schemas.Email, db: Session = Depends(get_db)):
    conf = ConnectionConfig(
        MAIL_USERNAME="sutpuser@gmail.com",
        MAIL_PASSWORD="app.sutpuser",
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_TLS=True,
        MAIL_SSL=False,
        MAIL_FROM=email.email,
        MAIL_FROM_NAME=email.full_name,
        USE_CREDENTIALS=True
    )

    # message schema for the email
    message = MessageSchema(
        subject="SCHOOLS UNDER TREES CONTACT MAIL",
        # recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        recipients=["zeroschoolsundertrees@gmail.com"],
        body=email.message,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)

    return crud.save_email(db=db, email=email)


@app.post('/upload-images/', tags=["School"])
async def upload_images(files: List[UploadFile] = File(...)):
    image_urls = []
    storage = firebase.storage()
    for file in files:
        image = file.file.read()
        storage.child("school_images/"+file.filename).put(image)
        download_url = storage.child("school_images/"+file.filename).get_url("")
        print(download_url)
        image_urls.append(download_url)
    return {"image_urls": image_urls}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)