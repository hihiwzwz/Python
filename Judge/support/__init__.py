# 各种类初始化
class init:
	def __init__(self, user, pid, language, code, session, timeout,time_interval):
		self.username = user["username"]
		self.password = user["password"]
		self.nickname = user["nickname"]
		self.pid = pid
		self.language = language
		self.code = code
		self.session = session
		self.timeout = timeout
		self.time_interval = time_interval

#自定义异常类型,需要继承Exception异常类
class NoMatchError(Exception):
	"""没有匹配到数据"""
	pass
class LoginError(Exception):
	"""登录失败"""
	pass
class SubmitError(Exception):
	"""提交失败"""
	pass