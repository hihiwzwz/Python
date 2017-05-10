import re
import time
import requests

from support import *

oj_src={
	#简单相对路径
	"a1":[r'src="',0],
	"a2":[r"src='",0],
	"a3":[r"src=",0],
	#带空格的相对路径
	"a4":[r'src = "',0],
	"a5":[r'src ="',0],
	"a6":[r'src= "',0],

	"a7":[r"src = '",0],
	"a8":[r"src= '",0],
	"a9":[r"src ='",0],

	"a10":[r"src = ",0],
	"a11":[r"src= ",0],
	"a12":[r"src =",0],
	#绝对路径
	"a13":[r'src="http',0],
	"a14":[r"src='http",0],
	"a15":[r"src=http",0],

	"a16":[r'src = "http',0],
	"a17":[r'src ="htpp',0],
	"a18":[r'src= "http',0],

	"a19":[r"src = 'http",0],
	"a20":[r"src= 'http",0],
	"a21":[r"src ='http",0],

	"a22":[r"src = http",0],
	"a23":[r"src= http",0],
	"a24":[r"src =http",0],
}

def spider(id,oj):
	#向网站发送请求
	r=requests.get(oj.url%id)
	#获取网站编码格式
	r.encoding=oj.encoding
	#获取网站代码
	html_code=r.text
	match=re.findall(oj.content["Description"],r.text)
	if match:
		return match[0]
	else:
		return None

def find_scr(description,oj_src,id,oj):
	for key,value in oj_src.items():
		match=re.findall(value[0],description)
		if match:
			value[1]+=1
			fp=open(oj.dress+"src\\"+key+".txt",'a+',encoding="utf-8")
			fp.write('%d '%id)
			fp.close()
def beginning(oj):
	fp=open(oj.dress+"src\\"+"000Error Message.txt",'a+',encoding="utf-8")
	#初始化
	for key,value in oj_src.items():
		value[1]=0
		f=open(oj.dress+"src\\"+key+".txt",'w',encoding="utf-8")
		f.write('!'+value[0]+'!\n')
		f.close()
	id=oj.minid
	while id<=oj.maxid:
		try:
			description=spider(id,oj)
			if description:
				find_scr(description,oj_src,id,oj)
			else:
				fp.write("%d题爬取失败\n"%id)
			id+=1
		except Exception as err:
			# 有任何未知错误发生（网络超时等）都进行retry
			print("%d题爬取时发生错误，错误信息:\n%s\n"%(id,err))
			# 每秒retry一次
			time.sleep(1)
			# 这里不执行 sid += 1 实现了retry
	fp.close()
	fp=open(oj.dress+"src\\"+"001total.txt",'w',encoding="utf-8")
	for key,value in oj_src.items():
		fp.write(key+'!'+value[0]+"! : %d\n"%value[1])
	fp.close()

if __name__=="__main__":
	beginning(HDU)
	beginning(POJ)
	beginning(SDUT)
	beginning(SDIBT)
	beginning(BAILIAN)