drop database dummy_db;
create database dummy_db;
use dummy_db;
create table dummy_table(hash varchar(64), num int);
insert into dummy_table values ('ola', 1);
select * from dummy_table;