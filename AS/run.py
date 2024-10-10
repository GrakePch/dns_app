from flask import Flask, request, jsonify

app = Flask(__name__)


dns_records = {}


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data or data.get("TYPE") != "A":
        return "Bad Request: Invalid data", 400

    dns_records[data.get("NAME")] = {"VALUE": data.get("VALUE"), "TTL": data.get("TTL")}
    return "Registered", 201


@app.route("/dns", methods=["GET"])
def query():
    name = request.args.get("name")
    record_type = request.args.get("type")

    if name in dns_records and record_type == "A":
        record = dns_records[name]
        return jsonify(record), 200
    else:
        return "Not Found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=53533)
