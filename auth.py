#!/usr/bin/python
#
# https://github.com/paulreece42/openvpn-python-mysql-auth
#
# This program is the one that OpenVPN calls to authenticate
# the connecting user
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
    ip=os.environ['untrusted_ip']
except:
    pass

try:
    ip=os.environ['untrusted_ip6']
except:
    pass

DATABASE = config.get('Database', 'Database')
HOST = config.get('Database', 'Host')
PORT = config.getint('Database', 'Port')
AUTH_PASSWD = config.get('AuthUser', 'Password')
AUTH_USER = config.get('AuthUser', 'Username')

def failrecord():
    c.execute("""INSERT INTO failures (username, time, remote_ip, local_ip) VALUES (%s, now(), %s, %s)""", (os.environ['username'], ip, '127.0.0.1'))
    db.commit()
    c.close()
    db.close()
    sys.exit(1)


db=MySQLdb.connect(host=HOST,port=PORT,passwd=AUTH_PASSWD,db=DATABASE,user=AUTH_USER,cursorclass=MySQLdb.cursors.DictCursor)

c=db.cursor()


c.execute("""SELECT count(*) AS failures FROM failures WHERE remote_ip = %s AND time > (NOW() - INTERVAL 15 MINUTE)""", (ip))

# I put this before it tries to pull the password, because it's harder to try SQL injecting with an IP address
if c.fetchone()['failures'] > 5:
    print """Too many failed password attempts for IP %s, failing""" % (ip)
    failrecord()

success=0


try:
    c.execute("""SELECT * FROM users WHERE username = %s""", (os.environ['username']))
except:
    print "could not execute"


try:
    if pbkdf2_sha512.verify(os.environ['password'], c.fetchone()['password']):
        print "logged in"
        success=1
    else:
        print "wrong username or password"
        success=0
except:
    print "other error"
    failrecord()


if success==1:
    sys.exit(0)
else:
    failrecord()

c.close()
db.close()
