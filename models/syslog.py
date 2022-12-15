from models.shared import db


class Syslog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, unique=False, nullable=False)
    author = db.Column(db.String(64), unique=False, nullable=True)
    msg = db.Column(db.String(200), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, nullable=True)

    @property
    def serialized(self):
        """Return object data in serializable format"""
        return {
            'id': self.id,
            'time': self.time,
            'author': self.author,
            'msg': self.msg,
            'level': self.level
        }

    def __repr__(self):
        return f'{self.id} {self.time} {self.msg} {self.author} {self.level}'

