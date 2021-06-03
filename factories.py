from sqlalchemy.orm import session
import factory
import models


class RegionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Region
        sqlalchemy_session = session

    # def create_region(name):
    #     return name

    name = ""
