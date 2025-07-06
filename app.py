from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, BlogPost, Project, About

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------- BLOG POSTS ----------
@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    return jsonify([post.to_dict() for post in posts])

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = BlogPost(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    post = BlogPost.query.get_or_404(id)
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify(post.to_dict()), 200

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'}), 200

# ---------- PROJECTS ----------
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    new_project = Project(
        title=data['title'],
        description=data['description'],
        link=data['link']
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.to_dict()), 201

@app.route('/api/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'}), 200

# ---------- ABOUT ----------
@app.route('/api/about', methods=['GET'])
def get_about():
    about = About.query.first()
    if about:
        return jsonify(about.to_dict())
    return jsonify({})

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
    return jsonify(about.to_dict()), 200

# ---------- MAIN ----------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
