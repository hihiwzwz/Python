'''山东工商学院'''

encoding = "utf-8"
# 正则表达式提取,小括号中是需要提取的部分
content = {
	"Title":r"</title><center><h2>(.+?)</h2>",
	"Time Limit":r"Time Limit: </span>(\d+?) Sec",
	"Memory Limit":r"Memory Limit: </span>(\d+?) MB",
	"Description":r"Description</h2><p>([\s\S]+?)</p><h2>Input",
	"Input":r"Input</h2><p>([\s\S]+?)</p><h2>Output",
	"Output":r"Output</h2><p>([\s\S]+?)</p><h2>Sample Input",
	"Sample Input":r"Sample Input</h2><pre>([\s\S]+?)</pre>",
	"Sample Output":r"Sample Output</h2><pre>([\s\S]+?)</pre>",
	"Source":r"Source</h2><p><a href=.+?>([\s\S]+?)</a>",
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