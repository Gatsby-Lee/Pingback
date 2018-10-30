"""
@author Gatsby Lee
@since 2018-10-29
"""
import logging
import os
import redis

from flask import Flask, request

from pbpy.cexception import IntegrityError
from pbpy.applogic import PingbackApp
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_DB = int(os.environ.get('REDIS_DB', 0))
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
REDIS_CLIENT = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,
                                 password=REDIS_PASSWORD)

RESPONSE_HEADER = {"content-type": "application/json; charset=utf-8"}
HELLO_PINGBACK = '[200, "Hello Pingback Service."]'

@app.route('/')
def home():
    """Return a friendly HTTP greeting."""
    return (HELLO_PINGBACK, 200, RESPONSE_HEADER)


@app.route('/pingback')
def pingback():
    """Responds to any HTTP request.
    @note possible request
    http://your-server.com/pingscript?taskId=$task_id
    http://your-server.com/pingscript?taskId=$task_id&postId=$post_id
    """

    try:
        pingback_src = request.path[1:].replace('-', '_')
        task_id = None
        try:
            task_id = request.args['taskId']
        except KeyError:
            logging.warn('taskId param is NOT provided. pingback_src=%s', pingback_src)
            return ('[400, ["FAIL", "taskId param is required."]]', 400, RESPONSE_HEADER)

        post_id = '-1'
        try:
            post_id = request.args['postId']
        except KeyError:
            pass

        try:
            PingbackApp.add_pingback(REDIS_CLIENT, pingback_src, (task_id, post_id))
            b = '[200, ["OK", ["%s", "%s"]]]' % (task_id, post_id)
            return (b, 200, RESPONSE_HEADER)
        except IntegrityError:
            logging.warn('Duplicated entry exists: pingback_src=%s,taskId=%s,postId=%s',
                         pingback_src, task_id, post_id)
            return ('[409, ["FAIL", "Duplicated Entry"]]', 409, RESPONSE_HEADER)
    except Exception as e:
        logging.exception(e)
        return ('[500, ["FAIL", "Server Error"]]', 500, RESPONSE_HEADER)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
