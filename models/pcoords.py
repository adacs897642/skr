from models.shared import db


class Pcoords(db.Model):
    alias = db.Column(db.String(64), primary_key=True)
    nico = db.Column(db.Integer, unique=False, nullable=False)

    @property
    def serialized(self):
        return {
            'alias': self.alias,
            'nico': self.nico
        }

    def __repr__(self):
        return f'{self.alias} {self.nico}'
