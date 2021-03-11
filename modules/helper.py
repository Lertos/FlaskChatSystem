import random, math
from modules import db_manager


classes = db_manager.getClasses()
itemTypes = db_manager.getItemTypes()
itemRarities = db_manager.getItemRarities()
itemPrefixes = db_manager.getItemPrefixes()
questMonsters = db_manager.getQuestMonsters()
bountyMonsters = db_manager.getBountyMonsters()



def debugServerDictionaries():
    '''
    debugSetupDictionary('Classes', classes)
    debugSetupDictionary('Item Types', itemTypes)
    debugSetupDictionary('Item Rarities', itemRarities)
    debugSetupDictionary('Item Prefixes', itemPrefixes)
    debugSetupDictionary('Quest Monsters', questMonsters)
    debugSetupDictionary('Bounty Monsters', bountyMonsters)
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
    itemTypeId = random.choice(list(itemTypes.keys()))
    print('\n=TYPE ' + str(itemTypeId) + ' ' + str(itemTypes[itemTypeId]['stat']) + ' ' + str(itemTypes[itemTypeId]['is_weapon']))

    itemPrefixId = getItemPrefix(itemTypeId)
    print('=PREFIX ' + str(itemPrefixId) + ' ' + str(itemPrefixes[itemPrefixId]['stat']) + ' ' + str(itemPrefixes[itemPrefixId]['is_weapon']))

    itemRarity = getItemRarity()

    itemStats = getItemStats(level, itemTypeId, itemPrefixId, itemRarity)
    print('=STATS ' + itemRarity + ' ' + str(level) + ' ' + str(itemStats))
    itemStats = trimItemStats(itemStats, itemRarity)
    print('=STATS-TRIMMED ' + itemRarity + ' ' + str(level) + ' ' + str(itemStats))

    #damage

    #armor

    #sell worth


def getItemPrefix(itemTypeId):
    trimmedDict = {}
    stat = itemTypes[itemTypeId]['stat']
    isWeapon = itemTypes[itemTypeId]['is_weapon']

    for prefix in itemPrefixes:
        if itemPrefixes[prefix]['stat'] == stat and itemPrefixes[prefix]['is_weapon'] == isWeapon:
            trimmedDict[prefix] = itemPrefixes[prefix]

    return random.choice(list(trimmedDict.keys()))


def getItemRarity():
    roll = random.random()
    dropChance = 0.0

    for rarity in itemRarities:
        dropChance += float(itemRarities[rarity]['drop_chance'])

        if roll < dropChance:
            return rarity


def getItemStats(level, itemTypeId, itemPrefixId, itemRarity):
    stats = [0,0,0,0,0]
    statMultipliers = ['strength_mult','dexterity_mult','intelligence_mult','constitution_mult','luck_mult']
    
    statsPerLevel = itemTypes[itemTypeId]['stats_per_level']
    rarityMultiplier = itemRarities[itemRarity]['multiplier']

    for x in range(0,5):
        stats[x] = float(level * statsPerLevel * rarityMultiplier * itemPrefixes[itemPrefixId][statMultipliers[x]])
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