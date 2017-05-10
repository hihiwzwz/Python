'''山东工商学院'''

import re
from . import init, NoMatchError, LoginError
# 继承初始化类
class Runner(init):
	encoding = "utf-8"
	def login(self):
		self.session.post("http://acm.sdibt.edu.cn/JudgeOnline/login.php",data = {
			"user_id":self.username,
			"password":self.password,
		}, timeout = self.timeout)
		r = self.session.get("http://acm.sdibt.edu.cn/JudgeOnline/", timeout = self.timeout)
		r.encoding = self.encoding
		if self.nickname not in r.text:
			raise LoginError

	def submit(self):
		self.session.post("http://acm.sdibt.edu.cn/JudgeOnline/submit.php", data = {
			"id":self.pid,
			"language":{"C":0, "C++":1, "Java":3}[self.language],
			"source":self.code,
		}, timeout=self.timeout)

	def get_last_runid(self):
		r = self.session.get("http://acm.sdibt.edu.cn/JudgeOnline/status.php?user_id=%s"%self.username, timeout=self.timeout)
		r.encoding = self.encoding
		match = re.findall(r"<tr align=center class='evenrow'><td>(\d+?)<td>", r.text)
		if not match:
			raise NoMatchError("runid")
		return int(match[0])

	def get_result(self,runid):
		r = self.session.get("http://acm.sdibt.edu.cn/JudgeOnline/status.php?user_id=%s"%self.username, timeout=self.timeout)
		r.encoding = self.encoding
		match = re.findall(str(runid) + r"[\s\S]+?<font color=.+?>(.+?)</font>.*?<td>(\d+?) <font color=red>kb</font><td>(\d+?) <font color=red>ms", r.text)
		if not match:
			raise NoMatchError("result")
		result = match[0][0]
		memoryused = int(match[0][1])
		timeused = int(match[0][2])
		return result, timeused, memoryused

	def get_compile_error_info(self, runid):
		r = self.session.get("http://acm.sdibt.edu.cn/JudgeOnline/ceinfo.php?sid=%s"%str(runid), timeout=self.timeout)
		r.encoding = self.encoding
		match = re.findall(r"<pre id='errtxt'>([\s\S]+?)</pre>", r.text)
		if not match:
			raise NoMatchError("errorinfo")
		return match[0]