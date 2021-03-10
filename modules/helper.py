import random, math
from modules import db_manager


globalClasses = db_manager.getClasses()
globalItemTypes = db_manager.getItemTypes()
globalItemRarities = db_manager.getItemRarities()
globalItemPrefixes = db_manager.getItemPrefixes()
globalQuestMonsters = db_manager.getQuestMonsters()
globalBountyMonsters = db_manager.getBountyMonsters()



def debugServerDictionaries():
    '''
    debugSetupDictionary('Classes', globalClasses)
    debugSetupDictionary('Item Types', globalItemTypes)
    debugSetupDictionary('Item Rarities', globalItemRarities)
    debugSetupDictionary('Item Prefixes', globalItemPrefixes)
    debugSetupDictionary('Quest Monsters', globalQuestMonsters)
    debugSetupDictionary('Bounty Monsters', globalBountyMonsters)
    '''
    createItem(1)
    createItem(10)
    createItem(20)
    createItem(30)
    createItem(40)
    createItem(50)


#Prints out the setup dictionaries in a readable format for debugging
def debugSetupDictionary(header, givenDict):
    print('\n\n == ' + header + ' == \n\n')

    for row in givenDict:
        print(str(row) + ' ' + str(givenDict[row]))

    print('\n\n')


def createItem(level):
    itemTypeId = random.choice(list(globalItemTypes.keys()))
    #print(str(itemTypeId))
    itemPrefixId = getItemPrefix(itemTypeId)
    #print(str(itemTypeId) + " " + str(itemPrefixId))
    itemRarity = getItemRarity()
    itemStats = getItemStats(level, itemTypeId, itemPrefixId, itemRarity)
    print(itemRarity + ' ' + str(level) + ' ' + str(itemStats))
    itemStats = trimItemStats(itemStats, itemRarity)
    print(itemRarity + ' ' + str(level) + ' ' + str(itemStats))


def getItemPrefix(itemTypeId):
    trimmedDict = {}

    for prefix in globalItemPrefixes:
        if globalItemPrefixes[prefix]['item_type_id'] == itemTypeId:
            trimmedDict[prefix] = globalItemPrefixes[prefix]

    return random.choice(list(trimmedDict.keys()))


def getItemRarity():
    roll = random.random()
    dropChance = 0.0

    for rarity in globalItemRarities:
        dropChance += float(globalItemRarities[rarity]['drop_chance'])

        if roll < dropChance:
            return rarity


def getItemStats(level, itemTypeId, itemPrefixId, itemRarity):
    stats = [0,0,0,0,0]
    statMultipliers = ['strength_multiplier','dexterity_multiplier','intelligence_multiplier','constitution_multiplier','luck_multiplier']
    
    statsPerLevel = globalItemTypes[itemTypeId]['stats_per_level']
    rarityMultiplier = globalItemRarities[itemRarity]['multiplier']

    for x in range(0,5):
        stats[x] = float(level * statsPerLevel * rarityMultiplier * globalItemPrefixes[itemPrefixId][statMultipliers[x]])
        #Apply a little randomization
        stats[x] *= float(random.uniform(0.9,1.1))
        stats[x] = math.floor(stats[x])

    return stats


#Deals with the removal of stats based on the rarity drop chance
def trimItemStats(itemStats, itemRarity):
    backupStats = itemStats.copy()
    removalChance = float(globalItemRarities[itemRarity]['drop_chance'])+ 0.05
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