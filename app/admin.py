from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from app import app, dao, db
from app.models import UserRoleEnum, User, Flight, Route, Airport, Aircraft, Policy
from datetime import datetime

class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin = Admin(app=app, name='Quản lý chuyến bay', template_mode='bootstrap4', index_view=MyAdmin())


class AuthenticatedAdmin(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class AuthenticatedAdminModel(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedEmployee(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.user_role == UserRoleEnum.EMPLOYEE or current_user.user_role == UserRoleEnum.ADMIN)


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedUser):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


class RouteViewModel(AuthenticatedEmployee):
    column_list = ('id', 'departure_airport.name', 'arrival_airport.name')
    column_labels = {
        'departure_airport.name': 'Departure Airport',
        'arrival_airport.name': 'Arrival Airport'
    }

class FlightViewModel(AuthenticatedEmployee):
    column_list = ('id', 'departure_time', 'time_flight', 'route', 'aircraft')
    column_labels = {
    }

class UserViewModel(AuthenticatedEmployee):
    column_list = ('id', 'name', 'username', 'user_role')

class EmployeeAdd(AuthenticatedAdmin):
    @expose('/')
    def index(self):
        return self.render('admin/add_employee.html', )

class PolicyManagement(AuthenticatedAdmin):
    @expose('/')
    def index(self):
        return self.render('admin/policy.html', policy=dao.get_policy())


class StatsView(AuthenticatedAdmin):
    @expose('/')
    def index(self):
        data = request.args
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        print(from_date, to_date)
        stats = dao.stats_revenue_route()
        month_year = data.get('month_year')
        if month_year:
            month_year_obj  = datetime.strptime(month_year, '%Y-%m')
            month = month_year_obj.month
            year = month_year_obj.year
            stats = dao.stats_revenue_route_by_month(year=year, month=month)
        if from_date:
            from_date = datetime.strptime(from_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
            to_date = datetime.strptime(to_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
            stats = dao.stats_revenue_route(from_date=from_date, to_date=to_date)
            print(stats)
        return self.render('admin/stats.html', stats=stats)


admin.add_view(FlightViewModel(Flight, db.session))
admin.add_view(AuthenticatedEmployee(Aircraft, db.session))
admin.add_view(AuthenticatedEmployee(Airport, db.session))
admin.add_view(RouteViewModel(Route, db.session))
admin.add_view(EmployeeAdd(name='Thêm nhân viên', endpoint='add_employee'))
admin.add_view(UserViewModel(User, db.session))
admin.add_view(StatsView(name='Thống kê', endpoint='thongke'))
admin.add_view(PolicyManagement(name='Quản lý quy định', endpoint='policy'))
admin.add_view(LogoutView(name='Đăng Xuất'))