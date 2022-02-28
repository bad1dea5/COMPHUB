#
#
#

import datetime

from COMPHUB.database import Column, ForeignKey, PKModel, db, reference_col, relationship

#
#
#
class Appointment(PKModel):
    __tablename__ = 'appointments'

    created = Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    date = Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    message = Column(db.Text, nullable=False)
    hardware = Column(db.String(16), default='None')
    device = Column(db.String(16), default='None')
    customer_id = Column(db.Integer, ForeignKey('customers.id'), nullable=False)

    def __repr__(self) -> str:
        return f'<Appointment({self.customer_id!r})>'

#
#
#
class Customer(PKModel):
    __tablename__ = 'customers'

    name = Column(db.String(32), nullable=False)
    surname = Column(db.String(32), nullable=False)
    email = Column(db.String(120), nullable=False)
    number = Column(db.String(15), nullable=True)
    comments = Column(db.Text, nullable=True)
    created = Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    appointments = relationship('Appointment', cascade='all, delete-orphan',
        backref='customers',
        lazy=True,
        order_by='Appointment.date')

    def __repr__(self) -> str:
        return f'<Appointment({self.id!r} {self.name!r} {self.surname!r})>'

    @property
    def jsonify(self):
        return {
            'id':       self.id,
            'name':     self.name,
            'surname':  self.surname,
            'email':    self.email,
            'number':   self.number,
        }
