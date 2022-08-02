import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database import Base
from models.city import City


class PostalCode(Base):
    __tablename__ = 'postal_code'

    # Fields from reference data from pochta.ru
    #   https://www.pochta.ru/support/database/ops
    index = sa.Column(sa.String(6), primary_key=True)
    ops_name = sa.Column(sa.String())
    ops_type = sa.Column(sa.String())
    ops_subm = sa.Column(sa.String(6))
    region = sa.Column(sa.String(), index=True)
    autonom = sa.Column(sa.String(), index=True)
    area = sa.Column(sa.String(), index=True)
    city = sa.Column(sa.String(), index=True)
    city_1 = sa.Column(sa.String(), index=True)
    actdate = sa.Column(sa.Date())
    indexold = sa.Column(sa.String(6))

    # extended fields from another data source bound to the same postal code
    ext_adm_region = sa.Column(sa.String(64), index=True)
    ext_district = sa.Column(sa.String(64), index=True)

    # Map postal codes to normalized cities
    city_ref_id = sa.Column(sa.Integer, sa.ForeignKey("city.id"), index=True)
    city_ref = relationship(City, lazy='joined')

    timezone = sa.Column(sa.String)
