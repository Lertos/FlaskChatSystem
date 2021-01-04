use flasksimplerpg;
create table users (id INT NOT NULL AUTO_INCREMENT , username VARCHAR(20), password VARCHAR(30), PRIMARY KEY(id));
alter table users AUTO_INCREMENT = 1;
select * from users;

insert into users values (7,'dee','pass123');
insert into users (username, password) values ('dee','pass123')