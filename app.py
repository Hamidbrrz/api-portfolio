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

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify([post.to_dict() for post in BlogPost.query.all()])

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post = BlogPost(title=data['title'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify([p.to_dict() for p in Project.query.all()])

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    p = Project(title=data['title'], description=data['description'], link=data['link'])
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@app.route('/api/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    p = Project.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

@app.route('/api/about', methods=['GET'])
def get_about():
    about = About.query.first()
    if not about:
        return jsonify({})
    return jsonify(about.to_dict())

@app.route('/api/about', methods=['POST'])
def update_about():
    data = request.get_json()
    about = About.query.first()
    if not about:
        about = About(name=data['name'], title=data['title'], bio=data['bio'], image_url=data['image_url'])
        db.session.add(about)
    else:
        about.name = data['name']
        about.title = data['title']
        about.bio = data['bio']
        about.image_url = data['image_url']
    db.session.commit()
    return jsonify(about.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
