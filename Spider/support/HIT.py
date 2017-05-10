'''哈尔滨工业大学'''

encoding = "utf-8"
# 正则表达式提取,小括号中是需要提取的部分
content = {
	"Title":r"<h1>(.+?)</h1>",
	"Time Limit":r"<strong>Time limit</strong> : (\d+?) sec",
	"Memory Limit":r"<strong>Memory limit</strong> : (\d+?) M",
	"Description":r'<div id="problem-detail">([\s\S]+?)<H3>Input:',
	"Input":r"Input.*?</H3>([\s\S]+?)<H3>Output:",
	"Output":r"Output.*?</H3>([\s\S]+?)<H3>Sample Input:",
	"Sample Input":r"Sample Input.*?</H3>([\s\S]+?)<H3>Sample Output:",
	"Sample Output":r"Sample Output.*?</H3>([\s\S]+?)</div>",
	"Source":r'<strong>Source</strong> : <a href=.+?>(.+?)</a>',
}
# 替换src中相对地址为绝对地址,并且针对不同的格式进行不同的替换.
def replace_src(description):
	import re
	if len(re.findall(r'src="http',description)) > 0:
		return description
	if len(re.findall(r'src="',description)) > 0:
		return description.replace('src="', 'src="http://acm.sdibt.edu.cn/')
	if len(re.findall(r"src=", description)) > 0:
		return description.replace("src=", "src=http://acm.sdibt.edu.cn/")
	return description