from secrets import *
import os
import io
import sys
import glob
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.command import Command
import ctypes  # for windows message pop-up

def get_os():
    # print(sys.platform)
    if "win" in sys.platform:
        # print("os = Windows")
        return "Windows"


def teardown():
    """Remove temp files from prior run before starting driver"""

    print('Start Teardown')
    if get_os() == "Windows":
        print("Do Windows")
        windowsUser = os.getlogin()
        for path in glob.iglob(os.path.join('C:\\', 'Users', windowsUser, 'AppData', 'Local', 'Temp', 'scoped_dir*')):
            print(path)
            shutil.rmtree(path)

        for path in glob.iglob(os.path.join('C:\\', 'Users', windowsUser, 'AppData', 'Local', 'Temp', 'chrome_BITS_*')):
            print(path)
            shutil.rmtree(path)
    print('Teardown complete')

def pause(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Macrovan", 1)


def start_driver():
    """Initialize Chrome WebDriver with option that saves user-data-dir to local
     folder to handle cookies"""
    # driver.get('chrome://settings/')
    # driver.set_window_size(1210, 720)

    # https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver

    chrome_options = Options()

    # todo: following lines added 7/8 trying to make repo pretty.
    #  Trying to save chrome-data elsewhere. Gave up. Maybe later.
    # chrome_options.add_argument(r"--user-data-dir='..\io\chrome-data'")
    # #chrome_options.add_argument("--enable-caret-browsing")

    # adding argument causes chrome to open with address bar highlighted and I can't figure out why!
    chrome_options.add_argument("--user-data-dir=chrome-data")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
    chrome_options.add_argument('disable-infobars')
    #display_to_console("Loading...")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    #display_to_console("Finished loading!")
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
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanInputItemviiFilterName_VanInputItemviiFilterName").send_keys(turf_name)
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_RefreshFilterButton").click()
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

def early_voting_twisty(driver):
    # some wait needed for page to load...
    wait_no_longer_than = 10
    # to click Early Voting Twisty
    element = WebDriverWait(driver, wait_no_longer_than).until(
        EC.presence_of_element_located((By.ID, 'ImageButtonSectionEarlyVoting')))
    print(f'Early Voting Section element located = {element}')
    driver.find_element(By.ID, "ImageButtonSectionEarlyVoting").click()


def notes_twisty(driver):
    wait_no_longer_than = 30
    element = WebDriverWait(driver, wait_no_longer_than).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ImageButtonSectionNotes"]')))
    print('Try to click "Notes" twisty')
    driver.find_element_by_xpath('//*[@id="ImageButtonSectionNotes"]').click()


# Returns list of turf name and last name pairs under a provided captain
def get_turfs_by_captain(captain, turf_dict):
    try:
        return turf_dict[captain]
    except KeyError:
        print("Turf captain doesn't exist: " + captain[0] + " " + captain[1])


# Returns list of all turf name and last name pairs
def get_all_turfs(turf_data):
    output = []
    for item in turf_data.values():
        output += item
    return output


# Return list of all block captains
def get_all_captains(turf_dict):
    output = []
    for item in turf_dict.keys():
        output += [item]
    return output


def turfselection_plus(driver, turf_name, captain_name):
    # ORIGINAL (SIDE) Test name: from turf selection

    # # SELECT OWNER (PRECINCT CAPTAIN) NAME
    # # On Folder page, click "owner" text entry field
    # driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_viiFilterOwner_rac_viiFilterOwner_Input").click()
    # # 9 | type | id=ctl00_ContentPlaceHolderVANPage_viiFilterOwner_rac_viiFilterOwner_Input | Law, Barbara
    # # Select Owners... (will need to cycle through list in outer loop)
    # # might want a try/except block here for owner not found:
    # driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_viiFilterOwner_rac_viiFilterOwner_Input").send_keys(captain_name)
    # # 10 | click | id=ctl00_ContentPlaceHolderVANPage_RefreshFilterButton (runs owner selection)
    # driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_RefreshFilterButton").click()

    # SELECT TURF NAME
    # use turf name selection method from macrovan
    print(f'Select turf_name = {turf_name}')
    select_turf(driver, turf_name)
    print('Handle erase current list alert')
    handle_alert(driver)

    # 14 | click | id=addStep |
    # Edit Search. Odd that this addStep works?
    driver.find_element(By.ID, "addStep").click()
    # 15 | click | id=stepTypeItem4 |
    # Narrow People (Selection from addStep dropdown)
    driver.find_element(By.ID, "stepTypeItem4").click()
    early_voting_twisty(driver)
    print('Click anyone Who Requested a Ballot')
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_EarlyVoteCheckboxId_RequestReceived").click()
    print('Click Preview Button')
    driver.find_element_by_id("ResultsPreviewButton").click()
    print("Driver title is: \n", driver.title)
    print('Click #AddNewStepButton')

    pause('Click Add New Step: Remove, and wait\n for page to load to continue')

    print('Unclick early voting twisty?')
    early_voting_twisty(driver)

    # click notes twisty
    notes_twisty(driver)

    print('Click in note text field. Is this needed?')
    driver.find_element(By.ID, "NoteText").click()
    print('Send keys to NoteText "*moved')
    driver.find_element(By.ID, "NoteText").send_keys("*moved")
    print(f'Sent keys *moved for remove step')

    # unclick notes_twisty
    notes_twisty(driver)

    # # This worked for notes before:
    # element = driver.find_element_by_id("ImageButtonSectionNotes").click()
    # print('Find NoteText')
    # element = driver.find_element_by_id('NoteText')
    # print('Send Keys: Voted')
    # element.send_keys('Voted')

    print('Run Search to Remove selected voters (Click Run Search Button)')
    element = driver.find_element_by_id("ctl00_ContentPlaceHolderVANPage_SearchRunButton").click()

    print("Driver title is: \n", driver.title)
    print("And done with SIDE function")


def print_list(driver, listName):
    # Print a List
    wait_no_longer_than = 30
    print('in print_list waiting for print icon')
    element = WebDriverWait(driver, wait_no_longer_than).until(
        EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolderVANPage_HyperLinkImagePrintReportsAndForms")))
    print('in print_list trying to click')
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_HyperLinkImagePrintReportsAndForms").click()
    print('just clicked print icon might need another EC')

    # Select Report Format Option
    # Locate the Sector and create a Select object
    print('Select Print Format Option')
    select_element = Select(driver.find_element_by_id(
        'ctl00_ContentPlaceHolderVANPage_VanDetailsItemReportFormatInfo_VANInputItemDetailsItemReportFormatInfo_ReportFormatInfo'
    )
    )
    element = select_element.select_by_visible_text("*2020 D68 Aug Primary")

    # Select Script Option
    # Locate the Sector and create a Select object
    select_element = Select(driver.find_element_by_id(
        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemvdiScriptID_VANInputItemDetailsItemActiveScriptID_ActiveScriptID"
    )
    )
    # print([o.text for o in select_element.options])
    element = select_element.select_by_visible_text('*2020 D68 Aug Primary')

    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemvdiScriptID_VANInputItemDetailsItemActiveScriptID_ActiveScriptID").click()

    # Script source selection (Walk)
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

    # Deselect Headers amd Breaks
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder1_Header1").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder1_Break1").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder2_Header2").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder2_Break2").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder3_Break3").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder3_Header3").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_Header4").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_Break4").click()

    # Sort Order 4
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_VANInputItemDetailsItemSortOrder4_SortOrder4").click()
    dropdown = Select(driver.find_element_by_id(
        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder4_VANInputItemDetailsItemSortOrder4_SortOrder4"))
    dropdown.select_by_index(4)

    # Sort Order 5
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder5_VANInputItemDetailsItemSortOrder5_SortOrder5").click()
    dropdown = Select(driver.find_element_by_id(
        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder5_VANInputItemDetailsItemSortOrder5_SortOrder5"))
    dropdown.select_by_index(5)

    # Sort Order 6
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6").click()
    dropdown = Select(driver.find_element_by_id(
        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemSortOrder6_VANInputItemDetailsItemSortOrder6_SortOrder6"))
    dropdown.select_by_index(0)

    # Submit
    driver.find_element(By.ID,
                        "ctl00_ContentPlaceHolderVANPage_VanDetailsItemPrintMapNew_VANInputItemDetailsItemPrintMapNew_PrintMapNew_0").click()
    pause("Double Check that selections are correct")
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_ButtonSortOptionsSubmit").click()
    driver.find_element(By.LINK_TEXT, "My PDF Files").click()

def return_to_folder(driver):
    driver.find_element(By.LINK_TEXT, "Home").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_HyperLinkMenuSavedLists").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(1) .grid-result").click()

#Close everything and cleanup
def exit_program(window, driver):
    try:
        window.destroy()
    except:
        print("Window does not exist!")
    else:
        print("Window closed!")

    try:
        driver.close
        driver.quit()
    except:
        print("Driver does not exist!")    
    else:
        print("Driver closed!")

    try:
        teardown()
    except:
        print("Teardown failed!")
    else:
        print("Teardown successfully ran!")

#Checks if the chrome browser is open or not closes everything if the chrome browser closed.
def check_browser(window, driver):
    if len(driver.get_log('driver')) > 0:
        if driver.get_log('driver')[0]['message'] == "Unable to evaluate script: disconnected: not connected to DevTools\n":
            exit_program(window, driver)
    else:
        window.after(1500, lambda: check_browser(window, driver))


def enable_print():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

def disable_print():
    text_trap = io.StringIO()
    sys.stdout = text_trap
    sys.stderr = text_trap

def display_to_console(x):
    enable_print()
    print(x)
    disable_print()