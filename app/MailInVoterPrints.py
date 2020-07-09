"""
Working file. Does not work :(
Testing whether selenium resume after windows pop-up (MessageBox) works... Seems to. :)

"""

from secrets import *
from app.utils import *
import ctypes  # An included library with Python install.

def pause():
    ctypes.windll.user32.MessageBoxW(0, "Click Ok to Finish", "Macrovan", 1)


def test_fromturfselection(driver):
    # ORIGINAL Test name: from turf selection
    # 2 | setWindowSize | 810x682 |
    #driver.set_window_size(810, 682)
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_viiFilterOwner_rac_viiFilterOwner_Input").click()
    # 9 | type | id=ctl00_ContentPlaceHolderVANPage_viiFilterOwner_rac_viiFilterOwner_Input | Law, Barbara
    # Select Owners...
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_viiFilterOwner_rac_viiFilterOwner_Input").send_keys("Law, Barbara")
    # 10 | click | id=ctl00_ContentPlaceHolderVANPage_RefreshFilterButton | 
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_RefreshFilterButton").click()
    # 11 | click | css=tr:nth-child(1) > td:nth-child(4) .grid-result | 
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(4) .grid-result").click()
    handle_alert(driver)

    # # 12 | assertConfirmation | Are you sure you want to load this Map Turf and overwrite your current version of My List? |
    # assert driver.switch_to.alert.text == "Are you sure you want to load this Map Turf and overwrite your current version of My List?"
    # # 13 | webdriverChooseOkOnVisibleConfirmation |  |
    # # gets list to edit
    # driver.switch_to.alert.accept()

    # 14 | click | id=addStep |
    # Edit Search
    driver.find_element(By.ID, "addStep").click()
    # 15 | click | id=stepTypeItem4 | 
    # Narrow People
    driver.find_element(By.ID, "stepTypeItem4").click()
    # 16 | click | id=ImageButtonSectionEarlyVoting | 
    # Early Voting Twisty

    wait_no_longer_than = 10
    element = WebDriverWait(driver, wait_no_longer_than).until(
                EC.presence_of_element_located((By.ID, 'ImageButtonSectionEarlyVoting')))
    print(f'Early Voting Section element located = {element}')

    driver.find_element(By.ID, "ImageButtonSectionEarlyVoting").click()
    # 17 | click | id=ctl00_ContentPlaceHolderVANPage_EarlyVoteCheckboxId_RequestReceived | 
    print('Anyone Who Requested a Ballot')
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_EarlyVoteCheckboxId_RequestReceived").click()

    # 18 | click | css=#ResultsPreviewButton > span:nth-child(2) |
    # Click Preview My results
    # driver.find_element(By.CSS_SELECTOR, "#ResultsPreviewButton > span:nth-child(2)").click()

    print('Click Preview Button')
    driver.find_element_by_id("ResultsPreviewButton").click()
    print("Driver title is: \n", driver.title)


    # 19 | click | css=#AddNewStepButton > span:nth-child(2) |
    #driver.find_element(By.CSS_SELECTOR, "#AddNewStepButton > span:nth-child(2)").click()

    #print('Waiting for invisibility')
    #WebDriverWait(driver, wait_no_longer_than).until(EC.invisibility_of_element_located(By.XPATH('//*[@id="ctl00_BodyTag"]/div[2]')))
    #print('Waiting before Add Step')
    #driver.implicitly_wait(25)
    print('Click #AddNewStepButton')
    pause()
    #driver.find_element(By.CSS_SELECTOR, "#AddNewStepButton").click()
    #driver.find_element_by_xpath('//*[@id="AddNewStepButton"]').click()

    #driver.find_element(By.ID, "AddNewStepButton").click()
    # gets error: selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <button id="AddNewStepButton" type="button" class="AddNewStep btn-full" ng-click="addStepClickHandler()" ng-class="{'AddStepActive' : showAddNewStepTypes }">...</button> is not clickable at point (850, 466). Other element would receive the click: <div class="loading-overlay" style="visibility: visible;"></div>
    # 20 | click | css=.ng-scope:nth-child(2) > .ng-binding |
    # Remove People
    #driver.find_element(By.CSS_SELECTOR, ".ng-scope:nth-child(2) > .ng-binding").click()

    # If wait too long? get:
    #selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: element is not attached to the page document

    # 21 | click | id=NoteText | 
    driver.find_element(By.ID, "NoteText").click()
    # 22 | type | id=NoteText | *moved
    driver.find_element(By.ID, "NoteText").send_keys("*moved")
    # 23 | click | css=#ctl00_ContentPlaceHolderVANPage_SearchRunButton > span:nth-child(2) | 
    # Run Search
    driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolderVANPage_SearchRunButton > span:nth-child(2)").click()


if __name__ == '__main__':

    driver = start_driver()
    get_page(driver)
    driver.implicitly_wait(10)
    login_to_page(driver)
    # Restart from here works!
    # print('Click to Restart')
    # pause()
    list_folders(driver)
    # # Then speed up (but tighten this up with EC WAITS
    # driver.implicitly_wait(10)
    select_folder(driver)
    #
    # # Need to begin loop here to cycle through all turfs

    # turf_name = 'P123 Turf 04'
    #turfs = [('P 138 Turf 01')]

    test_fromturfselection(driver)

    #After filtering and searching, back on the list page
    turf_name = '';   #Whatever we want the name for the list to be
    print_list(driver, turf_name)


    print('Click Preview Button')
    element = driver.find_element_by_id("ResultsPreviewButton").click()
    print("Driver title is: \n", driver.title)


    # select_turf(driver, turf_name)
    # handle_alert(driver)
    # print_title(driver)
    # edit_search(driver)
    # print_title(driver)

