from utils import *
from printing_steps import *

path = os.getcwd()

def read_vbm_excel():
    # Read VBM turfs to be printed from excel file
    fname = r"..\io\Input\Nov 2020 Tracking Non voters .xlsx"
    df = pd.read_excel(fname, sheet_name="Print Reports")
    return df

def get_vbm_turfs(df):
    turfs = []
    count = 0
    for turf in df['Name in VAN'].values:
        building = df['suffix'].values[count]
        print_type = df['Label/List'].values[count]
        turfs.append((turf, building, print_type))
        count += 1
    return turfs

def print_labels(driver, list_name):
    #Click on Labels from My List page
    expect_by_id(driver, "ctl00_ContentPlaceHolderVANPage_PrintLabelsLabel").click()
    #Send Name
    element = expect_by_id(driver,
                           "ctl00_ContentPlaceHolderVANPage_VANDetailsItemReportTitle_VANInputItemDetailsItemReportTitle_ReportTitle")
    element.clear()
    element.send_keys(list_name)
    #Select format
    select_element = Select(expect_by_id(driver,
                                         "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReportFormatInfo_VANInputItemDetailsItemReportFormatInfo_ReportFormatInfo"))
    select_element.select_by_visible_text("New Standard Mailing Labels (Avery 5160)")
    select_element = Select(expect_by_id(driver,
                                         "ctl00_ContentPlaceHolderVANPage_VanDetailsItemHouseholding_VANInputItemDetailsItemHouseholding_Householding"))
    select_element.select_by_visible_text("Print one label per Address")
    expect_by_id(driver, "ctl00_ContentPlaceHolderVANPage_ButtonSortOptionsSubmit").click()
    expect_by_link_text(driver, "My PDF Files").click()


if __name__ == '__main__':
    # teardown()
    driver = start_driver()
    get_page(driver)
    driver.implicitly_wait(10)
    login_to_page(driver)
    list_folders(driver)
    select_folder(driver)

    driver.implicitly_wait(30)
    print_labels(driver, "Test1")

    # data = read_vbm_excel()
    # turfs = get_vbm_turfs(data)
    #
    # for turf in turfs:
    #     turf_name = turf[0]
    #     print_list_name = turf[0] + " " + turf[1]
    #     select_turf(driver, turf_name)
    #     handle_alert(driver)
    #     print_controller(driver, print_list_name)
    #     driver.implicitly_wait(30)
    #     return_to_folder(driver)
    #     driver.implicitly_wait(30)