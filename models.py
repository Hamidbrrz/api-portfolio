from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'link': self.link
        }


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    title = db.Column(db.String(255))
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(255))

    def to_dict(self):
        return {
            'name': self.name,
            'title': self.title,
            'bio': self.bio,
            'image_url': self.image_url
        }
