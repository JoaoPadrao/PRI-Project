#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
CORS(app)

@app.route("/query-solr", methods=["POST"])
def query_solr():
    app.logger.info(f"Request received: {request.json}")
    try:
        data = request.json
        solr_uri = data.get("uri", "http://localhost:8983/solr")
        collection = data.get("collection", "wikiwar")
        params = data.get("params")

        uri = f"{solr_uri}/{collection}/select"

        payload = {
            "q": params.get("q"),
            "q.op": params.get("q_op", "AND"),
            "start": params.get("start", 0),
            "rows": params.get("rows", 10),
            "defType": params.get("defType", "edismax"),
            "qf": params.get("qf", "Description^5 Participants^4 Country^3 Name_War^2 Winner")
        }


        response = requests.get(uri, params=payload) 
        app.logger.debug(f"Response: {response.text}")

        response.raise_for_status()  

        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Erro na requisição ao Solr: {e}")
        return jsonify({"error": "Erro na requisição ao Solr", "message": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Erro desconhecido: {e}")
        return jsonify({"error": "Erro desconhecido", "message": str(e)}), 500


# Add CORS headers to all responses
# @app.after_request
# def add_cors_headers(response):
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     return response

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)