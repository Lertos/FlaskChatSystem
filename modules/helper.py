import random, math, time
from modules import db_manager


database = db_manager.MySQLPool()

#Clears all transactional data
database.clearAllTransactionalData()

#Holds the high-use backend data
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
    price = float(( ((level ** 3) * rarityMultiplier)  + 300) / 50)
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
        travellingPlayers.pop('playerId', None)


#After a player completes an event, process the rewards/stamina usage
def completePlayerEvent(playerId, playerWon, monsterInfo):
    stamina = monsterInfo['stamina']
    gold = 0
    xp = 0

    if playerWon:
        gold = monsterInfo['gold']
        xp = monsterInfo['xp']

    return database.givePlayerQuestRewards(playerId, stamina, gold, xp)


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


def getTimeLeftFromEpochTime(epochTimestamp):
    timeNow = int(time.time())
    return int(epochTimestamp) - timeNow


#===============================

#Quests

#===============================

def createRandomQuestMonsters(playerId, playerLevel, playerStats):
    pickedMonsters = []

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
        #monsterTime = random.randint(30,300)
        monsterTime = 2

        #Get random stats based on the players average stat
        stats = []
        statMultipliers = []
        for i in range(0,5):
            multiplier = float(random.uniform(0.60,1))
            stats.append(math.floor(averageStat * multiplier))
            statMultipliers.append(multiplier)

        #Give better stats based on class
        monsterClass = questMonsters[monsterId]['class_name']
        classStat = classes[monsterClass]['stat']

        applyMonsterStatBoosters(stats, classStat)

        #Add it to the database
        database.createQuestMonsterForPlayer(playerId, monsterId, monsterExp, monsterGold, monsterStamina, monsterTime, stats[0], stats[1], stats[2], stats[3], stats[4], statMultipliers[0], statMultipliers[1], statMultipliers[2], statMultipliers[3], statMultipliers[4])


def createMonsterForBattle(playerStats, playerId, monsterId, monsterType):
    monster = database.getMonsterStats(playerId, monsterId, monsterType)
    stat = classes[monster['class_name']]

    #Get average stat level
    averageStat = getAverageStatLevel(playerStats)
    
    #Get the monster stats based on multipliers and boosters
    stats = []
    statNames = ['strength', 'dexterity', 'intelligence', 'constitution', 'luck']

    for i in range(0, len(statNames)):
        monster[statNames[i]] = math.floor(averageStat * monster[statNames[i] + '_mult'])
        stats.append(monster[statNames[i]])

    stats = applyMonsterStatBoosters(stats, stat)

    for i in range(0, len(statNames)):
        monster[statNames[i]] = stats[i]

    monster['level'] = playerStats['level']
    monster['damage'] = math.floor(float(playerStats['damage']) * float(random.uniform(0.8,1.05)))
    monster['armor'] = math.floor(float(playerStats['armor']) * float(random.uniform(0.8,1.05)))

    return monster


#Returns the average level based on the players stats 
def getAverageStatLevel(playerStats):
    total = 0

    for key in playerStats:
        if not (key == 'damage' or key == 'armor' or key == 'name' or key == 'class_name' or key == 'file_name' or key == 'level'):
            total += int(playerStats[key])

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


#===============================

#Debug/Testing Functions

#===============================


#Simply for debugging purposes for testing new items
def debugCreateItems(playerId, playerClass, itemCount, levelMin, levelMax):
    database.debugRemoveAllPlayerItems(playerId)

    for i in range(0,itemCount):
        level = random.randint(levelMin, levelMax)
        createItem(playerId, playerClass, level)