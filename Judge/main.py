'''程序入口,进行数据库的读取和存储,读取出来的数据提交给judger模块'''

import time
import config
import judger
import pymysql
from support import NoMatchError, LoginError, SubmitError

def main():
	while True:
		# 打开数据库
		db = pymysql.connect(host = config.dbhost, port = config.dbport, user = config.dbuser, passwd = config.dbpassword, db = config.dbname, charset = config.dbcharset)
		cursor = db.cursor()

		match = cursor.execute("SELECT * FROM submit WHERE id = (SELECT min(id) FROM submit WHERE result = 'Waiting')")
		if not match:
			cursor.close()
			db.close()
			time.sleep(3)
			continue
		match = cursor.fetchall()
		sub = {}
		sub["oj"], sub["pid"], sub["language"], sub["code"] = match[0][1], match[0][2], match[0][3], match[0][4]
		print("New task")
		try:
			sub["runid"], sub["result"], sub["timeused"], sub["memoryused"], sub["errorinfo"] = judger.judge(sub, config.users, config.timeout, config.time_interval)
		except KeyError:
			cursor.execute("DELETE FROM submit WHERE id = %s",match[0][0])
			db.commit()
			print("%s Not Find In Support"%sub["oj"])
		except LoginError:
			print("Login error")
		except SubmitError:
			print("Submit error")
		except NoMatchError as error:
			print("No match error:%s"%error)
		except Exception as error:
			print("Unknown error:%s"%error)
		else:
			print("end of the judged")
			cursor.execute("UPDATE submit SET runid = %s, result = %s, timeused = %s, memoryused = %s, errorinfo = %s WHERE id = %s",(
			sub["runid"], sub["result"], sub["timeused"], sub["memoryused"], sub["errorinfo"], match[0][0]))
			db.commit()
		finally:
			cursor.close()
			db.close()
		break
if __name__=="__main__":
	main()