from flask import jsonify


class CorsOptions:
    def _build_cors_preflight_response():
        response = jsonify({'status': 'ok'})       
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")  # Permitir todos os cabeçalhos
        response.headers.add("Access-Control-Allow-Methods", "*")  # Permitir todos os métodos
        return response
