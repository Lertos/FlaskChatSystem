import mysql.connector

#Connect to the database. 
#Note: Id much rather connect once for every query - but I am getting 'Access Denied' errors 

conn = mysql.connector.connect(
  host='127.0.0.1',
  port='3306',
  user='root',
  password='flaskrpg123',
  database='flasksimplerpg'
)

#===============================

#Server Setup

#===============================


def getClasses():
  cursor = conn.cursor()
  cursor.execute('''SELECT class_name, stat, weapons, uses_two_handed, uses_shield, max_armor_reduction, health_modifier FROM classes;''')
  
  result = {}

  for row in cursor:
    result[row[0]] = {}
    result[row[0]]['stat'] = row[1]
    result[row[0]]['weapons'] = row[2]
    result[row[0]]['uses_two_handed'] = row[3]
    result[row[0]]['uses_shield'] = row[4]
    result[row[0]]['max_armor_reduction'] = row[5]
    result[row[0]]['health_modifier'] = row[6]

  cursor.close()

  return result


def getItemTypes():
  cursor = conn.cursor()
  cursor.execute('''SELECT item_type_id, is_weapon, item_type_name, is_two_handed, stat, damage_multiplier, armor_per_level, stats_per_level FROM item_types;''')
  
  result = {}

  for row in cursor:
    result[row[0]] = {}
    result[row[0]]['is_weapon'] = row[1]
    result[row[0]]['item_type_name'] = row[2]
    result[row[0]]['is_two_handed'] = row[3]
    result[row[0]]['stat'] = row[4]
    result[row[0]]['damage_multiplier'] = row[5]
    result[row[0]]['armor_per_level'] = row[6]
    result[row[0]]['stats_per_level'] = row[7]

  cursor.close()

  return result


def getItemRarities():
  cursor = conn.cursor()
  cursor.execute('''SELECT rarity_name, drop_chance, multiplier, css_class_name FROM item_rarities;''')
  
  result = {}

  for row in cursor:
    result[row[0]] = {}
    result[row[0]]['drop_chance'] = row[1]
    result[row[0]]['multiplier'] = row[2]
    result[row[0]]['css_class_name'] = row[3]

  cursor.close()

  return result


def getWeaponPrefixes():
  cursor = conn.cursor()

  cursor.execute('''SELECT item_prefix_id, prefix, damage_mult, strength_mult, dexterity_mult, intelligence_mult, constitution_mult, luck_mult FROM item_prefixes WHERE is_weapon = 1;''')
  result = {}

  for row in cursor:
    result[row[0]] = {}
    result[row[0]]['prefix'] = row[1]
    result[row[0]]['damage_mult'] = row[2]
    result[row[0]]['strength_mult'] = row[3]
    result[row[0]]['dexterity_mult'] = row[4]
    result[row[0]]['intelligence_mult'] = row[5]
    result[row[0]]['constitution_mult'] = row[6]
    result[row[0]]['luck_mult'] = row[7]

  cursor.close()

  return result


def getArmorPrefixes():
  cursor = conn.cursor()

  cursor.execute('''SELECT item_prefix_id, prefix, armor_mult, strength_mult, dexterity_mult, intelligence_mult, constitution_mult, luck_mult FROM item_prefixes WHERE is_weapon = 0;''')
  result = {}

  for row in cursor:
    result[row[0]] = {}
    result[row[0]]['prefix'] = row[1]
    result[row[0]]['armor_mult'] = row[2]
    result[row[0]]['strength_mult'] = row[3]
    result[row[0]]['dexterity_mult'] = row[4]
    result[row[0]]['intelligence_mult'] = row[5]
    result[row[0]]['constitution_mult'] = row[6]
    result[row[0]]['luck_mult'] = row[7]

  cursor.close()

  return result


def getQuestMonsters():
  cursor = conn.cursor()
  cursor.execute('''SELECT quest_monster_id, monster_name, class_name, file_name FROM quest_monsters;''')
  
  result = {}

  for row in cursor:
    result[row[0]] = {}
    result[row[0]]['monster_name'] = row[1]
    result[row[0]]['class_name'] = row[2]
    result[row[0]]['file_name'] = row[3]

  cursor.close()

  return result


def getBountyMonsters():
  cursor = conn.cursor()
  cursor.execute('''SELECT bounty_monster_id, monster_name, monster_suffix, region_name, class_name, file_name FROM bounty_monsters;''')
  
  result = {}

  for row in cursor:
    result[row[0]] = {}
    result[row[0]]['monster_name'] = row[1]
    result[row[0]]['monster_suffix'] = row[2]
    result[row[0]]['region_name'] = row[3]
    result[row[0]]['class_name'] = row[4]
    result[row[0]]['file_name'] = row[5]

  cursor.close()

  return result


#===============================

#Player Driven Calls

#===============================


def getPlayerLogin(username, password):
  cursor = conn.cursor(dictionary=True)

  data = [username, password]
  stmt = '''SELECT player_id, username, display_name, has_character FROM players WHERE username = %s and password = %s;'''
  cursor.execute(stmt, data)
  
  result = {}

  for row in cursor.fetchall():
    result = row

  cursor.close()

  return result


def createPlayerAccount(username, displayName, password):
  cursor = conn.cursor(dictionary=True)

  args = [username, displayName, password]
  cursor.callproc('usp_create_user_account', args)

  result = {}

  for row in cursor.stored_results():
    users = row.fetchall()

  for user in users:
    result = user

  cursor.close()

  return result


def createNewCharacter(data):
  cursor = conn.cursor()

  stmt = '''UPDATE players SET class_name = %s, file_name = %s, has_character = 1 WHERE player_id = %s;'''
  cursor.execute(stmt, data)
  
  conn.commit()
  cursor.close()


def getDashboardDetails(playerId):
  cursor = conn.cursor(dictionary=True)

  cursor.callproc('usp_get_dashboard_details', [playerId])

  result = {}

  for row in cursor.stored_results():
    users = row.fetchall()

  for user in users:
    result = user

  cursor.close()

  return result


def getPlayerInventory(playerId):
  cursor = conn.cursor(dictionary=True)

  cursor.callproc('usp_get_player_inventory_items', [playerId])

  result = []

  for row in cursor.stored_results():
    result = row.fetchall()

  cursor.close()

  return result


def createNewItem(playerId, level, itemTypeId, itemPrefixId, itemRarity, itemStats, itemDamage, itemArmor, itemWorth):  
  cursor = conn.cursor(dictionary=True)

  args = [playerId, level, itemTypeId, itemPrefixId, itemRarity, itemStats[0], itemStats[1], itemStats[2], itemStats[3], itemStats[4], itemDamage, itemArmor, itemWorth]
  cursor.callproc('usp_create_new_item', args)

  conn.commit()
  cursor.close()
