import random, math, time
from modules import db_manager


database = db_manager.mysql_pool


#Clears all transactional data
database.clearAllTransactionalData()
#database.resetDailyStats()

#Holds the high-use backend data
seasonList = database.getSeasonList()
classes = database.getClasses()
itemTypes = database.getItemTypes()
itemRarities = database.getItemRarities()
weaponPrefixes = database.getWeaponPrefixes()
armorPrefixes = database.getArmorPrefixes()
questMonsters = database.getQuestMonsters()
bountyMonsters = database.getBountyMonsters()

#Used to buff the lower level items since exponentials mean little at low numbers
additionalDamageConstant = 10

#Holds travel information when a player is in travel mode
travellingPlayers = {}

#Defines how many monsters for each page to create on load
questMonstersToSpawn = 4
bountyMonstersToSpawn = 3

#Holds the leaderboard-specific information
leaderboardInfo = {
        'level': {
            'header': 'Highest Level',
            'procedure': 'usp_leaderboard_get_highest_level'   
        },
        'honor': {
            'header': 'Highest Honor',
            'procedure': 'usp_leaderboard_get_highest_honor'   
        },
        'arena': {
            'header': 'Most Arena Wins',
            'procedure': 'usp_leaderboard_get_highest_arena_wins'   
        },
        'quest': {
            'header': 'Most Quests Completed',
            'procedure': 'usp_leaderboard_get_highest_quests_finished'   
        },
        'bounty': {
            'header': 'Most Bounties Completed',
            'procedure': 'usp_leaderboard_get_highest_bounties_finished'   
        },
        'gold': {
            'header': 'Most Gold Collected',
            'procedure': 'usp_leaderboard_get_highest_gold_collected'   
        },
        'items': {
            'header': 'Most Items Collected',
            'procedure': 'usp_leaderboard_get_highest_items_collected'   
        }
    } 

#===============================

#Items

#===============================

def createItem(playerId, playerClass, level):
    #Item Type
    itemTypeId = random.choice(list(itemTypes.keys()))
    isWeapon = itemTypes[itemTypeId]['is_weapon']

    #Item Prefix
    itemPrefixId = getItemPrefix(isWeapon)
    
    #Item Rarity
    itemRarity = getItemRarity()
    rarityMultiplier = itemRarities[itemRarity]['multiplier']

    #Item Stats
    itemStats = getItemStats(level, isWeapon, itemTypeId, itemPrefixId, rarityMultiplier)
    itemStats = trimItemStats(itemStats, itemRarity)

    #Item Damage or Armor
    itemDamage = 0
    itemArmor = 0

    if isWeapon == 0:
        itemArmor = getItemArmor(level, itemTypeId, itemPrefixId, rarityMultiplier)
    else:
        itemDamage = getItemDamage(level, itemTypeId, itemPrefixId, rarityMultiplier)

    #Sell Price
    itemWorth = getSellPrice(level, rarityMultiplier)

    #Check for incorrect class type on item
    if itemTypes[itemTypeId]['stat'] != classes[playerClass]['stat']:
        itemDamage, itemArmor, itemStats = reduceItemStats(itemDamage, itemArmor, itemStats)

    #Create the new item in the database
    database.createNewItem(playerId, level, itemTypeId, itemPrefixId, itemRarity, itemStats, itemDamage, itemArmor, itemWorth)


#Gets a random prefix based on if it's a weapon or armor
def getItemPrefix(isWeapon):
    if isWeapon == 0:
        return random.choice(list(armorPrefixes.keys()))
    else:
        return random.choice(list(weaponPrefixes.keys()))


#Gets the rarity based on the drop chances of each rarity
def getItemRarity():
    roll = random.random()
    dropChance = 0.0

    for rarity in itemRarities:
        dropChance += float(itemRarities[rarity]['drop_chance'])

        if roll < dropChance:
            return rarity


#Creates the stats for an item based on multipliers and level
def getItemStats(level, isWeapon, itemTypeId, itemPrefixId, rarityMultiplier):
    stats = [0,0,0,0,0]
    statMultipliers = ['strength_mult','dexterity_mult','intelligence_mult','constitution_mult','luck_mult']
    statsPerLevel = itemTypes[itemTypeId]['stats_per_level']

    itemPrefix = {}

    if isWeapon == 0:
        itemPrefix = armorPrefixes[itemPrefixId]
    else:
        itemPrefix = weaponPrefixes[itemPrefixId]

    for x in range(0,5):
        stats[x] = float(level * statsPerLevel * rarityMultiplier * itemPrefix[statMultipliers[x]])
        #Apply a little randomization
        stats[x] *= float(random.uniform(0.9,1.1))
        stats[x] = math.floor(stats[x])

    return stats


#Deals with the removal of stats based on the rarity drop chance
def trimItemStats(itemStats, itemRarity):
    backupStats = itemStats.copy()
    removalChance = float(itemRarities[itemRarity]['drop_chance'])+ 0.05
    count = 0

    for x in range(0,len(itemStats)):
        roll = random.random()

        if roll < removalChance:
            itemStats[x] = 0
            count += 1

    #If unlucky enough to remove all stats, give at least one
    if count == 5:
        randomStat = random.randrange(0,5)
        itemStats[randomStat] = backupStats[randomStat]

    return itemStats


#If the players class type does not match the item type stat, reduce stats by a fixed %
def reduceItemStats(itemDamage, itemArmor, itemStats):
    reductionAmount = 0.8

    itemDamage = math.floor(itemDamage * reductionAmount)
    itemArmor = math.floor(itemArmor * reductionAmount)

    for i in range(0, len(itemStats)):
        itemStats[i] = math.floor(itemStats[i] * reductionAmount)

    return [itemDamage, itemArmor, itemStats]


#Creates the armor for an item based on multipliers and level
def getItemArmor(level, itemTypeId, itemPrefixId, rarityMultiplier):
    armorPerLevel = itemTypes[itemTypeId]['armor_per_level']
    armor = level * armorPerLevel
    
    armorMultiplier = armorPrefixes[itemPrefixId]['armor_mult']

    armor = float(armor * rarityMultiplier * armorMultiplier)
    armor *= float(random.uniform(0.9,1.1))
    armor = math.floor(armor)

    return armor


#Creates the damage for an item based on multipliers and level
def getItemDamage(level, itemTypeId, itemPrefixId, itemRarity):
    isTwoHanded = itemTypes[itemTypeId]['is_two_handed']
    damageMultiplier = itemTypes[itemTypeId]['damage_multiplier']

    damage = 0

    if isTwoHanded == 1:
        damage = (level ** 2) + additionalDamageConstant
    else:
        damage = 0.5 * (level ** 2) + additionalDamageConstant

    damage *= float(damageMultiplier)
    damage *= float(random.uniform(0.9,1.1))
    damage = math.floor(damage)

    return damage


#Calculates the sell price of an item based on level
def getSellPrice(level, rarityMultiplier):
    price = float(( ((level ** 3) * rarityMultiplier)  + 300) / 40)
    price *= float(random.uniform(0.9,1.1))
    return math.floor(price)


#Returns a dictionary containing all details of a specified class
def getClassInfo(className):
    return classes[className]


#If a playerId exists inside the dictionary, return the contained dictionary - else return an empty dictionary
def getPlayerTravelInfo(playerId):
    if playerId in travellingPlayers:
        return travellingPlayers[playerId]
    return {}


#Remove the player from the travel info dictionary
def removePlayerTravelInfo(playerId):
    if playerId in travellingPlayers:
        travellingPlayers.pop(playerId, None)


#After a player completes an event, process the rewards/stamina usage
def completePlayerEvent(playerId, playerWon, playerInfo, monsterInfo, travelInfo):
    gold = 0
    xp = 0
    dungeonTier = None

    if playerWon:
        gold = monsterInfo['gold']
        xp = monsterInfo['xp']
        
        if travelInfo['droppedLoot'] == 1:
            createItem(playerId, playerInfo['class_name'], playerInfo['level'])

    if travelInfo['typeOfEvent'] == 'quest':
        stamina = monsterInfo['stamina']
    elif travelInfo['typeOfEvent'] == 'bounty' or travelInfo['typeOfEvent'] == 'dungeon':
        if travelInfo['typeOfEvent'] == 'dungeon':
            dungeonTier = travelInfo['dungeon_tier']
        stamina = 0

    return database.givePlayerQuestRewards(playerId, stamina, gold, xp, travelInfo['typeOfEvent'], dungeonTier)


#Inserts a new dictionary inside of the travelling dictionary based on the event the player chose to do
def addQuestToTravelInfo(playerId, monsterId):
    questMonsters = database.getPlayerQuestMonsters(playerId)

    #If the player doesn't have active quests return
    if questMonsters == []:
        return

    monster = None

    for i in range(0, len(questMonsters)):
        if int(questMonsters[i]['quest_monster_id']) == int(monsterId):
            monster = questMonsters[i]
            break

    #If the monsterId was changed by the player then there won't be a monster and return
    if monster == None:
        return

    #Calculate the unix time so that it can be accurate when the travel page loads
    timeNow = int(time.time())
    endTime = timeNow + int(monster['travel_time'])
    
    #Add a new entry into the travelling dictionary
    travellingPlayers[playerId] = {}
    travellingPlayers[playerId] = monster
    travellingPlayers[playerId]['travel_time'] = endTime
    travellingPlayers[playerId]['typeOfEvent'] = 'quest'

    #print(travellingPlayers[playerId])


#Inserts a new dictionary inside of the travelling dictionary based on the event the player chose to do
def addBountyToTravelInfo(playerId, monsterId, multiplier):
    bountyMonsters = database.getPlayerBountyMonsters(playerId)

    #If the player doesn't have active bounties return
    if bountyMonsters == []:
        return

    monster = None

    for i in range(0, len(bountyMonsters)):
        if int(bountyMonsters[i]['bounty_monster_id']) == int(monsterId):
            monster = bountyMonsters[i]
            break

    #If the monsterId was changed by the player then there won't be a monster and return
    if monster == None:
        return

    #Calculate the unix time so that it can be accurate when the travel page loads
    timeNow = int(time.time())
    endTime = timeNow + int(monster['travel_time'])
    
    #Add a new entry into the travelling dictionary
    travellingPlayers[playerId] = {}
    travellingPlayers[playerId] = monster
    travellingPlayers[playerId]['multiplier'] = multiplier
    travellingPlayers[playerId]['travel_time'] = endTime
    travellingPlayers[playerId]['typeOfEvent'] = 'bounty'

    #print(travellingPlayers[playerId])


#Inserts a new dictionary inside of the travelling dictionary based on the event the player chose to do
def addArenaFightToTravelInfo(player, playerId, opponentId):
    opponents = database.getPlayerArenaOpponents(playerId)

    #If the player doesn't have active opponents return
    if opponents == []:
        return

    opponent = None

    for i in range(0, len(opponents)):
        if int(opponents[i]['player_id']) == int(opponentId):
            opponent = opponents[i]
            break

    #If the opponentId was changed by the player then there won't be a opponent and return
    if opponent == None:
        return
 
    #Add a new entry into the travelling dictionary
    travellingPlayers[playerId] = {}
    travellingPlayers[playerId] = opponent
    travellingPlayers[playerId]['typeOfEvent'] = 'arena'

    if player['honor'] > opponent['honor']:
        honor = 9
    else:
        honor = 13

    travellingPlayers[playerId]['honor'] = honor


#Inserts a new dictionary inside of the travelling dictionary based on the event the player chose to do
def addDungeonToTravelInfo(playerId, dungeonTier):
    monster = database.getDungeonMonsterInfo(playerId, dungeonTier)

    #If the dungeon monster doesn't exist return
    if monster == []:
        return
 
    #Add a new entry into the travelling dictionary
    travellingPlayers[playerId] = {}
    travellingPlayers[playerId] = monster
    travellingPlayers[playerId]['typeOfEvent'] = 'dungeon'


def getTimeLeftFromEpochTime(epochTimestamp):
    timeNow = int(time.time())
    return int(epochTimestamp) - timeNow


#===============================

#Quests

#===============================

def createRandomQuestMonsters(playerId, playerStats):
    pickedMonsters = []
    playerLevel = playerStats['level']
    
    #Get average stat level
    averageStat = getAverageStatLevel(playerStats)

    for i in range(0,questMonstersToSpawn):
        #Get a random monster from the quest monster dictionary
        monsterId = random.choice(list(questMonsters.keys()))

        #Ensure the monsters are all unique
        while monsterId in pickedMonsters:
            monsterId = random.choice(list(questMonsters.keys()))
        pickedMonsters.append(monsterId)

        #Get the xp based on player level with randomness
        expForLevel = math.floor((playerLevel ** 2) * playerLevel ** 1.3) + 50
        questXp = math.floor((playerLevel ** 2)) + 10

        monsterExp = math.floor(questXp * float(random.uniform(0.75,1.25)))
   
        #Get the gold based on player level with randomness
        gold = (playerLevel ** 3) + 300
        questsNeeded = math.floor(expForLevel / questXp)
        goldPerQuest = math.floor(gold / questsNeeded)

        monsterGold = math.floor(goldPerQuest * float(random.uniform(0.75,1.25)))

        #Get a random stamina cost
        monsterStamina = random.randint(3,8)

        #Get a random travel time
        monsterTime = random.randint(30,300)

        #Get random stats based on the players average stat
        stats = []
        statMultipliers = []
        for i in range(0,5):
            if playerLevel <= 5:
                multiplier = float(random.uniform(0.2,0.4))
            else:
                multiplier = float(random.uniform(0.6,0.85))

            stats.append(math.floor(averageStat * multiplier))
            statMultipliers.append(multiplier)

        #If the player is under level 3 - make the monsters really easy as the players stats are too low to make it one sided
        if playerLevel < 3:
            for i in range(0,5):
                stats[i] = 1

        #Give better stats based on class
        monsterClass = questMonsters[monsterId]['class_name']
        classStat = classes[monsterClass]['stat']

        applyMonsterStatBoosters(stats, classStat)

        #Apply any blessings of the player
        blessing = database.getActiveBlessing(playerId)

        if blessing == 'gold':
            monsterGold = math.floor(monsterGold * 1.5)
        elif blessing == 'xp':
            monsterExp = math.floor(monsterExp * 1.5)

        #Add it to the database
        database.createQuestMonsterForPlayer(playerId, monsterId, monsterExp, monsterGold, monsterStamina, monsterTime, stats[0], stats[1], stats[2], stats[3], stats[4], statMultipliers[0], statMultipliers[1], statMultipliers[2], statMultipliers[3], statMultipliers[4])


#===============================

#Bounties

#===============================

def createRandomBountyMonsters(playerId, playerStats):
    pickedMonsters = []
    playerLevel = playerStats['level']
    
    #Get average stat level
    averageStat = getAverageStatLevel(playerStats)

    for i in range(0,bountyMonstersToSpawn):
        #Get a random monster from the quest monster dictionary
        monsterId = random.choice(list(bountyMonsters.keys()))

        #Ensure the monsters are all unique
        while monsterId in pickedMonsters:
            monsterId = random.choice(list(bountyMonsters.keys()))
        pickedMonsters.append(monsterId)

        #Get the xp based on player level with randomness
        expForLevel = math.floor((playerLevel ** 2) * playerLevel ** 1.3) + 50
        questXp = math.floor((playerLevel ** 2) * playerLevel ** 0.25) + 10

        monsterExp = math.floor(questXp * float(random.uniform(0.95,1.05)))

        #Get the gold based on player level with randomness
        gold = (playerLevel ** 3) + 300
        questsNeeded = math.floor(expForLevel / questXp)
        goldPerQuest = math.floor(gold / questsNeeded)

        monsterGold = math.floor(goldPerQuest * float(random.uniform(0.95,1.05)))

        #Get monster drop chance
        monsterDropChance = 0.75

        #Get a random travel time
        monsterTime = random.randint(30,300)

        #Get random stats based on the players average stat
        stats = []
        statMultipliers = []
        for j in range(0,5):
            multiplier = float(random.uniform(0.7,0.8))

            stats.append(math.floor(averageStat * multiplier))
            statMultipliers.append(multiplier)

        #Give better stats based on class
        monsterClass = bountyMonsters[monsterId]['class_name']
        classStat = classes[monsterClass]['stat']

        applyMonsterStatBoosters(stats, classStat)

        #Add the xp/gold/drop chance bonuses based on which one it is
        if i == 0:
            monsterGold = math.floor(monsterGold * 1.5)
        elif i == 1:
            monsterExp = math.floor(monsterExp * 1.5)
        else:
            monsterDropChance = 1.0

        #Apply any blessings of the player
        blessing = database.getActiveBlessing(playerId)

        if blessing == 'gold':
            monsterGold = math.floor(monsterGold * 1.5)
        elif blessing == 'xp':
            monsterExp = math.floor(monsterExp * 1.5)
        elif blessing == 'drops':
            monsterDropChance += 0.2

        #Add it to the database
        database.createBountyMonsterForPlayer(playerId, monsterId, monsterExp, monsterGold, monsterDropChance, monsterTime, stats[0], stats[1], stats[2], stats[3], stats[4], statMultipliers[0], statMultipliers[1], statMultipliers[2], statMultipliers[3], statMultipliers[4])


#Creates a new monster for the battle which uses current stats (incase the player equipped new items since the monsters were generated - or leveled up)
def createMonsterForBattle(playerStats, playerId, travelInfo):
    monsterType = travelInfo['typeOfEvent']
    
    if monsterType == 'quest':
        monsterId = travelInfo['quest_monster_id']
    elif monsterType == 'bounty':
        monsterId = travelInfo['bounty_monster_id']

    monster = database.getMonsterStats(playerId, monsterId, monsterType)
    stat = classes[monster['class_name']]['stat']

    #Get average stat level
    averageStat = getAverageStatLevel(playerStats)
    
    #Get the monster stats based on multipliers and boosters
    stats = []
    statNames = ['strength', 'dexterity', 'intelligence', 'constitution', 'luck']

    for i in range(0, len(statNames)):
        if monsterType == 'quest':
            monster[statNames[i]] = math.floor(float(averageStat) * float(monster[statNames[i] + '_mult']))
        elif monsterType == 'bounty':
            monster[statNames[i]] = math.floor(float(averageStat) * float(monster[statNames[i] + '_mult']) * float((1 + (float(travelInfo['multiplier']) / 100))))

        stats.append(monster[statNames[i]])

    stats = applyMonsterStatBoosters(stats, stat)

    for i in range(0, len(statNames)):
        monster[statNames[i]] = stats[i]

    playerLevel = playerStats['level']

    monster['level'] = playerLevel

    if playerLevel <= 2:
        monster['strength'] = 1
        monster['dexterity'] = 1
        monster['intelligence'] = 1
        monster['constitution'] = 1
        monster['luck'] = 1
        monster['damage'] = 0
        monster['armor'] = 0
    elif playerLevel <= 5:
        monster['damage'] = math.floor(float(playerStats['damage']) * float(random.uniform(0.3,0.5)))
        monster['armor'] = math.floor(float(playerStats['armor']) * float(random.uniform(0.3,0.5)))
    else:
        monster['damage'] = math.floor(float(playerStats['damage']) * float(random.uniform(0.7,0.8)))
        monster['armor'] = math.floor(float(playerStats['armor']) * float(random.uniform(0.7,0.8)))

    return monster


#Returns the average level based on the players stats 
def getAverageStatLevel(playerStats):
    statNames = ['strength', 'dexterity', 'intelligence', 'constitution', 'luck']
    total = 0

    for i in range(0, len(statNames)):
        total += int(playerStats[statNames[i]])
        total += int(playerStats['equip_' + statNames[i]])

    return math.floor(total / 5)


#Fixes player stats as base stats and equipment stats are separate
def combinePlayerStats(playerStats):
    statNames = ['strength', 'dexterity', 'intelligence', 'constitution', 'luck']

    for i in range(0, len(statNames)):
        playerStats[statNames[i]] = int(playerStats[statNames[i]]) + int(playerStats['equip_' + statNames[i]])

    return playerStats


#Applies a normalized booster for stats of a monster based on a class - so they don't look so random and stand a chance
def applyMonsterStatBoosters(stats, stat):
    if stat == 'str':
        stats[0] = math.floor(stats[0] * 1.4)
        stats[3] = math.floor(stats[3] * 1.35)
        stats[4] = math.floor(stats[4] * 1.15)
    elif stat == 'dex':
        stats[1] = math.floor(stats[0] * 1.5)
        stats[3] = math.floor(stats[0] * 1.25)
        stats[4] = math.floor(stats[4] * 1.15)
    else:
        stats[2] = math.floor(stats[0] * 1.6)
        stats[3] = math.floor(stats[0] * 1.15)
        stats[4] = math.floor(stats[0] * 1.5)
    return stats


#Returns the data needed when a leaderboard is called (header and board data)
def getLeaderboardData(boardType, season):
    header = leaderboardInfo[boardType]['header']
    procedure = leaderboardInfo[boardType]['procedure']

    data = database.getLeaderboardData(procedure, season)

    return [header, data]


#===============================

#Debug/Testing Functions

#===============================


#Simply for debugging purposes for testing new items
def debugCreateItems(playerId, playerClass, itemCount, levelMin, levelMax):
    database.debugRemoveAllPlayerItems(playerId)

    for i in range(0,itemCount):
        level = random.randint(levelMin, levelMax)
        createItem(playerId, playerClass, level)