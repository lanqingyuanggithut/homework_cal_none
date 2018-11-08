# -*- coding: utf-8 -*-
import requests
import codecs
from bs4 import BeautifulSoup 
#ModuleNotFoundError: No module named 'bs'

def main():
    titles = []
    for i in range(1, 29):
        #TypeError: can only concatenate str (not "int") to str
        url = ('https://blog.csdn.net/blogdevteam/article/list/'+str(i))
        response = requests.get(url) 
        #NameError: name 'html' is not defined,指定使用哪种解析器: 'html.parser'
        bs = BeautifulSoup(response.content, 'html.parser')
        para = bs.find('div', attrs={'class': "article-item-box csdn-tracking-statistics"})

        for j in range(20):
            try:
                title = para.find('h4').find('a').text.strip()
                title = "[" + str(title[0]) + "]" + title[1:].strip()
                titles.append(title)
                print (title) ##加括号
                para = para.find_next_sibling()
            except Exception as e:
                print(e)
                break
   ###codecs.open(filepath,method,encoding)
    f = codecs.open('csdn_crawl.txt','w','utf-8') 
    for title in titles:
        f.write(title+'\n')#IndentationError:
   
#####__main__
if __name__ == '__main__':
    main()