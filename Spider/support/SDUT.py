'''山东理工大学'''

encoding = "utf-8"
# 正则表达式提取,小括号中是需要提取的部分
content = {
    "Title":r'<h3 class="problem-header">(.+?)</h3>',
    "Time Limit":r'<span class="user-black">Time Limit:&nbsp;(\d+?)MS</span>',
    "Memory Limit":r'<span class="user-black">Memory Limit:&nbsp;(\d+?)KB</span>',
    "Description":r'<h4>Problem Description</h4>\s+?<div class="prob-content">([\s\S]+?)</div>\s+?<h4>Input',
    "Input":r'<h4>Input</h4>\s+?<div class="prob-content">([\s\S]+?)</div>\s+?<h4>Output',
    "Output":r'<h4>Output</h4>\s+?<div class="prob-content">([\s\S]+?)</div>\s+?<h4>Example Input',
    "Sample Input":r'<h4>Example Input</h4>\s+?<div class="prob-content">\s+?<pre>([\s\S]+?)</pre>\s+?</div>\s+?<h4>Example Output',
    "Sample Output":r'<h4>Example Output</h4>\s+?<div class="prob-content">\s+?<pre>([\s\S]+?)</pre>\s+?</div>\s+?<h4>Hint',
    "Source":r'<h4>Author</h4>\s+?<div class="prob-content">([\s\S]+?)</div>',
}
# 2590 2596这两个题的src格式根本不对,简直坑人的,逗B程序员.
# 替换src中相对地址为绝对地址,并且针对不同的格式进行不同的替换.
def replace_src(description):
    import re
    if len(re.findall(r'src="http',description))>0:
        return description
    if len(re.findall(r'src="',description))>0:
        return description.replace('src="','src="http://www.sdutacm.org/')
    if len(re.findall(r"src=", description))>0:
        return description.replace("src=","src=http://www.sdutacm.org/")
    return description