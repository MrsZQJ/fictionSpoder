import requests
from lxml import etree
import sys

class BiqugeSpider():
    def __init__(self,fiction_name,url):
        self.baseUrl = url
        self.fiction_name = fiction_name
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        self.send_url = "https://www.mcmssc.com/search.html?name={}".format(fiction_name)

    def send_req(self,to):
        if to:
            self.send_url = to
        r = requests.get(self.send_url,headers=self.headers)
        return r.content.decode()

    def dispose_data_one(self,datas):
        html = etree.HTML(datas)
        url_one = html.xpath("//span[@class='s2 wid']/a/@href")
        url_one = self.baseUrl.format(url_one[0])
        return url_one

    def dispose_data_two(self,datas):
        html = etree.HTML(datas)
        url_list = html.xpath("//div[@id='list']/dl/dd[position()>12]/a/@href")
        return url_list

    def dispose_data_three(self,datas):
        html = etree.HTML(datas)
        tit = html.xpath("//div[@class='bookname']/h1/text()")
        con = html.xpath("//div[@id='content']/text()")
        return tit[0],con

    def save_txt(self,tit,con):
        cons = con
        del cons[0:1]
        with open("aa.txt","a",encoding="utf-8") as f:
            f.write('\n')
            f.write("     ")
            f.write(tit)
            for i in cons:
                f.write(i)
                f.write('\n')

    def run(self):
        html_str = self.send_req(False)
        url_one = self.dispose_data_one(html_str)
        html_str = self.send_req(url_one)
        url_list = self.dispose_data_two(html_str)
        # url_list = ['/0_247/137806.html']
        for i in url_list:
            url_name = self.baseUrl.format(i)
            html_strs = self.send_req(url_name)
            tit,con = self.dispose_data_three(html_strs)
            self.save_txt(tit,con)

if __name__ == '__main__':
    url = "https://www.mcmssc.com{}"
    fict_name = sys.argv[1]
    fictions = BiqugeSpider(fict_name,url)
    fictions.run()