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
        # Get JSON data from request
        data = request.json
        solr_uri = data.get("uri", "http://localhost:8983/solr")
        collection = data.get("collection", "wikiwar")
        params = data.get("params")

        # Construct the Solr request URL
        uri = f"{solr_uri}/{collection}/select"

        # Query Solr
        response = requests.post(uri, json=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Return Solr results
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)