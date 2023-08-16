from flask import Flask, Blueprint, request, redirect, url_for, flash, render_template
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

client = pymongo.MongoClient("localhost", 27017)
database = client['todo_webapp']
collection_user = database['users']

auth = Blueprint('auth', __name__)

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

@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email_id = request.form.get("email_id")
        password = request.form.get("password")

        user = collection_user.find_one({"username":username})
        if user:
            flash(username + " username alreade exists")
            return render_template('signup.html', category="error", user=current_user)
        
        if username=="" or email_id=="" or password=="":
            flash("Please enter all the details.")
            return render_template('signup.html', category="error", user=current_user)
        
        collection_user.insert_one({"username":username, "email_id":email_id, "password":generate_password_hash(password, method="sha256")})
        user = collection_user.find_one({"username":username})
        user_obj = User(username = user['username'])
        login_user(user_obj)
        flash("Account registered", category="success")
        return redirect(url_for('views.todo'))

    return render_template('signup.html', user=current_user)

@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = collection_user.find_one({"username":username})
        if user:
            if check_password_hash(user["password"], password):
                flash("Logged in successfully!", category='success')
                user_obj = User(username = user['username'])
                login_user(user_obj)
                return redirect(url_for('views.todo'))
            else:
                flash("Incorrect password, try again", category='error')
        else:
            flash("User does not exist. Please sign up.", category='error')

    return render_template('login.html', user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))





