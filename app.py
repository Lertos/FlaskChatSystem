from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = b'\xe4$Y2\xd5\xbb_\xab#\xfd*\x1e\xe2v\xa8J'

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'joker420lolA!'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'flasksimplerpg'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #Instead of tuples, it uses dictionary

#mysql = MySQL(app)

#===============================

#Global Variables

#===============================

comments = []
users = []

#===============================

#Routes

#===============================

@app.route("/", methods=["GET", "POST"])
def index():
    
    if 'username' in session:
        return 'Logged in'
    return redirect(url_for('login'))

    #cursor = mysql.connection.cursor()

    data = [('Jane', 'pass123')]
    stmt = "INSERT INTO users (username, password) VALUES (%s, %s);"
    #cursor.executemany(stmt, data)
    #mysql.connection.commit()

    stmt = "SELECT * FROM users;"
    #cursor.execute(stmt)
    #results = cursor.fetchall()
    users = results

    if request.method == 'GET':
        return render_template('index.html', comments=comments, users=users)


    #If the request was not a GET - add the text inside of the 'contents' form to our list
    comments.append(request.form["contents"])

    #Says: Please request this page again, this time using a 'GET' method (default request)
    return redirect(url_for('main'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']

        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=80)