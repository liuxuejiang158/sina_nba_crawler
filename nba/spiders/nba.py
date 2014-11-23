# coding:utf-8
import re
import scrapy
from scrapy.http import Request
from scrapy import log
from ..items import nbaItem
class nbaSpider(scrapy.Spider):
    name = "nbaspider"
    allowd_domains = ['sina.com']
    start_urls=['http://nba.sports.sina.com.cn/players.php?dpc=1']

    def parse(self,response):
        for item in response.xpath("//tr[@id='playerslist']").extract():
            temp = item.split("</td>")
            for key in temp:
                number = re.search("<td>(.+?)<a",key)
                name = re.search('">([^<>]+?)</a>',key)
                href = re.search('<a href="(.+?)">',key)
                if number and name and href:
                    number=number.group(1).strip()
                    name=name.group(1).strip()
                    href=href.group(1).strip()
                    href = 'http://nba.sports.sina.com.cn/'+href
                    yield Request(href,meta={
                        'name':name,
                        'number':number
                    },
                    callback=self.parse_2)

    def parse_2(self,response):
        #解析个人信息
        basic_info={
            'team':"",#队名
            'location':"",#球场上的位置
            'birthday':"",#生日
            'age':"",#年龄
            'birth_place':"",#出生地
            'college':"",#毕业院校
            'height':"",#身高
            'weight':"",#体重
            'start_nba_year':"",#进入nba年份
            'nba_age':"",#球龄
            'sick_situation':"",#伤病情况
            'suspend_situation':"",#停赛情况
            'show_situation':"",#选秀情况
            'year_high_score':"",#赛季最高分
            'life_high_score':""#生涯最高分
        }
        #解析球队名
        basic_info['team']=response.xpath("//div[@id='table730top']/p/a[1]/text()").extract()[0]
        #解析队员在球场的位置
        temp=response.xpath('//div/p').extract()
        location=""
        for item in temp:
            temp=re.search('</a>\s\|(.+?)\|(.+?)\|',item)
            if temp:
                if temp.group(2):
                    basic_info['location']=temp.group(2)
                    break
        ##解析其它个人信息##
        temp=response.xpath("//tr[@bgcolor='#fcac08']").extract()
        if len(temp)==8:
            #获取年龄和出生日期
            list_temp=re.findall('">(.+?)</td>',temp[0])
            for item in list_temp:
                if '-' in item:
                    basic_info['birthday']=item.strip()
                if u'岁' in item:
                    basic_info['age']=item.strip()
            #获取出生地和毕业院校
            list_temp=re.findall('<td>(.+?)</td>',temp[1])
            if len(list_temp)==3:
                basic_info['birth_place']=list_temp[0]
                basic_info['college']=list_temp[2]
            #身高和体重
            string=temp[2].replace("\r\n\t","")
            for item in re.findall("<td>(.+?)</td>",string):
                if u'米' in item:
                    basic_info['height']=item.strip()
                if u'公斤' in item:
                    basic_info['weight']=item.strip()
            #获取NBA进入年份和球龄
            string=temp[3].replace("\r\n\t","")
            for item in re.findall("<td>(.+?)</td>",string):
                if u'年' in item:
                    year=item.split(u"年")
                    if year[0].isdigit():
                        if int(year[0])>1900:
                            basic_info['start_nba_year']=item.strip()
                        else:
                            basic_info['nba_age']=item.strip()
            #获取伤病情况
            #获取停赛情况
            #获取选秀情况
            string=temp[6].replace("\r\n\t","")
            for item in re.findall(">(.+?)</td>",string):
                if u'选中' in item:
                    basic_info['show_situation']=item.strip()
                    break
            #赛季最高分和生涯最高分
            string=temp[7].replace("\r\n","").replace("\t","")
            List=re.findall("<td>(.+?)</td>",string)
            if u'分' in List[0]:
                basic_info['year_high_score']=List[0].strip()
            if u'分' in List[2]:
                basic_info['life_high_score']=List[2].strip()
        '''
        #常规赛技术统计
        data_regular_season={
            'season_year':"",#赛季
            'team':"",#球队
            'appearance':"",#出场次数
            'first_team':"",#首发次数
            'time':"",#时间
            'shooting':"",#投篮
            'three_point':"",#三分
            'penalty':"",#罚球
            'before_rebound':"",#前场篮板
            'after_rebound':"",#后场篮板
            'total_rebound':"",#总篮板
            'assist':"",#助攻
            'steal':"",#抢断
            'block_shot':"",#盖帽
            'fault':"",#失误
            'foul':"",#犯规
            'score':"",#得分
            'high_score':""#最高分
        }
        #最近五场统计
        data_recent_field={
            'date':"",#日期
            'game_name':"",#比赛
            'category':"",#类型
            'first_team':"",#是否首发
            'time':"",#时间
            'shooting':"",#投篮
            'three_point':"",#三分
            'penalty':"",#罚球
            'before_rebound':"",#前场篮板
            'after_rebound':"",#后场篮板
            'total_rebound':"",#总篮板
            'assist':"",#助攻
            'steal':"",#抢断
            'block_shot':"",#盖帽
            'fault':"",#失误
            'foul':"",#犯规
            'score':"",#得分
        }
        '''
        temp=response.xpath("//tr[@bgcolor='#FFEFB6']").extract()
        regular_season=[]#常规赛技术统计
        recent_field=[]#最近五场统计
        for item in temp:
            if re.search('\d+-\d+-\d+',item):#最近五场统计
                string=item.replace("\r\n","").replace("\t","")
                List=re.findall("<td>(.*?)</td>",string)
                if len(List)==17:
                    data_recent_field={}
                    data_recent_field['date']=List[0]
                    if re.search('">(.+?)</a>',List[1]):
                        data_recent_field['game_name']=re.search('">(.+?)</a>',List[1]).group(1).strip()
                    else:
                        data_recent_field['game_name']=""
                    data_recent_field['category']=List[2]
                    data_recent_field['first_team']=List[3]
                    data_recent_field['time']=List[4]
                    data_recent_field['shooting']=List[5]
                    data_recent_field['three_point']=List[6]
                    data_recent_field['penalty']=List[7]
                    data_recent_field['before_rebound']=List[8]
                    data_recent_field['after_rebound']=List[9]
                    data_recent_field['total_rebound']=List[10]
                    data_recent_field['assist']=List[11]
                    data_recent_field['steal']=List[12]
                    data_recent_field['block_shot']=List[13]
                    data_recent_field['fault']=List[14]
                    data_recent_field['foul']=List[15]
                    data_recent_field['score']=List[16]
                    recent_field.append(data_recent_field)
            else:
                string=item.replace("\r\n","").replace("\t","")
                List=re.findall("<td>(.*?)</td>",string)
                if List and List[0].count('-')==1 and len(List)==17:
                    data_regular_season={}
                    data_regular_season['season_year']=List[0]
                    if re.search('">(.+?)</a>',List[1]):
                        data_regular_season['team']=re.search('">(.+?)</a>',List[1]).group(1).strip()
                    else:
                        data_regular_season['team']=""
                    data_regular_season['appearance']=List[2]
                    data_regular_season['first_team']=List[3]
                    data_regular_season['time']=List[4]
                    data_regular_season['shooting']=List[5]
                    data_regular_season['three_point']=List[6]
                    data_regular_season['penalty']=List[7]
                    data_regular_season['before_rebound']=List[8]
                    data_regular_season['after_rebound']=List[9]
                    data_regular_season['total_rebound']=List[10]
                    data_regular_season['assist']=List[11]
                    data_regular_season['steal']=List[12]
                    data_regular_season['block_shot']=List[13]
                    data_regular_season['fault']=List[14]
                    data_regular_season['foul']=List[15]
                    data_regular_season['score']=List[16]
                    regular_season.append(data_regular_season)
        log.msg(str(len(regular_season))+"\t"+str(len(recent_field))+'\n',level=log.ERROR)
        #NBA生涯
        temp=response.xpath("//tr[@bgcolor='#ffffff']").extract()
        nba_career={}
        for item in temp:
            if u'NBA生涯' in item:
                string=item.replace("\r\n","").replace("\t","")
                List=re.findall("<td>(.*?)</td>",string)
                if len(List)==15:
                    nba_career['appearance']=List[0]
                    nba_career['first_team']=List[1]
                    nba_career['time']=List[2]
                    nba_career['shooting']=List[3]
                    nba_career['three_point']=List[4]
                    nba_career['penalty']=List[5]
                    nba_career['before_rebound']=List[6]
                    nba_career['after_rebound']=List[7]
                    nba_career['total_rebound']=List[8]
                    nba_career['assist']=List[9]
                    nba_career['steal']=List[10]
                    nba_career['block_shot']=List[11]
                    nba_career['fault']=List[12]
                    nba_career['foul']=List[13]
                    nba_career['score']=List[14]
        item=nbaItem()
        item['name']=response.meta['name']
        item['number']=response.meta['number']
        item['data']={
            'basic_info':basic_info,
            'regular_season':regular_season,
            'recent_field':recent_field,
            'nba_career':nba_career
        }
        return item















