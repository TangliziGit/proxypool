import redis
import json
from flask import Flask

DB_HOST='localhost'
DB_PORT=6379
DB_ID=1
DB_IPPOOL_NAME="ProxyPool:IPPOOL"

WEB_IP='0.0.0.0'
WEB_PORT=3000

app=Flask(__name__)
rdb=redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID)

@app.route('/getip')
def getip():
    global rdb
    ippool=rdb.zrange(DB_IPPOOL_NAME, 0, -1)
    ippool=[x.decode('utf-8') for x in ippool]
    return json.dumps(ippool)

if __name__=='__main__':
    app.run(WEB_IP, WEB_PORT)
