import json
import logging
import os
import re
import sys
import xmltodict

from collections import defaultdict
from flask import Flask
from flask import jsonify
from flask import request

from flask_log_request_id import RequestID
from flask_log_request_id import RequestIDLogFilter

verbs = ['get', 'post', 'delete', 'put', 'patch']
routes = {v: defaultdict(dict) for v in verbs}

app = Flask(__name__)
RequestID(app)

logging.basicConfig(level='INFO', stream=sys.stderr)
handler = logging.getLogger().handlers[0]
handler.addFilter(RequestIDLogFilter())
handler.setFormatter(logging.Formatter(
    "%(asctime)s:%(request_id)s:%(levelname)s:%(name)s:%(lineno)d:%(funcName)s:%(message)s"))
logging.getLogger().addHandler(handler)

logger = logging.getLogger()


@app.route("/", defaults={'path': ''}, methods=['get', 'post', 'put', 'patch', 'delete'])
@app.route("/<path:path>", methods=['get', 'post', 'put', 'patch', 'delete'])
def catch_all(path, *args, **kwargs):
    verb = request.method
    path = "/" + path.replace("//", "/")
    file_to_serve = routes[verb.lower()].get(path, False)
    if file_to_serve:
        return render_json(file_to_serve)
    else:
        for key, file_path in routes[verb.lower()].iteritems():
            if re.match(key, path):
                matches = re.search(key, path)
                return render_json(file_path, **matches.groupdict())

    return jsonify({
        "message": "Not Found"
    }), 404


def render_json(path, **kwargs):
    with open(path, "r") as f:
        if path.lower().endswith('.xml'):
            d = xmltodict.parse(f.read())
        else:
            d = json.load(f)
        return jsonify(d), 200


def discover_routes(path, base_dir=None):
    base_dir = base_dir if base_dir is not None else path
    for f in os.listdir(path):
        fullpath = os.path.join(path, f)
        if os.path.isdir(fullpath):
            discover_routes(fullpath, base_dir)
        elif os.path.isfile(fullpath):
            filename, ext = f.split(".")
            if filename in verbs:
                comps = fullpath.split("/")
                route = "/".join(["(?P<" + c.strip(":") + ">.*)" if ":" in c else c for c in comps[:-1]])
                route = route.replace(base_dir, "")
                routes[filename][route] = fullpath


@app.before_request
def before():
    logger.info("request.method, request.path: {}, {}".format(request.method, request.path))
    logger.info("request.headers: {}".format(request.headers))
    logger.info("request.args: {}".format(request.args))
    logger.info("request.form: {}".format(request.form))
    logger.info("request.get_json(): {}".format(request.get_json()))


@app.after_request
def after(response):
    logger.info("response.status_code: {}".format(response.status_code))
    return response


if __name__ == '__main__':
    discover_routes("./apis")
    app.run(debug=True, host="0.0.0.0", port=5000)
