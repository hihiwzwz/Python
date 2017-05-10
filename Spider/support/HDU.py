'''杭州电子科技大学'''

encoding = "gbk"
# 正则表达式提取,小括号中是需要提取的部分
content = {
    "Title": r"<h1 style='color:#1A5CC8'>(.+?)</h1>",
    "Time Limit": r"Time Limit: \d+/(\d+?) MS",
    "Memory Limit": r"Memory Limit: \d+/(\d+?) K",
    "Description": r"Problem Description</div> <div class=panel_content>([\s\S]+?)</div><div class=panel_bottom>",
    "Input": r"Input</div> <div class=panel_content>([\s\S]+?)</div><div class=panel_bottom>",
    "Output": r"Output</div> <div class=panel_content>([\s\S]+?)</div><div class=panel_bottom>",
    "Sample Input": r"Sample Input</div><div class=panel_content><pre><div style=\"font-family:Courier New,Courier,monospace;\">([\s\S]+?)</div></pre></div><div class=panel_bottom>",
    "Sample Output": r"Sample Output</div><div class=panel_content><pre><div style=\"font-family:Courier New,Courier,monospace;\">([\s\S]+?)</div></pre></div><div class=panel_bottom>",
    "Source": r"Source</div> <div class=panel_content> <a href=.+?> ([\s\S]+?)</a> </div>",
}
# 替换src中相对地址为绝对地址,并且针对不同的格式进行不同的替换.
def replace_src(description):
    import re
    if len(re.findall(r"src=http",description))>0:
        return description
    if len(re.findall(r"src=",description))>0:
        return description.replace(r"src=", r"src=http://acm.hdu.edu.cn/")
    return description
