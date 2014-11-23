sina_nba_crawler
================
该爬虫爬取的网页:http://nba.sports.sina.com.cn/players.php?dpc=1中所有球员的信息
利用python-scrapy爬取新浪nba数据库中的球员数据，scrapy的使用主要注意三个文件：
items.py #该文件定义一个类，类的成员用于爬虫解析的最终结果数据类型
spiders/nba.py #这是爬虫的解析程序，大部分内容都是专门针对新浪网的解析
setting.py #设置了爬虫的最终结果保存在本地mongo数据库中
