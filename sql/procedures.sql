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
        
        SELECT username, display_name
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

#CALL usp_create_user_account('lertos2','Lertos2','lertos2');

/*==============================
	usp_get_dashboard_details
==============================*/

DROP PROCEDURE IF EXISTS usp_get_dashboard_details;

DELIMITER //
CREATE PROCEDURE usp_get_dashboard_details
(
	IN p_username VARCHAR(30)
)
BEGIN
	SELECT display_name, class_name, file_name, player_level, exp_until_level, strength, dexterity, intelligence,
		constitution, luck, gold, stamina, honor, inventory_space
	FROM players
	WHERE username = p_username;
END //
DELIMITER ;

#CALL usp_get_dashboard_details('lertos');