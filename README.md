openvpn-python-mysql-auth
=========================

Quick and easy wrapper script for openvpn authentication using Python, pbkdf2_sha512 hashed passwords, and prepared SQL statements

Don't use me yet, I'm in active development - will remove this when stable


grant select on users to authuser@localhost identified by 'password';
grant insert,select on failures to authuser@localhost identified by 'password';
grant insert,update,select,delete on users to adminuser@localhost identified by 'password';
grant insert,update,select on user_info to adminuser@localhost identified by 'password';
grant insert on log to loguser@localhost identified by 'password';
grant update (tx_bytes,rx_bytes,exit_signal,end_time) on log to loguser@localhost identified by 'password';

