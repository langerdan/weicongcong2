#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : Mysql_Connector_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : August 22 2016

import mysql


class MysqlConnector(object):
    def __int__(self, config, db_name):
        self.connect(config)
        self.cursor = self.cnx.cursor()
        self.select_db(db_name)

    def connect(self, config):
        try:
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "username or password incorrect!"
            else:
                print err

    def select_db(self, db_name):
        try:
            print "=>Select DB: %s" % db_name,
            self.cnx.database = db_name
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                try:
                    print "Failed: %s" % err.msg
                    print "=>Creating database: %s" % db_name,
                    self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
                except mysql.connector.Error as err:
                    print "=>Failed: %s" % err
                    exit(1)
                else:
                    print "OK!"
                self.cnx.database = db_name
            else:
                print(err.msg)
                exit(1)
        else:
            print "OK!"

    def insert(self, data_form, data):
        print "=>Insert item ... ",
        try:
            self.cursor.execute(data_form, data)
        except mysql.connector.errors.IntegrityError, e:
            if e.errno == 1062:
                print "PASS! %s" % e
            else:
                raise
        else:
            print "Done!"
        self.cnx.commit()

    def done(self):
        self.cursor.close()
        self.cnx.close()
