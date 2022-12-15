from models.shared import db


class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lpu = db.Column(db.String(256), unique=False, nullable=False)
    obj = db.Column(db.String(256), unique=False, nullable=True)
    alias = db.Column(db.String(64), unique=False, nullable=False)
    rname = db.Column(db.String(64), unique=False, nullable=True)
    pgroup = db.Column(db.String(64), unique=False, nullable=True)
    col = db.Column(db.Integer, unique=False, nullable=True)
    row = db.Column(db.Integer, unique=False, nullable=True)
    disp = db.Column(db.String(64), unique=False, nullable=True)
    timeout = db.Column(db.Integer, unique=False, nullable=True)
    tg = db.Column(db.String(64), unique=False, nullable=True)
    blocked = db.Column(db.Boolean, unique=False, nullable=True)
    tblock = db.Column(db.Integer, unique=False, nullable=True)
    blocktime = db.Column(db.DateTime, unique=False, nullable=False)
    sim = db.Column(db.String(64), unique=False, nullable=True)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'lpu': self.lpu,
            'obj': self.obj,
            'alias': self.alias,
            'col': self.col,
            'row': self.row,
            'sim': self.sim
        }

    def __repr__(self):
        return f'{self.id} {self.lpu} {self.obj} {self.alias} {self.rname} {self.pgroup} {self.col} {self.row} {self.sim}'
