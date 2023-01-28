from flask import Flask
from pyhash import fnv1a_32

app = Flask(__name__)
hash = fnv1a_32()

ROUND_TRIP = 29132
KM_TO_MI = 0.6213712
num_format = "{:,.0f}"

def validate_key(key):
    from os.path import exists
    from flask import abort

    if not key:
        return

    try:
        int(key, base=16)
    except ValueError:
        abort(400)

    if not exists(f"poems/{key}.txt"):
        abort(404)

def response_plain(text):
    from flask import make_response
    resp = make_response(text)
    resp.headers["Content-type"] = "text/plain"
    return resp

@app.route("/", methods=["GET"])
@app.route("/<key>", methods=["GET"])
def poem_view(key=""):
    from flask import render_template
    validate_key(key)

    poem = ""
    stats = {}
    if key:
        poem = open(f"poems/{key}.txt", 'r', encoding='utf-8').read()
        lines = poem.splitlines()[1:]
        words = sum([len(l.split()) for l in lines])
        breaks = len(lines) - 1
        posts = words + breaks
        km = posts * ROUND_TRIP
        mi = km * KM_TO_MI

        stats = dict(words=words, lines=breaks,
                roundtrip=num_format.format(ROUND_TRIP),
                km=num_format.format(km),
                mi=num_format.format(mi),
                )

    return render_template("index.html", key=key, poem=poem, stats=stats)

@app.route("/poem/<key>", methods=["GET"])
def poem_get(key):
    validate_key(key)

    if not key:
        return response_plain("")
    return response_plain(open(filename, 'r', encoding='utf-8').read())

@app.route("/poem/", methods=["POST"])
@app.route("/poem/<key>", methods=["POST"])
def poem_post(key=""):
    from flask import request

    validate_key(key)

    poem = ""
    if key:
        poem = open(f"poems/{key}.txt", 'r', encoding='utf-8').read()

    addend = request.get_data(as_text=True)
    if addend != "\n":
        addend = addend.split()[0]
        poem = f"{poem}{addend} "
    else:
        poem += "\n"

    newhash = "{0:08x}".format(hash(poem.encode('utf-8')))

    with open(f"poems/{newhash}.txt", 'w', encoding='utf-8') as f:
        f.write(poem)

    return response_plain(newhash)
