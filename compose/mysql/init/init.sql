-- Alter user 'admin'@'%' IDENTIFIED WITH mysql_native_password BY '1qazxsw2#$';
ALTER USER 'admin'@'%' IDENTIFIED WITH caching_sha2_password BY '1qazxsw2#$';
GRANT ALL PRIVILEGES ON gameplatform.* TO 'admin'@'%';
FLUSH PRIVILEGES;
