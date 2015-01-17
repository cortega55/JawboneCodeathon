from force import app
from flask import redirect, request, make_response
from redis import Redis
import requests
from jawbone.jawbone import Jawbone

client_id = "KOls4_kxR_Q"
client_secret = "d84b648530a3aa9029322c37fa77c75ce64664a4"
redirect_uri = "http://192.168.59.103/login"
scope = "basic_read,extended_read,location_read"
token = None


@app.route("/")
def root():
    jb = Jawbone(client_id, client_secret, redirect_uri, scope)
    auth = jb.auth()
    return redirect(auth)


@app.route("/login")
def login():
    code = request.args.get("code")
    if not code:
        return make_response("Not authenticated!", 501)

    jb = Jawbone(client_id, client_secret, redirect_uri, scope)
    token = jb.access_token(code)
    access_token = token["access_token"]
#    refresh_token = token["refresh_token"]

    endpoint = "/nudge/api/v.1.1/users/@me"

    headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {0}'.format(access_token)
        }

    response = requests.get("https://jawbone.com/nudge/api/v.1.1/users/@me", headers=headers)

    print
    print response.json()

    redis = Redis(host="redis_1", port=6379)
    redis.incr("hits")

    return make_response("Success! ({0})".format(redis.get("hits")), 200)
