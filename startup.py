import uvicorn
import sys

args = sys.argv

port=5000

if __name__ == '__main__':
    
    try:
        assert args[2].isnumeric(), "Only integer input for the port number"
        port=int(args[2])
    except:
        pass

    uvicorn.run('app.main:app', proxy_headers=True,forwarded_allow_ips='*',port=5000 ,reload=True)