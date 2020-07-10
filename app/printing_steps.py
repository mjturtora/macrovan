import os
import shutil
import glob
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# Initialize Chrome WebDriver
#opt = webdriver.ChromeOptions()
#opt.add_experimental_option('w3c', False)
#driver = webdriver.Chrome(chrome_options=opt)
driver = webdriver.Chrome('./chromedriver.exe')
# driver.get('chrome://settings/')
# driver.set_window_size(1210, 720)

# Get webpage
driver.get('https://www.votebuilder.com/Default.aspx')
print("Driver title is: \n", driver.title)

## login and initialize:
# Click ActionID Button to open login
driver.find_element_by_xpath("//a[@href='/OpenIdConnectLoginInitiator.ashx?ProviderID=4']").click();
print("Driver title is: \n", driver.title)
user_name = "***************"
pass_word = "****************"
username = driver.find_element_by_id("username")
username.send_keys(user_name)
password = driver.find_element_by_id("password")
password.send_keys(pass_word)
driver.find_element_by_class_name("btn-blue").click()

# driver.implicitly_wait(500)
WebDriverWait(driver, 100).until(EC.alert_is_present())
# driver.switch_to.alert.accept()

# driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_HyperLinkMenuSavedLists").click()
# driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(1) .grid-result").click()
# element = driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(4) .grid-result")
# actions = ActionChains(driver)
# actions.move_to_element(element).perform()
# driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(4) .grid-result").click()
# element = driver.find_element(By.CSS_SELECTOR, "body")
# actions = ActionChains(driver)
# actions.move_to_element(element, 0, 0).perform()

# assert driver.switch_to.alert.text == "Are you sure you want to load this Search and overwrite your current version of My List?"
driver.switch_to.alert.accept()

driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_HyperLinkImagePrintReportsAndForms").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReportFormatInfo_VANInputItemDetailsItemReportFormatInfo_ReportFormatInfo").click()
dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReportFormatInfo_VANInputItemDetailsItemReportFormatInfo_ReportFormatInfo")
dropdown.find_element(By.XPATH, "//option[. = '*2020 D68 VBM Enrollment']").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReportFormatInfo_VANInputItemDetailsItemReportFormatInfo_ReportFormatInfo").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemvdiScriptID_VANInputItemDetailsItemActiveScriptID_ActiveScriptID").click()
dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemvdiScriptID_VANInputItemDetailsItemActiveScriptID_ActiveScriptID")
dropdown.find_element(By.XPATH, "//option[. = '2020 D68 VBM Enrollment']").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemvdiScriptID_VANInputItemDetailsItemActiveScriptID_ActiveScriptID").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemVANDetailsItemScriptSource_ScriptSource_VANInputItemDetailsItemScriptSource_ScriptSource").click()
dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemVANDetailsItemScriptSource_ScriptSource_VANInputItemDetailsItemScriptSource_ScriptSource")
dropdown.find_element(By.XPATH, "//option[. = 'Walk']").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemVANDetailsItemScriptSource_ScriptSource_VANInputItemDetailsItemScriptSource_ScriptSource").click()
# driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VANDetailsItemReportTitle_VANInputItemDetailsItemReportTitle_ReportTitle").click()
# driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VANDetailsItemReportTitle_VANInputItemDetailsItemReportTitle_ReportTitle").send_keys("Test")
element = driver.find_element_by_id("ctl00_ContentPlaceHolderVANPage_VANDetailsItemReportTitle_VANInputItemDetailsItemReportTitle_ReportTitle")
element.clear()
element.send_keys('Insert Title Here')
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder1_Header1").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder1_Break1").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder2_Header2").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder2_Break2").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder3_Break3").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder3_Header3").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_Header4").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_Break4").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_VANInputItemDetailsItemSortOrder4_SortOrder4").click()
dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_VANInputItemDetailsItemSortOrder4_SortOrder4")
dropdown.find_element(By.XPATH, "//option[. = 'Street Number']").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_VANInputItemDetailsItemSortOrder4_SortOrder4").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder5_VANInputItemDetailsItemSortOrder5_SortOrder5").click()
dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder5_VANInputItemDetailsItemSortOrder5_SortOrder5")
dropdown.find_element(By.XPATH, "//option[. = 'Apartment']").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder5_VANInputItemDetailsItemSortOrder5_SortOrder5").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6").click()
dropdown = Select(driver.find_element_by_id("ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6"))
dropdown.select_by_index(0)
# dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6")
# dropdown.find_element(By.XPATH, "//option[. = 'label']").click()
# driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemPrintMapNew_VANInputItemDetailsItemPrintMapNew_PrintMapNew_0").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_ButtonSortOptionsSubmit").click()
driver.find_element(By.LINK_TEXT, "My PDF Files").click()