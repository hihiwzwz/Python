'''电子科技大学'''

import re
import json
from . import init, NoMatchError, LoginError

class Runner(init):
	encoding = "utf-8"
	def login(self):
		r = self.session.post("http://acm.uestc.edu.cn/user/login", data = json.dumps({
			"userName": self.username,
			"password": self.password,
		}), headers = {
			"Content-Type":"application/json;charset=UTF-8",
		}, timeout = self.timeout)
		r.encoding = self.encoding
		dict = json.loads(r.text)
		if dict["result"] != "success":
			raise LoginError

	def submit(self):
		self.session.post("http://acm.uestc.edu.cn/status/submit", data = json.dumps({
			"problemId": self.pid,
			"languageId":{"C":1 ,"C++":2, "Java":3}[self.language],
			"codeContent": self.code,
		}), headers = {
			"Content-Type":"application/json; charset=UTF-8",
		}, timeout = self.timeout)

	def get_last_runid(self):
		r = self.session.post("http://acm.uestc.edu.cn/status/search",data = json.dumps({
			"currentPage":1,
			"orderAsc":"false",
			"orderFields":"statusId",
			"userName":self.nickname,
		}), headers = {
			"Content-Type":"application/json;charset=UTF-8",
		}, timeout = self.timeout)
		r.encoding = self.encoding
		dic = json.loads(r.text)
		if dic["result"] != "success":
			raise NoMatchError("runid")
		return dic["list"][0]["statusId"]

	def get_result(self,runid):
		r = self.session.post("http://acm.uestc.edu.cn/status/search",data = json.dumps({
			"currentPage":1,
			"orderAsc":"false",
			"orderFields":"statusId",
			"userName":self.nickname,
		}), headers = {
			"Content-Type":"application/json;charset=UTF-8",
		}, timeout = self.timeout)
		r.encoding = self.encoding
		dic = json.loads(r.text)
		if dic["result"] != "success":
			raise NoMatchError("result")
		result=dic["list"][0]
		if result["returnType"] == "Accepted":
			return "Accepted", result["timeCost"], result["memoryCost"]
		if len(re.findall(r"on test \d+", result["returnType"])) > 0:
			return re.sub(r"on test \d+", "",result["returnType"]), 0, 0
		else:
			return result["returnType"], 0, 0
	def get_compile_error_info(self,runid):
		r = self.session.get("http://acm.uestc.edu.cn/status/info/%s"%str(runid), headers = {
			"Content-Type":"application/json; charset=UTF-8"
		}, timeout = self.timeout)
		r.encoding = self.encoding
		dic = json.loads(r.text)
		if dic["result"] != "success":
			raise NoMatchError("result")
		return dic["compileInfo"]