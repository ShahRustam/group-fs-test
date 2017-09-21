from selenium import webdriver
from time import sleep

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
driver.get("http://165.227.187.95")
driver.find_element_by_xpath("//input[@id='email']").send_keys("rustam@shakh.co")
driver.find_element_by_xpath("//input[@id='password']").send_keys("123456")
driver.find_element_by_xpath("//button").click()
sleep(3)
tablesLinks = driver.find_elements_by_xpath("//a[@class='nav-link ']")
countTables = len(tablesLinks)
tablesLinks[countTables / 2 - 1].click()
sleep(3)
jsonData = {}
pageBreak = True
while pageBreak:
    tableData = driver.find_elements_by_xpath("//tbody/tr")
    for trRow in tableData:
        inputsRow = trRow.find_elements_by_xpath("./td/input")
        for inputRow in inputsRow:
            id = inputRow.get_attribute("id")
            mongoID = id.split("__")[0]
            fieldName = id.split("__")[1].split(id.split("__")[1].split('-')[0] + "-")[1]
            if jsonData.get(mongoID) is None:
                jsonData[mongoID] = {}
            jsonData[mongoID][fieldName] = inputRow.get_attribute("value")
    nextPage = driver.find_element_by_xpath("//ul[@class='pagination']/li[contains(@class,'next')]")
    if "disabled" not in nextPage.get_attribute("class"):
        nextPage.find_element_by_xpath("./a").click()
    else:
        pageBreak = False

#print jsonData

print "Count of found rows: " + str(len(jsonData.keys()))
driver.quit()
