from flask import render_template, Blueprint

from src.models import Term, ConnectedTerm, Category



main_blueprint = Blueprint("main", __name__)



@main_blueprint.route("/")
@main_blueprint.route("/home")
def home():
    root_categories = Category.query.filter(Category.parent_id.is_(None)).all()
    terms = Term.query.all()
    return render_template("main/main.html", terms=terms, root_categories=root_categories)



@main_blueprint.route("/about")
def about():
    return render_template("main/about.html")



@main_blueprint.route("/contact")
def contact():
    return render_template("main/contact.html")



@main_blueprint.route("/term_not_found")
def term_not_found():
    root_categories = Category.query.filter(Category.parent_id.is_(None)).all()
    return render_template("main/term_not_found.html", root_categories=root_categories)



@main_blueprint.route("/term_detail/<int:term_id>")
def term_detail(term_id):
    term = Term.query.get_or_404(term_id)

    connected_terms = ConnectedTerm.query.filter(
        (ConnectedTerm.term1_id == term_id) | (ConnectedTerm.term2_id == term_id)
    ).all()

    synonyms = ConnectedTerm.query.filter(
        (ConnectedTerm.term1_id == term.id) | (ConnectedTerm.term2_id == term.id),
        ConnectedTerm.is_synonym == True
    ).all()
    
    return render_template("main/term_detail.html", term=term, connected_terms=connected_terms, synonyms=synonyms)