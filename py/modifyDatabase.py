#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : modifyDatabase
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 16 2016
# VERSION : v0.0.1a

import os
import re
import argparse
from datetime import datetime
from argparse import RawTextHelpFormatter

from base import print_colors
from config import mysql_config
from database_connector import MysqlConnector


def format_sql(s, option='where'):
    if option == 'where':
        if re.search('=', s):
            c = ' AND '.join([re.sub('(?<==)(.+?)(?:,|$)', '%s', x) for x in s.split(',')])
        elif re.search('LIKE', s):
            c = ' AND '.join([re.sub('(?<= LIKE )(.+?)(?:,|$)', '%s', x) for x in s.split(',')])
        else:
            raise Exception("[FORMAT_SQL] syntax error: no '=' or 'LIKE' ")
        return c
    elif option == 'set':
        return re.sub('(?<==)(.+?)(?=,|$)', '%s', s)
    else:
        raise Exception('[FORMAT_SQL] Unknown option: %s' % option)


def update():
    data = re.findall('=(.+?)(?:,|$)', args.sub) + re.findall('(?:=| LIKE )(.+?)(?:,|$)', args.match)
    sql_format = [args.table, format_sql(args.sub, 'set'), format_sql(args.match)]
    sql_query = "UPDATE {0:s} SET {1:s} WHERE {2:s} ".format(*sql_format)
    print print_colors("• UPDATE ", 'red') + print_colors(("%s %s ..." % (sql_query, data))[7:], 'yellow'),
    start = datetime.now()
    cursor = m_con.query(sql_query, data)
    print print_colors("OK!", 'green')
    print print_colors("------------------\n  %d rows affected(%fs)" % (cursor.rowcount, (datetime.now() - start).total_seconds()))


def delete():
    data = re.findall('=(.+?)(?:,|$)', args.match)
    sql_format = [args.table, format_sql(args.match)]
    sql_query = "DELETE FROM {0:s} WHERE {1:s} ".format(*sql_format)
    print print_colors("• DELETE ", 'red') + print_colors(("%s %s ..." % (sql_query, data))[7:], 'yellow'),
    start = datetime.now()
    cursor = m_con.query(sql_query, data)
    print print_colors("OK!", 'green')
    print print_colors("------------------\n  %d rows affected(%fs)" % (cursor.rowcount, (datetime.now() - start).total_seconds()))


def extract():
    data = re.findall('=(.+?)(?:,|$)', args.match)
    sql_format = [args.table, format_sql(args.match)]
    sql_query = "SELECT * FROM {0:s} WHERE {1:s}".format(*sql_format)
    print print_colors("• SELECT ", 'red') + print_colors(("%s %s ..." % (sql_query, data))[7:], 'yellow'),
    start = datetime.now()
    cursor = m_con.query(sql_query, data)
    print print_colors("OK!", 'green')
    print print_colors("------------------\n  %d rows affected(%fs)" % (cursor.rowcount, (datetime.now() - start).total_seconds()))
    if args.include_id:
        col_names = cursor.column_names
        results = cursor.fetchall()
    else:
        col_names = cursor.column_names[1:]
        results = [x[1:] for x in cursor.fetchall()]
    i_g = "INSERT INTO {0:s} ({1:s}) VALUES ({2:s})".format(args.table_b, ','.join(col_names), ','.join(['%s' for x in col_names]))
    print print_colors("• INSERT ", 'red') + print_colors(("%s [%d rows] ..." % (i_g, len(results)))[7:], 'yellow'),
    start = datetime.now()
    m_con.cursor.executemany(i_g, results)
    print print_colors("OK!", 'green')
    print print_colors("------------------\n  %d rows affected(%fs)" % (m_con.cursor.rowcount, (datetime.now() - start).total_seconds()))

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='modify_database', formatter_class=RawTextHelpFormatter,
                                     description="Modify Database:\n"
                                                 "1. update 'B1' with 'B2' if match 'A';\n"
                                                 "2. delete some rows if match 'A';\n"
                                                 "3. extract some rows if match 'A' from X to Y;")

    parser.add_argument('db_name', type=str, help='Database name')
    parser.add_argument('table', type=str, help='Table name')
    parser.add_argument('-u', '--username', type=str, help='Username for database')
    parser.add_argument('-p', '--password', type=str, help='Password for database')

    subparsers = parser.add_subparsers(help='Modify database with different method')

    parser_a = subparsers.add_parser('update', help='Update')
    parser_a.add_argument('match', metavar='COL_A=VALUE,COL_B=VALUE', type=str, help='Specifying criteria for a match condition')
    parser_a.add_argument('sub', metavar='COL_A=VALUE,COL_B=VALUE', type=str, help='Specifying criteria for substitution')
    parser_a.add_argument('-c', '--commit', action='store_true', help='commit after query/execute')
    parser_a.set_defaults(func=update)

    parser_b = subparsers.add_parser('delete', help='Delete')
    parser_b.add_argument('match', metavar='COL_A=VALUE,COL_B=VALUE', type=str, help='Specifying criteria for a match condition')
    parser_b.add_argument('-c', '--commit', action='store_true', help='commit after query/execute')
    parser_b.set_defaults(func=delete)

    parser_c = subparsers.add_parser('extract', help='Extract')
    parser_c.add_argument('match', metavar='COL_A=VALUE,COL_B=VALUE', type=str, help='Specifying criteria for a match condition')
    parser_c.add_argument('table_b', type=str, help='Table name which data copy to')
    parser_c.add_argument('-ii', '--include_id', action='store_true', help='insert include `id`')
    parser_c.add_argument('-c', '--commit', action='store_true', help='commit after query/execute')
    parser_c.set_defaults(func=extract)

    args = parser.parse_args()

    if args.username is not None:
        mysql_config['user'] = args.username
    if args.password is not None:
        mysql_config['password'] = args.password

    m_con = MysqlConnector(mysql_config, args.db_name)
    args.func()
    if args.commit:
        m_con.cnx.commit()
    m_con.done()