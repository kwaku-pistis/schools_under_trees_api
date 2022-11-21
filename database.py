from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases

# SQLALCHEMY_DATABASE_URL = 'postgresql://sut_user:sutuser@159.65.179.253/zero_schools_under_trees'

# SQLALCHEMY_DATABASE_URL = 'postgresql://sut_user:sutuser@159.65.179.253/sut'

SQLALCHEMY_DATABASE_URL = 'postgres://tleeazkaozcpwa:36c5213eb18222fa1a85375f3964cfda6e1b30faef8b56dae8bdcfb5e0618848@ec2-3-219-135-162.compute-1.amazonaws.com:5432/dds3fgmq1ctjm2';

psql_database = databases.Database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
