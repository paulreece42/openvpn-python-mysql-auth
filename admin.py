#!/usr/bin/python
#
# https://github.com/paulreece42/openvpn-python-mysql-auth
#
# Admin, add remove users etc
#
# Never developed a CLI before. I just hope to not be
# as bad as MegaCLI...
#

from passlib.hash import pbkdf2_sha512
import MySQLdb
import MySQLdb.cursors 
import os, sys, ConfigParser
from optparse import OptionParser
import random, string

# Stolen from http://stackoverflow.com/questions/7479442/high-quality-simple-random-password-generator
length = 13
chars = string.ascii_letters + string.digits + '!@#$%^&*()'
random.seed = (os.urandom(1024))

randpass = ''.join(random.choice(chars) for i in range(length))

config = ConfigParser.ConfigParser()
config.read('config.cfg')

DATABASE = config.get('Database', 'Database')
HOST = config.get('Database', 'Host')
PORT = config.getint('Database', 'Port')
AUTH_PASSWD = config.get('AdminUser', 'Password')
AUTH_USER = config.get('AdminUser', 'Username')


parser = OptionParser()
parser.add_option("-a", "--action", dest="action", type="string",
                  help="action. Should be one of add, edit, delete, show, resetpass")
parser.add_option("-u", "--user", dest="user", type="string",
                  help="username")

(options, args) = parser.parse_args()

db=MySQLdb.connect(host=HOST,port=PORT,passwd=AUTH_PASSWD,db=DATABASE,user=AUTH_USER,cursorclass=MySQLdb.cursors.DictCursor)

c=db.cursor()

if options.action == "add":
    hash = pbkdf2_sha512.encrypt(randpass)
    c.execute("""INSERT INTO users VALUES (%s, %s, 1, now(), now(), '0000-00-00 00:00:00')""", (options.user,hash))
    print """User: %s
Pass: %s""" % (options.user, randpass)

if options.action == "delete":
    c.execute("""DELETE FROM users WHERE username = %s""", (options.user))

if options.action == "edit":
    print """Not implemented yet, try mysql"""

if options.action == "resetpass":
    hash = pbkdf2_sha512.encrypt(randpass)
    c.execute("""UPDATE users SET password = %s WHERE username = %s""", (hash, options.user))
    print """User: %s
Pass: %s""" % (options.user, randpass)

if options.action == "show":
    c.execute("""SELECT * FROM users""")

db.commit()
c.close()
db.close()
