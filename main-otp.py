#!/usr/bin/env python3

from sqlalchemy.orm import sessionmaker
from functions import *
import argparse, sys, pyotp


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("--user", action="store", dest="user", help="username")
parser.add_argument("--code", action="store", dest="code", help="otp code")
# parser.add_argument("--one_code", action="store", dest="one_time_code", help="one time code")
args = parser.parse_args()

if args.user:
    username = args.user
else:
    print("can't process without user")
    sys.exit(1)
if args.code:
    code = args.code
else:
    code = ""
    print("can't process without code")
    sys.exit(1)
# if args.one_code:
#     one_time_code = args.one_code
# else:
#     one_time_code = 0

DBSession = sessionmaker(bind=engine)
session = DBSession()
db_one_time_codes = session.query(User.one_time_code).filter(User.vpn_username == username).one()
db_one_time_codes_as_list = db_one_time_codes[0].split(",")
try:
    db_one_time_codes_as_list.index(code)
    db_one_time_codes_as_list.remove(code)
    if len(db_one_time_codes_as_list) == 0:
        db_one_time_codes_as_list = generateNewReserveCodes()
    new_one_time_codes_field = ','.join([str(elem) for elem in db_one_time_codes_as_list])
    session.query(User.one_time_code).filter(User.vpn_username == username).update({User.one_time_code: str(new_one_time_codes_field)})
    session.flush()
    session.commit()
    one_time_code_authorized = 1
    print("Auth-Type = Accept\n")
except:
    one_time_code_authorized = 0

if one_time_code_authorized == 0:
    pin = session.query(User.pin).filter(User.vpn_username == username).one()[0]
    hotp = pyotp.TOTP(pin)

    if hotp.verify(code, valid_window=1):
        print("Auth-Type = Accept\n")
    else:
        print("Auth-Type = Denied\n")

