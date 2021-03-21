import random, math, time
from modules import helper


#Battle log tags
battleLogTags = {
    'HEALTH': '{name} has {amount} health',
    'HEALTH_LEFT': '{name} has {amount} health left',
    'EVADE': '{name} has evaded the attack!',
    'BLOCK': '{name} has blocked the attack!',
    'CRIT_DAMAGE': '{name} is hitting for an additional {amount} damage!',
    'DAMAGE_AFTER_ARMOR': '{name} is dealth {amount} of damage',
    'FENCER_FOCUS': '{name} has dropped their foes armor reduction by 15%',
    'IGNORE_ARMOR': '{name} is ignoring all armor!',
    'MAGIC_KNIGHT_REDUCE_ARMOR': '{name} reduced foes armor reduction by 5% (now {amount}%)',
    'DOUBLE_MAGIC_DAMAGE': '{name} is taking double damage due to their magic weakness',
    'STEAL_HEALTH': '{name} just stole {amount} health from their foe',
    'HEAL': '{name} has healed for {amount}',
    'HEAL_TWICE': '{name} has healed for an additional {amount}',
    'ROGUE_DOUBLE_HIT': '{name} isn''t done attacking yet!',
    'RESURRECTION': '{name} just resurrected!',
    'FIRE_DAMAGE_BONUS': '{name} has increased their damage by 15%!',
    'BERSERK': '{name} is attacking again!',
    'FROST_SHIELD': '{name} reduced their foes crit chance by 20% (now {amount})',
    'ASSASSIN_CRIT_DAMAGE': '{name} is doing an additional {amount} critical damage!'
}

#===============================

#Combat

#===============================

def setupFight(entity1, entity2):

    #Battle Log
    battleLog = {
        'winner': None,
        'goesFirst': None,
        'log': [[]] #First row is always the starting phase - declare health of each and any starting effects
    }

    #Calculate and insert each others resistances based on the other entities stats/level
    calculateResistances(entity1, entity2)
    calculateResistances(entity2, entity1)

    #Process secondary stats
    calculateSecondaryStats(entity1)
    calculateSecondaryStats(entity2)

    #Take care of class-specific bonuses
    classSpecificBonuses(entity1, entity2, battleLog)
    classSpecificBonuses(entity2, entity1, battleLog)

    #Decide who goes first - 50/50
    goesFirst = random.random()

    winner = None

    if goesFirst > 0.5:
        battleLog['goesFirst'] = entity1['name']
        winner = startFight(entity1, entity2, battleLog)
    else:
        battleLog['goesFirst'] = entity2['name']
        winner = startFight(entity2, entity1, battleLog)

    #Declare the winner
    battleLog['winner'] = winner['name']

    return battleLog


#Begins the fight between the two entities - having all the final stats ready
def startFight(entity1, entity2, battleLog):

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

        turnLog = []

        #Show the health at the start of every turn
        turnLog.append(entity1['name'] + ':HEALTH:' + str(entity1['health']))
        turnLog.append(entity2['name'] + ':HEALTH:' + str(entity2['health']))

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
        attackerClass = attacker['class_name']
        defenderClass = defender['class_name']

        if defenderClass == 'Scout' or defenderClass == 'Rogue' or defenderClass == 'Assassin' or defenderClass == 'Warrior':
            doesDefenderEvadeOrBlock = checkEvadeOrBlock(attacker, defender, turnLog)

        #If there was no evasion or block
        if not doesDefenderEvadeOrBlock:

            #Magic knight reduces armor reduction by 5%
            if attackerClass == 'Magic Knight':
                defender['armorReduction'] -= 5.0

                #Make sure the armor reduction isn't negative
                if defender['armorReduction'] < 0:
                    defender['armorReduction'] = 0

                turnLog.append(attacker['name'] + ':MAGIC_KNIGHT_REDUCE_ARMOR:' + str(defender['armorReduction']))

            #Check for critical hits
            isHitCritical = checkCriticalHit(attacker, defender, turnLog)

            if isHitCritical:
                processCriticalHit(attacker, defender, turnLog)

            #Total up the damage including ( [baseDamage + critDamage] * turnDamage )
            baseDamage = attacker['damage']

            #Berserker takes 2x damage from mages
            if helper.classes[attackerClass]['stat'] == 'int' and defenderClass == 'Berserker':
                baseDamage *= 2
                
                turnLog.append(defender['name'] + ':DOUBLE_MAGIC_DAMAGE')

            #Damage = ( (baseDmg + critDmg) * turnDmg ) - ( damage * (1 - (armorReduction/100) )
            attackerDamage = math.floor((float(baseDamage) + float(attacker['critDamage'])) * float(attacker['turnDamage']))
            damageAfterArmor = math.floor(float(attackerDamage) * (1 - defender['armorReduction'] / 100))

            turnLog.append(attacker['name'] + ':DAMAGE_AFTER_ARMOR:' + str(damageAfterArmor))

            defender['health'] -= damageAfterArmor

            if attackerClass == 'Dark Mage':
                if random.random() > 0.5:
                    healthStolen = math.floor(baseDamage / 3)
                    attacker['health'] += healthStolen

                    turnLog.append(attacker['name'] + ':STEAL_HEALTH:' + str(healthStolen))
                    
                    #Make sure health doesn't go over max
                    if attacker['health'] > attacker['maxHealth']:
                        attacker['health'] = attacker['maxHealth']

            #Check for resurrection
            checkIfRessurected(defender, turnLog)

        #Change the turn over to the other player
        if decider == 0:
            decider = 1
        else:
            decider = 0
        
        #Rogues attack twice - so change the decider back
        if attackerClass == 'Rogue':
            if hasAttackedTwice == False:
                if decider == 0:
                    decider = 1
                else:
                    decider = 0

                attacker['turnDamage'] -= 0.2
                hasAttackedTwice = True
                turnLog.append(attacker['name'] + ':ROGUE_DOUBLE_HIT')

            #Set the counter back for the next time its the rogue's turn
            else:
                hasAttackedTwice = False

        #Berserkers have a 50% chance to attack again
        if attackerClass == 'Berserker':
            if random.random() >= 0.5:
                if decider == 0:
                    decider = 1
                else:
                    decider = 0

                attacker['turnDamage'] -= 0.2

                turnLog.append(attacker['name'] + ':BERSERK')

        #If attacker is a fire mage, increase damage by 35% not 20%
        if attackerClass == 'Fire Mage':
            attacker['turnDamage'] += 0.35

            turnLog.append(attacker['name'] + ':FIRE_DAMAGE_BONUS')
        else:
            attacker['turnDamage'] += 0.2

        #Show defenders health left
        turnLog.append(defender['name'] + ':HEALTH_LEFT:' + str(defender['health']))

        #Add the turn log to the battle log list
        battleLog['log'].append(turnLog)

    if entity1['health'] <= 0:
        return entity2
    else:
        return entity1


#Calculates all of the entities secondary stats based on base stats
def calculateSecondaryStats(entity):
    calculateArmorReduction(entity)
    calculateDamage(entity)
    calculateHealth(entity)
    calculateCritChance(entity)


#Calculates armor reduction based on level and total armor
def calculateArmorReduction(entity):
    classMaxArmorReduction = helper.classes[entity['class_name']]['max_armor_reduction'] * 100
            
    armor = entity['armor']
    armorReduction = math.floor(armor / entity['level'])

    if armorReduction > classMaxArmorReduction:
        armorReduction = classMaxArmorReduction

    entity['armorReduction'] = armorReduction


#Calculates damage based on level and the main stat of the class
def calculateDamage(entity):
    level = entity['level']
    classStat = helper.classes[entity['class_name']]['stat']
    mainStat = None

    if classStat == 'str':
        mainStat = entity['strength']
    elif classStat == 'dex':
        mainStat = entity['dexterity']
    else:
        mainStat = entity['intelligence']

    damage = entity['damage']

    if level <= 5:
        damage = math.floor(damage/30 * (level ** 2) + 10)
    else:
        damage = math.floor(damage/40 * (level ** 2) + 10)

    entity['damage'] = damage


#Calculates health based on level and constitution
def calculateHealth(entity):
    constitution = int(entity['constitution'])
    level = int(entity['level'])
    healthModifier = helper.classes[entity['class_name']]['health_modifier']
    health = 0

    if level <= 5:
        health = math.floor(healthModifier * (level ** 2) * 4 * (constitution/20) + 60)
    else:
        health = math.floor(healthModifier * (level ** 2) * 4 * (constitution/30) + 60)

    entity['health'] = health
    entity['maxHealth'] = health


#Calculates critical chance based on level and luck
def calculateCritChance(entity):
    classMaxCritChance = helper.classes[entity['class_name']]['max_crit_chance'] * 100
    
    luck = int(entity['luck'])
    critChance = math.floor(luck / int(entity['level']))

    if critChance > classMaxCritChance:
        critChance = classMaxCritChance

    entity['critChance'] = critChance


#Adds/removes stats based on class-specific traits/abilities
def classSpecificBonuses(entity1, entity2, battleLog):
    #Fencer immediately removes 15% armor reduction
    if entity1['class_name'] == 'Fencer':
        battleLog['log'][0].append(entity1['name'] + ':FENCER_FOCUS')
        entity2['armorReduction'] -= 15.0

    #Mages ignore armor
    if helper.classes[entity1['class_name']]['stat'] == 'int' and entity2['class_name'] != 'Magic Knight':
        battleLog['log'][0].append(entity1['name'] + ':IGNORE_ARMOR')
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
def checkEvadeOrBlock(attacker, defender, turnLog):
    evadeBlockChance = 0.25
    attackerClass = attacker['class_name']
    defenderClass = defender['class_name']

	#Cannot evade magical attacks unless the defender is a scout
    if helper.classes[attackerClass]['stat'] == 'int' and defenderClass != 'Scout':
        return False
    else:
        #Scouts can evade magical attacks, but only with a 15% chance
        if defenderClass == 'Scout':
            evadeBlockChance -= 0.10
			
        if evadeBlockChance > random.random():
            if defenderClass == 'Warrior':
                turnLog.append(defender['name'] + ':BLOCK')
            else:
                turnLog.append(defender['name'] + ':EVADE')
            return True
    return False


#Checks if the attacker critically strikes
def checkCriticalHit(attacker, defender, turnLog):
    critChance = attacker['critChance']
    rand = random.random() * 100
    
    #Frost mages drop the critical chance of foes
    if defender['class_name'] == 'Frost Mage':
        critChance -= 20

        if critChance < 0:
            critChance = 0

        turnLog.append(attacker['name'] + ':FROST_SHIELD:' + str(critChance))

    if critChance > rand:
        return True
    else:
        return False


#If an entity critically strikes, process the critical hit for their class
def processCriticalHit(attacker, defender, turnLog):
    baseDamage = attacker['damage']

    #If the attacker is an assassin - your crit damage is twice as much
    if attacker['class_name'] == 'Assassin':
        attacker['critDamage'] = baseDamage * 2
        turnLog.append(attacker['name'] + ':ASSASSIN_CRIT_DAMAGE:' + str(attacker['critDamage']))
    
    #If the attacker is a blood mage, heal based on base damage
    elif attacker['class_name'] == 'Blood Mage':
        healAmount = math.floor(baseDamage / 2)
        attacker['health'] += healAmount

        turnLog.append(attacker['name'] + ':HEAL:' + str(healAmount))

        #If the enemy is a mage - heal twice as much
        if helper.classes[defender['class_name']]['stat'] == 'int':
            attacker['health'] += healAmount

            turnLog.append(attacker['name'] + ':HEAL_TWICE:' + str(healAmount))

        #Make sure health doesn't go over max
        if attacker['health'] > attacker['maxHealth']:
            attacker['health'] = attacker['maxHealth']
        
    else:
        attacker['critDamage'] = baseDamage
        turnLog.append(attacker['name'] + ':CRIT_DAMAGE:' + str(attacker['critDamage']))


#Checks if the defender is a demon hunter - is so check if resurrection is successful
def checkIfRessurected(defender, turnLog):
    if defender['health'] <= 0 and defender['class_name'] == 'Demon Hunter':
        if random.random() < 0.35:
            defender['health'] = defender['maxHealth']

            turnLog.append(defender['name'] + ':RESURRECTION')


#Translates the battle log to human-readable text - inserting the values in when applicable
def translateBattleLog(battleLog):
    for i in range(0, len(battleLog)):
        print('\n')
        for j in range(0, len(battleLog[i])):
            text = battleLog[i][j]
            splitText = text.split(':')
            keyValue = battleLogTags[splitText[1]]

            if len(splitText) == 2:
                print(keyValue.replace('{name}',splitText[0]))
            else:
                print(keyValue.replace('{name}',splitText[0]).replace('{amount}',splitText[2]))