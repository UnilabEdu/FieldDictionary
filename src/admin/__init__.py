from flask_admin import Admin
from src.admin.base import SecureIndexView
from src.admin.base import LogoutMenuLink



admin = Admin(index_view=SecureIndexView(), template_mode="bootstrap4", base_template="admin/admin_base.html")
admin.add_link(LogoutMenuLink(name="გასვლა", category="", url="/logout",  icon_type="fa", icon_value="fa-sign-out"))
