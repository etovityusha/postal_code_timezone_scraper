from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import text

from database import Base


class City(Base):
    created_at = sa.Column(
        sa.DateTime, default=datetime.utcnow, server_default=sa.func.now()
    )
    updated_at = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=sa.func.now(),
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String(512), unique=True)
    is_available_for_students = sa.Column(sa.Boolean, index=True, nullable=False,
                                          default=text('FALSE'), server_default=text('FALSE'))
    is_available_for_instructors = sa.Column(sa.Boolean, index=True, nullable=False,
                                             default=text('FALSE'), server_default=text('FALSE'))
