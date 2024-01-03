from flask_migrate import Migrate
from flask import request
from flask_restful import Resource
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import generate_password_hash
from config import app, db, api
import datetime
import traceback

migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
