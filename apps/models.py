# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Devices(db.Model):

    __tablename__ = 'Devices'

    id = db.Column(db.Integer, primary_key=True)

    #__Devices_FIELDS__
    serial = db.Column(db.Text, nullable=True)
    model = db.Column(db.Text, nullable=True)
    inst_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    site = db.Column(db.Text, nullable=True)
    coord = db.Column(db.Text, nullable=True)
    ssid_ap = db.Column(db.Text, nullable=True)
    pass_ap = db.Column(db.Text, nullable=True)
    ssid_site = db.Column(db.Text, nullable=True)
    pass_site = db.Column(db.Text, nullable=True)
    ip_wifi = db.Column(db.Text, nullable=True)
    gateway_wifi = db.Column(db.Text, nullable=True)
    ip_eth = db.Column(db.Text, nullable=True)
    gateway_eth = db.Column(db.Text, nullable=True)
    user_config = db.Column(db.Text, nullable=True)
    pass_config = db.Column(db.Text, nullable=True)
    inst_city = db.Column(db.Text, nullable=True)
    last_online = db.Column(db.DateTime, default=db.func.current_timestamp())
    alarm_state_in = db.Column(db.Boolean, nullable=True)
    armed_state_in = db.Column(db.Boolean, nullable=True)
    armed_order_out = db.Column(db.Boolean, nullable=True)
    alarm_panel_order_out = db.Column(db.Boolean, nullable=True)
    energizer_model = db.Column(db.Text, nullable=True)

    #__Devices_FIELDS__END

    def __init__(self, **kwargs):
        super(Devices, self).__init__(**kwargs)


class Users(db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)

    #__Users_FIELDS__
    name = db.Column(db.Text, nullable=True)
    registered_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    role = db.Column(db.Text, nullable=True)

    #__Users_FIELDS__END

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)


class History(db.Model):

    __tablename__ = 'History'

    id = db.Column(db.Integer, primary_key=True)

    #__History_FIELDS__
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    event = db.Column(db.Text, nullable=True)
    serial_device = db.Column(db.Text, nullable=True)
    readed_state = db.Column(db.Text, nullable=True)

    #__History_FIELDS__END

    def __init__(self, **kwargs):
        super(History, self).__init__(**kwargs)



#__MODELS__END
