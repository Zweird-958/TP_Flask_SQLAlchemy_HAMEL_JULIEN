from flask import Flask
from flask_migrate import Migrate
from .database import db
from .models import Reservation, Chambre, Client

migrate = Migrate()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = "secret-key"
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@db/hotel'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


  db.init_app(app)
  migrate.init_app(app, db)

  from .routes import main
  app.register_blueprint(main)

  return app


