from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS  # Importar CORS

app = Flask(__name__)
CORS(app)  # Permitir solicitudes de cualquier origen

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Jaztri20.@localhost/eventos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# MODELO de la tabla eventos
class Evento(db.Model):
    __tablename__ = 'eventos'  # tabla ya existente en tu base de datos
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    imagen_url = db.Column(db.Text)

    def __init__(self, titulo, descripcion, imagen_url):
        self.titulo = titulo
        self.descripcion = descripcion
        self.imagen_url = imagen_url

# ESQUEMA para serializar datos
class EventoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Evento

evento_schema = EventoSchema()
eventos_schema = EventoSchema(many=True)

# RUTAS DEL API

@app.route("/")
def inicio():
    return "API de eventos funcionando correctamente"

# GET - Ver todos los eventos
@app.route("/eventos", methods=["GET"])
def get_eventos():
    eventos = Evento.query.all()
    return eventos_schema.jsonify(eventos)  # Devolver los eventos serializados como JSON

# GET - Ver un solo evento
@app.route("/eventos/<int:id>", methods=["GET"])
def get_evento(id):
    evento = Evento.query.get(id)
    if evento:
        return evento_schema.jsonify(evento)  # Devolver el evento específico serializado
    else:
        return jsonify({"mensaje": "Evento no encontrado"}), 404

# POST - Agregar un evento nuevo
@app.route("/eventos", methods=["POST"])
def add_evento():
    titulo = request.json['titulo']
    descripcion = request.json['descripcion']
    imagen_url = request.json['imagen_url']
    nuevo_evento = Evento(titulo, descripcion, imagen_url)
    db.session.add(nuevo_evento)
    db.session.commit()
    return evento_schema.jsonify(nuevo_evento)

# PUT - Actualizar evento
@app.route("/eventos/<int:id>", methods=["PUT"])
def update_evento(id):
    evento = Evento.query.get(id)
    if evento:
        evento.titulo = request.json['titulo']
        evento.descripcion = request.json['descripcion']
        evento.imagen_url = request.json['imagen_url']
        db.session.commit()
        return evento_schema.jsonify(evento)
    else:
        return jsonify({"mensaje": "Evento no encontrado"}), 404

# DELETE - Eliminar evento
@app.route("/eventos/<int:id>", methods=["DELETE"])
def delete_evento(id):
    evento = Evento.query.get(id)
    if evento:
        db.session.delete(evento)
        db.session.commit()
        return jsonify({"mensaje": "Evento eliminado correctamente"})
    else:
        return jsonify({"mensaje": "Evento no encontrado"}), 404

# INICIAR API
if __name__ == "__main__":
    app.run(debug=True)
