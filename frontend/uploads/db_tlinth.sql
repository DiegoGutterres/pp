CREATE DATABASE db_tlinth;
USE db_tlinth;

CREATE TABLE req_user(
	id INT PRIMARY KEY AUTO_INCREMENT,
    modes VARCHAR(12),
    quantity_req INT
);

CREATE TABLE res_user(
	id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT, 
    response VARCHAR(640),
    FOREIGN KEY (user_id) REFERENCES req_user(id)
);

insert into req_user (modes, quantity_req) 
values('qr ca nd', 3);

select * from req_user;
select * from res_user;

insert into res_user(response, user_id)
values('-dfkiaospfkaf', 1);