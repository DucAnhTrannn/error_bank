from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    cause = db.Column(db.String(200), nullable=False)
    solution = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Error {self.product_code}>'
