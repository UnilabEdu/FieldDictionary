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
    english_synonyms = db.Column(db.Text, nullable=True)
    stylistic_label = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    category = db.relationship("Category", secondary="terms_categories", backref="terms")

    def __repr__(self):
        return f"({self.eng_word} - {self.geo_word})"

    def get_synonyms(self):
        connections = ConnectedTerm.query.filter(ConnectedTerm.is_synonym == True, (ConnectedTerm.term1_id == self.id) | (ConnectedTerm.term2_id == self.id)).all()
        synonym_ids = [connection.term1_id if connection.term1_id != self.id else connection.term2_id for connection in connections]
        synonyms = Term.query.filter(Term.id.in_(synonym_ids)).all()
        return synonyms

    def get_related_terms(self):
        connections = ConnectedTerm.query.filter(ConnectedTerm.is_synonym == False, (ConnectedTerm.term1_id == self.id) | (ConnectedTerm.term2_id == self.id)).all()
        connected_term_ids = [connection.term1_id if connection.term1_id != self.id else connection.term2_id for connection in connections]
        related_terms = Term.query.filter(Term.id.in_(connected_term_ids)).all()
        return related_terms

    def has_synonyms_or_relations(self):
        connections = ConnectedTerm.query.filter((ConnectedTerm.term1_id == self.id) | (ConnectedTerm.term2_id == self.id)).first()
        return connections != None
    
    def get_category_tree(self):
        category_trees = []
        for category in self.category:
            parents = category.get_parents()
            # Check if the current category and all parent categories are active
            if category.is_active:
                # Check all parents' active status
                if all(parent.is_active for parent in parents):
                    # Add parents and current category to the tree
                    parents.append(category)
                    category_trees.append(parents)
        return category_trees



class ConnectedTerm(BaseModel):
    __tablename__ = "connected_terms"

    id = db.Column(db.Integer, primary_key=True)
    term1_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=True)
    term2_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=True)
    is_synonym = db.Column(db.Boolean, nullable=False, default=False)

    term1 = db.relationship('Term', foreign_keys=[term1_id])
    term2 = db.relationship('Term', foreign_keys=[term2_id])


    def __repr__(self):
        return f"{self.term1} - {self.term2}"


class Category(BaseModel):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # Establish the relationship between parent and child categories
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    
    def get_descendants(self, include_inactive=False):
        """ Return all descendants of the category, optionally filtering only active ones. """
        descendants = []
        for child in self.children:
            # Only include the child if it's active or include_inactive is True
            if child.is_active or include_inactive:
                descendants.append(child)
                descendants.extend(child.get_descendants(include_inactive=include_inactive))
        return descendants
    
    def get_parents(self):
        parents = []
        if self.parent:
            if self.parent.is_active:
                parents.append(self.parent)
                parents.extend(self.parent.get_parents())
        return parents
    
    def __repr__(self):
        return self.name


class TermCategory(BaseModel):
    __tablename__ = "terms_categories"

    id = db.Column(db.Integer, primary_key=True)
    term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
