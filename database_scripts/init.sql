SET GLOBAL general_log = ON;
SET GLOBAL general_log_file='/var/log/mysql/mysql.log';
SET GLOBAL log_output = 'file';

USE server_db;

/* Creating 1 table */

CREATE TABLE Messages (
    message_id int NOT NULL AUTO_INCREMENT,
    sender_name varchar(40),
    message_text varchar(140),
    message_time timestamp,
    PRIMARY KEY (message_id)
);