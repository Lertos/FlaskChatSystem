USE flasksimplerpg;

/*==============================
	USERS table
==============================*/

DROP TABLE users;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    displayName VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(30) NOT NULL,
    hasCharacter TINYINT DEFAULT 0,
    PRIMARY KEY (id)
);

ALTER TABLE users AUTO_INCREMENT = 1;

INSERT INTO users (username,displayName,password) VALUES ('lertos','lertos','lertos');
INSERT INTO users (username,displayName,password,hasCharacter) VALUES ('lertos2','lertos2','lertos2',1);

SELECT * FROM users;

DROP PROCEDURE CreateUserAccount;

DELIMITER //

CREATE PROCEDURE CreateUserAccount(
	IN pUsername VARCHAR(30),
    IN pDisplayName VARCHAR(30),
    IN pPassword VARCHAR(30)
)
BEGIN
	IF NOT EXISTS (SELECT * FROM users WHERE username = pUsername or displayname = pDisplayName) THEN
		INSERT INTO users (username, displayName, password)
		VALUES (pUsername, pDisplayName, pPassword);
        
        SELECT username, displayName
        FROM users
        WHERE username = pUsername;
	ELSE
		IF EXISTS (SELECT * FROM users WHERE username = pUsername) THEN
			SELECT '' AS username, displayName
            FROM users
            WHERE username = pUsername;
		ELSE
			SELECT username, '' AS displayName
            FROM users
            WHERE displayName = pDisplayName;
		END IF;
	END IF; 
	
    COMMIT;
END //

DELIMITER ;

CALL CreateUserAccount('de223432e','d21234323ee','1')