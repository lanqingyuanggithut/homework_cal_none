# -*- coding: utf-8 -*-
import requests
import codecs
from bs4 import BeautifulSoup

def main():
    titles = []
    for i in range(1, 29):
        url = 'https://blog.csdn.net/blogdevteam/article/list/'+str(i)
        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'html.parser')

        para = bs.find('div', attrs={'class': "article-item-box csdn-tracking-statistics"})

        for j in range(20):
            try:
                title = para.find('h4').find('a').text.strip()
                title = str("[") + title[0] + str("]") + title[1:].strip()
                titles.append(title)
                print(title)
                para = para.find_next_sibling()
            except:
                break

    f = codecs.open('csdn_crawl.txt','w','utf-8')
    for title in titles:
        f.write(title+'\n')
 
if __name__ == '__main__':
    main()