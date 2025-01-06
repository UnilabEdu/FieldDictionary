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

    form_columns = ['name', 'parent', 'is_active']
    column_list = ['name', 'parent', 'is_active']

    column_labels = {
        "name": "კატეგორია",
        "parent": "მშობელი კატეგორია",
        "is_active": "აქტიური"
    }

    column_searchable_list = ['name']
    column_sortable_list = ['name']
    column_default_sort = ('name', False)
    column_filters = ['name', 'is_active']


class EnglishTermView(SecureModelView):
    column_labels = {
        "eng_word": "ტერმინი",
        "term": "ინგლისური სინონიმი"
    }

    column_list = ["eng_word", "term"]
    form_columns = column_list

    column_searchable_list = ("eng_word",)


class TermView(SecureModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_export = True

    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'

    column_filters = ["geo_word", "eng_word", "is_active"]
    column_default_sort = ("geo_word", False)

    column_list = [
        "geo_word",
        "eng_word",
        "grammar_form",
        "stylistic_label",
        "term_source",
        "definition_source",
        "term_type",
        "context",
        "context_source",
        "comment",
        "category",
        "synonyms",
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
        "stylistic_label": "სტილისტიკური კვალიფიკაცია",
        "term_source": "ტერმინის წყარო",
        "definition": "განმარტება",
        "definition_source": "განმარტების წყარო",
        "term_type": "ტერმინის ტიპი",
        "context": "კონტექსტი",
        "context_source": "კონტექსტის წყარო",
        "comment": "კომენტარი",
        "category": "კატეგორია",
        "synonyms": "სინონიმები",
        "connected_terms": "დაკავშირებული სიტყვები",
        "is_active": "აქტიური"
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
        "stylistic_label",
        "term_source",
        "definition",
        "definition_source",
        "term_type",
        "context",
        "context_source",
        "comment",
        "category",
        "synonyms_field",
        "eng_synonyms_field",
        "connections_field",
        "is_active"
    ]

    form_extra_fields = {"connections_field": QuerySelectMultipleField("დაკავშრებული სიტყვები", query_factory=lambda: Term.query),
                         "synonyms_field": QuerySelectMultipleField("ქართული სინონიმები", query_factory=lambda: Term.query),
                         "eng_synonyms_field": QuerySelectMultipleField("ინგლისური სინონიმები", query_factory=lambda: Term.query)}

    def create_model(self, form):
        try:
            model = self.build_new_instance()
            for synonym_id in form.synonyms_field.raw_data:
                ConnectedTerm(term1_id=model.id, term2_id=synonym_id, is_synonym=True, is_english=False).create(commit=False)

            for related_term_id in form.connections_field.raw_data:
                ConnectedTerm(term1_id=model.id, term2_id=related_term_id, is_synonym=False, is_english=False).create(commit=False)

            for eng_synonym_id in form.eng_synonyms_field.raw_data:
                ConnectedTerm(term1_id=model.id, term2_id=eng_synonym_id, is_synonym=True, is_english=True).create(commit=False)

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
        def update_connected_terms(existing_term_ids, field_term_ids, is_synonym, is_english):
            removed_terms = existing_term_ids.difference(field_term_ids)
            added_terms = field_term_ids.difference(existing_term_ids)

            for term_id in added_terms:
                if term_id != model.id and term_id not in existing_term_ids:
                    ConnectedTerm(term1_id=model.id, term2_id=term_id, is_synonym=is_synonym, is_english=is_english).create(commit=False)

            if removed_terms:
                ConnectedTerm.query.filter(ConnectedTerm.term1_id.in_(removed_terms),
                                           ConnectedTerm.term2_id == model.id,
                                           ConnectedTerm.is_synonym == is_synonym,
                                           ConnectedTerm.is_english == is_english).delete()

                ConnectedTerm.query.filter(ConnectedTerm.term2_id.in_(removed_terms),
                                           ConnectedTerm.term1_id == model.id,
                                           ConnectedTerm.is_synonym == is_synonym,
                                           ConnectedTerm.is_english == is_english).delete()


        try:
            if form.connections_field.data:
                related_term_ids = {term.id for term in model.get_related_terms()}
                field_term_ids = {int(term_id) for term_id in form.connections_field.raw_data}
                update_connected_terms(related_term_ids, field_term_ids, False, False)

            if form.synonyms_field.data:
                synonym_ids = {term.id for term in model.get_synonyms()}
                field_term_ids = {int(term_id) for term_id in form.synonyms_field.raw_data}
                update_connected_terms(synonym_ids, field_term_ids, True, False)

            if form.eng_synonyms_field.data:
                synonym_ids = {term.id for term in model.get_synonyms(is_english=True)}
                field_term_ids = {int(term_id) for term_id in form.eng_synonyms_field.raw_data}
                update_connected_terms(synonym_ids, field_term_ids, True, True)

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

        synonyms = [synonym for synonym in model.get_synonyms()]
        eng_synonyms = [synonym for synonym in model.get_synonyms(is_english=True)]
        related_words = [related_word for related_word in model.get_related_terms()]

        form.connections_field.default = related_words
        form.synonyms_field.default = synonyms
        form.eng_synonyms_field.default = eng_synonyms
        form.connections_field.process(None, related_words or unset_value)
        form.synonyms_field.process(None, synonyms or unset_value)
        form.eng_synonyms_field.process(None, eng_synonyms or unset_value)

        super().on_form_prefill(form, id)

    def on_model_delete(self, model):
        # Manually delete connections (ConnectedTerm records) referencing the term
        ConnectedTerm.query.filter((ConnectedTerm.term1_id == model.id) | (ConnectedTerm.term2_id == model.id)).delete(synchronize_session=False)

        # Proceed with the actual term deletion
        super().on_model_delete(model)

