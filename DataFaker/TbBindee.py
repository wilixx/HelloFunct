#!/usr/bin/env python
# coding=utf-8
# author: Allen Guo
import Config, MySql
try:
    import exrex
except:
    print("Please install&import exrex,\n see to <>")
'''
# 连接database，执行语句示例
sql = MySql.MySQL('DATABASE')
connect, cur = sql.connect()
sql.sqlcmd(cur, "sql_statement") # 这里要将字符串“sql_statement”替换为你要执行的sql语句
'''
class TbBindee():
    """ Database Managee Class
    Elements：
        self.sql = sql,tableName, tableHeaderDict
    Methods：
        setUpEnv(): 执行设置环境sql队列
        clearEnv(): 执行清理环境sql队列
        isChecked(): 检查sql语句合法性
        convertTableDict_toCreateTableStatement(): 字典转建表sql
    """

    # 构造方法，参数为mysql连接实例
    def __init__(self,sql,tableHeaderDict,tableName):
        self.sql = sql
        self.connect,self.cur = self.sql.connect()
        self.tableName = tableName
        self.tableHeaderDict = tableHeaderDict
        self.createTableStatement = ""
        self.dropTableStatement = ""
        self.insertRowStatement = ""
        self.delectRowStatement = ""
        self.updateRowStatement = ""

    # 检查sql语句合法性
    def isChecked(self,sql_string):
        '''该方法尚未编写
        :param sql_string:
        :return: 检查是否合法
        '''
        return True

    # 将根据表头字典创建表
    def create(self,key_id="mykey_id"):
        '''
        :param TableHeaderDict: 表头字典
        :param tableName: 表名称
        :param key_id: 主键名称
        :return: sql建表语句
        '''
        create_table_prefix = '''create table if not exists '''+self.tableName+"("
        create_table_prefix += key_id+ '''  int primary key not null auto_increment,'''
        create_table_statement = create_table_prefix
        for columTitle in self.tableHeaderDict.keys():
            create_table_statement += "\n" + columTitle + '  varchar(50)' + ","
        # close parentheses
        create_table_statement += "\n" + "additionalKey" + '  varchar(50)' + '' + ')'
        self.createTableStatement = create_table_statement
        print("sql statement formed as: ",create_table_statement)
        self.excuteSql(self.createTableStatement)

    # 根据模板插入同样内容的行
    def insertFakeRowFromTemplate(self,insertTemplateDict):
        cmd_heads = r"INSERT INTO " + self.tableName  + " ("
        cmd_tails = r" VALUES ("
        for columTile in insertTemplateDict.keys():
            cmd_heads += columTile + ','
            # cmd_tails += '' + r'"' + "FakeDataDefault" + r'"' + '' + ','
            cmd_tails += '' + r'"{' + columTile + r'}"' + '' + ','

        cmd = cmd_heads[0:-1] + ") " + cmd_tails[0:-1] + ");"
        cmd = cmd.format(**insertTemplateDict)
        self.excuteSql(cmd)

    # 无模板默认插入语句
    def insertFakeRowWithoutTemplate(self):
        cmd_heads = r"INSERT INTO " + self.tableName + " ("
        cmd_tails = r" VALUES ("
        for columTile in self.tableHeaderDict.keys():
            cmd_heads += columTile + ','
            cmd_tails += '' + r'"' + "FakeDataDefault" + r'"' + '' + ','
            # cmd_tails += '' + r'"{' + columTile + r'}"' + '' + ','

        cmd = cmd_heads[0:-1] + ") " + cmd_tails[0:-1] + ");"
        # cmd = cmd.format(**insertTemplateDict)
        self.excuteSql(cmd)
        # return cmd

    # 根据正则表达式模板插入行
    def insertFakeRowWithRandomData(self, insertTemplateDict):
        cmd_heads = r"INSERT INTO " + self.tableName + " ("
        cmd_tails = r" VALUES ("
        import exrex
        for columTile in insertTemplateDict.keys():
            cmd_heads += columTile + ','
            cmd_tails += '' + r'"' + exrex.getone(insertTemplateDict[columTile]) + r'"' + '' + ','
            # cmd_tails += '' + r'"{' + columTile + r'}"' + '' + ','

        cmd = cmd_heads[0:-1] + ") " + cmd_tails[0:-1] + ");"
        # cmd = cmd.format(**insertTemplateDict)
        self.excuteSql(cmd)
        # return cmd

    def insertManyRows(self,insertTemplateDict,rowsNum=10):
        for row in range(rowsNum):
            self.insertFakeRowWithRandomData(insertTemplateDict)
        print("## Totally inserted {} rows".format(rowsNum))

    # 删除此表格
    def dropTable(self):
        self.dropTableStatement = "drop table " + self.tableName
        self.excuteSql(self.dropTableStatement)

    # 执行sql
    def excuteSql(self,sqlStatement):
        try:
            self.sql.sqlcmd(self.cur, sqlStatement)
            self.connect.commit()
            print("excuted sql :", sqlStatement)
        except Exception as e:
            self.connect.rollback()
            print("error sql excution:", sqlStatement, e)


if __name__ == "__main__":
    # 工作流如下

    # step-1: 创建表头字典与插入模板
    TableHeaderDict = dict(userName="", wholeName="",studentId="", workId="", labPosition="",
                           mathScore="",englishScore="",physicsScore="",csScore="",
                           gender="",age="",paperCount="",phoneNo="",idCard=""
                           )
    # 创建插入模板正则表达式
    TableTempDict = dict(userName=r'(1[0-2]|0[1-9])(:[0-5]\d){2} (A|P)M',
                         wholeName=r'(赵|钱|孙|李|周|吴|郑|王|国|马|张|胡|沈)(月|水|火|天|地|星|空|金|少|邵|益)(居|业|国|泰|民|宝|玉|太|平)',
                         studentId=r'(1[6-9]0)(\d\d\d)(\d0\d\d\d) (通院|微院|电院)学生',
                         workId= r'(15000-)(3|5|8|7)-([0-9])(\d){8}',
                         labPosition=r'(150-)(A|B|C)-(\d){2}',
                         mathScore=r'([6-9][\d])',
                         englishScore=r'([6-9][\d])',
                         physicsScore=r'([6-9][\d])',
                         csScore=r'([6-9][\d])',
                         gender=r'(男|女|保密)',
                         age=r'([2-3][\d])',
                         paperCount=r'([0-9])',
                         phoneNo=r'(\+86)-(1(3|5|7|8)[0-9]-)([0-9]){4}-([0-9]){4}',
                         idCard=r'(6127)([0-9]){2}(19[4-9][0-9])(1[0-2]|0[1-9])([0-2][0-9])([0-9]){3}([0-9]|[X])'
                         )
    # Step-2 绑定数据库
    my_tb = TbBindee(MySql.MySQL('DATABASE'),TableHeaderDict,"gbq_table")

    # step-3: 首次使用新建表
    # my_tb.create()

    # Step-4 插入任意多行
    my_tb.insertManyRows(TableTempDict,rowsNum=30)
    '''按照单条插入，已弃用此方法
    # for i in range(50):
    #     my_tb.insertFakeRowWithRandomData(TableTempDict)
    '''
    # Step-5 销毁表格
    # my_tb.dropTable()


