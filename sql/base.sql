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
    PRIMARY KEY (id)
);

ALTER TABLE users AUTO_INCREMENT = 1;
SELECT * FROM users;

INSERT INTO users (username,displayName,password) VALUES ('dee','Lertos','dee123');
INSERT INTO users (username,displayName,password) VALUES ('dee2','Lertos2','dee1234');
INSERT INTO users (username,displayName,password) VALUES ('dee3','Lertos3','dee1234');

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