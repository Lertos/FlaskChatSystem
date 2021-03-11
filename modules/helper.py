import random, math
from modules import db_manager


classes = db_manager.getClasses()
itemTypes = db_manager.getItemTypes()
itemRarities = db_manager.getItemRarities()
weaponPrefixes = db_manager.getWeaponPrefixes()
armorPrefixes = db_manager.getArmorPrefixes()
questMonsters = db_manager.getQuestMonsters()
bountyMonsters = db_manager.getBountyMonsters()

#Used to buff the lower level items since exponentials mean little at low numbers
additionalDamageConstant = 10


#===============================

#Setup

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
    createItem(1, 40)
    '''
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


#Prints out the setup dictionaries in a readable format for debugging
def debugSetupDictionary(header, givenDict):
    print('\n\n == ' + header + ' == \n\n')

    for row in givenDict:
        print(str(row) + ' ' + str(givenDict[row]))

    print('\n\n')


#===============================

#Items

#===============================

def createItem(playerId, level):
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

    #TODO - sell worth 
    itemWorth = 10

    #Create the new item in the database
    db_manager.createNewItem(playerId, level, itemTypeId, itemPrefixId, itemRarity, itemStats, itemDamage, itemArmor, itemWorth)

    debug = 1

    #Debugging
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


#===============================

#Validation

#===============================
