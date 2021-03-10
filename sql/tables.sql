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


/*==============================
	classes
==============================*/

DROP TABLE IF EXISTS classes;

CREATE TABLE classes
(
    class_name VARCHAR(20) NOT NULL UNIQUE,
    stat VARCHAR(20) NOT NULL,
    weapons TINYINT NOT NULL,
    uses_two_handed TINYINT NOT NULL,
    uses_shield TINYINT NOT NULL,
    max_armor_reduction DECIMAL(4,3) NOT NULL,
    health_modifier DECIMAL(4,3) NOT NULL,
	PRIMARY KEY (class_name)
);

INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Warrior', 'str', 1, 0, 1, 0.6, 3.5);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Berserker', 'str', 1, 0, 0, 0.45, 2.8);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Magic Knight', 'str', 1, 0, 0, 0.5, 3.0);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Fencer', 'str', 1, 0, 0, 0.4, 2.7);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Scout', 'dex', 1, 1, 0, 0.3, 2.3);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Rogue', 'dex', 2, 0, 0, 0.2, 1.8);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Demon Hunter', 'dex', 1, 1, 0, 0.35, 2.3);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Assassin', 'dex', 1, 0, 0, 0.2, 1.8);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Frost Mage', 'int', 1, 1, 0, 0.2, 2.0);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Fire Mage', 'int', 1, 1, 0, 0.15, 1.7);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Blood Mage', 'int', 1, 1, 0, 0.15, 1.8);
INSERT INTO classes (class_name,stat,weapons,uses_two_handed,uses_shield,max_armor_reduction,health_modifier) VALUES ('Dark Mage', 'int', 1, 1, 0, 0.15, 1.9);

#SELECT * FROM classes;


/*==============================
	item_types
==============================*/

DROP TABLE IF EXISTS item_types;

CREATE TABLE item_types
(
	item_type_id SMALLINT NOT NULL AUTO_INCREMENT,
	is_weapon TINYINT NOT NULL,
    armor_type TINYINT NOT NULL,
    item_type_name VARCHAR(20) NOT NULL,
    is_two_handed TINYINT NOT NULL,
    stat VARCHAR(3) NOT NULL,
    damage_multiplier DECIMAL(4,3) NOT NULL,
    armor_per_level TINYINT NOT NULL,
    stats_per_level TINYINT NOT NULL,
    PRIMARY KEY (item_type_id)
);

INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 1, 'Helmet', 0, 'int', 1, 1, 8);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 2, 'Helmet', 0, 'dex', 1, 3, 7);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 3, 'Helmet', 0, 'str', 1, 6, 6);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 1, 'Chestplate', 0, 'int', 1, 2, 12);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 2, 'Chestplate', 0, 'dex', 1, 5, 11);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 3, 'Chestplate', 0, 'str', 1, 8, 10);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 1, 'Legs', 0, 'int', 1, 2, 10);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 2, 'Legs', 0, 'dex', 1, 4, 9);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 3, 'Legs', 0, 'str', 1, 7, 8);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 1, 'Gloves', 0, 'int', 1, 1, 5);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 2, 'Gloves', 0, 'dex', 1, 2, 4);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 3, 'Gloves', 0, 'str', 1, 3, 3);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 1, 'Boots', 0, 'int', 1, 1, 5);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 2, 'Boots', 0, 'dex', 1, 2, 5);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (0, 3, 'Boots', 0, 'str', 1, 3, 5);

INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Sword', 0, 'str', 1, 1, 7);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Axe', 0, 'str', 1, 1, 7);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Claws', 0, 'dex', 1.2, 1, 7);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Maul', 0, 'str', 1, 1, 7);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Hammer', 0, 'str', 1, 1, 7);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Spear', 0, 'dex', 1.2, 1, 7);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Shield', 0, 'str', 1, 1, 7);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Staff', 1, 'int', 1.5, 1, 14);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Book', 1, 'int', 1.5, 1, 14);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Bow', 1, 'dex', 1.2, 1, 14);
INSERT INTO item_types (is_weapon,armor_type,item_type_name,is_two_handed,stat,damage_multiplier,armor_per_level,stats_per_level) VALUES (1, 0, 'Crossbow', 1, 'dex', 1.2, 1, 14);

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

#INSERT INTO items (username,display_name,password) VALUES ('lertos','Lertos','lertos');
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

INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Common', 0.6, 1.0, 'borderCommon');
INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Uncommon', 0.3, 1.05, 'borderUncommon');
INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Rare', 0.08, 1.1, 'borderRare');
INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Legendary', 0.01, 1.15, 'borderLegendary');
INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Mythic', 0.005, 1.2, 'borderMythic');
INSERT INTO item_rarities (rarity_name,drop_chance,multiplier,css_class_name) VALUES ('Unique', 0.005, 1.15, 'borderUnique');

#SELECT * FROM item_rarities;


/*==============================
	item_prefixes
==============================*/

DROP TABLE IF EXISTS item_prefixes;

CREATE TABLE item_prefixes
(
	item_prefix_id SMALLINT NOT NULL AUTO_INCREMENT,
    item_type_id SMALLINT NULL,
    prefix VARCHAR(20) NOT NULL,
    strength_multiplier DECIMAL(4,3) DEFAULT 1.000,
    dexterity_multiplier DECIMAL(4,3) DEFAULT 1.000,
    intelligence_multiplier DECIMAL(4,3) DEFAULT 1.000,
    constitution_multiplier DECIMAL(4,3) DEFAULT 1.000,
    luck_multiplier DECIMAL(4,3) DEFAULT 1.000,
    PRIMARY KEY (item_prefix_id)
);

INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (1, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (2, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (3, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (4, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (5, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (6, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (7, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (8, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (9, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (10, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (11, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (12, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (13, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (14, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (15, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (16, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (17, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (18, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (19, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (20, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (21, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (22, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (23, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (24, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (25, 'Rusty', 1, 1, 1, 1, 1);
INSERT INTO item_prefixes (item_type_id,prefix,strength_multiplier,dexterity_multiplier,intelligence_multiplier,constitution_multiplier,luck_multiplier) VALUES (26, 'Rusty', 1, 1, 1, 1, 1);

#SELECT * FROM item_prefixes;


/*==============================
	player_inventories
==============================*/

DROP TABLE IF EXISTS player_inventories;

CREATE TABLE player_inventories
(
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
    sell_price SMALLINT NOT NULL
);

#SELECT * FROM player_inventories;


/*==============================
	house_items
==============================*/

DROP TABLE IF EXISTS house_items;

CREATE TABLE house_items
(
	house_item_id SMALLINT NOT NULL UNIQUE AUTO_INCREMENT,
    item_name VARCHAR(30) NOT NULL,
    item_level SMALLINT NOT NULL,
    bonus DECIMAL(6,3) NOT NULL,
    is_bonus_percentage TINYINT NOT NULL,
    cost_gold SMALLINT NOT NULL,
    cost_wood_tier_1 SMALLINT NOT NULL,
    cost_wood_tier_2 SMALLINT NOT NULL,
    cost_wood_tier_3 SMALLINT NOT NULL,
    cost_wood_tier_4 SMALLINT NOT NULL,
    cost_mine_tier_1 SMALLINT NOT NULL,
    cost_mine_tier_2 SMALLINT NOT NULL,
    cost_mine_tier_3 SMALLINT NOT NULL,
    cost_mine_tier_4 SMALLINT NOT NULL,
    cost_dig_tier_1 SMALLINT NOT NULL,
    cost_dig_tier_2 SMALLINT NOT NULL,
    cost_dig_tier_3 SMALLINT NOT NULL,
    cost_dig_tier_4 SMALLINT NOT NULL,
    PRIMARY KEY (house_item_id)
);

INSERT INTO house_items (item_name,item_level,bonus,is_bonus_percentage,cost_gold,cost_wood_tier_1,cost_wood_tier_2,cost_wood_tier_3,cost_wood_tier_4,cost_mine_tier_1,cost_mine_tier_2,cost_mine_tier_3,cost_mine_tier_4,cost_dig_tier_1,cost_dig_tier_2,cost_dig_tier_3,cost_dig_tier_4) VALUES ('Hatchet', 1, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO house_items (item_name,item_level,bonus,is_bonus_percentage,cost_gold,cost_wood_tier_1,cost_wood_tier_2,cost_wood_tier_3,cost_wood_tier_4,cost_mine_tier_1,cost_mine_tier_2,cost_mine_tier_3,cost_mine_tier_4,cost_dig_tier_1,cost_dig_tier_2,cost_dig_tier_3,cost_dig_tier_4) VALUES ('Pickaxe', 1, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO house_items (item_name,item_level,bonus,is_bonus_percentage,cost_gold,cost_wood_tier_1,cost_wood_tier_2,cost_wood_tier_3,cost_wood_tier_4,cost_mine_tier_1,cost_mine_tier_2,cost_mine_tier_3,cost_mine_tier_4,cost_dig_tier_1,cost_dig_tier_2,cost_dig_tier_3,cost_dig_tier_4) VALUES ('Shovel', 1, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO house_items (item_name,item_level,bonus,is_bonus_percentage,cost_gold,cost_wood_tier_1,cost_wood_tier_2,cost_wood_tier_3,cost_wood_tier_4,cost_mine_tier_1,cost_mine_tier_2,cost_mine_tier_3,cost_mine_tier_4,cost_dig_tier_1,cost_dig_tier_2,cost_dig_tier_3,cost_dig_tier_4) VALUES ('Fortune', 1, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO house_items (item_name,item_level,bonus,is_bonus_percentage,cost_gold,cost_wood_tier_1,cost_wood_tier_2,cost_wood_tier_3,cost_wood_tier_4,cost_mine_tier_1,cost_mine_tier_2,cost_mine_tier_3,cost_mine_tier_4,cost_dig_tier_1,cost_dig_tier_2,cost_dig_tier_3,cost_dig_tier_4) VALUES ('Knowledge', 1, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO house_items (item_name,item_level,bonus,is_bonus_percentage,cost_gold,cost_wood_tier_1,cost_wood_tier_2,cost_wood_tier_3,cost_wood_tier_4,cost_mine_tier_1,cost_mine_tier_2,cost_mine_tier_3,cost_mine_tier_4,cost_dig_tier_1,cost_dig_tier_2,cost_dig_tier_3,cost_dig_tier_4) VALUES ('Chance', 1, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO house_items (item_name,item_level,bonus,is_bonus_percentage,cost_gold,cost_wood_tier_1,cost_wood_tier_2,cost_wood_tier_3,cost_wood_tier_4,cost_mine_tier_1,cost_mine_tier_2,cost_mine_tier_3,cost_mine_tier_4,cost_dig_tier_1,cost_dig_tier_2,cost_dig_tier_3,cost_dig_tier_4) VALUES ('Haste', 1, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO house_items (item_name,item_level,bonus,is_bonus_percentage,cost_gold,cost_wood_tier_1,cost_wood_tier_2,cost_wood_tier_3,cost_wood_tier_4,cost_mine_tier_1,cost_mine_tier_2,cost_mine_tier_3,cost_mine_tier_4,cost_dig_tier_1,cost_dig_tier_2,cost_dig_tier_3,cost_dig_tier_4) VALUES ('Persuasion', 1, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO house_items (item_name,item_level,bonus,is_bonus_percentage,cost_gold,cost_wood_tier_1,cost_wood_tier_2,cost_wood_tier_3,cost_wood_tier_4,cost_mine_tier_1,cost_mine_tier_2,cost_mine_tier_3,cost_mine_tier_4,cost_dig_tier_1,cost_dig_tier_2,cost_dig_tier_3,cost_dig_tier_4) VALUES ('Holding', 1, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

#SELECT * FROM house_items;


/*==============================
	player_houses
==============================*/

DROP TABLE IF EXISTS player_houses;

CREATE TABLE player_houses
(
	player_id SMALLINT NOT NULL UNIQUE,
    strength SMALLINT NOT NULL DEFAULT 1,
    dexterity SMALLINT NOT NULL DEFAULT 1,
    intelligence SMALLINT NOT NULL DEFAULT 1,
    constitution SMALLINT NOT NULL DEFAULT 1,
    luck SMALLINT NOT NULL DEFAULT 1,
    hatchet SMALLINT NOT NULL DEFAULT 1,
    pickaxe SMALLINT NOT NULL DEFAULT 1,
    shovel SMALLINT NOT NULL DEFAULT 1,
    fortune SMALLINT NOT NULL DEFAULT 1,
    knowledge SMALLINT NOT NULL DEFAULT 1,
    chance SMALLINT NOT NULL DEFAULT 1,
    haste SMALLINT NOT NULL DEFAULT 1,
    persuasion SMALLINT NOT NULL DEFAULT 1,
    holding SMALLINT NOT NULL DEFAULT 1
);

#SELECT * FROM player_houses;


/*==============================
	arena_opponents
==============================*/

DROP TABLE IF EXISTS arena_opponents;

CREATE TABLE arena_opponents
(
	player_id SMALLINT NOT NULL UNIQUE,
    opponent_id_1 SMALLINT,
    opponent_id_2 SMALLINT,
    opponent_id_3 SMALLINT,
    opponent_id_4 SMALLINT
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

INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Grizzly Bear','Berserker','bear.png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Bogard','Warrior','bogard.png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Kree','Rogue','bug (1).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Pincee','Assassin','bug (2).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Gorbol','Fencer','bug (3).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Arkny','Demon Hunter','bug (4).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Swilly','Magic Knight','bug (5).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Garner','Dark Mage','bug (6).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Bourner','Fire Mage','bug (7).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Saucie','Blood Mage','bug (8).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Klayrie','Scout','bug (9).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Blobber','Dark Mage','bug (10).png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Morphie','Magic Knight','cat.png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Evil Clucker','Fencer','chicken.png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Crocodile','Berserker','crocodile.png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Crow','Assassin','crow.png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Ice Golem','Frost Mage','crystal_golem.png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Cursed Doll','Dark Mage','cursed_doll.png');
INSERT INTO quest_monsters (monster_name,class_name,file_name) VALUES ('Cyclops','Warrior','cyclop.png');

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
    luck SMALLINT NOT NULL
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

INSERT INTO bounty_monsters (monster_name,monster_suffix,region_name,class_name,file_name) VALUES ('Delrath','The Devious','The Deserted Desert','Assassin','delrath.png');

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
    luck SMALLINT NOT NULL
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
    gold SMALLINT NOT NULL,
    xp SMALLINT NOT NULL,
    drop_chance DECIMAL(4,3) NOT NULL,
    item_drop_level SMALLINT NOT NULL,
    strength SMALLINT NOT NULL,
    dexterity SMALLINT NOT NULL,
    intelligence SMALLINT NOT NULL,
    constitution SMALLINT NOT NULL,
    luck SMALLINT NOT NULL,
    PRIMARY KEY (dungeon_monster_id)
);

INSERT INTO dungeon_monsters (dungeon_tier,dungeon_floor,monster_name,class_name,file_name,gold,xp,drop_chance,item_drop_level,strength,dexterity,intelligence,constitution,luck) VALUES (1, 1, 'Blaze', 'Fire Mage', 'blaze.png',20, 300, 0.45, 5, 10, 15, 30, 20, 10);

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
	unlocked_gather_nodes
==============================*/

DROP TABLE IF EXISTS unlocked_gather_nodes;

CREATE TABLE unlocked_gather_nodes
(
    player_id SMALLINT NOT NULL UNIQUE,
    wood_tier_2 TINYINT DEFAULT 0,
    wood_tier_3 TINYINT DEFAULT 0,
    wood_tier_4 TINYINT DEFAULT 0,
    mine_tier_2 TINYINT DEFAULT 0,
    mine_tier_3 TINYINT DEFAULT 0,
    mine_tier_4 TINYINT DEFAULT 0,
    dig_tier_2 TINYINT DEFAULT 0,
    dig_tier_3 TINYINT DEFAULT 0,
    dig_tier_4 TINYINT DEFAULT 0
);

#SELECT * FROM unlocked_gather_nodes;
