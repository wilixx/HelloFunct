# pyspark统计数据表实例 #
## 准备工作 ##
- 安装JAVA并配置环境变量，配置数据库驱动 `jre/lib/ext/mysql-driver-versionX.0.jar`
- 安装python与pip，注意安装目录不能有空格，若旧版本python路径中包含空格，建议不要挣扎，直接另建一个目录新安装一个python，把`pip、python`名称加上特殊后缀，如 `pip-4`,`python-4`
- 准备mysql环境，建立数据表
- 编写Java代码，逐步调试改正编译错误
## python代码如下 ##

	from pyspark.context import SparkContext
	from pyspark.sql import SQLContext, HiveContext, Row
	import os
	os.environ ['JAVA_HOME'] = 'Disk:\Path\To\Java\jdk1.8.0_65' # 设置环境变量以消除错误
	sc = SparkContext('local')
	sc.setLogLevel("OFF") # 修改log级别，屏蔽报错信息
	
	# 配置JAVA jdbc-mysql-driver.jar 驱动
	url = \
	  "jdbc:mysql://127.0.0.1:3306/mysql?useUnicode=true&characterEncoding=UTF-8&useSSL=false&serverTimezone=UTC&user=your_user_name&password=your_pass_word"
	sqlContext = SQLContext(sc)
	df = sqlContext \
	  .read \
	  .format("jdbc") \
	  .option("url", url) \
	  .option("dbtable", "your_db_name.your_table_name") \
	  .load()
	# Looks the schema of this DataFrame.
	df.printSchema()
	
	# Counts people by age
	countsByAge = df.groupBy("age").count()
	countsByAge.show()
	countsByGender = df.groupBy("gender").count()
	countsByGender.show()
	