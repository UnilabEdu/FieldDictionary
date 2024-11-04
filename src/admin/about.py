from flask_ckeditor import CKEditorField
from src.config import Config
from flask_admin.form.upload import FileUploadField
from bs4 import BeautifulSoup

from src.admin.base import SecureModelView


class AboutView(SecureModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_export = True

    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'

    form_columns = ['about_text', 'partner_name', 'logo', 'logo_link']
    column_list = ['about_text', 'partner_name', 'logo', 'logo_link']

    column_labels = {
        "about_text": "გვერდის შესახებ ინფორმაცია",
        "partner_name": "პარტნიორი კომპანია",
        "logo": "ლოგო",
        "logo_link": "ლინკი",

    }

    column_searchable_list = ['partner_name']
    column_sortable_list = ['partner_name']
    column_default_sort = ('partner_name', False)
    column_filters = ['partner_name']

    form_overrides = {
        'logo_link': CKEditorField,
        'logo': FileUploadField
    }

    form_args = {
        "logo": {
            "base_path": Config.UPLOAD_PATH,
            "allowed_extensions": ["svg", "jpg", "jpeg", "png", "gif"],  # Allow SVGs
        }
    }

    def on_model_change(self, form, model, is_created):
        # Clean the logo_link before saving
        if form.logo_link.data:
            soup = BeautifulSoup(form.logo_link.data, 'html.parser')
            model.logo_link = soup.get_text()  # Save only the URL

        super().on_model_change(form, model, is_created)



