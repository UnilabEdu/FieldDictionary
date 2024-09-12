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



    term1 = Term(geo_word="არქიპელაგი", eng_word="Archipelago", grammar_form="არსებითი სახელი", 
                 term_source="https://www.google.co.uk/", 
                 definition="შემთხვევითად გენერირებული ტექსტი ეხმარება დიზაინერებს და ტიპოგრაფიული ნაწარმის შემქმნელებს, რეალურთან მაქსიმალურად მიახლოებული შაბლონი წარუდგინონ შემფასებელს. ხშირადაა შემთხვევა, როდესაც დიზაინის შესრულებისას საჩვენებელია, თუ როგორი იქნება ტექსტის ბლოკი. სწორედ ასეთ დროს არის მოსახერხებელი ამ გენერატორით შექმნილი ტექსტის გამოყენება, რადგან უბრალოდ „ტექსტი ტექსტი ტექსტი“ ან სხვა გამეორებადი სიტყვების ჩაყრა, ხელოვნურ ვიზუალურ სიმეტრიას ქმნის და არაბუნებრივად გამოიყურება.", 
                 definition_source="https://www.google.co.uk/", term_type="სლენგი", 
                 context="ეს არის კონტექსტი", context_source="https://www.google.co.uk/", 
                 comment="ეს არის კომენტარი", category=[category6,])

    term2 = Term(geo_word="ქართული სიტყვა", eng_word="English word", grammar_form="ზმნა", 
                 term_source="https://www.google.co.uk/", 
                 definition="შემთხვევითად გენერირებული ტექსტი ეხმარება დიზაინერებს და ტიპოგრაფიული ნაწარმის შემქმნელებს, რეალურთან მაქსიმალურად მიახლოებული შაბლონი წარუდგინონ შემფასებელს. ხშირადაა შემთხვევა, როდესაც დიზაინის შესრულებისას საჩვენებელია, თუ როგორი იქნება ტექსტის ბლოკი. სწორედ ასეთ დროს არის მოსახერხებელი ამ გენერატორით შექმნილი ტექსტის გამოყენება, რადგან უბრალოდ „ტექსტი ტექსტი ტექსტი“ ან სხვა გამეორებადი სიტყვების ჩაყრა, ხელოვნურ ვიზუალურ სიმეტრიას ქმნის და არაბუნებრივად გამოიყურება.", 
                 definition_source="https://www.google.co.uk/", 
                 context="ეს არის კონტექსტი", context_source="https://www.google.co.uk/", 
                 comment="ეს არის კომენტარი", category=[category7])
    
    term3 = Term(geo_word="Example", eng_word="მაგალითი", grammar_form="ზმნა", 
                 term_source="https://www.google.co.uk/", 
                 definition="შემთხვევითად გენერირებული ტექსტი ეხმარება დიზაინერებს და ტიპოგრაფიული ნაწარმის შემქმნელებს, რეალურთან მაქსიმალურად მიახლოებული შაბლონი წარუდგინონ შემფასებელს. ხშირადაა შემთხვევა, როდესაც დიზაინის შესრულებისას საჩვენებელია, თუ როგორი იქნება ტექსტის ბლოკი. სწორედ ასეთ დროს არის მოსახერხებელი ამ გენერატორით შექმნილი ტექსტის გამოყენება, რადგან უბრალოდ „ტექსტი ტექსტი ტექსტი“ ან სხვა გამეორებადი სიტყვების ჩაყრა, ხელოვნურ ვიზუალურ სიმეტრიას ქმნის და არაბუნებრივად გამოიყურება.", 
                 definition_source="https://www.google.co.uk/", 
                 context="ეს არის კონტექსტი", context_source="https://www.google.co.uk/", 
                 comment="ეს არის კომენტარი", category=[category7])
    
    term1.create()
    term2.create()
    term3.create()
    click.echo("Created terms!")
    


    # Connect terms using the ConnectedTerm model
    connected_term = ConnectedTerm(term1_id=term1.id, term2_id=term2.id, is_synonym=True)
    connected_term2 = ConnectedTerm(term1_id=term1.id, term2_id=term3.id, is_synonym=False)
    
    connected_term.create()
    connected_term2.create()
    click.echo("Created connected terms!")



    click.echo("Creating admin user...")
    admin = User(username="admin", password="admin123", email="testuser@gmail.com")

    admin.create()
    click.echo("Created admin user!")


    click.echo("Database populated!")