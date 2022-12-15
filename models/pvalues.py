
from models.shared import db


class Pvalues(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False)
    alias = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=True)
    time = db.Column(db.DateTime, unique=False, nullable=False)
    value = db.Column(db.String(64), unique=False, nullable=True)
    units = db.Column(db.String(8), unique=False, nullable=True)
    msg = db.Column(db.String(256), unique=False, nullable=True)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'alias': self.alias,
            'name': self.name,
            'time': self.time,
            'value': self.value,
            'units': self.units,
            'msg': self.msg,
        }

    def __repr__(self):
        pass

