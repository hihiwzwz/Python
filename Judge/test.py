import pymysql

db = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", passwd = "111111", db = "python", charset = "utf8")
cursor = db.cursor()

# codes = ["C:\\Python\\Judge\\code\\Accepted.txt",
# 		"C:\\Python\\Judge\\code\\Compile Error.txt",
# 		"C:\\Python\\Judge\\code\\Output Limit Exceed.txt",
# 		"C:\\Python\\Judge\\code\\Presentation Error.txt",
# 		"C:\\Python\\Judge\\code\\Time Limit Exceed.txt",
# 		"C:\\Python\\Judge\\code\\Wrong Answer.txt"]
# ojs = ["HDU", "POJ", "SDUT", "SDIBT", "UESTC", "HRBUST","BAILIAN"]
ojs = ["HRBUST"]
codes = ["C:\\Python\\Judge\\code\\Compile Error.txt"]

for oj in ojs:
	for code in codes:
		if oj == "UESTC":
			pid = 1
		else:
			pid = 1000
		sub = {
			"oj":oj,
			"pid":pid,
			"language":"C++",
			"result":"Waiting",
		}
		fp = open(code,'r')
		sub["code"] = fp.read()
		fp.close()
		cursor.execute('INSERT INTO submit(oj, pid, language, result, code) VALUES (%s,%s,%s,%s,%s)',(
		sub["oj"], sub["pid"], sub["language"], sub["result"], sub["code"]))
		db.commit()

cursor.close()
db.close()