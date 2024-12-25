from src.extensions import db
from src.models.base import BaseModel


class Term(BaseModel):
    __tablename__ = 'terms'

    id = db.Column(db.Integer, primary_key=True)
    geo_word = db.Column(db.String(100), nullable=False)
    eng_word = db.Column(db.String(100), nullable=False)
    grammar_form = db.Column(db.String(50), nullable=True)
    term_source = db.Column(db.Text, nullable=False)
    definition = db.Column(db.Text, nullable=False)
    definition_source = db.Column(db.Text, nullable=False)
    term_type = db.Column(db.String(50), nullable=True)
    context = db.Column(db.Text, nullable=True)
    context_source = db.Column(db.Text, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    stylistic_label = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    category = db.relationship("Category", secondary="terms_categories", backref="terms")
    english_connections = db.relationship("EnglishSynonym", back_populates="term")

    def __repr__(self):
        return f"({self.eng_word} - {self.geo_word})"

    def get_synonyms(self, is_english=False):
        connections = ConnectedTerm.query.filter(ConnectedTerm.is_synonym == True, (ConnectedTerm.term1_id == self.id) | (ConnectedTerm.term2_id == self.id), ConnectedTerm.is_english == is_english).all()
        synonym_ids = [connection.term1_id if connection.term1_id != self.id else connection.term2_id for connection in connections]
        synonyms = Term.query.filter(Term.id.in_(synonym_ids)).all()
        return synonyms

    def get_related_terms(self):
        connections = ConnectedTerm.query.filter(ConnectedTerm.is_synonym == False, (ConnectedTerm.term1_id == self.id) | (ConnectedTerm.term2_id == self.id)).all()
        connected_term_ids = [connection.term1_id if connection.term1_id != self.id else connection.term2_id for connection in connections]
        related_terms = Term.query.filter(Term.id.in_(connected_term_ids)).all()
        return related_terms

    def get_english_synonyms(self):
        english_synonyms = EnglishSynonym.query.filter((ConnectedTerm.term1_id == self.id) | (ConnectedTerm.term2_id == self.id)).all()
        return english_synonyms

    def has_synonyms_or_relations(self):
        connections = ConnectedTerm.query.filter((ConnectedTerm.term1_id == self.id) | (ConnectedTerm.term2_id == self.id)).first()
        return connections != None

    def get_category_tree(self):
        category_trees = []
        for category in self.category:
            categories = category.get_parents()
            categories.append(category)
            category_trees.append(categories)

        branched_tree = {}
        for category_tree in category_trees:
            current_dict = branched_tree
            for category in category_tree:
                if category not in current_dict:
                    current_dict[category] = {}
                current_dict = current_dict[category]
        return branched_tree



class ConnectedTerm(BaseModel):
    __tablename__ = "connected_terms"

    id = db.Column(db.Integer, primary_key=True)
    term1_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=True)
    term2_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=True)
    is_synonym = db.Column(db.Boolean, nullable=False, default=False)
    is_english = db.Column(db.Boolean, nullable=False, default=False)

    term1 = db.relationship('Term', foreign_keys=[term1_id])
    term2 = db.relationship('Term', foreign_keys=[term2_id])


    def __repr__(self):
        return f"{self.term1} - {self.term2}"


class EnglishSynonym(BaseModel):
    __tablename__ = "english_synonyms"

    id = db.Column(db.Integer, primary_key=True)
    eng_word = db.Column(db.String, nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=True)

    term = db.relationship('Term', back_populates="english_connections")

    def __repr__(self):
        return f"{self.eng_word} = {self.term}"


class Category(BaseModel):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # Establish the relationship between parent and child categories
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), order_by="Category.name.asc()")

    def get_descendants(self):
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    def get_parents(self):
        parents = []
        if self.parent:
            parents.extend(self.parent.get_parents())
            parents.append(self.parent)
        return parents
    
    def __repr__(self):
        return self.name


class TermCategory(BaseModel):
    __tablename__ = "terms_categories"

    id = db.Column(db.Integer, primary_key=True)
    term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
