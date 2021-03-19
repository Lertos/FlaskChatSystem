from multiprocessing import Pool
import mysql.connector
import mysql.connector.pooling


dbconfig = {
  'host':'127.0.0.1',
  'port':'3306',
  'user':'root',
  'password':'flaskrpg123',
  'database':'flasksimplerpg'
}


class MySQLPool(object):


    def __init__(self):
        self.dbconfig = dbconfig
        self.pool = self.create_pool(pool_name='pool', pool_size=3)


    def create_pool(self, pool_name, pool_size):
        pool = mysql.connector.pooling.MySQLConnectionPool(pool_name=pool_name, pool_size=pool_size, pool_reset_session=True, **self.dbconfig)
        return pool


    def close(self, conn, cursor):
        cursor.close()
        conn.close()


    def execute(self, sql, args=None, commit=False):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        if commit is True:
            conn.commit()
            self.close(conn, cursor)
            return None
        else:
            res = cursor.fetchall()
            self.close(conn, cursor)
            return res


    def getClasses(self):
      conn = self.pool.get_connection()
      cursor = conn.cursor()
      cursor.execute('''SELECT class_name, stat, uses_two_handed, uses_shield, max_armor_reduction, max_crit_chance, health_modifier FROM classes;''')
      
      result = {}

      for row in cursor:
        result[row[0]] = {}
        result[row[0]]['stat'] = row[1]
        result[row[0]]['uses_two_handed'] = row[2]
        result[row[0]]['uses_shield'] = row[3]
        result[row[0]]['max_armor_reduction'] = float(row[4])
        result[row[0]]['max_crit_chance'] = float(row[5])
        result[row[0]]['health_modifier'] = float(row[6])

      self.close(conn, cursor)

      return result


    def getItemTypes(self):
      conn = self.pool.get_connection()
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

      self.close(conn, cursor)

      return result


    def getItemRarities(self):
      conn = self.pool.get_connection()
      cursor = conn.cursor()
      cursor.execute('''SELECT rarity_name, drop_chance, multiplier, css_class_name FROM item_rarities;''')
      
      result = {}

      for row in cursor:
        result[row[0]] = {}
        result[row[0]]['drop_chance'] = row[1]
        result[row[0]]['multiplier'] = row[2]
        result[row[0]]['css_class_name'] = row[3]

      self.close(conn, cursor)

      return result


    def getWeaponPrefixes(self):
      conn = self.pool.get_connection()
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

      self.close(conn, cursor)

      return result


    def getArmorPrefixes(self):
      conn = self.pool.get_connection()
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

      self.close(conn, cursor)

      return result


    def getQuestMonsters(self):
      conn = self.pool.get_connection()
      cursor = conn.cursor()
      cursor.execute('''SELECT quest_monster_id, monster_name, class_name, file_name FROM quest_monsters;''')
      
      result = {}

      for row in cursor:
        result[row[0]] = {}
        result[row[0]]['monster_name'] = row[1]
        result[row[0]]['class_name'] = row[2]
        result[row[0]]['file_name'] = row[3]

      self.close(conn, cursor)

      return result


    def getBountyMonsters(self):
      conn = self.pool.get_connection()
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

      self.close(conn, cursor)

      return result


    #===============================

    #Player Driven Calls

    #===============================


    def getPlayerLogin(self, username, password):
      conn = self.pool.get_connection()
      cursor = conn.cursor(dictionary=True)

      data = [username, password]
      stmt = '''SELECT player_id, username, display_name, class_name, player_level, has_character FROM players WHERE username = %s and password = %s;'''
      cursor.execute(stmt, data)
      
      result = {}

      for row in cursor.fetchall():
        result = row

      self.close(conn, cursor)

      return result


    def createPlayerAccount(self, username, displayName, password):
      conn = self.pool.get_connection()
      cursor = conn.cursor(dictionary=True)

      args = [username, displayName, password]
      cursor.callproc('usp_create_user_account', args)

      result = {}

      for row in cursor.stored_results():
        users = row.fetchall()

      for user in users:
        result = user

      self.close(conn, cursor)

      return result


    def createNewCharacter(self, data):
      conn = self.pool.get_connection()
      cursor = conn.cursor()

      stmt = '''UPDATE players SET class_name = %s, file_name = %s, has_character = 1 WHERE player_id = %s;'''
      cursor.execute(stmt, data)
      
      conn.commit()
      self.close(conn, cursor)


    def getDashboardDetails(self, playerId):
      conn = self.pool.get_connection()
      cursor = conn.cursor(dictionary=True)

      cursor.callproc('usp_get_dashboard_details', [playerId])

      result = {}

      for row in cursor.stored_results():
        users = row.fetchall()

      for user in users:
        result = user

      self.close(conn, cursor)

      return result


    def getPlayerInventory(self, playerId):
      conn = self.pool.get_connection()
      cursor = conn.cursor(dictionary=True)

      cursor.callproc('usp_get_player_inventory_items', [playerId])

      result = []

      for row in cursor.stored_results():
        result = row.fetchall()

      self.close(conn, cursor)

      return result


    def getPlayerEquippedItems(self, playerId):
      conn = self.pool.get_connection()
      cursor = conn.cursor(dictionary=True)

      cursor.callproc('usp_get_player_equipped_items', [playerId])

      result = []

      for row in cursor.stored_results():
        result = row.fetchall()

      self.close(conn, cursor)

      return result


    def createNewItem(self, playerId, level, itemTypeId, itemPrefixId, itemRarity, itemStats, itemDamage, itemArmor, itemWorth):  
      conn = self.pool.get_connection()
      cursor = conn.cursor(dictionary=True)

      args = [playerId, level, itemTypeId, itemPrefixId, itemRarity, itemStats[0], itemStats[1], itemStats[2], itemStats[3], itemStats[4], itemDamage, itemArmor, itemWorth]
      cursor.callproc('usp_create_new_item', args)

      conn.commit()
      self.close(conn, cursor)


    def sellInventoryItem(self, playerId, sellPrice, inventoryId):  
      conn = self.pool.get_connection()
      cursor = conn.cursor()

      args = [playerId, sellPrice, inventoryId]
      cursor.callproc('usp_sell_inventory_item', args)

      conn.commit()
      self.close(conn, cursor)


    def equipInventoryItem(self, playerId, inventoryId):  
      conn = self.pool.get_connection()
      cursor = conn.cursor()

      args = [playerId, inventoryId]
      cursor.callproc('usp_equip_inventory_item', args)

      conn.commit()
      self.close(conn, cursor)


    def unequipInventoryItem(self, playerId, inventoryId):  
      conn = self.pool.get_connection()
      cursor = conn.cursor()

      args = [playerId, inventoryId]
      cursor.callproc('usp_unequip_inventory_item', args)

      conn.commit()
      self.close(conn, cursor)


    #===============================

    #Debug/Testing Functions

    #===============================

    def debugRemoveAllPlayerItems(self, playerId):
      conn = self.pool.get_connection()
      cursor = conn.cursor()

      data = [playerId]
      stmt = '''DELETE FROM player_inventories WHERE player_id = %s;'''
      cursor.execute(stmt, data)
      
      conn.commit()
      self.close(conn, cursor)



if __name__ == "__main__":
    mysql_pool = MySQLPool(**dbconfig)
    '''
    sql = "select 1=1"
    p = Pool()
    for i in range(5):
        p.apply_async(mysql_pool.execute, args=(sql,))
    '''


