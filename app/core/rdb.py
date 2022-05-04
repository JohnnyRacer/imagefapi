from ctypes import Union
from hashlib import sha256
import os
from typing import Optional
import redis
from app.core import config


#class IdentificationError(Exception):

ret_self = lambda ret_obj: ret_obj

class Redis:
    redis_host = "localhost"
    redis_port= 6379
    pass

class RedisInstance(Redis):
    
    def __init__(self) -> None:
        super(Redis).__init__()

class MockInstance:

    def __init__(self, imported_user_ids: list = [],imported_forbiddens: list = []) -> None:
        self.user_ids : list(str) = imported_user_ids
        self.invalid_ids : list(str) = imported_forbiddens
        self.userdb : dict = {}
        self.udb_keys : list(str) = ["uploaded", "saved", "uploaded_hashes","storage_used"]
        self.uld_keys : list(str) = ["svdir", "image_size", "timestamp", "format","tags"]
        self.last_update : float = 0

    check_usrid = lambda self, user_id : len(user_id) == (config.USER_ID_LEN or 64) and user_id.isalnum()      
    
    def uid_insert(self,user_id:str) -> None:

        if user_id not in list(self.userdb):
            self.userdb[user_id] = {} # Creates an empty entry for the user ID if none exists
        
    def uid_remove(self, user_id:str) -> None:
        
        if user_id in self.user_ids:
            del self.userdb[user_id]

    udb_init = lambda self, user_id, uploaded={},storage_used=0: self.userdb.update(zip([user_id], [dict(zip(self.udb_keys,[uploaded,uploaded,storage_used]))])) 

    uld_init = lambda self,svdir, image_size=0, timestamp=0, fmt="bin",tags=[]: dict(zip(self.uld_keys, [svdir, image_size, timestamp, fmt,tags]))

    uld_insert = lambda self,user_id , image_hash, uld : self.userdb.update(zip([user_id], [{image_hash:uld}] ))

    gen_userid = lambda self :  sha256(os.urandom(256)).hexdigest() if config.USER_ID_LEN == 0 or config.USER_ID_LEN >= 64 else sha256(os.urandom(256)).hexdigest()[config.USER_ID_LEN - 64 : ]

class ImageUserDB:
    def __init__(self):
        pass

database = MockInstance()


"""
tg_userid = database.gen_userid()

tg_img_hash = 'abcdef'

tg_img_svdir = '/tmp/image.png'

database.udb_init(tg_userid)

adict = database.uld_init(tg_img_svdir)

database.uld_insert(tg_userid, tg_img_hash,adict)

print(database.userdb[tg_userid])

"""