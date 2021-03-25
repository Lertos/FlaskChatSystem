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


#===============================

#Base Functions

#===============================


    #Executes a procedures without returning anything
    def executeStatementServerSetup(self, statement, attributeList):
      conn = self.pool.get_connection()
      cursor = conn.cursor()
      
      cursor.execute(statement)

      result = {}

      for row in cursor:
        result[row[0]] = {}

        for i in range(0, len(attributeList)):
          result[row[0]][attributeList[i]] = row[i+1]

      self.close(conn, cursor)
      return result


    #Executes a procedures without returning anything
    def executeStatement(self, statement, commit, dictCursor, makeList, returnList, args=None):
      conn = self.pool.get_connection()
      cursor = conn.cursor(dictionary=dictCursor)
      
      if args:
          cursor.execute(statement, args)
      else:
          cursor.execute(statement)
      
      #Check whether the results are in list or dictionary form
      result = None
      
      if returnList:
        result = []
      else:
        result = {}

      if makeList:
        result = list(cursor.fetchall())
      else:
        for row in cursor.fetchall():
          result = row

      if commit is True:
          conn.commit()

      self.close(conn, cursor)
      return result


    #Executes a procedures without returning anything
    def executeProcedure(self, procedure, commit, args=None):
      conn = self.pool.get_connection()
      cursor = conn.cursor()
      
      if args:
          cursor.callproc(procedure, args)
      else:
          cursor.callproc(procedure)
      
      if commit is True:
          conn.commit()

      self.close(conn, cursor)


    #Executes a procedure and returns a list
    def executeProcedureReturnList(self, procedure, commit, dictCursor, args=None):
        conn = self.pool.get_connection()
        cursor = conn.cursor(dictionary=dictCursor)
        
        if args:
            cursor.callproc(procedure, args)
        else:
            cursor.callproc(procedure)
        
        if commit is True:
            conn.commit()

        result = []

        for row in cursor.stored_results():
          result = row.fetchall()

        self.close(conn, cursor)
        return result


    #Executes a procedure and returns a dictonary
    def executeProcedureReturnDict(self, procedure, commit, dictCursor, args=None):
        conn = self.pool.get_connection()
        cursor = conn.cursor(dictionary=dictCursor)
        
        if args:
            cursor.callproc(procedure, args)
        else:
            cursor.callproc(procedure)
        
        if commit is True:
            conn.commit()

        result = {}

        for row in cursor.stored_results():
          result = row.fetchall()

        self.close(conn, cursor)
        return result


#===============================

#Specific Functions

#===============================


    def clearAllTransactionalData(self):
      self.executeProcedure('usp_clear_transactional_data', commit=True, args=None)


    def getSeasonList(self):
      statement = '''SELECT season, upcoming, start_date FROM seasons;'''
      result = self.executeStatement(statement, commit=False, dictCursor=True, makeList=True, returnList=True, args=None)

      return result


    def getClasses(self):
      statement = '''SELECT class_name, stat, uses_two_handed, uses_shield, max_armor_reduction, max_crit_chance, health_modifier FROM classes;'''
      attributeList = ['stat', 'uses_two_handed', 'uses_shield', 'max_armor_reduction', 'max_crit_chance', 'health_modifier']
      result = self.executeStatementServerSetup(statement, attributeList)

      for key in result:
        result[key]['max_armor_reduction'] = float(result[key]['max_armor_reduction'])
        result[key]['max_crit_chance'] = float(result[key]['max_crit_chance'])
        result[key]['health_modifier'] = float(result[key]['health_modifier'])

      return result


    def getItemTypes(self):
      statement = '''SELECT item_type_id, is_weapon, item_type_name, is_two_handed, stat, damage_multiplier, armor_per_level, stats_per_level FROM item_types;'''
      attributeList = ['is_weapon', 'item_type_name', 'is_two_handed', 'stat', 'damage_multiplier', 'armor_per_level', 'stats_per_level']
      result = self.executeStatementServerSetup(statement, attributeList)

      return result


    def getItemRarities(self):
      statement = '''SELECT rarity_name, drop_chance, multiplier, css_class_name FROM item_rarities;'''
      attributeList = ['drop_chance', 'multiplier', 'css_class_name']
      result = self.executeStatementServerSetup(statement, attributeList)

      return result


    def getWeaponPrefixes(self):
      statement = '''SELECT item_prefix_id, prefix, damage_mult, strength_mult, dexterity_mult, intelligence_mult, constitution_mult, luck_mult FROM item_prefixes WHERE is_weapon = 1;'''
      attributeList = ['prefix', 'damage_mult', 'strength_mult', 'dexterity_mult', 'intelligence_mult', 'constitution_mult', 'luck_mult']
      result = self.executeStatementServerSetup(statement, attributeList)

      return result


    def getArmorPrefixes(self):
      statement = '''SELECT item_prefix_id, prefix, armor_mult, strength_mult, dexterity_mult, intelligence_mult, constitution_mult, luck_mult FROM item_prefixes WHERE is_weapon = 0;'''
      attributeList = ['prefix', 'armor_mult', 'strength_mult', 'dexterity_mult', 'intelligence_mult', 'constitution_mult', 'luck_mult']
      result = self.executeStatementServerSetup(statement, attributeList)

      return result


    def getQuestMonsters(self):
      statement = '''SELECT quest_monster_id, monster_name, class_name, file_name FROM quest_monsters;'''
      attributeList = ['monster_name', 'class_name', 'file_name']
      result = self.executeStatementServerSetup(statement, attributeList)

      return result


    def getBountyMonsters(self):
      statement = '''SELECT bounty_monster_id, monster_name, monster_suffix, region_name, class_name, file_name FROM bounty_monsters;'''
      attributeList = ['monster_name', 'monster_suffix', 'region_name', 'class_name', 'file_name']
      result = self.executeStatementServerSetup(statement, attributeList)

      return result


    #===============================

    #Player Driven Calls

    #===============================


    def getPlayerLogin(self, username, password):
      args = [username, password]
      statement = '''SELECT player_id, username, display_name, class_name, player_level, has_character FROM players WHERE username = %s and password = %s;'''
      result = self.executeStatement(statement, commit=False, dictCursor=True, makeList=False, returnList=False, args=args)

      return result


    def createPlayerAccount(self, username, displayName, password, season):
      args = [username, displayName, password, season]
      result = self.executeProcedureReturnDict('usp_create_user_account', commit=True, dictCursor=True, args=args)

      return result[0]


    def createNewCharacter(self, data):
      args = data
      statement = '''UPDATE players SET class_name = %s, file_name = %s, has_character = 1 WHERE player_id = %s;'''
      result = self.executeStatement(statement, commit=True, dictCursor=False, makeList=False, returnList=False, args=args)


    def getDashboardDetails(self, playerId):
      args = [playerId]
      result = self.executeProcedureReturnDict('usp_get_dashboard_details', commit=True, dictCursor=True, args=args)

      return result[0]


    def getPlayerStats(self, playerId):   
      args = [playerId]
      result = self.executeProcedureReturnList('usp_get_player_info', commit=False, dictCursor=True, args=args)

      return result[0]


    def getMonsterStats(self, playerId, monsterId, monsterType):
      args = [playerId, monsterId]
      
      if monsterType == 'quest':
        result = self.executeProcedureReturnList('usp_get_quest_monster_info', commit=False, dictCursor=True, args=args)

      return result[0]


    def getPlayerInventory(self, playerId):
      args = [playerId]
      result = self.executeProcedureReturnList('usp_get_player_inventory_items', commit=False, dictCursor=True, args=args)

      return result


    def getPlayerEquippedItems(self, playerId):
      args = [playerId]
      result = self.executeProcedureReturnList('usp_get_player_equipped_items', commit=False, dictCursor=True, args=args)

      return result


    def createNewItem(self, playerId, level, itemTypeId, itemPrefixId, itemRarity, itemStats, itemDamage, itemArmor, itemWorth):  
      args = [playerId, level, itemTypeId, itemPrefixId, itemRarity, itemStats[0], itemStats[1], itemStats[2], itemStats[3], itemStats[4], itemDamage, itemArmor, itemWorth]
      self.executeProcedure('usp_create_new_item', commit=True, args=args)


    def sellInventoryItem(self, playerId, sellPrice, inventoryId):  
      args = [playerId, sellPrice, inventoryId]
      self.executeProcedure('usp_sell_inventory_item', commit=True, args=args)


    def equipInventoryItem(self, playerId, inventoryId):  
      args = [playerId, inventoryId]
      self.executeProcedure('usp_equip_inventory_item', commit=True, args=args)


    def unequipInventoryItem(self, playerId, inventoryId):
      args = [playerId, inventoryId]
      self.executeProcedure('usp_unequip_inventory_item', commit=True, args=args)


    def createQuestMonsterForPlayer(self, playerId, quest_monster_id, xp, gold, stamina, time, strength, dexterity, intelligence, constitution, luck, strengthMult, dexterityMult, intelligenceMult, constitutionMult, luckMult):  
      args = [playerId, quest_monster_id, xp, gold, stamina, time, strength, dexterity, intelligence, constitution, luck, strengthMult, dexterityMult, intelligenceMult, constitutionMult, luckMult]
      self.executeProcedure('usp_create_quest_monster_for_player', commit=True, args=args)

    
    def getPlayerQuestMonsters(self, playerId):  
      args = [playerId]
      result = self.executeProcedureReturnList('usp_get_player_quest_monsters', commit=False, dictCursor=True, args=args)

      return result

    
    def givePlayerQuestRewards(self, playerId, stamina, gold, xp):
      args = [playerId, stamina, gold, xp]
      result = self.executeProcedureReturnList('usp_give_player_quest_rewards', commit=True, dictCursor=True, args=args)

      return result


    #===============================

    #Debug/Testing Functions

    #===============================

    def debugRemoveAllPlayerItems(self, playerId):
      args = [playerId]
      statement = '''DELETE FROM player_inventories WHERE player_id = %s;'''
      result = self.executeStatement(statement, commit=True, dictCursor=False, makeList=False, returnList=False, args=args)



if __name__ == "__main__":
    mysql_pool = MySQLPool(**dbconfig)
    '''
    sql = "select 1=1"
    p = Pool()
    for i in range(5):
        p.apply_async(mysql_pool.execute, args=(sql,))
    '''


