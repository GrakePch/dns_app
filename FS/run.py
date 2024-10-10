from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)


def fib(n):
    if n <= 0:
        return 0
    if n == 1 or n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)


@app.route("/register", methods=["PUT"])
def register():
    data = request.get_json()
    if not data:
        abort(400)

    as_ip = data.get("as_ip")
    as_port = data.get("as_port")
    registration_message = {
        "TYPE": "A",
        "NAME": data.get("hostname"),
        "VALUE": data.get("ip"),
        "TTL": 10,
    }

    udp_url = f"http://{as_ip}:{as_port}/register"
    response = requests.post(udp_url, json=registration_message)

    if response.status_code == 201:
        return "Registered", 201
    else:
        return "Registration Failed", 400


@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    try:
        x = int(request.args.get("number"))
        return jsonify({"fibonacci": fib(x)}), 200
    except:
        abort(400)


app.run(host="0.0.0.0", port=9090, debug=True)
