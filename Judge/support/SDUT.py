'''山东理工大学'''

import re
from . import init, NoMatchError, LoginError

class Runner(init):
	encoding = "utf-8"
	def login(self):
		self.session.post("http://www.sdutacm.org/onlinejudge2/index.php/Login/login.html", data={
			"user_name": self.username,
			"password": self.password,
		}, timeout=self.timeout)
		r = self.session.get("http://www.sdutacm.org/onlinejudge2/index.php/Home", timeout=self.timeout)
		r.encoding = self.encoding
		if self.nickname not in r.text:
			raise LoginError

	def submit(self):
		self.session.post("http://www.sdutacm.org/onlinejudge2/index.php/Home/Solution/submitsolution", data={
			"pid":self.pid,
			"lang":{"C": "gcc", "C++": "g++", "Java": "java"}[self.language],
			"code":self.code,
		}, timeout=self.timeout)

	def get_last_runid(self):
		r = self.session.get("http://www.sdutacm.org/onlinejudge2/index.php/Home/Solution/status?username=%s" % self.username, timeout=self.timeout)
		r.encoding = self.encoding
		match = re.findall(r'<tr>\s+?<td>(\d+?)</td>\s+?<td><a href="/onlinejudge', r.text)
		if not match:
			raise NoMatchError("runid")
		return int(match[0])

	def get_result(self, runid):
		r = self.session.get("http://www.sdutacm.org/onlinejudge2/index.php/Home/Solution/status?runid=" + str(runid), timeout=self.timeout)
		r.encoding = self.encoding
		match = re.findall(str(runid) + r'[\s\S]+?<td class="bold .+?">(.+?)</td>\s+?<td>(\d+?)ms</td>\s+?<td>(\d+?)kb', r.text)
		if not match:
			raise NoMatchError("result")
		result = match[0][0]
		if "Compile Error" in result:
			result = "Compile Error"
		timeused = int(match[0][1])
		memoryused = int(match[0][2])
		return result, timeused, memoryused

	def get_compile_error_info(self, runid):
		r = self.session.get("http://www.sdutacm.org/onlinejudge2/index.php/Home/Compile/view/sid/" + str(runid), timeout=self.timeout)
		r.encoding = self.encoding
		match = re.findall(r"<pre>([\s\S]+?)</pre>", r.text)
		if not match:
			raise NoMatchError("errorinfo")
		return match[0]