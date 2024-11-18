from random import sample, randint
from flask.cli import with_appcontext
import click
from openpyxl import load_workbook
from os import path

from openpyxl.cell.rich_text import CellRichText

from src.config import Config
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
    filepath = path.join(Config.BASE_DIRECTORY, "IATGE.xlsx")
    workbook = load_workbook(filepath, rich_text=True)
    worksheet = workbook.worksheets[0]

    existing_categories = {category.name: category.id for category in Category.query.all()}
    for row in worksheet.iter_rows(min_row=2):

        def rich_to_html(row):
            text = ""
            if isinstance(row.value, CellRichText):
                hyperlink = row.hyperlink.target if row.hyperlink is not None else "#"
                for text_block in row.value:
                    if text_block.font.color.value == "FF0070C0":
                        text += f'<a href="{hyperlink}" target="_blank">{text_block.text}</a>'
                    else:
                        text += text_block.text.replace("-", "\n", 1)
            else:
                text = row
            return str(text)

        term_source = rich_to_html(row[6])
        definition_source = rich_to_html(row[8])
        context_source = rich_to_html(row[10])

        new_term = Term(geo_word=str(row[3].value), eng_word=str(row[2].value), grammar_form=str(row[4].value),
                        term_source=term_source,
                        definition=str(row[7].value), definition_source=definition_source,
                        context=str(row[9].value), context_source=context_source,
                        comment=str(row[12].value))
        new_term.create(commit=False, flush=True)

        categories = str(row[0].value)
        subcategories = str(row[1].value)
        for category in categories.split("-"):
            category = category.strip()
            if not category:
                continue

            if category not in existing_categories:
                new_category = Category(name=category)
                new_category.create(commit=False, flush=True)
                existing_categories[category] = new_category.id

            # If subcategory column is empty
            if not subcategories or subcategories == "None":
                term_category = TermCategory(term_id=new_term.id, category_id=existing_categories[category])
                term_category.create(commit=False)

        children_subcategories = subcategories.split("|")
        for index, subcategory in enumerate(children_subcategories):
            subcategory = subcategory.strip()
            if "\n" in subcategory or not subcategory or subcategory == "None":
                continue

            if subcategory not in existing_categories:
                if index == 0:
                    parent_id = existing_categories[str(row[0].value)]
                else:
                    parent_id = existing_categories[children_subcategories[index-1]]

                new_category = Category(name=subcategory, parent_id=parent_id)
                new_category.create(commit=False, flush=True)
                existing_categories[subcategory] = new_category.id

            # For child categories, only save LAST child to term
            if index == len(children_subcategories) - 1:
                term_category = TermCategory(term_id=new_term.id, category_id=existing_categories[subcategory])
                term_category.create(commit=False)

        related_subcategories = subcategories.split("-")
        for subcategory in related_subcategories:
            subcategory = subcategory.strip()
            if "|" in subcategory or not subcategory or subcategory == "None":
                continue

            if subcategory not in existing_categories:
                parent_id = existing_categories[str(row[0].value)]
                new_category = Category(name=subcategory, parent_id=parent_id)
                new_category.create(commit=False, flush=True)
                existing_categories[subcategory] = new_category.id

            # For multiple related categories, save ALL of them to term
            term_category = TermCategory(term_id=new_term.id, category_id=existing_categories[subcategory])
            term_category.create(commit=False)
    db.session.commit()

    click.echo("Creating admin user...")
    admin = User(username="admin", password="admin123", email="testuser@gmail.com")

    admin.create()
    click.echo("Created admin user!")

    click.echo("Database populated!")
