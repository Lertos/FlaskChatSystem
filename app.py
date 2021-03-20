from flask import Flask, render_template, redirect, request, url_for, session, Response
from modules import db_manager, helper

app = Flask(__name__)

app.secret_key = b'\xe4$Y2\xd5\xbb_\xab#\xfd*\x1e\xe2v\xa8J'

app.config['JSON_AS_ASCII'] = False

database = db_manager.MySQLPool()


#===============================

#Setup

#===============================

helper.debugServerDictionaries()


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

        result = database.getPlayerLogin(username, password)
        
        #If the statement returned anything (meaning the combo exists) - log them in
        if(result != {}):
            session['playerId'] = result['player_id']
            session['username'] = result['username']
            session['displayName'] = result['display_name']
            session['className'] = result['class_name']
            session['playerLevel'] = result['player_level']
            

            #Check is the character has been created yet
            if(result['has_character'] == 1):
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
        user = database.createPlayerAccount(username, displayName, password)

        #Account was successfully created
        if(user['username'] != '' and user['display_name'] != ''):
            session['playerId'] = user['player_id']
            session['username'] = user['username']
            session['displayName'] = user['display_name']

        #Either the username or the displayname is already taken
        else:
            if(user['username'] == ''):
                errorMessage = 'That username is already taken'
            else:
                errorMessage = 'That display name is already taken'

            return render_template('signup.html', errorMessage=errorMessage)

        #Take them to the character creation screen
        return redirect(url_for('characterCreation'))

    else:
        return render_template('signup.html', errorMessage='')


@app.route('/characterCreation', methods=['GET', 'POST'])
def characterCreation():
    if request.method == 'POST':
        data = [request.form['className'], request.form['avatarName'], session['playerId']]
        database.createNewCharacter(data)
        
        session['className'] = request.form['className']
        session['playerLevel'] = 1

        return redirect(url_for('dashboard'))

    return render_template('characterCreation.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    playerId = session['playerId']

    #For testing new items out
    #if request.method == 'POST':
    #    helper.debugCreateItems(playerId, session['className'], 28, 10, 100)

    player = database.getDashboardDetails(playerId)
    classInfo = helper.getClassInfo(session['className'])
    equippedItems = database.getPlayerEquippedItems(playerId)
    items = database.getPlayerInventory(playerId)


    return render_template('dashboard.html', player=player, classInfo=classInfo, equippedItems=equippedItems, items=items)


@app.route('/sellItem', methods=['POST'])
def sellItem():

    playerId = request.form['playerId']
    sellPrice = request.form['sellPrice']
    inventoryId = request.form['inventoryId']

    if int(playerId) == int(session['playerId']):
        database.sellInventoryItem(playerId, sellPrice, inventoryId)

    return Response('', status=201)


@app.route('/equipItem', methods=['POST'])
def equipItem():

    playerId = request.form['playerId']
    inventoryId = request.form['inventoryId']

    if int(playerId) == int(session['playerId']):
        database.equipInventoryItem(playerId, inventoryId)

    return Response('', status=201)


@app.route('/unequipItem', methods=['POST'])
def unequipItem():

    playerId = request.form['playerId']
    inventoryId = request.form['inventoryId']

    if int(playerId) == int(session['playerId']):
        database.unequipInventoryItem(playerId, inventoryId)

    return Response('', status=201)


@app.route('/travel')
def travel():

    playerId = session['playerId']

    #If player is not travelling - redirect to dashboard
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        return redirect(url_for('dashboard'))

    #Get the time left from the end of the travel
    timeLeft = helper.getTimeLeftFromEpochTime(travelInfo['travel_time'])

    if timeLeft <= 0:
        return redirect(url_for('results'))

    return render_template('travel.html', travelInfo=travelInfo, timeLeft=timeLeft)


@app.route('/eventDone')
def eventDone():

    playerId = session['playerId']

    #If player is not travelling return an error
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        return Response('', status=400)

    #Get the time left from the end of the travel
    timeLeft = helper.getTimeLeftFromEpochTime(travelInfo['travel_time'])

    if timeLeft <= 0:
        return Response('', status=201)

    return Response('', status=400)


@app.route('/results')
def results():

    playerId = session['playerId']

    #If player is not travelling - redirect to dashboard
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        return redirect(url_for('dashboard'))

    #Get the time left from the end of the travel
    timeLeft = helper.getTimeLeftFromEpochTime(travelInfo['travel_time'])

    return render_template('results.html', travelInfo=travelInfo, timeLeft=timeLeft)


@app.route('/startQuest', methods=['POST'])
def startQuest():

    playerId = session['playerId']

    monsterId = request.form['monsterId']
    helper.addQuestToTravelInfo(playerId, monsterId)

    if helper.getPlayerTravelInfo(playerId) != {}:
        return Response('', status=201)

    return Response('', status=400)


@app.route('/arena')
def arena():
    return render_template('arena.html')


@app.route('/quests')
def quests():

    playerId = session['playerId']

    #Check if the player is already travelling - if so, redirect them to the travel page
    #If player is not travelling - redirect to dashboard
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo != {}:
        return redirect(url_for('travel'))

    #Check if the player has active quests
    questMonsters = database.getPlayerQuestMonsters(playerId)

    #If they have active quests, load the quests page and build the quests provided
    if questMonsters != []:
        return render_template('quests.html', questMonsters=questMonsters)
    #If they do not have active quests, create some and reload the quests page
    else:
        playerStats = database.getPlayerStats(playerId)
        helper.createRandomQuestMonsters(playerId, session['playerLevel'], playerStats)
        
        return redirect(url_for('quests'))



@app.route('/bounties')
def bounties():
    return render_template('bounties.html')


@app.route('/dungeons')
def dungeons():
    return render_template('dungeons.html')


@app.route('/gathering')
def gathering():
    return render_template('gathering.html')


@app.route('/house')
def house():
    return render_template('house.html')


@app.route('/offerings')
def offerings():
    return render_template('offerings.html')


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))


@app.route('/sim')
def simulator():
    return render_template('/simulator/main.html')


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=80)