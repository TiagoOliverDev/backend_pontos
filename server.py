from flask import Flask
from flask_bcrypt import Bcrypt
from app.routes import routes_blueprint
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# Carregar configuração com base no ambiente
if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object('config.production')
    print('produção')
else:
    app.config.from_object('config.development')
    print('desenvolvimento')

bcrypt = Bcrypt(app)
app.register_blueprint(routes_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1010, debug=app.config['DEBUG'])




