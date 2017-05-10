'''哈尔滨理工大学'''

import re
from . import init, NoMatchError, LoginError

# 继承初始化类
class Runner(init):
	encoding = "utf-8"
	def login(self):
		self.session.post("http://acm.hrbust.edu.cn/index.php?m=User&a=login",data = {
			"user_name":self.username,
			"password":self.password,
			"ajax":1,
		}, timeout = self.timeout)
		r = self.session.get("http://acm.hrbust.edu.cn/", timeout = self.timeout)
		r.encoding = self.encoding
		if self.nickname not in r.text:
			raise LoginError

	def submit(self):
		self.session.post("http://acm.hrbust.edu.cn/index.php?m=ProblemSet&a=postCode", data = {
			"problem_id":self.pid,
			"language":{"C":1, "C++":2, "Java":3}[self.language],
			"source_code":self.code,
			}, timeout=self.timeout)

	def get_last_runid(self):
		r = self.session.get("http://acm.hrbust.edu.cn/index.php?jumpUrl=&m=Status&a=showStatus&user_name=%s"%self.username, timeout=self.timeout)
		r.encoding = self.encoding
		match = re.findall(r'<td>(\d+?)</td><td><a href="/index\.php\?m=ProblemSet&a=showProblem&problem_id=', r.text)
		if not match:
			raise NoMatchError("runid")
		return int(match[0])

	def get_result(self,runid):
		r = self.session.get("http://acm.hrbust.edu.cn/index.php?jumpUrl=&m=Status&a=showStatus&user_name=%s"%self.username, timeout=self.timeout)
		r.encoding = self.encoding
		match = re.findall(str(runid) + r'[\s\S]+?<td class=".+?color">([\s\S]+?)</td>[\s\S]+?<td>(\d+?)ms[\s\S]+?<td>(\d+?)k', r.text)
		if not match:
			raise NoMatchError("result")
		if "Compile Error" in match[0][0]:
			result = "Compile Error"
		else:
			retult = match[0][0]
		timeused = int(match[0][1])
		memoryused = int(match[0][2])
		return result, timeused, memoryused

	def get_compile_error_info(self, runid):
		r = self.session.get("http://acm.hrbust.edu.cn/index.php?m=Status&a=showCompileError&run_id=%s"%str(runid), timeout=self.timeout)
		r.encoding = self.encoding
		match = re.findall(r'<td class="showcode_mod_info"[\s\S]+?>([\s\S]+?)</td>', r.text)
		if not match:
			raise NoMatchError("errorinfo")
		return match[0]