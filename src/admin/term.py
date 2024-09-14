from src.admin.base import SecureModelView
from src.models import ConnectedTerm
from flask_ckeditor import CKEditorField
from flask_admin.form.widgets import Select2Widget



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


    form_overrides = {
            'context_source': CKEditorField,
            'term_source': CKEditorField,
            'definition_source': CKEditorField,
            
        }
    create_template = 'admin/edit.html'  
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
        "connected_terms"
    ]

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
        "synonyms",
        "connected_terms"
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
        "connected_terms": "დაკავშირებული სიტყვები"
    }


    form_args = {
        'synonyms': {
            'widget': Select2Widget(multiple=True)
        },
        'connected_terms': {
            'widget': Select2Widget(multiple=True)
        }
    }


    def on_model_change(self, form, model, is_created):
        
        # Add synonyms
        if form.synonyms.data:
            for synonym_id in form.synonyms.data:
                if synonym_id != model.id:
                    ConnectedTerm(term1_id=model.id, term2_id=synonym_id, is_synonym=True).save()
        
        # Add connected terms
        if form.connected_terms.data:
            for connected_id in form.connected_terms.data:
                if connected_id != model.id:
                    ConnectedTerm(term1_id=model.id, term2_id=connected_id, is_synonym=False).save()

        super().on_model_change(form, model, is_created)


    def on_model_delete(self, model):
        # Manually delete connections (ConnectedTerm records) referencing the term
        ConnectedTerm.query.filter(
            (ConnectedTerm.term1_id == model.id) | (ConnectedTerm.term2_id == model.id)
        ).delete(synchronize_session=False)

        # Proceed with the actual term deletion
        super().on_model_delete(model)


