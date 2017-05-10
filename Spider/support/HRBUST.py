'''哈尔滨理工大学'''

encoding = "utf-8"
# 正则表达式提取,小括号中是需要提取的部分
content = {
	"Title":r'<td class="problem_mod_name">(.+?)</td>',
	"Time Limit":r"Time Limit: (\d+?) MS",
	"Memory Limit":r"Memory Limit: (\d+?) K",
	"Description":r'Description</td></tr><tr><td class="problem_mod_content">([\s\S]+?)</td>',
	"Input":r'Input</td></tr><tr><td class="problem_mod_content">([\s\S]+?)</td>',
	"Output":r'Output</td></tr><tr><td class="problem_mod_content">([\s\S]+?)</td>',
	"Sample Input":r'Sample Input</td></tr><tr><td class="problem_mod_content">([\s\S]+?)</td>',
	"Sample Output":r'Sample Output</td></tr><tr><td class="problem_mod_content">([\s\S]+?)</td>',
	"Source":r'(?:Source|Author)</td></tr><tr><td class="problem_mod_content">(.+?)</td>',
}
# 替换src中相对地址为绝对地址,并且针对不同的格式进行不同的替换.
def replace_src(description):
	import re
	if len(re.findall(r'src="',description)) > 0:
		return description.replace('src="', 'src="http://acm.hrbust.edu.cn/')
	return description