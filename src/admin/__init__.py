from flask_admin import Admin
from src.admin.base import SecureIndexView
from src.admin.base import LogoutMenuLink


admin = Admin(index_view=SecureIndexView(), template_mode="bootstrap4")


admin.add_link(LogoutMenuLink(name="Logout", category="", url="/logout"))