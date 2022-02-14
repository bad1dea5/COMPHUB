#
#
#

import datetime as dt

from COMPHUB.database import Column, PKModel, db, reference_col, relationship

class Repair(PKModel):
    __tablename__ = "repair"

    name = Column(db.String(120), nullable=False)
    email = Column(db.String(120), nullable=False)
    number = Column(db.String(15), nullable=True)
    hardware = Column(db.String(30), nullable=False)
    message = Column(db.Text, nullable=False)
    datetime = Column(db.DateTime, nullable=False)
    status = Column(db.String(20), nullable=False)
    created = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
