import requests
import lxml.etree

start_url = "http://www.quanshuwang.com/book/111/111808"

response = requests.get(start_url)
response.encoding = "gbk"

html = lxml.etree.HTML(response.text)
chapters = html.xpath("//div[@class='clearfix dirconone']//li/a")

for chapter in chapters:
   chapterName = chapter.xpath("./text()")[0]
   chapterUrl = chapter.xpath("./@href")[0]

   response_2 = requests.get(chapterUrl)
   response_2.encoding = "gbk"

   html_2 = lxml.etree.HTML(response_2.text)
   chapterContent = "".join(html_2.xpath("//div[@id='content']/text()"))
   chapterContent = chapterContent.replace(r"\r\n","<br>")
   chapterContent = chapterContent.replace(r"\xa0", "&nbsp")
   print(chapterName)
   print(chapterContent)
   print("##########################################################")

