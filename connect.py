#!/usr/bin/python
#
# https://github.com/paulreece42/openvpn-python-mysql-auth
#
# This program is the one that OpenVPN calls to record the
# start and put it in the logfile
#

from passlib.hash import pbkdf2_sha512
import MySQLdb
import MySQLdb.cursors 
import os, sys, ConfigParser

config = ConfigParser.ConfigParser()
config.read('/etc/openvpn/scripts/config.cfg')

# This is at least going to be ipv6-ready; I don't use ipv4 so that's less
# well tested...
try:
    ip=os.environ['trusted_ip']
except:
    pass

try:
    ip=os.environ['trusted_ip6']
except:
    pass

DATABASE = config.get('Database', 'Database')
HOST = config.get('Database', 'Host')
PORT = config.getint('Database', 'Port')
AUTH_PASSWD = config.get('LogUser', 'Password')
AUTH_USER = config.get('LogUser', 'Username')


db=MySQLdb.connect(host=HOST,port=PORT,passwd=AUTH_PASSWD,db=DATABASE,user=AUTH_USER,cursorclass=MySQLdb.cursors.DictCursor)

c=db.cursor()

c.execute("""insert into log (username,start_time,remote_ip,remote_port,local_ip) values(%s, now(), %s, %s, %s)""", (os.environ['username'], ip, os.environ['trusted_port'], os.environ['ifconfig_pool_remote_ip']))

db.commit()
c.close()
db.close()

