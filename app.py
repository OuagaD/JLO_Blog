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


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    content = db.Column(db.Text)

    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content
    


with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("Erreur creation")



@app.route("/")
def index():
    return render_template("index.html")



@app.route('/inscription', methods=['GET'])
def inscript():
    return render_template('inscription.html')

@app.route('/inscription',methods=['POST'])
def inscription():
    if request.method == 'POST':
        name= request.form.get('nom')
        prenom = request.form.get('prenom')
        email= request.form.get('email')
        contact= request.form.get('contact')
        password= request.form.get('motpass')
        new_user = User(name, prenom, email, contact, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('seconnecter'))
    else:
        return render_template('inscription.html')






@app.route('/connect', methods=['GET'])
def connex():
    return render_template('seconnecter.html')


@app.route('/connect', methods=['POST'])
def seconnecter():
    #new_user = User.query.all()
    if request.method == 'POST':
        email= request.form.get('email')
        password= request.form.get('motpass')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['username'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            #flash("Connexion reussie")
            return redirect("/blog")
    return render_template('seconnecter.html')




@app.route('/blog', methods=['GET'])    
def blog():
    blogs = BlogPost.query.all()
    return render_template('blog.html', blogs=blogs)



@app.route('/blog', methods=['POST'])    
def blogpost():
    if request.method == 'POST':
        title= request.form.get('title')
        author= request.form.get('author')
        content= request.form.get('content')
        new_blog = BlogPost(title, author, content)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog')
    return render_template('blog.html')


@app.route('/supprimer/<int:id>', methods=['GET', 'POST'])
def supprimer(id):
    user = BlogPost.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('blog'))


@app.route('/modifier/<int:id>', methods=['GET'])
def modifier(id):
    user = BlogPost.query.get_or_404(id)
    return render_template('modifier.html', user=user)


@app.route('/modifier/<int:id>', methods=['POST'])
def modifierpost(id):
    user = BlogPost.query.get_or_404(id)
    if user:
        if request.method == 'POST':
            user.title = request.form.get('title')
            user.author = request.form.get('author')
            user.content = request.form.get('content')
            db.session.commit()
            return redirect('/blog')
        else:
            return render_template('modifier.html', user=user)



if __name__ == "__main__":
    app.run(debug=True)
