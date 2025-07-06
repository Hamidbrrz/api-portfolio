from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
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

@app.route('/api/contact', methods=['GET'])
def get_contact():
    contact = Contact.query.first()
    if contact:
        return jsonify(contact.to_dict())
    return jsonify({})

@app.route('/api/contact', methods=['POST'])
def update_contact():
    data = request.get_json()
    contact = Contact.query.first()
    if not contact:
        contact = Contact()
        db.session.add(contact)

    contact.email = data.get('email')
    contact.linkedin = data.get('linkedin')
    contact.github = data.get('github')
    contact.message = data.get('message')

    db.session.commit()
    return jsonify({'message': 'Contact updated!'})

# BLOG ROUTES
@app.route('/api/blog', methods=['GET'])
def get_blog():
    posts = BlogPost.query.all()
    return jsonify([post.to_dict() for post in posts])

@app.route('/api/blog', methods=['POST'])
def create_blog():
    data = request.get_json()
    post = BlogPost(title=data['title'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Article ajouté'}), 201

@app.route('/api/blog/<int:id>', methods=['DELETE'])
def delete_blog(id):
    post = BlogPost.query.get(id)
    if not post:
        return jsonify({'error': 'Introuvable'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Supprimé'})


# PROJETS ROUTES
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects])

@app.route('/api/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    project = Project(title=data['title'], description=data['description'], link=data['link'])
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Projet ajouté'})

@app.route('/api/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({'error': 'Introuvable'}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Supprimé'})


# À PROPOS ROUTES
@app.route('/api/about', methods=['GET'])
def get_about():
    about = About.query.first()
    return jsonify(about.to_dict() if about else {})

@app.route('/api/about', methods=['POST'])
def update_about():
    data = request.get_json()
    about = About.query.first()
    if not about:
        about = About()
        db.session.add(about)
    about.name = data.get('name', '')
    about.title = data.get('title', '')
    about.bio = data.get('bio', '')
    about.image_url = data.get('image_url', '')
    db.session.commit()
    return jsonify({'message': 'À propos mis à jour'})


if __name__ == '__main__':
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()  # ⚠️ Crée seulement si vide
    app.run(host='0.0.0.0', port=5000, debug=True)
