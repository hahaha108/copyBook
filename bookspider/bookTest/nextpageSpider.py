import requests
import lxml.etree

list = []

def getNext(url):
    response = requests.get(url)
    response.encoding = "gbk"

    html = lxml.etree.HTML(response.text)

    nextUrl = html.xpath("//a[@class='next']/@href")
    list.append(url)

    if nextUrl:
        nextUrl = nextUrl[0]
        getNext(nextUrl)
    return list

if __name__ == '__main__':
    startUrl = "http://www.quanshuwang.com/list/2_240.html"
    print(getNext(startUrl))
