from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from urllib.parse import unquote
from sqlalchemy import func
import re

from src.models import Term, Category, User, About
from src.views.main.forms import LoginForm, ContactForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@main_blueprint.route("/page/<int:page>")
def home(page=1):
    items = About.query.all()
    root_categories = Category.query.filter(Category.parent_id.is_(None), Category.is_active == True).all()
    filtered_categories = []
    terms = Term.query.filter(Term.is_active == True, Term.category.any(Category.is_active == True))
    search_word = request.args.get("searchWord", "")
    if search_word:
        if re.match("[A-Za-z0-9 .]+$", search_word):
            terms = terms.filter(Term.definition.ilike(f"%{search_word}%") | Term.eng_word.ilike(f"%{search_word}%") | Term.english_synonyms.ilike(f"%{search_word}%"))
        else:
            terms = terms.filter(Term.geo_word.ilike(f"%{search_word}%"))

    search_letter = request.args.get("searchLetter", "")
    if search_letter:
        terms = terms.filter(Term.geo_word.ilike(f"{search_letter}%") | Term.eng_word.ilike(f"{search_letter}%"))

    categories = request.args.get("categories")
    if categories:
        categories = unquote(categories).split(",")
        filtered_categories = Category.query.filter(Category.id.in_(categories)).all()
        terms = terms.join(Term.category).filter(Category.id.in_(categories))

    sort = request.args.get("sortType")
    if sort:
        sort_map = {
            "ka": Term.geo_word,
            "en": Term.eng_word,
            "recent": Term.id
        }
        terms = terms.order_by(sort_map[sort].desc()) if sort == "recent" else terms.order_by(func.lower(sort_map[sort]).asc())

    print(search_letter, search_word, categories, sort)
    terms = terms.paginate(per_page=5, page=page)
    return render_template("main/main.html", terms=terms,
                           root_categories=root_categories, filtered_categories=filtered_categories,
                           search_word=search_word, search_letter=search_letter, items=items)


@main_blueprint.route("/about")
def about():
    items = About.query.all()
    return render_template('main/about.html', items=items)


@main_blueprint.route("/contact", methods=["GET", "POST"])
def contact():
    items = About.query.all()
    form = ContactForm()
    if form.validate_on_submit():
        flash("შეტყობინება წარმატებით გაიგზავნა!", "success")
        return redirect(url_for('main.home'))
    elif form.is_submitted() and not form.validate():
        flash("გთხოვთ შეავსოთ ყველა ველი სწორად.", "error")

    return render_template("main/contact.html", items=items, form=form)


@main_blueprint.route("/term_detail/<int:term_id>")
def term_detail(term_id):
    items = About.query.all()
    term = Term.query.filter(Term.id == term_id, Term.is_active == True, Term.category.any(Category.is_active == True)).first_or_404()
    return render_template("main/term_detail.html", term=term, items=items)


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

    return render_template("main/login.html", form=form, error_message=error_message,)


@main_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("main.login"))
