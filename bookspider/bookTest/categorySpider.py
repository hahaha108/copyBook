import requests
import lxml.etree
import urllib

import os

response_1 = requests.get("http://www.quanshuwang.com/list/2_241.html")
response_1.encoding = "gbk"

html_1 = lxml.etree.HTML(response_1.text)

urls = html_1.xpath("//ul[@class='seeWell cf']/li/span/a[1]/@href")
for url in urls:
    response_2 = requests.get(url)
    response_2.encoding = "gbk"
    html_2 = lxml.etree.HTML(response_2.text)
    title = html_2.xpath("//div[@class='b-info']/h1/text()")[0]
    trueUrl = html_2.xpath("//div[@class='b-oper']/a[@class='reader']/@href")[0]
    author = html_2.xpath("//div[@class='bookDetail']/dl[@class='bookso']/dd[1]/text()")[0].strip()
    intro = html_2.xpath("//div[@id='waa']/text()")[0].strip()
    imgUrl = html_2.xpath("//a[@class='l mr11']/img/@src")[0]

    filename = title + '.jpg'
    dirpath = './cover'
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = os.path.join(dirpath,filename)
    urllib.request.urlretrieve(imgUrl,filepath)

    cover = 'cover/' + filename
    print(title,":",trueUrl,author,'\n',intro,cover)
    print("-----------------------------------------------")
