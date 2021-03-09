import mysql.connector

host = "127.0.0.1"
user = "root"
password = "joker420lolA!"
database = "flasksimplerpg"


def getClasses():
  conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
  cursor = conn.cursor()

  cursor.execute("SELECT class_name, stat, weapons, uses_two_handed, uses_shield, max_armor_reduction, health_modifier FROM classes;")
  
  result = {}

  for r in cursor:
    result[r[0]] = {}
    result[r[0]]['stat'] = r[1]
    result[r[0]]['weapons'] = r[2]
    result[r[0]]['uses_two_handed'] = r[3]
    result[r[0]]['uses_shield'] = r[4]
    result[r[0]]['max_armor_reduction'] = r[5]
    result[r[0]]['health_modifier'] = r[6]

  cursor.close()
  conn.close()

  return result

#"SELECT quest_monster_id, monster_name, class_name, file_name FROM quest_monsters;"