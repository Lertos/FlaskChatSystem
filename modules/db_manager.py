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
  cursor.execute('''SELECT item_type_id, is_weapon, armor_type, item_type_name, is_two_handed, stat, damage_multiplier, armor_per_level, stats_per_level FROM item_types;''')
  
  result = {}

  for row in cursor:
    result[row[0]] = {}
    result[row[0]]['is_weapon'] = row[1]
    result[row[0]]['armor_type'] = row[2]
    result[row[0]]['item_type_name'] = row[3]
    result[row[0]]['is_two_handed'] = row[4]
    result[row[0]]['stat'] = row[5]
    result[row[0]]['damage_multiplier'] = row[6]
    result[row[0]]['armor_per_level'] = row[7]
    result[row[0]]['stats_per_level'] = row[8]

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


def getItemPrefixes():
  cursor = conn.cursor()

  cursor.execute('''SELECT item_prefix_id, item_type_id, prefix, strength_multiplier, dexterity_multiplier, intelligence_multiplier, constitution_multiplier, luck_multiplier FROM item_prefixes;''')
  result = {}

  for row in cursor:
    result[row[0]] = {}
    result[row[0]]['item_type_id'] = row[1]
    result[row[0]]['prefix'] = row[2]
    result[row[0]]['strength_multiplier'] = row[3]
    result[row[0]]['dexterity_multiplier'] = row[4]
    result[row[0]]['intelligence_multiplier'] = row[5]
    result[row[0]]['constitution_multiplier'] = row[6]
    result[row[0]]['luck_multiplier'] = row[7]

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
  stmt = '''SELECT username, display_name, has_character FROM players WHERE username = %s and password = %s;'''
  cursor.execute(stmt, data)
  
  result = cursor.fetchall()
  print(result)

  cursor.close()

  return result