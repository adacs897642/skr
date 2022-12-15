from models.shared import db


class PvaluesLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(64), primary_key=True)
    time = db.Column(db.DateTime, unique=False, nullable=False)
    value = db.Column(db.String(64), unique=False, nullable=True)

    @property
    def serialized(self):
        return {
            # 'id': self.id,
            # 'alias': self.alias,
            'time': self.time,
            'value': self.value
        }

    def __repr__(self):
        pass

    pass
