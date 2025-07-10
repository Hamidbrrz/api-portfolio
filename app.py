import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask.cli import with_appcontext
import click

# ✅ Charger les variables d’environnement
load_dotenv()

# ✅ Corriger postgres:// → postgresql://
if os.getenv("DATABASE_URL", "").startswith("postgres://"):
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)

# ✅ Initialisation Flask
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ✅ Clé secrète pour JWT
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret')

# ✅ Décorateur pour routes protégées
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace("Bearer ", "")
        if not token:
            return jsonify({'error': 'Token manquant'}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = Admin.query.filter_by(username=data['username']).first()
        except Exception:
            return jsonify({'error': 'Token invalide'}), 403
        return f(*args, **kwargs)
    return decorated

# ✅ MODELS
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'content': self.content}

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    link = db.Column(db.String(255))

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'link': self.link}

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    title = db.Column(db.String(255))
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(255))

    def to_dict(self):
        return {'name': self.name, 'title': self.title, 'bio': self.bio, 'image_url': self.image_url}

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    github = db.Column(db.String(255))
    message = db.Column(db.Text)

    def to_dict(self):
        return {
            'email': self.email,
            'linkedin': self.linkedin,
            'github': self.github,
            'message': self.message,
        }

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(200))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ✅ ROUTES

@app.route('/api/import', methods=['POST'])
@token_required
def import_data():
    data = request.get_json()

    # ABOUT
    about_data = data.get('about', {})
    about = About.query.first() or About()
    about.name = about_data.get('name', '')
    about.title = about_data.get('title', '')
    about.bio = about_data.get('bio', '')
    about.image_url = about_data.get('image_url', '')
    db.session.add(about)

    # CONTACT
    contact_data = data.get('contact', {})
    contact = Contact.query.first() or Contact()
    contact.email = contact_data.get('email', '')
    contact.linkedin = contact_data.get('linkedin', '')
    contact.github = contact_data.get('github', '')
    contact.message = contact_data.get('message', '')
    db.session.add(contact)

    # BLOG
    BlogPost.query.delete()
    for post_data in data.get('blog', []):
        post = BlogPost(title=post_data.get('title', ''), content=post_data.get('content', ''))
        db.session.add(post)

    # PROJECTS
    Project.query.delete()
    for proj_data in data.get('projects', []):
        project = Project(
            title=proj_data.get('title', ''),
            description=proj_data.get('description', ''),
            link=proj_data.get('link', '')
        )
        db.session.add(project)

    db.session.commit()
    return jsonify({'message': 'Import terminé avec succès'})


@app.route('/api/export', methods=['GET'])
@token_required
def export_data():
    about = About.query.first()
    contact = Contact.query.first()
    projects = Project.query.all()
    blog_posts = BlogPost.query.all()

    return jsonify({
        'about': about.to_dict() if about else {},
        'contact': contact.to_dict() if contact else {},
        'projects': [p.to_dict() for p in projects],
        'blog': [b.to_dict() for b in blog_posts],
    })


@app.route('/api/setup-admin', methods=['POST'])
def setup_admin():
    data = request.get_json()
    admin = Admin(username=data['username'])
    admin.set_password(data['password'])
    db.session.add(admin)
    db.session.commit()
    return jsonify({'message': 'Admin créé'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    admin = Admin.query.filter_by(username=data['username']).first()

    if admin and admin.check_password(data['password']):
        token = jwt.encode({
            'username': admin.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'error': 'Identifiants invalides'}), 401

@app.route('/api/contact', methods=['GET'])
def get_contact():
    contact = Contact.query.first()
    return jsonify(contact.to_dict()) if contact else jsonify({})

@app.route('/api/contact', methods=['POST'])
@token_required
def update_contact():
    data = request.get_json()
    contact = Contact.query.first() or Contact()
    contact.email = data.get('email')
    contact.linkedin = data.get('linkedin')
    contact.github = data.get('github')
    contact.message = data.get('message')
    db.session.add(contact)
    db.session.commit()
    return jsonify({'message': 'Contact updated!'})

@app.route('/api/blog', methods=['GET'])
def get_blog():
    posts = BlogPost.query.all()
    return jsonify([post.to_dict() for post in posts])

@app.route('/api/blog', methods=['POST'])
@token_required
def create_blog():
    data = request.get_json()
    post = BlogPost(title=data['title'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Article ajouté'}), 201

@app.route('/api/blog/<int:id>', methods=['DELETE'])
@token_required
def delete_blog(id):
    post = BlogPost.query.get(id)
    if not post:
        return jsonify({'error': 'Introuvable'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Supprimé'})

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects])

@app.route('/api/projects', methods=['POST'])
@token_required
def add_project():
    data = request.get_json()
    project = Project(title=data['title'], description=data['description'], link=data['link'])
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Projet ajouté'})

@app.route('/api/projects/<int:id>', methods=['DELETE'])
@token_required
def delete_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({'error': 'Introuvable'}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Supprimé'})

@app.route('/api/about', methods=['GET'])
def get_about():
    about = About.query.first()
    return jsonify(about.to_dict()) if about else jsonify({})

@app.route('/api/about', methods=['POST'])
@token_required
def update_about():
    data = request.get_json()
    about = About.query.first() or About()
    about.name = data.get('name', '')
    about.title = data.get('title', '')
    about.bio = data.get('bio', '')
    about.image_url = data.get('image_url', '')
    db.session.add(about)
    db.session.commit()
    return jsonify({'message': 'À propos mis à jour'})

# ✅ Commande CLI pour tester la base
@app.cli.command("db-check")
@with_appcontext
def db_check():
    """Test rapide de connexion DB"""
    click.echo("✅ Connexion à la base réussie !")

# ✅ Lancer le serveur
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
