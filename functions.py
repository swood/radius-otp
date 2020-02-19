#!/usr/bin/env python3

import os
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, null
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import random
import configparser

if os.environ.get('DEV'):
    engine = create_engine('sqlite:///vpn_wifi.db', echo=True)
    Base = declarative_base()
else:
    Config = configparser.ConfigParser()
    Config.read("config.ini")
    user = Config.get("connection", "user")
    password = Config.get("connection", "password")
    host = Config.get("connection", "host")
    db = Config.get("connection", "db")
    engine = create_engine('mysql+pymysql://%s:%s@%s/%s' % (user, password, host, db))
    Base = declarative_base()

class User(Base):
    __tablename__ = 'vpnusers'
    vpn_id = Column(Integer, primary_key=True)
    vpn_username = Column(String(255), nullable=False, unique=True, default = 'pass')
    pass_hash = Column(String(20), nullable=False, default = 0)
    staffpass_id = Column(Integer, nullable=True, unique=True, default=null())
    pin = Column(String(255), nullable=True, default=null())
    one_time_code = Column(String(21), nullable=True, default = 0)
    primary = PrimaryKeyConstraint('vpn_id', name = "id_idx")
    def __repr__(self):
       return "<User(name='%s', pin='%s')>" % (self.vpn_username, self.pin)

def generateNewReserveCodes():
    res = list()
    for r in range(0,3):
        code = ""
        c = list()
        for n in range(0,6):
            c.append(random.randint(0,9))
        code = ''.join([str(elem) for elem in c])
        res.append(code)

    return res