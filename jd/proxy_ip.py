#!/usr/bin/python3
#coding=utf-8
'''
http ip代理爬取
'''

import urllib
import re
import pickle

class httpProxySpider:
    '''
    定向爬取http代理的爬虫程序
    '''
    def __init__(self):
        '''
        初始化抓取的网址url,加载现有ip地址
        '''
        self.url='http://www.xicidaili.com/wt/'
        with open('ip_list.txt') as f:
            try:
                ip_list=pickle.load(f)
            except:
                ip_list = []
        self.ip_list=ip_list
        self.len_before=len(self.ip_list)
        print('[INFO]当前已有ip数:%s'%self.len_before)

    def work(self,n):
        '''
        控制器，开始抓取
        :param n: 抓取最新的前ｎ页
        :return:
        '''

        r=re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        r_port=re.compile(r'<td>(\d{1,5})</td>')
        for page in range(1,n+1):
            self.loadPage(page,r,r_port)

        #对象文件中序列化存储
        with open('ip_list.txt','w') as f:
            pickle.dump(self.ip_list, f)

        print('[DONE]有效抓取ip数:%s'%(len(self.ip_list)-self.len_before))
        return self.ip_list

    def loadPage(self,page,r,r_port):
        '''
        发起请求并下载页面
        :param page: 下载第ｐａｇｅ页
        :return:
        '''
        print('正在抓取第%s页' % page)
        url_use=self.url+str(page)

        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }

        request=urllib2.Request(url_use,headers=headers)
        try:

            response=urllib2.urlopen(request)
            html=response.read()
            result=r.findall(html)
            port=r_port.findall(html)

            if result!=None:
                for i in range(len(result)):
                    ip_port=str(result[i])+':'+str(port[i])
                    if ip_port not in self.ip_list:
                        self.ip_list.append(ip_port)
        except Exception as e:
            print('第%s页抓取失败' % page)
        else:
            print('第%s页抓取完成' % page)

if __name__ == '__main__':
    spider=httpProxySpider()
    spider.work(3)