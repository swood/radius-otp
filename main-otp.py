#!/usr/bin/env python3

from sqlalchemy.orm import sessionmaker
from functions import *
import argparse, sys, pyotp
import sys


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("--user", action="store", dest="user", help="username")
parser.add_argument("--code", action="store", dest="code", help="otp code")
parser.add_argument("--generate_reserve_codes", action="store_true", dest="generator", help="this option need for initial generating reserve codes for all users")
args = parser.parse_args()
DBSession = sessionmaker(bind=engine)
session = DBSession()

if args.generator:
    generator = args.generator
else:
    generator = False

if generator:
    all_users = session.query(User.vpn_username)
    for username in all_users:
        print(username[0])
        db_one_time_codes_as_list = generateNewReserveCodes()
        try:
            new_one_time_codes_field = ','.join([str(elem) for elem in db_one_time_codes_as_list])
            session.query(User.one_time_code).filter(User.vpn_username == username[0]).update(
                {User.one_time_code: str(new_one_time_codes_field)})
            session.flush()
            session.commit()
        except:
            print("can't update one_time_codes for user %s" % username)
    print("All user has been updated")
else:
    if args.user:
        username = args.user
    else:
        print("can't process without user")
        sys.exit(1)
    if args.code:
        code = args.code
    else:
        code = ""

    db_one_time_codes = session.query(User.one_time_code).filter(User.vpn_username == username).one()
    is_2fa_disabled = session.query(User.skip_2fa).filter(User.vpn_username == username).one()
    db_one_time_codes_as_list = db_one_time_codes[0].split(",")
    if is_2fa_disabled[0] == 0:
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

            if hotp.verify(code):
                print("Auth-Type = Accept\n")
                sys.exit(0)
            else:
                print("Auth-Type = Denied\n")
                sys.exit(1)
    else:
        print("Auth-Type = Accept\n")
        sys.exit(0)
