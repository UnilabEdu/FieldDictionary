from random import sample, randint
from flask.cli import with_appcontext
import click

from src.extensions import db
from src.models import Term, TermCategory, Category, ConnectedTerm, User


@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Database creation in progress")
    db.drop_all()
    db.create_all()
    click.echo("Database created!")


@click.command("populate_db")
@with_appcontext
def populate_db():
    click.echo("Creating categories...")

    # Root categories
    category1 = Category(name="მეცნიერება")
    category2 = Category(name="ტექნიკა")
    category3 = Category(name="ბუნება")

    # Child categories
    category4 = Category(name="ფიზიკა", parent=category1)
    category5 = Category(name="მათემატიკა", parent=category1)
    category6 = Category(name="გეოგრაფია", parent=category1)

    # Further nested categories
    category7 = Category(name="ალგებრა", parent=category5)
    category8 = Category(name="გეომეტრია", parent=category5)

    categories = [category1, category2, category3, category4, category5, category6, category7, category8]

    for category in categories:
        category.create()

    click.echo("Created categories!")
    for i in range(1, 50):
        term = Term(geo_word=f"ქართული {i}", eng_word=f"English {i}", grammar_form="ზმნა", stylistic_label="შესაბამისი კვალიფიკაცია", term_source="google.com",
                    definition="შემთხვევითად გენერირებული ტექსტი ეხმარება დიზაინერებს და ტიპოგრაფიული ნაწარმის შემქმნელებს, "
                               "რეალურთან მაქსიმალურად მიახლოებული შაბლონი წარუდგინონ შემფასებელს. ხშირადაა შემთხვევა, "
                               "როდესაც დიზაინის შესრულებისას საჩვენებელია, თუ როგორი იქნება ტექსტის ბლოკი. სწორედ ასეთ დროს "
                               "არის მოსახერხებელი ამ გენერატორით შექმნილი ტექსტის გამოყენება, რადგან უბრალოდ „ტექსტი ტექსტი "
                               "ტექსტი“ ან სხვა გამეორებადი სიტყვების ჩაყრა, ხელოვნურ ვიზუალურ სიმეტრიას ქმნის და "
                               "არაბუნებრივად გამოიყურება.",
                    definition_source="google.com", term_type="სლენგი", context=f"ეს არის კონტექსტი {i}",
                    context_source="google.com", comment="ეს არის კომენტარი", category=sample(categories, 1))
        term.create()

    click.echo("Created terms!")
    for i in range(1, 10):
        connected_term = ConnectedTerm(term1_id=i, term2_id=randint(11, 50), is_synonym=randint(0, 1))
        connected_term.create()
    click.echo("Created connected terms!")

    click.echo("Creating admin user...")
    admin = User(username="admin", password="admin123", email="testuser@gmail.com")

    admin.create()
    click.echo("Created admin user!")

    click.echo("Database populated!")
