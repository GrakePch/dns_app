from flask import Flask, abort, request, jsonify
import requests

app = Flask(__name__)


@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    args = request.args
    hostname = args.get("hostname")
    fs_port = args.get("fs_port")
    number = args.get("number")
    as_ip = args.get("as_ip")
    as_port = args.get("as_port")

    if not all([hostname, fs_port, number, as_ip, as_port]):
        abort(400)

    try:
        number = int(number)
    except ValueError:
        abort(400)

    dns_query_url = f"http://{as_ip}:{as_port}/dns?name={hostname}&type=A"
    dns_response = requests.get(dns_query_url)
    if dns_response.status_code != 200:
        return "DNS Query Failed", 400

    ip_address = dns_response.json().get("VALUE")

    fibonacci_url = f"http://{ip_address}:{fs_port}/fibonacci?number={number}"
    fibonacci_response = requests.get(fibonacci_url)
    if fibonacci_response.status_code != 200:
        return "Fibonacci Query Failed", 400

    return str(fibonacci_response.json().get("fibonacci")), 200


app.run(host="0.0.0.0", port=8080, debug=True)
