'''北京大学百练考试系统'''

import re
from . import init, NoMatchError, LoginError

class Runner(init):
	encoding = "utf-8"
	def login(self):
		self.session.post("http://bailian.openjudge.cn/api/auth/login/", data = {
			"email":self.username,
			"password":self.password
		}, timeout = self.timeout)
		r = self.session.get("http://bailian.openjudge.cn/", timeout=self.timeout)
		r.encoding = self.encoding
		if self.nickname not in r.text:
			raise LoginError

	def submit(self):
		self.session.post("http://bailian.openjudge.cn/api/solution/submit/", data = {
			"problemNumber":self.pid,
			"language": {"C":"GCC", "C++":"G++", "Java":"Java"}[self.language],
			"source":self.code,
			"contestId":3,
			}, timeout = self.timeout)

	def get_last_runid(self):
		r = self.session.get("http://bailian.openjudge.cn/practice/status/?userName=%s"%self.nickname, timeout = self.timeout)
		r.encoding = self.encoding
		match = re.findall(r'<a href="/practice/solution/(\d+?)/.*?"', r.text)
		if not match:
			raise NoMatchError("runid")
		return int(match[0])

	def get_result(self,runid):
		r = self.session.get("http://bailian.openjudge.cn/practice/status/?userName=%s"%self.nickname, timeout = self.timeout)
		r.encoding = self.encoding
		match = re.findall(str(runid)+ r'/.+?class="result-.+?">(.+?)</a>[\s\S]+?<td class="memory">(.*?)</td>\s+?<td class="spending-time">(.*?)</td>', r.text)
		if not match:
			raise NoMatchError("result")
		result = match[0][0]
		raw_memoryused = match[0][1]
		raw_timeused = match[0][2]
		match = re.findall(r"(\d+?)kB", raw_memoryused)
		if not match:
			memoryused = 0
		else:
			memoryused = int(match[0])
		match = re.findall(r"(\d+?)ms", raw_timeused)
		if not match:
			timeused = 0
		else:
			timeused = int(match[0])
		return result, timeused, memoryused

	def get_compile_error_info(self,runid):
		r = self.session.get("http://bailian.openjudge.cn/practice/solution/"+str(runid), timeout = self.timeout)
		r.encoding = self.encoding
		match = re.findall(r'<pre>([\s\S]+?)</pre>', r.text)
		if not match:
			raise NoMatchError("errorinfo")
		return match[0]