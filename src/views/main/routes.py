from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_user, logout_user
from urllib.parse import unquote

from src.models import Term, ConnectedTerm, Category, User
from src.views.main.forms import LoginForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@main_blueprint.route("/page/<int:page>")
def home(page=1):
    # Retrieve only active root categories (those with no parent)
    root_categories = Category.query.filter(Category.parent_id.is_(None), Category.is_active.is_(True)).all()
    filtered_categories = []

    # Start with filtering active terms only (keep it a query object)
    terms_query = Term.query.filter(Term.is_active.is_(True))

    search_word = request.args.get("searchWord", "")
    if search_word:
        terms_query = terms_query.filter(
            Term.geo_word.ilike(f"%{search_word}%") |
            Term.eng_word.ilike(f"%{search_word}%") |
            Term.english_synonyms.ilike(f"%{search_word}%")
        )

    search_letter = request.args.get("searchLetter", "")
    if search_letter:
        terms_query = terms_query.filter(
            Term.geo_word.ilike(f"{search_letter}%") |
            Term.eng_word.ilike(f"{search_letter}%")
        )

    categories = request.args.get("categories")
    if categories:
        categories = unquote(categories).split(",")
        filtered_categories = Category.query.filter(
            Category.id.in_(categories),
            Category.is_active.is_(True)
        ).all()  # Ensure filtered categories are active

        # Join with TermCategory and filter based on category's active status as well
        terms_query = terms_query.join(Term.category).filter(
            Category.id.in_(categories),
            Category.is_active.is_(True)  # Ensure category is active
        )

    # Filter terms whose associated categories (and their parents) are active
    active_terms_query = terms_query.join(Term.category).filter(
        Category.is_active.is_(True) & Category.id.in_(
            [category.id for category in Category.query.all() if all(parent.is_active for parent in category.get_parents())]
        )
    )

    sort = request.args.get("sortType")
    if sort:
        sort_map = {
            "ka": Term.geo_word,
            "en": Term.eng_word,
            "recent": Term.id
        }
        active_terms_query = active_terms_query.order_by(sort_map[sort].desc())

    terms_paginated = active_terms_query.paginate(per_page=5, page=page)

    print(search_letter, search_word, categories)

    return render_template("main/main.html", terms=terms_paginated,
                           root_categories=root_categories, filtered_categories=filtered_categories,
                           search_word=search_word, search_letter=search_letter)


@main_blueprint.route("/about")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/contact")
def contact():
    return render_template("main/contact.html")


@main_blueprint.route("/term_detail/<int:term_id>")
def term_detail(term_id):
    # Fetch the term by ID and ensure that it belongs to at least one active category
    term = Term.query.filter(
        Term.id == term_id,
        Term.is_active.is_(True),  # Ensure the term itself is active
        Term.category.any(Category.is_active.is_(True))  # Ensure the term belongs to an active category
    ).first_or_404()

    return render_template("main/term_detail.html", term=term)


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
