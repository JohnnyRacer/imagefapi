import uvicorn
import sys
from argparse import ArgumentParser
from app.core.config import IMG_SAVE_DIR, IMG_CACHE_DIR
import os

argspack = ArgumentParser(description='Image-fastapi startup script help',add_help=True)
argspack.add_argument('-p', '--port', type=int, default=5000, help='Select which port to run the server, defaults to 5000')
argspack.add_argument('-r', '--noreload', type=bool, default=False, help='Select to disable autoreload or not, defaults to False')
argspack.add_argument('-n','--noauth', type=bool,default=False,help='Select to disable authentication on the endpoints or not, defaults to False')
args = argspack.parse_args()

os.path.isdir(IMG_CACHE_DIR) or os.makedirs(IMG_CACHE_DIR,exist_ok=True)
os.path.isdir(IMG_SAVE_DIR) or os.makedirs(IMG_SAVE_DIR,exist_ok=True)
os.environ["API_AUTH_CFG"] = str(int(not args.noauth))

    

if __name__ == '__main__':
    uvicorn.run('app.main:app', proxy_headers=True,forwarded_allow_ips='*',port=args.port ,reload= not args.noreload)