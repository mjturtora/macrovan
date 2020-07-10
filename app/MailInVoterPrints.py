from utils import *
#import utils

path = os.getcwd()
print(f"The current working directory is {path}")

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


if __name__ == '__main__':

    driver = start_driver()
    get_page(driver)
    driver.implicitly_wait(10)
    login_to_page(driver)
    list_folders(driver)
    select_folder(driver)

    test_dict = {
        ("Barbara", "Law"): [("P 144 Turf 02", "Prendergast"),  ("P 602 Turf 02", "Baker"), ("P138Hunter", "Hunter"),
    ("P 150 Turf 02", "Thurmond"), ("P 156 Turf 02", "Fling"), ('P 121Pincus', 'Pincus'), ('P 150 Turf 03','Davis'),
    ('P 155Tur', 'Tur'), ('P155Tur2', 'Tur')],

        ("Andy", "Bragg"): [("P130 Upper Downtown Turf 07", "O'Connor"), ("P130 Upper Downtown Turf 08", "Gardner"), ("P130 Upper Downtown Turf 09", "Warren"),
    ("P130 Upper Downtown Turf 10", "Strickler"), ("P130 Upper Downtown Turf 11", "Roux"), ("P130 Upper Downtown Turf 12", "Taylor"),
    ("P130 Upper Downtown Turf 13", "Grebenschikoff"), ("P130 Upper Downtown Turf 14", "Singer")]
    }

    captains = getAllCaptains(test_dict)

    """
    Remaining problems:
    note field
    print icon click fail
    anyone who requested (so early voting twisty i think)
    """

    for captain in captains:
        turfs = getTurfsByCaptain(captain, test_dict)
        captain_name = captain[1] + ", " + captain[0]
        for turf in turfs:
            turf_name = turf[0]
            list_name = turf[0] + " " + turf[1]
            turfselection_plus(driver, turf_name, captain_name)
            print_list(driver, list_name)
            driver.implicitly_wait(30)
            return_to_folder(driver)
            driver.implicitly_wait(30)
            # pause("Click Ok to continue")

            #Select Print Format Option??