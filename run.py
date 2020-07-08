from lxml import etree
from urllib import parse
import requests

base_url = 'https://store.steampowered.com/search/'
ua = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
url_dic = {
	'filter':'topsellers',
	'os':'win'
}
url = "{}?{}".format(base_url,parse.urlencode(url_dic))

with requests.get(url,headers={'User-agent':ua}) as response:
	content = response.text #HTML内容
	html = etree.HTML(content)#分析HTML，返回DOM根节点
	topsellers_list_name = html.xpath('//*[@class="col search_name ellipsis"]//span[@class="title"]/text()')
	topsellers_list_price = html.xpath('//div[@class="col search_price  responsive_secondrow"]/text() | //div[@class="col search_price discounted responsive_secondrow"]/text()')

	'''1、第一次处理大量空格、换行符和空元素'''
	i = 0#处理topsellers_list_price中，存在的大量空格、换行符和空元素
	while i < len(topsellers_list_price):
		topsellers_list_price[i] = topsellers_list_price[i].strip()#处理空格
		topsellers_list_price[i] = topsellers_list_price[i].strip('\r\n')#处理换行符

		if topsellers_list_price[i] == '':
			del topsellers_list_price[i]
		i+=1

	'''2、第二次处理多余空格'''
	i = 0#处理topsellers_list_price中，多余的空格
	while i < len(topsellers_list_price):
		topsellers_list_price[i] = topsellers_list_price[i].replace(" ","")
		i+=1

	print("Steam当前热销榜为：")
	for i,temp in enumerate(zip(topsellers_list_name,topsellers_list_price)):
		list_num = i + 1
		print('-'*30)
		print("{}.{}".format(list_num,temp))
