from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/electronics'
db = SQLAlchemy(app)


class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    model = db.Column(db.String(200))
    price = db.Column(db.Float)

    def to_json(self):
        return {"id": self.id, "model": self.model, "price": self.price}

# Select all notebooks
@app.route("/notebooks", methods=["GET"])
def select_notebooks():
    notebooks_obj = Notebook.query.all()
    notebooks_json = [notebook.to_json() for notebook in notebooks_obj]

    return generate_response(200, "notebooks", notebooks_json)
# Select notebook by id
@app.route("/notebook/<id>", methods=["GET"])
def select_notebook_by_id(id):
    
    try:
        notebooks_obj = Notebook.query.filter_by(id=id).first()
        notebooks_json = notebooks_obj.to_json()
        return generate_response(200, "notebook", notebooks_json)
    
    except Exception as e:
        print('Error: ', e)
        return generate_response(400, "notebook", {}, "Notebook not found")

# Create users
@app.route("/notebook", methods=["POST"])
def create_notebook():
    body = request.get_json()

    try:
        notebook = Notebook(model=body["model"], price= body["price"])
        db.session.add(notebook)
        db.session.commit()
        return generate_response(201, "notebook", notebook.to_json(), "Successfully created")
    except Exception as e:
        print('Error: ', e)
        return generate_response(400, "notebook", {}, "Error when Registering")

# Update users
@app.route("/notebook/<id>", methods=["PUT"])
def update_notebook(id):
    notebook_obj = Notebook.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('model' in body):
            notebook_obj.model = body['model']
        if('price' in body):
            notebook_obj.price = body['price']
        
        db.session.add(notebook_obj)
        db.session.commit()
        return generate_response(200, "notebook", notebook_obj.to_json(), "Successfully updated")
    except Exception as e:
        print('Error: ', e)
        return generate_response(400, "notebook", {}, "Error when Registering")

# Delete users
@app.route("/notebook/<id>", methods=["DELETE"])
def delete_notebook(id):
    notebook_obj = Notebook.query.filter_by(id=id).first()

    try:
        db.session.delete(notebook_obj)
        db.session.commit()
        return generate_response(200, "notebook", notebook_obj.to_json(), "Successfully deleted")
    except Exception as e:
        print('Erro', e)
        return generate_response(400, "notebook", {}, "Error when Registering")


def generate_response(status, content_name, content, message=False):
    body = {}
    body[content_name] = content

    if(message):
        body["message"] = message

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()