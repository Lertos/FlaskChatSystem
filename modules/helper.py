import random, math, time
from modules import db_manager


database = db_manager.MySQLPool()

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

    #Debugging
    debug = 0

    if debug == 1:
        print('\n=TYPE ' + str(itemTypeId) + ' ' + str(itemTypes[itemTypeId]['item_type_name']) + ' ' + str(itemTypes[itemTypeId]['stat']))

        if isWeapon == 0:
            print('=PREFIX ' + str(itemPrefixId) + ' ' + str(armorPrefixes[itemPrefixId]['prefix']))
            print('=ARMOR ' + str(itemArmor))
        else:
            print('=PREFIX ' + str(itemPrefixId) + ' ' + str(weaponPrefixes[itemPrefixId]['prefix']))
            print('=DAMAGE ' + str(itemDamage))

        print('=LEVEL ' + str(level))
        print('=STATS ' + itemRarity + ' ' + str(itemStats))
        print('=STATS-TRIMMED ' + itemRarity + ' ' + str(itemStats))


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

    #Find average stat amount
    total = 0
    for key in playerStats:
        if not (key == 'damage' or key == 'armor'):
            total += int(playerStats[key])

    averageStat = math.floor(total / 5)

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
        for i in range(0,5):
            stats.append(math.floor(averageStat * float(random.uniform(0.60,1))))

        #Give better stats based on class
        monsterClass = questMonsters[monsterId]['class_name']
        classStat = classes[monsterClass]['stat']

        if classStat == 'str':
            stats[0] = math.floor(stats[0] * 1.4)
            stats[3] = math.floor(stats[3] * 1.35)
            stats[4] = math.floor(stats[4] * 1.15)
        elif classStat == 'dex':
            stats[1] = math.floor(stats[0] * 1.5)
            stats[3] = math.floor(stats[0] * 1.25)
            stats[4] = math.floor(stats[4] * 1.15)
        else:
            stats[2] = math.floor(stats[0] * 1.6)
            stats[3] = math.floor(stats[0] * 1.15)
            stats[4] = math.floor(stats[0] * 1.5)

        #Add it to the database
        database.createQuestMonsterForPlayer(playerId, monsterId, monsterExp, monsterGold, monsterStamina, monsterTime, stats[0], stats[1], stats[2], stats[3], stats[4])


#===============================

#Combat

#===============================

def setupFight(entity1, entity2):

    #Calculate and insert each others resistances based on the other entities stats/level
    calculateResistances(entity1, entity2)
    calculateResistances(entity2, entity1)

    #Process secondary stats
    calculateSecondaryStats(entity1)
    calculateSecondaryStats(entity2)

    #Take care of class-specific bonuses
    classSpecificBonuses(entity1, entity2)
    classSpecificBonuses(entity2, entity1)

    #Decide who goes first - 50/50
    goesFirst = math.random()

    if goesFirst > 0.5:
        startFight(entity1, entity2)
    else:
        startFight(entity2, entity1)


#Begins the fight between the two entities - having all the final stats ready
def startFight(entity1, entity2):

    #Initialize base turn damage
    entity1['turnDamage'] = 1.0
    entity2['turnDamage'] = 1.0

    #Controls who attacks each loop iteration
    decider = 0
    attacker = None
    defender = None

    #Tracks the turn of a rogue since they essentially take two turns
    hasAttackedTwice = False

    while entity1['health'] > 0 and entity2['health'] > 0:
        if decider == 0:
            attacker = entity1
            defender = entity2
        else:
            attacker = entity2
            defender = entity1

        #Reset critical damage every turn before damage calculation
        entity1['critDamage'] = 0
        entity2['critDamage'] = 0

        #Check for evasion and blocking
        doesDefenderEvadeOrBlock = False
        defenderClass = defender['class_name']

        if defenderClass == 'Scout' or defenderClass == 'Rogue' or defenderClass == 'Assassin' or defenderClass == 'Warrior':
            doesDefenderEvadeOrBlock = checkEvadeOrBlock(attacker, defender)

        #If there was no evasion or block
        if not doesDefenderEvadeOrBlock:

            #Magic knight reduces armor reduction by 5%
            if attacker['class_name'] == 'Magic Knight':
                defender['armorReduction'] -= 5.0
                print('[CLASS] ' + attacker['name'] + ' has reduced the opponents armor by 5%. NOW: ' + defender['armorReduction'])
            
            #Make sure the armor reduction isn't negative
            if defender['armorReduction'] < 0:
                defender['armorReduction'] = 0

            #Check for critical hits
            isHitCritical = checkCriticalHit(attacker, defender)

            if isHitCritical:
                print('[CRIT] ' + attacker['name'] + ' is going to CRITICALLY hit!')
                processCriticalHit(attacker, defender)

            #Total up the damage including ( [baseDamage + critDamage] * turnDamage )
            baseDamage = attacker['damage']

            #Berserker takes 2x damage from mages
            if classes[attacker['class_name']]['stat'] == 'int' and defender['class_name'] == 'Berserker':
                baseDamage *= 2
                print('[CLASS] ' + defender['name'] + ' just took DOUBLE DMG from a magical attack!')

            attackerDamage = math.floor((baseDamage + attacker['critDamage']) * attacker['turnDamage'])
            damageAfterArmor = math.floor(attackerDamage * (1 - defender['armorReduction'] / 100))
            print('attackerDamage: ' + attackerDamage + " damageAfterArmor: " + damageAfterArmor)
            damageBlocked = attackerDamage - damageAfterArmor

            defender['health'] -= damageAfterArmor
            print('[HIT] ' + attacker['name'] + ' hits for ' + damageAfterArmor + ' damage (' + damageBlocked + ' was blocked) || ' + defender['name'] + ' has ' + defender['health'] + ' health')

            if attacker['class_name'] == 'Dark Mage':
                if math.random() > 0.5:
                    attacker['health'] += math.floor(baseDamage / 3)
                    print('[CLASS] ' + attacker['name'] + ' just STOLE LIFE equal to 1/3 of their base damage!')
                    
                    #Make sure health doesn't go over max
                    if attacker['health'] > attacker['maxHealth']:
                        attacker['health'] = attacker['maxHealth']

            #Check for resurrection
            checkIfRessurected(defender)

        #Change the turn over to the other player
        if decider == 0:
            decider = 1
        else:
            decider = 0
        
        #Rogues attack twice - so change the decider back
        if attacker['class_name'] == 'Rogue':
            if hasAttackedTwice == False:
                if decider == 0:
                    decider = 1
                else:
                    decider = 0

                attacker['turnDamage'] -= 0.2
                hasAttackedTwice = True

            #Set the counter back for the next time its the rogue's turn
            else:
                hasAttackedTwice = False
                print('[CLASS] ' + attacker['name'] + ' just attacked twice!')

        #Berserkers have a 50% chance to attack again
        if attacker['class_name'] == 'Berserker':
            if math.random() >= 0.5:
                if decider == 0:
                    decider = 1
                else:
                    decider = 0

                attacker['turnDamage'] -= 0.2
                print('[CLASS] ' + attacker['name'] + ' IS ATTACKING AGAIN!')

        #If attacker is a fire mage, increase damage by 35% not 20%
        if attacker['class_name'] == 'fireMage':
            attacker['turnDmg'] += 0.35
        else:
            attacker['turnDmg'] += 0.2

    if entity1['health'] <= 0:
        return entity1
    else:
        return entity2


#Calculates all of the entities secondary stats based on base stats
def calculateSecondaryStats(entity):
    calculateArmorReduction(entity)
    calculateHealth(entity)
    calculateCritChance(entity)


#Calculates armor reduction based on level and total armor
def calculateArmorReduction(entity):
    classMaxArmorReduction = classes[entity['class_name']] * 100
            
    armor = entity['armor']
    armorReduction = math.floor(armor / entity['level'])

    if armorReduction > classMaxArmorReduction:
        armorReduction = classMaxArmorReduction

    entity['armorReduction'] = armorReduction


#Calculates health based on level and constitution
def calculateHealth(entity):
    constitution = entity['constitution']
    level = entity['level']
    healthModifier = classes[entity['class_name']]['health_modifier']
    health = 0

    if level <= 5:
        health = math.floor(healthModifier * (level ** 2) * 4 * (constitution/20) + 60)
    else:
        health = math.floor(healthModifier * (level ** 2) * 4 * (constitution/30) + 60)

    entity['health'] = health
    entity['maxHealth'] = health


#Calculates critical chance based on level and luck
def calculateCritChance(entity):
    classMaxCritChance = classes[entity['class_name']] * 100
    
    luck = entity['luck']
    critChance = math.floor(luck / entity['level'])

    if critChance > classMaxCritChance:
        critChance = classMaxCritChance

    entity['critChance'] = critChance


#Adds/removes stats based on class-specific traits/abilities
def classSpecificBonuses(entity1, entity2):
    #Fencer immediately removes 15% armor reduction
    if entity1['class_name'] == 'Fencer':
        entity2['armorReduction'] -= 15.0

    #Mages ignore armor
    if classes[entity1['class_name']]['stat'] == 'int' and entity2['class_name'] != 'Magic Knight':
        entity2['armorReduction'] = 0

    #Make sure armor reduction isn't negative
    if entity2['armorReduction'] < 0:
        entity2['armorReduction'] = 0


#Calculates the resistances of of the entity by using the opponents stats
def calculateResistances(entity1, entity2):
    entity1['strengthResistance'] = math.floor(entity2['strength'] / 2)
    entity1['dexterityResistance'] = math.floor(entity2['dexterity'] / 2)
    entity1['intelligenceResistance'] = math.floor(entity2['intelligence'] / 2)


#Checks if the defender can block/evade - if so check if it is successful
def checkEvadeOrBlock(attacker, defender):
    evadeBlockChance = 0.25

	#Cannot evade magical attacks unless the defender is a scout
    if classes[attacker['class_name']]['stat'] == 'int' and defender['class_name'] != 'Scout':
        return False
    else:
        #Scouts can evade magical attacks, but only with a 15% chance
        if defender['class_name'] == 'Scout':
            evadeBlockChance -= 0.10
			
        if evadeBlockChance > math.random():
            #print('[CLASS] ' + defender['name'] + ' dodged/blocked!')
            return True
    return False


#Checks if the attacker critically strikes
def checkCriticalHit(attacker, defender):
    critChance = attacker['critChance']
    random = math.random() * 100
    
    #Frost mages drop the critical chance of foes
    if defender['class_name'] == 'Frost Mage':
        critChance -= 20
        #print('[CLASS] ' + defender['name'] + ' just DROPPED foes CRIT CHANCE by 20!')

    if critChance > random:
        return True
    else:
        return False


#If an entity critically strikes, process the critical hit for their class
def processCriticalHit(attacker, defender):
    baseDamage = attacker['damage']
		
    if attacker['critChance'] > math.random():
        if attacker['class_name'] == 'Assassin':
            attacker['critDamage'] = baseDamage * 2
        elif attacker['class_name'] == 'Blood Mage':
            attacker['health'] += math.floor(baseDamage / 2)
            #print('[CLASS] ' + attacker['name'] + ' just HEALED for 50% of base damage!')

            if classes[defender['class_name']]['stat'] == 'int':
                attacker['health'] += math.floor(baseDamage / 2)
                #print('[CLASS] ' + attacker['name'] + ' just HEALED for an additional 50% of base damage due to MAGE!')

            #Make sure health doesn't go over max
            if attacker['health'] > attacker['maxHealth']:
                attacker['health'] = attacker['maxHealth']
        else:
            attacker['critDamage'] = baseDamage


#Checks if the defender is a demon hunter - is so check if resurrection is successful
def checkIfRessurected(defender):
    if defender['health'] <= 0 and defender['class_name'] == 'Demon Hunter':
        if math.random() < 0.35:
            defender['health'] = defender['maxHealth']
            #print('[CLASS] ' + defender['name'] + ' just RESURRECTED! Spooky!')

#===============================

#Validation

#===============================



#===============================

#Debug/Testing Functions

#===============================


def debugServerDictionaries():
    '''
    debugSetupDictionary('Classes', classes)
    debugSetupDictionary('Item Types', itemTypes)
    debugSetupDictionary('Item Rarities', itemRarities)
    debugSetupDictionary('Item Prefixes', itemPrefixes)
    debugSetupDictionary('Quest Monsters', questMonsters)
    debugSetupDictionary('Bounty Monsters', bountyMonsters)
    '''
    '''
    createItem(1, 40)
    createItem(1, 10)
    createItem(1, 20)
    createItem(1, 30)
    createItem(1, 40)
    createItem(1, 50)
    createItem(1, 60)
    createItem(1, 70)
    createItem(1, 80)
    createItem(1, 90)
    createItem(1, 100)
    '''


#Simply for debugging purposes for testing new items
def debugCreateItems(playerId, playerClass, itemCount, levelMin, levelMax):
    database.debugRemoveAllPlayerItems(playerId)

    for i in range(0,itemCount):
        level = random.randint(levelMin, levelMax)
        createItem(playerId, playerClass, level)


#Prints out the setup dictionaries in a readable format for debugging
def debugSetupDictionary(header, givenDict):
    print('\n\n == ' + header + ' == \n\n')

    for row in givenDict:
        print(str(row) + ' ' + str(givenDict[row]))

    print('\n\n')