from typing import Optional, List
from pydantic import BaseModel, Field


class DistrictBase(BaseModel):
    name: str
    region_id: int

    class Config:
        orm_mode = True


class RegionBase(BaseModel):
    name: str
    district: Optional[str] = None

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    image_url: str
    category: str = Field(title="Image Category", description="This field specifies whether the image is a before, during or an after picture.")


class SchoolImagesBase(ImageBase):
    school_id: int

    class Config:
        orm_mode = True


class SchoolBase(BaseModel):
    name: str = Field(title="Name of School")
    description: Optional[str] = Field(description='A short description of the school')
    location: str = Field(title="School's location", description='This will store the google locations of the school')
    district_id: int
    school_images: Optional[List[ImageBase]] = None

    class Config:
        orm_mode = True
