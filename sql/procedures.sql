USE flasksimplerpg;

/*==============================
	usp_clear_transactional_data
==============================*/

DROP PROCEDURE IF EXISTS usp_clear_transactional_data;

DELIMITER //
CREATE PROCEDURE usp_clear_transactional_data ()
BEGIN

	DELETE FROM active_quests;
    DELETE FROM active_bounties;
    DELETE FROM travel_info;

END //
DELIMITER ;

#CALL usp_clear_transactional_data();


/*==============================
	usp_create_user_account
==============================*/

DROP PROCEDURE IF EXISTS usp_create_user_account;

DELIMITER //
CREATE PROCEDURE usp_create_user_account(
	IN p_username VARCHAR(30),
    IN p_display_name VARCHAR(30),
    IN p_password VARCHAR(30),
    IN p_season SMALLINT
)
BEGIN
	IF NOT EXISTS (SELECT * FROM players WHERE username = p_username or display_name = p_display_name) THEN
		INSERT INTO players (username, display_name, password, character_season)
		VALUES (p_username, p_display_name, p_password, p_season);
        
		INSERT INTO player_dungeons (player_id) VALUES ((SELECT player_id FROM players WHERE username = p_username));
        
        SELECT player_id, username, display_name
        FROM players
        WHERE username = p_username;
	ELSE
		IF EXISTS (SELECT * FROM players WHERE username = p_username) THEN
			SELECT '' AS username, display_name
            FROM players
            WHERE username = p_username;
		ELSE
			SELECT username, '' AS display_name
            FROM players
            WHERE display_name = p_display_name;
		END IF;
	END IF; 
	
    COMMIT;
END //
DELIMITER ;

#CALL usp_create_user_account('lertos99','lertos99','lertos99',1);


/*==============================
	usp_get_dashboard_details
==============================*/

DROP PROCEDURE IF EXISTS usp_get_dashboard_details;

DELIMITER //
CREATE PROCEDURE usp_get_dashboard_details
(
	IN p_player_id SMALLINT
)
BEGIN
	SELECT player_id, display_name, class_name, file_name, player_level, exp_until_level, strength, dexterity, intelligence,
		constitution, luck, gold, stamina, honor, blessing
	FROM players
	WHERE player_id = p_player_id;
END //
DELIMITER ;

#CALL usp_get_dashboard_details(1);


/*==============================
	usp_insert_travel_info
==============================*/

DROP PROCEDURE IF EXISTS usp_insert_travel_info;

DELIMITER //
CREATE PROCEDURE usp_insert_travel_info
(
	p_player_id SMALLINT,
	p_type_of_event VARCHAR(16),
	p_opponent_id SMALLINT,
	p_travel_time INT,
	p_multiplier DECIMAL(5,3),
	p_drop_chance DECIMAL(4,3),
	p_dungeon_tier SMALLINT,
	p_dungeon_floor SMALLINT,
	p_level SMALLINT,
	p_name VARCHAR(20),
	p_opponent_suffix VARCHAR(30),
	p_region_name VARCHAR(30),
	p_class_name VARCHAR(30),
	p_file_name VARCHAR(40),
	p_gold INT,
	p_xp INT,
	p_stamina SMALLINT,
	p_honor SMALLINT,
	p_strength SMALLINT,
	p_dexterity SMALLINT,
	p_intelligence SMALLINT,
	p_constitution SMALLINT,
	p_luck SMALLINT,
	p_damage INT,
	p_armor INT
)
BEGIN

	IF NOT EXISTS(SELECT player_id FROM travel_info WHERE player_id = p_player_id) THEN
    BEGIN
		INSERT INTO travel_info
		VALUES(
			p_player_id, 
            p_type_of_event, 
            p_opponent_id, 
            p_travel_time, 
            p_multiplier, 
            p_drop_chance, 
            p_dungeon_tier, 
            p_dungeon_floor, 
            p_level, 
            p_name, 
            p_opponent_suffix, 
			p_region_name, 
            p_class_name, 
            p_file_name, 
            p_gold, 
            p_xp, 
            p_stamina, 
            p_honor, 
            p_strength, 
            p_dexterity, 
            p_intelligence, 
            p_constitution, 
            p_luck, 
            p_damage, 
            p_armor
		);
	END;
    END IF;

END //
DELIMITER ;

#CALL usp_insert_travel_info(1);


/*==============================
	usp_get_player_inventory_items
==============================*/

DROP PROCEDURE IF EXISTS usp_get_player_inventory_items;

DELIMITER //
CREATE PROCEDURE usp_get_player_inventory_items
(
	IN p_player_id SMALLINT
)
BEGIN
    
    SELECT a.inventory_item_id, a.item_level, d.prefix, b.item_name, b.file_name, c.item_type_name, c.is_weapon, c.is_two_handed, c.stat, a.equipped, a.rarity_name, e.css_class_name, a.strength, a.dexterity, a.intelligence, a.constitution, a.luck, a.damage, a.armor, a.sell_price
	FROM player_inventories a
    JOIN items b ON a.item_id = b.item_id
    JOIN item_types c on b.item_type_id = c.item_type_id
    JOIN item_prefixes d on a.item_prefix_id = d.item_prefix_id
    JOIN item_rarities e on a.rarity_name = e.rarity_name
    WHERE a.player_id = p_player_id and a.equipped = 0;
    
END //
DELIMITER ;

#CALL usp_get_player_inventory_items(1);

/*==============================
	usp_get_player_equipped_items
==============================*/

DROP PROCEDURE IF EXISTS usp_get_player_equipped_items;

DELIMITER //
CREATE PROCEDURE usp_get_player_equipped_items
(
	IN p_player_id SMALLINT
)
BEGIN
    
    SELECT a.inventory_item_id, a.item_level, d.prefix, b.item_name, b.file_name, c.item_type_name, c.is_weapon, c.is_two_handed, c.stat, a.equipped, a.rarity_name, e.css_class_name, a.strength, a.dexterity, a.intelligence, a.constitution, a.luck, a.damage, a.armor, a.sell_price
	FROM player_inventories a
    JOIN items b ON a.item_id = b.item_id
    JOIN item_types c on b.item_type_id = c.item_type_id
    JOIN item_prefixes d on a.item_prefix_id = d.item_prefix_id
    JOIN item_rarities e on a.rarity_name = e.rarity_name
    WHERE a.player_id = p_player_id and a.equipped = 1;
    
END //
DELIMITER ;

#CALL usp_get_player_equipped_items(1);


/*==============================
	usp_get_player_items_price_and_type
==============================*/

DROP PROCEDURE IF EXISTS usp_get_player_items_price_and_type;

DELIMITER //
CREATE PROCEDURE usp_get_player_items_price_and_type
(
	IN p_player_id SMALLINT
)
BEGIN

    SELECT a.inventory_item_id, c.item_type_name, c.is_weapon, c.is_two_handed, c.stat, a.sell_price
	FROM player_inventories a
    JOIN items b ON a.item_id = b.item_id
    JOIN item_types c on b.item_type_id = c.item_type_id
    WHERE a.player_id = p_player_id;
    
END //
DELIMITER ;

#CALL usp_get_player_items_price_and_type(1);


/*==============================
	usp_create_new_item
==============================*/

DROP PROCEDURE IF EXISTS usp_create_new_item;

DELIMITER //
CREATE PROCEDURE usp_create_new_item
(
	IN p_player_id SMALLINT,
    IN p_level SMALLINT,
    IN p_item_type_id SMALLINT,
    IN p_item_prefix_id SMALLINT,
    IN p_rarity_name VARCHAR(20),
    IN p_strength SMALLINT,
    IN p_dexterity SMALLINT,
    IN p_intelligence SMALLINT,
    IN p_constitution SMALLINT,
    IN p_luck SMALLINT,
    IN p_damage SMALLINT,
    IN p_armor SMALLINT,
    IN p_worth INT
)
BEGIN
	DECLARE v_item_id SMALLINT;

	SET v_item_id = (
		SELECT item_id 
		FROM items 
		WHERE item_type_id = p_item_type_id
		ORDER BY RAND()
		LIMIT 1
    );
    
    INSERT INTO player_inventories (player_id, item_id, item_level, rarity_name, item_prefix_id, equipped, strength, dexterity, intelligence, constitution, luck, damage, armor, sell_price)
    VALUES (p_player_id, v_item_id, p_level, p_rarity_name, p_item_prefix_id, 0, p_strength, p_dexterity, p_intelligence, p_constitution, p_luck, p_damage, p_armor, p_worth);
    
    UPDATE players
    SET items_collected = items_collected + 1, 
    legendary_collected = legendary_collected + CASE WHEN p_rarity_name = 'Legendary' THEN 1 ELSE 0 END,
    mythic_collected = mythic_collected + CASE WHEN p_rarity_name = 'Mythic' THEN 1 ELSE 0 END
    WHERE player_id = p_player_id;
    
    IF p_rarity_name = 'Mythic' THEN
		INSERT INTO mythic_feed
        VALUES (p_player_id, v_item_id, p_level, p_rarity_name, p_item_prefix_id, p_strength, p_dexterity, p_intelligence, p_constitution, p_luck, p_damage, p_armor, NOW());
    END IF;
    
END //
DELIMITER ;

#CALL usp_create_new_item(1, 20, 1, 1, 'Rare', 10, 15, 20, 25, 30, 0, 45, 10);
#SELECT * FROM player_inventories;


/*==============================
	usp_sell_inventory_item
==============================*/

DROP PROCEDURE IF EXISTS usp_sell_inventory_item;

DELIMITER //
CREATE PROCEDURE usp_sell_inventory_item
(
	IN p_player_id SMALLINT,
    IN p_sell_price INT,
    IN p_inventory_id INT
)
BEGIN

	UPDATE players
    SET gold = gold + p_sell_price, gold_collected = gold_collected + p_sell_price
    WHERE player_id = p_player_id;

	DELETE FROM player_inventories
    WHERE player_id = p_player_id AND inventory_item_id = p_inventory_id;
   
END //
DELIMITER ;

#CALL usp_sell_inventory_item(1, 20, 925);
#SELECT * FROM players where player_id = 1;
#SELECT * FROM player_inventories where player_id = 1;


/*==============================
	usp_equip_inventory_item
==============================*/

DROP PROCEDURE IF EXISTS usp_equip_inventory_item;

DELIMITER //
CREATE PROCEDURE usp_equip_inventory_item
(
	IN p_player_id SMALLINT,
    IN p_inventory_id INT
)
BEGIN	

	UPDATE player_inventories
    SET equipped = 1
    WHERE player_id = p_player_id AND inventory_item_id = p_inventory_id;
   
END //
DELIMITER ;

#CALL usp_equip_inventory_item(1, 2232);


/*==============================
	usp_unequip_inventory_item
==============================*/

DROP PROCEDURE IF EXISTS usp_unequip_inventory_item;

DELIMITER //
CREATE PROCEDURE usp_unequip_inventory_item
(
	IN p_player_id SMALLINT,
    IN p_inventory_id INT
)
BEGIN

	UPDATE player_inventories
    SET equipped = 0
    WHERE player_id = p_player_id AND inventory_item_id = p_inventory_id;
   
END //
DELIMITER ;

#CALL usp_unequip_inventory_item(1, 925);


/*==============================
	usp_create_quest_monster_for_player
==============================*/

DROP PROCEDURE IF EXISTS usp_create_quest_monster_for_player;

DELIMITER //
CREATE PROCEDURE usp_create_quest_monster_for_player
(
	IN p_player_id SMALLINT,
    IN p_quest_monster_id SMALLINT,
    IN p_xp INT,
    IN p_gold INT,
    IN p_stamina TINYINT,
    IN p_time SMALLINT,
    IN p_strength SMALLINT,
    IN p_dexterity SMALLINT,
    IN p_intelligence SMALLINT,
    IN p_constitution SMALLINT,
    IN p_luck SMALLINT,
    IN p_strength_mult DECIMAL(4,3),
    IN p_dexterity_mult DECIMAL(4,3),
    IN p_intelligence_mult DECIMAL(4,3),
    IN p_constitution_mult DECIMAL(4,3),
    IN p_luck_mult DECIMAL(4,3)
)
BEGIN

	INSERT INTO active_quests (player_id, quest_monster_id, gold, xp, stamina, travel_time, strength, dexterity, intelligence, constitution, luck, strength_mult, dexterity_mult, intelligence_mult, constitution_mult, luck_mult) 
    VALUES (p_player_id, p_quest_monster_id, p_gold, p_xp, p_stamina, p_time, p_strength, p_dexterity, p_intelligence, p_constitution, p_luck, p_strength_mult, p_dexterity_mult, p_intelligence_mult, p_constitution_mult, p_luck_mult);

END //
DELIMITER ;

#CALL usp_create_quest_monster_for_player(1, 925);


/*==============================
	usp_get_player_quest_monsters
==============================*/

DROP PROCEDURE IF EXISTS usp_get_player_quest_monsters;

DELIMITER //
CREATE PROCEDURE usp_get_player_quest_monsters
(
	IN p_player_id SMALLINT
)
BEGIN

	SELECT a.quest_monster_id, b.monster_name, b.class_name, b.file_name, a.gold, a.xp, a.stamina, a.travel_time, a.strength, a.dexterity, a.intelligence, a.constitution, a.luck
    FROM active_quests a
    JOIN quest_monsters b on a.quest_monster_id = b.quest_monster_id
	WHERE a.player_id = p_player_id;

END //
DELIMITER ;

#CALL usp_get_player_quest_monsters(1);
#delete from active_quests;
#select * from active_quests;


/*==============================
	usp_create_bounty_monster_for_player
==============================*/

DROP PROCEDURE IF EXISTS usp_create_bounty_monster_for_player;

DELIMITER //
CREATE PROCEDURE usp_create_bounty_monster_for_player
(
	IN p_player_id SMALLINT,
    IN p_bounty_monster_id SMALLINT,
    IN p_xp INT,
    IN p_gold INT,
    IN p_drop_chance DECIMAL(4,3),
    IN p_time SMALLINT,
    IN p_strength SMALLINT,
    IN p_dexterity SMALLINT,
    IN p_intelligence SMALLINT,
    IN p_constitution SMALLINT,
    IN p_luck SMALLINT,
    IN p_strength_mult DECIMAL(4,3),
    IN p_dexterity_mult DECIMAL(4,3),
    IN p_intelligence_mult DECIMAL(4,3),
    IN p_constitution_mult DECIMAL(4,3),
    IN p_luck_mult DECIMAL(4,3)
)
BEGIN

	INSERT INTO active_bounties (player_id, bounty_monster_id, gold, xp, drop_chance, travel_time, strength, dexterity, intelligence, constitution, luck, strength_mult, dexterity_mult, intelligence_mult, constitution_mult, luck_mult) 
    VALUES (p_player_id, p_bounty_monster_id, p_gold, p_xp, p_drop_chance, p_time, p_strength, p_dexterity, p_intelligence, p_constitution, p_luck, p_strength_mult, p_dexterity_mult, p_intelligence_mult, p_constitution_mult, p_luck_mult);

END //
DELIMITER ;

#CALL usp_create_bounty_monster_for_player(1, 925);


/*==============================
	usp_get_player_bounty_monsters
==============================*/

DROP PROCEDURE IF EXISTS usp_get_player_bounty_monsters;

DELIMITER //
CREATE PROCEDURE usp_get_player_bounty_monsters
(
	IN p_player_id SMALLINT
)
BEGIN

	SELECT a.bounty_monster_id, b.monster_name, b.monster_suffix, b.region_name, b.class_name, b.file_name, a.gold, a.xp, a.drop_chance, a.travel_time, a.strength, a.dexterity, a.intelligence, a.constitution, a.luck
    FROM active_bounties a
    JOIN bounty_monsters b on a.bounty_monster_id = b.bounty_monster_id
	WHERE a.player_id = p_player_id;

END //
DELIMITER ;

#CALL usp_get_player_bounty_monsters(1);
#delete from active_bounties;
#select * from active_bounties;


/*==============================
	usp_get_player_info
==============================*/

DROP PROCEDURE IF EXISTS usp_get_player_info;

DELIMITER //
CREATE PROCEDURE usp_get_player_info
(
	IN p_player_id SMALLINT
)
BEGIN

	IF EXISTS (SELECT * FROM player_inventories WHERE player_id = p_player_id AND equipped = 1) THEN
		SELECT a.player_id, a.display_name AS name, a.class_name, a.file_name, a.player_level AS level, a.stamina, a.honor, a.gold, a.blessing, a.bounty_attempts, a.dungeon_attempts, a.arena_attempts,
			a.strength, a.dexterity, a.intelligence, a.constitution, a.luck, 
			SUM(b.strength) AS equip_strength, SUM(b.dexterity) AS equip_dexterity, SUM(b.intelligence) AS equip_intelligence, SUM(b.constitution) AS equip_constitution, SUM(b.luck) AS equip_luck, 
			SUM(b.damage) AS damage, SUM(b.armor) AS armor
		FROM players a
		LEFT JOIN player_inventories b on a.player_id = b.player_id
		WHERE a.player_id = p_player_id AND b.equipped = 1;
	ELSE
		SELECT player_id, display_name AS name, class_name, file_name, player_level AS level, stamina, honor, gold, blessing, bounty_attempts, dungeon_attempts, arena_attempts,
			strength, dexterity, intelligence, constitution, luck, 
			0 AS equip_strength, 0 AS equip_dexterity, 0 AS equip_intelligence, 0 AS equip_constitution, 0 AS equip_luck, 
			0 AS damage, 0 AS armor
		FROM players
		WHERE player_id = p_player_id;
	END IF;
    
END //
DELIMITER ;

#CALL usp_get_player_info(1);


/*==============================
	usp_get_player_base_stats
==============================*/

DROP PROCEDURE IF EXISTS usp_get_player_base_stats;

DELIMITER //
CREATE PROCEDURE usp_get_player_base_stats
(
	IN p_player_id SMALLINT
)
BEGIN

	SELECT player_id, gold, strength, dexterity, intelligence, constitution, luck
	FROM players
	WHERE player_id = p_player_id;
    
END //
DELIMITER ;

#CALL usp_get_player_base_stats(1);


/*==============================
	usp_get_quest_monster_info
==============================*/

DROP PROCEDURE IF EXISTS usp_get_quest_monster_info;

DELIMITER //
CREATE PROCEDURE usp_get_quest_monster_info
(
	IN p_player_id SMALLINT,
    IN p_quest_monster_id SMALLINT
)
BEGIN

	SELECT b.monster_name AS name, b.class_name, b.file_name, a.gold, a.xp, a.stamina, a.strength_mult, a.dexterity_mult, a.intelligence_mult, a.constitution_mult, a.luck_mult
	FROM active_quests a
	INNER JOIN quest_monsters b on a.quest_monster_id = b.quest_monster_id
	WHERE a.quest_monster_id = p_quest_monster_id AND a.player_id = p_player_id;

END //
DELIMITER ;

#CALL usp_get_quest_monster_info(1,4);


/*==============================
	usp_get_bounty_monster_info
==============================*/

DROP PROCEDURE IF EXISTS usp_get_bounty_monster_info;

DELIMITER //
CREATE PROCEDURE usp_get_bounty_monster_info
(
	IN p_player_id SMALLINT,
    IN p_bounty_monster_id SMALLINT
)
BEGIN

	SELECT b.monster_name AS name, b.class_name, b.file_name, a.gold, a.xp, a.drop_chance, a.strength_mult, a.dexterity_mult, a.intelligence_mult, a.constitution_mult, a.luck_mult
	FROM active_bounties a
	INNER JOIN bounty_monsters b on a.bounty_monster_id = b.bounty_monster_id
	WHERE a.bounty_monster_id = p_bounty_monster_id AND a.player_id = p_player_id;

END //
DELIMITER ;

#CALL usp_get_quest_monster_info(1,4);


/*==============================
	usp_give_player_quest_rewards
==============================*/

DROP PROCEDURE IF EXISTS usp_give_player_quest_rewards;

DELIMITER //
CREATE PROCEDURE usp_give_player_quest_rewards
(
	IN p_player_id SMALLINT,
    IN p_stamina TINYINT,
    IN p_gold INT,
    IN p_xp INT,
    IN p_monster_id SMALLINT,
    IN p_battle_log VARCHAR(16000)
)
BEGIN

	DECLARE v_exp_until_level INT;

	DELETE FROM active_quests WHERE player_id = p_player_id;

	UPDATE players
    SET stamina = stamina - p_stamina, gold = gold + p_gold, exp_until_level = exp_until_level - p_xp, quests_finished = quests_finished + 1, gold_collected = gold_collected + p_gold
    WHERE player_id = p_player_id;

	INSERT INTO mail (player_id , opponent_id, event_type, is_player_winner, event_date, battle_log) 
	VALUES (p_player_id, p_monster_id, 'quest', (SELECT CASE WHEN p_gold > 0 THEN 1 ELSE 0 END), NOW(), p_battle_log);

	SET v_exp_until_level = (
		SELECT exp_until_level 
		FROM players 
		WHERE player_id = p_player_id
    );
    
    IF v_exp_until_level <= 0 THEN CALL usp_player_level_up(p_player_id);
    END IF;
    
    SELECT player_level
    FROM players
    WHERE player_id = p_player_id;
    
END //
DELIMITER ;

#CALL usp_give_player_quest_rewards(1, 4, 20, 126);


/*==============================
	usp_give_player_bounty_rewards
==============================*/

DROP PROCEDURE IF EXISTS usp_give_player_bounty_rewards;

DELIMITER //
CREATE PROCEDURE usp_give_player_bounty_rewards
(
	IN p_player_id SMALLINT,
    IN p_stamina TINYINT,
    IN p_gold INT,
    IN p_xp INT,
	IN p_monster_id SMALLINT,
    IN p_battle_log VARCHAR(16000)
)
BEGIN

	DECLARE v_exp_until_level INT;

	DELETE FROM active_bounties WHERE player_id = p_player_id;

	UPDATE players
    SET bounty_attempts = bounty_attempts - 1, gold = gold + p_gold, exp_until_level = exp_until_level - p_xp, bounties_finished = bounties_finished + 1, gold_collected = gold_collected + p_gold
    WHERE player_id = p_player_id;

	INSERT INTO mail (player_id , opponent_id, event_type, is_player_winner, event_date, battle_log) 
	VALUES (p_player_id, p_monster_id, 'bounty', (SELECT CASE WHEN p_gold > 0 THEN 1 ELSE 0 END), NOW(), p_battle_log);

	SET v_exp_until_level = (
		SELECT exp_until_level 
		FROM players 
		WHERE player_id = p_player_id
    );
    
    IF v_exp_until_level <= 0 THEN CALL usp_player_level_up(p_player_id);
    END IF;
    
    SELECT player_level
    FROM players
    WHERE player_id = p_player_id;
    
END //
DELIMITER ;

#CALL usp_give_player_bounty_rewards(1, 4, 20, 126);


/*==============================
	usp_give_player_dungeon_rewards
==============================*/

DROP PROCEDURE IF EXISTS usp_give_player_dungeon_rewards;

DELIMITER //
CREATE PROCEDURE usp_give_player_dungeon_rewards
(
	IN p_player_id SMALLINT,
    IN p_stamina TINYINT,
    IN p_gold INT,
    IN p_xp INT,
    IN p_dungeon_tier TINYINT,
    IN p_battle_log VARCHAR(16000)
)
BEGIN

	DECLARE v_exp_until_level INT;

	SET @s = CONCAT('UPDATE player_dungeons SET dungeon_tier_', p_dungeon_tier, '_floor = dungeon_tier_', p_dungeon_tier, '_floor + 1 WHERE player_id = ', p_player_id, ';');

	PREPARE stmt FROM @s;
    
	IF (p_gold > 0 AND p_xp > 0) THEN EXECUTE stmt;
    END IF;

	UPDATE players
    SET dungeon_attempts = dungeon_attempts - 1, gold = gold + p_gold, exp_until_level = exp_until_level - p_xp, gold_collected = gold_collected + p_gold
    WHERE player_id = p_player_id;
    
    SET @s = CONCAT('INSERT INTO mail (player_id , opponent_id, event_type, is_player_winner, event_date, battle_log) VALUES (',p_player_id,
    ',(SELECT dungeon_monster_id FROM dungeon_monsters WHERE dungeon_tier = ',p_dungeon_tier,' AND dungeon_floor = (SELECT dungeon_tier_',p_dungeon_tier,'_floor FROM player_dungeons WHERE player_id = ',p_player_id,') - (SELECT CASE WHEN ',p_gold,' > 0 THEN 1 ELSE 0 END) )',
    ', "dungeon", (SELECT CASE WHEN ',p_gold,' > 0 THEN 1 ELSE 0 END), NOW(), "',p_battle_log,'");'
    );

	PREPARE stmt FROM @s;
    
	EXECUTE stmt;

	SET v_exp_until_level = (
		SELECT exp_until_level 
		FROM players 
		WHERE player_id = p_player_id
    );
    
    IF v_exp_until_level <= 0 THEN CALL usp_player_level_up(p_player_id);
    END IF;
    
    SELECT player_level
    FROM players
    WHERE player_id = p_player_id;
    
END //
DELIMITER ;

#CALL usp_give_player_dungeon_rewards(1, 4, 20, 126,'ddd',2);


/*==============================
	usp_player_level_up
==============================*/

DROP PROCEDURE IF EXISTS usp_player_level_up;

DELIMITER //
CREATE PROCEDURE usp_player_level_up
(
	IN p_player_id SMALLINT
)
BEGIN

	UPDATE players
    SET player_level = LEAST(player_level + 1, 100), exp_until_level = (SELECT cost FROM level_up_costs WHERE level = LEAST(player_level + 1, 100)) - exp_until_level
    WHERE player_id = p_player_id;

END //
DELIMITER ;

#CALL usp_player_level_up(1);


/*==============================
	usp_leaderboard_get_highest_level
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_level;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_level
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.display_name, a.class_name, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.player_level DESC, a.honor DESC
		LIMIT 100
    ) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_level(1);


/*==============================
	usp_leaderboard_get_highest_honor
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_honor;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_honor
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.display_name, a.class_name, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.honor DESC, a.player_level DESC
		LIMIT 100
    ) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_honor(1);


/*==============================
	usp_leaderboard_get_highest_arena_wins
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_arena_wins;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_arena_wins
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.display_name, a.class_name, a.arena_wins, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.arena_wins DESC, a.player_level DESC, a.honor DESC
		LIMIT 100
    ) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_arena_wins(1);


/*==============================
	usp_leaderboard_get_highest_arena_losses
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_arena_losses;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_arena_losses
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.display_name, a.class_name, a.arena_losses, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.arena_losses DESC, a.player_level DESC, a.honor DESC
		LIMIT 100
    ) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_arena_losses(1);


/*==============================
	usp_leaderboard_get_highest_quests_finished
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_quests_finished;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_quests_finished
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.display_name, a.class_name, a.quests_finished, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.quests_finished DESC, a.player_level DESC, a.honor DESC
		LIMIT 100
    ) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_quests_finished(1);


/*==============================
	usp_leaderboard_get_highest_bounties_finished
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_bounties_finished;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_bounties_finished
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.display_name, a.class_name, a.bounties_finished, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.bounties_finished DESC, a.player_level DESC, a.honor DESC
		LIMIT 100
    ) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_bounties_finished(1);


/*==============================
	usp_leaderboard_get_highest_gold_collected
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_gold_collected;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_gold_collected
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.display_name, a.class_name, a.gold_collected, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.gold_collected DESC, a.player_level DESC, a.honor DESC
		LIMIT 100
	) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_gold_collected(1);


/*==============================
	usp_leaderboard_get_highest_items_collected
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_items_collected;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_items_collected
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.display_name, a.class_name, a.items_collected, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.items_collected DESC, a.player_level DESC, a.honor DESC
		LIMIT 100
    ) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_items_collected(1);


/*==============================
	usp_leaderboard_get_highest_legendary_collected
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_legendary_collected;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_legendary_collected
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.display_name, a.class_name, a.legendary_collected, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.legendary_collected DESC, a.player_level DESC, a.honor DESC
		LIMIT 100
    ) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_legendary_collected(1);


/*==============================
	usp_leaderboard_get_highest_mythic_collected
==============================*/

DROP PROCEDURE IF EXISTS usp_leaderboard_get_highest_mythic_collected;

DELIMITER //
CREATE PROCEDURE usp_leaderboard_get_highest_mythic_collected
(
	IN p_season SMALLINT
)
BEGIN

	SET @player_rank = 0;

	SELECT (@player_rank := @player_rank + 1) AS player_rank, a.* FROM (
		SELECT a.player_id, a.display_name, a.class_name, a.mythic_collected, a.player_level, a.honor,
		(a.strength + SUM(IFNULL(b.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(b.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(b.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(b.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(b.luck,0))) AS luck
		FROM players a
		LEFT JOIN player_inventories b ON a.player_id = b.player_id AND IFNULL(b.equipped,1) = 1
		WHERE a.character_season = p_season AND a.has_character = 1
		GROUP BY a.player_id
		ORDER BY a.mythic_collected DESC, a.player_level DESC, a.honor DESC
		LIMIT 100
    ) AS a;

END //
DELIMITER ;

#CALL usp_leaderboard_get_highest_mythic_collected(1);


/*==============================
	usp_create_arena_opponents
==============================*/

DROP PROCEDURE IF EXISTS usp_create_arena_opponents;

DELIMITER //
CREATE PROCEDURE usp_create_arena_opponents
(
	IN p_player_id SMALLINT
)
BEGIN

	DECLARE v_honor INT;
    DECLARE v_season INT;
    
    SET v_honor = (
		SELECT honor
        FROM players
        WHERE player_id = p_player_id
    );
    
    SET v_season = (
		SELECT character_season
        FROM players
        WHERE player_id = p_player_id
    );

	INSERT INTO arena_opponents
	(SELECT p_player_id, player_id FROM players WHERE honor >= v_honor AND player_id <> p_player_id AND character_season = v_season AND has_character = 1 ORDER BY honor ASC LIMIT 2)
	UNION
	(SELECT p_player_id, player_id FROM players WHERE honor < v_honor AND player_id <> p_player_id AND character_season = v_season AND has_character = 1 ORDER BY honor DESC LIMIT 2);

END //
DELIMITER ;

#CALL usp_create_arena_opponents(1);


/*==============================
	usp_get_arena_opponents
==============================*/

DROP PROCEDURE IF EXISTS usp_get_arena_opponents;

DELIMITER //
CREATE PROCEDURE usp_get_arena_opponents
(
	IN p_player_id SMALLINT
)
BEGIN

	SELECT a.player_id, a.display_name, a.class_name, a.file_name, a.player_level, a.honor,
    (a.strength + SUM(IFNULL(c.strength,0))) AS strength, (a.dexterity + SUM(IFNULL(c.dexterity,0))) AS dexterity, (a.intelligence + SUM(IFNULL(c.intelligence,0))) AS intelligence, (a.constitution + SUM(IFNULL(c.constitution,0))) AS constitution, (a.luck + SUM(IFNULL(c.luck,0))) AS luck,
    SUM(IFNULL(c.damage,0)) AS damage, SUM(IFNULL(c.armor,0)) AS armor
	FROM players a
    INNER JOIN arena_opponents b ON b.opponent_id = a.player_id
	LEFT OUTER JOIN player_inventories c ON b.opponent_id  = c.player_id
	WHERE b.player_id = p_player_id AND IFNULL(c.equipped,1) = 1
    GROUP BY a.player_id;

END //
DELIMITER ;

#CALL usp_get_arena_opponents(4);


/*==============================
	usp_process_arena_honor
==============================*/

DROP PROCEDURE IF EXISTS usp_process_arena_honor;

DELIMITER //
CREATE PROCEDURE usp_process_arena_honor
(
	IN p_player_id SMALLINT,
    IN p_winner_id SMALLINT,
    IN p_loser_id SMALLINT,
    IN p_battle_log VARCHAR(16000)
)
BEGIN

	DECLARE v_winner_honor INT;
    DECLARE v_loser_honor INT;
    
    SET v_winner_honor = (SELECT honor FROM players WHERE player_id = p_winner_id);
    SET v_loser_honor = (SELECT honor FROM players WHERE player_id = p_loser_id);

	UPDATE players
    SET arena_attempts = arena_attempts - 1,
    arena_wins = arena_wins + CASE WHEN p_player_id = p_winner_id THEN 1 ELSE 0 END,
    arena_losses = arena_losses + CASE WHEN p_player_id = p_winner_id THEN 0 ELSE 1 END,
    honor = honor + CASE
		WHEN p_player_id = p_winner_id AND honor < v_loser_honor THEN 8
        WHEN p_player_id = p_winner_id AND honor >= v_loser_honor THEN 6
        WHEN p_player_id = p_loser_id AND honor < v_winner_honor THEN -8
        WHEN p_player_id = p_loser_id AND honor >= v_winner_honor THEN -10
        END
    WHERE player_id = p_player_id;
    
    IF p_player_id = p_winner_id THEN
		INSERT INTO mail (player_id , opponent_id, event_type, is_player_winner, event_date, battle_log) 
		VALUES (p_winner_id, p_loser_id, 'arena', 1, NOW(), p_battle_log);
	ELSE
		INSERT INTO mail (player_id , opponent_id, event_type, is_player_winner, event_date, battle_log) 
		VALUES (p_loser_id, p_winner_id, 'arena', 0, NOW(), p_battle_log);
	END IF;
    
    DELETE FROM arena_opponents
    WHERE player_id = p_player_id;

END //
DELIMITER ;

#CALL usp_process_arena_honor(1, 4, 1);


/*==============================
	usp_get_player_mail
==============================*/

DROP PROCEDURE IF EXISTS usp_get_player_mail;

DELIMITER //
CREATE PROCEDURE usp_get_player_mail
(
	IN p_player_id SMALLINT,
    IN p_event_type VARCHAR(20)
)
BEGIN

	SELECT 
		(SELECT display_name FROM players WHERE player_id = p_player_id) AS player_name,
        (SELECT CASE
			WHEN p_event_type = 'arena' THEN (SELECT display_name FROM players WHERE player_id = CASE WHEN p_player_id = a.player_id THEN a.opponent_id ELSE a.player_id END) 
            WHEN p_event_type = 'dungeon' THEN (SELECT monster_name FROM dungeon_monsters WHERE dungeon_monster_id = a.opponent_id)
            WHEN p_event_type = 'quest' THEN (SELECT monster_name FROM quest_monsters WHERE quest_monster_id = a.opponent_id)
            WHEN p_event_type = 'bounty' THEN (SELECT monster_name FROM bounty_monsters WHERE bounty_monster_id = a.opponent_id)
		END) AS opponent_name, 
        event_type, 
        CASE WHEN (p_player_id = player_id AND is_player_winner = 1) OR (p_player_id = opponent_id AND is_player_winner = 0) THEN 1 ELSE 0 END AS is_player_winner, 
        event_date, 
        battle_log
    FROM mail a
    WHERE (a.player_id = p_player_id or a.opponent_id = p_player_id) AND a.event_type = p_event_type
    ORDER BY mail_id DESC
    LIMIT 10;

END //
DELIMITER ;
/*
select * from mail
delete from mail
update players set arena_attempts = 20
*/
#CALL usp_get_player_mail(2);

/*==============================
	usp_get_player_dungeon_info
==============================*/

DROP PROCEDURE IF EXISTS usp_get_player_dungeon_info;

DELIMITER //
CREATE PROCEDURE usp_get_player_dungeon_info
(
	IN p_player_id SMALLINT
)
BEGIN

	(SELECT a.* FROM dungeon_monsters a INNER JOIN player_dungeons b ON a.dungeon_floor = b.dungeon_tier_1_floor WHERE a.dungeon_tier = 1 AND b.player_id = p_player_id)
    UNION
    (SELECT a.* FROM dungeon_monsters a INNER JOIN player_dungeons b ON a.dungeon_floor = b.dungeon_tier_2_floor WHERE a.dungeon_tier = 2 AND b.player_id = p_player_id)
    UNION
    (SELECT a.* FROM dungeon_monsters a INNER JOIN player_dungeons b ON a.dungeon_floor = b.dungeon_tier_3_floor WHERE a.dungeon_tier = 3 AND b.player_id = p_player_id)
    UNION
    (SELECT a.* FROM dungeon_monsters a INNER JOIN player_dungeons b ON a.dungeon_floor = b.dungeon_tier_4_floor WHERE a.dungeon_tier = 4 AND b.player_id = p_player_id);

END //
DELIMITER ;

#CALL usp_get_player_dungeon_info(4);

/*==============================
	usp_get_dungeon_monster_info
==============================*/

DROP PROCEDURE IF EXISTS usp_get_dungeon_monster_info;

DELIMITER //
CREATE PROCEDURE usp_get_dungeon_monster_info
(
	IN p_player_id SMALLINT,
    IN p_tier_id TINYINT
)
BEGIN

	SET @s = CONCAT(
		'SELECT a.*, a.monster_level AS level, a.monster_name AS name ',
        'FROM dungeon_monsters a ',
        'INNER JOIN player_dungeons b ON a.dungeon_floor = b.dungeon_tier_', p_tier_id, '_floor ',
        'WHERE a.dungeon_tier = ', p_tier_id, ' AND b.player_id = ', p_player_id, ';');

	PREPARE stmt FROM @s;
	EXECUTE stmt;

END //
DELIMITER ;

#CALL usp_get_dungeon_monster_info(4,2);


/*==============================
	usp_get_mythic_feed
==============================*/

DROP PROCEDURE IF EXISTS usp_get_mythic_feed;

DELIMITER //
CREATE PROCEDURE usp_get_mythic_feed ()
BEGIN
	
    SELECT b.display_name, c.item_name, c.file_name, a.item_level, a.rarity_name, d.prefix, a.strength, a.dexterity, a.intelligence, a.constitution, a.luck, a.damage, a.armor, a.time_dropped
    FROM mythic_feed a
    INNER JOIN players b ON b.player_id = a.player_id
    INNER JOIN items c ON c.item_id = a.item_id
    INNER JOIN item_prefixes d ON d.item_prefix_id = a.item_prefix_id
    ORDER BY a.time_dropped DESC
    LIMIT 10;

END //
DELIMITER ;

#CALL usp_get_mythic_feed();