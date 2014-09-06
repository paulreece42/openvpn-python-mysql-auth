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
config.read('config.cfg')

DATABASE = config.get('Database', 'Database')
HOST = config.get('Database', 'Host')
PORT = config.getint('Database', 'Port')
AUTH_PASSWD = config.get('AuthUser', 'Password')
AUTH_USER = config.get('AuthUser', 'Username')


db=MySQLdb.connect(host=HOST,port=PORT,passwd=AUTH_PASSWD,db=DATABASE,user=AUTH_USER,cursorclass=MySQLdb.cursors.DictCursor)

#hash = pbkdf2_sha512.encrypt(os.environ['password'])
c=db.cursor()


c.execute("""SELECT count(*) AS failures FROM failures WHERE remote_ip = %s AND time > (NOW() - INTERVAL 15 MINUTE)""", (os.environ['untrusted_ip']))

# I put this before it tries to pull the password, because it's harder to try SQL injecting with an IP address
if c.fetchone()['failures'] > 5:
    print """Too many failed password attempts for IP %s, failing""" % (os.environ['untrusted_ip'])
    sys.exit(1)


c.execute("""SELECT * FROM users WHERE username = %s""", (os.environ['username']))

success=0

try:
    if pbkdf2_sha512.verify(os.environ['password'], c.fetchone()['password']):
        print "logged in"
        success=1
    else:
        print "wrong username or password"
        success=0
except:
    print "other error"
    sys.exit(1)


if success==1:
    sys.exit(0)
else:
    c.execute("""INSERT INTO failues (username, time, remote_ip, local_ip) VALUES (%s, now(), %s, %s)""", (os.environ['username'], os.environ['untrusted_ip'], '127.0.0.1'))
    db.commit()
    sys.exit(1)


c.close()
db.close()
