from src.extensions import db
from src.models.base import BaseModel



class Term(BaseModel):
    __tablename__ = 'terms'

    id = db.Column(db.Integer, primary_key=True)
    geo_word = db.Column(db.String(100), nullable=False)
    eng_word = db.Column(db.String(100), nullable=False)
    grammar_form = db.Column(db.String(50), nullable=True)
    term_source = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    definition_source = db.Column(db.String(100), nullable=False)
    term_type = db.Column(db.String(50), nullable=True)
    context = db.Column(db.Text, nullable=True)
    context_source = db.Column(db.String(100), nullable=True)
    comment = db.Column(db.Text, nullable=True)

    category = db.relationship("Category", secondary="terms_categories", backref="terms")
    

    def __repr__(self):
        return f"({self.eng_word} - {self.geo_word})"



class ConnectedTerm(BaseModel):
    __tablename__ = "connected_terms"

    id = db.Column(db.Integer, primary_key=True)
    term1_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=True)
    term2_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=True)
    is_synonym = db.Column(db.Boolean, nullable=False)

    term1 = db.relationship('Term', foreign_keys=[term1_id], backref='term1_connections')
    term2 = db.relationship('Term', foreign_keys=[term2_id], backref='term2_connections')


    def __repr__(self):
        return f"ConnectedTerm('{self.term1_id}', '{self.term2_id}', synonym={self.is_synonym})"


    

class Category(BaseModel):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)

    
    # Establish the relationship between parent and child categories
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')


    def get_descendants(self):
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants


    def __repr__(self):
        return self.name



class TermCategory(BaseModel):

    __tablename__ = "terms_categories"

    id = db.Column(db.Integer, primary_key=True)
    term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))