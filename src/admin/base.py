from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask import url_for, redirect, make_response
from flask_admin.menu import MenuLink
from flask_login import current_user

from csv import writer
from codecs import BOM_UTF8
from io import StringIO

from werkzeug.utils import secure_filename


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("main.login"))

    def _export_csv(self, return_url):
        _, row_data = self._export_data()
        columns = [column[1] for column in self._export_columns]

        memory_stream = StringIO()
        csv = writer(memory_stream)

        csv.writerow(columns)
        for row in row_data:
            values = [self.get_export_value(row, c[0]) for c in self._export_columns]
            csv.writerow(values)
        memory_stream.seek(0)

        filename = self.get_export_name(export_type='csv')
        response = make_response(f"{BOM_UTF8.decode('utf-8')}{memory_stream.getvalue()}")
        response.mimetype = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={secure_filename(filename)}'
        return response


class SecureIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("main.login"))

    def is_visible(self):
        return False
        
    @expose('/')
    def index(self):
        return redirect(url_for('term_panel.index_view'))
    

class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated
    
class LoginMenuLink(MenuLink):
    def is_accessible(self):
        return not current_user.is_authenticated 
    
