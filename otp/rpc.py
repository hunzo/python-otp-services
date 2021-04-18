from nameko.rpc import rpc
from datetime import timedelta
from validate_email import validate_email
import math
import random
import redis
import string
import os

EXPIRES_MINUTES = os.environ.get("EXPIRES_MINUTES")
REDIS_SERVER = os.environ.get("REDIS_SERVER")


def connect():
    redisConnect = redis.Redis(host=REDIS_SERVER, port=6379)
    return redisConnect


r = connect()


def generate_otp():
    length = 6
    # return ''.join(random.choices(string.ascii_uppercase+string.digits, k=length))
    return ''.join(random.choices(string.digits, k=length))


def val_email(email):
    return validate_email(email)


def exist_key(email):
    if r.exists(email) == 1:
        exits = True
    else:
        exits = False
    return exits


# def create(email):
#     if exist_key(email):
#         return "exits email"


#     otp = generate_otp()
#     r.setex(email, timedelta(seconds=10), str(otp))

#     return {
#         "otp": otp,
#         "chkmail": val_email(email)
#     }


def delete(email):
    success = False
    if exist_key(email):
        r.delete(email)
        success = True
    return True


class OTPServices:
    name = "otp"

    @rpc
    def create(self, email):
        if exist_key(email):
            return "email has exits"

        if not val_email(email):
            return "invalid email format"

        otp = generate_otp()
        r.setex(email, timedelta(minutes=int(EXPIRES_MINUTES)), str(otp))

        return otp

    @rpc
    def delete(self, email):
        success = 0
        if exist_key(email):
            r.delete(email)
            success = 1

        return success

    @rpc
    def authen(self, email, otp):
        success = 0
        if exist_key(email):
            chk = r.get(email)
            otp = bytes(otp, 'utf-8')
            if chk == otp:
                delete(email)
                success = 1
        return success
