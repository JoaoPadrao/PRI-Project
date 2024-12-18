#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template
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

        min_year = params.get("minYear")
        max_year = params.get("maxYear")

        payload = {
            "q": params.get("q"),
            "q.op": params.get("q_op", "AND"),
            "start": params.get("start", 0),
            "rows": params.get("rows", 10),
            "defType": params.get("defType", "edismax"),
            "qf": params.get("qf", "Description^5 Participants^4 Country^3 Name_War^2 Winner")
        }

        if min_year is not None and max_year is not None:
            payload["fq"] = f"Year:[{min_year} TO {max_year}]"

        app.logger.debug(f"Payload: {payload}")

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


@app.route("/battle-detail/<battle_id>")
def battle_detail(battle_id):
    try:
        # Buscar detalhes da batalha no Solr
        uri = "http://localhost:8983/solr/wikiwar/select"
        params = {
            "q": f"ID:{battle_id}",
            "rows": 1,
        }

        response = requests.get(uri, params=params)
        data = response.json()
        print("CONSULTA", data)
        if data['response']['numFound'] == 0:
            return "Battle not found", 404

        # Extrair os detalhes da batalha
        battle = data['response']['docs'][0]
        
        return render_template('battle_detail.html', battle=battle)
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching battle details: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)