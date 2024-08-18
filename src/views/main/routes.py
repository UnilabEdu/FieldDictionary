from flask import render_template, Blueprint



main_blueprint = Blueprint("main", __name__)



@main_blueprint.route("/")
@main_blueprint.route("/home")
def home():
    return render_template("main/main.html")



@main_blueprint.route("/about")
def about():
    return render_template("about/about.html")



@main_blueprint.route("/contact")
def contact():
    return render_template("contact/contact.html")



@main_blueprint.route("/term_not_found")
def term_not_found():
    return render_template("term_not_found/term_not_found.html")



@main_blueprint.route("/term_detail")
def term_detail():
    return render_template("term_detail/term_detail.html")