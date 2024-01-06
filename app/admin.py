from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from app import app, dao, db
from app.models import UserRoleEnum, User

class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin = Admin(app=app, name='Quản lý chuyến bay', template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.account_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedUser):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


admin.add_view(ModelView(User, db.session))
admin.add_view(LogoutView(name='Đăng Xuất'))