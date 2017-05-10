'''北京大学'''

encoding = "utf-8"
# 正则表达式提取,小括号中是需要提取的部分
content = {
    "Title": r'<div class="ptt" lang="en-US">(.+?)</div>',
    "Time Limit": r'Time Limit:</b> (\d+?)MS',
    "Memory Limit": r'Memory Limit:</b> (\d+?)K',
    "Description": r'<p class="pst">Description</p><div class="ptx" lang="en-US">([\s\S]+?)</div><p class="pst">Input',
    "Input": r'<p class="pst">Input</p><div class="ptx" lang="en-US">([\s\S]+?)</div><p class="pst">Output',
    "Output": r'<p class="pst">Output</p><div class="ptx" lang="en-US">([\s\S]+?)</div><p class="pst">Sample Input',
    "Sample Input": r'<p class="pst">Sample Input</p><pre class="sio">([\s\S]+?)</pre><p class="pst">Sample Output',
    "Sample Output": r'<p class="pst">Sample Output</p><pre class="sio">([\s\S]+?)</pre><p class="pst">',
    "Source": r'<p class="pst">Source</p><div class="ptx" lang="en-US"><a href=.+?>([\s\S]+?)</a></div>',
}
# 替换src中相对地址为绝对地址,并且针对不同的格式进行不同的替换.
def replace_src(description):
    import re
    if len(re.findall(r'src="http',description))>0 or len(re.findall(r"src=http",description))>0:
        return description
    if len(re.findall(r'src="', description))>0:
        return description.replace('src="', 'src="http://poj.org/')
    if len(re.findall(r"src='", description))>0:
        return description.replace("src='", "src='http://poj.org/")
    if len(re.findall(r"src=", description))>0:
        return description.replace("src=", "src=http://poj.org/")
    if len(re.findall(r'src = "',description))>0:
        return description.replace('src = "','src="http://poj.org/')
    if len(re.findall(r"src =",description))>0:
        return description.replace("src =","src=http://poj.org/")
    return description