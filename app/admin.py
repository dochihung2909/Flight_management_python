from flask_admin import Admin, BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect, request
from app import app, dao
from models import UserRoleEnum

from datetime import datetime

admin = Admin(app=app, name='Quản lý chuyến bay', template_mode='bootstrap4')


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return True


class AuthenticatedAdmin(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.account_role == UserRoleEnum.ADMIN


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


admin.add_view(LogoutView(name='Đăng Xuất'))