# OJ判题模块,接收主函数信息,将信息拿到各个OJ上进行提交,最后获取结果返回给主函数
import time
import requests
import support.HDU as HDU
import support.POJ as POJ
import support.SDUT as SDUT
import support.SDIBT as SDIBT
import support.UESTC as UESTC
import support.HRBUST as HRBUST
import support.BAILIAN as BAILIAN
from support import SubmitError

# 为True时打印判题过程中的细节
debug=True

oj_group={
	"HDU":HDU,
	"POJ":POJ,
	"SDUT":SDUT,
	"SDIBT":SDIBT,
	"UESTC":UESTC,
	"HRBUST":HRBUST,
	"BAILIAN":BAILIAN,
}

def judge(sub, users, timeout, time_interval):
	# 将相应的参数传递给对应的OJ类进行初始化,并生成一个对象
	OJ = oj_group[sub["oj"]]
	user = users[sub["oj"]]
	pid = sub["pid"]
	language = sub["language"]
	code = sub["code"]
	session = requests.session()
	OJRunner = OJ.Runner(user, pid, language, code, session,timeout, time_interval)

	# 登陆
	if debug:
		print("login...",end="")
	time.sleep(time_interval)
	OJRunner.login()
	if debug:
		print("ok")

	# 提交代码前获取最后一次提交的runid,用于判断提交成功与否
	if debug:
		print("\ngetting old runid...",end="")
	time.sleep(time_interval)
	runid_old=OJRunner.get_last_runid()
	if debug:
		print(runid_old)

	# 提交代码
	if debug:
		print("\nsubmitting...",end="")
	time.sleep(time_interval)
	OJRunner.submit()
	if debug:
		print("ok")

	# 获取新的runid
	n=0
	while True:
		if debug:
			print("\ngetting new runid...")
		time.sleep(time_interval)
		runid = OJRunner.get_last_runid()

		# 如果和runid_old不同,说明提交成功
		if runid != runid_old:
			break

		n+=1
		# 十次都没有新的提交信息,说明提交失败
		if n==10:
			raise SubmitError
	if debug:
		print("\ngot new runid:", runid)

	# 获取提交结果
	while True:
		if debug:
			print("\ngetting result...",end="")
		time.sleep(time_interval)
		result, timeused, memoryused = OJRunner.get_result(runid)
		if debug:
			print(result)

		# 若判题结果为 Waiting / Judging / Compiling / ...
		# 继续获取
		if "ing" in result:
			continue

		# 如果是编译错误
		errorinfo = None
		if "compil" in result.lower() and "error" in result.lower():
			time.sleep(time_interval)
			errorinfo = OJRunner.get_compile_error_info(runid)

		# 返回各项结果
		return runid, result, timeused, memoryused, errorinfo