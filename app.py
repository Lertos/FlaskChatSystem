from flask import Flask, render_template, redirect, request, url_for, session, Response
from modules import db_manager, helper, combat, validation
import random, time, os


#===============================

#Setup

#===============================


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.secret_key = os.urandom(24)


database = db_manager.mysql_pool


#===============================

#Routes

#===============================


@app.route("/")
def index():
    #If session exists - they are already logged in; send to dashboard
    if 'playerId' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('signin'))

#===============================

#Signin / Signup / Character Creation

#===============================


@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if request.method == 'POST':

        if 'playerId' in session:
            session.pop('playerId', None)
        if 'className' in session:
            session.pop('className', None)
        if 'playerLevel' in session:
            session.pop('playerLevel', None)
        if 'displayName' in session:
            session.pop('displayName', None)

        username = request.form['username']
        password = request.form['password']

        result = database.getPlayerLogin(username, password)

        #If the statement returned anything (meaning the combo exists) - log them in
        if(result != {}):
            session['playerId'] = result['player_id']
            session['playerLevel'] = result['player_level']
            session['displayName'] = result['display_name']

            #Check is the character has been created yet
            if(result['has_character'] == 1):
                session['className'] = result['class_name']
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
        return redirect(url_for('signin'))

    else:
        return render_template('signup.html', errorMessage='', seasonList=seasonList)


@app.route('/characterCreation', methods=['GET', 'POST'])
def characterCreation():

    #If the player is logged in and has a character
    if 'playerId' in session and 'className' in session:
        print(session)
        return redirect(url_for('dashboard'))

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


#@app.route('/dashboard', methods=['GET','POST'])
@app.route('/dashboard', methods=['GET'])
def dashboard():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']
    #playerLevel = session['playerLevel']

    #For testing new items out
    #if request.method == 'POST':
    #    pass
        #helper.debugCreateItems(playerId, session['className'], 21, playerLevel, playerLevel)

    player = database.getDashboardDetails(playerId)
    classInfo = helper.getClassInfo(session['className'])
    equippedItems = database.getPlayerEquippedItems(playerId)
    items = database.getPlayerInventory(playerId)

    print('----->',session['displayName'],'DASHBOARD')
    return render_template('dashboard.html', player=player, classInfo=classInfo, equippedItems=equippedItems, items=items)


@app.route('/sellItem', methods=['POST'])
def sellItem():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = request.form['playerId']
    sellPrice = request.form['sellPrice']
    inventoryId = request.form['inventoryId']

    #Check for tampering
    if int(playerId) == int(session['playerId']):
        items = database.getPlayerItemsWithSellPriceAndType(playerId)

        if validation.isPriceCorrect(items, sellPrice, inventoryId):
            database.sellInventoryItem(playerId, sellPrice, inventoryId)
            return Response('', status=203)

    return Response('', status=201)


@app.route('/equipItem', methods=['POST'])
def equipItem():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = request.form['playerId']
    inventoryId = request.form['inventoryId']

    if int(playerId) == int(session['playerId']):
        database.equipInventoryItem(playerId, inventoryId)

    return Response('', status=201)


@app.route('/unequipItem', methods=['POST'])
def unequipItem():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = request.form['playerId']
    inventoryId = request.form['inventoryId']

    if int(playerId) == int(session['playerId']):
        database.unequipInventoryItem(playerId, inventoryId)

    return Response('', status=201)


@app.route('/upgradeStats', methods=['POST'])
def upgradeStats():

    if 'playerId' not in session:
        return redirect(url_for('signin'))


    playerId = session['playerId']
    stats = [request.form['totalStrength'], request.form['totalDexterity'], request.form['totalIntelligence'], request.form['totalConstitution'], request.form['totalLuck']]

    #Check to make sure the player can actually afford the upgrades
    spentGold = validation.canAffordUpgrades(playerId, stats)

    if spentGold != -1:
        #Only make the changes in the database if they didn't alter anything
        database.upgradePlayerStats(playerId, spentGold, stats)

    return Response('', status=201)

#===============================

#Quests

#===============================


@app.route('/quests')
def quests():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']

    #Check if the player travelling for another event
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo != {}:

        if travelInfo['typeOfEvent'] == 'arena' or travelInfo['typeOfEvent'] == 'dungeon':
            return redirect(url_for('results'))
        elif travelInfo['typeOfEvent'] == 'bounty' or travelInfo['typeOfEvent'] == 'quest':
            return redirect(url_for('travel'))

    #Check if the player has active quests
    questMonsters = database.getPlayerQuestMonsters(playerId)

    #If they have active quests, load the quests page and build the quests provided
    if questMonsters != []:
        playerStats = database.getPlayerStats(playerId)
        playerStamina = playerStats['stamina']

        print('----->',session['displayName'],'QUESTS')
        return render_template('quests.html', questMonsters=questMonsters, playerStamina=playerStamina)

    #If they do not have active quests, create some and reload the quests page
    else:
        playerStats = database.getPlayerStats(playerId)
        helper.createRandomQuestMonsters(playerId, playerStats)

        return redirect(url_for('quests'))


@app.route('/startQuest', methods=['POST'])
def startQuest():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

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

        return Response('START_QUEST', status=203)

    return Response('ALREADY_IN_EVENT', status=202)


#===============================

#Travel

#===============================


@app.route('/travel')
def travel():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']

    #If player is not travelling - redirect to dashboard
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        print('==ERROR: Travel redirect to dashboard')
        return redirect(url_for('dashboard'))

    #Check for travel types that should not be here
    if travelInfo['typeOfEvent'] == 'arena' or travelInfo['typeOfEvent'] == 'dungeon':
        return redirect(url_for('results'))

    #Get the time left from the end of the travel
    timeLeft = helper.getTimeLeftFromEpochTime(travelInfo['travel_time'])

    if timeLeft <= 0:
        return redirect(url_for('results'))

    print('----->',session['displayName'],'TRAVEL')
    return render_template('travel.html', travelInfo=travelInfo, timeLeft=timeLeft)


@app.route('/eventDone')
def eventDone():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']

    #If player is not travelling return an error
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        print('==ERROR: /eventDone had no travel info')
        return Response('', status=202)

    #Get the time left from the end of the travel
    timeLeft = helper.getTimeLeftFromEpochTime(travelInfo['travel_time'])

    if timeLeft <= 0:
        return Response('', status=201)

    return Response('', status=203)


@app.route('/cancelEvent', methods=['POST'])
def cancelEvent():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']

    #Remove the player from the travel dict
    helper.removePlayerTravelInfo(playerId)

    return Response('', status=201)


#===============================

#Results

#===============================


@app.route('/results')
def results():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']

    #If player is not travelling - redirect to dashboard
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        print('==ERROR: /results Empty travel info')
        return redirect(url_for('dashboard'))

    #Get the time left from the end of the travel for quests and bounties
    if travelInfo['typeOfEvent'] == 'quest' or travelInfo['typeOfEvent'] == 'bounty':
        timeLeft = helper.getTimeLeftFromEpochTime(travelInfo['travel_time'])

        if timeLeft > 0:
            return redirect(url_for('travel'))

    #Get the stats of the player and the monster
    player = database.getPlayerStats(playerId)

    if travelInfo['typeOfEvent'] == 'arena':
        monster = database.getPlayerStats(travelInfo['player_id'])
        monster = helper.combinePlayerStats(monster)
    elif travelInfo['typeOfEvent'] == 'dungeon':
        monster = travelInfo
    else:
        monster = helper.createMonsterForBattle(player, playerId, travelInfo)
        if monster == -1:
            print('==ERROR: /results MONSTER stats cannot be found - redirect to dashboard')
            return redirect(url_for('dashboard'))

    #Fix player stats as base stats and equipment stats are separate
    player = helper.combinePlayerStats(player)

    #Start combat
    battleLog = combat.setupFight(player, monster)
    combat.translateBattleLog(battleLog['log'])

    #Give winnings
    playerWon = False
    if battleLog['winner'] == player['name'] and travelInfo['typeOfEvent'] != 'arena':
        playerWon = True

        #Check if the entity will drop something
        if travelInfo['typeOfEvent'] == 'bounty':
            dropChance = monster['drop_chance']
        elif travelInfo['typeOfEvent'] == 'dungeon':
            dropChance = 1.0
        else:
            #Apply any blessings of the player
            blessing = database.getActiveBlessing(playerId)

            if blessing == 'drops':
                dropChance = 0.65
            else:
                dropChance = 0.45

            if session['playerLevel'] <= 4:
                dropChance += 0.25

        if random.uniform(0,1) <= dropChance:
            if database.doesPlayerHaveInventorySpace(playerId):
                travelInfo['droppedLoot'] = 1
            else:
                travelInfo['droppedLoot'] = 0
        else:
            travelInfo['droppedLoot'] = 0

    #Give the player the rewards
    if travelInfo['typeOfEvent'] == 'arena':
        if battleLog['winner'] == player['name']:
            winnerId = player['player_id']
            loserId = monster['player_id']
        else:
            loserId = player['player_id']
            winnerId = monster['player_id']

        database.processArenaHonor(player['player_id'], winnerId, loserId)
    else:
        playerLevel = helper.completePlayerEvent(playerId, playerWon, player, monster, travelInfo)
        playerLevel = playerLevel[0]['player_level']

        #Check for level ups
        if session['playerLevel'] != playerLevel:
            session['playerLevel'] = playerLevel

    #Remove travel information to generate new events
    helper.removePlayerTravelInfo(playerId)

    print('----->',session['displayName'],'RESULTS')
    return render_template('results.html', travelInfo=travelInfo, player=player, monster=monster, battleLog=battleLog)


#===============================

#Bounties

#===============================


@app.route('/bounties')
def bounties():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']

    #Check if the player is high enough level to try bounties
    if session['playerLevel'] < 10:
        print('----->',session['displayName'],'BOUNTIES')
        return render_template('bounties.html', bountyMonsters=None, bountyAttempts=None, unlocked=False)

    #Check if the player travelling for another event
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo != {}:
        if travelInfo['typeOfEvent'] == 'arena' or travelInfo['typeOfEvent'] == 'dungeon':
            return redirect(url_for('results'))
        elif travelInfo['typeOfEvent'] == 'quest' or travelInfo['typeOfEvent'] == 'bounty':
            return redirect(url_for('travel'))

    #Check if the player has active bounties
    bountyMonsters = database.getPlayerBountyMonsters(playerId)

    #If they have active bounties, load the bounties page and build the bounties provided
    if bountyMonsters != []:
        playerStats = database.getPlayerStats(playerId)
        bountyAttempts = playerStats['bounty_attempts']

        print('----->',session['displayName'],'BOUNTIES')
        return render_template('bounties.html', bountyMonsters=bountyMonsters, bountyAttempts=bountyAttempts, unlocked=True)

    #If they do not have active bounties, create some and reload the bounties page
    else:
        playerStats = database.getPlayerStats(playerId)
        helper.createRandomBountyMonsters(playerId, playerStats)

        return redirect(url_for('bounties'))


@app.route('/startBounty', methods=['POST'])
def startBounty():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

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

        return Response('START_BOUNTY', status=203)

    return Response('ALREADY_IN_EVENT', status=202)


#===============================

#Arena

#===============================


@app.route('/arena')
def arena():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']

    #Check if the player travelling for another event
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo != {}:
        if travelInfo['typeOfEvent'] == 'dungeon' or travelInfo['typeOfEvent'] == 'arena':
            return redirect(url_for('results'))
        elif travelInfo['typeOfEvent'] == 'quest' or travelInfo['typeOfEvent'] == 'bounty':
            return redirect(url_for('travel'))

    #Check if the player has active opponents
    opponents = database.getPlayerArenaOpponents(playerId)

    #If they have active opponents, load the arena page and build the opponents provided
    if opponents != []:
        playerStats = database.getPlayerStats(playerId)
        playerHonor = playerStats['honor']
        arenaAttempts = playerStats['arena_attempts']

        print('----->',session['displayName'],'ARENA')
        return render_template('arena.html', playerHonor=playerHonor, opponents=opponents, arenaAttempts=arenaAttempts)

    #If they do not have active opponents, create some and reload the arena page
    else:
        database.createArenaOpponents(playerId)

        return redirect(url_for('arena'))


@app.route('/startArenaFight', methods=['POST'])
def startArenaFight():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']
    opponentId = request.form['opponentId']

    #If the player isn't travelling already, proceed
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        #Get the player stats and add travel info - assuming they have enough attempts
        player = database.getPlayerStats(playerId)
        helper.addArenaFightToTravelInfo(player, playerId, opponentId)

        #Get the travel info again to ensure they have arena attempts
        travelInfo = helper.getPlayerTravelInfo(playerId)

        #Check if player has bounty attempts - if not remove them from the travel dict
        if player['arena_attempts'] <= 0:
            helper.removePlayerTravelInfo(playerId)
            return Response('NO_ATTEMPTS', status=201)

        return Response('START_ARENA', status=203)

    return Response('ALREADY_IN_EVENT', status=202)


#===============================

#Dungeons

#===============================


@app.route('/dungeons')
def dungeons():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']

    #Check if the player travelling for another event
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo != {}:
        if travelInfo['typeOfEvent'] == 'arena' or travelInfo['typeOfEvent'] == 'dungeon':
            return redirect(url_for('results'))
        elif travelInfo['typeOfEvent'] == 'quest' or travelInfo['typeOfEvent'] == 'bounty':
            return redirect(url_for('travel'))

    #Get the players dungeon info
    dungeonMonsters = database.getPlayerDungeonMonsters(playerId)

    #If they don't have it setup - return them to the dashboard gracefully
    if dungeonMonsters == []:
        return redirect(url_for('dashboard'))

    #Get the player dungeon attempts
    playerStats = database.getPlayerStats(playerId)
    dungeonAttempts = playerStats['dungeon_attempts']

    print('----->',session['displayName'],'DUNGEONS')
    return render_template('dungeons.html', dungeonMonsters=dungeonMonsters, dungeonAttempts=dungeonAttempts)


@app.route('/startDungeon', methods=['POST'])
def startDungeon():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']
    dungeonTier = request.form['dungeonTier']

    #If the player isn't travelling already, proceed
    travelInfo = helper.getPlayerTravelInfo(playerId)

    if travelInfo == {}:
        #Get the player stats and add travel info - assuming they have enough keys
        player = database.getPlayerStats(playerId)
        helper.addDungeonToTravelInfo(playerId, dungeonTier)

        #Get the travel info again to ensure they have dungeon keys
        travelInfo = helper.getPlayerTravelInfo(playerId)

        #Check if player has bounty attempts - if not remove them from the travel dict
        if player['dungeon_attempts'] <= 0:
            helper.removePlayerTravelInfo(playerId)
            return Response('NO_KEYS', status=201)

        return Response('START_DUNGEON', status=203)

    return Response('ALREADY_IN_EVENT', status=202)


#===============================

#Offerings

#===============================


@app.route('/offerings')
def offerings():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    playerId = session['playerId']
    active = database.getActiveBlessing(playerId)

    print('----->',session['displayName'],'OFFERINGS')
    return render_template('offerings.html', active=active)


@app.route('/applyBlessing', methods=['POST'])
def applyBlessing():

    if 'playerId' not in session:
        return redirect(url_for('signin'))

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

    if 'playerId' not in session:
        return redirect(url_for('signin'))

    seasonList = helper.seasonList

    if request.method == 'POST':
        boardType = request.form['boardType']
        season = request.form['season']

        boardData = helper.getLeaderboardData(boardType, season)

        header = boardData[0]
        data = boardData[1]

        print('----->',session['displayName'],'LEADERBOARD')
        return render_template('leaderboard.html', seasonList=seasonList, boardType=boardType, season=season, header=header, data=data, displayName=session['displayName'])

    print('----->',session['displayName'],'LEADERBOARD')
    return render_template('leaderboard.html', seasonList=seasonList, boardType='')


@app.route('/faq', methods=['GET'])
def faq():
    print('----->',session['displayName'],'FAQ')
    return render_template('faq.html')


@app.route('/logout')
def logout():
    session.pop('playerId', None)
    session.pop('className', None)
    session.pop('playerLevel', None)
    session.pop('displayName', None)
    return redirect(url_for('signin'))


@app.route('/sim')
def simulator():
    return render_template('/simulator/main.html')


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=80)