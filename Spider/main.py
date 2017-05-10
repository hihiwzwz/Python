'''主函数模块,从数据库中获取题目ID及OJ,然后爬取题目的详细信息,爬取结束后进行存储'''

import time
import config
import spider
import pymysql

def main(problem):
	#打开数据库
	db = pymysql.connect(host = config.dbhost,
		port = config.dbport,
		user = config.dbuser,
		passwd = config.dbpassword,
		db = config.dbname, 
		charset = config.dbcharset)
	cursor = db.cursor()

	oj = problem[0]
	pid = problem[1]
	maxid = problem[2]
	# 开始爬取
	while pid <= maxid:
		raw_problem = {
			"oj":oj,
			"pid":pid,
		}
		try:
			problem = spider.crawl(raw_problem, config.urls, config.timeout)
			# 如果没有爬取到问题
			if not problem:
				print("%s,%d problem can not crawl"%(raw_problem["oj"],raw_problem["pid"]))
				# 查询数据库中是否存在该题,如果是,则将其删除.
				match = cursor.execute("SELECT * FROM problem WHERE oj = %s AND pid = %s",(raw_problem["oj"],raw_problem["pid"]))
				if match:
					cursor.execute("DELETE FROM problem WHERE oj = %s AND pid = %s",(raw_problem["oj"],raw_problem["pid"]))
					db.commit()
			else:
				# 如果爬取到问题,进行数据库的更新工作
				match = cursor.execute("SELECT * FROM problem WHERE oj = %s AND pid = %s",(raw_problem["oj"],raw_problem["pid"]))
				# 如果有该题,则更新
				if match:
					cursor.execute("UPDATE problem SET title = %s, time = %s, memory = %s, description = %s, input = %s, output = %s, samplein = %s, sampleout = %s, source = %s WHERE oj = %s AND pid = %s",(
					problem["Title"], problem["Time Limit"], problem["Memory Limit"], problem["Description"], problem["Input"], problem["Output"], problem["Sample Input"], problem["Sample Output"], problem["Source"], problem["oj"], problem["pid"]))
				# 没有就创建题目
				else:
					problem["Total Submit"] = 0
					problem["Total AC"] = 0
					cursor.execute("INSERT INTO problem VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
					problem["oj"], problem["pid"], problem["Title"], problem["Time Limit"], problem["Memory Limit"], problem["Total Submit"], problem["Total AC"], problem["Description"], problem["Input"], problem["Output"], problem["Sample Input"], problem["Sample Output"], problem["Source"]))
				db.commit()
			pid += 1
		except Exception as error:
			print(error,"error:",raw_problem["oj"],",",raw_problem["pid"])
			time.sleep(1)
	# 输出数据库内容查看
	cursor.execute("SELECT * FROM problem")
	match = cursor.fetchall()
	for value in match:
		fp = open(config.address+value[0]+"--"+str(value[1])+".txt", 'w', encoding = "utf-8")
		for i in range(2,13):
			fp.write(str(value[i])+"\n\n")
		fp.write("\n\n")
	cursor.close()
	db.close()
if __name__ == "__main__":
	problems = [["HDU", 1700, 1710],
		["POJ", 1700, 1710],
		["SDUT", 1700, 1710],
		["SDIBT", 1700, 1710],
		["UESTC", 1000, 1010],
		["HRBUST", 1456, 1456],
		["BAILIAN", 1700, 1710]]
	for problem in problems:
		main(problem)