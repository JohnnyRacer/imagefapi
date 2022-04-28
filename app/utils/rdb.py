import redis

class BaseDB:
    redis_host = "localhost"
    redis_port= 6379
    pass

class ImageUserDB(BaseDB):
    def __init__(self):
        pass