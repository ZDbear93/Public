import os, webbrowser, bs4, re, openpyxl, datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pythonJobs = [['Id','Title','Company','Location','Link','Timestamp']]
rootURL = 'https://pythonjob.xyz'
URL = 'https://pythonjob.xyz/jobs/all/United%20States%20of%20America/all/all'
driver = webdriver.Chrome()
driver.get(URL)
masterfile = ## full path of excel file
soup=bs4.BeautifulSoup(driver.page_source,'html.parser')

def main():
    def scrape():
        soup=bs4.BeautifulSoup(driver.page_source,'html.parser')
        id = ''
        for posting in soup.find_all('div', attrs={'class':'job-header shadow-xs'}):
            company = posting.find('a', href=True, title=re.compile('Python Jobs at.*')).get('title').replace('Python Jobs at ','')
            link = rootURL + posting.find('a', href=True, class_=False).get('href')
            location = posting.find(class_=re.compile('ml-2 leading-4.*')).get_text()
            title = posting.find('h2', attrs={'itemprop':'title'}).get_text()
            timestamp = datetime.datetime.now()
            pythonJobs.append([id,title,company,location,link,timestamp])
    pageNum=1
    while True:
        print('Scraping page: ' + str(pageNum))
        scrape()
        soup=bs4.BeautifulSoup(driver.page_source,'html.parser')
        if soup.find_all('a',class_=re.compile('.*border-teal.*text-white.*')):
            for el in soup.find_all('a',class_=re.compile('.*border-teal.*text-white.*')):
                if re.compile('.*More Python Jobs.*').search(str(el)):
                    nextpage = el.get('href')
                else:
                    nextpage = ''
        else: nexpage = ''
        link = rootURL + nextpage
        if link != rootURL:
            driver.get(link)
        else:
            break
        pageNum += 1
    driver.close()

    id = 1
    for record in pythonJobs[1:]:
        record[0] = id
        id += 1

    if os.path.exists(masterfile):
        os.remove(masterfile)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Jobs'
    ws = wb['Jobs']
    for record in pythonJobs:
        ws.append(record)
    wb.save(masterfile)
    return 0
main()
