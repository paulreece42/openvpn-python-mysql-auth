#Quickstart - CentOS6 with EPEL

    yum --enablerepo=epel install openvpn easy-rsa

    cd /usr/share/easy-rsa/2.0
    nano -w vars

Fill in the options as appropriate

    source vars
    ./clean-all
    ./build-ca
    ./build-dh
    ./build-key-server `hostname`
    ./build-key client
    mkdir /etc/openvpn/keys
    cp -arv dh2048.pem /etc/openvpn/keys/
    cp -arv client.crt /etc/openvpn/keys/
    cp -arv client.key /etc/openvpn/keys/
    cp -arv `hostname`.crt /etc/openvpn/keys/
    cp -arv `hostname`.key /etc/openvpn/keys/
    cp -arv ca.crt /etc/openvpn/keys/    


Done with keys, now setup OpenVPN as normal but change the auth config:


    script-security 3
    username-as-common-name
    auth-user-pass-verify /etc/openvpn/scripts/auth.py via-env
    client-connect /etc/openvpn/scripts/connect.py 
    client-disconnect /etc/openvpn/scripts/disconnect.py

Now make the DB:

    create database openvpn;

And import:

     mysql openvpn < openvpn.sql

And add the grants as needed:


    grant select on users to authuser@localhost identified by 'password';
    grant insert,select on failures to authuser@localhost identified by 'password';
    grant insert,update,select,delete on users to adminuser@localhost identified by 'password';
    grant insert,update,select on user_info to adminuser@localhost identified by 'password';
    grant select,insert on log to loguser@localhost identified by 'password';
    grant update (tx_bytes,rx_bytes,exit_signal,end_time) on log to loguser@localhost identified by 'password';

