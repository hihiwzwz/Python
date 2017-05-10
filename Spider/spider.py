'''OJ爬虫模块,接收主函数信息,按照信息到相应的OJ爬取相应的题目'''

import re
import json
import requests

import support.HDU as HDU
import support.POJ as POJ
import support.SDUT as SDUT
import support.SDIBT as SDIBT
import support.UESTC as UESTC
import support.HRBUST as HRBUST
import support.BAILIAN as BAILIAN

def crawl(problem, urls, timeout):
	oj_group={
		"HDU":HDU,
		"POJ":POJ,
		"SDUT":SDUT,
		"SDIBT":SDIBT,
		"UESTC":UESTC,
		"HRBUST":HRBUST,
		"BAILIAN":BAILIAN,
	}
	OJ = oj_group[problem["oj"]]
	url = urls[problem["oj"]]
	if problem["oj"] == "UESTC":
		# 向网站发送请求
		r = requests.post(url%problem["pid"],headers = {
			"Content-Type":"application/json; charset=UTF-8",
		}, timeout = timeout)
		r.encoding = OJ.encoding
		dic = json.loads(r.text)
		if dic["result"] != "success":
			return None
		problem["Title"] = dic["problem"]["title"]
		problem["Time Limit"] = dic["problem"]["timeLimit"]
		problem["Memory Limit"] = dic["problem"]["memoryLimit"]
		problem["Description"] = OJ.replace_src(dic["problem"]["description"])
		problem["Input"] = dic["problem"]["input"]
		problem["Output"] = dic["problem"]["output"]
		problem["Sample Input"] = OJ.replace_dic(dic["problem"]["sampleInput"])
		problem["Sample Output"] = OJ.replace_dic(dic["problem"]["sampleOutput"])
		problem["Source"] = dic["problem"]["source"]
	else:
		# 向网站发送请求
		r = requests.get(url%problem["pid"], timeout = timeout)
		r.encoding = OJ.encoding
		html_code = r.text
		# 遍历正则表达式进行题目提取
		for key,value in OJ.content.items():
			match = re.findall(value,html_code)
			# 匹配到了,加入字典
			if match:
				problem[key]=match[0]
			# 描述不能为空，若空则放弃
			elif key == "Description":
				return None
			else:
			#其他内容皆可为空
				problem[key]=""
		problem["Time Limit"] = int(problem["Time Limit"])
		problem["Memory Limit"] = int(problem["Memory Limit"])
		# 山东工商学院的单位是 秒 和 MB,转换成 毫秒 和 KB
		if problem["oj"] == "SDIBT" or problem["oj"] == "HIT":
			problem["Time Limit"] *= 1000
			problem["Memory Limit"] *= 1024
		#将描述中图片的相对地址替换成绝对地址
		problem["Description"] = OJ.replace_src(problem["Description"])
	return problem
