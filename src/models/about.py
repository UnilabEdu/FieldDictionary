from src.extensions import db
from src.models.base import BaseModel


class About(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    partner_name = db.Column(db.String(100), nullable=True)
    logo = db.Column(db.String(200), nullable=True)
    logo_link = db.Column(db.Text, nullable=True)
    about_text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return self.partner_name
    

