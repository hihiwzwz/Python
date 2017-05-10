'''全局配置'''

dbhost = "127.0.0.1"

dbport = 3306

dbuser = "root"

dbpassword = "111111"

dbname = "python"

dbcharset = "utf8"

address = "C:\\Python\\Spider\\problem\\"

timeout = 3

time_interval = 1

urls = {
	"HDU":"http://acm.hdu.edu.cn/showproblem.php?pid=%d",
	"POJ":"http://poj.org/problem?id=%d",
	"SDUT":"http://www.sdutacm.org/onlinejudge2/index.php/Home/Index/problemdetail/pid/%d.html",
	"SDIBT":"http://acm.sdibt.edu.cn/JudgeOnline/problem.php?id=%d",
	"UESTC":"http://acm.uestc.edu.cn/problem/data/%d",
	"HRBUST":"http://acm.hrbust.edu.cn/index.php?m=ProblemSet&a=showProblem&problem_id=%d",
	"BAILIAN":"http://bailian.openjudge.cn/practice/%d/",
}