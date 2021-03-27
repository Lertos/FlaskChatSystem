from flask import Flask, render_template, redirect, request, url_for, session, Response
from modules import db_manager, helper, combat, validation
import random


#===============================

#Setup

#===============================


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.secret_key = b'\xe4$Y2\xd5\xbb_\xab#\xfd*\x1e\xe2v\xa8J'

database = db_manager.MySQLPool()


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


#===============================

#Signin / Signup / Character Creation

#===============================


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        result = database.getPlayerLogin(username, password)
        
        #If the statement returned anything (meaning the combo exists) - log them in
        if(result != {}):
            session['playerId'] = result['player_id']
            session['className'] = result['class_name']
            session['playerLevel'] = result['player_level']
            session['displayName'] = result['display_name']

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

        username = request.form['username']
        displayName = request.form['displayName']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']
        season = request.form['season']

        errorMessage = validation.validateAccountInfo(username, displayName, password, passwordConfirm, season)

        #If there was an error message send it back to the page
        if errorMessage != '':
            return render_template('signup.html', errorMessage=errorMessage, seasonList=seasonList)

        #Make the call to create the account to the database and check if the username and/or display name already exist
        user = database.createPlayerAccount(username, displayName, password, season)

        #Account was successfully created
        if(user['username'] != '' and user['display_name'] != ''):
            session['playerId'] = user['player_id']
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


#===============================

#Dashboard

#===============================


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    playerId = session['playerId']
    playerLevel = session['playerLevel']

    #For testing new items out
    if request.method == 'POST':
        helper.debugCreateItems(playerId, session['className'], 21, playerLevel, playerLevel)

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


#===============================

#Quests

#===============================


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


#===============================

#Travel

#===============================


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


@app.route('/cancelEvent', methods=['POST'])
def cancelEvent():

    playerId = session['playerId']

    #Remove the player from the travel dict
    helper.removePlayerTravelInfo(playerId)

    return Response('', status=201)


#===============================

#Results

#===============================


@app.route('/results')
def results():

    playerId = session['playerId']

    #If player is not travelling - redirect to dashboard
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        return redirect(url_for('dashboard'))

    #Get the stats of the player and the monster
    player = database.getPlayerStats(playerId)
    monster = helper.createMonsterForBattle(player, playerId, travelInfo)

    #Fix player stats as base stats and equipment stats are separate
    player = helper.combinePlayerStats(player)

    #Start combat
    battleLog = combat.setupFight(player, monster)
    combat.translateBattleLog(battleLog['log'])

    #Give winnings
    playerWon = False
    if battleLog['winner'] == player['name']:
        playerWon = True

        #Check if the entity will drop something
        if travelInfo['typeOfEvent'] == 'bounty':
            dropChance = monster['drop_chance']
        else:
            #Apply any blessings of the player
            blessing = database.getActiveBlessing(playerId)

            if blessing == 'drops':
                dropChance = 0.43
            else:
                dropChance = 0.33

        if random.uniform(0,1) <= dropChance:
            if database.doesPlayerHaveInventorySpace(playerId):
                travelInfo['droppedLoot'] = 1
            else:
                travelInfo['droppedLoot'] = 0
        else:
            travelInfo['droppedLoot'] = 0

    #Give the player the rewards
    playerLevel = helper.completePlayerEvent(playerId, playerWon, player, monster, travelInfo)
    playerLevel = playerLevel[0]['player_level']

    #Check for level ups
    if session['playerLevel'] != playerLevel:
        session['playerLevel'] = playerLevel

    #Remove travel information to generate new events
    helper.removePlayerTravelInfo(playerId)

    return render_template('results.html', travelInfo=travelInfo, player=player, monster=monster, battleLog=battleLog)


#===============================

#Bounties

#===============================


@app.route('/bounties')
def bounties():

    playerId = session['playerId']
    
    #Check if the player is high enough level to try bounties
    if session['playerLevel'] < 10:
        return render_template('bounties.html', bountyMonsters=None, bountyAttempts=None, unlocked=False)

    #Check if the player is already travelling - if so, redirect them to the travel page
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo != {}:
        return redirect(url_for('travel'))

    #Check if the player has active bounties
    bountyMonsters = database.getPlayerBountyMonsters(playerId)

    #If they have active bounties, load the bounties page and build the bounties provided
    if bountyMonsters != []:
        playerStats = database.getPlayerStats(playerId)
        bountyAttempts = playerStats['bounty_attempts']

        return render_template('bounties.html', bountyMonsters=bountyMonsters, bountyAttempts=bountyAttempts, unlocked=True)

    #If they do not have active bounties, create some and reload the bounties page
    else:
        playerStats = database.getPlayerStats(playerId)
        helper.createRandomBountyMonsters(playerId, playerStats)
        
        return redirect(url_for('bounties'))


@app.route('/startBounty', methods=['POST'])
def startBounty():

    playerId = session['playerId']
    monsterId = request.form['monsterId']
    multiplier = request.form['multiplier']

    #If the player isn't travelling already, proceed
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        #Get the player stats and add travel info - assuming they have enough attempts
        player = database.getPlayerStats(playerId)
        helper.addBountyToTravelInfo(playerId, monsterId, multiplier)

        #Get the travel info again to ensure they have bounty attempts
        travelInfo = helper.getPlayerTravelInfo(playerId)

        #Check if player has bounty attempts - if not remove them from the travel dict
        if player['bounty_attempts'] <= 0:
            helper.removePlayerTravelInfo(playerId)
            return Response('NO_ATTEMPTS', status=201)

        return Response('START_BOUNTY', status=201)

    return Response('ALREADY_IN_EVENT', status=201)


#===============================

#Arena

#===============================


@app.route('/arena')
def arena():
    return render_template('arena.html')


#===============================

#Dungeons

#===============================


@app.route('/dungeons')
def dungeons():

    playerId = session['playerId']

    return render_template('dungeons.html')


#===============================

#Offerings

#===============================


@app.route('/offerings')
def offerings():
    playerId = session['playerId']
    active = database.getActiveBlessing(playerId)

    return render_template('offerings.html', active=active)


@app.route('/applyBlessing', methods=['POST'])
def applyBlessing():
    playerId = session['playerId']
    blessing = request.form['blessingType']
    active = database.getActiveBlessing(playerId)

    if active != '':
        return Response('ALREADY_BLESSED', status=201)

    database.applyBlessing(playerId, blessing)

    return Response('', status=201)


#===============================

#Leaderboards

#===============================


@app.route('/leaderboard', methods=['GET','POST'])
def leaderboard():
    seasonList = helper.seasonList

    if request.method == 'POST':
        boardType = request.form['boardType']
        season = request.form['season']

        boardData = helper.getLeaderboardData(boardType, season)

        header = boardData[0]
        data = boardData[1]
        
        return render_template('leaderboard.html', seasonList=seasonList, boardType=boardType, season=season, header=header, data=data, displayName=session['displayName'])

    return render_template('leaderboard.html', seasonList=seasonList, boardType='')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))


@app.route('/sim')
def simulator():
    return render_template('/simulator/main.html')


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=80)