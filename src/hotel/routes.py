from flask import jsonify, Blueprint, request
from .models import Reservation, Chambre, Client, Status, Type
from .database import db
from sqlalchemy import and_
from .utils import send_error, send_success

main = Blueprint('main', __name__)

@main.route('/api/chambres/disponibles', methods=['GET'])
def chambres_disponibles():
  date_arrivee = request.args.get('date_arrivee')
  date_depart = request.args.get('date_depart')

  if date_arrivee is None or date_depart is None:
    return send_error('date_arrivee et date_depart requis'), 400
  
  chambres = Chambre.query.filter(~Chambre.reservations.any(and_(Reservation.date_arrivee <= date_depart, Reservation.date_depart >= date_arrivee))).all() 

  return jsonify([chambre.format for chambre in chambres])

@main.route('/api/reservations', methods=['POST'])
def creer_reservations():
  data = request.get_json()

  id_client, id_chambre, date_arrivee, date_depart = data.get('id_client'), data.get('id_chambre'), data.get('date_arrivee'), data.get('date_depart')
  
  if id_client is None or id_chambre is None or date_arrivee is None or date_depart is None:
    return send_error(
      "id_client, id_chambre, date_arrivee et date_depart requis."
    ), 400
  
  
  if not Client.query.get(id_client):
    return send_error(
    "Client introuvable."
    ), 404
  
  if not Chambre.query.get(id_chambre):
    return send_error(
    "Chambre introuvable."
    ), 404
  
  chambre = Chambre.query.get(id_chambre)

  if not chambre:
    return send_error(
    "Chambre introuvable."
    ), 404

  chambres = chambre.query.filter(Chambre.id == id_chambre, Chambre.reservations.any(and_(Reservation.date_arrivee <= date_depart, Reservation.date_depart >= date_arrivee))).all()

  if len(chambres) > 0:
    return send_error(
    "La chambre est déjà réservée pour cette période."
    ), 400
  
  reservation = Reservation(id_client=id_client, id_chambre=id_chambre, date_arrivee=date_arrivee, date_depart=date_depart, status=Status.en_attente)
  db.session.add(reservation)
  db.session.commit()

  return send_success("Réservation créée avec succès.")

@main.route('/api/reservations/<int:id>', methods=['DELETE'])
def annuler_reservation(id):
  reservation = Reservation.query.get(id)

  if not reservation:
    return send_error(
    "Réservation introuvable."
    ), 404


  db.session.delete(reservation)
  db.session.commit()

  return send_success("Réservation annulée avec succès.")

@main.route('/api/chambres', methods=['POST'])
def creer_chambre():
  data = request.get_json()

  numero, type, prix = data.get('numero'), data.get('type'), data.get('prix')

  if numero is None or type is None or prix is None:
    return send_error(
      "numero, type et prix requis."
    ), 400
  
  types = [enum_type.name for enum_type in Type]
  
  if type not in types:
    return send_error(
    f"Type invalide. Les types valides sont: {', '.join(types)}"
    ), 400
  
  if Chambre.query.filter_by(numero=numero).first():
    return send_error(
    "Chambre déjà existante."
    ), 400
  
  chambre = Chambre(numero=numero, type=type, prix=prix)
  db.session.add(chambre)
  db.session.commit()

  return send_success("Chambre ajoutée avec succès.")

@main.route('/api/chambres/<int:id>', methods=['PUT','DELETE'])
def chambre(id):
  if request.method == 'DELETE':
    chambre = Chambre.query.get(id)

    if not chambre:
      return send_error(
      "Chambre introuvable."
      ), 404

    db.session.delete(chambre)
    db.session.commit()

    return send_success("Chambre supprimée avec succès.")
  
  data = request.get_json()

  chambre = Chambre.query.get(id)

  if not chambre:
    return send_error(
    "Chambre introuvable."
    ), 404
  
  numero, type, prix = data.get('numero'), data.get('type'), data.get('prix')

  if numero is None or type is None or prix is None:
    return send_error(
      "numero, type et prix requis."
    ), 400
  
  types = [enum_type.name for enum_type in Type]

  if type not in types:
    return send_error(
    f"Type invalide. Les types valides sont: {', '.join(types)}"
    ), 400

  if Chambre.query.filter_by(numero=numero).first():
    return send_error(
    "Ce numéro de chambre est déjà pris."
    ), 409

  chambre.numero, chambre.type, chambre.prix = data.get('numero'), data.get('type'), data.get('prix')
  db.session.commit()

  return send_success("Chambre mise à jour avec succès.")