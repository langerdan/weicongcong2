#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : Mysql_Connector_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : August 22 2016

import mysql.connector
from mysql.connector import errorcode

# CONFIG AREA
mysql_config_example = {
	'user': 'username',
	'password': 'password',
	'host': '127.0.0.1',
	'raise_on_warnings': True
}

db_name_example = 'database'


class MysqlConnector(object):
	def __init__(self, config, db_name):
		self.cnx = None
		self.connect(config)
		# needs to be buffered to use .fetch* methods, .rowcount attribute ...
		self.cursor = self.cnx.cursor(buffered=True)
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

	def insert(self, i_grammar, data):
		"""
		add_employee = ("INSERT INTO employees "
						"(first_name, last_name, hire_date, gender, birth_date) "
						"VALUES (%s, %s, %s, %s, %s)")
		data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))
		# Insert new employee
		cursor.execute(add_employee, data_employee)
		emp_no = cursor.lastrowid

		add_salary = ("INSERT INTO salaries "
						"(emp_no, salary, from_date, to_date) "
						"VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")
		data_salary = {
			'emp_no': emp_no,
			'salary': 50000,
			'from_date': tomorrow,
			'to_date': date(9999, 1, 1),
		}
		# Insert salary information
		cursor.execute(add_salary, data_salary)
		# Make sure data is committed to the database
		cnx.commit()
		"""

		print "=>Insert item ... ",
		try:
			self.cursor.execute(i_grammar, data)
		except mysql.connector.errors.IntegrityError, e:
			if e.errno == 1062:
				print "PASS! %s" % e
			else:
				raise
		else:
			print "Done!"
		self.cnx.commit()

	def query(self, q_grammar, data):
		self.cursor.execute(q_grammar, data)
		return self.cursor

	def done(self):
		self.cursor.close()
		self.cnx.close()
