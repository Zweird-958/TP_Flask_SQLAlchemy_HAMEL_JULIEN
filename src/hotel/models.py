import enum
from sqlalchemy.ext.hybrid import hybrid_property
from .database import db

class Status(enum.Enum):
  en_attente = 'en attente'
  confirmee = 'confirmée'

class Type(enum.Enum):
  simple = 'simple'
  double = 'double'
  suite = 'suite'

class Client(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nom = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  reservations = db.relationship('Reservation', backref='client', lazy=True, cascade="all")

class Chambre(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  numero = db.Column(db.Integer, unique=True ,nullable=False)
  type = db.Column(db.Enum(Type), nullable=False)
  prix = db.Column(db.Float, nullable=False)
  reservations = db.relationship('Reservation', backref='chambre', lazy=True, cascade="all")

  @hybrid_property
  def format(self):
    return {
      'id': self.id,
      'numero': self.numero,
      'type': self.type.value,
      'prix': self.prix,
    }

class Reservation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
  id_chambre = db.Column(db.Integer, db.ForeignKey('chambre.id'), nullable=False)
  date_arrivee = db.Column(db.DateTime, nullable=False)
  date_depart = db.Column(db.DateTime, nullable=False)
  status = db.Column(db.Enum(Status), nullable=False)