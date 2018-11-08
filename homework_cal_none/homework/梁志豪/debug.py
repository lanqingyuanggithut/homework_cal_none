# -*- coding: utf-8 -*-
import requests
import codecs
from bs4 import BeautifulSoup

def main():
    titles = []
    for i in range(1, 29):
        url = 'https://blog.csdn.net/blogdevteam/article/list/%s'%i  
        #字符串中含有变量，使用占位符%s后用%衔接变量
        response = requests.get(url)
        bs = BeautifulSoup(response.content, "html.parser") #bs( ,“html.parser”)

        para = bs.find('div', attrs={'class': "article-item-box csdn-tracking-statistics"})

        for j in range(20):
            try:
                title = para.find('h4').find('a').text.strip()
                title = str("[") + title[0] + str("]") + title[1:].strip() 
                ##原错误为int()字符串
                titles.append(title)
                print(title)
                para = para.find_next_sibling()
            except:
                break

    f = codecs.open('csdn_crawl.txt','w','utf-8')  
    ##codes.open写入方式不对,应该为('filename','w\r\a','code')
    for title in titles:
        f.write(title+'\n') 

main()  
#注：原先按了步进也会跳过def函数，设置了断点依然跳过，
#根本没有参数传入当然跳过，因此在此引用函数才能步入检验

if __name__ == 'main':
    main()

#注实际上已转行，只是txt没有显示，用word或其他文本打开即可