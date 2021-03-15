USE flasksimplerpg;

/*==============================
	usp_create_user_account
==============================*/

DROP PROCEDURE IF EXISTS usp_create_user_account;

DELIMITER //
CREATE PROCEDURE usp_create_user_account(
	IN p_username VARCHAR(30),
    IN p_display_name VARCHAR(30),
    IN p_password VARCHAR(30)
)
BEGIN
	IF NOT EXISTS (SELECT * FROM players WHERE username = p_username or display_name = p_display_name) THEN
		INSERT INTO players (username, display_name, password)
		VALUES (p_username, p_display_name, p_password);
        
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

#CALL usp_create_user_account('lertos99','lertos99','lertos99');

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
	SELECT display_name, class_name, file_name, player_level, exp_until_level, strength, dexterity, intelligence,
		constitution, luck, gold, stamina, honor, inventory_space
	FROM players
	WHERE player_id = p_player_id;
END //
DELIMITER ;

#CALL usp_get_dashboard_details(1);


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
    
END //
DELIMITER ;

#CALL usp_create_new_item(1, 20, 1, 1, 'Common', 10, 15, 20, 25, 30, 0, 45, 10);
#SELECT * FROM player_inventories;
