# -*- coding: utf-8 -*-
import control.dbconfig as dbconfig
import mysql.connector as MySQL

class Control:
    def __init__(self):
        self.con = None
        self.cursor = None

    def connect(self):
        self.con = MySQL.connect(user=dbconfig.user, password=dbconfig.password, host=dbconfig.host, database=dbconfig.database)
        self.cursor = self.con.cursor()

    def disconnect(self):
        self.cursor.close
        self.con.close()
