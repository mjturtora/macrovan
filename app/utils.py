from secrets import *

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import ctypes  # An included library with Python install.


def pause(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Macrovan", 1)


def start_driver():
    """Initialize Chrome WebDriver with option to save user data to local
     folder to handle cookies"""
    # todo: check for valid (up-to-date) webdriver
    # driver.get('chrome://settings/')
    # driver.set_window_size(1210, 720)

    # https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver

    chrome_options = Options()

    # todo: following lines added 7/8 trying to make repo pretty. Gave up. Maybe later.
    # Or maybe someone else can tell what I was trying to do and make it work. :)
    # chrome_options.add_argument(r"--user-data-dir='..\io\chrome-data'")
    # #chrome_options.add_argument("--enable-caret-browsing")
    # driver = webdriver.Chrome(r'..\io\drivers\chromedriver 83', options=chrome_options)
    # # adding argument opens with address bar highlighted and I can't figure out why!
    # #driver = webdriver.Chrome('./chromedriver 83')

    chrome_options.add_argument("--user-data-dir=chrome-data")
    driver = webdriver.Chrome('./chromedriver 83', options=chrome_options)

    return driver


def print_title(driver):
    print("Driver title is: \n", driver.title)


def get_page(driver):
    # Get webpage
    driver.get('https://www.votebuilder.com/Default.aspx')
    print_title(driver)
    return


def login_to_page(driver):
    # login and initialize:
    # Click ActionID Button to open login

    wait_no_longer_than = 30
    element = WebDriverWait(driver, wait_no_longer_than).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="/OpenIdConnectLoginInitiator.ashx?ProviderID=4"]')))
    #print(f'ELEMENT = {element}')

    driver.find_element_by_xpath("//a[@href='/OpenIdConnectLoginInitiator.ashx?ProviderID=4']").click()
    print('After ActionID Button')
    print_title(driver)

    wait_no_longer_than = 30
    element = WebDriverWait(driver, wait_no_longer_than).until(
                EC.presence_of_element_located((By.ID, 'username')))
    #print(f'ELEMENT = {element}')

    username = driver.find_element_by_id("username")
    username.send_keys(user_name)
    password = driver.find_element_by_id("password")
    password.send_keys(pass_word)
    driver.find_element_by_class_name("btn-blue").click()

    #wait_no_longer_than = 30
    # element = WebDriverWait(driver, wait_no_longer_than).until(
    #             EC.presence_of_element_located((By.ID,
    #             "ctl00_ContentPlaceHolderVANPage_VANDetailsItemPIN_VANInputItemDetailsItemPINCode_PINCode")))
    #
    # driver.find_element(
    #     By.NAME,
    #     "ctl00$ContentPlaceHolderVANPage$VANDetailsItemPIN$VANInputItemDetailsItemPINCode$PINCode"
    #     ).click()
    # driver.find_element(
    #     By.NAME,
    #     "ctl00$ContentPlaceHolderVANPage$VANDetailsItemPIN$VANInputItemDetailsItemPINCode$PINCode"
    #     ).send_keys('fdsfds')  #Keys.NULL)

    # element = driver.find_element_by_id(
    #     'ctl00_ContentPlaceHolderVANPage_VANDetailsItemPIN_VANInputItemDetailsItemPINCode_PINCode'
    #     )
    #
    # ActionChains(driver).move_to_element(element).perform()
    return


def remember_this(driver):
    driver.find_element_by_class_name("checkbox").click()
    # wait at least long enough to enter code and pin
    #driver.implicitly_wait(25)


def list_folders(driver):
    # List "My Folders" and select folder:
    wait_no_longer_than = 60
    element = WebDriverWait(driver, wait_no_longer_than).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="FolderList.aspx"]')))
    #print(f'ELEMENT = {element}')
    driver.find_element_by_xpath('//a[@href="FolderList.aspx"]').click()
    print('AFTER FOLDER LIST CLICK')


def select_folder(driver):
    print('Select Folder')
    #driver.find_element_by_xpath('//*[text()="District 68 2020 3/17 Primary/Municipals"]').click()
    driver.find_element_by_xpath('//*[text()="2020 District 68"]').click()
    print_title(driver)


def select_turf(driver, turf_name):
    print('Select Saved Search')
    driver.find_element_by_xpath('//*[text()="' + turf_name + '"]').click()


def handle_alert(driver):
    """Are you sure you want to load this Map Turf
    and overwrite your current version of My List"""
    obj = driver.switch_to.alert
    obj.accept()
    print_title(driver)


def edit_search(driver):
    # Edit Search:
    print('Edit Search')
    driver.find_element_by_xpath('//button[normalize-space()="Edit Search"]').click()


#Returns list of turf name and last name pairs under a provided captain
def getTurfsByCaptain(captain, turf_data):
    try:
        return turf_data[captain]
    except KeyError:
        print("Turf captain doesn't exist: " + captain[0] + " " + captain[1])


#Returns list of all turf name and last name pairs
def getAllTurfs(turf_data):
    output = []
    for item in turf_data.values():
        output += item
    return output


#Return list of all block captains
def getAllCaptains(turf_data):
    output = []
    for item in turf_data.keys():
        output += [item]
    return output


def print_list(driver, listName):
    #Print a List
    wait_no_longer_than=30
    print('in print_list waiting for print icon')
    element = WebDriverWait(driver, wait_no_longer_than).until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolderVANPage_HyperLinkImagePrintReportsAndForms")))
    #print(f'ELEMENT = {element}')

    print('in print_list about to click')

    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_HyperLinkImagePrintReportsAndForms").click()
    print('just clicked')
    pause("What happened?")

    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReportFormatInfo_VANInputItemDetailsItemReportFormatInfo_ReportFormatInfo").click()
    dropdown = driver.find_element(By.ID,
                                   "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReportFormatInfo_VANInputItemDetailsItemReportFormatInfo_ReportFormatInfo")
    dropdown.find_element(By.XPATH, "//option[. = '*2020 D68 VBM Enrollment']").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReportFormatInfo_VANInputItemDetailsItemReportFormatInfo_ReportFormatInfo").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemvdiScriptID_VANInputItemDetailsItemActiveScriptID_ActiveScriptID").click()
    dropdown = driver.find_element(By.ID,
                                   "ctl00_ContentPlaceHolderVANPage_VanDetailsItemvdiScriptID_VANInputItemDetailsItemActiveScriptID_ActiveScriptID")
    dropdown.find_element(By.XPATH, "//option[. = '2020 D68 VBM Enrollment']").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemvdiScriptID_VANInputItemDetailsItemActiveScriptID_ActiveScriptID").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemVANDetailsItemScriptSource_ScriptSource_VANInputItemDetailsItemScriptSource_ScriptSource").click()
    dropdown = driver.find_element(By.ID,
                                   "ctl00_ContentPlaceHolderVANPage_VanDetailsItemVANDetailsItemScriptSource_ScriptSource_VANInputItemDetailsItemScriptSource_ScriptSource")
    dropdown.find_element(By.XPATH, "//option[. = 'Walk']").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemVANDetailsItemScriptSource_ScriptSource_VANInputItemDetailsItemScriptSource_ScriptSource").click()
    # driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VANDetailsItemReportTitle_VANInputItemDetailsItemReportTitle_ReportTitle").click()
    # driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VANDetailsItemReportTitle_VANInputItemDetailsItemReportTitle_ReportTitle").send_keys("Test")
    element = driver.find_element_by_id(
        "ctl00_ContentPlaceHolderVANPage_VANDetailsItemReportTitle_VANInputItemDetailsItemReportTitle_ReportTitle")
    element.clear()
    element.send_keys(listName)
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder1_Header1").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder1_Break1").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder2_Header2").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder2_Break2").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder3_Break3").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder3_Header3").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_Header4").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_Break4").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_VANInputItemDetailsItemSortOrder4_SortOrder4").click()
    dropdown = driver.find_element(By.ID,
                                   "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_VANInputItemDetailsItemSortOrder4_SortOrder4")
    dropdown.find_element(By.XPATH, "//option[. = 'Street Number']").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_VANInputItemDetailsItemSortOrder4_SortOrder4").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder5_VANInputItemDetailsItemSortOrder5_SortOrder5").click()
    dropdown = driver.find_element(By.ID,
                                   "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder5_VANInputItemDetailsItemSortOrder5_SortOrder5")
    dropdown.find_element(By.XPATH, "//option[. = 'Apartment']").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder5_VANInputItemDetailsItemSortOrder5_SortOrder5").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6").click()
    dropdown = Select(driver.find_element_by_id(
        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6"))
    dropdown.select_by_index(0)
    # dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6")
    # dropdown.find_element(By.XPATH, "//option[. = 'label']").click()
    # driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6").click()
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemPrintMapNew_VANInputItemDetailsItemPrintMapNew_PrintMapNew_0").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_ButtonSortOptionsSubmit").click()
    driver.find_element(By.LINK_TEXT, "My PDF Files").click()
