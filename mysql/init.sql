SET GLOBAL general_log = ON;
SET GLOBAL general_log_file='/var/log/mysql/mysql.log';
SET GLOBAL log_output = 'file';

CREATE USER 'db_user'@'%' IDENTIFIED BY 'user-password';
GRANT ALL PRIVILEGES ON *.* TO 'db_user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
