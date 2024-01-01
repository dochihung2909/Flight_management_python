from flask import render_template

from app import app

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

@app.route('/')
def index():
    return render_template('frontpage.html')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, port=4000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
