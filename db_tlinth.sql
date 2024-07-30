CREATE DATABASE db_tlinth;
USE db_tlinth;


CREATE TABLE res_user(
	id INT PRIMARY KEY AUTO_INCREMENT,
	modes VARCHAR(120), 
    response TEXT,
    user_id VARCHAR(36) NOT NULL
);

insert into req_user (modes, quantity_req) 
values('qrcode arquivo camera numero', 3);

select * from res_user;

drop table res_user;		