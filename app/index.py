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
app.add_url_rule('/login', 'login', controller.login, methods=['POST', 'GET'])
app.add_url_rule('/signup', 'signup', controller.signup, methods=['POST', 'GET'])
app.add_url_rule('/logout', 'logout', controller.logout)
app.add_url_rule('/em/<slug>', 'employee', controller.employee_page)
app.add_url_rule('/api/flight', 'add_flight', controller.add_flight, methods=['POST', 'GET'])

# Create a permission with a single Need, in this case a RoleNeed.


# protect a view with a principal for that need
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    user = current_user
    # Add the UserNeed to the identity
    if hasattr(user, 'id'):
        identity.provides.add(UserNeed(user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(user, 'user_role'):
        # for role in user.user_role:
        identity.provides.add(RoleNeed(user.user_role))


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db.metadata.clear()
    from app.admin import *

    app.run(debug=True, port=4000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
