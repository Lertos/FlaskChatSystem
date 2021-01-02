from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #Instead of tuples, it uses dictionary

mysql = MySQL(app)


comments = []

@app.route("/", methods=["GET", "POST"])
def main():
    cursor = mysql.connection.cursor()
    cursor.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')

    #If it was a GET request, simply display the page
    if request.method == "GET":
        return render_template("index.html", comments=comments)

    #If the request was not a GET - add the text inside of the 'contents' form to our list
    comments.append(request.form["contents"])
    #Says: Please request this page again, this time using a 'GET' method (default request)
    return redirect(url_for('main'))

@app.route("/about")
def about():
    return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)