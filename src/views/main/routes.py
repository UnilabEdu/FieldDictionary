from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_user, logout_user

from src.models import Term, ConnectedTerm, Category, User
from src.views.main.forms import LoginForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    root_categories = Category.query.filter(Category.parent_id.is_(None)).all()

    page = request.args.get("page", type=int)
    terms = Term.query.paginate(per_page=10, page=page)
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


@main_blueprint.route('/categories/<int:category_id>/terms')
def view_terms_by_category(category_id):
    # Get the selected category by ID
    category = Category.query.get_or_404(category_id)

    # Get all descendant categories including the current category
    descendant_categories = [category] + category.get_descendants()

    # Fetch all terms that belong to the selected category or any of its descendants
    terms = Term.query.filter(Term.category.any(Category.id.in_([c.id for c in descendant_categories]))).all()

    # Render the template with the terms and category
    return render_template('main/main.html', terms=terms, category=category)


@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error_message = None
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next", None)
            if next:
                return redirect(next)
            else:
                return redirect(url_for("admin.index"))
        else:
            error_message = "Incorrect username or password! Please try again."

    return render_template(
        "main/login.html",
        form=form,
        error_message=error_message,
    )


@main_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("main.login"))
