USE flasksimplerpg;

/*==============================
	USERS table
==============================*/

DROP TABLE users;

CREATE TABLE users (
    username VARCHAR(20) NOT NULL UNIQUE,
    displayName VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(30) NOT NULL,
    hasCharacter TINYINT DEFAULT 0,
    className VARCHAR(30) NULL,
    avatarName VARCHAR(30) NULL,
    playerLevel INT DEFAULT 1,
    expUntilLevel INT DEFAULT 50,
	baseStrength INT DEFAULT 10,
    baseDexterity INT DEFAULT 10,
    baseIntelligence INT DEFAULT 10,
    baseConstitution INT DEFAULT 10,
    baseLuck INT DEFAULT 10,
    gold INT DEFAULT 5,
    stamina INT DEFAULT 100,
    inventorySpace INT DEFAULT 12,
    playersKilled INT DEFAULT 0,
    monstersKilled INT DEFAULT 0,
    goldCollected INT DEFAULT 20,
	questsDone INT DEFAULT 0,
    PRIMARY KEY (username)
);

INSERT INTO users (username,displayName,password) VALUES ('lertos','Lertos','lertos');

SELECT * FROM users;

DROP PROCEDURE CreateUserAccount;

# PROC - ACCOUNT CREATION
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

CALL CreateUserAccount('lertos2','Lertos2','lertos2');

DROP PROCEDURE GetDashboardDetails;

# PROC - DASHBOARD DETAILS
DELIMITER //

CREATE PROCEDURE GetDashboardDetails(
	IN pUsername VARCHAR(30)
)
BEGIN
	SELECT displayName, className, avatarName, playerLevel, expUntilLevel, baseStrength, baseDexterity, baseIntelligence,
		baseConstitution, baseLuck, gold, stamina, inventorySpace, playersKilled, monstersKilled, goldCollected, questsDone
	FROM users
	WHERE username = pUsername;
END //

DELIMITER ;

CALL GetDashboardDetails('lertos');