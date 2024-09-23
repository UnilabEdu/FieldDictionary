from flask import flash
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from flask_ckeditor import CKEditorField
from wtforms.utils import unset_value

from src.admin.base import SecureModelView
from src.models import ConnectedTerm, Term


class CategoryView(SecureModelView):
    can_view_details = True
    edit_modal = True
    create_modal = True
    can_create = True
    can_edit = True
    can_export = True

    form_columns = ['name', 'parent']
    column_list = ['name', 'parent']

    column_labels = {
        "name": "კატეგორია",
        "parent": "მშობელი კატეგორია",
    }


class TermView(SecureModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_export = True

    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'

    column_filters = ["geo_word", "eng_word"]
    column_default_sort = ("geo_word", True)

    column_list = [
        "geo_word",
        "eng_word",
        "grammar_form",
        "term_source",
        "definition_source",
        "term_type",
        "context",
        "context_source",
        "comment",
        "category",
        "synonyms",
        "english_synonyms",
    ]

    column_sortable_list = [
        "geo_word",
        "eng_word"
    ]

    column_searchable_list = [
        "geo_word",
        "eng_word"
    ]

    column_labels = {
        "geo_word": "ქართული სიტყვა",
        "eng_word": "ინგლისური სიტყვა",
        "grammar_form": "გრამატიკული ფორმა",
        "term_source": "ტერმინის წყარო",
        "definition": "განმარტება",
        "definition_source": "განმარტების წყარო",
        "term_type": "ტერმინის ტიპი",
        "context": "კონტექსტი",
        "context_source": "კონტექსტის წყარო",
        "comment": "კომენტარი",
        "category": "კატეგორია",
        "synonyms": "სინონიმები",
        "english_synonyms": "ინგლისური სინონიმები",
        "connected_terms": "დაკავშირებული სიტყვები"
    }

    form_overrides = {
        'context_source': CKEditorField,
        'term_source': CKEditorField,
        'definition_source': CKEditorField,
    }

    form_columns = [
        "geo_word",
        "eng_word",
        "grammar_form",
        "term_source",
        "definition",
        "definition_source",
        "term_type",
        "context",
        "context_source",
        "comment",
        "category",
        "synonyms_field",
        "english_synonyms",
        "connections_field"
    ]

    form_extra_fields = {"connections_field": QuerySelectMultipleField("დაკავშრებული სიტყვები", query_factory=lambda: Term.query),
                         "synonyms_field": QuerySelectMultipleField("სინონიმები", query_factory=lambda: Term.query)}

    def create_model(self, form):
        try:
            model = self.build_new_instance()
            for synonym_id in form.synonyms_field.raw_data:
                ConnectedTerm(term1_id=model.id, term2_id=synonym_id, is_synonym=True).create(commit=False)

            for related_term_id in form.connections_field.raw_data:
                ConnectedTerm(term1_id=model.id, term2_id=related_term_id, is_synonym=True).create(commit=False)

            model.save()
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(f'Failed to create record. {str(ex)}s', 'error')
            self.session.rollback()
            return False

        super().create_model(form)
        return model

    def update_model(self, form, model):
        try:
            if form.connections_field.data:
                related_term_ids = {term.id for term in model.get_related_terms()}
                field_term_ids = {int(term_id) for term_id in form.connections_field.raw_data}

                removed_terms = related_term_ids.difference(field_term_ids)
                added_terms = field_term_ids.difference(related_term_ids)

                for term_id in added_terms:
                    if term_id != model.id and term_id not in related_term_ids:
                        ConnectedTerm(term1_id=model.id, term2_id=term_id, is_synonym=False).create(commit=False)

                if removed_terms:
                    ConnectedTerm.query.filter(ConnectedTerm.term1_id.in_(removed_terms),
                                               ConnectedTerm.term2_id == model.id,
                                               ConnectedTerm.is_synonym == False).delete()

                    ConnectedTerm.query.filter(ConnectedTerm.term2_id.in_(removed_terms),
                                               ConnectedTerm.term1_id == model.id,
                                               ConnectedTerm.is_synonym == False).delete()


            if form.synonyms_field.data:
                synonym_ids = {term.id for term in model.get_synonyms()}
                field_term_ids = {int(term_id) for term_id in form.synonyms_field.raw_data}

                removed_terms = synonym_ids.difference(field_term_ids)
                added_terms = field_term_ids.difference(synonym_ids)

                for term_id in added_terms:
                    if term_id != model.id and term_id not in synonym_ids:
                        ConnectedTerm(term1_id=model.id, term2_id=term_id, is_synonym=True).create(commit=False)

                if removed_terms:
                    ConnectedTerm.query.filter(ConnectedTerm.term1_id.in_(removed_terms),
                                               ConnectedTerm.term2_id == model.id,
                                               ConnectedTerm.is_synonym == True).delete()

                    ConnectedTerm.query.filter(ConnectedTerm.term2_id.in_(removed_terms),
                                               ConnectedTerm.term1_id == model.id,
                                               ConnectedTerm.is_synonym == True).delete()

            model.save()
            super().update_model(form, model)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(f'Failed to update record. {str(ex)}', 'error')
            self.session.rollback()
            return False
        return True

    def on_form_prefill(self, form, id):
        model = Term.query.get(id)

        synonyms = model.get_synonyms()
        related_words = model.get_related_terms()

        form.connections_field.default = related_words
        form.synonyms_field.default = synonyms
        form.connections_field.process(None, related_words or unset_value)
        form.synonyms_field.process(None, synonyms or unset_value)

        super().on_form_prefill(form, id)

    def on_model_delete(self, model):
        # Manually delete connections (ConnectedTerm records) referencing the term
        ConnectedTerm.query.filter((ConnectedTerm.term1_id == model.id) | (ConnectedTerm.term2_id == model.id)).delete(synchronize_session=False)

        # Proceed with the actual term deletion
        super().on_model_delete(model)
