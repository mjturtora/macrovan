"""
Working file. Does not work :(
Testing whether selenium resume after windows pop-up (MessageBox) works... Seems to. :)

"""

from secrets import *
from app.utils import *
# import ctypes  # An included library with Python install.
#
# def pause(message):
#     ctypes.windll.user32.MessageBoxW(0, message, "Macrovan", 1)


def turfselection_plus(driver, turf_name):
    # ORIGINAL (SIDE) Test name: from turf selection

    # SELECT OWNER (PRECINCT CAPTAIN) NAME
    # On Folder page, click "owner" text entry field
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_viiFilterOwner_rac_viiFilterOwner_Input").click()
    # 9 | type | id=ctl00_ContentPlaceHolderVANPage_viiFilterOwner_rac_viiFilterOwner_Input | Law, Barbara
    # Select Owners... (will need to cycle through list in outer loop)
    # might want a try/except block here for owner not found:
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_viiFilterOwner_rac_viiFilterOwner_Input").send_keys("Law, Barbara")
    # 10 | click | id=ctl00_ContentPlaceHolderVANPage_RefreshFilterButton (runs owner selection)
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_RefreshFilterButton").click()

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
    # some wait needed for page to load...
    wait_no_longer_than = 10
    # to click Early Voting Twisty
    element = WebDriverWait(driver, wait_no_longer_than).until(
                EC.presence_of_element_located((By.ID, 'ImageButtonSectionEarlyVoting')))
    print(f'Early Voting Section element located = {element}')
    driver.find_element(By.ID, "ImageButtonSectionEarlyVoting").click()
    print('Click anyone Who Requested a Ballot')
    driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_EarlyVoteCheckboxId_RequestReceived").click()
    print('Click Preview Button')
    driver.find_element_by_id("ResultsPreviewButton").click()
    print("Driver title is: \n", driver.title)
    print('Click #AddNewStepButton')
    pause('Click Add New Step: Remove, and wait\n for page to load to continue')

    print('Try to click "Notes" twisty')
    driver.find_element_by_xpath('//*[@id="ImageButtonSectionNotes"]').click()
    print('Click in note text field. Is this needed?')
    driver.find_element(By.ID, "NoteText").click()
    print('Send keys to NoteText "*moved')
    driver.find_element(By.ID, "NoteText").send_keys("*moved")
    print(f'Sent keys *moved for remove step')

    # # This worked for notes before:
    # element = driver.find_element_by_id("ImageButtonSectionNotes").click()
    # print('Find NoteText')
    # element = driver.find_element_by_id('NoteText')
    # print('Send Keys: Voted')
    # element.send_keys('Voted')


    # Run Search
    # print('Run Search ?')
    # driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolderVANPage_SearchRunButton > span:nth-child(2)").click()
    print('Run Search to Remove selected voters (Click Run Search Button)')
    element = driver.find_element_by_id("ctl00_ContentPlaceHolderVANPage_SearchRunButton").click()

    print("Driver title is: \n", driver.title)
    print("And done with SIDE function")



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


    turf_name = 'P 138 Turf 01'
    print(f'Call Turf Selection from main')
    turfselection_plus(driver, turf_name)


    print(' Back in Main from turf selection Click Preview Button')
    # element = driver.find_element_by_id("ResultsPreviewButton").click()
    # print("Driver title is: \n", driver.title)

    listName = 'huh'
    print_list(driver, listName)

    # select_turf(driver, turf_name)
    # handle_alert(driver)
    # print_title(driver)
    # edit_search(driver)
    # print_title(driver)

