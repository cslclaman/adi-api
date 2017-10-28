# -*- coding: utf-8 -*-

import mysql.connector as MySQL

USER = 'localuser'
PASS = 'ms987654'
HOST = 'localhost'
DB = 'adi6_db'

global cursor

def connect():
    con = MySQL.connect(user=USER, password=PASS, host=HOST, database=DB)
