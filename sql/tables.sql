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
    character_season SMALLINT NOT NULL DEFAULT 1,
    player_level SMALLINT DEFAULT 1,
    exp_until_level INT DEFAULT 51,
	strength SMALLINT DEFAULT 10,
    dexterity SMALLINT DEFAULT 10,
    intelligence SMALLINT DEFAULT 10,
    constitution SMALLINT DEFAULT 10,
    luck SMALLINT DEFAULT 10,
    gold INT DEFAULT 25,
    stamina SMALLINT DEFAULT 100,
    honor SMALLINT DEFAULT 100,
    blessing VARCHAR(10) NULL,
    bounty_attempts TINYINT DEFAULT 3,
    dungeon_attempts TINYINT DEFAULT 5,
    arena_attempts TINYINT DEFAULT 10,
    arena_wins INT DEFAULT 0,
    arena_losses INT DEFAULT 0,
    quests_finished INT DEFAULT 0,
    bounties_finished INT DEFAULT 0,
    gold_collected INT DEFAULT 25,
	items_collected SMALLINT DEFAULT 0,
    legendary_collected SMALLINT DEFAULT 0,
    mythic_collected SMALLINT DEFAULT 0,
    PRIMARY KEY (player_id)
);

DELETE FROM player_inventories;
DELETE FROM player_dungeons;
DELETE FROM arena_opponents;
DELETE FROM active_quests;
DELETE FROM active_bounties;


/*==============================
	travel_info
==============================*/

DROP TABLE IF EXISTS travel_info;

CREATE TABLE travel_info
(
	player_id SMALLINT NOT NULL,
    type_of_event VARCHAR(16) NOT NULL,
    opponent_id SMALLINT NOT NULL,
    travel_time INT NULL,
    multiplier DECIMAL(5,3) NULL,
    drop_chance DECIMAL(4,3) NULL,
    dungeon_tier SMALLINT NULL,
    dungeon_floor SMALLINT NULL,
    level SMALLINT NULL,
    name VARCHAR(20) NULL,
	opponent_suffix VARCHAR(30) NULL,
    region_name VARCHAR(30) NULL,
    class_name VARCHAR(30) NULL,
    file_name VARCHAR(40) NULL,
    gold INT NULL,
    xp INT NULL,
    stamina SMALLINT NULL,
    honor SMALLINT NULL,
	strength SMALLINT NULL,
    dexterity SMALLINT NULL,
    intelligence SMALLINT NULL,
    constitution SMALLINT NULL,
    luck SMALLINT NULL,
    damage INT NULL,
    armor INT NULL,
    PRIMARY KEY (player_id)
);

#SELECT * FROM travel_info;


/*==============================
	seasons
==============================*/

DROP TABLE IF EXISTS seasons;

CREATE TABLE seasons
(
    season SMALLINT NOT NULL UNIQUE,
    start_date VARCHAR(40) NOT NULL,
	PRIMARY KEY (season)
);

#INSERT INTO seasons (season,start_date) VALUES (1, 'Mar-12-2021');


/*==============================
	mail
==============================*/

DROP TABLE IF EXISTS mail;

CREATE TABLE mail
(
    mail_id SMALLINT NOT NULL UNIQUE AUTO_INCREMENT,
    player_id SMALLINT NOT NULL,
    opponent_id SMALLINT NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    is_player_winner TINYINT NOT NULL,
    event_date DATETIME NOT NULL,
    battle_log VARCHAR(16000) NOT NULL,
	PRIMARY KEY (mail_id)
);

#INSERT INTO mail (player_id,opponent_id,event_type,is_player_winner,event_date,battle_log) VALUES (1,'Dee','Lee','arena',1,CURDATE(),'TURN1 lol TURN2 lol');


/*==============================
	classes
==============================*/

DROP TABLE IF EXISTS classes;

CREATE TABLE classes
(
    class_name VARCHAR(20) NOT NULL UNIQUE,
    stat VARCHAR(20) NOT NULL,
    uses_two_handed TINYINT NOT NULL,
    uses_shield TINYINT NOT NULL,
    max_armor_reduction DECIMAL(4,3) NOT NULL,
    max_crit_chance DECIMAL(4,3) NOT NULL,
    health_modifier DECIMAL(4,3) NOT NULL,
	PRIMARY KEY (class_name)
);

INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Warrior', 'str', 0, 1, 0.6, 0.3, 3.5);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Berserker', 'str', 0, 0, 0.45, 0.3, 2.8);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Magic Knight', 'str', 0, 0, 0.5, 0.3, 3.0);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Fencer', 'str', 0, 0, 0.4, 0.6, 2.7);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Scout', 'dex', 1, 0, 0.3, 0.3, 2.3);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Rogue', 'dex', 0, 0, 0.2, 0.3, 1.8);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Demon Hunter', 'dex', 1, 0, 0.35, 0.3, 2.3);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Assassin', 'dex', 0, 0, 0.2, 0.5, 1.8);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Frost Mage', 'int', 1, 0, 0.2, 0.3, 2.0);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Fire Mage', 'int', 1, 0, 0.15, 0.3, 1.7);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Blood Mage', 'int', 1, 0, 0.15, 0.3, 1.8);
INSERT INTO classes (class_name,stat,uses_two_handed,uses_shield,max_armor_reduction,max_crit_chance,health_modifier) VALUES ('Dark Mage', 'int', 1, 0, 0.15, 0.3, 1.9);

#SELECT * FROM classes;

/*==============================
	item_types
==============================*/

DROP TABLE IF EXISTS item_types;

CREATE TABLE item_types
(
	item_type_id SMALLINT NOT NULL AUTO_INCREMENT,
	is_weapon TINYINT NOT NULL,
    item_type_name VARCHAR(20) NOT NULL,
    is_two_handed TINYINT NOT NULL,
    stat VARCHAR(3) NOT NULL,
    damage_multiplier DECIMAL(4,3) NOT NULL,
    armor_per_level TINYINT NOT NULL,
    stats_per_level TINYINT NOT NULL,
    PRIMARY KEY (item_type_id)
);

#SELECT * FROM item_types;


/*==============================
	items
==============================*/

DROP TABLE IF EXISTS items;

CREATE TABLE items
(
	item_id SMALLINT NOT NULL AUTO_INCREMENT,
    item_type_id SMALLINT NOT NULL,
    item_name VARCHAR(40) NOT NULL,
    file_name VARCHAR(40) NOT NULL,
    PRIMARY KEY (item_id)
);

#SELECT * FROM items;


/*==============================
	item_rarities
==============================*/

DROP TABLE IF EXISTS item_rarities;

CREATE TABLE item_rarities
(
	rarity_name VARCHAR(20) NOT NULL UNIQUE,
    drop_chance DECIMAL(4,3) NOT NULL,
    multiplier DECIMAL(4,3) NOT NULL,
    css_class_name VARCHAR(30) NOT NULL,
    PRIMARY KEY (rarity_name)
);

INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Common', 0.6, 1.0, 'itemBorderCommon');
INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Uncommon', 0.3, 1.05, 'itemBorderUncommon');
INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Rare', 0.08, 1.1, 'itemBorderRare');
INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Legendary', 0.01, 1.15, 'itemBorderLegendary');
INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Mythic', 0.01, 1.2, 'itemBorderMythic');

#SELECT * FROM item_rarities;


/*==============================
	item_prefixes
==============================*/

DROP TABLE IF EXISTS item_prefixes;

CREATE TABLE item_prefixes
(
	item_prefix_id SMALLINT NOT NULL AUTO_INCREMENT,
    is_weapon TINYINT NULL,
    prefix VARCHAR(20) NOT NULL,
    damage_mult DECIMAL(4,3),
    armor_mult DECIMAL(4,3),
    strength_mult DECIMAL(4,3),
    dexterity_mult DECIMAL(4,3),
    intelligence_mult DECIMAL(4,3),
    constitution_mult DECIMAL(4,3),
    luck_mult DECIMAL(4,3),
    PRIMARY KEY (item_prefix_id)
);

#SELECT * FROM item_prefixes;


/*==============================
	player_inventories
==============================*/

DROP TABLE IF EXISTS player_inventories;

CREATE TABLE player_inventories
(
	inventory_item_id INT NOT NULL UNIQUE AUTO_INCREMENT,
	player_id SMALLINT NOT NULL,
    item_id SMALLINT NOT NULL,
    item_level SMALLINT NOT NULL,
    rarity_name VARCHAR(20) NOT NULL,
    item_prefix_id SMALLINT,
    equipped TINYINT NOT NULL,
    strength SMALLINT NOT NULL,
    dexterity SMALLINT NOT NULL,
    intelligence SMALLINT NOT NULL,
    constitution SMALLINT NOT NULL,
    luck SMALLINT NOT NULL,
	damage SMALLINT NOT NULL,
    armor SMALLINT NOT NULL,
    sell_price INT NOT NULL,
    PRIMARY KEY (inventory_item_id)
);

#SELECT * FROM player_inventories;


/*==============================
	arena_opponents
==============================*/

DROP TABLE IF EXISTS arena_opponents;

CREATE TABLE arena_opponents
(
	player_id SMALLINT NOT NULL,
    opponent_id SMALLINT NOT NULL
);

#SELECT * FROM arena_opponents;


/*==============================
	quest_monsters
==============================*/

DROP TABLE IF EXISTS quest_monsters;

CREATE TABLE quest_monsters
(
	quest_monster_id SMALLINT NOT NULL UNIQUE AUTO_INCREMENT,
    monster_name VARCHAR(30),
    class_name VARCHAR(20),
    file_name VARCHAR(40),
    PRIMARY KEY (quest_monster_id)
);

#SELECT * FROM quest_monsters;


/*==============================
	active_quests
==============================*/

DROP TABLE IF EXISTS active_quests;

CREATE TABLE active_quests
(
	player_id SMALLINT NOT NULL,
    quest_monster_id SMALLINT NOT NULL,
    gold SMALLINT NOT NULL,
    xp SMALLINT NOT NULL,
    stamina SMALLINT NOT NULL,
    travel_time SMALLINT NOT NULL,
    strength SMALLINT NOT NULL,
    dexterity SMALLINT NOT NULL,
    intelligence SMALLINT NOT NULL,
    constitution SMALLINT NOT NULL,
    luck SMALLINT NOT NULL,
    strength_mult DECIMAL(4,3) NOT NULL,
    dexterity_mult DECIMAL(4,3) NOT NULL,
    intelligence_mult DECIMAL(4,3) NOT NULL,
    constitution_mult DECIMAL(4,3) NOT NULL,
    luck_mult DECIMAL(4,3) NOT NULL
);

#SELECT * FROM active_quests;


/*==============================
	bounty_monsters
==============================*/

DROP TABLE IF EXISTS bounty_monsters;

CREATE TABLE bounty_monsters
(
	bounty_monster_id SMALLINT NOT NULL UNIQUE AUTO_INCREMENT,
    monster_name VARCHAR(20),
    monster_suffix VARCHAR(30),
    region_name VARCHAR(30),
    class_name VARCHAR(20),
    file_name VARCHAR(40),
    PRIMARY KEY (bounty_monster_id)
);

#SELECT * FROM bounty_monsters;


/*==============================
	active_bounties
==============================*/

DROP TABLE IF EXISTS active_bounties;

CREATE TABLE active_bounties
(
	player_id SMALLINT NOT NULL,
    bounty_monster_id SMALLINT NOT NULL,
    gold SMALLINT NOT NULL,
    xp SMALLINT NOT NULL,
    drop_chance DECIMAL(4,3) NOT NULL,
    travel_time SMALLINT NOT NULL,
    strength SMALLINT NOT NULL,
    dexterity SMALLINT NOT NULL,
    intelligence SMALLINT NOT NULL,
    constitution SMALLINT NOT NULL,
    luck SMALLINT NOT NULL,
	strength_mult DECIMAL(4,3) NOT NULL,
    dexterity_mult DECIMAL(4,3) NOT NULL,
    intelligence_mult DECIMAL(4,3) NOT NULL,
    constitution_mult DECIMAL(4,3) NOT NULL,
    luck_mult DECIMAL(4,3) NOT NULL
);

#SELECT * FROM active_bounties;


/*==============================
	dungeon_monsters
==============================*/

DROP TABLE IF EXISTS dungeon_monsters;

CREATE TABLE dungeon_monsters
(
    dungeon_monster_id SMALLINT NOT NULL UNIQUE AUTO_INCREMENT,
    dungeon_tier TINYINT NOT NULL,
    dungeon_floor TINYINT NOT NULL,
    monster_name VARCHAR(30) NOT NULL,
    class_name VARCHAR(20) NOT NULL,
    file_name VARCHAR(40) NOT NULL,
    monster_level SMALLINT NOT NULL,
    gold INT NOT NULL,
    xp INT NOT NULL,
    strength SMALLINT NOT NULL,
    dexterity SMALLINT NOT NULL,
    intelligence SMALLINT NOT NULL,
    constitution SMALLINT NOT NULL,
    luck SMALLINT NOT NULL,
    damage SMALLINT NOT NULL,
    armor SMALLINT NOT NULL,
    PRIMARY KEY (dungeon_monster_id)
);

#SELECT * FROM dungeon_monsters;


/*==============================
	player_dungeons
==============================*/

DROP TABLE IF EXISTS player_dungeons;

CREATE TABLE player_dungeons
(
    player_id SMALLINT NOT NULL UNIQUE,
    dungeon_tier_1_floor TINYINT DEFAULT 1,
    dungeon_tier_2_floor TINYINT DEFAULT 1,
    dungeon_tier_3_floor TINYINT DEFAULT 1,
    dungeon_tier_4_floor TINYINT DEFAULT 1
);

#SELECT * FROM player_dungeons;


/*==============================
	level_up_costs
==============================*/

DROP TABLE IF EXISTS level_up_costs;

CREATE TABLE level_up_costs
(
    level SMALLINT NOT NULL UNIQUE AUTO_INCREMENT,
    cost INT NOT NULL,
    PRIMARY KEY (level)
);

#SELECT * FROM level_up_costs;
#INSERT INTO level_up_costs (cost) VALUES ()


/*==============================
	mythic_feed
==============================*/

DROP TABLE IF EXISTS mythic_feed;

CREATE TABLE mythic_feed
(
	player_id SMALLINT NOT NULL,
    item_id SMALLINT NOT NULL,
    item_level SMALLINT NOT NULL,
    rarity_name VARCHAR(20) NOT NULL,
    item_prefix_id SMALLINT,
    strength SMALLINT NOT NULL,
    dexterity SMALLINT NOT NULL,
    intelligence SMALLINT NOT NULL,
    constitution SMALLINT NOT NULL,
    luck SMALLINT NOT NULL,
	damage SMALLINT NOT NULL,
    armor SMALLINT NOT NULL,
    time_dropped DATETIME NOT NULL
);

#SELECT * FROM mythic_feed;