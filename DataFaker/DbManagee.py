#!/usr/bin/env python
# coding=utf-8
# author: Allen Guo
# 导入Config.py, MySql.py包，用来加载配置文件和连接数据库
import Config, MySql

# 连接数据库示例如下
# sql = MySql.MySQL('DATABASE')
# connect, cur = sql.connect()

# 执行sql语句示例如下：
# sql.sqlcmd(cur, "sql_statement") # 这里要将字符串“sql_statement”替换为你要执行的sql语句

class DbManagee():
      # 类构造方法，要传入sql连接实例，即sql = MySql.MySQL('DATABASE')
    def __init__(self,sql):
        self.connect,self.cur = sql.connect()
        self.setUp_statements = []
        self.tearDown_statements = []
      # 检查sql语句是否合法的内置函数，避免危险操作
    def isChecked(self,sql_string):
        '''该方法尚未编写，思路为用正则表达式检查语句合法性，避免删库等危险操作
        :param sql_string:
        :return: 检查是否合法
        '''
        return True

      # 将字典转换为创建表sql语句的内置工具方法
    def convertTableDict_toCreateTableStatement(self,TableHeaderDict,table_name,key_id="mykey_id"):
        '''
        :param TableHeaderDict: 数据库表的字典
        :param table_name: 要创建的表名称
        :param key_id: 表的主键名称，默认为"mykey_id"
        :return: sql建表语句
        '''
        create_table_prefix = '''create table if not exists '''+table_name+"("
        create_table_prefix += key_id+ '''int primary key not null auto_increment,'''
        create_table_statement = create_table_prefix
        for columTitle in TableHeaderDict.keys():
            create_table_statement += "\n" + columTitle + '  varchar(50)' + ","
        # close parentheses
        create_table_statement += "\n" + "additionalKey" + '  varchar(50)' + '' + ')'
        print("sql statement formed as: ",create_table_statement)
        return create_table_statement

      # 添加setUp的语句队列
    def add_setUp_statement(self,sql_string):
        if (self.isChecked(sql_string)):
            self.sql_statements.append(sql_string)

    def add_setUp_statement_fromList(self, sql_string_list):
        for sql_string in sql_string_list:
            if (self.isChecked(sql_string)):
                self.sql_statements.append(sql_string)

      # 添加tearDown的语句队列
    def add_tearDown_statement(self, sql_string):
        if (self.isChecked(sql_string)):
            self.tearDown_statements.append(sql_string)

    def add_tearDown_statement_fromList(self, sql_string_list):
        for sql_string in sql_string_list:
            if (self.isChecked(sql_string)):
                self.tearDown_statements.append(sql_string)

                      # 执行指定语句队列
    def excuteSqlList(self,sql_list):#设置
        if len(sql_list) <0:
              print("no statement found")
        else:
              for sql_statement in self.sql_list:
                    try:
                          self.sql.sqlcmd(self.cur, sql_statement)
                          self.sql.commit()
                    except Exception as e:
                          self.sql.rollback()
                          print("error sql excution:",sql_statement,e,)
    # 设置环境，执行setUp队列中的全部方法
    def setUpEnv(self):
        self.excuteSqlList(self.setUp_statements)

    # 清理环境，执行tearDown队列中的全部方法
    def clearEnv(self):
        self.excuteSqlList(self.tearDown_statements)

if __name__ == "__main__":
    # 工作流如下

    # step-1: 创建Dbmanagee与数据库链接实例
    my_db = DbManagee(MySql.MySQL('DATABASE'))

    # step-2: 准备setUp语句队列，clearDown语句队列
    statement_setup = [
        "select 8 from table_name",
        "select item from table_name"
    ]
    statement_cleardown = [
        "select 8 from table_name",
        "select item from table_name"
    ]

    # step-3: 准备setUp语句队列，clearDown语句队列
    my_db.add_setUp_statement_fromList(statement_setup)
    my_db.add_setUp_statement_fromList(statement_cleardown)

    # step-3-替代版: 上面为直接多条添加，这里为逐条添加
    # for sql in statement_setup:
    #     my_db.add_setUp_statement(sql)
    # for sql in statement_cleardown:
    #     my_db.add_tearDown_statement(sql)
    # my_db.setUpEnv()
    # my_db.clearEnv()

# step-4: 准备setUp语句队列，clearDown语句队列
    my_db.setUpEnv()
    my_db.clearEnv()

