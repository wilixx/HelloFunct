#!/usr/bin/env python
# coding=utf-8
# author: Allen Guo
import Config, MySql
sql = MySql.MySQL('DATABASE')
connect, cur = sql.connect()

class DbManagee():
      def __init__(self,sql):
            self.connect,self.cur = sql.connect()
            self.setUp_statements = []
            self.tearDown_statements = []

      def isChecked(self,sql_string):
            return False
      def convertTableDict_toCreateTableStatement(self,TableHeaderDict,table_name,key_id):
          create_table_prefix = '''create table if not exists '''+table_name+"("
          create_table_prefix += key_id+ '''int primary key not null auto_increment,'''
          create_table_statement = create_table_prefix
          for columTitle in TableHeaderDict.keys():
              create_table_statement += "\n" + columTitle + '  varchar(50)' + ","
          # close parentheses
          create_table_statement += "\n" + "additionalKey" + '  varchar(50)' + '' + ')'

          print("sql statement formed as: ",create_table_statement)
          return create_table_statement
      def add_setUp_statement(self,sql_string):
            if (self.isChecked(sql_string)):
                  self.sql_statements.append(sql_string)

      def add_tearDown_statement(self, sql_string):
            if (self.isChecked(sql_string)):
                  self.tearDown_statements.append(sql_string)

      def excuteSqlList(self,sql_list):#设置
            if len(sql_list) <0:
                  print("no statement found")
            else:
                  for sql_statement in self.sql_list:
                        try:
                              self.sql.sqlcmd(cur, sql_statement)
                              self.sql.commit()
                        except Exception as e:
                              self.sql.rollback()
                              print("error sql excution:",sql_statement,e,)
      def setUpEnv(self):
            self.excuteSqlList(self.setUp_statements)

      def clearEnv(self):
            self.excuteSqlList(self.tearDown_statements)

