# -*- coding: utf-8 -*-
# author: Jason Xiao


import urllib2
import re
import time
import smtplib
import concurrent.futures
import signal
import datetime

from selenium import webdriver
 

class SwitchNotifier():
    def __init__(self):
        self.urls = [
        "http://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/5670100.p?skuId=5670100",
        "http://www.target.com/p/-/A-52189185",
        "http://www.gamestop.com/nintendo-switch/consoles/nintendo-switch-console-with-neon-blue-and-neon-red-joy-con/141887",
        "http://www.toysrus.com/product/index.jsp?productId=119513666&cp=2255974.119659196&parentPage=family",
        ]

        # self.urls = [
        # "http://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/5670100.p?skuId=5670100",
        # "http://www.target.com/p/the-legend-of-zelda-153-breath-of-the-wild-153-nintendo-switch/-/A-52161264?lnk=rec|pdpipadh1|related_prods_vv|pdpipadh1|52161264|0",
        # "http://www.gamestop.com/nintendo-switch/games/the-legend-of-zelda-breath-of-the-wild/141904",
        # "http://www.toysrus.com/product/index.jsp?productId=119513686&ab=TRU:tproduct_rr:Customers%20Also%20Liked:1"        
        # ]

        self.keywords = [
        'data-purchasable="true"',
        'add to cart',
        'lnkAddToCart',
        'stock avail'
        ]

        self.message = ""


    def getAvailability(self, url, keyword, driver):

        driver.get(url) 
        print datetime.datetime.now(), "get url done"
        # will print the page source
        data = driver.page_source

        print datetime.datetime.now(), "get page done"
        pattern = re.compile(keyword,re.S)
        print datetime.datetime.now(), "get pattern done"
        avail = re.search(pattern,data)
        print datetime.datetime.now(), "search keyword done"
        if avail is not None:
            print url, True
            print avail
            self.message += url + "\n\n"
        else:
            print url, False
    
    # sendEmail method from:
    # https://www.mkyong.com/python/how-do-send-email-in-python-via-smtplib/
    def sendEmail(self, msg):
        to = 'xxxxxxx@gmail.com'
        # enter your email address and password
        gmail_user = 'yyyyyyyyy@gmail.com'
        gmail_pwd = '**********'
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: Switch re-stock! \n'
        print header
        message = header + '\n' + msg + '  \n\n'
        smtpserver.sendmail(gmail_user, to, message)
        print 'done!'
        smtpserver.close()

    def start(self):
        service_args = [
            '--load-images=no',
            # '--disk-cache=yes',
        ]
        driver = webdriver.PhantomJS(service_args=service_args) 

        searcher = concurrent.futures.ThreadPoolExecutor(16)
        futures_search = [searcher.submit(self.getAvailability, self.urls[i], self.keywords[i], driver) for i in range(0, len(self.urls))]
        concurrent.futures.wait(futures_search)

        driver.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
        driver.quit()   
        # for i in range(0, 4):
        #     self.getAvailability(self.urls[i], self.keywords[i])
        # self.getAvailability(self.urls[0], self.keywords[0])
 
        if self.message:
            self.sendEmail(self.message)




notifier = SwitchNotifier()
# test.getAvailability(url, keyword)
notifier.start()
