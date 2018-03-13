import requests
import lxml.etree

start_url = "http://www.quanshuwang.com/"

response = requests.get(start_url)
response.encoding = "gbk"
# print(response.text)

html = lxml.etree.HTML(response.text)

categorys = html.xpath("//ul[@class='channel-nav-list']/li/a")

for category in categorys:
    url = category.xpath("./@href")[0]
    name = category.xpath("./text()")[0]
    print(name,":",url)
    print("----------------------------------------")
