from typing import Optional
from pydantic import BaseModel, Field


class SchoolBase(BaseModel):
    name: str = Field(title="Name of School")
    description: Optional[str] = Field(description='A short description of the school')
    location: str = Field(title="School's location", description='This will store the google locations of the school')
    district_id: int
    # region: str

    class Config:
        orm_mode = True


class DistricBase(BaseModel):
    name: str
    region_id: int

    class Config:
        orm_mode = True


class RegionBase(BaseModel):
    name: str
    district: Optional[str] = None

    class Config:
        orm_mode = True
