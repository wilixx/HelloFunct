#!/usr/bin/env python
# coding=utf-8
# author: Allen Guo
import Config, MySql
'''
# 连接database，执行语句示例
sql = MySql.MySQL('DATABASE')
connect, cur = sql.connect()
sql.sqlcmd(cur, "sql_statement") # 这里要将字符串“sql_statement”替换为你要执行的sql语句
'''
class DbManagee():
    """ Database Managee Class
    Elements：
        setUp_statements,tearDown_statements,# 两组sql队列
    Methods：
        setUpEnv(): 执行设置环境sql队列
        clearEnv(): 执行清理环境sql队列
        isChecked(): 检查sql语句合法性
        convertTableDict_toCreateTableStatement(): 字典转建表sql
    """

    # 构造方法，参数为mysql连接实例
    def __init__(self,sql):
        self.sql = sql
        self.connect,self.cur = self.sql.connect()
        self.setUp_statements = []
        self.tearDown_statements = []

    # 检查sql语句合法性
    def isChecked(self,sql_string):
        '''该方法尚未编写
        :param sql_string:
        :return: 检查是否合法
        '''
        return True

    # 将字典转换为建表语句
    def convertTableDict_toCreateTableStatement(TableHeaderDict,table_name,key_id="mykey_id"):
        '''
        :param TableHeaderDict: 表头字典
        :param table_name: 表名称
        :param key_id: 主键名称
        :return: sql建表语句
        '''
        create_table_prefix = '''create table if not exists '''+table_name+"("
        create_table_prefix += key_id+ '''  int primary key not null auto_increment,'''
        create_table_statement = create_table_prefix
        for columTitle in TableHeaderDict.keys():
            create_table_statement += "\n" + columTitle + '  varchar(50)' + ","
        # close parentheses
        create_table_statement += "\n" + "additionalKey" + '  varchar(50)' + '' + ')'
        print("sql statement formed as: ",create_table_statement)
        return create_table_statement

    def insertSingleFakeRowsIntoTableStatement(TableHeaderDict, table_name):
        cmd_heads = r"INSERT INTO " + table_name + " ("
        cmd_tails = r" VALUES ("
        for columTile in TableHeaderDict.keys():
            cmd_heads += columTile + ','
            # cmd_tails += '' + r'"{' + columTile + r'}"' + '' + ','
            cmd_tails += '' + r'"' + "Fake-Data-Default" + r'"' + '' + ','

        cmd = cmd_heads[0:-1] + ") " + cmd_tails[0:-1] + ");"
        return cmd
            #     try:
            #         self.sql.sqlcmd(self.cur, cmd)
            #         # print("execute insert ok")
            #         self.connect.commit()
            #     except Exception as e:
            #         print(cmd, e)
            #         self.connect.rollback()
            #         print("error")
            # print("inserted {} raws into table {}".format(volume,table_name))

    def insertFakeRowsIntoTableStatement(self,TableHeaderDict,table_name,volume):
        cmd_heads = r"INSERT INTO " + table_name + " ("
        cmd_tails = r" VALUES ("
        for columTile in TableHeaderDict.keys():
            cmd_heads += columTile + ','
            # cmd_tails += '' + r'"{' + columTile + r'}"' + '' + ','
            cmd_tails += '' + r'"' + "Fake-Data-Default" + r'"' + '' + ','

        cmd = cmd_heads[0:-1] + ") " + cmd_tails[0:-1] + ");"
        for fake_id in range(volume):
            yield cmd
        #     try:
        #         self.sql.sqlcmd(self.cur, cmd)
        #         # print("execute insert ok")
        #         self.connect.commit()
        #     except Exception as e:
        #         print(cmd, e)
        #         self.connect.rollback()
        #         print("error")
        # print("inserted {} raws into table {}".format(volume,table_name))


    # 添加单条sql到setUp队列
    def add_setUp_statement(self,sql_string):
        if (self.isChecked(sql_string)):
            self.setUp_statements.append(sql_string)

    # 添加多条sql到tearDown队列
    def add_setUp_statement_fromList(self, sql_string_list):
        for sql_string in sql_string_list:
            if (self.isChecked(sql_string)):
                self.setUp_statements.append(sql_string)

    def add_setUp_statement_withInsertStatement(self, sql_string, rows):
        for row in range(rows):
            if (self.isChecked(sql_string)):
                self.setUp_statements.append(sql_string)

    # 添加单条sql到tearDown队列
    def add_tearDown_statement(self, sql_string):
        if (self.isChecked(sql_string)):
            self.tearDown_statements.append(sql_string)

    # 添加多条sql到tearDown队列
    def add_tearDown_statement_fromList(self, sql_string_list):
        for sql_string in sql_string_list:
            if (self.isChecked(sql_string)):
                self.tearDown_statements.append(sql_string)

    # 执行指定sql队列
    def excuteSqlList(self,sql_list):#设置
        if len(sql_list) <0:
            print("no statement found")
        else:
            for sql_statement in sql_list:
                try:
                    self.sql.sqlcmd(self.cur, sql_statement)
                    self.connect.commit()
                    print("excuted sql :",sql_statement)
                except Exception as e:
                    self.connect.rollback()
                    print("error sql excution:",sql_statement,e,)

    # 设置环境，逐条执行setUp语句队列
    def setUpEnv(self):
        self.excuteSqlList(self.setUp_statements)

    # 清理环境，逐条执行tearDown语句队列
    def clearEnv(self):
        self.excuteSqlList(self.tearDown_statements)

if __name__ == "__main__":
    # 工作流如下

    # step-1: 创建Dbmanagee并连接mySQL
    my_db = DbManagee(MySql.MySQL('DATABASE'))

    # step-2: 准备sql队列
    TableHeaderDict = dict(userName="", studentId="", workId="", labPosition="")

    sql_01 = DbManagee.convertTableDict_toCreateTableStatement(TableHeaderDict,"myTable_1","myKeyId")
    sql_02 = DbManagee.convertTableDict_toCreateTableStatement(TableHeaderDict,"myTable_2","myKeyId")
    sql_03 = DbManagee.insertSingleFakeRowsIntoTableStatement(TableHeaderDict,"myTable_1")

    statement_setup = [sql_01, sql_02 ]
    statement_cleardown = ["drop table myTable_1", "drop table myTable_2" ]

    # step-3: 添加sql队列
    my_db.add_setUp_statement_fromList(statement_setup)
    my_db.add_setUp_statement_withInsertStatement(sql_03,100)
    my_db.add_tearDown_statement_fromList(statement_cleardown)

    # step-4: 执行队列
    my_db.setUpEnv()
    # my_db.clearEnv()

