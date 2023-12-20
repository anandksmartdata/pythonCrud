from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.cli import FlaskGroup
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import secrets
import os

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key


db = SQLAlchemy(app)
migrate = Migrate(app, db)
# manager = Manager(app, db)
# manager.add_command('db', MigrateCommand)
cli = FlaskGroup(app)
# Add the MigrateCommand to the FlaskGroup
# cli.add_command('db', MigrateCommand)
# cli = FlaskGroup(app)


bcrypt = Bcrypt(app)
CORS(app)

