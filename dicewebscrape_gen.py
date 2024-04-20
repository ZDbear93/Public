import os, webbrowser, bs4, re, openpyxl, datetime, time, logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    diceListings = []
    rootURL = 'https://www.dice.com/job-detail/'
    URL = 'https://www.dice.com/jobs?location=Chicago,%20IL,%20USA&latitude=41.8781136&longitude=-87.6297982&countryCode=US&locationPrecision=City&adminDistrictCode=IL&radius=30&radiusUnit=mi&page=1&pageSize=100&language=en&eid=4676'
    driver = webdriver.Chrome()
    driver.get(URL)

    masterfile = ## full path of excel spreadsheet
    jobXPATH = '/html/body/dhi-js-dice-client/div/dhi-search-page-container/dhi-search-page/div/div[2]/dhi-search-page-results/div/div[3]/js-search-display/div/div[3]/dhi-search-cards-widget/div/dhi-search-card[1]/div/div[1]/div/div[2]/div[1]/h5/a'
    nextpageXPATH = '/html/body/dhi-js-dice-client/div/dhi-search-page-container/dhi-search-page/div/div[2]/dhi-search-page-results/div/div[3]/js-search-display/div/div[4]/div[1]/js-search-pagination-container/pagination/ul/li[7]/a'
    jobTotalXPATH = '/html/body/dhi-js-dice-client/div/dhi-search-page-container/dhi-search-page/div/div[2]/dhi-search-page-results/div/div[1]/div/div/h4/span'
    
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, jobXPATH)))
    soup=bs4.BeautifulSoup(driver.page_source,'html.parser')
    
    def scrape():
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, nextpageXPATH)))
        soup=bs4.BeautifulSoup(driver.page_source,'html.parser')
        id = ''
        for posting in soup.find_all('dhi-search-card'):
            try:
                title = posting.find('a', attrs={'data-cy':'card-title-link'}).get_text().strip()
                company = posting.find('a', attrs={'data-cy':'search-result-company-name'}).get_text().strip()
                location = posting.find('span', class_='search-result-location').get_text().strip()
                link  = rootURL + posting.find('a', attrs={'data-cy':'card-title-link'}).get('id')
                timestamp = datetime.datetime.now()
                diceListings.append([id,title,company,location,link,timestamp])
            except:
                if __name__ == "__main__":
                    logging.basicConfig(level=logging.DEBUG, filename="dicelog", filemode="a+",
                                        format="%(asctime)-15s %(levelname)-8s %(message)s")
                    logging.info("Error extracting from element" + str(posting))
    def nextPage(page):
        soup=bs4.BeautifulSoup(driver.page_source,'html.parser')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, nextpageXPATH)))
        driver.get('https://www.dice.com/jobs?location=Chicago,%20IL,%20USA&latitude=41.8781136&longitude=-87.6297982&countryCode=US&locationPrecision=City&adminDistrictCode=IL&radius=30&radiusUnit=mi&page=' + str(page) +'&pageSize=100&language=en&eid=4676')
    
    jobLowBound = 1
    jobUpBound = 100
    jobTotal = int(soup.find('span', attrs={'data-cy':'search-count-mobile'}).get_text().replace(',',''))

    page=1
    while jobUpBound <= jobTotal:
        print('Scraping ' + str(jobLowBound) + ' - ' + str(jobUpBound) + ' of ' + str(jobTotal) + ' Jobs')
        scrape()
        nextPage(page)
        if jobUpBound == jobTotal:
            break
        jobLowBound += 100
        jobUpBound = min(jobUpBound + 100, jobTotal)
        page += 1
    driver.close()

    id = 1
    for record in diceListings:
        record[0] = id
        id += 1

    wb = openpyxl.load_workbook(masterfile)
    ws = wb.active
    ws.title = 'Jobs'
    ws = wb['Jobs']
    for record in diceListings:
        ws.append(record)
    wb.save(masterfile)
        
main()
