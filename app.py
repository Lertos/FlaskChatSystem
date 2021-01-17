from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = b'\xe4$Y2\xd5\xbb_\xab#\xfd*\x1e\xe2v\xa8J'

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'joker420lolA!'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'flasksimplerpg'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #Instead of tuples, it uses dictionary

mysql = MySQL(app)

#===============================

#Global Variables

#===============================



#===============================

#Routes

#===============================

@app.route("/")
def index():
    #If the session DOES exist, they are already logged in - send them to their dashboard
    if 'username' in session:
        return redirect(url_for('dashboard'))
    #If the session DOES NOT exist for this connection, make the user sign in
    else:
        return redirect(url_for('signin'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        #Check if the username/password combination exists
        data = [username, password]
        stmt = '''SELECT username, displayName, hasCharacter FROM users WHERE username = %s and password = %s;'''
        cursor.execute(stmt, data)
        
        results = cursor.fetchone()
        
        #If the statement returned anything (meaning the combo exists) - log them in
        if(results is not None):
            session['username'] = results['username']
            session['displayName'] = results['displayName']

            #Check is the character has been created yet
            if(results['hasCharacter'] == 1):
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('characterCreation'))

        #If the username/password combo doesn't exist - display combo error
        else:
            return render_template('signin.html', errorMessage='That username/password combination doesn''t exist')

    else:
        return render_template('signin.html', errorMessage='')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        errorMessage = ''

        username = request.form['username']
        displayName = request.form['displayName']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']

        #Check if the username/display name/password meets length requirements
        if(len(username) < 6 or len(displayName) < 6 or len(password) < 6):

            if(len(username) < 6):
                errorMessage = 'Your username must be more than 6 characters'

            elif(len(displayName) < 6):
                errorMessage = 'Your display name must be more than 6 characters'
                
            else:
                errorMessage = 'Your password must be more than 6 characters'

            return render_template('signup.html', errorMessage=errorMessage)

        #Check if passwords are the same
        if(password != passwordConfirm):
            errorMessage = 'Passwords do not match'
            return render_template('signup.html', errorMessage=errorMessage)

        #Make the call to create the account to the database and check if the username and/or display name already exist
        args = [username, displayName, password]
        cursor = mysql.connection.cursor()
        
        cursor.callproc('CreateUserAccount', args)

        user = cursor.fetchone()

        #Account was successfully created
        if(user['username'] != '' and user['displayName'] != ''):
            session['username'] = user['username']
            session['displayName'] = user['displayName']
        #Either the username or the displayname is already taken
        else:
            if(user['username'] == ''):
                errorMessage = 'That username is already taken'
            else:
                errorMessage = 'That display name is already taken'

            return render_template('signup.html', errorMessage=errorMessage)


        cursor.close()

        #Take them to the character creation screen
        return redirect(url_for('characterCreation'))

    else:
        return render_template('signup.html', errorMessage='')


@app.route('/characterCreation', methods=['GET', 'POST'])
def characterCreation():
    if request.method == 'POST':

        username = session['username']
        className = request.form['className']
        avatarName = request.form['avatarName']

        print(str(className) + " - " + str(avatarName))

        cursor = mysql.connection.cursor()
        
        data = [className, avatarName, username]
        stmt = '''UPDATE users SET className = %s, avatarName = %s, hasCharacter = 1 WHERE username = %s;'''
        cursor.execute(stmt, data)

        mysql.connection.commit()

        cursor.close()
        
        return redirect(url_for('dashboard'))

    return render_template('characterCreation.html')


@app.route('/dashboard')
def dashboard():

    args = [session['username']]
    cursor = mysql.connection.cursor()
    
    cursor.callproc('GetDashboardDetails', args)

    user = cursor.fetchone()

    cursor.close()

    displayName = user['displayName']
    className = user['className']
    avatarName = user['avatarName']

    return render_template('dashboard.html', displayName=displayName, className=className, avatarName=avatarName)


@app.route('/arena')
def arena():
    return render_template('arena.html')


@app.route('/tavern')
def tavern():
    return render_template('tavern.html')


@app.route('/market')
def market():
    return render_template('market.html')


@app.route('/dungeon')
def dungeon():
    return render_template('dungeon.html')


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))



if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=80)