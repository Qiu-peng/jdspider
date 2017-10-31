# -*- coding: utf-8 -*-
import re
import urllib

import scrapy
import jsonpath
import json
from jd.items import JdItem
from scrapy.spiders import CrawlSpider
class JdsSpider(scrapy.Spider):
    name = 'jds'
    allowed_domains = ['jd.com']
    start_urls = ['https://dc.3.cn/category/get?callback=getCategoryCallback']

    # 从首页分类 进入分类列表页
    def parse(self, response):
        res = response.replace(body = response.body.decode(response.encoding).encode('utf-8'), encoding = 'utf-8', url = response.url)
        a = response.text.index('(')
        res = response.text[a+1:-1]
        json_obj = json.loads(res)
        n_list = jsonpath.jsonpath(json_obj,'$.data[:].s[:].s[:].s[:].n')

        a = [i.split('|')[0] for i in n_list if i.split('|')[0] !='']
        c = [i.split('|') for i in n_list if i.split('|')[0] !='']

        b = [['list.jd.com/list.html?cat=' + i[0].replace('-',','),i[1]] if '-' in i[0] and 'html' not in i[0] else i for i in c ]

        for item in b:
            yield scrapy.Request('https://' + item[0],meta={'cate':item[1]} ,callback=self.parse_list)

    def parse_list(self,response):
        # 对活动页面进行处理
        try:
            # 第一种匹配规则,适应电脑分类
            pd_list_str1 = re.findall(r'aosList =(.+?);',response.text)[0]
            pd_list_str2 = re.findall(r'attrList =(.+?);',response.text)[0]
            pd_list_str = pd_list_str1 + pd_list_str2
        except Exception as e:
            print('[',e,']'+'其他规则页面',response.url)
        else:
            print('获取价格信息中...')
            # 获取列表的sku_id
            keys_list = list(set(re.findall(r'(\d+?):',pd_list_str)))
            keys_list_str =''
            for pid in keys_list:
                keys_list_str += 'J_'+pid+'%2C'
                print(pid)
            print('====')
            yield scrapy.Request('https://p.3.cn/prices/mgets?skuIds='+keys_list_str,
                                 meta={'cate':response.meta['cate']},
                                 callback=self.parse_items)
            # 翻页
            next_link = response.xpath('//span[@class="p-num"]/a[@class="pn-next"]/@href').extract()
            if next_link:
                print('****')
                # print('进入下一页中...'+'https://list.jd.com'+next_link[0])
                yield scrapy.Request('https://list.jd.com'+next_link[0], meta={'cate':response.meta['cate']}, callback=self.parse_list)

    def parse_items(self,response):
        print('封装该页商品信息中...')
        cate = response.meta['cate']
        json_obj = json.loads(response.text())
        for pd in json_obj:
            item = JdItem()
            item['pid'] = pd['id'][2:]
            item['cate'] = cate
            item['price'] =pd['p']
            item['link'] = 'item.jd.com/'+item['pid']+'.html'
            print(item)
            yield item # 不需要采集商品标题
            # 需要采集商品标题
            # yield scrapy.Request(item['link'],meta={'item':item},callback=self.parse_title)

    def parse_title(self,response):
        item = response.meta['item']
        title = response.xpath('//div[@class="itemInfo-wrap"]/div[@class="sku-name"]/text()').extract()[0]
        item['title'] = title
        yield item