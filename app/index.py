from flask import render_template, Response
from sqlalchemy.future import engine

from app import app, controller, dao, db, login, principals
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed, Permission
from app.models import User, UserRoleEnum

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app.add_url_rule('/', 'homepage', controller.home)
app.add_url_rule('/admin/login', 'admin_login', controller.login_page, methods=['POST'])
app.add_url_rule('/admin/employee', 'add_employee', controller.add_employee, methods=['POST'])
app.add_url_rule('/admin/policy/<policy_id>', 'update_policy', controller.update_policy, methods=['POST'])
app.add_url_rule('/login', 'login', controller.login, methods=['POST', 'GET'])
app.add_url_rule('/signup', 'signup', controller.signup, methods=['POST', 'GET'])
app.add_url_rule('/logout', 'logout', controller.logout)
app.add_url_rule('/em/<slug>', 'employee', controller.employee_page)
app.add_url_rule('/em', 'employee_login', controller.employee_login)
app.add_url_rule('/em/sell_ticket', 'employee_sell_ticket', controller.sell_ticket, methods=['POST', 'GET'])
app.add_url_rule('/api/flight', 'add_flight', controller.add_flight, methods=['POST', 'GET'])
app.add_url_rule('/flight', 'flight_view', controller.flight_booking, methods=['POST', 'GET'])
app.add_url_rule('/flight/payment', 'payment', controller.payment, methods=['POST','GET'])
app.add_url_rule('/api/checkout', 'checkout_ticket', controller.checkout, methods=['POST'])


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db.metadata.clear()
    from app.admin import *

    app.run(debug=True, port=4000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
