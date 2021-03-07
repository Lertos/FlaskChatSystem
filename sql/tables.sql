USE flasksimplerpg;

/*==============================
	players
==============================*/

DROP TABLE IF EXISTS players;

CREATE TABLE players
(
	player_id SMALLINT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    display_name VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(30) NOT NULL,
    has_character TINYINT DEFAULT 0,
    class_name VARCHAR(30) NULL,
    file_name VARCHAR(30) NULL,
    player_level SMALLINT DEFAULT 1,
    exp_until_level SMALLINT DEFAULT 0,
	strength SMALLINT DEFAULT 1,
    dexterity SMALLINT DEFAULT 1,
    intelligence SMALLINT DEFAULT 1,
    constitution SMALLINT DEFAULT 1,
    luck SMALLINT DEFAULT 1,
    gold INT DEFAULT 5,
    stamina SMALLINT DEFAULT 100,
    honor SMALLINT DEFAULT 100,
    blessing VARCHAR(10) NULL,
    bounty_attempts TINYINT DEFAULT 3,
    dungeon_attempts TINYINT DEFAULT 3,
    arena_attempts TINYINT DEFAULT 3,
    wood_tier_1 SMALLINT DEFAULT 0,
    wood_tier_2 SMALLINT DEFAULT 0,
    wood_tier_3 SMALLINT DEFAULT 0,
    wood_tier_4 SMALLINT DEFAULT 0,
    mine_tier_1 SMALLINT DEFAULT 0,
    mine_tier_2 SMALLINT DEFAULT 0,
    mine_tier_3 SMALLINT DEFAULT 0,
    mine_tier_4 SMALLINT DEFAULT 0,
    dig_tier_1 SMALLINT DEFAULT 0,
    dig_tier_2 SMALLINT DEFAULT 0,
    dig_tier_3 SMALLINT DEFAULT 0,
    dig_tier_4 SMALLINT DEFAULT 0,
    inventory_space SMALLINT DEFAULT 7,
    players_killed SMALLINT DEFAULT 0,
    monsters_killed SMALLINT DEFAULT 0,
    gold_collected INT DEFAULT 5,
	quests_done SMALLINT DEFAULT 0,
    PRIMARY KEY (player_id)
);

INSERT INTO players (username,display_name,password) VALUES ('lertos','Lertos','lertos');
#SELECT * FROM players;