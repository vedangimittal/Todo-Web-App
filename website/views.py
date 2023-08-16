from flask import Flask, Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_login import current_user, login_required
import pymongo
from bson.objectid import ObjectId

views = Blueprint('views', __name__)

client = pymongo.MongoClient("localhost", 27017)
database = client['todo_webapp']
collection_user = database['users']
new_database = client['user_todo']

@views.route("/todo", methods=["GET", "POST"])
@login_required
def todo():

    note = request.form.get('note')
    new_collection = new_database[current_user.get_id()]  
    all_notes = new_collection.find()
     
    if request.method == 'POST':

        all_notes = new_collection.find()
        
        new_collection.insert_one({"todo":note})
        flash("Note added in Todo!", category='success') 

    return render_template('todo.html', user=current_user, all_notes=all_notes)

@views.route('/delete')
@login_required
def delete():
    
    new_collection = new_database[current_user.get_id()]

    key=request.args.get("_id")    
    new_collection.delete_one({"_id":ObjectId(key)})       

    return redirect("/todo")

