from src.admin.base import SecureModelView
from wtforms import PasswordField
from werkzeug.security import generate_password_hash



class UserView(SecureModelView):
    can_view_details = True
    can_create = True
    can_delete = True
    column_list = ["username", "password", "email"]

    form_overrides = dict(password=PasswordField)
    form_extra_fields = {
        
        'password': PasswordField('Password')
    }

    form_columns = ('username', 'email', 'password',)

    



    


        

        