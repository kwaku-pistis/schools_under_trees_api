from sqlalchemy.orm.session import Session
from sqlalchemy.sql.base import SchemaEventTarget
import uvicorn
from fastapi import FastAPI, Depends
import models, schemas, crud
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



@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Schools Under Trees Web Api"}


@app.post('/create_regions/')
def create_regions(region: schemas.RegionBase, db: Session = Depends(get_db)):
    """
        Create regions in Ghana with the following information

        - **name**: The name of the region and this is required.
    """
    return crud.create_region(db=db, region=region)


@app.get('/regions/')
def get_all_regions(db: Session = Depends(get_db)):
    return crud.get_all_regions(db=db)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)