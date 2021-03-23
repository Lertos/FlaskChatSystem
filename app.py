from flask import Flask, render_template, redirect, request, url_for, session, Response
from modules import db_manager, helper, combat
import re

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.secret_key = b'\xe4$Y2\xd5\xbb_\xab#\xfd*\x1e\xe2v\xa8J'

database = db_manager.MySQLPool()


#===============================

#Setup

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
    
    seasonList = helper.seasonList
    
    if request.method == 'POST':

        errorMessage = ''

        username = request.form['username']
        displayName = request.form['displayName']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']
        season = request.form['season']

        #Check for tampering with the season value
        try:
            season = int(season)
        except ValueError:
            errorMessage = 'Dont mess with form values...'
            return render_template('signup.html', errorMessage=errorMessage, seasonList=seasonList)

        #Check if the username/display name/password meets length requirements
        if(len(username) < 6 or len(displayName) < 6 or len(password) < 6):

            if(len(username) < 6):
                errorMessage = 'Your username must be more than 6 characters'

            elif(len(displayName) < 6):
                errorMessage = 'Your display name must be more than 6 characters'
                
            else:
                errorMessage = 'Your password must be more than 6 characters'

            return render_template('signup.html', errorMessage=errorMessage, seasonList=seasonList)

        #Check if there are any symbols in the players username
        if re.match('^[\w-]+$', username) is None:
            errorMessage = 'Your username must not have symbols in it'
            return render_template('signup.html', errorMessage=errorMessage, seasonList=seasonList)

        #Check if there are any symbols in the players display name
        if re.match('^[\w-]+$', displayName) is None:
            errorMessage = 'Your display name must not have symbols in it'
            return render_template('signup.html', errorMessage=errorMessage, seasonList=seasonList)

        #Check if passwords are the same
        if(password != passwordConfirm):
            errorMessage = 'Passwords do not match'
            return render_template('signup.html', errorMessage=errorMessage, seasonList=seasonList)

        #Make the call to create the account to the database and check if the username and/or display name already exist
        user = database.createPlayerAccount(username, displayName, password, season)

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

            return render_template('signup.html', errorMessage=errorMessage, seasonList=seasonList)

        #Take them to the character creation screen
        return redirect(url_for('characterCreation'))

    else:
        return render_template('signup.html', errorMessage='', seasonList=seasonList)


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
    playerLevel = session['playerLevel']

    #For testing new items out
    if request.method == 'POST':
        helper.debugCreateItems(playerId, session['className'], 28, playerLevel, playerLevel)

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

    #If the event was a monster
    if travelInfo['typeOfEvent'] != 'gather':
        #Get the stats of the player and the monster
        player = database.getPlayerStats(playerId)
        monster = helper.createMonsterForBattle(player, playerId, travelInfo['quest_monster_id'], travelInfo['typeOfEvent'])

        #Fix player stats as base stats and equipment stats are separate
        player = helper.combinePlayerStats(player)

        #Start combat
        battleLog = combat.setupFight(player, monster)
        combat.translateBattleLog(battleLog['log'])

        #Give winnings
        playerWon = False
        if battleLog['winner'] == player['name']:
            playerWon = True

        playerLevel = helper.completePlayerEvent(playerId, playerWon, monster)
        playerLevel = playerLevel[0]['player_level']

        #Check for level ups
        if session['playerLevel'] != playerLevel:
            session['playerLevel'] = playerLevel

        #Remove travel information to generate new events
        helper.removePlayerTravelInfo(playerId)

        return render_template('results.html', travelInfo=travelInfo, player=player, monster=monster, battleLog=battleLog)
    #If the event was gathering
    else:
        pass


@app.route('/cancelEvent', methods=['POST'])
def cancelEvent():

    playerId = session['playerId']

    #Remove the player from the travel dict
    helper.removePlayerTravelInfo(playerId)

    return Response('', status=201)


@app.route('/startQuest', methods=['POST'])
def startQuest():

    playerId = session['playerId']
    monsterId = request.form['monsterId']

    #If the player isn't travelling already, proceed
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        #Get the player stats and add travel info - assuming they have enough stamina
        player = database.getPlayerStats(playerId)
        helper.addQuestToTravelInfo(playerId, monsterId)

        #Get the travel info again to ensure they have the correct stamina
        travelInfo = helper.getPlayerTravelInfo(playerId)

        #Check if player has stamina - if not remove them from the travel dict
        if player['stamina'] < travelInfo['stamina']:
            helper.removePlayerTravelInfo(playerId)
            return Response('NO_STAMINA', status=201)

        return Response('START_QUEST', status=201)

    return Response('ALREADY_IN_EVENT', status=201)


@app.route('/arena')
def arena():
    return render_template('arena.html')


@app.route('/quests')
def quests():

    playerId = session['playerId']

    #Check if the player is already travelling - if so, redirect them to the travel page
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo != {}:
        return redirect(url_for('travel'))

    #Check if the player has active quests
    questMonsters = database.getPlayerQuestMonsters(playerId)

    #If they have active quests, load the quests page and build the quests provided
    if questMonsters != []:
        playerStats = database.getPlayerStats(playerId)
        playerStamina = playerStats['stamina']

        return render_template('quests.html', questMonsters=questMonsters, playerStamina=playerStamina)
    #If they do not have active quests, create some and reload the quests page
    else:
        playerStats = database.getPlayerStats(playerId)
        helper.createRandomQuestMonsters(playerId, playerStats)
        
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