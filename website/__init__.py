from flask import Flask, Blueprint
import pymongo
from flask_login import LoginManager

client = pymongo.MongoClient("localhost", 27017)
database = client['todo_webapp']
collection_user = database['users']

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aa'

    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix = "/")
    app.register_blueprint(views, url_prefix = "/")

    class User:
        def __init__(self, username):
            self.username = username

        @staticmethod
        def is_authenticated():
            return True

        @staticmethod
        def is_active():
            return True

        @staticmethod
        def is_anonymous():
            return False

        def get_id(self):
            return self.username

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(username):
        u = collection_user.find_one({"username": username})
        if not u:
            return None
        return User(username=u['username'])

    return app