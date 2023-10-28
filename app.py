from flask import Flask, render_template, redirect, url_for, flash, request, send_file, Response, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = "super secret key"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    contact = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, name, prenom, email, contact, password):
        self.name = name
        self.prenom = prenom
        self.email = email
        self.contact = contact
        self.password = password



@app.route("/")
def index():
    return render_template("index.html")



with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("Erreur creation")




if __name__ == "__main__":
    app.run(debug=True)