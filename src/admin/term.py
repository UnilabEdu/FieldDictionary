from src.admin.base import SecureModelView
from src.models import Category



class ConnectedTermView(SecureModelView): 
    can_view_details = True
    
    # Exclude the relationship fields
    column_exclude_list = ['term1', 'term2']
    # Display foreign keys instead
    column_list = ['term1_id', 'term2_id', 'is_synonym']




class TermView(SecureModelView):
    can_view_details = True
    edit_modal = True
    create_modal = True
    can_create = True
    can_edit = True
    can_export = True

    inline_models = (Category,)

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
        "category"
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
        "category"
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
    }