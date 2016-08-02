# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 22:49:50 2016

@author: Franklin
"""

#syntax to set the environment, or get color of fonts
import time
import datetime
from selenium import webdriver
chromepath=r"/Users/Franklin/Downloads/chromedriver"
driver=webdriver.Chrome(chromepath)


#Expedia!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#driver.get("https://www.expedia.com/Hotel-Search?#&destination=Chicago (and vicinity), Illinois, United States of America&startDate=06/28/2016&endDate=06/29/2016&regionId=178248&adults=2")
panelTotalData = {}
webSite = "https://www.expedia.com/Hotel-Search?#&destination=Chicago (and vicinity), Illinois, United States of America&startDate="

count_num = 0

for timeExpandOfPanelData in range(20):
    startDateFormat = datetime.datetime.now() + datetime.timedelta(days=timeExpandOfPanelData)
    startDate = startDateFormat.strftime("%m/%d/%Y")                                                            #"06/28/2016"
    endDate = (startDateFormat + datetime.timedelta(days=1)).strftime("%m/%d/%Y")          #"06/29/2016"
    rest = "&regionId=178248&adults=2&page="
    
    startWebsite = webSite + startDate + "&endDate=" + endDate + rest + str(1)
    driver.get(startWebsite)
    time.sleep(5)
    
    totalHotelString = driver.find_elements_by_class_name("section-header-main")
    
    for number in totalHotelString:
        numberContainer = number.text
        totalHotelNumber = [int(s) for s in numberContainer.split() if s.isdigit()]
   
    count_num = count_num + 1
    print (count_num)
    pages = range( int( totalHotelNumber[0]/50 ) + 1 )
    allWebSiteLoop = list()

    for page in pages:
        allWebSiteLoop.append( webSite + startDate + "&endDate=" + endDate + rest + str(page+1) )

    panelData = {}
    for web in allWebSiteLoop:
        driver.get(web)
        time.sleep(5)
        #hotels = driver.find_elements_by_class_name("hotelName")
        hotels= driver.find_elements_by_xpath("//span[@class='hotelName']")
        #prices = driver.find_elements_by_xpath("//span[@class='actualPrice fakeLink' or @class='badge badge-urgent badge-notification soldOutMsg soldOutGeneral']")
       # totalNumber = driver.find_elements_by_class_name("hotelTitle")
        prices = driver.find_elements_by_xpath("//*[@class='actualPrice fakeLink' or (@class = 'error' and @class='badge badge-urgent badge-notification soldOutMsg soldOutGeneral') or @class='errorText' or @class='error']")
        a = list()
        b = list()
        for hotel in hotels:
            a.append(hotel.text)
        for price in prices:
            b.append(price.text)
            
        b = [x for x in b if ( (bool(x)) and ('/' not in x) )]

        
        for count in range(len(b)):
                panelData.update( { a[count]: [ b[count] ]} ) 
    
    for element in panelData:
        if panelTotalData.setdefault(element,[]):
            panelTotalData.setdefault(element, []).append( ",".join(str(x) for x in panelData[element]) )
        else:
            panelTotalData.update({ element: panelData[element] })

# filter invalidData
for element in panelTotalData:
    stayList = []
    stayList = [i for i in range( len(panelTotalData[element]) ) if panelTotalData[element][i].startswith("$")]
    panelTotalData[element] = [i for j, i in enumerate(panelTotalData[element]) if j in stayList]
    panelTotalData[element] = [ int(validValue.replace('$', '').replace(',', '')) for validValue in panelTotalData[element] ]

print (panelTotalData)

for element in panelTotalData:
    panelTotalData[element.replace(',', '')] = panelTotalData.pop(element)

with open('hotelTimeSeries.csv', 'w') as f:
    for i in panelTotalData.keys():   
            f.write(i + ',' + ','.join(str(x) for x in panelTotalData[i]) + "\n")