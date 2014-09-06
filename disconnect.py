#!/usr/bin/python
#
# https://github.com/paulreece42/openvpn-python-mysql-auth
#
# This program is the one that OpenVPN calls after the user
# disconnects. It goes back and updates the values in the
# previous record for that user
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

c.execute("""update log set end_time=now(), rx_bytes=%s, tx_bytes=%s where username=%s and end_time is null order by start_time desc limit 1""", (os.environ['bytes_received'], os.environ['bytes_sent'], os.environ['username']))

db.commit()

c.close()
db.close()

