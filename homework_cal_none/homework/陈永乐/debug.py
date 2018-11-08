# -*- coding: utf-8 -*-
import requests
import codecs
from bs4 import BeautifulSoup #模块名是bs4

def main():
    titles = []
    for i in range(1, 29):
        url = 'https://blog.csdn.net/blogdevteam/article/list/'+str(i) #应把i转成字符串类型
        response = requests.get(url)
        bs = BeautifulSoup(response.content, 'lxml')#BeautifulSoup指定模式'lxml'

        para = bs.find('div', attrs={'class': "article-item-box csdn-tracking-statistics"})

        for j in range(20):
            try:
                title = para.find('h4').find('a').text.strip()
                title = "[" + title[0] + "]" + title[1:].strip()#int("[")不对
                titles.append(title)
                print(title)        #print使用错误
                para = para.find_next_sibling()
            except:
                break

    f = codecs.open('csdn_crawl.txt','a','utf-8')#只读模式应该改为追加模式
    for title in titles:
        f.write(title+'\n')#缩进
    f.close() #没有关闭文件


if __name__ == '__main__':#缺了双下划线
    main()