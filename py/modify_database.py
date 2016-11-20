#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : modify_database
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 16 2016
# VERSION : v0.0.1a

import os
import re
import time
import argparse
from argparse import RawTextHelpFormatter

from base import print_colors
from config import mysql_config
from database_connector import MysqlConnector


def format_sql(c):
        return re.sub('(?<=\=)(.+?)(?=,|$)', '%s', c)


def replace():
    data = re.findall('=(.+?)(?:,|$)', args.match) + re.findall('=(.+?)(?:,|$)', args.sub)
    sql_format = [args.table, re.sub('(?<=\=)(.+?)(?=,|$)', '%s', args.match), re.sub('(?<=\=)(.+?)(?=,|$)', '%s', args.sub)]
    sql_query = "UPDATE {0:s} SET {1:s} WHERE {2:s} ".format(*sql_format)
    print print_colors("• Update ") + print_colors("%s %s ... " % (sql_query, data), 'yellow'),
    start = int(round(time.time() * 1000))
    result = m_con.query(sql_query, data)
    print print_colors("OK!", 'green')
    print print_colors("------------------\n%d rows affected(%f)" % (result.rowcount, (int(round(time.time() * 1000)) - start)))
    #m_con.cnx.commit()


def delete():
    data = re.findall('=(.+?)(?:,|$)', args.match)
    sql_format = [args.table, re.sub('(?<=\=)(.+?)(?=,|$)', '%s', args.match)]
    sql_query = "DELETE FROM {0:s} WHERE {1:s} ".format(*sql_format)
    print print_colors("• Delete ") + print_colors("%s %s" % (sql_query, str(data)), 'yellow'),
    start = int(round(time.time() * 100))
    result = m_con.query(sql_query, data)
    print print_colors("OK!", 'green')
    print print_colors("------------------\n%d rows affected(%f)" % (result.rowcount, (int(round(time.time() * 100)) - start)))
    #m_con.cnx.commit()


def extract():
    print "incomplete"

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='modify_database', formatter_class=RawTextHelpFormatter,
                                     description="Modify Database:\n"
                                                 "1. replace 'B1' with 'B2' if match 'A';\n"
                                                 "2. delete some rows if match 'A';\n"
                                                 "3. extract some rows if match 'A' from X to Y;")

    parser.add_argument('db_name', type=str, help='Database name')
    parser.add_argument('table', type=str, help='Table name')
    parser.add_argument('-u', '--username', type=str, help='Username for database')
    parser.add_argument('-p', '--password', type=str, help='Password for database')

    subparsers = parser.add_subparsers(help='Modify database with different method')

    parser_a = subparsers.add_parser('replace', help='Replace')
    parser_a.add_argument('match', metavar='COL_A=VALUE,COL_B=VALUE', type=str, help='Specifying criteria for a match condition')
    parser_a.add_argument('sub', metavar='COL_A=VALUE,COL_B=VALUE', type=str, help='Specifying criteria for substitution')
    parser_a.set_defaults(func=replace)

    parser_b = subparsers.add_parser('delete', help='Delete')
    parser_b.add_argument('match', metavar='COL_A=VALUE,COL_B=VALUE', type=str, help='Specifying criteria for a match condition')
    parser_b.set_defaults(func=delete)

    parser_c = subparsers.add_parser('extract', help='Extract')
    parser_c.set_defaults(func=extract)

    args = parser.parse_args()

    m_con = MysqlConnector(mysql_config, args.db_name)
    args.func()
    m_con.done()