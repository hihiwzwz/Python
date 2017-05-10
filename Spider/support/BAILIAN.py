'''北京大学百练考试系统'''

encoding = "utf-8"
# 正则表达式提取,小括号中是需要提取的部分
content = {
    "Title":r'<div id="pageTitle"><h2>\d+?:([\s\S]+?)</h2></div>',
    "Time Limit":r"<dt>总时间限制: </dt>\s+?<dd>(\d+?)ms</dd>",
    "Memory Limit":r"<dt>内存限制: </dt>\s+?<dd>(\d+?)kB</dd>",
    "Description":r"<dt>描述</dt>\s+?<dd>([\s\S]+?)</dd>\s+?<dt>输入",
    "Input":r"<dt>输入</dt>\s+?<dd>([\s\S]+?)</dd>\s+?<dt>输出",
    "Output":r"<dt>输出</dt>\s+?<dd>([\s\S]+?)</dd>\s+?<dt>样例输入",
    "Sample Input":r"<dt>样例输入</dt>\s+?<dd><pre>([\s\S]+?)</pre>",
    "Sample Output":r"<dt>样例输出</dt>\s+?<dd><pre>([\s\S]+?)</pre>",
    "Source":r"<dt>来源</dt>\s+?<dd>([\s\S]+?)</dd>",
}
# 替换src中相对地址为绝对地址.此处无需替换,百练的所有格式均为绝对地址
def replace_src(description):
    return description
