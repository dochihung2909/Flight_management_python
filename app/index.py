from flask import render_template
from sqlalchemy.future import engine

from app import app, controller, dao, db, login

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app.add_url_rule('/', 'homepage', controller.home)
app.add_url_rule('/admin/login', 'admin_login', controller.login_page, methods=['POST'])
app.add_url_rule('/em/schedule', 'employee_schedule', controller.creae_schedule)
app.add_url_rule('/api/flight', 'add_flight', controller.add_flight, methods=['POST'])
app.add_url_rule('/api/flight', 'show_flight', controller.show_flight, methods=['GET'])

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db.metadata.clear()
    from app.admin import *

    app.run(debug=True, port=4000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
