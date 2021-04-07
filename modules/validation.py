import re, math
from modules import db_manager

database = db_manager.mysql_pool



#Validates the account creation info provided by the new player
def validateAccountInfo(username, displayName, password, passwordConfirm, season):
    #Check for tampering with the season value
    try:
        season = int(season)
    except ValueError:
        return 'Dont mess with form values...'

    #Check if the username/display name/password meets length requirements
    if(len(username) < 6 or len(displayName) < 6 or len(password) < 6):

        if(len(username) < 6):
            return 'Your username must be more than 6 characters'
        elif(len(displayName) < 6):
            return 'Your display name must be more than 6 characters'
        else:
            return 'Your password must be more than 6 characters'

    #Check if there are any symbols in the players username
    if re.match('^[\w-]+$', username) is None:
        return 'Your username must not have symbols in it'

    #Check if there are any symbols in the players display name
    if re.match('^[\w-]+$', displayName) is None:
        return 'Your display name must not have symbols in it'

    #Check if passwords are the same
    if(password != passwordConfirm):
        return 'Passwords do not match'

    return ''


#Checks if the player can actually afford the levels the page sent (to check for page tampering)
def canAffordUpgrades(playerId, stats):
    playerStats = database.getPlayerBaseStats(playerId)
    playerGold = playerStats['gold']
    spentGold = 0

    statNames = ['strength', 'dexterity', 'intelligence', 'constitution', 'luck']

    for i in range(0, len(statNames)):
        currentStatLevel = int(playerStats[statNames[i]])
        upgradedStatLevel = int(stats[i])

        if currentStatLevel > upgradedStatLevel:
            print('==ERROR: CanAffordUpgrades - Current stat bbigger than upgrade stat level')
            return -1

        for j in range(currentStatLevel, upgradedStatLevel):
            levelUpCost = getStatLevelCost(j + 1)
            playerGold -= levelUpCost
            spentGold += levelUpCost

        #Check if the player gold is zero yet
        if playerGold < 0:
            return -1

    return spentGold


#Gets the cost of the next stat level
def getStatLevelCost(level):
    return math.floor((level ** 2)/20 + 1)


#Check for tampering with sell prices of items
def isPriceCorrect(itemList, sellPrice, itemId):
    for i in range(0, len(itemList)):
        if int(itemList[i]['inventory_item_id']) == int(itemId):
            if int(itemList[i]['sell_price']) == int(sellPrice):
                return True
    
    return False