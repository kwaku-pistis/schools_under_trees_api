from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


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


class SchoolImagesBase(BaseModel):
    school_id: int
    image_urls: List[ImageBase]

    class Config:
        orm_mode = True


class UploadImageBase(BaseModel):
    image: List


class SchoolBase(BaseModel):
    name: str = Field(title="Name of School")
    description: Optional[str] = Field(description='A short description of the school')
    location: str = Field(title="School's location", description='This will store the google locations of the school')
    district_id: int
    school_images: Optional[List[ImageBase]] = None

    class Config:
        orm_mode = True


class Email(BaseModel):
    full_name: str
    email: EmailStr
    contact_number: Optional[str] = None
    message: str

    class Config:
        orm_mode = True


class EmailSchema(BaseModel):
    email: List[EmailStr]
