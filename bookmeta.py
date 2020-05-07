from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib import request 
import click
import os
import time
import json

class BookMeta:
    def __init__(self,dwdir=None):
        self.url='https://search.douban.com/book/subject_search?search_text='
        self.timeout=10
        self.browser=webdriver.Chrome('C:/Users/tengy14/AppData/Local/Google/Chrome/Application/chromedriver')
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.dwdir=dwdir
        self.info=[]
    
    def buildinfo(self):
        infodir='%s/book.json' % self.dwdir
        open(infodir,'w',encoding='utf-8').writelines(json.dumps(self.info,ensure_ascii=False))

    def quit(self):
        self.browser.quit()


    def get(self,name):
        self.browser.get(self.url+name)
        for div in self.browser.find_elements_by_css_selector('div.item-root'):
            try:
                title=div.find_element_by_css_selector('div.title a').text
                try:
                    rating=div.find_element_by_css_selector('span.rating_nums').text
                except:
                    rating=0
                start=div.find_element_by_css_selector('span.rating-stars').get_attribute('class').replace('rating-stars','').replace('allstar','')
                info=div.find_element_by_css_selector('div.meta.abstract').text.split('/')
                cover=div.find_element_by_css_selector('img.cover').get_attribute('src')
                price=0
                pubdate=''
                publisher=''
                author=''
                if len(info)>3:
                    price=info[-1]
                    pubdate=info[-2].strip()
                    publisher=info[-3].strip()
                    author='/'.join(info[0:-3]).strip()
                else:
                    price=info[-1]
                    author=info[0].strip()
                book= {
                    'input':name,
                    'title':title,
                    'rating':float(rating),
                    'start':int(start)/10,
                    'cover':cover,
                    'price':price,
                    'pubdate':pubdate,
                    'publisher':publisher,
                    'author':author
                }
                try:
                    if self.dwdir:
                        if not os.path.exists(self.dwdir):
                            os.mkdir(self.dwdir)
                        else:
                            if not os.path.isdir(self.dwdir):
                                self.dwdir=self.dwdir+time.strftime("-%Y%m%d%H%M%S", time.localtime())
                                os.mkdir(self.dwdir)
                    request.urlretrieve(cover,os.path.join(self.dwdir,cover.split('/')[-1]))
                except Exception as e:
                    print('Save %s cover failure. Err:%s'%(title,str(e)))
                self.info.append(book)
                return book
            except Exception as e:
                #print(str(e))
                continue
        book={"input":name}
        self.info.append(book)
        return book

@click.command()
@click.option('--name',help='a name list to get book meta split by ","')
@click.option('--path',default=None,help='the path to save book cover,default is None (do not save cover)')
def getmeta(name,path=None):
    meta=BookMeta()
    for x in name.split(','):
        print(meta.get(x,path))
    meta.quit()

