# coding=utf-8
'''
Created on 2017年12月29日

@author: gWX403582
'''
import pymysql, configparser, os, logging

configdir = os.getcwd()
configPath = configdir + "\\config\\config.properties"
config = configparser.ConfigParser()


class MySQL(object):
    def __init__(self, config_info):
        config.read(configPath)
        self.Host = config.get(config_info, 'host')
        self.Port = config.get(config_info, 'port')
        self.User = config.get(config_info, 'user')
        self.Password = config.get(config_info, 'password')
        self.Database = config.get(config_info, 'database')

    def connect(self):
        connect = pymysql.connect(host=self.Host, port=int(self.Port),
                                  user=self.User, passwd=self.Password,
                                  db=self.Database, use_unicode=True, charset="utf8")
        cur = connect.cursor()
        cur.execute("USE %s " % self.Database)
        return connect, cur

    def disconnect(self, connect, cur):
        cur.close()
        connect.close()

    def sqlcmd(self, cur, sql_cmd, flag=False):
        try:
            if flag == False:
                return cur.execute(sql_cmd)
            else:
                return cur.fetchall()
        except Exception as error:
            logging.error(" [%s] command excute Failed!" % (sql_cmd))
            logging.error("Reason : %s" % (str(error)))