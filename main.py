from flask import Flask
from flask_cors import CORS

from app.routes.expediente_routes import expediente_bp
from app.routes.usuario_routes import usuario_bp
from app.routes.acta_proclamacion_routes import  acta_proclamacion_bp
from app.routes.acta_reunion_routes import  acta_reunion_bp
from app.routes.asistencia_routes import asistencia_bp
from app.routes.citacion_routes import citacion_bp
from app.routes.comision_routes import comision_bp
from app.routes.disposicion_routes import disposicion_bp
from app.routes.estadistica_routes import estadistica_bp
from app.routes.notificacion_routes import notificacion_bp
from app.routes.reunion_routes import reunion_bp
from app.routes.tema_routes import tema_bp
from app.routes.temario_routes import temario_bp
from app.routes.auth_routes import auth_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.votacion_routes import votacion_bp
from app.routes.consejero_routes import (consejero_bp)
from app.routes.licencia_routes import (licencia_bp)
from app.routes.constitucion_routes import (constitucion_bp)
from app.routes.comision_consejero_routes import (comision_consejero_bp)


app = Flask(__name__)

CORS(app)

@app.route("/")
def home():
    return "Backend funcionando ✅"

app.register_blueprint(expediente_bp, url_prefix="/api")
app.register_blueprint(usuario_bp, url_prefix="/api")
app.register_blueprint(acta_proclamacion_bp, url_prefix="/api")
app.register_blueprint(acta_reunion_bp, url_prefix="/api")
app.register_blueprint(asistencia_bp, url_prefix="/api")
app.register_blueprint(citacion_bp, url_prefix="/api")
app.register_blueprint(comision_bp, url_prefix="/api")
app.register_blueprint(disposicion_bp, url_prefix="/api")
app.register_blueprint(estadistica_bp, url_prefix="/api")
app.register_blueprint(notificacion_bp, url_prefix="/api")
app.register_blueprint(reunion_bp, url_prefix="/api")
app.register_blueprint(tema_bp, url_prefix="/api")
app.register_blueprint(temario_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(dashboard_bp, url_prefix="/api")
app.register_blueprint(votacion_bp, url_prefix="/api")
app.register_blueprint(consejero_bp, url_prefix="/api")
app.register_blueprint(licencia_bp, url_prefix="/api")
app.register_blueprint(constitucion_bp, url_prefix="/api")
app.register_blueprint(comision_consejero_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)