from flask_admin import Admin
from src.admin.base import SecureIndexView, LogoutMenuLink
from src.admin.term import EnglishTermView, TermView, CategoryView
from src.admin.user import UserView
from src.admin.about import AboutView



admin = Admin(index_view=SecureIndexView(), template_mode="bootstrap4", base_template="admin/admin_base.html")
admin.add_link(LogoutMenuLink(name="გასვლა", category="", url="/logout",  icon_type="fa", icon_value="fa-sign-out"))
