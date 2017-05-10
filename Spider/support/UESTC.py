'''电子科技大学'''

encoding = "utf-8"

def replace_src(description):
	import re
	match = re.findall(r'''\((?:"|'|)(/images/problem/.+?\.(?:png|jpg|gif|PNG|JPG|GIF|Png|Jpg|Gif))(?:"|'|)\)''', description)
	if match:
		return re.sub(match[0], "http://acm.uestc.edu.cn" + match[0], description)
	return description

def replace_dic(str):
	import re
	match = re.findall(r'\[".+?"\]', str)
	if match:
		str = re.sub(r'\["', "", str)
		str = re.sub(r'"\]', "", str)
		str = re.sub(r'"', "", str)
		str = re.sub(r'\\n', '\n', str)
	return str